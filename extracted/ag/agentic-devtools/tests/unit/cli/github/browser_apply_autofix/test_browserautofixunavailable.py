"""Tests for BrowserAutofixUnavailable."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.github.browser_apply_autofix import BrowserAutofixUnavailable


class TestBrowserAutofixUnavailable:
    """Tests for the BrowserAutofixUnavailable exception."""

    def test_is_runtime_error_subclass(self) -> None:
        assert issubclass(BrowserAutofixUnavailable, RuntimeError)

    def test_can_be_raised_with_message(self) -> None:
        with pytest.raises(BrowserAutofixUnavailable, match="missing deps"):
            raise BrowserAutofixUnavailable("missing deps")
