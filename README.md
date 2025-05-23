# PDF Product Parse

This repository includes two Python scripts designed to extract product information from PDFs in different formats — one tailored for Autry products and the other for Copenhagen products.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Autry Parser](#autry-parser)
  - [Copenhagen Parser](#copenhagen-parser)
- [Output Format](#output-format)
- [Notes](#notes)

## Features

- **Autry Parser** (`main_1.py`):
  - Extracts text from digital PDFs using `pdfplumber`
  - Parses structured product information including:
    - Product ID
    - Product name
    - Sizes and quantities
    - Material and color
    - Unit price and total cost
  - Handles European price formatting (e.g., `1.234,56` → `1234.56`)

- **Copenhagen Parser** (`main_2.py`):
  - Extracts text from scanned PDFs using OCR (`pytesseract`)
  - Converts PDF pages to images using `pdf2image`
  - Extracts product data such as:
    - Name
    - Material
    - Sizes and quantities
    - Pricing and totals

## Requirements

### Common Requirements
- Python 3.6 or higher
- PIP package manager

### Autry Parser Specific
- `pdfplumber`
- `re` (standard library)
- `json` (standard library)

### Copenhagen Parser Specific
- `pytesseract`
- `pdf2image`
- `PIL` (Pillow)
- Tesseract OCR engine (must be installed separately)

### Installing Tesseract OCR (for Copenhagen Parser)

- install all requirements like pdfplumber, pdf2image, regex, pytesseract etc.

### Usage

#Autry Parse
- python main_1.py
- update your pdf path and output will be saved in json format.

#Copenhagen Parse
- python main_2.py
- update your pdf path and output will be saved in json format.

### Output format

- "products": [
  {
    "name": "",
    "id": "",
    "brand": "",
    "colors": [
      {
        "name": "",
        "sizes": [
          {
            "name": "",
            "quantity": 0
          }
        ]
      }
    ],
    "material": "",
    "total_quantity": 0,
    "unit_price": 0.0,
    "total_cost": 0.0,
    "discount": 0.0
  }
]

### Notes

- main_1.py is for machine-readable PDFs; main_2.py is for scanned or encoded PDFs where OCR (e.g., Tesseract) is required instead of tools like pdfplumber.
- Handles European number formats like 1.234,56 correctly.
- Update pdf_path in each script to point to your input file.
- Output is saved in a structured json file.
- Parsing logic can be adapted for similar product PDF formats.
