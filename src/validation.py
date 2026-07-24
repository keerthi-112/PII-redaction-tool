# Placeholder validation module.
from __future__ import annotations

import re
from collections import defaultdict
from typing import Dict, List

from .utils import DetectedEntity


class Validation:
    """
    Validates generated replacement values before rewriting
    the document.
    """

    EMAIL_REGEX = re.compile(

        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    )

    PHONE_REGEX = re.compile(

        r"^[\d+\-()\s]{7,20}$"

    )

    SSN_REGEX = re.compile(

        r"^\d{3}-\d{2}-\d{4}$"

    )

    IPV4_REGEX = re.compile(

        r"^(?:\d{1,3}\.){3}\d{1,3}$"

    )

    CREDIT_CARD_REGEX = re.compile(

        r"^\d(?:[\d -]{10,23})\d$"

    )

    DOB_REGEX = re.compile(

        r"^\d{2}[/-]\d{2}[/-]\d{2,4}$"

    )

    def __init__(self):

        pass

    # =====================================================
    # Individual Validation
    # =====================================================

    def validate_entity(

        self,

        entity: DetectedEntity

    ) -> bool:

        value = entity.replacement

        if entity.label == "EMAIL":

            return bool(

                self.EMAIL_REGEX.fullmatch(value)

            )

        if entity.label == "PHONE_NUMBER":

            return bool(

                self.PHONE_REGEX.fullmatch(value)

            )

        if entity.label == "SSN":

            return bool(

                self.SSN_REGEX.fullmatch(value)

            )

        if entity.label == "IP_ADDRESS":

            return bool(

                self.IPV4_REGEX.fullmatch(value)

            )

        if entity.label == "CREDIT_CARD":

            return bool(

                self.CREDIT_CARD_REGEX.fullmatch(value)

            )

        if entity.label == "DATE_OF_BIRTH":

            return bool(

                self.DOB_REGEX.fullmatch(value)

            )

        return True

    # =====================================================
    # Whole Validation
    # =====================================================

    def validate(

        self,

        entities: List[DetectedEntity]

    ) -> Dict:

        report = {

            "total": len(entities),

            "passed": 0,

            "failed": 0,

            "errors": []

        }

        for entity in entities:

            if self.validate_entity(entity):

                report["passed"] += 1

            else:

                report["failed"] += 1

                report["errors"].append(

                    {

                        "text": entity.text,

                        "replacement": entity.replacement,

                        "label": entity.label

                    }

                )

        return report

    # =====================================================
    # Collision Detection
    # =====================================================

    def detect_collisions(

        self,

        entities: List[DetectedEntity]

    ):

        reverse = defaultdict(list)

        for entity in entities:

            reverse[

                entity.replacement

            ].append(entity.text)

        collisions = []

        for replacement, originals in reverse.items():

            if len(set(originals)) > 1:

                collisions.append(

                    {

                        "replacement": replacement,

                        "originals": sorted(

                            set(originals)

                        )

                    }

                )

        return collisions

    # =====================================================
    # Public API
    # =====================================================

    def run(

        self,

        entities: List[DetectedEntity]

    ) -> Dict:

        print(

            "\nRunning validation...\n"

        )

        validation = self.validate(

            entities

        )

        collisions = self.detect_collisions(

            entities

        )

        print(

            f"Passed : {validation['passed']}"

        )

        print(

            f"Failed : {validation['failed']}"

        )

        print(

            f"Collisions : {len(collisions)}"

        )

        return {

            "validation": validation,

            "collisions": collisions

        }