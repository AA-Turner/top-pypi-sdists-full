"""Accessibility DOM capture utility.

This module provides functions to capture the full Accessibility DOM tree
from a web page using Playwright's accessibility API.

Ported verbatim from the reference accessibility-capture implementation
(the internal browser-automation project this capture logic originates
from) with exactly these mechanical changes: the original's
``from src.browser_protocol import AccessibilityNode`` is dropped (the
binding must not import from ``src.*``) and every ``AccessibilityNode``
construction/annotation is renamed to the binding-local ``AxNode`` (from
``testmu._helpers._dom_structured``). No logic is redesigned; this port
is verified byte-identical in behavior against the original.

The original's ``capture_accessibility_tree_as_dict`` helper is
intentionally NOT ported: it is not part of the frame-aware capture path
this package feeds into ``serialize_ax_tree`` (the original keeps its own
copy), and it calls ``AxNode.to_dict()`` which the binding-local ``AxNode``
does not define (a method, not a capture-only field — out of scope for
this port).
"""

import asyncio
from typing import Any

from playwright.async_api import Page

from .._dom_structured import AxNode
from ._constants import INTERACTIVE_ROLES, is_in_viewport, is_visible


def _parse_snapshot_node(
    node: dict[str, Any],
    viewport_width: float = 1280,
    viewport_height: float = 800,
) -> AxNode:
    """Parse a Playwright accessibility snapshot node into an AxNode.

    Args:
        node: Raw node dictionary from Playwright's accessibility.snapshot().
        viewport_width: Viewport width for calculating in_viewport.
        viewport_height: Viewport height for calculating in_viewport.

    Returns:
        Parsed AxNode with all properties and children.
    """
    children = []
    if "children" in node:
        children = [
            _parse_snapshot_node(child, viewport_width, viewport_height)
            for child in node["children"]
        ]

    bounding_box = node.get("boundingBox")
    node_is_visible = is_visible(bounding_box)
    node_in_viewport = is_in_viewport(bounding_box, viewport_width, viewport_height)

    return AxNode(
        role=node.get("role", ""),
        name=node.get("name", ""),
        description=node.get("description", ""),
        value=node.get("value", ""),
        bounding_box=bounding_box,
        in_viewport=node_in_viewport,
        is_visible=node_is_visible,
        focused=node.get("focused", False),
        disabled=node.get("disabled", False),
        checked=_normalize_tristate(node.get("checked")),
        expanded=node.get("expanded"),
        selected=node.get("selected"),
        pressed=_normalize_tristate(node.get("pressed")),
        readonly=node.get("readonly", False),
        required=node.get("required", False),
        level=node.get("level"),
        autocomplete=node.get("autocomplete"),
        multiselectable=node.get("multiselectable"),
        orientation=node.get("orientation"),
        children=children,
    )


def _get_cdp_property_value(
    properties: list[dict[str, Any]] | None, name: str
) -> Any:
    """Extract a property value from CDP accessibility node properties.

    Args:
        properties: List of CDP property dictionaries.
        name: The property name to find.

    Returns:
        The property value, or None if not found.
    """
    if not properties:
        return None
    for prop in properties:
        if prop.get("name") == name:
            value = prop.get("value", {})
            return value.get("value")
    return None


def _normalize_tristate(value: Any) -> bool | str | None:
    """Normalize a tri-state AX value to True / False / "mixed" / None.

    CDP reports tri-state AXValues (``checked``, ``pressed``) as the STRINGS
    "true" / "false" / "mixed", not as booleans. Python treats the non-empty
    string "false" as truthy, so a raw pass-through makes an UNCHECKED box
    indistinguishable from a checked one to every downstream truthiness test
    (observed regression: five empty checkboxes serialized as ``[checked]``).

    Playwright's snapshot format already uses real booleans / "mixed", so this
    is idempotent there and safe to apply on both parse paths.

    Returns None for absent or unrecognized values — "this element has no
    tri-state", which is distinct from False ("it has one and it is off").
    """
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if lowered == "mixed":
            return "mixed"
    return None


def _parse_cdp_ax_node(
    node: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
    viewport_width: float = 1280,
    viewport_height: float = 800,
) -> AxNode:
    """Parse a CDP accessibility node into an AxNode.

    Args:
        node: Raw node dictionary from CDP Accessibility.getFullAXTree.
        nodes_by_id: Dictionary mapping node IDs to node data for child lookup.
        viewport_width: Viewport width for calculating in_viewport.
        viewport_height: Viewport height for calculating in_viewport.

    Returns:
        Parsed AxNode with all properties and children.
    """
    role_info = node.get("role", {})
    role = role_info.get("value", "") if isinstance(role_info, dict) else ""

    name_info = node.get("name", {})
    name = name_info.get("value", "") if isinstance(name_info, dict) else ""

    desc_info = node.get("description", {})
    description = desc_info.get("value", "") if isinstance(desc_info, dict) else ""

    value_info = node.get("value", {})
    value = value_info.get("value", "") if isinstance(value_info, dict) else ""

    properties = node.get("properties", [])

    bounding_box = node.get("_bounding_box")
    node_is_visible = is_visible(bounding_box)
    node_in_viewport = is_in_viewport(bounding_box, viewport_width, viewport_height)

    children = []
    child_ids = node.get("childIds", [])
    for child_id in child_ids:
        child_node = nodes_by_id.get(child_id)
        if child_node:
            children.append(
                _parse_cdp_ax_node(
                    child_node, nodes_by_id, viewport_width, viewport_height
                )
            )

    return AxNode(
        role=role,
        name=name,
        description=description,
        value=value,
        bounding_box=bounding_box,
        in_viewport=node_in_viewport,
        is_visible=node_is_visible,
        focused=_get_cdp_property_value(properties, "focused") or False,
        disabled=_get_cdp_property_value(properties, "disabled") or False,
        checked=_normalize_tristate(_get_cdp_property_value(properties, "checked")),
        expanded=_get_cdp_property_value(properties, "expanded"),
        selected=_get_cdp_property_value(properties, "selected"),
        pressed=_normalize_tristate(_get_cdp_property_value(properties, "pressed")),
        readonly=_get_cdp_property_value(properties, "readonly") or False,
        required=_get_cdp_property_value(properties, "required") or False,
        level=_get_cdp_property_value(properties, "level"),
        autocomplete=_get_cdp_property_value(properties, "autocomplete"),
        multiselectable=_get_cdp_property_value(properties, "multiselectable"),
        orientation=_get_cdp_property_value(properties, "orientation"),
        roledescription=_get_cdp_property_value(properties, "roledescription"),
        haspopup=_get_cdp_property_value(properties, "hasPopup"),
        url=_get_cdp_property_value(properties, "url"),
        keyshortcuts=_get_cdp_property_value(properties, "keyshortcuts"),
        backend_dom_node_id=node.get("backendDOMNodeId"),
        children=children,
    )


async def _capture_ax_tree_via_session(
    cdp_session: Any,
    *,
    frame_id: str | None = None,
    depth: int | None = None,
    viewport_width: float = 1280,
    viewport_height: float = 800,
    all_bounding_boxes: bool = False,
    skip_bounding_boxes: bool = False,
) -> AxNode | None:
    """Capture one frame's accessibility tree via an already-open CDP session.

    Shared by ``_capture_accessibility_tree_via_cdp`` (main-frame path, which
    owns/detaches its own session) and ``frame_capture.py`` (per-frame
    capture), which reuses a session it manages itself: either the page's main
    session + a same-process child's ``frame_id``, or an OOPIF's own
    dedicated session with ``frame_id=None`` (its default root IS that
    frame). Does not create or detach ``cdp_session`` — that is the
    caller's responsibility.

    Args:
        cdp_session: An already-attached CDP session (``Accessibility``
            domain reachable from it).
        frame_id: CDP frame id to pass as ``Accessibility.getFullAXTree``'s
            ``frameId`` param. None omits the param (root/default frame of
            whatever target ``cdp_session`` is attached to).
        depth: Maximum depth of the tree. None for full tree.
        viewport_width: Viewport width for calculating in_viewport.
        viewport_height: Viewport height for calculating in_viewport.
        all_bounding_boxes: If True, fetch bounding boxes for all visible
            nodes (not just interactive). Used by full flat DOM.
        skip_bounding_boxes: If True, fetch NO bounding boxes at all — zero
            ``DOM.getBoxModel`` calls are issued, regardless of
            ``all_bounding_boxes``. Used by text-mode AX document capture
            (see ``PlaywrightBrowser.get_ax_document``), where there is no
            viewport section to render and geometry for the single acted-on
            node is instead fetched lazily via ``prepare_ref_action``.
            Takes precedence over ``all_bounding_boxes``.

    Returns:
        The root AxNode, or None if empty.
    """
    params: dict[str, Any] = {}
    if depth is not None:
        params["depth"] = depth
    if frame_id:
        params["frameId"] = frame_id

    result = await cdp_session.send("Accessibility.getFullAXTree", params)

    nodes = result.get("nodes", [])
    if not nodes:
        return None

    # Decide which nodes need bounding boxes.
    skip_box_roles = frozenset({"none", "generic", "rootwebarea", "webarea"})
    nodes_for_boxes = []
    if not skip_bounding_boxes:
        for node in nodes:
            backend_id = node.get("backendDOMNodeId")
            if not backend_id:
                continue
            role_info = node.get("role", {})
            role_val = (
                role_info.get("value", "").strip().lower()
                if isinstance(role_info, dict)
                else ""
            )
            if all_bounding_boxes:
                # Full flat DOM mode: all visible nodes except containers
                if role_val not in skip_box_roles:
                    nodes_for_boxes.append((node, backend_id))
            else:
                # Interactive-only mode (default): minimal CDP calls
                if role_val in INTERACTIVE_ROLES:
                    nodes_for_boxes.append((node, backend_id))

    bounding_boxes: dict[int, dict[str, float]] = {}

    async def _fetch_box(bid: int) -> tuple[int, dict[str, float] | None]:
        try:
            box_result = await cdp_session.send(
                "DOM.getBoxModel",
                {"backendNodeId": bid},
            )
            model = box_result.get("model", {})
            # Use border quad (not content) — matches
            # getBoundingClientRect() and gives the full
            # clickable area including padding/border.
            content = model.get("border", [])
            if len(content) >= 8:
                x = min(content[0], content[2], content[4], content[6])
                y = min(content[1], content[3], content[5], content[7])
                x_max = max(content[0], content[2], content[4], content[6])
                y_max = max(content[1], content[3], content[5], content[7])
                return bid, {
                    "x": x, "y": y,
                    "width": x_max - x, "height": y_max - y,
                }
        except Exception:
            pass
        return bid, None

    if nodes_for_boxes:
        try:
            results = await asyncio.gather(
                *(_fetch_box(bid) for _, bid in nodes_for_boxes)
            )
            for bid, box in results:
                if box is not None:
                    bounding_boxes[bid] = box
        except Exception:
            pass

    nodes_by_id: dict[str, dict[str, Any]] = {}
    for node in nodes:
        node_id = node.get("nodeId")
        if node_id:
            backend_id = node.get("backendDOMNodeId")
            if backend_id and backend_id in bounding_boxes:
                node["_bounding_box"] = bounding_boxes[backend_id]
            nodes_by_id[node_id] = node

    root_node = None
    for node in nodes:
        if not node.get("parentId"):
            root_node = node
            break

    if not root_node and nodes:
        root_node = nodes[0]

    if not root_node:
        return None

    return _parse_cdp_ax_node(
        root_node, nodes_by_id, viewport_width, viewport_height
    )


async def _capture_accessibility_tree_via_cdp(
    page: Page,
    *,
    depth: int | None = None,
    viewport_width: float = 1280,
    viewport_height: float = 800,
    all_bounding_boxes: bool = False,
    skip_bounding_boxes: bool = False,
) -> AxNode | None:
    """Capture accessibility tree using Chrome DevTools Protocol.

    This is the fallback method for Playwright 1.57+ where page.accessibility
    was removed.

    Args:
        page: The Playwright page.
        depth: Maximum depth of the tree. None for full tree.
        viewport_width: Viewport width for calculating in_viewport.
        viewport_height: Viewport height for calculating in_viewport.
        all_bounding_boxes: If True, fetch bounding boxes for all visible
            nodes (not just interactive). Used by full flat DOM.
        skip_bounding_boxes: If True, fetch NO bounding boxes at all — zero
            ``DOM.getBoxModel`` calls are issued, regardless of
            ``all_bounding_boxes``. Used by text-mode AX document capture
            (see ``PlaywrightBrowser.get_ax_document``), where there is no
            viewport section to render and geometry for the single acted-on
            node is instead fetched lazily via ``prepare_ref_action``.
            Takes precedence over ``all_bounding_boxes``.

    Returns:
        The root AxNode, or None if empty.
    """
    try:
        cdp_session = await page.context.new_cdp_session(page)
        try:
            return await _capture_ax_tree_via_session(
                cdp_session,
                depth=depth,
                viewport_width=viewport_width,
                viewport_height=viewport_height,
                all_bounding_boxes=all_bounding_boxes,
                skip_bounding_boxes=skip_bounding_boxes,
            )
        finally:
            await cdp_session.detach()

    except Exception:
        return None


async def capture_accessibility_tree(
    page: Page,
    *,
    interesting_only: bool = False,
    viewport_width: float | None = None,
    viewport_height: float | None = None,
    all_bounding_boxes: bool = False,
    skip_bounding_boxes: bool = False,
) -> AxNode | None:
    """Capture the full accessibility tree from a page.

    This function uses Playwright's accessibility API to capture the complete
    accessibility DOM tree, including all elements with their roles, names,
    descriptions, states, and bounding boxes.

    For Playwright 1.57+ where page.accessibility was removed, this function
    falls back to using Chrome DevTools Protocol (CDP) to get the tree.

    Args:
        page: The Playwright page to capture the accessibility tree from.
        interesting_only: If True, only return nodes that are considered
            "interesting" by Playwright (elements that are focusable or have
            an accessible name). If False (default), returns all nodes.
            Note: This parameter is ignored when using CDP fallback.
        viewport_width: Viewport width for calculating in_viewport. If None,
            will be fetched from page.
        viewport_height: Viewport height for calculating in_viewport. If None,
            will be fetched from page.
        all_bounding_boxes: If True, fetch bounding boxes for all visible
            nodes (not just interactive). Used by full flat DOM.
        skip_bounding_boxes: If True, fetch NO bounding boxes at all (zero
            ``DOM.getBoxModel`` calls) on the CDP fallback path. Used by
            text-mode AX document capture. Takes precedence over
            ``all_bounding_boxes``. Only honored on the CDP path — the
            legacy ``page.accessibility.snapshot()`` path (unreachable on
            the pinned Playwright >=1.57) has no equivalent knob.

    Returns:
        The root AxNode of the tree, or None if the tree is empty
        or if the accessibility API is not available.
    """
    viewport_width = viewport_width or 1280
    viewport_height = viewport_height or 800

    if hasattr(page, "accessibility"):
        snapshot = await page.accessibility.snapshot(interesting_only=interesting_only)
        if snapshot is not None:
            return _parse_snapshot_node(snapshot, viewport_width, viewport_height)

    return await _capture_accessibility_tree_via_cdp(
        page, viewport_width=viewport_width, viewport_height=viewport_height,
        all_bounding_boxes=all_bounding_boxes,
        skip_bounding_boxes=skip_bounding_boxes,
    )
