#!/usr/bin/env python3
"""Validate that every agdt.* skill file is classified in the fixture.

Exit codes:
  0 — all files present with correct buckets, no parse warnings.
  1 — one or more violations found (unregistered, mismatch, orphan, warning, error).
  2 — fixture file not found or malformed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Ensure the repo root is on sys.path so agentic_devtools can be imported
# when this script is run directly (python scripts/validate_skill_classification.py).
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "skill_classification_expected.json"


def main() -> int:
    """Run skill classification validation and print diagnostics."""
    from agentic_devtools.cli.checks.skill_classification import (
        validate_skill_classification,
    )

    try:
        result = validate_skill_classification(REPO_ROOT, FIXTURE_PATH)
    except FileNotFoundError:
        print(
            f"ERROR: Fixture file not found: {FIXTURE_PATH}\n"
            "  Create or populate tests/fixtures/skill_classification_expected.json.",
            file=sys.stderr,
        )
        return 2
    except OSError as exc:
        print(
            f"ERROR: Could not read fixture file: {FIXTURE_PATH}\n  {exc}",
            file=sys.stderr,
        )
        return 2
    except (json.JSONDecodeError, ValueError) as exc:
        print(
            f"ERROR: Malformed fixture file: {FIXTURE_PATH}\n  {exc}",
            file=sys.stderr,
        )
        return 2

    if result.is_valid:
        print(f"OK — {result.validated_count} skill file(s) validated, no violations found.")
        return 0

    # Print diagnostics per category.
    total_violations = 0

    if result.unregistered_files:
        total_violations += len(result.unregistered_files)
        print("UNREGISTERED FILES (on disk but not in fixture):")
        for f in result.unregistered_files:
            print(f"  - {f}")
        print("  → Add these files to tests/fixtures/skill_classification_expected.json\n")

    if result.mismatches:
        total_violations += len(result.mismatches)
        print("BUCKET MISMATCHES (normalized ≠ fixture):")
        for m in result.mismatches:
            print(f"  - {m.file}")
            print(f"    expected: {m.expected}")
            print(f"    actual:   {m.actual}")
        print("  → Update the fixture or fix the file's frontmatter\n")

    if result.orphan_entries:
        total_violations += len(result.orphan_entries)
        print("ORPHAN FIXTURE ENTRIES (in fixture but not on disk):")
        for f in result.orphan_entries:
            print(f"  - {f}")
        print("  → Remove these entries from tests/fixtures/skill_classification_expected.json\n")

    if result.parse_warnings:
        total_violations += len(result.parse_warnings)
        print("PARSE WARNINGS (treated as errors):")
        for w in result.parse_warnings:
            print(f"  - {w.file}: {w.message}")
        print("  → Fix the frontmatter to use valid values\n")

    if result.parse_errors:
        total_violations += len(result.parse_errors)
        print("PARSE ERRORS (unparseable YAML frontmatter):")
        for e in result.parse_errors:
            print(f"  - {e.file}: {e.error}")
        print("  → Fix the YAML syntax\n")

    print(f"FAIL — {total_violations} violation(s) found.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
