"""Tests for extract_acceptance_criteria."""

from __future__ import annotations

from agentic_devtools.orchestration.nodes._issue_retrieval import extract_acceptance_criteria


class TestExtractAcceptanceCriteria:
    """Tests for ATX heading-based acceptance criteria extraction."""

    def test_returns_none_for_none_input(self) -> None:
        assert extract_acceptance_criteria(None) is None

    def test_returns_none_for_empty_string(self) -> None:
        assert extract_acceptance_criteria("") is None

    def test_returns_none_when_no_headings(self) -> None:
        assert extract_acceptance_criteria("Just some text without headings") is None

    def test_returns_none_when_no_matching_heading(self) -> None:
        desc = "## Overview\nSome overview text\n## Design\nDesign text"
        assert extract_acceptance_criteria(desc) is None

    def test_extracts_acceptance_criteria_heading(self) -> None:
        desc = "## Overview\nSome text\n## Acceptance Criteria\n- Item 1\n- Item 2\n## Notes\nOther"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "- Item 1" in result
        assert "- Item 2" in result
        assert "Other" not in result

    def test_extracts_ac_heading(self) -> None:
        desc = "## Overview\nText\n## AC\n- Criterion A\n- Criterion B"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "Criterion A" in result

    def test_extracts_definition_of_done_heading(self) -> None:
        desc = "## Definition of Done\n- Done item 1\n## Other\nStuff"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "Done item 1" in result

    def test_priority_order_acceptance_criteria_first(self) -> None:
        desc = "## AC\nAC content\n## Acceptance Criteria\nAC full content"
        result = extract_acceptance_criteria(desc)
        # "Acceptance Criteria" has higher priority than "AC"
        assert result is not None
        assert "AC full content" in result

    def test_extracts_until_same_level_heading(self) -> None:
        desc = "## Acceptance Criteria\nContent here\n## Next Section\nOther content"
        result = extract_acceptance_criteria(desc)
        assert result == "Content here"

    def test_extracts_until_eof_when_last_section(self) -> None:
        desc = "## Overview\nText\n## Acceptance Criteria\n- Last section content"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "Last section content" in result

    def test_case_insensitive_heading_match(self) -> None:
        desc = "## acceptance criteria\n- Item"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "Item" in result

    def test_returns_none_for_empty_section(self) -> None:
        desc = "## Acceptance Criteria\n## Next"
        result = extract_acceptance_criteria(desc)
        assert result is None


class TestExtractAcceptanceCriteriaBranches:
    """Cover the heading-end search loop exhaustion branch."""

    def test_ac_heading_is_last_heading(self) -> None:
        """When AC heading is the last heading, loop exhausts without break."""
        text = "# Intro\nSome text\n## Acceptance Criteria\n- Crit 1\n- Crit 2"
        result = extract_acceptance_criteria(text)
        assert result is not None
        assert "Crit 1" in result
        assert "Crit 2" in result


class TestExtractACDeeperHeadingDoesNotEnd:
    """A deeper heading after AC doesn't terminate the section."""

    def test_deeper_heading_included_in_ac(self) -> None:
        text = "## Acceptance Criteria\n- Must work\n### Sub-section\n- Detail\n## Other Section\nStuff"
        result = extract_acceptance_criteria(text)
        assert result is not None
        assert "Must work" in result
        assert "Detail" in result
        assert "Stuff" not in result


class TestExtractAcceptanceCriteriaJiraWiki:
    """Tests for Jira wiki heading-based acceptance criteria extraction."""

    def test_jira_h3_plain(self) -> None:
        desc = "h2. Overview\nSome text\nh3. Acceptance Criteria\n- Item 1\n- Item 2\nh2. Notes\nOther"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "Item 1" in result
        assert "Item 2" in result
        assert "Other" not in result

    def test_jira_h3_decorated_plus(self) -> None:
        """+...+ Jira underline markup is stripped before matching."""
        desc = "h2. Overview\nSome text\nh3. +Acceptance Criteria+\n- Crit A\n- Crit B\nh2. Notes\n"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "Crit A" in result
        assert "Crit B" in result

    def test_jira_definition_of_done(self) -> None:
        desc = "h3. Definition of Done\n- Done item\nh3. Other\nStuff"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "Done item" in result

    def test_jira_ac_heading_last_section(self) -> None:
        desc = "h2. Overview\nText\nh3. Acceptance Criteria\n- Last item"
        result = extract_acceptance_criteria(desc)
        assert result is not None
        assert "Last item" in result

    def test_jira_empty_ac_section_returns_none(self) -> None:
        desc = "h3. Acceptance Criteria\nh3. Next Section\n"
        result = extract_acceptance_criteria(desc)
        assert result is None
