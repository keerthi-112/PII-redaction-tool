# Placeholder: use finalized generation implementation from our discussion.
from __future__ import annotations

import random
from typing import Dict, List

from faker import Faker

from .utils import DetectedEntity


class Generation:
    """
    Generates deterministic fake replacements for detected PII entities.

    Each DetectedEntity receives its generated replacement in the
    `replacement` field. Identical original values always receive the
    same replacement.
    """

    def __init__(self) -> None:

        self.fake = Faker()

        Faker.seed(42)
        random.seed(42)

        # Original text -> fake value
        self.cache: Dict[str, str] = {}

        # Person mapping is used for realistic email generation
        self.person_cache: Dict[str, str] = {}

    # =====================================================
    # PERSON
    # =====================================================

    def generate_person(self, original: str) -> str:

        if original in self.person_cache:
            return self.person_cache[original]

        fake_name = self.fake.name()

        self.person_cache[original] = fake_name

        return fake_name

    # =====================================================
    # EMAIL
    # =====================================================

    def generate_email(self, original: str) -> str:

        username = original.split("@")[0].lower()

        for real_name, fake_name in self.person_cache.items():

            real_tokens = real_name.lower().split()

            if any(token in username for token in real_tokens):

                fake_tokens = fake_name.lower().split()

                if len(fake_tokens) >= 2:
                    return (
                        f"{fake_tokens[0]}."
                        f"{fake_tokens[-1]}"
                        "@example.com"
                    )

                return f"{fake_tokens[0]}@example.com"

        return self.fake.email()

    # =====================================================
    # PHONE
    # =====================================================

    def generate_phone(self, original: str) -> str:

        digits = [c for c in original if c.isdigit()]

        fake_digits = [
            str(random.randint(0, 9))
            for _ in digits
        ]

        output = []

        idx = 0

        for ch in original:

            if ch.isdigit():

                output.append(fake_digits[idx])

                idx += 1

            else:

                output.append(ch)

        return "".join(output)

    # =====================================================
    # ORGANIZATION
    # =====================================================

    def generate_company(self, original: str) -> str:

        return self.fake.company()

    # =====================================================
    # ADDRESS
    # =====================================================

    def generate_address(self, original: str) -> str:

        return self.fake.address().replace("\n", ", ")

    # =====================================================
    # SSN
    # =====================================================

    def generate_ssn(self, original: str) -> str:

        return self.fake.ssn()

    # =====================================================
    # CREDIT CARD
    # =====================================================

    def generate_credit_card(self, original: str) -> str:

        digits = [c for c in original if c.isdigit()]

        fake_digits = [
            str(random.randint(0, 9))
            for _ in digits
        ]

        output = []

        idx = 0

        for ch in original:

            if ch.isdigit():

                output.append(fake_digits[idx])

                idx += 1

            else:

                output.append(ch)

        return "".join(output)

    # =====================================================
    # IP ADDRESS
    # =====================================================

    def generate_ip(self, original: str) -> str:

        return self.fake.ipv4()

    # =====================================================
    # DATE OF BIRTH
    # =====================================================

    def generate_dob(self, original: str) -> str:

        dob = self.fake.date_of_birth(
            minimum_age=18,
            maximum_age=80
        )

        separator = "/"

        if "-" in original:
            separator = "-"

        parts = original.split(separator)

        if len(parts[-1]) == 2:
            year = str(dob.year)[2:]
        else:
            year = str(dob.year)

        return (
            f"{dob.day:02d}"
            f"{separator}"
            f"{dob.month:02d}"
            f"{separator}"
            f"{year}"
        )

    # =====================================================
    # Dispatcher
    # =====================================================

    def generate_fake_value(
        self,
        entity: DetectedEntity
    ) -> str:

        label = entity.label

        if label == "PERSON":
            return self.generate_person(entity.text)

        if label == "EMAIL":
            return self.generate_email(entity.text)

        if label == "PHONE_NUMBER":
            return self.generate_phone(entity.text)

        if label == "ORGANIZATION":
            return self.generate_company(entity.text)

        if label == "ADDRESS":
            return self.generate_address(entity.text)

        if label == "SSN":
            return self.generate_ssn(entity.text)

        if label == "CREDIT_CARD":
            return self.generate_credit_card(entity.text)

        if label == "IP_ADDRESS":
            return self.generate_ip(entity.text)

        if label == "DATE_OF_BIRTH":
            return self.generate_dob(entity.text)

        return entity.text


            # =====================================================
    # Main Generation Pipeline
    # =====================================================

    def generate(
        self,
        entities: List[DetectedEntity]
    ) -> List[DetectedEntity]:
        """
        Generate fake replacements for every detected entity.

        Identical original values always receive the same replacement.
        The generated value is stored directly inside each entity.
        """

        print("\nStarting Fake Data Generation...\n")

        for entity in entities:

            # Already generated previously
            if entity.text in self.cache:

                entity.replacement = self.cache[entity.text]

                continue

            fake_value = self.generate_fake_value(entity)

            self.cache[entity.text] = fake_value

            entity.replacement = fake_value

        print(
            f"Generated replacements for "
            f"{len(self.cache)} unique entities."
        )

        return entities

    # =====================================================
    # Statistics
    # =====================================================

    def print_summary(
        self,
        entities: List[DetectedEntity]
    ) -> None:

        counts = {}

        for entity in entities:

            counts[entity.label] = (

                counts.get(entity.label, 0)

                + 1

            )

        print("\n========== Generation Summary ==========\n")

        for label in sorted(counts):

            print(

                f"{label:<20} : "

                f"{counts[label]}"

            )

        print(

            f"\nUnique replacements : "

            f"{len(self.cache)}"

        )

        print("\n========================================\n")

    # =====================================================
    # Public API
    # =====================================================

    def run(
        self,
        entities: List[DetectedEntity]
    ) -> List[DetectedEntity]:

        try:

            entities = self.generate(entities)

            self.print_summary(entities)

            return entities

        except Exception as exc:

            raise RuntimeError(

                f"Generation stage failed: {exc}"

            ) from exc