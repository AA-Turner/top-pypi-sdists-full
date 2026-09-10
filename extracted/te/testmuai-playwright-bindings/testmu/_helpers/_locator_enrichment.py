"""Synthesize a stable selector for a DOM element via CDP.

Strategy priority:
  1. backend_dom_node_id  → DOM.resolveNode (exact node)
  2. bounding_box only    → Runtime.evaluate elementFromPoint(cx, cy)
  3. else                 → None

Selector synthesis, once the node is resolved:
  a. With a ``page``: tag the node with a temporary attribute and ask
     Playwright's own selector generator (the per-frame ``resolveSelector``
     protocol command — the same engine ``codegen`` and the authoring tape
     use) to describe it. The result is unique by construction and carries
     the element's role/name (``internal:role=link[name="…"i]``), so a healed
     selector for one row of a list never matches its siblings. An
     iframe-resident node comes back as a cross-frame chain; only the leaf is
     returned (the caller scopes the retry with its own frame chain).
  b. Fallback (no ``page``, or the generator found nothing): the attribute
     walk — #id → [data-testid="…"]/[data-test*] → tag[aria-label="…"]
     → minimal CSS path (tag:nth-of-type) → null. Note that ids and test ids
     are often shared across repeated rows; this path does not check
     uniqueness, which is why every heal passes the page.

Output: {"locator": str, "locator_type": "playwright" | "css"} or None.
"""
from __future__ import annotations

import contextlib
import logging
import uuid
from typing import Any

_log = logging.getLogger("testmu")

# Temporary marker set on the resolved node so Playwright's generator can be
# pointed at exactly that element; always removed afterwards.
_TAG_ATTR = "data-testmu-resolve"

# Delimiter Playwright uses to join cross-frame selector parts (frames.js,
# ``Frame.resolveSelector``). Only the leaf element selector is kept.
_CROSS_FRAME_DELIM = " >> internal:control=enter-frame >> "

# Runs on the resolved node. A text node has no attributes — climb to its
# parent element so a real, taggable element is marked.
_TAG_JS = """
function(tag) {
    var el = (this.nodeType === 3 ? this.parentElement : this);
    if (!el || el.nodeType !== 1) return false;
    el.setAttribute('data-testmu-resolve', tag);
    return true;
}
"""

# Finds the tagged element (piercing shadow roots) and removes the marker.
# Returns true when it removed one.
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

_SELECTOR_JS = r"""
function() {
    const el = this;
    if (!el || el.nodeType !== 1) return null;

    if (el.id && /^[A-Za-z][\w-]*$/.test(el.id)) {
        return {locator: '#' + CSS.escape(el.id), locator_type: 'css'};
    }
    for (const a of ['data-testid','data-test-id','data-test','data-qa']) {
        const v = el.getAttribute(a);
        if (v) {
            return {
                locator: '[' + a + '="' + v.replace(/"/g,'\\"') + '"]',
                locator_type: 'css',
            };
        }
    }
    const aria = el.getAttribute('aria-label');
    if (aria) {
        return {
            locator: el.tagName.toLowerCase() + '[aria-label="' + aria.replace(/"/g,'\\"') + '"]',
            locator_type: 'css',
        };
    }
    function path(node) {
        const segs = [];
        while (node && node.nodeType === 1 && node !== document.body) {
            let seg = node.tagName.toLowerCase();
            if (node.parentNode) {
                const sib = Array.from(node.parentNode.children || []).filter(
                    c => c.tagName === node.tagName
                );
                if (sib.length > 1) {
                    seg += ':nth-of-type(' + (sib.indexOf(node) + 1) + ')';
                }
            }
            segs.unshift(seg);
            node = node.parentNode;
        }
        return segs.join(' > ');
    }
    const css = path(el);
    if (css) return {locator: css, locator_type: 'css'};
    return null;
}
"""


async def _resolve_object_id(cdp, element: dict[str, Any]) -> str | None:
    bid = element.get("backend_dom_node_id")
    if bid is not None:
        try:
            r = await cdp.send("DOM.resolveNode", {"backendNodeId": bid})
            return r.get("object", {}).get("objectId")
        except Exception as e:
            _log.warning("[autoheal] DOM.resolveNode(backendNodeId=%s) failed: %s", bid, e)

    bbox = element.get("bounding_box")
    if bbox:
        cx = int(bbox.get("x", 0) + bbox.get("width", 0) / 2)
        cy = int(bbox.get("y", 0) + bbox.get("height", 0) / 2)
        try:
            r = await cdp.send("Runtime.evaluate", {
                "expression": f"document.elementFromPoint({cx},{cy})",
                "returnByValue": False,
            })
            return r.get("result", {}).get("objectId")
        except Exception as e:
            _log.warning("[autoheal] elementFromPoint(%d,%d) failed: %s", cx, cy, e)
    return None


def _frames_main_first(page) -> list[Any]:
    """``page.frames`` with the main frame first — the common case is tried
    before any iframe."""
    main = page.main_frame
    return [main] + [f for f in page.frames if f != main]


async def _resolve_selector_across_frames(page, selector: str) -> tuple[str | None, Any]:
    """Ask Playwright's per-frame ``resolveSelector`` for ``selector`` until a
    frame answers. Returns ``(resolved, frame)`` or ``(None, None)``.

    The command is private to the driver protocol (no public wrapper), which
    is also how the authoring side records tape locators; the Python client
    unwraps the single-key result to the selector string.
    """
    for frame in _frames_main_first(page):
        try:
            channel = frame._impl_obj._channel
            try:
                resolved = await channel.send("resolveSelector", None, {"selector": selector})
            except TypeError:
                # Older client signature without the timeout argument.
                resolved = await channel.send("resolveSelector", {"selector": selector})
        except Exception:
            continue
        if isinstance(resolved, dict):
            resolved = resolved.get("resolvedSelector")
        if resolved:
            return str(resolved), frame
    return None, None


async def _remove_tag(page, tag: str, frame: Any = None) -> None:
    """Remove the marker. With ``frame`` known, only that frame is cleaned;
    otherwise every frame is scanned until one reports a removal."""
    frames = [frame] if frame is not None else list(page.frames)
    for f in frames:
        try:
            removed = await f.evaluate(_UNTAG_JS, tag)
        except Exception:
            continue
        if removed and frame is None:
            return


async def _generate_with_playwright(cdp, object_id: str, page) -> dict[str, Any] | None:
    """Tag the resolved node and let Playwright's generator describe it."""
    tag = "h" + uuid.uuid4().hex[:12]
    try:
        r = await cdp.send("Runtime.callFunctionOn", {
            "objectId": object_id,
            "functionDeclaration": _TAG_JS,
            "arguments": [{"value": tag}],
            "returnByValue": True,
        })
        if not (r.get("result") or {}).get("value"):
            return None
    except Exception as e:
        _log.warning("[autoheal] tagging the resolved node failed: %s", e)
        return None

    frame = None
    try:
        resolved, frame = await _resolve_selector_across_frames(
            page, f"css=[{_TAG_ATTR}='{tag}']",
        )
        if not resolved:
            return None
        leaf = resolved.split(_CROSS_FRAME_DELIM)[-1].strip()
        if not leaf:
            return None
        return {"locator": leaf, "locator_type": "playwright"}
    finally:
        with contextlib.suppress(Exception):
            await _remove_tag(page, tag, frame)


async def enrich_element_locator(
    cdp, element: dict[str, Any], page: Any = None,
) -> dict[str, Any] | None:
    """Return {locator, locator_type} for a flat-DOM element, or None.

    Pass ``page`` whenever it is available: it enables Playwright's own
    selector generator, whose output is unique by construction. Without it the
    attribute walk runs alone, and its ids/test ids may be shared across
    repeated rows.
    """
    object_id = await _resolve_object_id(cdp, element)
    if not object_id:
        return None

    if page is not None:
        generated = await _generate_with_playwright(cdp, object_id, page)
        if generated:
            return generated

    try:
        resp = await cdp.send("Runtime.callFunctionOn", {
            "objectId": object_id,
            "functionDeclaration": _SELECTOR_JS,
            "returnByValue": True,
        })
        r = resp.get("result", {}).get("value")
        if r and r.get("locator"):
            return {"locator": r["locator"], "locator_type": r.get("locator_type", "css")}
    except Exception as e:
        _log.warning("[autoheal] selector synthesis failed: %s", e)
    return None
