"""Tests for count_commit_suggestion_buttons."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.cli.github.browser_apply_autofix import (
    SELECTOR_COMMIT_SUGGESTION_BUTTON,
    count_commit_suggestion_buttons,
)


class TestCountCommitSuggestionButtons:
    """Tests for count_commit_suggestion_buttons."""

    def test_returns_count(self) -> None:
        page = MagicMock()
        page.locator.return_value.count.return_value = 2
        assert count_commit_suggestion_buttons(page) == 2
        page.locator.assert_called_once_with(SELECTOR_COMMIT_SUGGESTION_BUTTON)
