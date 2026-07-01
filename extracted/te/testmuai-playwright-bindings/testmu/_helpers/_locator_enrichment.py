from __future__ import annotations

"""Synthesize a stable selector for a flat-DOM element via CDP.

Strategy priority:
  1. backend_dom_node_id  → DOM.resolveNode + Runtime.callFunctionOn → JS
  2. bounding_box only    → Runtime.evaluate elementFromPoint(cx, cy) → same JS
  3. else                 → None

JS selector priority:
    #id  →  [data-testid="…"]/[data-test*]  →  tag[aria-label="…"]
        →  minimal CSS path (tag:nth-of-type)  →  null.

Output: {"locator": str, "locator_type": "css"} or None.
"""
import logging
from typing import Any

_log = logging.getLogger("testmu")

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


async def enrich_element_locator(cdp, element: dict[str, Any]) -> dict[str, Any] | None:
    """Return {locator, locator_type} for a flat-DOM element, or None."""
    object_id = await _resolve_object_id(cdp, element)
    if not object_id:
        return None
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
