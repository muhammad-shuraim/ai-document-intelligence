import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import io

def main():
    st.title("AI Document Intelligence MVP")
    st.write("Upload an Invoice or Resume (PDF, JPG, PNG) and we will extract the information for you!")

    # Step 1: Upload a Document
    uploaded_file = st.file_uploader("Choose a document...", type=["pdf", "jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.success(f"Successfully uploaded: {uploaded_file.name}")
        st.write(f"File type: {uploaded_file.type}")
        
        # We will add next steps here!

if __name__ == "__main__":
    main()
