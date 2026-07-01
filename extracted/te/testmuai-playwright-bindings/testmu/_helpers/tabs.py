from __future__ import annotations

import logging
from typing import Optional

from testmu import _configure

_log = logging.getLogger("testmu")

__all__ = ["new_tab", "switch_tab", "close_tab", "ensure_active_page"]


async def new_tab(context, url: Optional[str] = None):
    """Open a new browser tab, navigate, and return the Page.

    Navigation target:
    - If *url* is provided: always navigate to that URL (any kane_version).
    - If *url* is None and kane_version=='v3': navigate to 'https://www.google.com'
      (V2-parity: V2 always lands on Google for blank new tabs).
    - If *url* is None and kane_version!='v3' (default 'v4'): do NOT navigate
      (preserves the legacy/inert behavior of the pre-V3 path).
    """
    page = await context.new_page()
    target = url
    if target is None and _configure.get("kane_version") == "v3":
        target = "https://www.google.com"
    if target is not None:
        await page.goto(target)
    await page.bring_to_front()
    _log.info("    [new_tab] opened tab (url=%s)", target or "<none>")
    return page


async def switch_tab(context, tab_index, *, title=None):
    """Switch to a browser tab by 0-based index, or by title.

    If *title* is given, switches to the first tab whose title matches (mirrors
    ``close_tab``'s title resolution) and ignores *tab_index* — V3 codegen emits
    both the positional index and ``title='...'``, with title taking precedence.
    Otherwise switches by 0-based *tab_index*, waiting for the CDP page-creation
    event if the tab isn't in the list yet (e.g. a click opened target="_blank").
    """
    if title is not None:
        for page in context.pages:
            if await page.title() == title:
                await page.bring_to_front()
                _log.info("    [switch_tab] switched to tab title=%r (url=%s)", title, page.url)
                return page
        raise ValueError(f"No tab with title {title!r}")
    pages = context.pages
    _log.info("    [switch_tab] target_index=%d current_tabs=%d", tab_index, len(pages))
    if tab_index >= len(pages):
        try:
            # Tab not in list yet — wait for CDP Target.targetCreated
            await context.wait_for_event("page", timeout=5000)
        except Exception:
            pass  # Playwright TimeoutError isn't Python's built-in TimeoutError
        pages = context.pages
    if tab_index >= len(pages):
        raise ValueError(f"Tab {tab_index} does not exist ({len(pages)} tabs open)")
    page = pages[tab_index]
    await page.bring_to_front()
    _log.info("    [switch_tab] switched to tab %d (url=%s)", tab_index, page.url)
    return page


async def close_tab(context, *, index: Optional[int] = None, title: Optional[str] = None) -> None:
    """Close a browser tab and activate the most-recent remaining tab.

    V3 gating: when kane_version=='v3', raises RuntimeError if only one tab is
    open (mirrors the selenium-python close_tab guard). When NOT v3 (default
    'v4'), the guard is skipped — legacy behavior allows closing the last tab.

    Resolution order:
    - *index*: close context.pages[index].
    - *title*: iterate pages, close the first whose title matches.
    - Neither: close context.pages[-1] (the most-recent / active page).

    After closing, brings context.pages[-1] to front (if any remain).
    """
    if _configure.get("kane_version") == "v3" and len(context.pages) <= 1:
        raise RuntimeError("Cannot close the only open tab")

    if index is not None:
        target = context.pages[index]
    elif title is not None:
        target = None
        for page in context.pages:
            if await page.title() == title:
                target = page
                break
        if target is None:
            raise ValueError(f"No tab with title {title!r}")
    else:
        target = context.pages[-1]

    _log.info("    [close_tab] closing tab (url=%s)", getattr(target, "url", "<unknown>"))
    await target.close()

    if context.pages:
        await context.pages[-1].bring_to_front()


async def ensure_active_page(page):
    """Return *page* if still open, else re-point to the last surviving tab.

    The Playwright analog of the selenium-python binding's per-action
    ``_heal_stale_window``.  Generated V3 code threads the active tab as a local
    ``page`` handle that is only rebound on explicit tab ops, so a tab closed as
    a side effect of an action (e.g. a click firing ``window.close()``) leaves
    that handle pointing at a dead page.  V3 export calls this before each op
    that follows a tab op, re-pointing to the surviving tab — mirroring the
    runtime's last-surviving-page rule and selenium's stale-window heal.

    - *page* still open: returned untouched — the common, no-tab-close path; no
      ``bring_to_front`` so focus is never stolen needlessly.
    - *page* closed: re-point to the last non-closed page in its context, bring
      it to front, and return it.
    - no surviving tab: raise ``RuntimeError`` (rather than an opaque IndexError).
    """
    if not page.is_closed():
        return page
    survivors = [p for p in page.context.pages if not p.is_closed()]
    if not survivors:
        raise RuntimeError(
            "ensure_active_page: the active tab was closed and no surviving tab "
            "remains in the browser context"
        )
    page = survivors[-1]
    await page.bring_to_front()
    _log.info(
        "    [ensure_active_page] active tab closed; re-pointed to surviving tab (url=%s)",
        getattr(page, "url", "<unknown>"),
    )
    return page
