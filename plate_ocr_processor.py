import cv2
import os
import json
from google.cloud import vision
import numpy as np

# Set path ke kredensial Google Vision API

# TODO: change path to credentials.json location
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\\Example\\credentials.json"

# Fungsi untuk membaca gambar dan melakukan preprocessing (Otsu Thresholding)
def adaptive_filtering_otsu(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Gambar '{image_path}' tidak ditemukan.")
    _, otsu_thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return otsu_thresh

# Fungsi untuk OCR menggunakan Google Vision API
def perform_ocr(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description.strip()
    return ""

# Fungsi untuk menghitung akurasi OCR berdasarkan string referensi
def calculate_accuracy(ocr_text, ground_truth):
    if not ocr_text or not ground_truth:
        return 0.0
    ocr_text = ocr_text.replace(" ", "").upper()
    ground_truth = ground_truth.replace(" ", "").upper()
    matches = sum(1 for o, g in zip(ocr_text, ground_truth) if o == g)
    return (matches / max(len(ocr_text), len(ground_truth))) * 100

# Fungsi untuk normalisasi gambar (ubah latar belakang menjadi putih dan teks menjadi hitam)
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Gambar '{image_path}' tidak ditemukan.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Hitung jumlah piksel hitam dan putih
    black_pixels = np.sum(binary == 0)
    white_pixels = np.sum(binary == 255)

    # Jika latar belakang dominan hitam, invert warna
    if black_pixels > white_pixels:
        binary = cv2.bitwise_not(binary)

    return binary

# Fungsi untuk memproses semua gambar
def process_images(image_folder, ground_truth_file):
    # Membaca ground truth dari file teks
    with open(ground_truth_file, 'r') as file:
        ground_truths = json.load(file)  # Format: {"gambar1.jpg": "B 1234 ABC", ...}

    # Pastikan folder untuk hasil preprocessing ada
    results_image_folder = "resultsImage"
    if not os.path.exists(results_image_folder):
        os.makedirs(results_image_folder)

    results = []

    for image_name, ground_truth in ground_truths.items():
        image_path = os.path.join(image_folder, image_name)
        if not os.path.exists(image_path):
            print(f"File gambar '{image_name}' tidak ditemukan, dilewatkan.")
            continue

        print(f"Memproses {image_name}...")

        # OCR tanpa filtering
        ocr_original_raw = perform_ocr(image_path)
        ocr_original = ocr_original_raw[:10]  # Ambil 10 karakter pertama dari hasil OCR
        accuracy_original = calculate_accuracy(ocr_original, ground_truth)

        # Terapkan preprocessing
        preprocessed_image = preprocess_image(image_path)
        preprocessed_path = os.path.join(results_image_folder, f"preprocessed_{image_name}")
        cv2.imwrite(preprocessed_path, preprocessed_image)

        # OCR setelah preprocessing
        ocr_filtered_raw = perform_ocr(preprocessed_path)
        ocr_filtered = ocr_filtered_raw[:10]  # Ambil 10 karakter pertama dari hasil OCR
        accuracy_filtered = calculate_accuracy(ocr_filtered, ground_truth)

        # Tentukan status hasil filtering
        if accuracy_filtered > accuracy_original:
            status = "meningkat"
        elif accuracy_filtered < accuracy_original:
            status = "menurun"
        else:
            status = "tetap"

        # Simpan hasil
        result = {
            "image_name": image_name,
            "ground_truth": ground_truth,
            "ocr_original": ocr_original,
            "accuracy_original": accuracy_original,
            "ocr_filtered": ocr_filtered,
            "accuracy_filtered": accuracy_filtered,
            "filtering_status": status
        }
        results.append(result)

        # Tampilkan hasil
        print(f"  Hasil OCR Tanpa Filtering: {ocr_original}")
        print(f"  Akurasi Tanpa Filtering: {accuracy_original:.2f}%")
        print(f"  Hasil OCR Dengan Filtering: {ocr_filtered}")
        print(f"  Akurasi Dengan Filtering: {accuracy_filtered:.2f}%")
        print(f"  Status hasil filtering: {status}")

    return results

# Main pipeline
if __name__ == "__main__":
    # Path ke folder gambar dan file ground truth
    image_folder = "images"
    ground_truth_file = "ground_truth.json"

    # Proses semua gambar
    results = process_images(image_folder, ground_truth_file)

    # Simpan hasil ke file JSON
    with open("results.json", "w") as result_file:
        json.dump(results, result_file, indent=4)
    print("Hasil telah disimpan ke 'results.json'.")
