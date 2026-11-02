"""Tests for _click_if_present."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.cli.github.browser_apply_autofix import BUTTON_NEXT, _click_if_present


class TestClickIfPresent:
    """Tests for _click_if_present."""

    def test_clicks_when_present(self) -> None:
        page = MagicMock()
        locator = page.get_by_role.return_value
        locator.count.return_value = 1
        assert _click_if_present(page, BUTTON_NEXT) is True
        page.get_by_role.assert_called_once_with("button", name=BUTTON_NEXT)
        locator.first.click.assert_called_once_with()

    def test_returns_false_when_absent(self) -> None:
        page = MagicMock()
        page.get_by_role.return_value.count.return_value = 0
        assert _click_if_present(page, BUTTON_NEXT) is False
        page.get_by_role.return_value.first.click.assert_not_called()
