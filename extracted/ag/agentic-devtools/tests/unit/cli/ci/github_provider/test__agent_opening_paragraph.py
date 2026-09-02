"""Tests for _agent_opening_paragraph()."""

from agentic_devtools.cli.ci.github_provider import _agent_opening_paragraph


class TestAgentOpeningParagraph:
    """Tests for the paragraph naming how many Code Review Agent comments were left."""

    def test_opening_plural_form(self) -> None:
        assert _agent_opening_paragraph(2, is_first_section=True) == (
            "@copilot - there were 2 comments left by the Code Review Agent."
        )

    def test_opening_singular_form(self) -> None:
        assert _agent_opening_paragraph(1, is_first_section=True) == (
            "@copilot - there was a comment left by the Code Review Agent."
        )

    def test_continuation_plural_form(self) -> None:
        assert _agent_opening_paragraph(2, is_first_section=False) == (
            "Additionally, there were 2 comments left by the Code Review Agent."
        )

    def test_continuation_singular_form(self) -> None:
        assert _agent_opening_paragraph(1, is_first_section=False) == (
            "Additionally, there was a comment left by the Code Review Agent."
        )

    def test_does_not_carry_the_decision_framework(self) -> None:
        """The four-option framework is shared with the author section and emitted once."""
        assert "4 options" not in _agent_opening_paragraph(2, is_first_section=True)
        assert "blindly" not in _agent_opening_paragraph(2, is_first_section=True)
