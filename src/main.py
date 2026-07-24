from __future__ import annotations

import sys
import traceback

from pipeline import Pipeline


def main() -> None:
    """
    Entry point for the PII Redaction Tool.
    """

    try:
        pipeline = Pipeline()
        pipeline.execute()

        print("\nPII Redaction completed successfully.\n")

    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        sys.exit(1)

    except Exception as exc:
        print("\nERROR: Pipeline execution failed.\n")
        print(str(exc))

        print("\nDetailed Traceback:\n")
        traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()