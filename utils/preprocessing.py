import re
import unicodedata
import numpy as np
from PIL import Image
import cv2

def clean_and_normalize_text(text: str) -> str:
    """
    Step 2: Clean and normalize extracted text:
    - Normalizes unicode characters.
    - Replaces odd whitespace/control characters with standard spaces.
    - Condenses multiple spaces and tabs into a single space.
    - Collapses multiple blank lines into a single blank line.
    - Strips leading and trailing whitespace.
    """
    if not text:
        return ""
    
    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)
    
    # Replace non-breaking spaces and carriage returns
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    
    # Remove control characters except standard whitespace
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Collapse multiple horizontal whitespace (spaces/tabs) into one
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Collapse 3 or more consecutive newlines down to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip whitespace from each individual line
    lines = [line.strip() for line in text.split('\n')]
    cleaned = '\n'.join(lines).strip()
    
    return cleaned

def is_text_sufficient(text: str, min_chars: int = 20) -> bool:
    """Check if extracted text meets minimum character threshold."""
    if not text:
        return False
    return len(re.sub(r'\s+', '', text)) >= min_chars

def preprocess_image_for_ocr(image: Image.Image, method: str = "adaptive") -> Image.Image:
    """
    Step 3: Improve OCR handling using OpenCV image preprocessing:
    - Resizing/Scaling to optimal DPI
    - Grayscale conversion
    - Noise reduction (Bilateral filtering)
    - Adaptive thresholding / Otsu binarization
    """
    cv_img = np.array(image.convert("RGB"))
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

    # Resize if image is small (< 1200px on max dimension)
    h, w = cv_img.shape[:2]
    max_dim = max(h, w)
    if max_dim < 1200:
        scale = 1200.0 / max_dim
        new_w, new_h = int(w * scale), int(h * scale)
        cv_img = cv2.resize(cv_img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    # Grayscale conversion
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # Noise reduction using bilateral filter
    denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # Binarization
    if method == "otsu":
        blurred = cv2.GaussianBlur(denoised, (3, 3), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 11
        )

    return Image.fromarray(thresh)
