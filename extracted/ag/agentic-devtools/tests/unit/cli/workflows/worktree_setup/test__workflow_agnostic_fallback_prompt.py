"""Tests for the _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT constant."""

from agentic_devtools.cli.workflows.worktree_setup import _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT


class TestWorkflowAgnosticFallbackPrompt:
    """Tests for the workflow-agnostic fallback start prompt."""

    def test_prompt_is_single_line(self):
        """The fallback prompt must have no newline characters."""
        assert "\n" not in _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT

    def test_prompt_names_the_agdt_command(self):
        """The prompt must name the agdt-get-next-workflow-prompt command."""
        assert "agdt-get-next-workflow-prompt" in _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT

    def test_prompt_does_not_name_an_at_mention_agent(self):
        """The prompt must not reference an @-prefixed agent name."""
        assert "@agdt." not in _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT

    def test_prompt_does_not_contain_template_variables(self):
        """The prompt must be a static string with no template variables."""
        assert "{{" not in _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT
        assert "}}" not in _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT
