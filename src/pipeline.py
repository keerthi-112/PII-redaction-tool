from __future__ import annotations

from typing import Any, Dict, List

from .config import (
    INPUT_FILE,
    OUTPUT_FILE,
    MAPPING_FILE,
    REPORT_FILE,
    SAVE_MAPPING,
    SAVE_REPORT,
)

from .discovery import Discovery
from .generation import Generation
from .validation import Validation
from .rewrite import Rewrite
from .utils import (
    DetectedEntity,
    ensure_directory,
    save_json,
)



class Pipeline:
    """
    Executes the complete PII Redaction pipeline.

    Flow:
        Discovery
            ↓
        Generation
            ↓
        Validation
            ↓
        Rewrite
            ↓
        Save Outputs
    """

    def __init__(self) -> None:

        self.discovery = Discovery()
        self.generation = Generation()
        self.validation = Validation()
        self.rewrite = Rewrite()

    # =====================================================
    # Mapping
    # =====================================================

    @staticmethod
    def build_mapping(
        entities: List[DetectedEntity],
    ) -> List[Dict[str, str]]:

        return [
            {
                "original": entity.text,
                "replacement": entity.replacement,
                "entity_type": entity.label,
            }
            for entity in entities
        ]

    # =====================================================
    # Evaluation Report
    # =====================================================

    @staticmethod
    def build_report(
        validation_report: Dict[str, Any],
        entities: List[DetectedEntity],
    ) -> Dict[str, Any]:

        return {
            "total_entities": len(entities),
            "validation": validation_report["validation"],
            "collisions": validation_report["collisions"],
        }

    # =====================================================
    # Execute Pipeline
    # =====================================================

    def execute(
        self,
        input_file=INPUT_FILE,
        output_file=OUTPUT_FILE,
        mapping_file=MAPPING_FILE,
        report_file=REPORT_FILE,
    ):

        print("\n========== PII Redaction Pipeline ==========\n")

        ensure_directory(output_file.parent)

        # ---------------------------------------------
        # Discovery
        # ---------------------------------------------

        document, entities = self.discovery.run(input_file)

        # ---------------------------------------------
        # Generation
        # ---------------------------------------------

        entities = self.generation.run(entities)

        # ---------------------------------------------
        # Validation
        # ---------------------------------------------

        validation_report = self.validation.run(entities)

        if validation_report["validation"]["failed"] > 0:
            raise RuntimeError(
                "Validation failed. Fix generated replacements before rewriting."
            )

        # ---------------------------------------------
        # Rewrite
        # ---------------------------------------------

        document = self.rewrite.run(
            document,
            entities,
        )

        # ---------------------------------------------
        # Save DOCX
        # ---------------------------------------------

        document.save(output_file)

        print(f"\n✓ Redacted document saved to:\n{output_file}")

        # ---------------------------------------------
        # Save Mapping
        # ---------------------------------------------

        if SAVE_MAPPING:

            save_json(
                self.build_mapping(entities),
                mapping_file,
            )

            print(f"✓ Mapping saved to:\n{mapping_file}")

        # ---------------------------------------------
        # Save Evaluation Report
        # ---------------------------------------------

        if SAVE_REPORT:

            save_json(
                self.build_report(
                    validation_report,
                    entities,
                ),
                report_file,
            )

            print(f"✓ Evaluation report saved to:\n{report_file}")

        print("\n========== Pipeline Completed Successfully ==========\n")

        return document