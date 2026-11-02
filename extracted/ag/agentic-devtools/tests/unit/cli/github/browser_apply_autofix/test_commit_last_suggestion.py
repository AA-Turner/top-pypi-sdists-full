"""Tests for _commit_last_suggestion."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.cli.github.browser_apply_autofix import (
    BUTTON_APPLY_SUGGESTION,
    _commit_last_suggestion,
)


def _make_page(message_box_count: int):
    page = MagicMock()
    commit_locator = MagicMock()
    apply_btn = MagicMock()
    message_box = MagicMock()
    message_box.count.return_value = message_box_count
    page.locator.return_value = commit_locator

    def get_by_role(role, name):
        if role == "textbox":
            return message_box
        return apply_btn

    page.get_by_role.side_effect = get_by_role
    return page, commit_locator, apply_btn, message_box


class TestCommitLastSuggestion:
    """Tests for _commit_last_suggestion."""

    def test_fills_message_when_box_present(self) -> None:
        page, commit_locator, apply_btn, message_box = _make_page(1)
        _commit_last_suggestion(page, "my message")
        commit_locator.last.click.assert_called_once_with()
        message_box.fill.assert_called_once_with("my message")
        apply_btn.click.assert_called_once_with()
        page.get_by_role.assert_any_call("button", name=BUTTON_APPLY_SUGGESTION)

    def test_skips_fill_when_box_absent(self) -> None:
        page, commit_locator, apply_btn, message_box = _make_page(0)
        _commit_last_suggestion(page, "my message")
        commit_locator.last.click.assert_called_once_with()
        message_box.fill.assert_not_called()
        apply_btn.click.assert_called_once_with()
