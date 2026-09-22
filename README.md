# AI Document Intelligence & Workflow Platform

**Task 02: Improve Document Understanding (Week 3 Upgrade)**
*Zyroo AI/ML Internship Program*

An end-to-end intelligent document processing application that ingests PDFs and images, cleans and normalizes OCR/PDF text, performs machine learning document classification with calibrated confidence scores, and extracts critical structured information with robust missing-field resilience.

---

## 🌟 What's New in Week 3 (Changes from Week 2)

| Feature | Week 2 MVP | Week 3 Upgrade |
|---|---|---|
| **Text Preprocessing** | Direct extraction without cleaning | Unicode normalization (NFKC), whitespace condensation, control character stripping, short/empty text validation |
| **OCR Handling** | Basic `pytesseract` pass | OpenCV pipeline: auto-rescaling, grayscale conversion, bilateral noise filtration, and Adaptive/Otsu thresholding |
| **Classification** | Naive keyword matching (`if 'invoice' in text`) | Machine Learning pipeline: TF-IDF n-grams + Logistic Regression with calibrated confidence percentages |
| **Model Comparison** | None | Cross-validated comparison of **Logistic Regression**, **Linear SVM**, and **Multinomial Naive Bayes** |
| **Field Extraction** | Rigid 1-2 line regex patterns | Multi-format regex for dates (`DD-MM-YYYY`, `YYYY-MM-DD`, written formats), international amounts (`$`, `€`, `£`, `₹`), and dynamic 70+ technology skill mining |
| **Missing Fields** | Unhandled / partial failure | Graceful fallback to `Not Found` with UI status badges and summary counts without crashing |
| **Confidence Scoring** | None | Real-time prediction probability display (e.g. `96.4%`) with class distribution breakdown |
| **Evaluation Metrics** | None | Accuracy, Precision, Recall, F1-Score, and Confusion Matrix generated and embedded in the dashboard |

---

## 🏗️ Architecture & Pipeline Flow

```
Upload (PDF/Image) 
       ↓ 
Read Text / OCR Preprocessing (OpenCV + PyMuPDF / Tesseract) 
       ↓ 
Clean & Normalize Text (NFKC, Whitespace Condensation) 
       ↓ 
Identify Document Type (TF-IDF Vectorizer + Logistic Regression) 
       ↓ 
Confidence Calculation (predict_proba / Calibrated Probability) 
       ↓ 
Extract Fields (Invoices & Resumes via improved patterns) 
       ↓ 
Handle Missing Fields (Graceful fallback to "Not Found") 
       ↓ 
Interactive Streamlit UI Results & Model Evaluation Dashboard
```

---

## 📊 Model Evaluation & Comparison Results

Evaluated across balanced document categories (**Invoice**, **Resume**, **Other**) using 5-Fold Stratified Cross-Validation:

### 1. Cross-Validation Model Comparison
| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
|---|---|---|---|---|
| **Logistic Regression (Selected)** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| **Linear SVM** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| **Multinomial Naive Bayes** | 0.8667 | 0.9111 | 0.8667 | 0.8578 |

> **Selection Rationale:** While Linear SVM and Logistic Regression both achieve exceptional performance, **Logistic Regression** naturally yields true calibrated probability estimates (`predict_proba`) essential for displaying **Classifier Confidence %** (Week 3 Requirement Step 9).

### 2. Held-Out Test Split Metrics (Logistic Regression)
- **Accuracy:** 77.8% - 100% (depending on split)
- **Precision:** 86.7%
- **Recall:** 77.8%
- **F1-Score:** 75.0%

### 3. Confusion Matrix
```
             Pred: Invoice   Pred: Other   Pred: Resume
Actual Invoice     [ 3             0             0 ]
Actual Other       [ 2             1             0 ]
Actual Resume      [ 0             0             3 ]
```

---

## 🎯 Target Extraction Fields

### Invoice
- `Invoice Number` (e.g., `INV-2026-9042`, `#88219`, `AUR-5510`)
- `Date` (e.g., `15-09-2026`, `2026-03-14`, `October 05, 2026`)
- `Company Name` (Header and vendor labeling heuristic)
- `Total Amount` (e.g., `$5,629.00`, `€1,200.00`, `₹4,500`)

### Resume
- `Candidate Name` (Candidate header parsing, excluding links & labels)
- `Email` (RFC-compliant email pattern)
- `Phone Number` (International and domestic formats)
- `Skills` (Dynamic dictionary matching against 70+ languages, frameworks, cloud, and ML libraries)

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train and Evaluate Models
```bash
python train_classifier.py
```
This script cleans the dataset, runs 5-fold cross-validation, saves the evaluation metrics JSON, and writes serialized artifacts to `models/classifier_model.pkl` and `models/tfidf_vectorizer.pkl`.

### 3. Run Automated Tests
```bash
python -m unittest tests/test_pipeline.py
```

### 4. Launch the Web Application
```bash
streamlit run app.py
```

---

## 📁 Repository Structure
```
ai-document-intelligence/
│
├── app.py                      # Updated Streamlit web application
├── train_classifier.py         # Model training, cross-validation, and evaluation
├── requirements.txt            # Dependency list
├── README.md                   # Project documentation and Week 3 change summary
│
├── utils/
│   ├── __init__.py
│   ├── preprocessing.py        # Text normalization & OpenCV OCR enhancement
│   └── extraction.py           # Improved field extraction & missing field logic
│
├── data/
│   ├── prepare_data.py         # Dataset generation script
│   └── documents_dataset.json  # Balanced multi-class training data
│
├── models/
│   ├── classifier_model.pkl    # Serialized Logistic Regression classifier
│   ├── tfidf_vectorizer.pkl    # Serialized TF-IDF vectorizer
│   └── evaluation_metrics.json # Stored metrics and confusion matrix
│
├── samples/                    # Test documents (PDF, PNG, missing fields)
│   ├── create_samples.py
│   ├── invoice_complete.pdf
│   ├── invoice_missing_fields.pdf
│   ├── resume_complete.pdf
│   ├── resume_missing_phone.pdf
│   ├── document_nda_other.pdf
│   └── scanned_invoice.png
│
└── tests/
    └── test_pipeline.py        # Complete unit test suite (8 passing tests)
```
