import os
import fitz  # PyMuPDF
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

def read_datasheet_contents(folder_path='./Data/Datasheet'):
    pdf_contents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith('.pdf'):
            try:
                with fitz.open(file_path) as pdf_document:
                    content = ""
                    for page_num in range(pdf_document.page_count):
                        page = pdf_document.load_page(page_num)
                        content += page.get_text()
                    pdf_contents.append(content)
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")
    return pdf_contents

def read_excel_page(folder_path='./Data/Test', sheet_number=0):
    df = None
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith('.xlsx'):
            try:
                # Load the entire sheet to find the first non-empty row
                temp_df = pd.read_excel(file_path, sheet_name=sheet_number, header=None)
                # Find the first non-empty row
                header_row = temp_df.apply(lambda row: row.notna().any(), axis=1).idxmax()
                # Read the Excel file again using the detected header row
                df = pd.read_excel(file_path, sheet_name=sheet_number, header=header_row)
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")
    return df


def create_price_architecture_report(data_str, output_format='pdf', output_path='./Data/Report'):
    data = json.loads(data_str)
    file_path = None
    name = 'test'
    df = pd.DataFrame(data)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if output_format == 'excel':
        file_path = os.path.join(output_path, f'{name}_report.xlsx')
        df.to_excel(file_path, index=False)
    elif output_format == 'pdf':
        file_path = os.path.join(output_path, f'{name}_report.pdf')
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        y_position = height - 100
        for index, row in df.iterrows():
            if y_position < 100:  # Start a new page if space is insufficient
                c.showPage()
                y_position = height - 100
            reference = row.get("Reference", "")
            designation = row.get("Designation", "")
            article_number = row.get("Article_number", "")
            quantity = row.get("Quantity", "")
            price = row.get("Price", "")
            c.drawString(100, y_position, f"Reference: {reference}")
            y_position -= 20
            c.drawString(100, y_position, f"Designation: {designation}")
            y_position -= 20
            c.drawString(100, y_position, f"Article number: {article_number}")
            y_position -= 20
            c.drawString(100, y_position, f"Quantity: {quantity}")
            y_position -= 20
            c.drawString(100, y_position, f"Price: {price}")
            y_position -= 40  # Add extra space between entries
        c.save()
    else:
        raise ValueError("Unsupported format. Use 'pdf' or 'excel'.")
    return file_path
