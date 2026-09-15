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
        
        # Step 4: Extract Simple Information
        st.subheader("Extracted Details")
        details = {}
        
        if doc_type == "Invoice":
            # Very simple regular expressions for MVP
            inv_num = re.search(r'Invoice Number[:\s]*(INV-\d+|\d+)', text, re.IGNORECASE)
            date = re.search(r'Date[:\s]*(\d{2}-\d{2}-\d{4}|\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
            total = re.search(r'Total[:\s]*([A-Z]*\s*\d+[,\.]?\d*)', text, re.IGNORECASE)
            
            # Simple assumption: Company name is the first line
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            company_name = lines[0] if lines else "Not Found"
            
            details["Invoice Number"] = inv_num.group(1) if inv_num else "Not Found"
            details["Date"] = date.group(1) if date else "Not Found"
            details["Company"] = company_name
            details["Total Amount"] = total.group(1) if total else "Not Found"
            
        elif doc_type == "Resume":
            email = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
            phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
            
            # Simple assumption: Name is the first line
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            name = lines[0] if lines else "Not Found"
            
            details["Name"] = name
            details["Email"] = email.group(0) if email else "Not Found"
            details["Phone"] = phone.group(0) if phone else "Not Found"
            details["Skills"] = "Python, Streamlit, Machine Learning" # Mocking this for simplicity, can get complex!
            
        else:
            st.write("We do not support extracting details from this type yet.")
            
        # Step 5: Show the Result
        if details:
            for key, value in details.items():
                st.write(f"**{key}:** {value}")
        
        # We are done!

if __name__ == "__main__":
    main()
