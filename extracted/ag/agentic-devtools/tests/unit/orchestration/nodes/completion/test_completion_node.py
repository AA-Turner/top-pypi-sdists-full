"""Tests for completion_node."""

from unittest.mock import patch

from agentic_devtools.orchestration.nodes.completion import (
    completion_node,
)


class TestCompletionNode:
    def test_fails_fast_when_issue_key_is_missing(self):
        """completion_node returns a failure immediately when issue_key is absent."""
        result = completion_node({})
        assert result["error"] == "issue_key is required and must be a non-empty string"
        assert result["step"] == "completion"
        assert result["status"] == "failed"
        assert result["events"][0]["event"] == "completion_failed"

    def test_fails_fast_when_issue_key_is_blank(self):
        """completion_node returns a failure immediately when issue_key is whitespace."""
        result = completion_node({"issue_key": "   "})
        assert result["error"] == "issue_key is required and must be a non-empty string"
        assert result["status"] == "failed"
        assert result["events"][0]["event"] == "completion_failed"

    def test_fails_fast_when_issue_key_is_non_string(self):
        """completion_node returns a failure immediately when issue_key is not a string."""
        for bad_value in [None, 42, True, []]:
            result = completion_node({"issue_key": bad_value})
            assert result["error"] == "issue_key is required and must be a non-empty string", bad_value
            assert result["step"] == "completion", bad_value
            assert result["status"] == "failed", bad_value
            assert result["events"][0]["event"] == "completion_failed", bad_value

    def test_sets_status_completed_jira(self):
        with patch(
            "agentic_devtools.orchestration.nodes.completion._post_jira_comment",
            return_value=True,
        ):
            result = completion_node(
                {
                    "issue_key": "TEST-1",
                    "issue_provider": "jira",
                    "pr_url": "http://pr",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            assert result["status"] == "completed"
            assert result["step"] == "completion"
            assert result["completion_comment_posted"] is True

    def test_emits_event(self):
        with patch(
            "agentic_devtools.orchestration.nodes.completion._post_jira_comment",
            return_value=True,
        ):
            result = completion_node(
                {
                    "issue_key": "TEST-1",
                    "issue_provider": "jira",
                    "pr_url": "",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            assert result["events"][0]["event"] == "completion_completed"

    def test_handles_github_provider(self):
        with patch(
            "agentic_devtools.orchestration.nodes.completion._post_github_comment",
            return_value=True,
        ) as mock_post:
            result = completion_node(
                {
                    "issue_key": "42",
                    "issue_provider": "github",
                    "pr_url": "",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            assert result["status"] == "completed"
            assert result["completion_comment_posted"] is True
            mock_post.assert_called_once()

    def test_dry_run_skips_posting(self):
        with (
            patch("agentic_devtools.orchestration.nodes.completion._post_jira_comment") as mock_jira,
            patch("agentic_devtools.orchestration.nodes.completion._post_github_comment") as mock_gh,
        ):
            result = completion_node(
                {
                    "issue_key": "TEST-1",
                    "issue_provider": "jira",
                    "dry_run": True,
                    "pr_url": "",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            assert result["completion_comment_posted"] is False
            assert result["dry_run_skipped"] is True
            mock_jira.assert_not_called()
            mock_gh.assert_not_called()

    def test_dry_run_logs_rendered_comment_preview(self, caplog):
        caplog.set_level("INFO")
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.format_completion_comment",
                return_value="rendered completion",
            ),
            patch("agentic_devtools.orchestration.nodes.completion._post_jira_comment") as mock_jira,
        ):
            result = completion_node(
                {
                    "issue_key": "TEST-1",
                    "issue_provider": "jira",
                    "dry_run": True,
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )

        assert result["dry_run_skipped"] is True
        assert "rendered completion" in caplog.text
        mock_jira.assert_not_called()

    def test_truthy_non_bool_dry_run_does_not_skip(self):
        """A truthy non-bool dry_run value (e.g. string '1') must NOT skip posting."""
        with (
            patch("agentic_devtools.orchestration.nodes.completion._post_jira_comment", return_value=True) as mock_jira,
            patch("agentic_devtools.orchestration.nodes.completion._post_github_comment") as mock_gh,
        ):
            result = completion_node(
                {
                    "issue_key": "TEST-1",
                    "issue_provider": "jira",
                    "dry_run": "1",
                    "pr_url": "",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            assert result["dry_run_skipped"] is False
            mock_jira.assert_called_once()
            mock_gh.assert_not_called()

    def test_github_comment_post_success(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter") as mock_adapter_cls,
        ):
            from agentic_devtools.orchestration.nodes.completion import _post_github_comment

            result = _post_github_comment("#42", "test comment")
            assert result is True
            mock_adapter_cls.return_value.add_comment.assert_called_once_with("42", "test comment")

    def test_github_comment_skipped_when_normalized_issue_key_empty(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.orchestration.nodes.completion.normalize_github_issue_number",
                return_value="",
            ),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter") as mock_adapter_cls,
        ):
            from agentic_devtools.orchestration.nodes.completion import _post_github_comment

            result = _post_github_comment("#", "test comment")
            assert result is False
            mock_adapter_cls.assert_not_called()

    def test_github_comment_post_exception_suppressed(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                side_effect=RuntimeError("no config"),
            ),
        ):
            from agentic_devtools.orchestration.nodes.completion import _post_github_comment

            result = _post_github_comment("42", "test comment")
            assert result is False

    def test_github_comment_skipped_when_repo_unresolvable(self):
        with patch(
            "agentic_devtools.orchestration.nodes.completion.resolve_github_repo_safe",
            return_value=None,
        ):
            from agentic_devtools.orchestration.nodes.completion import _post_github_comment

            result = _post_github_comment("42", "test comment")
            assert result is False

    def test_continues_on_jira_comment_failure(self):
        with patch(
            "agentic_devtools.orchestration.nodes.completion._post_jira_comment",
            return_value=False,
        ):
            result = completion_node(
                {
                    "issue_key": "TEST-1",
                    "issue_provider": "jira",
                    "pr_url": "",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            assert result["status"] == "completed"
            assert result["completion_comment_posted"] is False

    def test_maps_existing_workflow_outputs_into_completion_data(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.format_completion_comment",
                return_value="formatted",
            ) as mock_format,
            patch("agentic_devtools.orchestration.nodes.completion._post_jira_comment", return_value=True),
        ):
            completion_node(
                {
                    "issue_key": "TEST-1",
                    "issue_provider": "jira",
                    "checklist_items": [
                        {"description": "Implement feature", "is_complete": True},
                        {"description": "Write tests", "is_complete": True},
                    ],
                    "implementation_log": [
                        {"item_index": 0, "status": "completed"},
                        {"item_index": 1, "status": "completed"},
                    ],
                    "affected_paths": ["agentic_devtools/foo.py", "tests/unit/foo/test_bar.py"],
                    "verification_output": "All targeted checks passed",
                    "events": [{"event": "verification_passed", "timestamp": "2026-01-01T00:00:00Z"}],
                    "token_usage_prompt": 10,
                    "token_usage_completion": 5,
                }
            )

        completion_data = mock_format.call_args.args[0]
        assert "Implement feature" in completion_data["what_was_done"]
        assert "agentic_devtools/foo.py" in completion_data["what_was_done"]
        assert completion_data["quality_gates"] == [
            {"name": "Targeted checks", "status": "pass", "details": "All targeted checks passed"}
        ]

    def test_maps_non_list_verification_events_to_failed_quality_gate(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.format_completion_comment",
                return_value="formatted",
            ) as mock_format,
            patch("agentic_devtools.orchestration.nodes.completion._post_jira_comment", return_value=True),
        ):
            completion_node(
                {
                    "issue_key": "TEST-1",
                    "issue_provider": "jira",
                    "checklist_items": [],
                    "verification_output": "checks output present",
                    "events": {"event": "verification_passed"},
                    "token_usage_prompt": 1,
                    "token_usage_completion": 1,
                }
            )

        completion_data = mock_format.call_args.args[0]
        assert completion_data["quality_gates"] == [
            {"name": "Targeted checks", "status": "fail", "details": "checks output present"}
        ]

    def test_derives_github_provider_from_issue_key_when_missing(self):
        """When issue_provider is absent, derive from issue_key to avoid posting to Jira."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion._post_github_comment",
                return_value=True,
            ) as mock_gh,
            patch(
                "agentic_devtools.orchestration.nodes.completion._post_jira_comment",
            ) as mock_jira,
        ):
            completion_node(
                {
                    "issue_key": "42",
                    "pr_url": "",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            mock_gh.assert_called_once()
            mock_jira.assert_not_called()

    def test_derives_jira_provider_from_issue_key_when_missing(self):
        """Jira-format issue_key without issue_provider must post to Jira."""
        with patch(
            "agentic_devtools.orchestration.nodes.completion._post_jira_comment",
            return_value=True,
        ):
            result = completion_node(
                {
                    "issue_key": "TEST-1",
                    "pr_url": "",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            assert result["status"] == "completed"

    def test_derives_provider_when_issue_provider_is_invalid(self):
        """An invalid issue_provider must fall back to detection from issue_key (GitHub numeric)."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion._post_github_comment",
                return_value=True,
            ) as mock_gh,
            patch(
                "agentic_devtools.orchestration.nodes.completion._post_jira_comment",
            ) as mock_jira,
        ):
            completion_node(
                {
                    "issue_key": "42",
                    "issue_provider": "corrupted",
                    "pr_url": "",
                    "checklist_items": [],
                    "token_usage_prompt": 0,
                    "token_usage_completion": 0,
                }
            )
            mock_gh.assert_called_once()
            mock_jira.assert_not_called()

    def test_derives_provider_when_issue_provider_is_unhashable(self):
        """An unhashable issue_provider (dict/list) must not raise TypeError — fall back to detection."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion._post_github_comment",
                return_value=True,
            ) as mock_gh,
            patch(
                "agentic_devtools.orchestration.nodes.completion._post_jira_comment",
            ) as mock_jira,
        ):
            for bad_value in [{"corrupted": True}, ["jira"], [42]]:
                mock_gh.reset_mock()
                mock_jira.reset_mock()
                completion_node(
                    {
                        "issue_key": "42",
                        "issue_provider": bad_value,
                        "pr_url": "",
                        "checklist_items": [],
                        "token_usage_prompt": 0,
                        "token_usage_completion": 0,
                    }
                )
                mock_gh.assert_called_once(), bad_value
                mock_jira.assert_not_called(), bad_value


class TestPostJiraComment:
    def test_success_returns_true(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
            ) as mock_config,
            patch(
                "agentic_devtools.tools.jira.add_comment",
            ),
        ):
            from agentic_devtools.orchestration.nodes.completion import _post_jira_comment

            result = _post_jira_comment("TEST-1", "comment")
            assert result is True
            mock_config.assert_called_once()

    def test_failure_returns_false(self):
        with patch(
            "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
            side_effect=ValueError("no PAT"),
        ):
            from agentic_devtools.orchestration.nodes.completion import _post_jira_comment

            result = _post_jira_comment("TEST-1", "comment")
            assert result is False
