# AI Document Intelligence MVP

This is a simple Streamlit web application that lets users upload a PDF or image, reads the text, identifies if it is an Invoice or a Resume, and extracts simple details.

## How to Run
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure you have Tesseract OCR installed on your system if you want to read text from images.
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Features
- **Upload:** Supports PDF, JPG, PNG.
- **Read Text:** Uses PyMuPDF for PDFs and PyTesseract for images.
- **Identify Type:** Identifies "Invoice" and "Resume" based on simple keywords.
- **Extract Fields:** Extracts Invoice Number, Date, Company, Total for Invoices, and Name, Email, Phone, Skills for Resumes using Regular Expressions.
