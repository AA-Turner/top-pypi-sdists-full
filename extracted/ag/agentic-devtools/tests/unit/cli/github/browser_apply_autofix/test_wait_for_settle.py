"""Tests for _wait_for_settle."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.cli.github.browser_apply_autofix import _wait_for_settle


class TestWaitForSettle:
    """Tests for _wait_for_settle."""

    def test_waits_for_networkidle(self) -> None:
        page = MagicMock()
        _wait_for_settle(page)
        page.wait_for_load_state.assert_called_once_with("networkidle")
