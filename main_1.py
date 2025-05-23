import pdfplumber
import re
from typing import List, Dict, Any
import json
import logging

# Extract text from pdf
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# create a function that manage the comma and dot in price value because of european format(price)
def parse_european_number(num_str: str) -> float:
    # Remove thousands separator (.) and replace decimal comma with dot
    return float(num_str.replace('.', '').replace(',', '.'))


# Parsing the text
def parse_autry_text(text: str) -> List[Dict[str, Any]]:
    products = []

    # splitting the each products into product blocks
    product_blocks = re.split(r'\n([A-Z]{3,4} - [A-Z0-9]{2,4})', text)[1:]

    for i in range(0, len(product_blocks), 2):
        product_id = product_blocks[i].strip()
        product_content = product_blocks[i+1]
        logging.info(f"Product ID: {product_id}")

        
        # extract product name 
        match_name = re.search(r'^(.+?)\s+\d+', product_content, re.MULTILINE)
        if not match_name:
            logging.warning("No product name found.")
            continue
        product_name = match_name.group(1).strip()

        # extract price for each product(quantity, unit price, total price)
        match_price = re.search(r'(\d+)\s+([\d.,]+)\s*€\s+([\d.,]+)\s*€', product_content)
        if not match_price:
            logging.warning("Price regex did not match.")
            continue      

        # extract the all sizes and their quantities 
        sizes = {}

        # break the product_content into lines
        lines =  product_content.split('\n')

        # extract only numeric characters
        numeric_lines = [line.strip() for line in lines if re.fullmatch(r'[\d\s]+', line)]

        # concatenate numeric lines and convert to list of lists of integers
        numbers_per_line = [list(map(int, line.split())) for line in numeric_lines]

        if len(numbers_per_line) >= 2:
            size_labels = list(map(str, numbers_per_line[0] + numbers_per_line[2]))  # first and third line as labels
            size_quantities = numbers_per_line[1] + numbers_per_line[3]  # second and fourth line as quantities

            sizes = {size: qty for size, qty in zip(size_labels, size_quantities) if qty > 0}

        # extract colour / material from product name 
        colour_material = product_name.split('-')[-1].strip() if '-' in product_name else ''
        parts = colour_material.split(' ', 1)
        material = parts[0]
        colour =  parts[1] if len(parts) > 1 else ""

        products.append({
            "name": product_name,
            "id": product_id,
            "brand": "Autry",
            "colours": [{
                "name": colour,
                "sizes": [{
                    "name": size, 
                    "quantity": qty} for size, qty in sizes.items()]
            }],
            "material": material,
            "total_quantity": int(match_price.group(1)),
            "unit_price": parse_european_number(match_price.group(2)),
            "total_cost": parse_european_number(match_price.group(3)),
            "discount": 0.0 # Not mentioned in data file
        })

    return products
        
if __name__ == "__main__":
    pdf_path = "/Users/ankushbhatt/Desktop/Challenge/Autry_Challenge_.pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    products = parse_autry_text(pdf_text)

    with open("autry_products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    logging.info("JSON file written successfully.")
