import os
import re
import shutil
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PyPDF2 import PdfReader
from docx import Document

# Function 1 - Find the reference 
def extract_reference_code(text):
    pattern = r'\b\d{2}/\d{4}\b'  # Regex for nn/nnnn format
    match = re.search(pattern, text)
    return match.group() if match else None

# Funtion 2.1 - PDF extractor
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
    
# Function 2.2 Word doc extractor
def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        text = " ".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading Word file: {e}")
        return ""

# Function 2.3 Text File Extractor
def extract_text_from_text(text_path):
    try:
        with open(text_path, 'r', 'utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return ""

# Funtion to sort files into their own folder
def move_file_to_new_folder(file_path, reference_code, base_folder):
    # / Can mess up the folder reading
    safe_reference_code = reference_code.replace("/", "_")
    # Creating the new folder 
    folder_path = os.path.join(base_folder, safe_reference_code)
    os.makedirs(folder_path, exist_ok=True)
    # Giving the file directions
    new_file_path = os.path.join(folder_path, os.path.basename(file_path))
    # Move file to new path
    shutil.move(file_path, new_file_path)
    print(f"Moved file from {file_path} to {new_file_path}")

