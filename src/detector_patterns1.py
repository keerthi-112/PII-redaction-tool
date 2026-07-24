import re
EMAIL_REGEX=re.compile(r"[\w.-]+@[\w.-]+")
PHONE_REGEX = re.compile(
    r"\b(?:\+\d{1,3}[- ]?)?(?:\(?\d{3}\)?[- ]?)\d{3}[- ]?\d{4}\b"
)
SSN_REGEX=re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CREDIT_CARD_REGEX=re.compile(r"\b(?:\d[ -]*?){13,16}\b")
IP_REGEX=re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOB_REGEX=re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b")
