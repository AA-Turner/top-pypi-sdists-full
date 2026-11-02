"""Tests for _post_jira_comment."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class TestPostJiraCommentIdempotency:
    """Idempotency paths in _post_jira_comment."""

    def test_cache_hit_skips_api_and_returns_true(self):
        from agentic_devtools.orchestration.nodes.completion import _post_jira_comment

        fake_entry = MagicMock(status="success")
        fake_registry = MagicMock()
        fake_registry.check.return_value = fake_entry

        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.build_idempotency_registry",
                return_value=fake_registry,
            ),
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config") as mock_config,
        ):
            result = _post_jira_comment("TEST-1", "comment", run_id="run-abc")

        assert result is True
        mock_config.assert_not_called()

    def test_no_cache_hit_calls_api_and_records(self):
        from agentic_devtools.orchestration.nodes.completion import _post_jira_comment

        fake_registry = MagicMock()
        fake_registry.check.return_value = None

        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.build_idempotency_registry",
                return_value=fake_registry,
            ),
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config"),
            patch("agentic_devtools.tools.jira.add_comment"),
        ):
            result = _post_jira_comment("TEST-1", "comment", run_id="run-abc")

        assert result is True
        fake_registry.record.assert_called_once()

    def test_no_registry_posts_directly(self):
        from agentic_devtools.orchestration.nodes.completion import _post_jira_comment

        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.build_idempotency_registry",
                return_value=None,
            ),
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config"),
            patch("agentic_devtools.tools.jira.add_comment"),
        ):
            result = _post_jira_comment("TEST-1", "comment", run_id=None)

        assert result is True
