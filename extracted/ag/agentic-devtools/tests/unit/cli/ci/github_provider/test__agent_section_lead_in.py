"""Tests for _agent_section_lead_in()."""

from agentic_devtools.cli.ci.github_provider import _agent_section_lead_in

_CLOSING_PARAGRAPH = (
    "For these comments, please reply to each one with your decision and the rationale behind it. If you made "
    "changes as a result of the comment, link the commit where the changes can be found in the reply. If you "
    "create a follow-up issue (option 4), link the follow-up issue in the reply. If you decided on option 4 but "
    "fail to create the follow-up issue for whatever reason, include everything needed to create it (title, "
    "body, labels, issue type, etc.) in a `<details>` block at the end of your reply to that comment. After you "
    "have replied to each comment, ensure that it is resolved and closed as well, so that those comments no "
    "longer block a merge."
)


class TestAgentSectionLeadIn:
    """Tests for the heading and reply contract introducing the Code Review Agent's comments."""

    def test_emits_the_hidden_marker_and_the_visible_heading_in_that_order(self) -> None:
        """The visible heading is authoritative; the hidden marker is a machine-readable copy."""
        entries = _agent_section_lead_in(2, is_first_section=True)
        assert entries[0] == ""
        assert entries[1] == "<!-- repair-section:code-review-agent-comments -->"
        assert entries[2] == "## Comments from the Code Review Agent"

    def test_opening_form_omits_the_restated_count_paragraph(self) -> None:
        """When the section is first, the count already opened the body."""
        entries = _agent_section_lead_in(2, is_first_section=True)
        assert len(entries) == 5
        assert entries[3] == ""
        assert entries[4] == _CLOSING_PARAGRAPH

    def test_continuation_form_restates_the_count_under_the_heading(self) -> None:
        """An author section opened the body, so the agent count is restated in its own section."""
        entries = _agent_section_lead_in(2, is_first_section=False)
        assert len(entries) == 7
        assert entries[4] == "Additionally, there were 2 comments left by the Code Review Agent."
        assert entries[5] == ""
        assert entries[6] == _CLOSING_PARAGRAPH

    def test_continuation_form_uses_the_singular_wording_for_one_comment(self) -> None:
        entries = _agent_section_lead_in(1, is_first_section=False)
        assert entries[4] == "Additionally, there was a comment left by the Code Review Agent."

    def test_does_not_duplicate_the_shared_decision_framework(self) -> None:
        """The four-option framework is emitted once per dispatch, above every section."""
        joined = "\n".join(_agent_section_lead_in(2, is_first_section=True))
        assert "Therefore, for each comment you have 4 options:" not in joined
        assert "1. Accept the comment and implement it as suggested." not in joined

    def test_carries_no_collapsed_markup_of_its_own(self) -> None:
        """The only ``<details>`` mention is the one the agent writes into *its* reply."""
        entries = _agent_section_lead_in(1, is_first_section=True)
        assert not any(entry.startswith("<details>") or "<summary>" in entry for entry in entries)
