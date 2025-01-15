import os
import re
import shutil
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PyPDF2 import PdfReader
from docx import Document

# Function to extract reference code using regex
def extract_reference_code(text, pattern):
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
def move_file_to_reference_folder(file_path, reference_code, base_folder):
    safe_reference_code = reference_code.replace("/", "_")
    folder_path = os.path.join(base_folder, safe_reference_code)
    os.makedirs(folder_path, exist_ok=True)
    new_file_path = os.path.join(folder_path, os.path.basename(file_path))
    shutil.move(file_path, new_file_path)
    print(f"Moved file: {file_path} to {new_file_path}")

# Function to process files
def process_files(file_paths, pattern, base_folder):
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
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
        reference_code = extract_reference_code(text, pattern)
        if reference_code:
            print(f"Found reference code: {reference_code} in file: {file_name}")
            move_file_to_reference_folder(file_path, reference_code, base_folder)
        else:
            print(f"No reference code found in file: {file_name}")

# Tkinter GUI
def main():
    def select_files():
        global file_paths
        file_paths = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf"), ("Word Documents", "*.docx"), ("Text Files", "*.txt")]
        )
        if file_paths:
            selected_files_label.config(text=f"{len(file_paths)} files selected.")

    def select_folder():
        global base_folder
        base_folder = filedialog.askdirectory(title="Select Endpoint Folder")
        if base_folder:
            folder_label.config(text=f"Destination: {base_folder}")

    def process():
        pattern = pattern_entry.get()
        if not pattern:
            messagebox.showerror("Error", "Please enter a regex pattern.")
            return
        if not file_paths or not base_folder:
            messagebox.showerror("Error", "Please select files and a destination folder.")
            return
        process_files(file_paths, pattern, base_folder)
        messagebox.showinfo("Success", "Files processed successfully!")

    # Initialize Tkinter
    root = Tk()
    root.title("File Processing Interface")
    root.geometry("500x300")

    # Widgets
    Label(root, text="Step 1: Select Files").pack(pady=5)
    Button(root, text="Choose Files", command=select_files).pack()
    selected_files_label = Label(root, text="No files selected.")
    selected_files_label.pack()

    Label(root, text="Step 2: Enter Regex Pattern").pack(pady=5)
    pattern_entry = Entry(root, width=40)
    pattern_entry.pack()

    Label(root, text="Step 3: Select Destination Folder").pack(pady=5)
    Button(root, text="Choose Folder", command=select_folder).pack()
    folder_label = Label(root, text="No folder selected.")
    folder_label.pack()

    Button(root, text="Process Files", command=process, bg="green", fg="white").pack(pady=20)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()