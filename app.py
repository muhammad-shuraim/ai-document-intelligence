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
        
        # Step 2: Read the Text
        text = ""
        with st.spinner("Reading text from document..."):
            if uploaded_file.type == "application/pdf":
                try:
                    pdf_bytes = uploaded_file.read()
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    for page in doc:
                        text += page.get_text()
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
            else:
                try:
                    image = Image.open(uploaded_file)
                    text = pytesseract.image_to_string(image)
                except Exception as e:
                    st.error(f"Error reading Image: {e}")
        
        st.subheader("Extracted Text Snippet")
        st.text(text[:300] + "..." if len(text) > 300 else text)
        
        # Step 3: Simple Document Type Classification
        doc_type = "Other"
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["invoice", "total", "invoice number"]):
            doc_type = "Invoice"
        elif any(word in text_lower for word in ["resume", "skills", "education", "experience"]):
            doc_type = "Resume"
            
        st.subheader("Document Type")
        st.info(f"We identified this document as: **{doc_type}**")
        
        # We will add next steps here!

if __name__ == "__main__":
    main()
