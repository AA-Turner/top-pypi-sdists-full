"""Tests for _author_section_lead_in()."""

from agentic_devtools.cli.ci.github_provider import _author_section_lead_in

#: The recording contract stated under the author section's own heading.
_RECORDING_CONTRACT = (
    "These comments have no review thread of their own. Record your decision on each one — the option you "
    "chose and the rationale behind it — in the summary comment you post on the PR when you have completed "
    "your work, so I know what was decided in each case and why."
)


class TestAuthorSectionLeadIn:
    """Tests for the heading and recording contract introducing the PR author's own comments."""

    def test_emits_the_hidden_marker_and_the_visible_heading_in_that_order(self) -> None:
        """The visible heading is authoritative; the hidden marker is a machine-readable copy."""
        entries = _author_section_lead_in()
        assert entries[1] == "<!-- repair-section:author-comments -->"
        assert entries[2] == "## Comments from the PR author"

    def test_states_the_recording_contract_under_the_heading(self) -> None:
        """Author comments have no thread to reply on, so decisions go in the summary comment."""
        assert _author_section_lead_in()[4] == _RECORDING_CONTRACT

    def test_returns_exactly_five_entries_owning_its_leading_blank(self) -> None:
        """The shared decision block always precedes it, so the lead-in owns the separating blank."""
        entries = _author_section_lead_in()
        assert len(entries) == 5
        assert entries[0] == ""
        assert entries[3] == ""

    def test_carries_no_collapsed_markup(self) -> None:
        """Content inside a ``<details>`` block does not reach the cloud coding agent."""
        assert not any("<details>" in entry or "<summary>" in entry for entry in _author_section_lead_in())
