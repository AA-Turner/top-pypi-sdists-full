"""Tests for _extract_required_sections in retro_spec/synthesis.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.synthesis import _extract_required_sections


class TestExtractRequiredSections:
    """Tests for the _extract_required_sections helper."""

    def test_ignores_empty_required_blocks(self) -> None:
        """Empty required sections are skipped by the extractor."""
        content = "\n".join(
            ["## User Scenarios & Testing", "scenario", "## Requirements", "## Success Criteria", "details"]
        )

        sections = _extract_required_sections(content)

        assert sections == ["## User Scenarios & Testing\nscenario", "## Success Criteria\ndetails"]

    def test_extracts_artifact_availability_section(self) -> None:
        """Artifact Availability is extracted as a required section."""
        content = "\n".join(
            [
                "## Artifact Availability",
                "No PR diffs available.",
                "## User Scenarios & Testing",
                "scenario",
                "## Requirements",
                "### Functional Requirements",
                "- FR1",
                "### Non-Functional Requirements",
                "- NFR1",
                "## Success Criteria",
                "- SC1",
            ]
        )

        sections = _extract_required_sections(content)

        assert sections[0].startswith("## Artifact Availability")
        assert "No PR diffs available." in sections[0]
