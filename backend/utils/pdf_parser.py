# pdf_parser.py - Extracts plain text from a PDF resume
# PyPDF2 is a free library that reads PDF files

import PyPDF2
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Takes a PDF file as bytes and returns all the text inside it.
    
    Example: A resume PDF → "John Doe, Software Engineer, Skills: Python, Java..."
    """
    try:
        # Create a PDF reader object from the file bytes
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        
        full_text = ""
        
        # Loop through every page in the PDF and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            full_text += page.extract_text() + "\n"
        
        return full_text.strip()
    
    except Exception as e:
        return f"Error reading PDF: {str(e)}"