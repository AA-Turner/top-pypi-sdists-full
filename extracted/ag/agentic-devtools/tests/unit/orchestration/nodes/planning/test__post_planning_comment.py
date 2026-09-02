"""Tests for _post_planning_comment."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes.planning import _post_planning_comment


class TestPostPlanningComment:
    def test_jira_success(self):
        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment.__wrapped__", create=True),
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config"),
            patch("agentic_devtools.tools.jira.add_comment"),
        ):
            result = _post_planning_comment("TEST-1", "the plan", {"issue_key": "TEST-1", "issue_provider": "jira"})
            assert result is True

    def test_github_success(self):
        with (
            patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo"),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter") as mock_cls,
        ):
            result = _post_planning_comment("#42", "the plan", {"issue_key": "#42", "issue_provider": "github"})
            assert result is True
            mock_cls.return_value.add_comment.assert_called_once()

    def test_github_no_repo_returns_false(self):
        with patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value=None):
            result = _post_planning_comment("42", "plan", {"issue_key": "42", "issue_provider": "github"})
            assert result is False

    def test_github_empty_key_returns_false(self):
        with patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="o/r"):
            result = _post_planning_comment("#", "plan", {"issue_key": "#", "issue_provider": "github"})
            assert result is False

    def test_jira_failure_returns_false(self):
        with patch(
            "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
            side_effect=ValueError("no PAT"),
        ):
            result = _post_planning_comment("TEST-1", "plan", {"issue_key": "TEST-1", "issue_provider": "jira"})
            assert result is False

    def test_passes_structured_sections_to_formatter(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning.format_planning_comment",
                return_value="formatted",
            ) as mock_format,
            patch("agentic_devtools.tools.jira.add_comment"),
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config"),
        ):
            result = _post_planning_comment(
                "TEST-1",
                "plan",
                {"issue_provider": "jira"},
                tasks=["Task A"],
                affected_files=["src/a.py"],
                risks=["Regression"],
            )

        assert result is True
        mock_format.assert_called_once_with(
            "plan",
            "jira",
            mock_format.call_args.args[2],
            tasks=["Task A"],
            affected_files=["src/a.py"],
            risks=["Regression"],
        )


class TestPostPlanningCommentIdempotency:
    """Idempotency paths in _post_planning_comment."""

    def test_cache_hit_skips_api_and_returns_true(self):
        """If registry has a successful cached result, the API is not called."""
        fake_entry = MagicMock(status="success")
        fake_registry = MagicMock()
        fake_registry.check.return_value = fake_entry

        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning.build_idempotency_registry",
                return_value=fake_registry,
            ),
            patch(
                "agentic_devtools.orchestration.nodes._helpers.get_run_id",
                return_value="run-abc",
            ),
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config") as mock_config,
        ):
            result = _post_planning_comment("TEST-1", "plan", {"issue_provider": "jira"})

        assert result is True
        mock_config.assert_not_called()

    def test_no_cache_hit_calls_api_and_records(self):
        """When cache misses, the API is called and the result is recorded."""
        fake_registry = MagicMock()
        fake_registry.check.return_value = None

        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning.build_idempotency_registry",
                return_value=fake_registry,
            ),
            patch(
                "agentic_devtools.orchestration.nodes._helpers.get_run_id",
                return_value="run-abc",
            ),
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config"),
            patch("agentic_devtools.tools.jira.add_comment"),
        ):
            result = _post_planning_comment("TEST-1", "plan", {"issue_provider": "jira"})

        assert result is True
        fake_registry.record.assert_called_once()

    def test_no_registry_still_posts(self):
        """When run_id is absent, registry is None and the API is called directly."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning.build_idempotency_registry",
                return_value=None,
            ),
            patch(
                "agentic_devtools.orchestration.nodes._helpers.get_run_id",
                return_value=None,
            ),
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config"),
            patch("agentic_devtools.tools.jira.add_comment"),
        ):
            result = _post_planning_comment("TEST-1", "plan", {"issue_provider": "jira"})

        assert result is True

    def test_idempotency_key_excludes_volatile_comment_for_github(self):
        """Idempotency key uses stable issue identity instead of full comment payload."""
        fake_registry = MagicMock()
        fake_registry.check.return_value = None

        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning.build_idempotency_registry",
                return_value=fake_registry,
            ),
            patch(
                "agentic_devtools.orchestration.nodes._helpers.get_run_id",
                return_value="run-abc",
            ),
            patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo"),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter"),
        ):
            result = _post_planning_comment("#42", "plan text", {"issue_provider": "github"})

        assert result is True
        fake_registry.check.assert_called_once_with("github_add_comment", {"issue_number": "42"}, "planning")
        fake_registry.record.assert_called_once_with(
            "github_add_comment",
            {"issue_number": "42"},
            "planning",
            result_summary="success",
        )
