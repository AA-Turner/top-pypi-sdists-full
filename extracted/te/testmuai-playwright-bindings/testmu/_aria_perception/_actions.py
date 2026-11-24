"""Portable per-element operations keyed by a portable handle.

Every CDP ``DOM.*`` / ``Runtime.callFunctionOn`` use on the Chrome path has
an equivalent here built on ``page.locator("aria-ref=<ref>")`` (which routes
into iframes by itself) and ``locator.evaluate``. Locator baking stays
Playwright's own per-frame ``resolveSelector`` (the private channel command
the Chrome path already uses); only the tagging step differs.

ground_ref, viewport_status, scroll_ref_into_view, clickability_facts,
enrich_point_locator and option_click_redirect are the runner-facing API.
"""
from __future__ import annotations

import contextlib
import json
import logging
import uuid
from typing import Any

from ._engine import page_engine
from ._refs import (
    anchor_locator,
    call_on_ref,
    frame_id_for_ref,
    handle_to_aria_ref,
    is_option_handle,
    option_parts,
    ref_locator,
)
from ._snapshot import PlaywrightInternalsError, internals_error

_log = logging.getLogger("testmu")

# Per-operation budget. A live element answers in milliseconds; a stale ref is
# caught up front by a count() (ValueError "node not found"), never waited out.
_TIMEOUT_MS = 1000

# Temporary marker the resolveSelector scan looks for; always removed afterwards.
_TAG_ATTR = "data-testmu-resolve"

# Delimiter Playwright uses to join cross-frame selector parts (frames.js,
# ``Frame.resolveSelector``).
_CROSS_FRAME_DELIM = " >> internal:control=enter-frame >> "

_INTERACTIVE_TAGS = ("a", "button", "input", "select", "textarea")

# Runs on the element (text nodes climb to their parent).
_SET_ATTR_FN = """function(arg) {
    var el = (this.nodeType === 3 ? this.parentElement : this);
    if (!el || el.nodeType !== 1) return false;
    el.setAttribute(arg[0], arg[1]);
    return true;
}"""

_UNTAG_JS = """(tag) => {
    const sel = '[data-testmu-resolve="' + tag + '"]';
    let el = document.querySelector(sel);
    if (!el) {
        for (const h of document.querySelectorAll('*')) {
            if (h.shadowRoot) {
                el = h.shadowRoot.querySelector(sel);
                if (el) break;
            }
        }
    }
    if (el) { el.removeAttribute('data-testmu-resolve'); return true; }
    return false;
}"""

_SCROLL_FN = """function(smooth) {
    var el = (this.nodeType === 3 ? this.parentElement : this);
    if (!el) return false;
    el.scrollIntoView({behavior: smooth ? 'smooth' : 'auto', block: 'center', inline: 'nearest'});
    return true;
}"""

# Role/name fallback when the caller has no parsed node for the handle.
_ROLE_NAME_FN = """function() {
    var el = (this.nodeType === 3 ? this.parentElement : this);
    if (!el) return {role: '', name: ''};
    var tag = (el.tagName || '').toLowerCase();
    var type = (el.getAttribute('type') || '').toLowerCase();
    var role = el.getAttribute('role') || '';
    if (!role) {
        var map = {a: el.hasAttribute('href') ? 'link' : 'generic', button: 'button', select: el.multiple ? 'listbox' : 'combobox',
                   textarea: 'textbox', img: 'image', h1: 'heading', h2: 'heading', h3: 'heading', h4: 'heading',
                   h5: 'heading', h6: 'heading', option: 'option', iframe: 'iframe', li: 'listitem', ul: 'list', ol: 'list'};
        if (tag === 'input') {
            role = {checkbox: 'checkbox', radio: 'radio', range: 'slider', number: 'spinbutton', search: 'searchbox',
                    button: 'button', submit: 'button', reset: 'button', image: 'button'}[type] || 'textbox';
        } else {
            role = map[tag] || 'generic';
        }
    }
    var name = el.getAttribute('aria-label') || '';
    if (!name && el.labels && el.labels.length) name = el.labels[0].textContent || '';
    if (!name) name = el.getAttribute('alt') || el.getAttribute('title') || el.getAttribute('placeholder') || '';
    if (!name && !/^(input|select|textarea)$/.test(tag)) name = (el.innerText || el.textContent || '');
    return {role: role, name: name.replace(/\\s+/g, ' ').trim().slice(0, 200)};
}"""

# Tag the element at a point, descending into open shadow roots and walking up
# to the nearest interactive ancestor (mirrors the runner's elementFromPoint
# tagger). Reports an <iframe> hit instead of tagging it so the caller can
# descend into that frame. mode "select": only a native <select> qualifies.
_TAG_AT_POINT_JS = """([x, y, tag, mode, iTags, iRoles]) => {
    const TAGS = new Set(iTags), ROLES = new Set(iRoles);
    let el = document.elementFromPoint(x, y);
    while (el && el.shadowRoot) {
        const inner = el.shadowRoot.elementFromPoint(x, y);
        if (!inner || inner === el) break;
        el = inner;
    }
    if (!el) return {ok: false};
    if (el.tagName === 'IFRAME' || el.tagName === 'FRAME') {
        const r = el.getBoundingClientRect();
        el.setAttribute('data-testmu-resolve-frame', tag);
        return {ok: false, frame: true,
                dx: r.left + el.clientLeft, dy: r.top + el.clientTop};
    }
    let target = null;
    if (mode === 'select') {
        target = el.closest('select');
        if (!target) return {ok: false};
    } else {
        let c = el;
        for (let i = 0; i < 10 && c && c !== document.documentElement; i++) {
            const t = c.tagName.toLowerCase();
            const role = (c.getAttribute('role') || '').toLowerCase();
            if (TAGS.has(t) || ROLES.has(role)) { target = c; break; }
            c = c.parentElement;
        }
        target = target || el;
    }
    target.setAttribute('data-testmu-resolve', tag);
    return {ok: true};
}"""

# Accessible name of a native <option> (aria-label, else its label).
_OPTION_NAME_JS = """el => (el.getAttribute('aria-label') || el.label || el.textContent || '')
    .replace(/\\s+/g, ' ').trim()"""

_OPTION_PROBE_JS = """el => {
    if (!el || el.tagName !== 'OPTION') return null;
    const sel = el.closest('select');
    if (!sel) return null;
    return {label: (el.label || el.textContent || '').trim()};
}"""


# ---------------------------------------------------------------------------
# resolveSelector helpers (copied from testmu/_helpers/_locator_enrichment.py)
# ---------------------------------------------------------------------------

def _frames_main_first(page) -> list[Any]:
    main = page.main_frame
    return [main] + [f for f in page.frames if f != main]


async def _resolve_selector_across_frames(page, selector: str) -> tuple[str | None, Any]:
    """Ask Playwright's per-frame ``resolveSelector`` for ``selector`` until a
    frame answers. Returns ``(resolved, frame)`` or ``(None, None)``. The
    answering frame builds the full cross-frame chain back to the root."""
    for frame in _frames_main_first(page):
        try:
            channel = frame._impl_obj._channel
            try:
                resolved = await channel.send("resolveSelector", None, {"selector": selector})
            except TypeError:
                resolved = await channel.send("resolveSelector", {"selector": selector})
        except Exception as e:
            err = internals_error("resolveSelector", e)
            if err is not None:
                raise err from e
            continue
        if isinstance(resolved, dict):
            resolved = resolved.get("resolvedSelector")
        if resolved:
            return str(resolved), frame
    return None, None


async def _remove_tag(page, tag: str, frame: Any = None) -> None:
    frames = [frame] if frame is not None else list(page.frames)
    for f in frames:
        try:
            removed = await f.evaluate(_UNTAG_JS, tag)
        except Exception:
            continue
        if removed and frame is None:
            return


def _split_cross_frame_chain(resolved: str) -> tuple[str, list[dict[str, Any]]]:
    """Split a cross-frame selector into (leaf, FrameInfo list outer->inner)."""
    parts = resolved.split(_CROSS_FRAME_DELIM)
    frame_info_list = [
        {
            "type": "iframe",
            "selectors": [{"selector": part, "score": 100, "isXPath": False}],
            "boundingBox": None,
        }
        for part in parts[:-1]
    ]
    return parts[-1], frame_info_list


async def _resolve_tagged(page, element: dict, tag: str) -> dict:
    """resolveSelector on ``[data-testmu-resolve=tag]`` -> split -> cleanup.
    Keeps the element's existing locator when nothing resolves."""
    frame = None
    try:
        resolved, frame = await _resolve_selector_across_frames(page, f"css=[{_TAG_ATTR}='{tag}']")
        if resolved:
            leaf, frame_info_list = _split_cross_frame_chain(resolved)
            element["locator"] = leaf
            element["locator_type"] = "playwright"
            if frame_info_list:
                element["frame_info"] = {"frameInfo": frame_info_list}
            else:
                element.pop("frame_info", None)
    except PlaywrightInternalsError:
        raise
    except Exception as e:  # noqa: BLE001
        _log.debug("aria_perception: resolveSelector failed: %s", e)
    finally:
        with contextlib.suppress(Exception):
            await _remove_tag(page, tag, frame)
    return element


def _new_tag() -> str:
    return "testmu-resolve-" + uuid.uuid4().hex[:12]


async def _tag_at_point(page, x: float, y: float, tag: str, mode: str, interactive_roles) -> bool:
    """Tag the element at viewport point (x, y), descending through iframes
    (up to 5 levels). True when an element was tagged."""
    frame = page.main_frame
    for _ in range(5):
        result = await frame.evaluate(
            _TAG_AT_POINT_JS,
            [x, y, tag, mode, list(_INTERACTIVE_TAGS), sorted(interactive_roles)],
        )
        result = result or {}
        if result.get("ok"):
            return True
        if not result.get("frame"):
            return False
        sel = f"[data-testmu-resolve-frame='{tag}']"
        handle = await frame.query_selector(sel)
        child = await handle.content_frame() if handle else None
        with contextlib.suppress(Exception):
            await frame.evaluate(
                "(s) => { const e = document.querySelector(s); if (e) e.removeAttribute('data-testmu-resolve-frame'); }",
                sel,
            )
        if child is None:
            return False
        x -= float(result.get("dx") or 0)
        y -= float(result.get("dy") or 0)
        frame = child
    return False


def _box_center(element: dict) -> tuple[float, float] | None:
    bb = element.get("bounding_box")
    if not bb:
        return None
    return (
        float(bb.get("x", 0)) + float(bb.get("width", 0)) / 2,
        float(bb.get("y", 0)) + float(bb.get("height", 0)) / 2,
    )


def _rect_in_viewport(rect: dict, vw: float, vh: float) -> bool:
    """Same containment rule as the runner's ``_rect_in_viewport``."""
    x, y, w, h = rect["x"], rect["y"], rect["width"], rect["height"]
    if x >= 0 and y >= 0 and (x + w) <= vw and (y + h) <= vh:
        return True
    if h > vh or w > vw:
        return 0 <= x < vw and 0 <= y < vh
    return False


async def _viewport_size(page) -> tuple[float, float]:
    try:
        vp = await page.evaluate("() => [window.innerWidth, window.innerHeight]")
        return float(vp[0]), float(vp[1])
    except Exception:  # noqa: BLE001
        size = page.viewport_size or {}
        return float(size.get("width") or 1280), float(size.get("height") or 800)


def _maybe_json(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return value
    return value


def _anchor_handle(handle: int) -> int:
    """The select's handle for a native-option handle (geometry, scrolling
    and clickability are the select's); any other handle as is."""
    return option_parts(handle)[0] if is_option_handle(handle) else handle


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def ground_ref(page, handle: int, *, scroll: bool = True, node: Any = None) -> dict:
    """Ground a portable handle to the runner's flat-DOM element dict.

    ``{'role','name','locator': "role=<role>[name='<name>']", 'locator_type':'role',
    'bounding_box':{x,y,width,height}, 'backend_dom_node_id': handle, 'frame_id': ...}``.
    role/name come from ``node`` (the handle's AxNode from the latest parse)
    when given, else from the element itself. A native-option handle grounds
    to ``role="option"`` with the live option's name and the select's box.
    ``ValueError("node not found")`` at once when the ref does not resolve,
    or when it has no box.
    """
    try:
        ref = handle_to_aria_ref(handle)
    except ValueError as e:
        raise ValueError("node not found") from e
    locator = ref_locator(page, handle)
    # Geometry comes from the select for a native option (no box of its own).
    anchor = anchor_locator(page, handle)
    try:
        if await locator.count() == 0:
            raise ValueError("node not found")
        if scroll:
            with contextlib.suppress(Exception):
                await anchor.scroll_into_view_if_needed(timeout=_TIMEOUT_MS)
        box = await anchor.bounding_box(timeout=_TIMEOUT_MS)
    except Exception as e:
        raise ValueError("node not found") from e
    if not box or box.get("width", 0) <= 0 and box.get("height", 0) <= 0:
        raise ValueError("node not found")

    if is_option_handle(handle):
        # The live option's own name, so a shifted option index shows up as
        # a name mismatch against the doc instead of acting on a neighbour.
        try:
            name = str(await locator.evaluate(_OPTION_NAME_JS, timeout=_TIMEOUT_MS) or "")
        except Exception as e:
            raise ValueError("node not found") from e
        role = "option"
    elif node is not None:
        role, name = (node.role or ""), (node.name or "")
    else:
        try:
            rn = await call_on_ref(page, handle, _ROLE_NAME_FN, timeout_ms=_TIMEOUT_MS) or {}
        except Exception:  # noqa: BLE001
            rn = {}
        role, name = rn.get("role", ""), rn.get("name", "")
    safe_name = name.replace("'", "\\'")
    return {
        "role": role,
        "name": name,
        "locator": f"role={role}[name='{safe_name}']",
        "locator_type": "role",
        "bounding_box": {
            "x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"],
        },
        "backend_dom_node_id": handle,
        "frame_id": frame_id_for_ref(ref),
    }


async def viewport_status(page, handle: int) -> dict:
    """``{"in_viewport": bool, "rect": dict|None}``; any failure ->
    ``{"in_viewport": True, "rect": None}`` (unknown geometry never
    manufactures a scroll)."""
    try:
        anchor = anchor_locator(page, handle)
        if await anchor.count() == 0:
            return {"in_viewport": True, "rect": None}
        box = await anchor.bounding_box(timeout=_TIMEOUT_MS)
    except Exception:  # noqa: BLE001
        return {"in_viewport": True, "rect": None}
    if not box:
        return {"in_viewport": True, "rect": None}
    rect = {"x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]}
    vw, vh = await _viewport_size(page)
    return {"in_viewport": _rect_in_viewport(rect, vw, vh), "rect": rect}


async def scroll_ref_into_view(page, handle: int, *, smooth: bool = True) -> bool:
    try:
        ok = await call_on_ref(page, _anchor_handle(handle), _SCROLL_FN, bool(smooth), timeout_ms=_TIMEOUT_MS)
    except Exception as e:  # noqa: BLE001
        _log.debug("aria_perception.scroll_ref_into_view failed: %s", e)
        return False
    if ok and smooth:
        with contextlib.suppress(Exception):
            await page.wait_for_timeout(300)
    return bool(ok)


async def scroll_offsets(page, handle: int, fn_decl: str) -> dict:
    """``{"window_y", "element_y"}`` from the caller's offsets function; never raises."""
    try:
        value = _maybe_json(await call_on_ref(page, _anchor_handle(handle), fn_decl, timeout_ms=_TIMEOUT_MS)) or {}
        return {
            "window_y": float(value.get("window_y", 0.0) or 0.0),
            "element_y": float(value.get("element_y", 0.0) or 0.0),
        }
    except Exception:  # noqa: BLE001
        return {"window_y": 0.0, "element_y": 0.0}


async def tag_ref(page, handle: int, attr: str, value: str) -> bool:
    try:
        return bool(await call_on_ref(page, handle, _SET_ATTR_FN, [attr, value], timeout_ms=_TIMEOUT_MS))
    except Exception as e:  # noqa: BLE001
        _log.debug("aria_perception.tag_ref failed: %s", e)
        return False


async def element_snapshot(page, handle: int, fn_decl: str) -> dict | None:
    """Run the caller's element-snapshot JS payload on the element."""
    try:
        value = _maybe_json(await call_on_ref(page, handle, fn_decl, timeout_ms=_TIMEOUT_MS))
    except Exception as e:  # noqa: BLE001
        _log.debug("aria_perception.element_snapshot failed: %s", e)
        return None
    return value if isinstance(value, dict) and value else None


async def clickability_facts(page, handle: int, facts_fn_decl: str) -> dict:
    """The caller's facts function result + ``click_listeners: None`` (event
    listeners are CDP-only; reported as unsupported, never as empty)."""
    try:
        facts = _maybe_json(await call_on_ref(page, _anchor_handle(handle), facts_fn_decl, timeout_ms=_TIMEOUT_MS))
    except Exception:  # noqa: BLE001
        return {"error": "unresolved"}
    if not isinstance(facts, dict):
        return {"error": "facts unavailable"}
    if "error" in facts:
        return facts
    facts["click_listeners"] = None
    facts["click_listeners_unsupported"] = page_engine(page)
    return facts


async def enrich_ref_locator(page, element: dict) -> dict:
    """Tag the handle's element -> cross-frame resolveSelector -> split frame
    chain -> cleanup. Sets ``locator`` / ``locator_type="playwright"`` and
    ``frame_info`` when iframe-resident; keeps the role locator on failure."""
    handle = element.get("backend_dom_node_id")
    tag = _new_tag()
    if is_option_handle(handle):
        return await _enrich_option_locator(page, element, handle, tag)
    if not await tag_ref(page, handle, _TAG_ATTR, tag):
        return element
    return await _resolve_tagged(page, element, tag)


async def _enrich_option_locator(page, element: dict, handle: int, tag: str) -> dict:
    """A native option has no locator of its own from resolveSelector (it
    yields the select's): bake the select's, then chain the option by its
    accessible name (by position when it has none). Playwright treats an
    option of a visible select as visible, so the chain resolves."""
    select_handle, index = option_parts(handle)
    if not await tag_ref(page, select_handle, _TAG_ATTR, tag):
        return element
    before = element.get("locator")
    element = await _resolve_tagged(page, element, tag)
    if element.get("locator") == before or element.get("locator_type") != "playwright":
        return element
    name = element.get("name") or ""
    option = (f"internal:role=option[name={json.dumps(name)}s]" if name
              else f"internal:role=option >> nth={index}")
    element["locator"] = f"{element['locator']} >> {option}"
    return element


async def enrich_point_locator(page, element: dict, types: "ModeTypes") -> dict:
    """``bounding_box`` centre -> elementFromPoint (+ iframe descent) -> tag ->
    same resolve/cleanup as ``enrich_ref_locator``."""
    center = _box_center(element)
    if center is None:
        return element
    tag = _new_tag()
    try:
        tagged = await _tag_at_point(page, center[0], center[1], tag, "interactive", types.interactive_roles)
    except Exception as e:  # noqa: BLE001
        _log.debug("aria_perception.enrich_point_locator: tagging failed: %s", e)
        return element
    if not tagged:
        return element
    return await _resolve_tagged(page, element, tag)


async def option_click_redirect(page, locator_str: str, frame_info=None) -> tuple[str, str] | None:
    """If ``locator_str`` resolves to an ``<option>`` inside a ``<select>``:
    ``(select_locator_str, option_label)``, else None. The select locator is
    a leaf selector in the same frame as the option (reuse ``frame_info``)."""
    try:
        scope: Any = page
        for fi in ((frame_info or {}).get("frameInfo") or []):
            sel = ((fi.get("selectors") or [{}])[0]).get("selector")
            if sel:
                scope = scope.frame_locator(sel)
        locator = scope.locator(locator_str).first
        # Not attached (yet): no probe wait; the real click owns the wait.
        if await locator.count() == 0:
            return None
        probe = await locator.evaluate(_OPTION_PROBE_JS, timeout=_TIMEOUT_MS)
    except Exception:  # noqa: BLE001
        return None
    if not probe:
        return None
    tag = _new_tag()
    try:
        ok = await locator.evaluate(
            "(el, tag) => { const s = el.closest('select'); if (!s) return false;"
            " s.setAttribute('data-testmu-resolve', tag); return true; }",
            tag, timeout=_TIMEOUT_MS,
        )
    except Exception:  # noqa: BLE001
        return None
    if not ok:
        return None
    element = await _resolve_tagged(page, {}, tag)
    select_locator = element.get("locator")
    if not select_locator:
        return None
    return select_locator, str(probe.get("label") or "")
