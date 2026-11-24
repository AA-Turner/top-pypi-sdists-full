"""Press ONE button on an open page — in any frame — and report what the press did.

Used by ``PlaywrightBrowserPool.inspect_url(press=...)`` (``/browser-inspect`` url mode). The caller opened the page
as a person (their cookie); this finds the button by its visible label / accessible name across EVERY frame (an
embedded app renders in its own, often cross-origin, frame — Playwright's frame handles reach it where the main
frame's DOM cannot), clicks it, confirms a dialog if one appears, and records the calls the press made: every
non-GET response plus any response whose URL contains a caller ``watch`` substring, with status and a capped body
excerpt (for an NDJSON stream, its last telling event). Then it waits — until every ``until_text`` word shows, the
calls have answered, or ``wait_seconds`` runs out — and reads the page again.

Generic on purpose: nothing here knows any platform's paths; the caller names what to watch.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any

from matrx_scraper.utils.proxy import redact_url_secrets

logger = logging.getLogger(__name__)

PRESS_MAX_WAIT_SECONDS = 45.0
PRESS_DEFAULT_WAIT_SECONDS = 12.0
PRESS_BODY_EXCERPT_CHARS = 1_500
PRESS_MAX_CALLS = 20
PRESS_MAX_LABELS = 40
_CLICK_TIMEOUT_MS = 5_000
_ROLES = ("button", "link", "menuitem", "tab")
#: Words a dialog's primary (go-ahead) button carries; a dialog with none of these gets its last non-cancel button.
_PRIMARY_WORDS = ("confirm", "yes", "ok", "continue", "run", "save", "delete", "submit", "send", "proceed", "apply")
_CANCEL_WORDS = ("cancel", "close", "no", "back", "dismiss", "not now")
_SKIP_METHODS = {"GET", "HEAD", "OPTIONS"}

_VISIBLE_LABELS_JS = r"""(cap) => {
  const out = [];
  const seen = new Set();
  for (const el of document.querySelectorAll('button,[role=button],a[href],[role=menuitem],[role=tab],input[type=submit],input[type=button]')) {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const label = ((el.getAttribute('aria-label') || el.innerText || el.value || el.title || '') + '').trim().replace(/\s+/g, ' ');
    if (!label || label.length > 80 || seen.has(label)) continue;
    seen.add(label); out.push(label);
    if (out.length >= cap) break;
  }
  return out;
}"""


@dataclass
class PressSpec:
    button: str
    within: str | None = None
    until_text: list[str] = field(default_factory=list)
    wait_seconds: float = PRESS_DEFAULT_WAIT_SECONDS
    #: Label of a confirm dialog's button to press if a dialog appears; None = the dialog's primary button.
    confirm: str | None = None
    #: URL substrings whose responses are recorded even when they are GETs (a run-status poll).
    watch: list[str] = field(default_factory=list)


@dataclass
class PressCall:
    method: str
    url: str
    status: int
    body_excerpt: str = ""
    #: The response's Content-Range header: a data-API write answering "*/*" or ".../0" changed no row.
    content_range: str = ""
    #: The request's Content-Profile / Accept-Profile header: which schema a data-API function call named.
    profile: str = ""


@dataclass
class PressOutcome:
    found: bool
    pressed: bool = False
    pressed_label: str = ""
    frame_url: str = ""
    error: str | None = None
    visible_buttons: list[str] = field(default_factory=list)
    confirmed: str | None = None
    #: A confirm step appeared after the press and was not answered: its words (and its buttons).
    confirm_unanswered: str | None = None
    #: ``within`` was given and no visible element shows that text (a filter, a date, a hidden row).
    within_missing: bool = False
    calls: list[PressCall] = field(default_factory=list)
    text_before: str = ""
    text_after: str = ""
    console_errors_after: list[str] = field(default_factory=list)
    http_errors_after: list[str] = field(default_factory=list)
    #: Toast / alert / live-region text seen at any moment after the press (a toast can vanish before the re-read).
    notices: list[str] = field(default_factory=list)
    seconds: float = 0.0


def _is_error_event(event: Any) -> bool:
    """An NDJSON event that says the work failed: ``type`` / ``event`` error, a failed/error/refused ``status``, or a
    non-empty ``error`` field."""
    if not isinstance(event, dict):
        return False
    if str(event.get("type") or "").lower() == "error" or str(event.get("event") or "").lower() == "error":
        return True  # the platform stream's wire shape is {"event": "error", "data": {...}}
    if str(event.get("status") or "").lower() in ("error", "failed", "refused"):
        return True
    return bool(event.get("error"))


def _excerpt(body: str, content_type: str) -> str:
    """A capped excerpt. For an NDJSON stream: the FIRST error event when there is one (an earlier failure is never
    hidden behind a later "completed"), else the last event that names a result, else the last line."""
    body = body or ""
    if "ndjson" in content_type or ("\n{" in body and body.lstrip().startswith("{")):
        lines = [ln for ln in body.splitlines() if ln.strip()]
        events: list[tuple[str, Any]] = []
        for ln in lines:
            try:
                events.append((ln, json.loads(ln)))
            except ValueError:
                continue
        for ln, event in events:
            if _is_error_event(event):
                return ln[:PRESS_BODY_EXCERPT_CHARS]
        for ln, event in reversed(events):
            blob = json.dumps(event)[:4000].lower()
            if any(k in blob for k in ('"action_result"', '"completed"', '"done"', '"result"')):
                return ln[:PRESS_BODY_EXCERPT_CHARS]
        return (lines[-1] if lines else "")[:PRESS_BODY_EXCERPT_CHARS]
    return body[:PRESS_BODY_EXCERPT_CHARS]


#: Toasts, banners and live regions: what a page says about a press, often for only a second or two. A
#: MutationObserver installed in every frame before the click records each one the moment it appears, so a toast
#: gone before the final re-read is still seen.
_NOTICE_SELECTOR = "[role=status],[role=alert],[aria-live]:not([aria-live=off]),[data-sonner-toast],.toast"
_WATCH_NOTICES_JS = r"""(sel) => {
  const seen = (window.__matrxPressNotices = window.__matrxPressNotices || []);
  const grab = (root) => {
    const els = [];
    if (root.matches && root.matches(sel)) els.push(root);
    if (root.querySelectorAll) els.push(...root.querySelectorAll(sel));
    for (const el of els) {
      const t = ((el.innerText || el.textContent || '') + '').trim().replace(/\s+/g, ' ');
      if (t && t.length <= 300 && !seen.includes(t)) seen.push(t);
    }
  };
  if (!window.__matrxPressObserver) {
    window.__matrxPressObserver = new MutationObserver((muts) => {
      for (const m of muts) {
        if (m.type === 'characterData') { if (m.target.parentElement) grab(m.target.parentElement.closest(sel) || m.target.parentElement); continue; }
        for (const n of m.addedNodes) if (n.nodeType === 1) grab(n);
        if (m.target && m.target.nodeType === 1 && m.target.closest && m.target.closest(sel)) grab(m.target.closest(sel));
      }
    });
    window.__matrxPressObserver.observe(document.documentElement, {childList: true, subtree: true, characterData: true});
  }
  const now = [];
  for (const el of document.querySelectorAll(sel)) {
    const t = ((el.innerText || '') + '').trim().replace(/\s+/g, ' ');
    if (t && t.length <= 300) now.push(t);
  }
  return now;
}"""
_READ_NOTICES_JS = "() => (window.__matrxPressNotices || []).slice(0, 40)"


async def _watch_notices(page: Any) -> set[str]:
    """Install the notice observer in every frame; returns the notices already showing (never the press's)."""
    showing: set[str] = set()
    for frame in page.frames:
        try:
            showing.update(await frame.evaluate(_WATCH_NOTICES_JS, _NOTICE_SELECTOR) or [])
        except Exception:  # noqa: BLE001 — a detached frame has no notices; the others still count
            continue
    return showing


async def _notices(page: Any) -> list[str]:
    found: list[str] = []
    for frame in page.frames:
        try:
            got = await frame.evaluate(_READ_NOTICES_JS)
        except Exception:  # noqa: BLE001
            continue
        for text in got or []:
            if text not in found:
                found.append(text)
    return found


async def _visible_labels(page: Any) -> list[str]:
    labels: list[str] = []
    for frame in page.frames:
        try:
            got = await frame.evaluate(_VISIBLE_LABELS_JS, PRESS_MAX_LABELS)
        except Exception:  # noqa: BLE001 — a detached frame has no buttons; the others still count
            continue
        for label in got or []:
            if label not in labels:
                labels.append(label)
    return labels[:PRESS_MAX_LABELS]


async def _first_visible(locator: Any) -> Any | None:
    try:
        count = await locator.count()
    except Exception:  # noqa: BLE001
        return None
    for i in range(min(count, 10)):
        item = locator.nth(i)
        try:
            if await item.is_visible():
                return item
        except Exception:  # noqa: BLE001
            continue
    return None


_HOLDERS = "section,article,form,li,tr,[role=row],[role=group],[role=dialog],[role=listitem],div,span,td"


async def _within_visible(page: Any, within: str) -> bool:
    for frame in page.frames:
        if await _first_visible(frame.get_by_text(within, exact=False)) is not None:
            return True
    return False


async def _scoped(frame: Any, loc: Any, within: str) -> Any | None:
    """The first visible ``loc`` inside the SMALLEST visible element holding both ``within``'s text and that control.
    Holders come in document order, an ancestor before its descendants, so walking them from the end meets the
    innermost first."""
    holders = frame.locator(_HOLDERS).filter(has_text=within).filter(has=loc)
    try:
        count = await holders.count()
    except Exception:  # noqa: BLE001
        return None
    for i in range(count - 1, max(-1, count - 40), -1):
        holder = holders.nth(i)
        try:
            if not await holder.is_visible():
                continue
        except Exception:  # noqa: BLE001
            continue
        hit = await _first_visible(holder.locator(loc))
        if hit is not None:
            return hit
    return None


async def _find(page: Any, button: str, within: str | None) -> tuple[Any, Any] | None:
    """(frame, locator) of the first visible control named ``button`` — exact name first, then contains, then
    plain text — inside the smallest visible element that also shows ``within`` when given. Every frame."""
    for exact in (True, False):
        for frame in page.frames:
            for role in _ROLES:
                loc = frame.get_by_role(role, name=button, exact=exact)
                hit = await (_scoped(frame, loc, within) if within else _first_visible(loc))
                if hit is not None:
                    return frame, hit
    for frame in page.frames:
        loc = frame.get_by_text(button, exact=True)
        hit = await (_scoped(frame, loc, within) if within else _first_visible(loc))
        if hit is not None:
            return frame, hit
    return None


#: Marks every control that existed before the click, so a confirm step that appears after it is told apart.
_MARK_SEEN_JS = r"""() => { for (const b of document.querySelectorAll('button,[role=button],input[type=button],input[type=submit]')) b.setAttribute('data-matrx-press-seen', ''); return true; }"""
#: The controls that appeared after the click, with the text of the group that holds them.
_NEW_CONTROLS_JS = r"""() => {
  const out = [];
  const sel = 'button:not([data-matrx-press-seen]),[role=button]:not([data-matrx-press-seen]),input[type=button]:not([data-matrx-press-seen]),input[type=submit]:not([data-matrx-press-seen])';
  document.querySelectorAll(sel).forEach((el, i) => {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const label = ((el.getAttribute('aria-label') || el.innerText || el.value || '') + '').trim().replace(/\s+/g, ' ');
    const group = el.closest('[data-matrx-run-confirm],[role=alertdialog],[role=dialog],dialog,[role=group],form') || el.parentElement;
    const words = group ? ((group.innerText || '') + '').trim().replace(/\s+/g, ' ').slice(0, 300) : '';
    const go = el.hasAttribute('data-matrx-run-confirm-run');
    el.setAttribute('data-matrx-press-new', String(i));
    out.push({ i, label, words, go });
  });
  return out;
}"""


def _is_cancel(label: str) -> bool:
    low = label.lower().strip()
    return any(low == w or low.startswith(w + " ") for w in _CANCEL_WORDS)


async def _answer_confirm(page: Any, confirm: str | None) -> tuple[str | None, str | None]:
    """Answer the confirm step a press opened, in any frame: a dialog (``role=dialog`` / ``alertdialog``), the
    platform run button's inline question ("This runs an AI step." · go-ahead · Cancel), or any group of new
    controls holding a Cancel. Returns ``(pressed label, None)``, ``(None, the step's words)`` when one appeared and
    was not answered, or ``(None, None)`` when no confirm step appeared."""
    for frame in page.frames:
        try:
            new = await frame.evaluate(_NEW_CONTROLS_JS) or []
        except Exception:  # noqa: BLE001 — a detached frame shows no confirm step
            continue
        dialog = await _first_visible(frame.locator("[role=alertdialog],[role=dialog],dialog[open]"))
        if not new and dialog is None:
            continue
        is_step = dialog is not None or any(c.get("go") for c in new) or any(_is_cancel(c.get("label", "")) for c in new)
        if not is_step:
            continue
        words = next((c.get("words") for c in new if c.get("words")), "") or "a confirm step"
        pick = None
        if confirm:
            low = confirm.lower()
            pick = next((c for c in new if c.get("label", "").lower() == low), None) or next(
                (c for c in new if low in c.get("label", "").lower()), None)
        else:
            pick = next((c for c in new if c.get("go")), None) or next(
                (c for c in new if any(w in c.get("label", "").lower() for w in _PRIMARY_WORDS)
                 and not _is_cancel(c.get("label", ""))), None) or next(
                (c for c in new if c.get("label") and not _is_cancel(c.get("label", ""))), None)
        if pick is not None:
            await frame.locator(f'[data-matrx-press-new="{pick["i"]}"]').first.click(timeout=_CLICK_TIMEOUT_MS)
            return pick.get("label") or "the confirm button", None
        if dialog is not None and not new:
            legacy = await _confirm_dialog_legacy(dialog, confirm)
            if legacy:
                return legacy, None
            try:
                words = ((await dialog.inner_text()) or words).strip()[:300]
            except Exception:  # noqa: BLE001
                pass
        labels = [c.get("label") for c in new if c.get("label")]
        return None, f"{words}" + (f" (its buttons: {', '.join(repr(x) for x in labels)})" if labels else "")
    return None, None


async def _confirm_dialog_legacy(dialog: Any, confirm: str | None) -> str | None:
    """A dialog whose buttons existed before the click (a reused modal): its go-ahead by label or by word."""
    if confirm:
        hit = await _first_visible(dialog.get_by_role("button", name=confirm))
    else:
        hit = None
        buttons = dialog.get_by_role("button")
        names: list[tuple[Any, str]] = []
        for i in range(min(await buttons.count(), 12)):
            b = buttons.nth(i)
            try:
                if await b.is_visible():
                    names.append((b, ((await b.inner_text()) or (await b.get_attribute("aria-label")) or "").strip()))
            except Exception:  # noqa: BLE001
                continue
        hit = next((b for b, n in names if any(w in n.lower() for w in _PRIMARY_WORDS)), None)
        if hit is None:
            rest = [b for b, n in names if n and not _is_cancel(n)]
            hit = rest[-1] if rest else None
    if hit is None:
        return None
    label = ((await hit.inner_text()) or confirm or "").strip()
    await hit.click(timeout=_CLICK_TIMEOUT_MS)
    return label or "the dialog's button"


async def _all_text(page: Any) -> str:
    from matrx_scraper.browser_pool import _frames_visible_text

    return await _frames_visible_text(page)


async def press_on_page(
    page: Any, spec: PressSpec, *, console_errors: list[str], http_errors: list[str], text_before: str,
) -> PressOutcome:
    """Find, press, confirm, record, wait, re-read. Never raises for a page-level failure: it is reported."""
    started = time.monotonic()
    out = PressOutcome(found=False, text_before=text_before)
    wait_seconds = max(0.5, min(float(spec.wait_seconds), PRESS_MAX_WAIT_SECONDS))
    target = await _find(page, spec.button, spec.within)
    if target is None:
        out.visible_buttons = await _visible_labels(page)
        if spec.within and not await _within_visible(page, spec.within):
            out.within_missing = True
        out.seconds = time.monotonic() - started
        return out
    frame, hit = target
    out.found = True
    out.frame_url = redact_url_secrets(frame.url or "")
    try:
        out.pressed_label = ((await hit.inner_text()) or (await hit.get_attribute("aria-label")) or spec.button).strip()[:120]
    except Exception:  # noqa: BLE001
        out.pressed_label = spec.button

    console_mark, http_mark = len(console_errors), len(http_errors)
    pending: list[asyncio.Task[None]] = []
    watch = [w for w in spec.watch if w]
    #: Requests the page STARTED after the click: a response to anything sent earlier is never the press's.
    started_after_click: list[Any] = []
    clicked = False
    notices_before = await _watch_notices(page)
    for f in page.frames:
        try:
            await f.evaluate(_MARK_SEEN_JS)
        except Exception:  # noqa: BLE001 — a detached frame has nothing to confirm
            continue

    def _on_request(req: Any) -> None:
        if clicked:
            started_after_click.append(req)

    async def _collect_notices() -> None:
        for text in await _notices(page):
            if text not in notices_before and text not in out.notices and len(out.notices) < 20:
                out.notices.append(text)

    async def _record(resp: Any) -> None:
        if len(out.calls) >= PRESS_MAX_CALLS:
            return
        call = PressCall(method=resp.request.method, url=redact_url_secrets(resp.url), status=resp.status)
        out.calls.append(call)
        headers = resp.headers or {}
        call.content_range = str(headers.get("content-range", ""))[:80]
        try:
            sent = await resp.request.all_headers()
            call.profile = str(sent.get("content-profile") or sent.get("accept-profile") or "")[:63]
        except Exception:  # noqa: BLE001 — no profile read: the default schema is assumed, the call still counts
            call.profile = str((resp.request.headers or {}).get("content-profile") or "")[:63]
        try:
            ctype = headers.get("content-type", "")
            call.body_excerpt = _excerpt(await resp.text(), ctype)
        except Exception as exc:  # noqa: BLE001 — a body we could not read is named, not invented
            call.body_excerpt = f"(body not readable: {type(exc).__name__})"

    def _on_response(resp: Any) -> None:
        if not any(resp.request is r for r in started_after_click):
            return
        method = resp.request.method
        if method in _SKIP_METHODS and not any(w in resp.url for w in watch):
            return
        if resp.request.resource_type in ("image", "font", "stylesheet", "media"):
            return
        pending.append(asyncio.ensure_future(_record(resp)))

    async def _on_dialog(dialog: Any) -> None:
        # A native confirm()/alert(): pressing the button is the intent, so it is accepted (never on beforeunload).
        try:
            out.confirmed = dialog.message[:200] if dialog.type != "beforeunload" else out.confirmed
            await (dialog.accept() if dialog.type != "beforeunload" else dialog.dismiss())
        except Exception:  # noqa: BLE001
            pass

    page.on("request", _on_request)
    page.on("response", _on_response)
    page.on("dialog", _on_dialog)
    try:
        try:
            clicked = True
            await hit.click(timeout=_CLICK_TIMEOUT_MS)
            out.pressed = True
        except Exception as exc:  # noqa: BLE001 — disabled / covered / detached: say which
            out.error = f"the button is there but could not be pressed: {str(exc).splitlines()[0][:300]}"
            out.seconds = time.monotonic() - started
            return out
        await asyncio.sleep(0.8)
        try:
            label, unanswered = await _answer_confirm(page, spec.confirm)
            if label:
                out.confirmed = label
            elif unanswered:
                out.confirm_unanswered = unanswered
        except Exception as exc:  # noqa: BLE001 — the step is named, never silently skipped
            out.confirm_unanswered = f"a confirm step could not be pressed ({type(exc).__name__})"
        deadline = started + wait_seconds
        until = [t for t in spec.until_text if t]
        confirm_until = time.monotonic() + 6.0
        while time.monotonic() < deadline:
            await asyncio.sleep(0.5)
            await _collect_notices()
            if out.confirmed is None and time.monotonic() < confirm_until:
                # A confirm step can appear a moment after the click (it asks the server what the button costs).
                try:
                    label, unanswered = await _answer_confirm(page, spec.confirm)
                except Exception as exc:  # noqa: BLE001
                    label, unanswered = None, f"a confirm step could not be pressed ({type(exc).__name__})"
                if label:
                    out.confirmed, out.confirm_unanswered = label, None
                    continue
                if unanswered:
                    out.confirm_unanswered = unanswered
            if pending and not all(t.done() for t in pending):
                continue
            if until:
                text = await _all_text(page)
                if all(t in text for t in until):
                    break
            elif pending and time.monotonic() - started > 2.5:
                break
        await asyncio.sleep(0.5)
        if pending:
            await asyncio.wait(pending, timeout=2.0)
        await _collect_notices()
    finally:
        page.remove_listener("request", _on_request)
        page.remove_listener("response", _on_response)
        page.remove_listener("dialog", _on_dialog)
        for task in pending:
            if not task.done():
                task.cancel()
    out.text_after = await _all_text(page)
    out.console_errors_after = console_errors[console_mark:][:20]
    out.http_errors_after = http_errors[http_mark:][:20]
    out.seconds = time.monotonic() - started
    return out


__all__ = ["PRESS_DEFAULT_WAIT_SECONDS", "PRESS_MAX_WAIT_SECONDS", "PressCall", "PressOutcome", "PressSpec",
           "press_on_page"]
