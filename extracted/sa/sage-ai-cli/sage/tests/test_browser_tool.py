"""Tests for the browser-tool abstraction (D11).

Sage can't verify frontend changes without a browser. This module
exposes a thin Playwright wrapper that the engine can call. When
Playwright isn't installed (most users won't have it on a fresh
install), the tool reports itself unavailable and methods raise
`BrowserUnavailable` — engine degrades to "use the test runner only"
instead of crashing.
"""

from __future__ import annotations

import pytest


class TestBrowserToolAvailability:

    def test_is_available_returns_bool(self):
        from sage.core.browser import BrowserTool
        result = BrowserTool.is_available()
        assert isinstance(result, bool)

    def test_unavailable_methods_raise(self):
        """When Playwright isn't installed, methods must raise
        BrowserUnavailable with an actionable message."""
        from sage.core.browser import BrowserTool, BrowserUnavailable

        # Force unavailable state for the test
        tool = BrowserTool(force_unavailable=True)
        with pytest.raises(BrowserUnavailable) as exc_info:
            tool.navigate("https://example.com")
        # Error message should tell the user how to enable
        msg = str(exc_info.value).lower()
        assert "playwright" in msg
        assert "pip install" in msg or "install" in msg


class TestBrowserToolInterface:
    """Tests the shape of the API without requiring Playwright actually
    installed. We use the `force_unavailable=True` path to verify the
    interface; integration with a real browser would be a separate suite."""

    def test_has_navigate_method(self):
        from sage.core.browser import BrowserTool
        assert hasattr(BrowserTool, "navigate")

    def test_has_screenshot_method(self):
        from sage.core.browser import BrowserTool
        assert hasattr(BrowserTool, "screenshot")

    def test_has_evaluate_method(self):
        from sage.core.browser import BrowserTool
        assert hasattr(BrowserTool, "evaluate")

    def test_has_click_method(self):
        from sage.core.browser import BrowserTool
        assert hasattr(BrowserTool, "click")

    def test_has_fill_method(self):
        from sage.core.browser import BrowserTool
        assert hasattr(BrowserTool, "fill")

    def test_close_is_idempotent(self):
        from sage.core.browser import BrowserTool
        tool = BrowserTool(force_unavailable=True)
        tool.close()  # no-op when never opened
        tool.close()  # second call must not raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
