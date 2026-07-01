"""CDP accessibility + DOM snapshot capture for selector-less textual queries.

Ports the Chrome / Android CDP capture path from the V2 Selenium source
textual_query and viewport-node-index logic. Used by the textual_query
direct-read path when there is no element selector to locate — the snapshot
is sent to the textual-query endpoint, which reads the value server-side.

iOS Safari has no CDP; that path is intentionally unsupported here and raises
NotImplementedError rather than silently degrading.
"""
import json


def _execute_cdp_command(driver, cmd: str, params=None):
    """Send a raw CDP command via the Selenium command executor (V2 port)."""
    params = params or {}
    platform = driver.capabilities.get("platformName", "").lower()
    if platform == "android":
        resource = "/session/%s/goog/cdp/execute" % driver.session_id
    else:
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({"cmd": cmd, "params": params})
    response = driver.command_executor._request("POST", url, body)
    return response.get("value")


def capture_a11y_dom_snapshot(driver):
    """Capture (a11y_snapshot, dom_snapshot, viewport_node_indices) via CDP.

    Mirrors the V2 Chrome/Android textual query capture path. When the DOM has
    more than 3000 nodes, computes viewport node indices so the endpoint only
    formats what's visible (same threshold + math as V2).
    """
    platform = driver.capabilities.get("platformName", "").lower()
    browser = driver.capabilities.get("browserName", "").lower()
    if platform == "ios" or browser == "safari":
        raise NotImplementedError(
            "Selector-less textual_query direct-read is unsupported on iOS "
            "Safari (no CDP). Provide a selector or run on Chrome."
        )

    _execute_cdp_command(driver, "Accessibility.enable")
    a11y_snapshot = _execute_cdp_command(driver, "Accessibility.getFullAXTree")
    if isinstance(a11y_snapshot, str):
        a11y_snapshot = json.loads(a11y_snapshot)

    dom_snapshot = _execute_cdp_command(driver, "DOMSnapshot.captureSnapshot", {
        "computedStyles": [
            "color", "background-color", "border-color",
            "font-size", "font-family", "font-weight", "font-style",
            "display", "visibility", "opacity",
        ],
        "includeDOMRects": True,
    })
    if isinstance(dom_snapshot, str):
        dom_snapshot = json.loads(dom_snapshot)

    viewport_node_indices = None
    documents = dom_snapshot.get("documents", [{}])
    main_doc = documents[0] if documents else {}
    dom_node_count = len(main_doc.get("nodes", {}).get("nodeType", []))
    if dom_node_count > 3000:
        css_dims = driver.execute_script(
            "return {w: window.innerWidth, h: window.innerHeight, "
            "sx: window.scrollX, sy: window.scrollY}"
        )
        css_w = css_dims.get("w", 1280)
        css_h = css_dims.get("h", 960)
        # CDP bounds are layout pixels; JS returns CSS pixels. Scale CSS
        # viewport to layout coords so the rect comparison is correct (mobile
        # devicePixelRatio differs from desktop).
        content_w = main_doc.get("contentWidth", css_w)
        scale = content_w / css_w if css_w > 0 else 1
        if "scrollOffsetX" in main_doc:
            scroll_x = main_doc["scrollOffsetX"]
            scroll_y = main_doc.get("scrollOffsetY", 0)
        else:
            scroll_x = round(css_dims.get("sx", 0) * scale)
            scroll_y = round(css_dims.get("sy", 0) * scale)
        viewport = {
            "x": scroll_x,
            "y": scroll_y,
            "w": round(css_w * scale),
            "h": round(css_h * scale),
        }
        viewport_node_indices = _compute_viewport_node_indices(dom_snapshot, viewport)

    return a11y_snapshot, dom_snapshot, viewport_node_indices


def _compute_viewport_node_indices(dom_snapshot: dict, viewport: dict, buffer_px: int = 200) -> list:
    """DOM node indices whose layout bounds intersect the viewport (V2 port).

    Returns visible node indices plus all their ancestors (so the tree stays
    well-formed) plus direct text-node children of visible nodes (text nodes
    have no layout rect but carry the content the endpoint needs).
    """
    documents = dom_snapshot.get("documents", [])
    if not documents:
        return []

    doc = documents[0]
    layout = doc.get("layout", {})
    layout_node_idx = layout.get("nodeIndex", [])
    layout_bounds = layout.get("bounds", [])
    parent_idx = doc.get("nodes", {}).get("parentIndex", [])

    vx = viewport["x"] - buffer_px
    vy = viewport["y"] - buffer_px
    vw = viewport["w"] + 2 * buffer_px
    vh = viewport["h"] + 2 * buffer_px

    visible = set()
    for i, node_idx in enumerate(layout_node_idx):
        if i >= len(layout_bounds):
            break
        bx, by, bw, bh = layout_bounds[i]
        if bx + bw > vx and bx < vx + vw and by + bh > vy and by < vy + vh:
            visible.add(node_idx)

    ancestors = set()
    for idx in visible:
        current = idx
        while 0 <= current < len(parent_idx) and current not in ancestors:
            ancestors.add(current)
            current = parent_idx[current]

    all_visible = visible | ancestors
    layout_node_set = set(layout_node_idx)
    children_of_visible = set()
    for ci in range(len(parent_idx)):
        if parent_idx[ci] in visible and ci not in layout_node_set:
            children_of_visible.add(ci)

    return sorted(all_visible | children_of_visible)
