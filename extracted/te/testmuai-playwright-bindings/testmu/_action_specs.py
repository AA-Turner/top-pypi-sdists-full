"""Per-verb behaviour specs for heal-driven action execution.

Each verb provides:
  - runner: async, locator-based action (the verb on a real Locator).
  - coord_runner: async, page-mouse/keyboard fallback when the COORDINATE
    heal tier returns pixels rather than a selector. Verbs that can't be
    performed by coords (e.g. scroll_into_view) leave it None and override
    tiers to skip COORDINATE.
  - tiers: optional override of the default cascade order.

Behavioural parity reference: the Selenium action-per-verb modules.
Each Selenium file is ~50 LoC; collapsed here since Playwright async is terser.

Public surface: _VERB_SPECS dict (verb_name → _VerbSpec). Consumed by the
Locator monkey-patch and VisionLocator.
"""
from __future__ import annotations

import asyncio
import logging

from testmu._action_engine import _VerbSpec

_log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

async def _hold_modifiers(page, modifiers):
    """Press modifier keys; returns a callable that releases them in reverse."""
    if not modifiers:
        async def _noop(): pass
        return _noop
    for m in modifiers:
        await page.keyboard.down(m)
    async def _release():
        for m in reversed(modifiers):
            await page.keyboard.up(m)
    return _release


# ---------------------------------------------------------------------------
# click / dblclick / hover — pure pointer verbs
# ---------------------------------------------------------------------------

async def _try_option_bridge(locator) -> bool:
    """Selenium-parity bridge: rewrite ``<option>.click()`` into
    ``<select>.select_option(label=...)`` on the ancestor.

    Native HTML ``<option>`` inside a closed ``<select>`` is not laid out
    as a clickable target in modern browsers. Selenium's WebDriver protocol
    special-cases option clicks (synthesises a select-by-option at the
    driver level); Playwright has no equivalent — ``option.click()`` times
    out, the verb sinks into the heal cascade, and coordinate/vision tiers
    can't see closed-dropdown text either. Bridge runs before the real
    click so the cascade is never triggered for this shape.

    Returns True when the bridge fired (caller skips ``locator.click``).
    Returns False on any failure or when the locator is not an OPTION —
    callers fall through to the original click, preserving non-bridge
    behaviour.
    """
    try:
        tag = await locator.evaluate("el => el && el.tagName")
    except Exception:
        return False
    if not isinstance(tag, str) or tag.upper() != "OPTION":
        return False
    parent = locator.locator("xpath=ancestor::select[1]")
    try:
        if await parent.count() == 0:
            return False
    except Exception:
        return False
    try:
        label = await locator.evaluate("el => el.textContent || ''")
    except Exception:
        return False
    label = (label or "").strip()
    if not label:
        return False
    await parent.select_option(label=label)
    return True


async def _click_runner(locator, **kw):
    if await _try_option_bridge(locator):
        return
    await locator.click(**kw)


async def _click_coord_runner(page, x, y, **kw):
    button = kw.get("button", "left")
    click_count = kw.get("click_count", 1)
    delay = kw.get("delay", 0)
    release = await _hold_modifiers(page, kw.get("modifiers"))
    try:
        await page.mouse.click(x, y, button=button, click_count=click_count, delay=delay)
    finally:
        await release()


CLICK_SPEC = _VerbSpec(runner=_click_runner, coord_runner=_click_coord_runner)


async def _dblclick_runner(locator, **kw):
    await locator.dblclick(**kw)


async def _dblclick_coord_runner(page, x, y, **kw):
    button = kw.get("button", "left")
    delay = kw.get("delay", 0)
    release = await _hold_modifiers(page, kw.get("modifiers"))
    try:
        await page.mouse.dblclick(x, y, button=button, delay=delay)
    finally:
        await release()


DBLCLICK_SPEC = _VerbSpec(runner=_dblclick_runner, coord_runner=_dblclick_coord_runner)


async def _hover_runner(locator, **kw):
    await locator.hover(**kw)


async def _hover_coord_runner(page, x, y, **kw):
    release = await _hold_modifiers(page, kw.get("modifiers"))
    try:
        await page.mouse.move(x, y)
    finally:
        await release()


HOVER_SPEC = _VerbSpec(runner=_hover_runner, coord_runner=_hover_coord_runner)


# ---------------------------------------------------------------------------
# long_press — press-and-hold gesture (V3 click_modifier)
# ---------------------------------------------------------------------------
#
# hover → mouse.down → hold (duration + 0.1s buffer) → mouse.up. The +0.1s
# buffer is applied here (post-validation) so a 30s hold reaches 30.1s real
# hold — mirrors V2 _do_long_press. Duration bounds are validated upstream
# (VisionLocator.long_press → validate_click_modifier) before dispatch.


async def _long_press_runner(locator, **kw):
    duration = float(kw.get("duration", 0.0) or 0.0)
    page = locator.page
    await locator.hover()
    await page.mouse.down()
    await asyncio.sleep(duration + 0.1)
    await page.mouse.up()


async def _long_press_coord_runner(page, x, y, **kw):
    duration = float(kw.get("duration", 0.0) or 0.0)
    await page.mouse.move(x, y)
    await page.mouse.down()
    await asyncio.sleep(duration + 0.1)
    await page.mouse.up()


LONG_PRESS_SPEC = _VerbSpec(runner=_long_press_runner, coord_runner=_long_press_coord_runner)


# ---------------------------------------------------------------------------
# multi_click — N discrete clicks on a SINGLE resolved target (V3 freq>2)
# ---------------------------------------------------------------------------
#
# The selectorless freq>2 path routes through _run_verb so the heal cascade
# resolves the target ONCE; the runner then clicks that one resolved Locator
# (or coordinate) N times — V2 _do_multi_click parity, instead of re-running the
# whole heal/vision cascade per click. freq==2 (native dblclick) and freq==1
# (plain click) are handled upstream in _helpers.gesture.multi_click and never
# reach this spec.


async def _multi_click_runner(locator, **kw):
    frequency = int(kw.get("frequency", 0))
    gap = float(kw.get("gap", 0.1))
    for i in range(frequency):
        await locator.click()
        if i < frequency - 1:
            await asyncio.sleep(gap)


async def _multi_click_coord_runner(page, x, y, **kw):
    frequency = int(kw.get("frequency", 0))
    gap = float(kw.get("gap", 0.1))
    for i in range(frequency):
        await page.mouse.click(x, y)
        if i < frequency - 1:
            await asyncio.sleep(gap)


MULTI_CLICK_SPEC = _VerbSpec(runner=_multi_click_runner, coord_runner=_multi_click_coord_runner)


# ---------------------------------------------------------------------------
# clear / fill / type / press — text-input verbs
# ---------------------------------------------------------------------------
#
# Coord runners click at the healed coordinate first to focus the field, then
# manipulate the keyboard. Mirrors Selenium _action_clear/_action_type
# 3-step ActionBuilder dance, adapted for Playwright's mouse + keyboard APIs.


def _coerce_text(value):
    """Coerce a scalar fill/type value to the ``str`` Playwright requires.

    Variables are type-preserving — ``testmu.var()`` returns the stored value
    untouched — so a number/bool produced by ``execute_js`` (or stored via
    ``set_var``) can reach a text-input verb as an ``int``/``float``/``bool``.
    Playwright's ``Locator.fill``/``type`` reject non-``str`` values ("expected
    string, got number"); Selenium's ``send_keys`` coerces via ``str()``
    internally, so this restores parity.

    Only scalars are coerced. ``dict``/``list`` (the separate
    API-variable-not-stringified case) are left untouched so they surface loudly
    as a clear Playwright error rather than silently filling a wrong
    ``"{'k': 'v'}"`` value. ``None`` is likewise left as-is (missing vars resolve
    to ``""`` upstream, so it is effectively unreachable here).
    """
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):  # bool is an int subclass → str(True) == "True"
        return str(value)
    return value


async def _clear_runner(locator, **kw):
    await locator.clear(**kw)


async def _clear_coord_runner(page, x, y, **kw):
    """Click + Ctrl+A + Delete. Mirrors Selenium _clear_coord_runner."""
    await page.mouse.click(x, y)
    await page.keyboard.press("Control+a")
    await page.keyboard.press("Delete")


CLEAR_SPEC = _VerbSpec(runner=_clear_runner, coord_runner=_clear_coord_runner)


async def _fill_runner(locator, value, **kw):
    await locator.fill(_coerce_text(value), **kw)


async def _fill_coord_runner(page, x, y, value, **kw):
    """Click + Ctrl+A + type. Mirrors Playwright fill semantics (replace existing)."""
    await page.mouse.click(x, y)
    await page.keyboard.press("Control+a")
    await page.keyboard.type(_coerce_text(value))


FILL_SPEC = _VerbSpec(runner=_fill_runner, coord_runner=_fill_coord_runner)


async def _type_runner(locator, text, **kw):
    await locator.type(_coerce_text(text), **kw)


async def _type_coord_runner(page, x, y, text, **kw):
    """Click + type (append). Playwright `type` appends without clearing,
    matching the Locator method's semantics."""
    delay = kw.get("delay", 0)
    await page.mouse.click(x, y)
    await page.keyboard.type(_coerce_text(text), delay=delay)


TYPE_SPEC = _VerbSpec(runner=_type_runner, coord_runner=_type_coord_runner)


async def _press_runner(locator, key, **kw):
    await locator.press(key, **kw)


async def _press_coord_runner(page, x, y, key, **kw):
    delay = kw.get("delay", 0)
    await page.mouse.click(x, y)
    await page.keyboard.press(key, delay=delay)


PRESS_SPEC = _VerbSpec(runner=_press_runner, coord_runner=_press_coord_runner)


# ---------------------------------------------------------------------------
# set_input_files — file upload
# ---------------------------------------------------------------------------
#
# Coord-runner mirrors Selenium's _set_input_files_coord_runner. Two stages:
#   1. Anchor on the healed pixel: elementFromPoint, then walk up ancestors AND
#      across OPEN shadow boundaries (shadowRoot / getRootNode().host).
#   2. Shadow-aware global fallback: elementFromPoint returns null for elements
#      outside the viewport and querySelector can't pierce shadow, so recurse the
#      light DOM + every open shadow root, collecting input[type=file], and pick
#      the nearest to the healed pixel. Kept identical to Selenium's resolver.

# Selectorless DOM-first resolver — V2 handle_upload parity. Before the heal
# cascade, a selectorless upload probes the DOM for the first <input type=file>
# (light + open shadow). File inputs are commonly display:none behind a styled
# trigger, so coordinate heal can't anchor on them; pure DOM find works because
# send_keys / set_input_files work on hidden inputs.
_FIND_FIRST_FILE_INPUT_JS = """() => {
    const found = [];
    const collect = (root) => {
        let direct = [];
        try { direct = root.querySelectorAll('input[type=file]'); } catch (e) {}
        for (const inp of direct) found.push(inp);
        let all = [];
        try { all = root.querySelectorAll('*'); } catch (e) {}
        for (const host of all) { if (host.shadowRoot) collect(host.shadowRoot); }
    };
    collect(document);
    return found.length ? found[0] : null;
}"""


async def _resolve_file_input_dom(page):
    """First <input type=file> via pure DOM (light + open shadow), no coordinate.

    Returns an ElementHandle or None; never raises — probe failure falls back to
    the heal cascade unchanged.
    """
    try:
        handle = await page.evaluate_handle(_FIND_FIRST_FILE_INPUT_JS)
        return handle.as_element()
    except Exception:  # noqa: BLE001 — probe is best-effort
        _log.info("    [upload] DOM file-input probe failed", exc_info=True)
        return None


_RESOLVE_FILE_INPUT_JS = """
([x, y]) => {
    const isFile = (n) => !!n && n.tagName === 'INPUT' && (n.type || '').toLowerCase() === 'file';

    let el = document.elementFromPoint(x, y);
    if (isFile(el)) return el;
    if (el && el.closest) {
        const lbl = el.closest('label');
        if (lbl && isFile(lbl.control)) return lbl.control;
    }
    let node = el;
    while (node) {
        if (isFile(node)) return node;
        if (node.shadowRoot) {
            const inner = node.shadowRoot.querySelector('input[type=file]');
            if (inner) return inner;
        }
        if (node.querySelector) {
            const inner = node.querySelector('input[type=file]');
            if (inner) return inner;
        }
        const root = node.getRootNode && node.getRootNode();
        node = node.parentElement || (root instanceof ShadowRoot ? root.host : null);
    }

    const found = [];
    const collect = (root) => {
        let direct = [];
        try { direct = root.querySelectorAll('input[type=file]'); } catch (e) {}
        for (const inp of direct) found.push(inp);
        let all = [];
        try { all = root.querySelectorAll('*'); } catch (e) {}
        for (const host of all) { if (host.shadowRoot) collect(host.shadowRoot); }
    };
    collect(document);
    if (found.length === 1) return found[0];
    if (found.length > 1) {
        let best = null, bestDist = Infinity;
        for (const inp of found) {
            const r = inp.getBoundingClientRect();
            const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
            const d = (cx - x) * (cx - x) + (cy - y) * (cy - y);
            if (d < bestDist) { bestDist = d; best = inp; }
        }
        return best;
    }
    return null;
}
"""


async def _set_input_files_runner(locator, files, **kw):
    await locator.set_input_files(files, **kw)


async def _set_input_files_coord_runner(page, x, y, files, **kw):
    """Resolve <input type=file> near the healed pixel and upload to it."""
    handle = await page.evaluate_handle(_RESOLVE_FILE_INPUT_JS, [x, y])
    element = handle.as_element()
    if element is None:
        raise RuntimeError(
            f"set_input_files: no <input type='file'> at/near healed coordinate ({x}, {y})"
        )
    await element.set_input_files(files)


SET_INPUT_FILES_SPEC = _VerbSpec(
    runner=_set_input_files_runner,
    coord_runner=_set_input_files_coord_runner,
    # DESKTOP_LOCATE is primary: file inputs often live in shadow roots or
    # off-viewport; the /v2/locate/desktop coordinate resolver delivers a pixel
    # the coord_runner bridges to the nearest <input type=file> regardless of
    # DOM depth or viewport position.  VISION_QUERY is retained as a selector
    # fallback: when DESKTOP_LOCATE misses, Playwright can re-run the verb with
    # the healed selector just as it does for other verbs — the "can't use"
    # concern was a mis-read of the runner/coord_runner dispatch logic.
    tiers=("DESKTOP_LOCATE", "VISION_QUERY"),
)


# ---------------------------------------------------------------------------
# scroll_into_view — DESKTOP_LOCATE_FULL_PAGE primary + VISION_QUERY fallback
# ---------------------------------------------------------------------------
#
# Tiers override = ('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY').
# DESKTOP_LOCATE_FULL_PAGE uses a full-page screenshot to locate below-fold
# targets and provides a coord_runner for fine-adjustment after scroll.
# VISION_QUERY is retained as a selector fallback.


async def _scroll_into_view_runner(locator, **kw):
    await locator.scroll_into_view_if_needed(**kw)


async def _scroll_coord_runner(page, x, y, **kw):
    """Coordinate fallback for DESKTOP_LOCATE_FULL_PAGE — spec §9.3.
    elementFromPoint(x,y)?.scrollIntoView({block:'center'}) — idempotent fine-adjustment."""
    await page.evaluate(
        "([x, y]) => { var el = document.elementFromPoint(x, y); if (el) { el.scrollIntoView({block: 'center'}); } }",
        [x, y]
    )


SCROLL_INTO_VIEW_SPEC = _VerbSpec(
    runner=_scroll_into_view_runner,
    coord_runner=_scroll_coord_runner,
    tiers=("DESKTOP_LOCATE_FULL_PAGE", "VISION_QUERY"),
)


# ---------------------------------------------------------------------------
# Verb registry
# ---------------------------------------------------------------------------

_VERB_SPECS: dict[str, _VerbSpec] = {
    "click": CLICK_SPEC,
    "dblclick": DBLCLICK_SPEC,
    "long_press": LONG_PRESS_SPEC,
    "multi_click": MULTI_CLICK_SPEC,
    "hover": HOVER_SPEC,
    "clear": CLEAR_SPEC,
    "fill": FILL_SPEC,
    "type": TYPE_SPEC,
    "press": PRESS_SPEC,
    "set_input_files": SET_INPUT_FILES_SPEC,
    "scroll_into_view_if_needed": SCROLL_INTO_VIEW_SPEC,
}


def get_verb_spec(verb_name: str) -> _VerbSpec | None:
    """Look up a verb spec by Playwright method name. Returns None for
    unknown verbs (caller treats as 'not auto-healable')."""
    return _VERB_SPECS.get(verb_name)


__all__ = [
    "CLICK_SPEC", "DBLCLICK_SPEC", "LONG_PRESS_SPEC", "MULTI_CLICK_SPEC", "HOVER_SPEC",
    "CLEAR_SPEC", "FILL_SPEC", "TYPE_SPEC", "PRESS_SPEC",
    "SET_INPUT_FILES_SPEC", "SCROLL_INTO_VIEW_SPEC",
    "_scroll_coord_runner", "_long_press_coord_runner",
    "_FIND_FIRST_FILE_INPUT_JS", "_resolve_file_input_dom",
    "_VERB_SPECS", "get_verb_spec",
]
