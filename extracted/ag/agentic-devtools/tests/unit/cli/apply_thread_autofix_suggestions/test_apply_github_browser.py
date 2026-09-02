"""Tests for _apply_github_browser."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.apply_thread_autofix_suggestions import _apply_github_browser

_RESOLVE_REPO = "agentic_devtools.cli.github.repo_resolution.resolve_github_repo"
_APPLY_BROWSER = "agentic_devtools.cli.github.browser_apply_autofix.apply_pr_suggestions_via_browser"


class TestApplyGithubBrowser:
    """Tests for the browser-strategy dispatcher."""

    def test_success_dispatch(self) -> None:
        with (
            patch(_RESOLVE_REPO, return_value="owner/repo"),
            patch(
                _APPLY_BROWSER,
                return_value={"applied": 2, "strategy": "browser", "dry_run": False},
            ) as mock_apply,
        ):
            result = _apply_github_browser(7, "owner/repo", [1], "msg", True, False)

        assert result["applied"] == 2
        mock_apply.assert_called_once_with(
            pr_number=7,
            repo="owner/repo",
            comment_ids=[1],
            message="msg",
            resolve=True,
            dry_run=False,
        )

    def test_unavailable_returns_error_dict(self) -> None:
        from agentic_devtools.cli.github.browser_apply_autofix import BrowserAutofixUnavailable

        with (
            patch(_RESOLVE_REPO, return_value="owner/repo"),
            patch(_APPLY_BROWSER, side_effect=BrowserAutofixUnavailable("no playwright")),
        ):
            result = _apply_github_browser(7, "owner/repo", None, "msg", True, True)

        assert result["error"] == "no playwright"
        assert result["strategy"] == "browser"
        assert result["dry_run"] is True
        assert result["applied"] == 0

    def test_credential_error_returns_error_dict(self) -> None:
        from agentic_devtools.cli.github.browser_apply_autofix import BrowserCredentialError

        with (
            patch(_RESOLVE_REPO, return_value="owner/repo"),
            patch(_APPLY_BROWSER, side_effect=BrowserCredentialError("env unset")),
        ):
            result = _apply_github_browser(7, None, None, "msg", False, False)

        assert result["error"] == "env unset"
        assert result["dry_run"] is False
