"""ADR-014 existence and content validation helper.

Provides ``validate_adr_014()`` which asserts that the ADR file exists,
contains all required sections, references all four evaluated options,
and that the summary table in ``docs/09-architecture-decisions.md``
includes a row for ADR-014.
"""

from __future__ import annotations

from pathlib import Path

_ADR_PATH = "docs/architecture-decisions/ADR-014-autonomous-execution-model.md"
_SUMMARY_PATH = "docs/09-architecture-decisions.md"

_REQUIRED_SECTIONS = [
    "Status",
    "Context",
    "Decision",
    "Consequences",
]

_REQUIRED_OPTIONS = [
    "Option A",
    "Option B",
    "Option C",
    "Option D",
]


def validate_adr_014(repo_root: str | Path | None = None) -> None:
    """Assert ADR-014 exists and contains all required content.

    Raises ``AssertionError`` with a descriptive message if any check fails.

    Args:
        repo_root: Repository root directory.  Defaults to the current
            working directory.
    """
    root = Path(repo_root) if repo_root else Path.cwd()

    # --- ADR file existence ---
    adr_file = root / _ADR_PATH
    if not adr_file.is_file():
        raise AssertionError(f"ADR-014 not found at {adr_file}")

    content = adr_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    # --- Required sections (line-based heading detection) ---
    # Matches "## Section" headings or "**Section**" bold-label style.
    for section in _REQUIRED_SECTIONS:
        section_lower = section.lower()
        found = any(
            line.strip().lower().startswith(f"## {section_lower}")
            or line.strip().lower().startswith(f"**{section_lower}**")
            for line in lines
        )
        if not found:
            raise AssertionError(f"ADR-014 missing required section: {section}")

    # --- All four options referenced (line-based) ---
    for option in _REQUIRED_OPTIONS:
        option_lower = option.lower()
        if not any(option_lower in line.lower() for line in lines):
            raise AssertionError(f"ADR-014 missing option reference: {option}")

    # --- Summary table row ---
    summary_file = root / _SUMMARY_PATH
    if not summary_file.is_file():
        raise AssertionError(f"Summary table not found at {summary_file}")

    summary_content = summary_file.read_text(encoding="utf-8")
    if not any("| 014 |" in line for line in summary_content.splitlines()):
        raise AssertionError("docs/09-architecture-decisions.md does not contain a row for ADR-014")
