"""The two page-reading primitives every browser surface shares.

* ``element_text`` — text AS IT APPEARS ON SCREEN (``innerText`` semantics).
  ``textContent`` is the wrong reader for an agent: it returns the source of
  inline ``<style>``/``<script>`` blocks and runs table cells together with no
  separator (a Wikipedia infobox came back as CSS followed by
  ``Founded2021HeadquartersSan Francisco``). ``get_text`` already used
  ``innerText``; ``get_element`` and ``query_selectors`` now share this helper
  so the three cannot disagree again.
* ``capture_png`` — a PNG of the page OR of one element. A selector that
  matches nothing raises ``SelectorNotFound`` naming the selector; it never
  falls back to a viewport shot (a picture of the wrong thing is a lie).
"""

from __future__ import annotations

from typing import Any


class SelectorNotFound(LookupError):
    """The selector handed to a capture matched no element."""

    def __init__(self, selector: str) -> None:
        self.selector = selector
        super().__init__(f"selector not found: {selector}")


async def element_text(element: Any) -> str:
    """Rendered text of an ElementHandle: no style/script source, cells and rows separated."""
    return (await element.inner_text()) or ""


async def capture_png(page: Any, *, selector: str | None = None, full_page: bool = False) -> bytes:
    """PNG of ``selector``'s first match, else the page (viewport or ``full_page``)."""
    if selector:
        element = await page.query_selector(selector)
        if element is None:
            raise SelectorNotFound(selector)
        return await element.screenshot(type="png")
    return await page.screenshot(type="png", full_page=full_page)
