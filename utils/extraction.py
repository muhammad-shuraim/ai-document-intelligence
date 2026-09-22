import re
from typing import Dict, List, Any

# Extensive skill set for resume skill mining
SKILLS_TAXONOMY = [
    # Programming Languages
    "python", "java", "c++", "c#", "c", "javascript", "typescript", "ruby", "php", "go", "golang",
    "rust", "swift", "kotlin", "r", "scala", "matlab", "perl", "dart", "sql", "html", "css",
    # Frameworks & Libraries
    "react", "react.js", "angular", "vue", "vue.js", "node.js", "express", "django", "flask",
    "fastapi", "spring", "spring boot", "asp.net", ".net", "flutter", "react native", "next.js",
    # AI / ML / Data Science
    "machine learning", "deep learning", "nlp", "natural language processing", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas", "numpy", "scipy",
    "opencv", "llm", "transformers", "xgboost", "lightgbm", "spacy", "nltk", "data analysis",
    "tableau", "power bi", "matplotlib", "seaborn",
    # Cloud, DevOps & Tools
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "git", "github", "gitlab",
    "ci/cd", "jenkins", "linux", "bash", "terraform", "ansible", "kafka", "rabbitmq", "redis",
    "mongodb", "postgresql", "mysql", "sqlite", "graphql", "rest api", "jira", "agile", "scrum"
]

def extract_invoice_fields(text: str) -> Dict[str, str]:
    """
    Step 7 & 8: Extract fields from invoice text with robust fallbacks:
    - Invoice Number
    - Date
    - Company Name
    - Total Amount
    Handles missing fields gracefully by returning 'Not Found'.
    """
    details: Dict[str, str] = {
        "Invoice Number": "Not Found",
        "Date": "Not Found",
        "Company": "Not Found",
        "Total Amount": "Not Found"
    }
    
    if not text:
        return details

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # 1. Invoice Number
    # Match patterns like "Invoice # 1234", "INV-2026-001", "Invoice No: ABC-998", "Bill No. 445"
    inv_patterns = [
        r'(?:invoice\s*(?:number|no\.?|#|id)|inv\s*(?:#|no\.?)|bill\s*(?:no\.?|#))[:\s]*([A-Za-z0-9\-_/]+)',
        r'\b(INV-[A-Za-z0-9\-]+)\b',
        r'#\s*([0-9]{4,10})\b'
    ]
    for pattern in inv_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = match.group(1).strip()
            # Ignore false matches like "Date" or empty
            if val.lower() not in ["date", "due", "to", "total", "no"]:
                details["Invoice Number"] = val
                break

    # 2. Date
    # Match: YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY, MM/DD/YYYY, or "September 21, 2026"
    date_patterns = [
        r'(?:date|invoice\s*date|issue\s*date|dated)[:\s]*([0-9]{1,2}[-/.][0-9]{1,2}[-/.][0-9]{2,4})',
        r'(?:date|invoice\s*date|issue\s*date|dated)[:\s]*([0-9]{4}[-/.][0-9]{1,2}[-/.][0-9]{1,2})',
        r'(?:date|invoice\s*date|issue\s*date|dated)[:\s]*([A-Za-z]{3,9}\s+[0-9]{1,2},?\s+[0-9]{4})',
        r'\b([0-9]{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+[0-9]{4})\b',
        r'\b([0-9]{1,2}[-/.][0-9]{1,2}[-/.][0-9]{4})\b',
        r'\b([0-9]{4}[-/.][0-9]{1,2}[-/.][0-9]{2})\b'
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            details["Date"] = match.group(1).strip()
            break

    # 3. Company Name
    # Match labeled fields e.g., "From: XYZ Corp", "Billed By: ABC Inc", "Vendor: Acron" or deduce from top lines
    company_patterns = [
        r'(?:billed\s*by|from|vendor|provider|seller|company)[:\s]*([A-Za-z0-9\s&,.\'-]{3,40})',
    ]
    for pattern in company_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            c_val = match.group(1).split("\n")[0].strip()
            if len(c_val) > 2 and not any(kw in c_val.lower() for kw in ["invoice", "date", "bill to", "tax"]):
                details["Company"] = c_val
                break

    if details["Company"] == "Not Found" and lines:
        # Fallback: Top non-generic header line often represents company name
        for line in lines[:5]:
            if any(kw in line.lower() for kw in ["invoice", "bill to", "tax invoice", "receipt", "customer"]):
                continue
            if len(line) >= 3 and len(line) <= 50 and not re.match(r'^[0-9\W]+$', line):
                details["Company"] = line
                break

    # 4. Total Amount
    # Match patterns like: "Total: $1,250.00", "Grand Total: INR 5000", "Amount Due: 450.50"
    total_patterns = [
        r'(?:grand\s*total|total\s*amount|total\s*due|balance\s*due|amount\s*due|total)[:\s]*([$€£₹A-Z]{0,4}\s*[\d,]+\.?\d*)',
        r'([$€£₹]\s*[\d,]+\.\d{2})',
    ]
    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            t_val = match.group(1).strip()
            # Ensure it's not a generic word
            if any(char.isdigit() for char in t_val):
                details["Total Amount"] = t_val
                break

    return details

def extract_resume_fields(text: str) -> Dict[str, str]:
    """
    Step 7 & 8: Extract fields from resume text:
    - Candidate Name
    - Email
    - Phone Number
    - Skills (matched against skill taxonomy)
    Handles missing fields gracefully with 'Not Found'.
    """
    details: Dict[str, str] = {
        "Name": "Not Found",
        "Email": "Not Found",
        "Phone": "Not Found",
        "Skills": "Not Found"
    }

    if not text:
        return details

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # 1. Email Address (standard RFC-compliant email regex)
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    if email_match:
        details["Email"] = email_match.group(0).strip()

    # 2. Phone Number
    # Matches +1-234-567-8900, (123) 456-7890, +91 9876543210, 123.456.7890, etc.
    phone_match = re.search(r'(?:\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b', text)
    if phone_match:
        details["Phone"] = phone_match.group(0).strip()

    # 3. Candidate Name
    # Candidate name is usually prominently displayed at top of the resume before contact info
    for line in lines[:6]:
        # Skip if contains email, phone, web links, or heading keywords
        if "@" in line or "http" in line or any(kw in line.lower() for kw in ["resume", "curriculum vitae", "cv", "portfolio", "phone", "email", "summary", "profile"]):
            continue
        # Filter strings that look like a human name (2-4 capitalized words, no punctuation/numbers)
        words = line.split()
        if 2 <= len(words) <= 4 and all(re.match(r'^[A-Z][a-zA-Z\'.\-]*$', w) for w in words):
            details["Name"] = line
            break
    
    # Fallback to first non-empty line if reasonable length and not a keyword
    if details["Name"] == "Not Found" and lines:
        first_line = lines[0]
        if len(first_line) <= 40 and not any(k in first_line.lower() for k in ["resume", "cv", "page"]):
            details["Name"] = first_line

    # 4. Skills extraction
    # Search for skills section or scan entire document against known taxonomy
    text_lower = text.lower()
    found_skills = set()
    
    # Prioritize searching inside dedicated skills section if present
    skills_section_match = re.search(r'(?:skills|technical skills|technologies|proficiencies|core competencies)[:\s\n]+([^\n\r]+(?:\n[^\n\r]+){0,5})', text, re.IGNORECASE)
    search_scope = skills_section_match.group(1).lower() if skills_section_match else text_lower

    for skill in SKILLS_TAXONOMY:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, search_scope):
            # Format nicely
            found_skills.add(skill.title() if len(skill) > 3 and skill not in ["aws", "gcp", "sql", "nlp", "llm", "css", "html"] else skill.upper())

    if not found_skills and skills_section_match:
        # If taxonomy missed, parse comma-separated skills in the section
        tokens = [t.strip() for t in re.split(r'[,|•*]', skills_section_match.group(1)) if t.strip()]
        for tok in tokens[:8]:
            if len(tok) < 25 and not any(kw in tok.lower() for kw in ["experience", "education", "project"]):
                found_skills.add(tok.title())

    if found_skills:
        details["Skills"] = ", ".join(sorted(list(found_skills))[:12])

    return details
