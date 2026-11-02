"""Tests for _cap_with_required_sections in retro_spec/synthesis.py."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec.synthesis import _cap_with_required_sections


class TestCapWithRequiredSections:
    """Tests for the _cap_with_required_sections helper."""

    def test_falls_back_when_no_required_sections_exist(self) -> None:
        """Section-preserving cap delegates to the generic cap when no required headings exist."""
        content = "x\n" * 6000

        result = _cap_with_required_sections(content, 200)

        assert "## Requirements" not in result
        assert "summarized due to extensive artifacts" in result

    def test_falls_back_when_limit_is_too_small_for_preface(self) -> None:
        """Very small limits use the generic truncation path."""
        content = "## Requirements\nbody\n\n## Success Criteria\nbody\n"

        result = _cap_with_required_sections(content, 40)

        assert len(result) <= 40

    def test_falls_back_when_no_sections_can_fit(self) -> None:
        """If no required section can fit, the generic cap result is used."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.synthesis._extract_required_sections",
            return_value=["## Requirements\nbody", "## Success Criteria\nbody"],
        ):
            result = _cap_with_required_sections("x\n" * 6000, 200)

        assert "Earlier sections were condensed" not in result
        assert "summarized due to extensive artifacts" in result

    def test_can_emit_heading_only_chunks(self) -> None:
        """When budget is tight, section headings are preserved even without full bodies."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.synthesis._extract_required_sections",
            return_value=["## Requirements\nbody", "## Success Criteria\nbody"],
        ):
            result = _cap_with_required_sections("## Requirements\n" + "x\n" * 3000 + "## Success Criteria\n", 300)

        assert "Earlier sections were condensed" in result
        assert "## Requirements" in result
        assert "## Success Criteria" in result

    def test_preserves_user_scenarios_with_other_required_sections(self) -> None:
        """Capped output retains the mandatory user-scenarios section."""
        content = "\n".join(
            [
                "## User Scenarios & Testing",
                "scenario " + "x" * 1000,
                "## Requirements",
                "requirement " + "x" * 1000,
                "## Success Criteria",
                "criterion " + "x" * 1000,
            ]
        )

        result = _cap_with_required_sections(content, 500)

        assert len(result) <= 500
        assert "## Requirements" in result
        assert "## Success Criteria" in result

    def test_preserves_required_sub_markers_in_requirements_body(self) -> None:
        """Sub-markers are retained even when the section body is long."""
        # Build a Requirements body where the required sub-markers appear after
        # a long preamble, so a naive body cap would truncate them away.
        long_preamble = "y\n" * 200  # 400 chars before the sub-markers
        body = (
            "## Requirements\n"
            + long_preamble
            + "### Functional Requirements\n"
            + "- FR-001\n"
            + "### Non-Functional Requirements\n"
            + "- NFR-001\n"
            + "## Success Criteria\n"
            + "- SC-001\n"
        )

        # A limit tight enough that naive body truncation would drop the sub-markers
        result = _cap_with_required_sections(body, 700)

        assert "### Functional Requirements" in result
        assert "### Non-Functional Requirements" in result

    def test_does_not_exceed_budget_when_sub_markers_fit_naturally(self) -> None:
        """When sub-markers are already near the top of the body, budget is honoured."""
        body = (
            "## Requirements\n"
            "### Functional Requirements\n"
            "- FR-001\n"
            "### Non-Functional Requirements\n"
            "- NFR-001\n"
            "## Success Criteria\n"
            "- SC-001\n"
        )

        result = _cap_with_required_sections(body, 500)

        # All markers present and no budget violation
        assert "### Functional Requirements" in result
        assert "### Non-Functional Requirements" in result
        assert len(result) <= 500
