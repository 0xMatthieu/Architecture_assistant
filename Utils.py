import os
import fitz  # PyMuPDF
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

def read_first_page_excel(folder_path='./Data/Price'):
    excel_contents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith('.xlsx'):
            try:
                df = pd.read_excel(file_path, sheet_name=0)
                excel_contents.append(df)
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")
    return excel_contents

def create_price_architecture_report(data, output_format='pdf', output_path='./Data/Report'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    df = pd.DataFrame(data)

    if output_format == 'excel':
        file_path = os.path.join(output_path, 'price_architecture_report.xlsx')
        df.to_excel(file_path, index=False)
    elif output_format == 'pdf':
        file_path = os.path.join(output_path, 'price_architecture_report.pdf')
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, "Price and Architecture Report")
        for i, (ref, price, arch) in enumerate(zip(data['Reference'], data['Price'], data['Architecture'])):
            c.drawString(100, height - 150 - i * 20, f"{ref}: {price} - {arch}")
        c.save()
    else:
        raise ValueError("Unsupported format. Use 'pdf' or 'excel'.")
    return file_path
