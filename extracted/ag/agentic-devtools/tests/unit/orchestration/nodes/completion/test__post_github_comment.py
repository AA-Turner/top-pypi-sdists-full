"""Tests for _post_github_comment."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class TestPostGithubCommentIdempotency:
    """Idempotency paths in _post_github_comment."""

    def test_cache_hit_skips_api_and_returns_true(self):
        from agentic_devtools.orchestration.nodes.completion import _post_github_comment

        fake_entry = MagicMock(status="success")
        fake_registry = MagicMock()
        fake_registry.check.return_value = fake_entry

        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.build_idempotency_registry",
                return_value=fake_registry,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.completion.resolve_github_repo_safe",
                return_value="owner/repo",
            ) as mock_repo,
        ):
            result = _post_github_comment("42", "comment", run_id="run-abc")

        assert result is True
        mock_repo.assert_not_called()

    def test_no_cache_hit_calls_api_and_records(self):
        from agentic_devtools.orchestration.nodes.completion import _post_github_comment

        fake_registry = MagicMock()
        fake_registry.check.return_value = None

        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.build_idempotency_registry",
                return_value=fake_registry,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.completion.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter"),
        ):
            result = _post_github_comment("42", "comment", run_id="run-abc")

        assert result is True
        fake_registry.record.assert_called_once()

    def test_no_registry_posts_directly(self):
        from agentic_devtools.orchestration.nodes.completion import _post_github_comment

        with (
            patch(
                "agentic_devtools.orchestration.nodes.completion.build_idempotency_registry",
                return_value=None,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.completion.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter"),
        ):
            result = _post_github_comment("42", "comment", run_id=None)

        assert result is True
