"""Tests for _title_case_display_name in issue_type_discovery."""

from __future__ import annotations

from agentic_devtools.cli.setup.issue_type_discovery import _title_case_display_name


class TestTitleCaseDisplayName:
    """Tests for the _title_case_display_name helper."""

    def test_underscores_replaced_and_title_cased(self) -> None:
        """story_points → 'Story Points'."""
        assert _title_case_display_name("story_points") == "Story Points"

    def test_camel_case_treated_as_single_word(self) -> None:
        """customField10042 → 'Customfield10042' (no camelCase splitting)."""
        assert _title_case_display_name("customField10042") == "Customfield10042"

    def test_single_word(self) -> None:
        """summary → 'Summary'."""
        assert _title_case_display_name("summary") == "Summary"

    def test_empty_string(self) -> None:
        """Empty string → empty string."""
        assert _title_case_display_name("") == ""

    def test_already_title_cased(self) -> None:
        """Already title-cased input remains unchanged."""
        assert _title_case_display_name("Story Points") == "Story Points"

    def test_multiple_underscores(self) -> None:
        """acceptance_criteria_notes → 'Acceptance Criteria Notes'."""
        assert _title_case_display_name("acceptance_criteria_notes") == "Acceptance Criteria Notes"
