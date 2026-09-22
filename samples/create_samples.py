import os
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

os.makedirs("samples", exist_ok=True)

# 1. Invoice 1 (Complete PDF)
doc1 = fitz.open()
page1 = doc1.new_page(width=595, height=842)
text_inv1 = """
NEXUS TECH SOLUTIONS INC.
450 Innovation Parkway, Suite 300, San Jose, CA 95134
Email: billing@nexustech.io | Phone: (408) 555-0182

INVOICE
--------------------------------------------------------------------------------
Invoice Number: INV-2026-9042
Date: 15-09-2026
Due Date: 15-10-2026
Billed To: CloudWave Global Services

Description                             Qty      Rate        Amount
--------------------------------------------------------------------------------
Enterprise API Platform Subscription     1     $3,200.00   $3,200.00
Cloud Integration & Setup Consultation   10       $150.00   $1,500.00
Dedicated Support Package (Monthly)       1       $500.00     $500.00
--------------------------------------------------------------------------------
Subtotal:                                                   $5,200.00
Tax (8.25%):                                                  $429.00
Total Amount:                                               $5,629.00

Payment Terms: Net 30 days. Remit payment to Silicon Valley Bank.
Thank you for choosing Nexus Tech!
"""
page1.insert_text((50, 60), text_inv1, fontsize=11, fontname="courier")
doc1.save("samples/invoice_complete.pdf")
doc1.close()

# 2. Invoice 2 (Missing total amount - to test Step 8 graceful handling)
doc2 = fitz.open()
page2 = doc2.new_page(width=595, height=842)
text_inv2 = """
AURORA LOGISTICS LTD
Freight & Cargo Forwarding

COMMERCIAL PRO-FORMA BILL
Bill No: AUR-5510
Date: 04-09-2026
Customer: Pacific Export Group

Goods description: Precision optical instruments (3 crates).
Shipping destination: Rotterdam Port.
Customs Clearance: Pending inspection.

Note: Pricing subject to final customs tariff calculation.
Total Amount: PENDING FINAL WEIGHING
"""
page2.insert_text((50, 60), text_inv2, fontsize=11, fontname="courier")
doc2.save("samples/invoice_missing_fields.pdf")
doc2.close()

# 3. Resume 1 (Complete Software Engineer PDF)
doc3 = fitz.open()
page3 = doc3.new_page(width=595, height=842)
text_res1 = """
Alexander Morgan
alexander.morgan@devmail.io | +1 (415) 555-8392 | San Francisco, CA
GitHub: github.com/alexandermorgan | LinkedIn: linkedin.com/in/alexm

PROFESSIONAL SUMMARY
Senior Full-Stack & Machine Learning Software Engineer with 7+ years of experience designing high-scale web platforms and deploying NLP and deep learning systems.

WORK EXPERIENCE
AlphaAI Technologies - Senior AI Engineer (2022 - Present)
• Architected document intelligence and computer vision workflows using PyTorch and OpenCV.
• Scaled Python FastAPI microservices serving 15,000 requests per minute with Docker & Kubernetes.
• Mentored junior engineers and led Scrum sprint planning.

Starlight Systems - Software Developer (2019 - 2022)
• Developed interactive frontend web applications using React, TypeScript, and Tailwind.
• Implemented automated CI/CD pipelines with GitHub Actions and AWS EC2/S3.

TECHNICAL SKILLS
Languages: Python, TypeScript, JavaScript, SQL, C++, Bash
Frameworks: React, FastAPI, Django, Flask, PyTorch, Scikit-Learn
Cloud & Tools: AWS, Docker, Kubernetes, Git, Linux, PostgreSQL, Redis, OpenCV

EDUCATION
B.S. in Computer Science & Applied Mathematics, UC Berkeley (2015 - 2019)
"""
page3.insert_text((50, 60), text_res1, fontsize=10, fontname="courier")
doc3.save("samples/resume_complete.pdf")
doc3.close()

# 4. Resume 2 (Missing phone number - tests Step 8)
doc4 = fitz.open()
page4 = doc4.new_page(width=595, height=842)
text_res2 = """
Kavita Patel
Email: kavita.patel@datahorizon.org
Location: Seattle, WA

DATA SCIENTIST & NLP RESEARCHER
Experience in predictive analytics, feature engineering, and LLM fine-tuning.

Technical Skills:
Python, Pandas, NumPy, Scikit-Learn, TensorFlow, SQL, Tableau, Power BI, Git

Education:
Master of Science in Data Science, University of Washington
"""
page4.insert_text((50, 60), text_res2, fontsize=11, fontname="courier")
doc4.save("samples/resume_missing_phone.pdf")
doc4.close()

# 5. Non-Document (Other type PDF)
doc5 = fitz.open()
page5 = doc5.new_page(width=595, height=842)
text_other = """
STANDARD MUTUAL CONFIDENTIALITY AGREEMENT (NDA)

This Agreement is entered into on September 1, 2026 by Alpha Corp and Omega Partner Ltd.
The Receiving Party agrees to maintain in confidence and not disclose proprietary trade secrets or research designs.
This agreement shall be governed by the laws of the State of California.

Signed:
Officer of Alpha Corp
Officer of Omega Partner Ltd
"""
page5.insert_text((50, 60), text_other, fontsize=11, fontname="courier")
doc5.save("samples/document_nda_other.pdf")
doc5.close()

# 6. Scanned/Image Invoice PNG (To test Step 3 OCR and Image Preprocessing)
img = Image.new('RGB', (800, 600), color=(245, 245, 245))
d = ImageDraw.Draw(img)
# Draw simulated invoice text
lines_img = [
    "QUICKPRINT STATIONERY SUPPLIES",
    "TAX INVOICE",
    "Invoice Number: INV-88219",
    "Date: 18-09-2026",
    "Billed To: Vanguard Logistics",
    "--------------------------------------",
    "Item: Premium A4 Paper Reams x 10 = $90.00",
    "Item: Color Cartridge Set x 2     = $120.00",
    "Shipping: $15.00",
    "--------------------------------------",
    "Total Amount: $225.00",
    "Paid via MasterCard ending 8812"
]
y_offset = 50
for line in lines_img:
    d.text((50, y_offset), line, fill=(20, 20, 20))
    y_offset += 35

img.save("samples/scanned_invoice.png")

print("Successfully generated test samples in samples/ directory.")
