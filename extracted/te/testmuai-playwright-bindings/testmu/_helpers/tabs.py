from __future__ import annotations

import base64
import logging
import uuid
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from testmu import _configure

_log = logging.getLogger("testmu")

__all__ = ["new_tab", "switch_tab", "close_tab", "ensure_active_page"]

# V3 automind tab-heal endpoint (V2 kaneai_switch_tab_heal parity).
_TAB_HEAL_PATH = "/v1/heal/switch-tab"


# ---------------------------------------------------------------------------
# V3 tolerant tab-identifier resolution (parity with selenium-python tabs.py)
# ---------------------------------------------------------------------------

def _strip_www(host: str) -> str:
    return host[4:] if host.startswith("www.") else host


def _url_matches(identifier: str, url) -> bool:
    """Host/prefix-aware match of a tab ``identifier`` against a live ``url``.

    The identifier may be a bare domain (``github.com``) or a full URL
    (``https://example.com/checkout``). Matching is by URL host, so
    ``github.com`` matches host ``github.com`` but NOT ``gist.github.com`` or
    ``github.com.evil.com``. If the identifier carries a path, the URL path must
    also start with it. ``www.`` is ignored on both sides.
    """
    if not isinstance(url, str) or not url:
        return False
    parsed_id = urlparse(identifier if "://" in identifier else "//" + identifier)
    id_host = _strip_www(parsed_id.netloc.lower())
    if not id_host:
        return False
    parsed_url = urlparse(url)
    if _strip_www(parsed_url.netloc.lower()) != id_host:
        return False
    id_path = parsed_id.path.rstrip("/")
    if id_path:
        return parsed_url.path.startswith(id_path)
    return True


async def _seen_pages(context) -> List[Tuple[object, str, str]]:
    """Snapshot ``(page, title, url)`` for every open tab.

    A tab that errors while being read (e.g. closed mid-iteration) contributes
    empty title/url so it simply fails to match, rather than aborting resolution.
    """
    seen: List[Tuple[object, str, str]] = []
    for page in context.pages:
        try:
            title = await page.title()
            url = page.url
        except Exception:
            title, url = "", ""
        seen.append((page, title or "", url or ""))
    return seen


def _match_tab_tiers(seen: List[Tuple[object, str, str]], identifier: str) -> list:
    """Match ``identifier`` against ``seen`` in tolerant priority order.

    Tiers (first non-empty wins): exact title/URL, case-insensitive exact title,
    host/prefix-aware URL, case-insensitive title CONTAINS. Authors type title
    fragments and V2 never title-matched at all, so exact-only is stricter than
    any authored expectation.
    """
    ident_lower = identifier.lower()
    return (
        [p for p, t, u in seen if t == identifier or u == identifier]
        or [p for p, t, _ in seen if t.lower() == ident_lower]
        or [p for p, _, u in seen if _url_matches(identifier, u)]
        or [p for p, t, _ in seen if ident_lower and ident_lower in t.lower()]
    )


async def _resolve_tab_page(context, identifier: str):
    """Return the Page matching ``identifier`` via the tolerant tiers, or None.

    On multiple matches in the winning tier the first (in page order) is used and
    a warning is logged — the intended tab is not recoverable from the recording.
    """
    seen = await _seen_pages(context)
    matches = _match_tab_tiers(seen, identifier)
    if not matches:
        return None
    if len(matches) > 1:
        _log.warning(
            "    [tabs] %d open tabs matched identifier %r; using the first. "
            "The intended tab is not recoverable from the recording.",
            len(matches), identifier,
        )
    return matches[0]


def _org_id_int(raw) -> int:
    try:
        return int(raw)
    except (TypeError, ValueError):
        return 0


async def _post_tab_heal(url: str, payload: dict, headers: dict) -> Optional[dict]:
    """POST to the automind tab-heal endpoint. Separated for testability.

    Returns the parsed JSON body, or None on a non-200 response.
    """
    import httpx as _httpx

    async with _httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            _log.warning("    [tabs] automind %s status=%d", _TAB_HEAL_PATH, resp.status_code)
            return None
        return resp.json()


async def _automind_resolve_tab(context, intent: str, operation_type: str):
    """Resolve the target tab via automind ``/v1/heal/switch-tab`` (V2
    ``kaneai_switch_tab_heal`` parity): the op intent + live tab titles resolve to
    a tab index.

    Returns the resolved Page, or None on ANY failure (missing creds/URL, HTTP
    error, out-of-range index) so callers fall back to their static behavior.
    """
    try:
        base_url = _configure.get("automind_url", "")
        username = _configure.get("username", "")
        accesskey = _configure.get("accesskey", "")
        if not (username and accesskey and base_url):
            _log.warning("    [tabs] automind tab resolution unavailable (missing creds/URL)")
            return None

        seen = await _seen_pages(context)
        titles = [t for _, t, _ in seen]
        # Playwright has no definitive "current tab" from the context alone; use
        # the last page as a best-effort front-most hint.
        current_tab = titles[-1] if titles else ""
        payload = {
            "code_request_id": uuid.uuid4().hex[:16],
            "intent": intent,
            "open_tabs": titles,
            "current_tab": current_tab,
            "operation_type": operation_type,
            "test_id": _configure.get("test_id", ""),
            "billing_run_id": _configure.billing_run_id(),
            "session_id": _configure.get("session_id", ""),
            "commit_id": _configure.get("commit_id", ""),
            "org_id": _org_id_int(_configure.get("org_id", 0)),
            "current_action": {"operation_type": operation_type, "operation_intent": intent},
            # Playwright binding drives desktop web only; sel derives these from
            # driver capabilities. Static values match vision.py's automind calls.
            "is_mobile": False,
            "device_os": "",
        }
        auth = base64.b64encode(f"{username}:{accesskey}".encode()).decode()
        headers = {"Content-Type": "application/json", "Authorization": f"Basic {auth}"}

        result = await _post_tab_heal(f"{base_url}{_TAB_HEAL_PATH}", payload, headers)
        if not result:
            return None
        idx = result.get("tab_index")
        if idx is None or not (0 <= int(idx) < len(seen)):
            _log.warning("    [tabs] automind tab resolution unusable: %s", result)
            return None
        _log.info(
            "    [tabs] automind resolved intent %r -> tab %d (%r)",
            intent, int(idx), titles[int(idx)],
        )
        return seen[int(idx)][0]
    except Exception as exc:
        _log.warning("    [tabs] automind tab resolution failed: %s", exc)
        return None


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
    from testmu._session import _apply_page_timeouts
    _apply_page_timeouts(page)
    target = url
    if target is None and _configure.get("kane_version") == "v3":
        target = "https://www.google.com"
    if target is not None:
        await page.goto(target)
    await page.bring_to_front()
    _log.info("    [new_tab] opened tab (url=%s)", target or "<none>")
    return page


async def switch_tab(context, tab_index, *, title=None, description=None):
    """Switch to a browser tab by 0-based index, or by title.

    If *title* is given, switches to the tab matching that identifier and ignores
    *tab_index* — V3 codegen emits both the positional index and ``title='...'``,
    with title taking precedence. Under kane_version=='v3' the identifier is
    resolved with the tolerant tiers (exact -> ci-exact title -> host/prefix URL
    -> ci-contains) and, on a miss, an automind rescue (V2 kaneai_switch_tab_heal
    parity) before raising. Under v4 the prior exact-title behavior is kept.
    Otherwise switches by 0-based *tab_index*, waiting for the CDP page-creation
    event if the tab isn't in the list yet (e.g. a click opened target="_blank").

    *description* is the authored tab intent. It is emitted only by the kane_v3
    codegen strategy: under v3, with no *title*, it resolves the tab via automind.
    Under v4 it is accepted and ignored, so the v4 path stays unchanged.
    """
    if title is None and description is not None and _configure.get("kane_version", "v4") == "v3":
        page = await _automind_resolve_tab(context, description, "SWITCH_TAB")
        if page is None:
            raise ValueError(f"No tab matching description {description!r}")
        await page.bring_to_front()
        _log.info("    [switch_tab] switched via automind description=%r", description)
        return page

    if title is not None:
        if _configure.get("kane_version", "v4") == "v3":
            page = await _resolve_tab_page(context, title)
            if page is None:
                page = await _automind_resolve_tab(context, title, "SWITCH_TAB")
            if page is None:
                raise ValueError(f"No tab with title {title!r}")
            await page.bring_to_front()
            _log.info("    [switch_tab] switched to tab identifier=%r (url=%s)", title, page.url)
            return page
        # V4: exact-title match only.
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


async def close_tab(
    context,
    *,
    index: Optional[int] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> None:
    """Close a browser tab and activate the most-recent remaining tab.

    V3 gating: when kane_version=='v3', raises RuntimeError if only one tab is
    open (mirrors the selenium-python close_tab guard). When NOT v3 (default
    'v4'), the guard is skipped — legacy behavior allows closing the last tab.

    Resolution order differs by kane_version, and V4's order is unchanged:
    - v3: *title* first (V3 codegen emits both, with index defaulting to 0 as a
      meaningless placeholder, so closing by index kills the WRONG tab), resolved
      via the tolerant tiers then an automind rescue (V2 kaneai_switch_tab_heal
      parity); then *index*; then the most-recent tab.
    - v4 (default): *index* first, then exact-title match, then the most-recent
      tab — byte-for-byte the legacy behavior.

    *description* is the authored tab intent, emitted only by the kane_v3 codegen
    strategy. Under v3, when a *title* is present it is the tolerant title match's
    automind rescue query; when no *title* is present it resolves via automind
    BEFORE any static index — V2's tab_index=0 default otherwise closes the WRONG
    tab. Under v4 it is accepted and ignored.

    After closing, brings context.pages[-1] to front (if any remain).
    """
    is_v3 = _configure.get("kane_version", "v4") == "v3"

    if is_v3 and len(context.pages) <= 1:
        raise RuntimeError("Cannot close the only open tab")

    async def _exact_title_match():
        for page in context.pages:
            if await page.title() == title:
                return page
        raise ValueError(f"No tab with title {title!r}")

    if is_v3 and title is not None:
        # v3 title-first: tolerant tiers, then an automind rescue on a miss (using
        # the authored description when present, else the title). Mirrors switch_tab
        # and the selenium/java/csharp close_tab siblings — resolving the static
        # title identifier BEFORE automind so all four bindings pick the same tab.
        target = await _resolve_tab_page(context, title)
        if target is None:
            target = await _automind_resolve_tab(context, description or title, "CLOSE_TAB")
        if target is None:
            raise ValueError(f"No tab with title {title!r}")
    elif is_v3 and description is not None:
        # No title identifier: resolve the authored intent via automind before any
        # static index (V2's tab_index=0 default otherwise closes the WRONG tab).
        target = await _automind_resolve_tab(context, description, "CLOSE_TAB")
        if target is None and index is not None:
            target = context.pages[index]
        if target is None:
            target = context.pages[-1]
    elif index is not None:
        target = context.pages[index]
    elif title is not None:
        target = await _exact_title_match()
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
