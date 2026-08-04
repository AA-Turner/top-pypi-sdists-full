"""Common structured (accessibility-tree) DOM capture + serializer.

General DOM infrastructure holding the nested ``AxNode`` representation, the
``build_structured_dom`` serializer, and the CDP tree-capture glue. Used by the
textual heal path today but not specific to it.

The serialize logic produces a stable, nested index space so a recorded
extraction's ``el(i)`` references resolve consistently at record, replay, and heal
time. It walks a binding-local ``AxNode`` so it has no external dependencies.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any

_log = logging.getLogger("testmu")

# Structural-container roles that never render — children promoted to the
# container's depth (mirrors Playwright normalizeGenericRoles for always-redundant
# roles). 'generic' is handled separately (kept when structural).
_ALWAYS_COLLAPSE = frozenset({"none", "rootwebarea", "webarea", "genericcontainer"})
# Static-text roles render as `text: ...` without an index.
_TEXT_ROLES = frozenset({"statictext", "text"})


@dataclass
class AxNode:
    """Binding-local accessibility node read by the serializer."""

    role: str = ""
    name: str = ""
    description: str = ""
    value: str = ""
    url: str | None = None
    level: int | None = None
    checked: bool | str | None = None
    disabled: bool = False
    selected: bool | None = None
    expanded: bool | None = None
    pressed: bool | str | None = None
    required: bool = False
    readonly: bool = False
    focused: bool = False
    is_visible: bool | None = None
    in_viewport: bool | None = None
    backend_dom_node_id: int | None = None
    # Capture-only fields (A2): set by the frame-aware CDP/snapshot parsers
    # ported from the runner's accessibility.py so the port stays a verbatim
    # AccessibilityNode->AxNode rename. Additive and inert to the serializer —
    # serialize_ax_tree never reads them. Names/defaults match the runner's
    # src.browser_protocol.AccessibilityNode exactly (A3 parity).
    bounding_box: dict[str, float] | None = None
    autocomplete: str | None = None
    multiselectable: bool | None = None
    orientation: str | None = None
    roledescription: str | None = None
    haspopup: str | None = None
    keyshortcuts: str | None = None
    children: list["AxNode"] = field(default_factory=list)

    def __post_init__(self) -> None:
        # AX ``value`` may arrive numeric: a range slider, number spinbutton,
        # meter, or progressbar reports its value as an int/float (Playwright's
        # accessibility snapshot returns e.g. ``50``, CDP an AXValue number).
        # The serializer treats ``value`` as text (len/truncate), so a numeric
        # value crashed the WHOLE page snapshot. Coerce to str at the single
        # construction boundary; ``None``/``""`` normalize to ``""`` so the
        # ``if node.value`` guards still read "no value", and ``0`` renders as
        # ``"0"`` (a real value, not empty).
        if self.value is None:
            self.value = ""
        elif not isinstance(self.value, str):
            self.value = str(self.value)


@dataclass
class StructuredDom:
    """``text`` = nested prompt snapshot; ``index_to_backend_id`` maps each
    rendered ``[i]`` to its CDP backend_dom_node_id for el(i) resolution."""

    text: str
    index_to_backend_id: dict[int, int]


def build_structured_dom(root: AxNode) -> StructuredDom:
    lines: list[str] = []
    index_to_backend_id: dict[int, int] = {}
    counter = [0]
    _walk(root, 0, lines, index_to_backend_id, counter)
    return StructuredDom(text="\n".join(lines), index_to_backend_id=index_to_backend_id)


def _walk(node: AxNode, depth: int, lines: list[str],
          index_to_backend_id: dict[int, int], counter: list[int]) -> None:
    role = (node.role or "").strip().lower()

    # Visibility / viewport filter — exclude the node but still walk its children
    # at the same depth (so a hidden wrapper doesn't drop visible descendants).
    if node.is_visible is False or node.in_viewport is False:
        _walk_children(node, depth, lines, index_to_backend_id, counter)
        return

    if role in _TEXT_ROLES:
        if node.name:
            lines.append(f'{"  " * depth}text: {node.name}')
        return

    if _should_collapse(role, node):
        _walk_children(node, depth, lines, index_to_backend_id, counter)
        return

    counter[0] += 1
    index = counter[0]
    indent = "  " * depth
    lines.append(_render_line(node, role, index, indent))
    if node.backend_dom_node_id is not None:
        index_to_backend_id[index] = node.backend_dom_node_id
    if node.url:
        lines.append(f'{"  " * (depth + 1)}/url: {node.url}')

    _walk_children(node, depth + 1, lines, index_to_backend_id, counter)


def _walk_children(node: AxNode, depth: int, lines: list[str],
                   index_to_backend_id: dict[int, int], counter: list[int]) -> None:
    for child in node.children:
        _walk(child, depth, lines, index_to_backend_id, counter)


def _should_collapse(role: str, node: AxNode) -> bool:
    if role in _ALWAYS_COLLAPSE:
        return True
    if role == "generic":
        return _visible_child_count(node) < 2
    return False


def _visible_child_count(node: AxNode) -> int:
    return sum(
        1
        for c in node.children
        if c.is_visible is not False and c.in_viewport is not False
    )


def _render_line(node: AxNode, role: str, index: int, indent: str) -> str:
    parts = [f'{indent}[{index}] {role} "{node.name}"']
    if node.level is not None:
        parts.append(f"[level={node.level}]")
    if node.checked is True:
        parts.append("[checked]")
    elif node.checked == "mixed":
        parts.append("[checked=mixed]")
    if node.disabled:
        parts.append("[disabled]")
    if node.selected is True:
        parts.append("[selected]")
    if node.expanded is True:
        parts.append("[expanded]")
    if node.pressed is True:
        parts.append("[pressed]")
    if node.required:
        parts.append("[required]")
    if node.readonly:
        parts.append("[readonly]")
    if node.focused:
        parts.append("[focused]")
    if node.value:
        parts.append(f'value="{node.value}"')
    if node.description:
        parts.append(f'[desc="{node.description}"]')
    return " ".join(parts)


# ---------------------------------------------------------------------------
# CDP tree capture (integration glue). Produces an AxNode tree with
# is_visible/in_viewport derived from DOM.getBoxModel boxes, so
# build_structured_dom's viewport filter is effective. Not unit-tested (CDP I/O).
# ---------------------------------------------------------------------------

_SKIP_BOX_ROLES = frozenset({"none", "generic", "rootwebarea", "webarea"})


def _is_visible(box: dict | None) -> bool | None:
    if box is None:
        return None
    return box.get("width", 0) > 0 and box.get("height", 0) > 0


def _is_in_viewport(box: dict | None, vw: float, vh: float) -> bool | None:
    if box is None:
        return None
    x, y = box.get("x", 0), box.get("y", 0)
    w, h = box.get("width", 0), box.get("height", 0)
    if x + w < 0 or x > vw:
        return False
    if y + h < 0 or y > vh:
        return False
    return True


def _cdp_prop(properties: list[dict] | None, name: str) -> Any:
    if not properties:
        return None
    for p in properties:
        if p.get("name") == name:
            v = p.get("value", {})
            return v.get("value") if isinstance(v, dict) else None
    return None


def _ax_value(node: dict, key: str) -> str:
    info = node.get(key, {})
    return info.get("value", "") if isinstance(info, dict) else ""


def _parse_node(node: dict, by_id: dict[str, dict], vw: float, vh: float) -> AxNode:
    props = node.get("properties", [])
    box = node.get("_bounding_box")
    children = []
    for cid in node.get("childIds", []):
        child = by_id.get(cid)
        if child:
            children.append(_parse_node(child, by_id, vw, vh))
    return AxNode(
        role=_ax_value(node, "role"),
        name=_ax_value(node, "name"),
        description=_ax_value(node, "description"),
        value=_ax_value(node, "value"),
        url=_cdp_prop(props, "url"),
        level=_cdp_prop(props, "level"),
        checked=_cdp_prop(props, "checked"),
        disabled=_cdp_prop(props, "disabled") or False,
        selected=_cdp_prop(props, "selected"),
        expanded=_cdp_prop(props, "expanded"),
        pressed=_cdp_prop(props, "pressed"),
        required=_cdp_prop(props, "required") or False,
        readonly=_cdp_prop(props, "readonly") or False,
        focused=_cdp_prop(props, "focused") or False,
        is_visible=_is_visible(box),
        in_viewport=_is_in_viewport(box, vw, vh),
        backend_dom_node_id=node.get("backendDOMNodeId"),
        children=children,
    )


async def capture_structured_dom(page) -> StructuredDom | None:
    """Capture the current viewport as a structured (nested) DOM snapshot.

    getFullAXTree → fetch DOM.getBoxModel boxes for visible non-container nodes →
    derive is_visible/in_viewport → AxNode tree → build_structured_dom. Returns
    None if the tree is empty or capture fails.
    """
    vp = page.viewport_size or {}
    vw = vp.get("width")
    vh = vp.get("height")
    if not vw or not vh:
        # viewport_size is None when Playwright connects over CDP (grid / real
        # device) since the viewport was never set. Read the live viewport
        # directly so the in-viewport filter stays effective. Mirrors the TS binding.
        try:
            dims = await page.evaluate(
                "() => ({ width: window.innerWidth, height: window.innerHeight })"
            )
            if dims and dims.get("width") and dims.get("height"):
                vw, vh = dims["width"], dims["height"]
        except Exception:  # noqa: BLE001
            pass
    vw = float(vw or 1280)
    vh = float(vh or 800)
    try:
        cdp = await page.context.new_cdp_session(page)
        try:
            result = await cdp.send("Accessibility.getFullAXTree", {})
            nodes = result.get("nodes", [])
            if not nodes:
                return None

            box_targets = []
            for node in nodes:
                bid = node.get("backendDOMNodeId")
                if not bid:
                    continue
                role = _ax_value(node, "role").strip().lower()
                if role not in _SKIP_BOX_ROLES:
                    box_targets.append(bid)

            boxes: dict[int, dict] = {}

            async def _fetch(bid: int):
                try:
                    r = await cdp.send("DOM.getBoxModel", {"backendNodeId": bid})
                    border = r.get("model", {}).get("border", [])
                    if len(border) >= 8:
                        xs = border[0::2][:4]
                        ys = border[1::2][:4]
                        x, y = min(xs), min(ys)
                        boxes[bid] = {"x": x, "y": y,
                                      "width": max(xs) - x, "height": max(ys) - y}
                except Exception:  # noqa: BLE001
                    pass

            if box_targets:
                await asyncio.gather(*(_fetch(b) for b in box_targets))

            by_id: dict[str, dict] = {}
            for node in nodes:
                nid = node.get("nodeId")
                if nid:
                    bid = node.get("backendDOMNodeId")
                    if bid and bid in boxes:
                        node["_bounding_box"] = boxes[bid]
                    by_id[nid] = node

            root = next((n for n in nodes if not n.get("parentId")), nodes[0])
            tree = _parse_node(root, by_id, vw, vh)
            return build_structured_dom(tree)
        finally:
            await cdp.detach()
    except Exception as e:  # noqa: BLE001
        _log.warning("[dom_structured] capture failed: %s", e)
        return None
