"""Tests for apply_pr_suggestions_via_browser."""

from __future__ import annotations

import contextlib
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.github import browser_apply_autofix
from agentic_devtools.cli.github.browser_apply_autofix import apply_pr_suggestions_via_browser


def _patches(page, drain_result, captured_kwargs=None):
    @contextlib.contextmanager
    def fake_ctx(credentials=None, **kwargs):
        if captured_kwargs is not None:
            captured_kwargs.update(kwargs)
        yield page

    return (
        patch.object(browser_apply_autofix, "load_credentials", return_value=MagicMock()),
        patch.object(browser_apply_autofix, "_authenticated_page", fake_ctx),
        patch.object(browser_apply_autofix, "drain_commit_rescan", return_value=drain_result),
    )


class TestApplyPrSuggestionsViaBrowser:
    """Tests for apply_pr_suggestions_via_browser."""

    def test_dry_run_returns_without_resolving(self) -> None:
        page = MagicMock()
        drain = {"candidates": 4, "commits": 0, "iterations": 1, "dry_run": True}
        captured_kwargs: dict = {}
        p_load, p_ctx, p_drain = _patches(page, drain, captured_kwargs)
        with (
            p_load,
            p_ctx,
            p_drain,
            patch.object(browser_apply_autofix, "_resolve_threads") as mock_resolve,
            patch.object(browser_apply_autofix, "_fetch_pr_head_sha") as mock_sha,
        ):
            result = apply_pr_suggestions_via_browser(7, "owner/repo", dry_run=True)
        assert result["applied"] == 4
        assert result["commits"] == 0
        assert result["dry_run"] is True
        assert result["resolution"] is None
        mock_resolve.assert_not_called()
        mock_sha.assert_not_called()
        # Authentication (and any lazy login) is checked against the target PR
        # URL rather than the GitHub home page — see _authenticated_page.
        assert captured_kwargs["target_url"] == "https://github.com/owner/repo/pull/7"

    def test_applies_and_resolves(self) -> None:
        page = MagicMock()
        drain = {"candidates": 2, "commits": 1, "iterations": 2, "dry_run": False}
        p_load, p_ctx, p_drain = _patches(page, drain)
        with (
            p_load,
            p_ctx,
            p_drain,
            patch.object(
                browser_apply_autofix,
                "_resolve_threads",
                return_value={"resolved": [1], "failed": []},
            ) as mock_resolve,
            patch.object(browser_apply_autofix, "_fetch_pr_head_sha", return_value="abc123") as mock_sha,
        ):
            result = apply_pr_suggestions_via_browser(7, "owner/repo", dry_run=False, resolve=True, comment_ids=[1])
        assert result["applied"] == 2
        assert result["commits"] == 1
        assert result["commit"] == "abc123"
        assert result["resolution"] == {"resolved": [1], "failed": []}
        mock_resolve.assert_called_once_with(7, "owner/repo", [1])
        mock_sha.assert_called_once_with(7, "owner/repo")

    def test_commit_sha_none_when_no_commits_made(self) -> None:
        page = MagicMock()
        drain = {"candidates": 0, "commits": 0, "iterations": 0, "dry_run": False}
        p_load, p_ctx, p_drain = _patches(page, drain)
        with (
            p_load,
            p_ctx,
            p_drain,
            patch.object(browser_apply_autofix, "_resolve_threads"),
            patch.object(browser_apply_autofix, "_fetch_pr_head_sha") as mock_sha,
        ):
            result = apply_pr_suggestions_via_browser(7, "owner/repo", dry_run=False, resolve=False)
        assert result["commit"] is None
        mock_sha.assert_not_called()

    def test_no_resolve_when_disabled(self) -> None:
        page = MagicMock()
        drain = {"candidates": 2, "commits": 1, "iterations": 2, "dry_run": False}
        p_load, p_ctx, p_drain = _patches(page, drain)
        with (
            p_load,
            p_ctx,
            p_drain,
            patch.object(browser_apply_autofix, "_resolve_threads") as mock_resolve,
            patch.object(browser_apply_autofix, "_fetch_pr_head_sha", return_value=None),
        ):
            result = apply_pr_suggestions_via_browser(7, "owner/repo", dry_run=False, resolve=False, comment_ids=[1])
        assert result["resolution"] is None
        mock_resolve.assert_not_called()

    def test_no_resolve_when_no_comment_ids(self) -> None:
        page = MagicMock()
        drain = {"candidates": 2, "commits": 1, "iterations": 2, "dry_run": False}
        p_load, p_ctx, p_drain = _patches(page, drain)
        with (
            p_load,
            p_ctx,
            p_drain,
            patch.object(browser_apply_autofix, "_resolve_threads") as mock_resolve,
            patch.object(browser_apply_autofix, "_fetch_pr_head_sha", return_value=None),
        ):
            result = apply_pr_suggestions_via_browser(7, "owner/repo", dry_run=False, resolve=True, comment_ids=None)
        assert result["resolution"] is None
        mock_resolve.assert_not_called()
