import unittest
import os
import joblib
from PIL import Image
from utils.preprocessing import clean_and_normalize_text, is_text_sufficient, preprocess_image_for_ocr
from utils.extraction import extract_invoice_fields, extract_resume_fields

class TestDocumentIntelligencePipeline(unittest.TestCase):

    def test_text_cleaning_and_normalization(self):
        raw_text = "  Invoice   Number:   INV-1024  \n\n\n\r\nDate:   2026-09-21\xa0\xa0\n\n\nTotal: $500   "
        cleaned = clean_and_normalize_text(raw_text)
        self.assertNotIn("\xa0", cleaned)
        self.assertNotIn("\r", cleaned)
        self.assertNotIn("\n\n\n", cleaned)
        self.assertTrue(is_text_sufficient(cleaned))

    def test_empty_text_handling(self):
        self.assertEqual(clean_and_normalize_text(""), "")
        self.assertFalse(is_text_sufficient("    \n\t  "))
        self.assertFalse(is_text_sufficient("short"))

    def test_invoice_field_extraction(self):
        sample = """
        Apex Solutions Inc.
        TAX INVOICE
        Invoice Number: INV-2026-881
        Date: 15-09-2026
        Total Amount: $4,500.00
        """
        extracted = extract_invoice_fields(clean_and_normalize_text(sample))
        self.assertEqual(extracted["Invoice Number"], "INV-2026-881")
        self.assertEqual(extracted["Date"], "15-09-2026")
        self.assertEqual(extracted["Company"], "Apex Solutions Inc.")
        self.assertEqual(extracted["Total Amount"], "$4,500.00")

    def test_invoice_missing_fields_graceful(self):
        sample = "Partial order receipt without total or invoice number.\nDate: 01/01/2026"
        extracted = extract_invoice_fields(clean_and_normalize_text(sample))
        self.assertEqual(extracted["Invoice Number"], "Not Found")
        self.assertEqual(extracted["Total Amount"], "Not Found")
        self.assertEqual(extracted["Date"], "01/01/2026")

    def test_resume_field_extraction(self):
        sample = """
        Jonathan Miller
        jonathan.miller@example.com | (555) 123-4567 | Austin, TX
        
        SKILLS
        Python, React, Docker, AWS, Scikit-Learn, SQL
        
        EXPERIENCE
        Senior Software Developer at CloudCorp
        """
        extracted = extract_resume_fields(clean_and_normalize_text(sample))
        self.assertEqual(extracted["Name"], "Jonathan Miller")
        self.assertEqual(extracted["Email"], "jonathan.miller@example.com")
        self.assertEqual(extracted["Phone"], "(555) 123-4567")
        self.assertIn("Python", extracted["Skills"])
        self.assertIn("Docker", extracted["Skills"])

    def test_resume_missing_fields_graceful(self):
        sample = "Draft bio without contact info.\nSkills: Python, Git."
        extracted = extract_resume_fields(clean_and_normalize_text(sample))
        self.assertEqual(extracted["Email"], "Not Found")
        self.assertEqual(extracted["Phone"], "Not Found")

    def test_model_inference_and_confidence(self):
        model_path = os.path.join("models", "classifier_model.pkl")
        vec_path = os.path.join("models", "tfidf_vectorizer.pkl")
        self.assertTrue(os.path.exists(model_path))
        self.assertTrue(os.path.exists(vec_path))

        clf = joblib.load(model_path)
        vec = joblib.load(vec_path)

        inv_text = "Tax Invoice Bill To: Acme Corp Total: $990 Invoice Number: 4401"
        inv_vec = vec.transform([clean_and_normalize_text(inv_text)])
        pred = clf.predict(inv_vec)[0]
        proba = clf.predict_proba(inv_vec)[0]
        conf = max(proba) * 100

        self.assertEqual(pred, "Invoice")
        self.assertGreater(conf, 50.0)

    def test_ocr_image_preprocessing(self):
        img = Image.new("RGB", (200, 200), color="white")
        processed = preprocess_image_for_ocr(img)
        self.assertIsNotNone(processed)
        self.assertGreaterEqual(processed.size[0], 1200)

if __name__ == "__main__":
    unittest.main()
