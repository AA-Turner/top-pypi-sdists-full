from __future__ import annotations

"""Shared CDP flat-DOM + element-snapshot capture.

Lifted out of vision.py so autoheal and textual_query both reuse it
without circular imports. 1-based indexing matches the recorder's flat-DOM format.
"""
import json as _json
import logging
from typing import Any

_log = logging.getLogger("testmu")

_CSS_PROPERTIES = [
    "color", "background-color", "border-color",
    "font-size", "font-family", "font-weight", "font-style",
    "display", "visibility", "opacity",
]

_SKIP_ROLES = frozenset({"none", "generic", "rootwebarea", "webarea", "inlinetextbox"})

_SNAPSHOT_JS = """
function() {
    let el = this;
    if (el.nodeType === 3 || !el.tagName) {
        el = el.parentElement || el.parentNode;
    }
    if (!el || !el.tagName) {
        return { tag_name: '', text_content: '', attributes: {}, styles: {}, states: {} };
    }
    const attrs = {};
    for (const attr of el.attributes || []) attrs[attr.name] = attr.value;
    const states = {};
    for (const k of ['disabled','checked','readOnly','required','hidden','selected','value','type']) {
        if (k in el) states[k] = el[k];
    }
    const styles = {};
    try {
        const cs = window.getComputedStyle(el);
        for (const p of %s) {
            const v = cs.getPropertyValue(p);
            if (v) styles[p] = v;
        }
    } catch(e) {}
    return {
        tag_name: el.tagName.toLowerCase(),
        text_content: (el.textContent || '').trim().substring(0, 500),
        attributes: attrs, states, styles,
    };
}
""" % _json.dumps(_CSS_PROPERTIES)


def build_flat_dom(a11y_nodes: list) -> list[dict[str, Any]]:
    """CDP Accessibility.getFullAXTree → flat DOM (1-based index)."""
    result = []
    index = 1
    for node in a11y_nodes:
        if node.get("ignored", False):
            continue
        role_obj = node.get("role", {})
        role = (role_obj.get("value", "") if isinstance(role_obj, dict) else str(role_obj)).strip().lower()
        if role in _SKIP_ROLES:
            continue
        name_obj = node.get("name", {})
        name = name_obj.get("value", "") if isinstance(name_obj, dict) else str(name_obj)

        element: dict[str, Any] = {"index": index, "role": role, "name": name}
        if (bid := node.get("backendDOMNodeId")) is not None:
            element["backend_dom_node_id"] = bid

        props = {}
        for prop in node.get("properties", []):
            v = prop.get("value", {})
            val = v.get("value") if isinstance(v, dict) else v
            if val is not None:
                props[prop.get("name", "")] = val
        if props.get("disabled"):
            element["disabled"] = True
        for k in ("checked", "expanded", "selected", "pressed", "focused", "required", "readonly"):
            if k in props:
                element[k] = props[k]

        val_obj = node.get("value", {})
        if isinstance(val_obj, dict) and val_obj.get("value"):
            element["value"] = val_obj["value"]
        desc_obj = node.get("description", {})
        if isinstance(desc_obj, dict) and desc_obj.get("value"):
            element["description"] = desc_obj["value"]

        result.append(element)
        index += 1
    return result


async def capture_flat_dom(page) -> tuple[Any, list[dict[str, Any]]]:
    """Open a CDP session and capture the flat DOM. Caller owns cdp.detach()."""
    cdp = await page.context.new_cdp_session(page)
    await cdp.send("DOM.enable")
    a11y_resp = await cdp.send("Accessibility.getFullAXTree")
    return cdp, build_flat_dom(a11y_resp.get("nodes", []))


async def get_element_snapshot(cdp, backend_dom_node_id: int) -> dict[str, Any]:
    """CDP snapshot of a single element matching the recorder's format."""
    resolve_resp = await cdp.send("DOM.resolveNode", {"backendNodeId": backend_dom_node_id})
    object_id = resolve_resp.get("object", {}).get("objectId")
    if not object_id:
        return {"tag_name": "", "text_content": "", "attributes": {}, "styles": {}, "states": {}}
    try:
        call_resp = await cdp.send("Runtime.callFunctionOn", {
            "objectId": object_id,
            "functionDeclaration": _SNAPSHOT_JS,
            "returnByValue": True,
        })
        result = call_resp.get("result", {}).get("value", {}) or {}
        return {
            "tag_name": result.get("tag_name", ""),
            "text_content": result.get("text_content", ""),
            "attributes": result.get("attributes", {}),
            "styles": result.get("styles", {}),
            "states": result.get("states", {}),
        }
    except Exception as e:
        _log.warning("[dom_capture] snapshot failed for backendNodeId=%s: %s", backend_dom_node_id, e)
        return {"tag_name": "", "text_content": "", "attributes": {}, "styles": {}, "states": {}}
