import os
import fitz  # PyMuPDF

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
