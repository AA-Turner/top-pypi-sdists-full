#!/usr/bin/env python
"""Validate setup expectations document against source code.

Thin CLI wrapper around the package validator.  Exit codes:
  0 — doc is consistent with source
  1 — drift detected (details printed to stdout)
"""

from __future__ import annotations

import sys

# Force UTF-8 stdout/stderr so emoji survive on Windows cp1252 terminals.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


def main() -> int:
    """Run the setup expectations validator."""
    from agentic_devtools.cli.setup.expectations_validator import validate_expectations

    result = validate_expectations()
    if result.passed:
        print("✅ Setup expectations document is consistent with source.")
        return 0

    print("❌ Setup expectations document drift detected:")
    for err in result.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
