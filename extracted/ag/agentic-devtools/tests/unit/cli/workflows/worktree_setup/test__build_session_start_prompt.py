"""Tests for _build_session_start_prompt."""

from agentic_devtools.cli.workflows.worktree_setup import _build_session_start_prompt


class TestBuildSessionStartPrompt:
    """Tests for the _build_session_start_prompt helper."""

    def test_contains_the_exact_relative_path(self):
        """The prompt must include the exact path that was passed in."""
        path = ".agdt/workflows/_unscoped/temp-pull-request-review-initiate-prompt.md"
        result = _build_session_start_prompt(path)
        assert path in result

    def test_is_single_line(self):
        """The returned prompt must not contain newline characters."""
        result = _build_session_start_prompt("some/relative/path.md")
        assert "\n" not in result

    def test_contains_no_template_variables(self):
        """The returned prompt must be a static string with no {{ }} placeholders."""
        result = _build_session_start_prompt("some/relative/path.md")
        assert "{{" not in result
        assert "}}" not in result

    def test_contains_no_at_agent_handoff(self):
        """The returned prompt must not reference an @-prefixed agent name."""
        result = _build_session_start_prompt("some/relative/path.md")
        assert "@agdt." not in result

    def test_contains_no_glob_wildcards(self):
        """The returned prompt must not contain shell glob wildcards."""
        path = ".agdt/workflows/_unscoped/temp-work-on-jira-issue-planning-prompt.md"
        result = _build_session_start_prompt(path)
        assert "*" not in result

    def test_different_paths_produce_different_prompts(self):
        """Two distinct paths must produce two distinct prompt strings."""
        path_a = ".agdt/workflows/_unscoped/temp-pr-review-initiate-prompt.md"
        path_b = ".agdt/workflows/_unscoped/temp-work-on-jira-issue-planning-prompt.md"
        assert _build_session_start_prompt(path_a) != _build_session_start_prompt(path_b)
