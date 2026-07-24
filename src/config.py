from pathlib import Path
import random

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

INPUT_FILE = INPUT_DIR / "rhp.docx"

OUTPUT_FILE = OUTPUT_DIR / "redacted_rhp.docx"

MAPPING_FILE = OUTPUT_DIR / "mapping.json"

REPORT_FILE = OUTPUT_DIR / "evaluation_report.json"

# ==========================================================
# NLP Configuration
# ==========================================================

SPACY_MODEL = "en_core_web_sm"

LANGUAGE = "en"

# ==========================================================
# Supported Entity Types
# ==========================================================

SUPPORTED_ENTITIES = {
    "PERSON",
    "EMAIL",
    "PHONE_NUMBER",
    "ORGANIZATION",
    "ADDRESS",
    "SSN",
    "CREDIT_CARD",
    "DATE_OF_BIRTH",
    "IP_ADDRESS",
}

# ==========================================================
# Faker Configuration
# ==========================================================

FAKER_SEED = 42
random.seed(FAKER_SEED)

# ==========================================================
# Validation
# ==========================================================

MIN_CONFIDENCE = 0.50

# ==========================================================
# Output Options
# ==========================================================

SAVE_MAPPING = True
SAVE_REPORT = True

# ==========================================================
# Logging
# ==========================================================

VERBOSE = True
PRINT_STATS = True