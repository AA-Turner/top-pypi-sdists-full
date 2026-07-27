"""Browser/Playwright tool abstraction (D11).

A thin wrapper around Playwright so the engine can verify frontend
changes (render a page, screenshot it, click a button, read DOM). The
abstraction degrades gracefully when Playwright isn't installed — most
sage users won't have it on a fresh install, and we don't want missing
deps to crash the engine.

Usage from engine:
    tool = BrowserTool()
    if not tool.is_available():
        # Skip browser-verification step
        return
    tool.navigate("http://localhost:5173")
    text = tool.evaluate("document.title")
    tool.screenshot("/tmp/dashboard.png")
    tool.close()

Install requirement (only when user opts in):
    pip install playwright
    playwright install chromium
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = ["BrowserTool", "BrowserUnavailable"]


class BrowserUnavailable(RuntimeError):
    """Raised when a BrowserTool method is called without Playwright installed."""


def _playwright_installed() -> bool:
    try:
        import playwright  # type: ignore  # noqa: F401
        return True
    except ImportError:
        return False


class BrowserTool:
    """Lazy-loaded Playwright wrapper.

    The browser process is spawned only on first call to `navigate()`
    or another method that needs it — constructing the tool is cheap
    and safe even when Playwright isn't installed.

    Pass `force_unavailable=True` in tests to exercise the degraded path
    without uninstalling Playwright.
    """

    @classmethod
    def is_available(cls) -> bool:
        return _playwright_installed()

    def __init__(self, *, force_unavailable: bool = False) -> None:
        self._force_unavailable = force_unavailable
        self._playwright: Any = None  # opaque Playwright handle
        self._browser: Any = None
        self._page: Any = None

    def _available(self) -> bool:
        return not self._force_unavailable and _playwright_installed()

    def _require(self) -> None:
        if not self._available():
            raise BrowserUnavailable(
                "Browser tool requires Playwright. Install with: "
                "`pip install playwright && playwright install chromium`. "
                "Then re-run sage."
            )

    def _ensure_page(self):
        self._require()
        if self._page is not None:
            return self._page
        # Lazy import only when we actually need to spawn a browser.
        from playwright.sync_api import sync_playwright  # type: ignore
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=True)
        self._page = self._browser.new_page()
        return self._page

    def navigate(self, url: str) -> None:
        page = self._ensure_page()
        page.goto(url)

    def screenshot(self, path: str | Path) -> str:
        page = self._ensure_page()
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(out))
        return str(out)

    def evaluate(self, expression: str) -> Any:
        page = self._ensure_page()
        return page.evaluate(expression)

    def click(self, selector: str) -> None:
        page = self._ensure_page()
        page.click(selector)

    def fill(self, selector: str, text: str) -> None:
        page = self._ensure_page()
        page.fill(selector, text)

    def text_content(self, selector: str) -> str | None:
        page = self._ensure_page()
        return page.text_content(selector)

    def wait_for_selector(self, selector: str, timeout_ms: int = 5000) -> None:
        page = self._ensure_page()
        page.wait_for_selector(selector, timeout=timeout_ms)

    def close(self) -> None:
        """Tear down the browser. Safe to call multiple times."""
        if self._page is not None:
            try:
                self._page.close()
            except Exception:
                pass
            self._page = None
        if self._browser is not None:
            try:
                self._browser.close()
            except Exception:
                pass
            self._browser = None
        if self._playwright is not None:
            try:
                self._playwright.stop()
            except Exception:
                pass
            self._playwright = None
