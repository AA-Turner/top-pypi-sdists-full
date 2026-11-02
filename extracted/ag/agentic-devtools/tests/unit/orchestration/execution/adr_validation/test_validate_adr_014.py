"""Tests for validate_adr_014 helper."""

from pathlib import Path

import pytest

from agentic_devtools.orchestration.execution.adr_validation import validate_adr_014

# Resolve repo root dynamically from test file location
_REPO_ROOT = Path(__file__).resolve().parents[5]


class TestValidateAdr014:
    def test_passes_with_real_repo(self) -> None:
        """ADR-014 exists and contains all required content."""
        validate_adr_014(_REPO_ROOT)

    def test_fails_when_adr_missing(self, tmp_path) -> None:  # noqa: ANN001
        """Raises AssertionError when ADR file is missing."""
        with pytest.raises(AssertionError, match="not found"):
            validate_adr_014(tmp_path)

    def test_fails_when_section_missing(self, tmp_path) -> None:  # noqa: ANN001
        """Raises AssertionError when required section is missing."""
        adr_dir = tmp_path / "docs" / "architecture-decisions"
        adr_dir.mkdir(parents=True)
        adr_file = adr_dir / "ADR-014-autonomous-execution-model.md"
        adr_file.write_text("# ADR-014\n\n## Status\nAccepted\n")
        with pytest.raises(AssertionError, match="missing required section"):
            validate_adr_014(tmp_path)

    def test_fails_when_section_name_appears_only_in_prose(self, tmp_path) -> None:  # noqa: ANN001
        """Section names embedded in prose do not satisfy the heading requirement."""
        adr_dir = tmp_path / "docs" / "architecture-decisions"
        adr_dir.mkdir(parents=True)
        adr_file = adr_dir / "ADR-014-autonomous-execution-model.md"
        # "context" and "decision" appear in prose but NOT as `## Context` / `**Context**` headings
        adr_file.write_text("# ADR-014\n\n## Status\nAccepted\n\nIn this context the decision was made.\n")
        with pytest.raises(AssertionError, match="missing required section"):
            validate_adr_014(tmp_path)

    def test_fails_when_option_missing(self, tmp_path) -> None:  # noqa: ANN001
        """Raises AssertionError when option reference is missing."""
        adr_dir = tmp_path / "docs" / "architecture-decisions"
        adr_dir.mkdir(parents=True)
        adr_file = adr_dir / "ADR-014-autonomous-execution-model.md"
        adr_file.write_text(
            "# ADR-014\n\n## Status\n## Context\n## Decision\n## Consequences\nOption A\nOption B\nOption C\n"
        )
        with pytest.raises(AssertionError, match="Option D"):
            validate_adr_014(tmp_path)

    def test_fails_when_summary_row_missing(self, tmp_path) -> None:  # noqa: ANN001
        """Raises AssertionError when summary table lacks ADR-014 row."""
        adr_dir = tmp_path / "docs" / "architecture-decisions"
        adr_dir.mkdir(parents=True)
        adr_file = adr_dir / "ADR-014-autonomous-execution-model.md"
        adr_file.write_text(
            "\n".join(
                [
                    "# ADR",
                    "## Status",
                    "## Context",
                    "## Decision",
                    "## Consequences",
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D",
                ]
            )
            + "\n"
        )
        summary = tmp_path / "docs" / "09-architecture-decisions.md"
        summary.write_text("| 013 | something |\n")
        with pytest.raises(AssertionError, match="does not contain a row"):
            validate_adr_014(tmp_path)

    def test_fails_when_summary_has_false_positive_014(self, tmp_path) -> None:  # noqa: ANN001
        """Raises AssertionError when 014 appears outside the summary table row."""
        adr_dir = tmp_path / "docs" / "architecture-decisions"
        adr_dir.mkdir(parents=True)
        adr_file = adr_dir / "ADR-014-autonomous-execution-model.md"
        adr_file.write_text(
            "# ADR\n## Status\n## Context\n## Decision\n## Consequences\nOption A\nOption B\nOption C\nOption D\n"
        )
        summary = tmp_path / "docs" / "09-architecture-decisions.md"
        summary.write_text("Reference: ADR-014 path\n| 013 | something |\n")
        with pytest.raises(AssertionError, match="does not contain a row"):
            validate_adr_014(tmp_path)

    def test_fails_when_summary_file_missing(self, tmp_path) -> None:  # noqa: ANN001
        """Raises AssertionError when summary table file is missing."""
        adr_dir = tmp_path / "docs" / "architecture-decisions"
        adr_dir.mkdir(parents=True)
        adr_file = adr_dir / "ADR-014-autonomous-execution-model.md"
        adr_file.write_text(
            "# ADR\n## Status\n## Context\n## Decision\n## Consequences\nOption A\nOption B\nOption C\nOption D\n"
        )
        with pytest.raises(AssertionError, match="Summary table not found"):
            validate_adr_014(tmp_path)
