
# ==========================================================
# Data Models
# ==========================================================

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, Any


@dataclass
class DetectedEntity:
    """
    Represents a detected PII entity along with its location
    and generated replacement value.
    """

    text: str
    label: str

    start: int
    end: int

    paragraph_index: Optional[int] = None
    table_index: Optional[int] = None
    row_index: Optional[int] = None
    cell_index: Optional[int] = None

    confidence: float = 1.0
    source: str = ""

    # NEW FIELD
    replacement: str = ""



# ==========================================================
# Directory Utilities
# ==========================================================

def ensure_directory(path: Path):

    path.mkdir(
        parents=True,
        exist_ok=True
    )


# ==========================================================
# JSON Utilities
# ==========================================================

def save_json(data: Dict[str, Any], path: Path):

    ensure_directory(path.parent)

    with open(path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_json(path: Path):

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as file:

        return json.load(file)



# ==========================================================
# Statistics
# ==========================================================

def count_entities(entities):

    stats = {}

    for entity in entities:

        stats[entity.label] = stats.get(entity.label, 0) + 1

    return stats


def print_statistics(stats):

    print("\n========== Entity Statistics ==========\n")

    for entity, count in sorted(stats.items()):

        print(f"{entity:<20} : {count}")

    print()