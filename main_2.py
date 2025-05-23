import pytesseract
from pdf2image import convert_from_path
from typing import List, Dict, Any
import re
import json
import logging

def extract_text_via_ocr(pdf_path: str):
    """Extract text using Tesseract OCR"""
    images = convert_from_path(pdf_path)
    text = "\n".join([pytesseract.image_to_string(img) for img in images])
    return text

# function that manage the comma and dot separator in the price value becuase of european format
def parse_european_number(num_str: str) -> float:
    return float(num_str.replace('.', '').replace(',', '.'))

# parsing the text
def parse_text(text: str) -> List[Dict[str, Any]]:
    products = []

    # split into product blocks
    product_blocks = re.split(r'\n(?=CPH\d+)', text.strip())

    for block in product_blocks:
        if not block.strip():
            continue

        # extract product id and name 
        match_id = re.match(r'(CPH\d+)\s+(.+?)(?=\[|\n|$])', block)
        if not match_id:
            logging.warning("ID not match.")
            continue

        product_id = match_id.group(1)
        product_name = match_id.group(2).strip()

        # extract sizes and quantities
        size_quanities = {}
        for size_match in re.finditer(r'\[(\d+)\]:\s*(\d+)\s*p[ce]', block):
            size = size_match.group(1)
            quantity = int(size_match.group(2))
            size_quanities[size] = quantity

        # extract retail price (vk)
        vk_match = re.search(r'retail price\s+([\d.,]+)\s*€', block)
        retail_price = parse_european_number(vk_match.group(1)) if vk_match else None

        # extract cost price(ek)
        ek_match = re.search(rf'{re.escape(product_id)}(?:.|\n)*?EK[\s:]*([\d.,]+)\s*€', text, re.IGNORECASE | re.DOTALL) 
        cost_price = parse_european_number(ek_match.group(1)) if ek_match else None

        #find material and colour
        name_words = product_name.split()
        material = ""
        colour = ""

        material_keywords = {'leather', 'hairy', 'vintage', 'nubuck'}
        colour_keywords = {'cream', 'brown', 'black', 'white', 'blue'}

        for word in reversed(name_words):
            if word.lower() in material_keywords:
                material = word
                break
        
        for word in reversed(name_words):
            if word.lower() in colour_keywords:
                colour = word
                break
        
        # if there is no colour then use last word as reference to maintain the emptiness
        if not colour and name_words:
            colour = name_words[-1]
        
        products.append({
            "name": product_name,
            "id": product_id,
            "brand": "Copenhagen",
            "colours": [{
                "name": colour,
                "sizes": [{
                    "name": size,
                    "quantity": qty 
                } for size, qty in size_quanities.items()]
            }],
            "material": material,
            "total_quantity": sum(size_quanities.values()),
            "unit_price": cost_price,
            "total_cost": round(cost_price * sum(size_quanities.values()), 2) if cost_price else None,
            "retail_price": retail_price,
            "discount": 0.0 # Not mentioned in data file
        })

    return products

if __name__ == "__main__":
    pdf_path = "/Users/ankushbhatt/Desktop/Challenge/Copenhagen_Challenge.pdf"
    pdf_text = extract_text_via_ocr(pdf_path)
    products = parse_text(pdf_text)

    with open("copenhagen_products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    logging.info("JSON file written successfully.")
