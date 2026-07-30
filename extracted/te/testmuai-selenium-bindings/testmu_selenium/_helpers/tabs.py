"""Driver-level tab management helpers.

Maps to V3 codegen handlers:
- new_tab handler — currently emits 2-3 LOC inline
- switch_tab handler — currently emits up to ~13 LOC for title-search
- close_tab handler — currently emits up to ~13 LOC

This module encapsulates that logic so the generated test.py becomes one-liners.
"""
from __future__ import annotations

import base64
import logging
import os
import uuid
from urllib.parse import urlparse

import httpx
from selenium.common.exceptions import NoSuchWindowException

_log = logging.getLogger(__name__)


def _automind_resolve_tab(driver, intent: str, operation_type: str):
    """V2-parity (``kaneai_switch_tab_heal`` FF): resolve the target tab via
    automind ``/v1/heal/switch-tab`` from the op intent + live tab titles.

    V2's static fallback (blind ``handles[tab_index]``, tab_index defaulting
    to 0) closes/switches the WRONG tab for intents like "close the current
    tab" — the FF-on automind tier is what makes those ops correct on V2, so
    it is the parity mechanism here too. Returns the resolved handle, or
    ``None`` on ANY failure (missing creds/URL, HTTP error, out-of-range
    index) — callers fall back to their static behavior.
    """
    try:
        handles = driver.window_handles
        current = driver.current_window_handle
        titles = []
        for h in handles:
            driver.switch_to.window(h)
            titles.append(driver.title)
        current_index = handles.index(current)
        driver.switch_to.window(current)

        from testmu_selenium import _config
        username = os.getenv("LT_USERNAME", "")
        accesskey = os.getenv("LT_ACCESS_KEY", "")
        automind_url = _config.get("automind_url")
        if not (username and accesskey and automind_url):
            _log.warning("    [tabs] automind tab resolution unavailable (missing creds/URL)")
            return None

        device_os = str((driver.capabilities or {}).get("platformName", "")).lower()
        payload = {
            "code_request_id": uuid.uuid4().hex[:16],
            "intent": intent,
            "open_tabs": titles,
            "current_tab": titles[current_index],
            "operation_type": operation_type,
            "test_id": os.getenv("TEST_ID", ""),
            "session_id": driver.session_id,
            "current_action": {"operation_type": operation_type, "operation_intent": intent},
            "commit_id": os.getenv("COMMIT_ID", ""),
            "org_id": int(os.getenv("ORG_ID", "0") or "0"),
            "is_mobile": device_os in ("android", "ios"),
            "device_os": device_os,
        }
        auth = base64.b64encode(f"{username}:{accesskey}".encode()).decode()
        resp = httpx.post(
            f"{automind_url}/v1/heal/switch-tab",
            json=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Basic {auth}"},
            timeout=30,
        )
        if resp.status_code != 200:
            _log.warning("    [tabs] automind /v1/heal/switch-tab status=%d", resp.status_code)
            return None
        result = resp.json()
        idx = result.get("tab_index")
        if idx is None or not (0 <= int(idx) < len(handles)):
            _log.warning("    [tabs] automind tab resolution unusable: %s", result)
            return None
        _log.info(
            "    [tabs] automind resolved intent %r -> tab %d (%r)",
            intent, int(idx), titles[int(idx)],
        )
        return handles[int(idx)]
    except Exception as exc:
        _log.warning("    [tabs] automind tab resolution failed: %s", exc)
        return None


def new_tab(driver, *, url: str | None = None) -> None:
    """Open a new tab, switch to it, and optionally navigate to ``url``.

    V3 emission reference: ``window.open()`` + ``switch_to.window(handles[-1])`` + optional ``driver.get(url)``.
    Note: unlike V3's no-url path, we do NOT navigate to google.com when url is None.
    """
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url if url is not None else "https://www.google.com")


def _strip_www(host: str) -> str:
    return host[4:] if host.startswith("www.") else host


def _url_matches(identifier: str, url) -> bool:
    """Host/prefix-aware match of a tab ``identifier`` against a live ``url``.

    The identifier may be a bare domain (``github.com``) or a full URL
    (``https://example.com/checkout``). Matching is by URL host, so
    ``github.com`` matches host ``github.com`` but NOT ``gist.github.com`` or
    ``github.com.evil.com``. If the identifier carries a path, the URL path
    must also start with it. ``www.`` is ignored on both sides.
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


def _resolve_tab_handle(driver, identifier: str):
    """Resolve the window handle for a tab ``identifier`` (title or URL).

    V2-authored blobs carry an opaque ``tab_identifier`` string (a title like
    ``Google`` or a URL like ``github.com``) with no structured match-type and
    no concrete index — the live tab was resolved by the authoring agent and
    never persisted. So resolve it at runtime against the open tabs.

    Visits each handle once (recording title + URL), then matches in priority
    order: exact title/URL, case-insensitive exact title, host/prefix-aware
    URL match, and finally case-insensitive title CONTAINS — authors type
    title fragments ("IP Data Intelligence" vs the real
    "IP Data Intelligence & API Provider | IPinfo"), and V2 never
    title-matched at all, so exact-only is stricter than any authored
    expectation. On multiple matches in the winning tier the first (in handle
    order) is used and a warning is logged — the intended tab is not
    recoverable from the blob. Raises :class:`NoSuchWindowException` when
    nothing matches.
    """
    seen = []  # list of (handle, title, current_url)
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        seen.append((handle, driver.title, driver.current_url))

    ident_lower = identifier.lower()
    matches = (
        [h for h, t, u in seen if t == identifier or u == identifier]
        or [h for h, t, _ in seen if t.lower() == ident_lower]
        or [h for h, _, u in seen if _url_matches(identifier, u)]
        or [h for h, t, _ in seen if ident_lower and ident_lower in t.lower()]
    )

    if not matches:
        # Name the candidates in the failure: dev-testing V2-authored sessions
        # showed bare "not found" is undiagnosable without knowing what the
        # open tabs actually were (authored fragment vs real <title> drift).
        candidates = "; ".join(f"title={t!r} url={u!r}" for _, t, u in seen)
        raise NoSuchWindowException(
            f"Tab identifier not found in the list of open tabs "
            f"(identifier={identifier!r}; open tabs: {candidates})"
        )
    if len(matches) > 1:
        _log.warning(
            "    [tabs] %d open tabs matched identifier %r; using the first. "
            "The intended tab is not recoverable from the recording.",
            len(matches), identifier,
        )
    return matches[0]


def switch_tab(driver, *, index: int | None = None, title: str | None = None,
               description: str | None = None) -> None:
    """Switch to a tab by ``index`` or by ``title`` (title-or-URL identifier).

    - ``title`` present: resolve the tab by identifier (exact title/URL, then
      host/prefix-aware URL, then title-contains) across all handles; on an
      identifier miss, fall back to automind intent resolution (V2
      ``kaneai_switch_tab_heal`` parity) before raising. Any ``index`` is
      ignored (it is only a placeholder default for identifier switches).
    - ``index`` only: switch directly by index.
    - Neither: raise ValueError.
    """
    if index is None and title is None:
        raise ValueError("switch_tab requires index or title")

    if title is not None:
        _log.info("    [switch_tab] identifier=%r current_tabs=%d", title, len(driver.window_handles))
        try:
            driver.switch_to.window(_resolve_tab_handle(driver, title))
        except NoSuchWindowException:
            handle = _automind_resolve_tab(driver, description or title, "SWITCH_TAB")
            if handle is None:
                raise
            driver.switch_to.window(handle)
    else:
        _log.info("    [switch_tab] index=%d current_tabs=%d", index, len(driver.window_handles))
        driver.switch_to.window(driver.window_handles[index])

    _log.info("    [switch_tab] switched (url=%s, title=%r)", driver.current_url, driver.title)


def close_tab(driver, *, index: int | None = None, title: str | None = None,
              description: str | None = None) -> None:
    """Close a tab by ``index`` or by ``title`` (title-or-URL identifier), then
    switch to the most recent remaining tab.

    With a ``description`` and no ``title``, the target is resolved via
    automind intent resolution FIRST (V2 ``kaneai_switch_tab_heal`` parity):
    V2-authored blobs carry tab_index=0 as an unmeaning default, so a blind
    ``handles[index]`` close kills the wrong tab for intents like "close the
    current tab" (grid-found: closed the ipinfo tab instead of the current
    one). Falls back to ``index`` / current tab when automind is unavailable.

    With neither argument: close the current tab.
    """
    if len(driver.window_handles) <= 1:
        raise RuntimeError("Cannot close the only open tab")

    if title is not None:
        try:
            driver.switch_to.window(_resolve_tab_handle(driver, title))
        except NoSuchWindowException:
            handle = _automind_resolve_tab(driver, description or title, "CLOSE_TAB")
            if handle is None:
                raise
            driver.switch_to.window(handle)
    elif description:
        handle = _automind_resolve_tab(driver, description, "CLOSE_TAB")
        if handle is not None:
            driver.switch_to.window(handle)
        elif index is not None:
            _log.warning(
                "    [close_tab] automind unavailable; falling back to "
                "authored tab_index=%d", index,
            )
            driver.switch_to.window(driver.window_handles[index])
        # else: close the current tab.
    elif index is not None:
        driver.switch_to.window(driver.window_handles[index])
    # else: close the current tab.

    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


__all__ = ["new_tab", "switch_tab", "close_tab"]
