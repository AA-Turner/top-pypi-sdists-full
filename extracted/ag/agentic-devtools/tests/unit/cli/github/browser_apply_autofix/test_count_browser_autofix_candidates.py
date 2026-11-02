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
        captured_kwargs: dict = {}

        @contextlib.contextmanager
        def fake_ctx(credentials=None, **kwargs):
            captured_kwargs.update(kwargs)
            yield page

        with (
            patch.object(browser_apply_autofix, "load_credentials", return_value=MagicMock()) as mock_load,
            patch.object(browser_apply_autofix, "_authenticated_page", fake_ctx),
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons", return_value=5),
        ):
            result = count_browser_autofix_candidates("owner/repo", 7, credentials_path="x")

        assert result == 5
        mock_load.assert_not_called()
        # Authentication (and any lazy login) is checked against the target PR
        # URL rather than the GitHub home page — see _authenticated_page.
        assert captured_kwargs["target_url"] == "https://github.com/owner/repo/pull/7"
        assert captured_kwargs["credentials_path"] == "x"
