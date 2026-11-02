"""Tests for _render_step_prompt function."""

from unittest.mock import patch

from agentic_devtools import state
from agentic_devtools.cli.workflows.manager import _render_step_prompt


class TestRenderStepPrompt:
    """Tests for _render_step_prompt function."""

    def test_state_values_added_to_variables(self, temp_state_dir):
        """State values for common keys should be added to template variables."""
        state.set_value("jira.issue_key", "PROJECT-999")
        state.set_value("commit_message", "fix: something")

        with patch(
            "agentic_devtools.cli.workflows.manager.load_and_render_prompt",
            return_value="rendered",
        ) as mock_render:
            _render_step_prompt("work-on-jira-issue", "implementation", {})

        call_kwargs = mock_render.call_args
        variables = call_kwargs.kwargs.get("variables") or call_kwargs[1].get("variables")
        assert variables["jira_issue_key"] == "PROJECT-999"
        assert variables["commit_message"] == "fix: something"

    def test_commit_message_sets_git_commit_usage(self, temp_state_dir):
        """When commit_message is set, git_commit_usage should be the short form."""
        state.set_value("commit_message", "feat: new feature")

        with patch(
            "agentic_devtools.cli.workflows.manager.load_and_render_prompt",
            return_value="rendered",
        ) as mock_render:
            _render_step_prompt("work-on-jira-issue", "commit", {})

        call_kwargs = mock_render.call_args
        variables = call_kwargs.kwargs.get("variables") or call_kwargs[1].get("variables")
        assert variables["git_commit_usage"] == "agdt-git-commit"

    def test_jira_update_state_keys_added_to_variables(self, temp_state_dir):
        """jira.user_request and jira.issue_* keys should be exposed to templates."""
        state.set_value("jira.issue_key", "PROJECT-42")
        state.set_value("jira.user_request", "Update the summary")
        state.set_value("jira.issue_summary", "Test Summary")
        state.set_value("jira.issue_type", "Story")
        state.set_value("jira.issue_labels", "backend, api")
        state.set_value("jira.issue_description", "Desc")
        state.set_value("jira.issue_comments", "Comments")

        with patch(
            "agentic_devtools.cli.workflows.manager.load_and_render_prompt",
            return_value="rendered",
        ) as mock_render:
            _render_step_prompt("update-jira-issue", "make-updates", {})

        call_kwargs = mock_render.call_args
        variables = call_kwargs.kwargs.get("variables") or call_kwargs[1].get("variables")
        assert variables["jira_user_request"] == "Update the summary"

    def test_jira_last_issue_fields_extracted(self, temp_state_dir):
        """jira.last_issue dict fields populate issue_* template variables."""
        state.set_value(
            "jira.last_issue",
            {"fields": {"summary": "S", "issuetype": {"name": "Bug"}, "labels": ["a", "b"], "description": "D"}},
        )

        with patch(
            "agentic_devtools.cli.workflows.manager.load_and_render_prompt",
            return_value="rendered",
        ) as mock_render:
            _render_step_prompt("work-on-jira-issue", "planning", {})

        call_kwargs = mock_render.call_args
        variables = call_kwargs.kwargs.get("variables") or call_kwargs[1].get("variables")
        assert variables["issue_summary"] == "S"

    def test_checklist_markdown_added_when_checklist_exists(self, temp_state_dir):
        """checklist_markdown uses the rendered checklist when one exists."""
        from unittest.mock import MagicMock

        mock_checklist = MagicMock()
        mock_checklist.render_markdown.return_value = "- [ ] item"

        with (
            patch(
                "agentic_devtools.cli.workflows.manager.load_and_render_prompt",
                return_value="rendered",
            ) as mock_render,
            patch(
                "agentic_devtools.cli.workflows.checklist.get_checklist",
                return_value=mock_checklist,
            ),
        ):
            _render_step_prompt("work-on-jira-issue", "implementation", {})

        call_kwargs = mock_render.call_args
        variables = call_kwargs.kwargs.get("variables") or call_kwargs[1].get("variables")
        assert variables["checklist_markdown"] == "- [ ] item"

    def test_warn_on_missing_is_false_for_create_jira_issue_initiate(self, temp_state_dir):
        """warn_on_missing should be False for create-jira-issue initiate."""
        with patch(
            "agentic_devtools.cli.workflows.manager.load_and_render_prompt",
            return_value="rendered",
        ) as mock_render:
            _render_step_prompt("create-jira-issue", "initiate", {})

        call_kwargs = mock_render.call_args
        warn_on_missing = (
            call_kwargs.kwargs.get("warn_on_missing") if call_kwargs.kwargs else call_kwargs[1].get("warn_on_missing")
        )
        assert warn_on_missing is False

    def test_non_dict_jira_last_issue_skips_field_extraction(self, temp_state_dir):
        """When jira_last_issue is a non-dict value, field extraction should be skipped."""
        # Pass jira_last_issue as a string (non-dict) in context
        context = {"jira_last_issue": "some-string-value"}

        with patch(
            "agentic_devtools.cli.workflows.manager.load_and_render_prompt",
            return_value="rendered",
        ) as mock_render:
            _render_step_prompt("work-on-jira-issue", "implementation", context)

        call_kwargs = mock_render.call_args
        variables = call_kwargs.kwargs.get("variables") or call_kwargs[1].get("variables")
        # issue_summary should not be set from fields extraction
        assert variables.get("issue_summary") is None or variables.get("issue_summary") == ""
