# License Plate OCR Processor

This project provides a pipeline to process license plate images using Otsu Thresholding for preprocessing and evaluates the OCR results before and after filtering. The system outputs preprocessed images and a JSON file containing OCR performance details.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
  - [Enable Google Vision API](#1-enable-google-vision-api)
  - [Clone the Repository](#2-clone-the-repository)
  - [Install Dependencies](#3-install-dependencies)
  - [Prepare Input Data](#4-prepare-input-data)
- [Project Directory Structure](#project-directory-structure)
- [Usage](#usage)
- [Output](#output)
- [Contributors](#contributors)
- [License](#license)

## Features
- **Image Preprocessing**: Enhances input images using Otsu Thresholding.
- **Google Vision API OCR**: Reads text from images.
- **Accuracy Evaluation**: Compares OCR results with ground truth.
- **Output**:
  - Preprocessed images stored in the `resultsImage` folder.
  - Results and analysis saved as `results.json`.

## Requirements
- Python 3.7 or later
- Libraries:
  - `opencv-python`
  - `google-cloud-vision`
  - `numpy`
- Google Cloud Platform account with Vision API enabled

## Setup

### 1. Enable Google Vision API
1. Visit [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select an existing project.
3. Enable the Vision API under **API & Services > Library**.
4. Generate credentials:
   - Navigate to **API & Services > Credentials**.
   - Click **Create Credentials** > **Service Account Key**.
   - Choose a role (e.g., "Project > Editor").
   - Save the generated JSON file as `credentials.json`.

### 2. Clone the Repository
```bash
git clone https://github.com/username/license-plate-ocr.git
cd license-plate-ocr
```

### 3. Install Dependencies
```bash
pip install opencv-python google-cloud-vision numpy
```

### 4. Prepare Input Data
1. Place input images in the `images/` folder.
2. Create a `ground_truth.json` file with the following format:
   ```json
   {
       "image1.jpg": "B 1234 ABC",
       "image2.jpg": "D 5678 DEF"
   }
   ```

## Project Directory Structure
Ensure your project follows this structure:
```
project/
│
├── credentials.json       # Google Vision API credentials
├── images/                # Folder for input images
│   ├── image1.jpg
│   └── image2.jpg
├── ground_truth.json      # Ground truth reference data
├── resultsImage/          # Folder for preprocessed images (auto-created)
├── results.json           # JSON file for OCR results (auto-created)
└── plate_ocr_processor.py   # Main script
```

## Usage
Run the script to process images:
```bash
python plate_ocr_processor.py
```

## Output
1. **Preprocessed Images**: Saved in the `resultsImage/` folder.
2. **OCR Results**: Stored in `results.json` with the following format:
   ```json
   [
       {
           "image_name": "image1.jpg",
           "ground_truth": "B 1234 ABC",
           "ocr_original": "B1234ABC",
           "accuracy_original": 85.71,
           "ocr_filtered": "B1234ABC",
           "accuracy_filtered": 100.0,
           "filtering_status": "improved"
       }
   ]
   ```

## Contributors
| Name                          | NPM               |
|-------------------------------|-------------------|
| Annisa Amalia Putri           |50421172           |
| Bernadhetta Ira Tri Lita A    |50421276           |
| Ferdinand Andhika Widhiyan    |50421513           |
| Gideon Aprileo                |50421562           |
| Muhammad Farhan Fathurrohman  |50421953           |

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.