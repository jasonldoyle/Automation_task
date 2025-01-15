import os
import re
import shutil
from PyPDF2 import PdfReader
from docx import Document

# Function to extract reference code using regex
def extract_reference_code(text):
    pattern = r'\b\d{2}/\d{4}\b'  # Regex for nn/nnnn format
    match = re.search(pattern, text)
    return match.group() if match else None

# Function to extract text from a PDF file
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

# Function to extract text from a Word document
def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        text = " ".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading Word file: {e}")
        return ""

# Function to extract text from a plain text file
def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return ""

# Function to move a file into a new folder based on reference code
def move_file_to_reference_folder(file_path, reference_code, base_folder="Today's emails"):
    # Replace '/' in the reference code with a safe character, e.g., '_'
    safe_reference_code = reference_code.replace("/", "_")

    # Create the folder path
    folder_path = os.path.join(base_folder, safe_reference_code)
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    
    # Move the file into the folder
    new_file_path = os.path.join(folder_path, os.path.basename(file_path))
    shutil.move(file_path, new_file_path)
    print(f"Moved file: {file_path} to {new_file_path}")

# Function to process files in a directory
def process_files(directory_path, base_folder="Today's emails"):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"Processing file: {file_name}")
            
            # Determine file type and extract text
            if file_name.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif file_name.endswith(".docx"):
                text = extract_text_from_docx(file_path)
            elif file_name.endswith(".txt"):
                text = extract_text_from_txt(file_path)
            else:
                print(f"Unsupported file type: {file_name}")
                continue

            # Search for reference code in the extracted text
            reference_code = extract_reference_code(text)
            if reference_code:
                print(f"Found reference code: {reference_code} in file: {file_name}")
                move_file_to_reference_folder(file_path, reference_code, base_folder)
            else:
                print(f"No reference code found in file: {file_name}")

# Provide the path to the directory containing your files
directory_path = "/Users/jason/Desktop/Automation"  # The folder containing the source files
base_folder = "/Users/jason/Desktop/Automation/Today's emails"  # Full path to the 'Today's emails' folder
process_files(directory_path, base_folder)