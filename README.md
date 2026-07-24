# PII Redaction Tool

This project reads a Word (.docx) document, detects Personally Identifiable Information (PII), and replaces it with realistic fake values while keeping the document formatting unchanged.

Approach

The detection is done using a combination of:

- Regular Expressions (Regex) for email addresses, phone numbers, SSNs, credit card numbers, IP addresses and dates of birth.
- spaCy Named Entity Recognition (NER) for names, organizations and locations.
- Microsoft Presidio Analyzer as an additional detection layer.

After collecting all detected entities, duplicates and overlapping detections are removed. Fake replacements are generated using the Faker library, and the document is rewritten without changing its formatting.

Supported PII

- Full Names
- Email Addresses
- Phone Numbers
- Company Names
- Physical Addresses
- Social Security Numbers (SSNs)
- Credit Card Numbers
- Dates of Birth
- IP Addresses

Project Files

input/
- Input document

output/
- redacted_rhp.docx
- mapping.json
- evaluation_report.json

src/
- Source code

requirements.txt
README.md
evaluation_report.md

Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

Download the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

Run

```bash
python src/main.py
```

Trade-offs

Regex works well for structured information like emails, phone numbers and SSNs. spaCy and Presidio help identify names, organizations and addresses that cannot be detected using regex alone. During testing, some address components were occasionally detected separately by the NER model, but duplicate removal and overlap resolution reduced these cases.