"""Tests for count_browser_autofix_candidates."""

from __future__ import annotations

import contextlib
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.github import browser_apply_autofix
from agentic_devtools.cli.github.browser_apply_autofix import count_browser_autofix_candidates


class TestCountBrowserAutofixCandidates:
    """Tests for count_browser_autofix_candidates."""

    def test_counts_candidates(self) -> None:
        page = MagicMock()

        @contextlib.contextmanager
        def fake_ctx(credentials, **kwargs):
            yield page

        with (
            patch.object(browser_apply_autofix, "load_credentials", return_value=MagicMock()) as mock_load,
            patch.object(browser_apply_autofix, "_authenticated_page", fake_ctx),
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons", return_value=5),
        ):
            result = count_browser_autofix_candidates("owner/repo", 7, credentials_path="x")

        assert result == 5
        mock_load.assert_called_once_with("x")
        page.goto.assert_called_once_with("https://github.com/owner/repo/pull/7")
