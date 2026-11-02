"""Tests for _ci_section_lead_in()."""

from agentic_devtools.cli.ci.github_provider import _ci_section_lead_in


class TestCiSectionLeadIn:
    """Tests for the lead-in and heading introducing the failing CI checks."""

    def test_opening_form_leads_with_the_failures(self) -> None:
        assert _ci_section_lead_in(3, is_first_section=True) == [
            "@copilot please fix the following ci failures:",
            "",
            "## CI failures",
        ]

    def test_opening_form_single_failure_uses_singular_wording(self) -> None:
        assert _ci_section_lead_in(1, is_first_section=True)[0] == "@copilot please fix the following ci failure:"

    def test_continuation_form_leads_with_the_failures(self) -> None:
        assert _ci_section_lead_in(3, is_first_section=False)[1] == (
            "Additionally, CI checks are failing — please fix the following ci failures:"
        )

    def test_continuation_form_single_failure_uses_singular_wording(self) -> None:
        assert _ci_section_lead_in(1, is_first_section=False)[1] == (
            "Additionally, CI checks are failing — please fix the following ci failure:"
        )

    def test_both_forms_end_on_the_visible_section_heading(self) -> None:
        """The heading mirrors the two comment sections, immediately above the failure blocks."""
        assert _ci_section_lead_in(2, is_first_section=True)[-1] == "## CI failures"
        assert _ci_section_lead_in(2, is_first_section=False)[-1] == "## CI failures"

    def test_continuation_form_owns_the_separating_blank_line(self) -> None:
        """Never a trailing blank — the first CI failure block supplies that itself."""
        assert len(_ci_section_lead_in(2, is_first_section=True)) == 3
        continuation = _ci_section_lead_in(2, is_first_section=False)
        assert len(continuation) == 4
        assert continuation[0] == ""
