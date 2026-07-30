"""Accessibility + DOM snapshot capture for selector-less textual queries.

Chrome and Android keep the native CDP capture path. Browsers without CDP use
the snapshot runtime provisioned on the test worker. The captured tuple is sent
to the textual-query endpoint, which reads the value server-side.
"""
import json
import sys
from collections.abc import Mapping
from functools import lru_cache

from selenium.common.exceptions import JavascriptException, WebDriverException


_LINUX_RUNTIME_ASSET_PATH = "/home/ltuser/foreman/ltuser/aria_snapshot.js"
_MACOS_RUNTIME_ASSET_PATH = "/Users/ltuser/foreman/ltuser/aria_snapshot.js"
_WINDOWS_RUNTIME_ASSET_PATH = "D:/foreman/ltuser/aria_snapshot.js"
_RUNTIME_EXPORTED_GLOBALS = (
    "__ariaSnapshot",
    "__ariaSnapshotDetails",
    "__ariaSnapshotJSON",
    "__ariaSnapshotCDP",
    "__ariaSnapshotRaw",
    "__domSnapshot",
    "__domSnapshotCDP",
    "__resolveDomSnapshotNode",
    "__domSnapshotRaw",
    "__domSnapshotRefs",
    "__aria_snap_dom_streamer__",
)
_RUNTIME_CAPTURE_CALL = (
    "\nreturn {a11y_snapshot: globalThis.__ariaSnapshotCDP(), "
    "dom_snapshot: globalThis.__domSnapshotCDP()};"
)
_RUNTIME_CLEANUP = (
    "\n} finally {\n"
    f"  for (const name of {json.dumps(_RUNTIME_EXPORTED_GLOBALS)}) {{\n"
    "    try {\n"
    "      delete globalThis[name];\n"
    "    } catch (_ignoredCleanupError) {}\n"
    "  }\n"
    "}"
)
_MISSING_RUNTIME_ERROR = "Required runtime asset was not provisioned."
_INVALID_RUNTIME_ERROR = "Required runtime asset returned an invalid snapshot."
_CDP_BROWSERS = {"chrome", "chromium", "edge", "microsoftedge"}


def _read_runtime_source(path: str) -> str:
    """Read the worker-provisioned runtime. Kept separate as an internal test seam."""
    with open(path, encoding="utf-8") as runtime_file:
        return runtime_file.read()


def _runtime_asset_path(platform_name=None) -> str:
    """Return the fixed Foreman asset path for the worker host OS."""
    platform_name = sys.platform if platform_name is None else platform_name
    normalized = str(platform_name).lower()
    if normalized == "darwin":
        return _MACOS_RUNTIME_ASSET_PATH
    if normalized.startswith("win"):
        return _WINDOWS_RUNTIME_ASSET_PATH
    return _LINUX_RUNTIME_ASSET_PATH


@lru_cache(maxsize=1)
def _load_runtime_source() -> str:
    """Load the worker-provisioned runtime once, on first non-CDP capture."""
    try:
        source = _read_runtime_source(_runtime_asset_path())
    except (OSError, UnicodeError):
        raise RuntimeError(_MISSING_RUNTIME_ERROR) from None
    if not isinstance(source, str) or not source.strip():
        raise RuntimeError(_MISSING_RUNTIME_ERROR) from None
    return source


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
    value = response.get("value")
    if isinstance(value, Mapping) and ("error" in value or "message" in value):
        error = str(value.get("error", "") or "").strip()
        message = str(value.get("message", "") or "").strip()
        detail = ": ".join(part for part in (error, message) if part)
        raise WebDriverException(detail or "CDP command failed")
    return value


def _capture_cdp_snapshot(driver):
    """Capture the two endpoint snapshots through the existing CDP route."""
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

    return a11y_snapshot, dom_snapshot


def _invalid_runtime_snapshot():
    raise RuntimeError(_INVALID_RUNTIME_ERROR) from None


def _capture_runtime_snapshot(driver):
    """Inject and invoke the provisioned runtime in the current document realm."""
    source = _load_runtime_source()
    script = "try {\n" + source + _RUNTIME_CAPTURE_CALL + _RUNTIME_CLEANUP
    try:
        result = driver.execute_script(script)
    except JavascriptException:
        _invalid_runtime_snapshot()

    if not isinstance(result, Mapping):
        _invalid_runtime_snapshot()

    a11y_snapshot = result.get("a11y_snapshot")
    dom_snapshot = result.get("dom_snapshot")
    if not isinstance(a11y_snapshot, dict) or not isinstance(a11y_snapshot.get("nodes"), list):
        _invalid_runtime_snapshot()
    if not isinstance(dom_snapshot, dict):
        _invalid_runtime_snapshot()

    documents = dom_snapshot.get("documents")
    strings = dom_snapshot.get("strings")
    if not isinstance(documents, list) or not documents or not isinstance(strings, list):
        _invalid_runtime_snapshot()

    main_doc = documents[0]
    if not isinstance(main_doc, dict):
        _invalid_runtime_snapshot()
    nodes = main_doc.get("nodes")
    layout = main_doc.get("layout")
    if not isinstance(nodes, dict) or not isinstance(layout, dict):
        _invalid_runtime_snapshot()
    if any(not isinstance(nodes.get(key), list) for key in (
        "nodeName", "nodeType", "nodeValue", "attributes", "parentIndex",
    )):
        _invalid_runtime_snapshot()
    if any(not isinstance(layout.get(key), list) for key in ("nodeIndex", "styles", "bounds")):
        _invalid_runtime_snapshot()

    return a11y_snapshot, dom_snapshot


def _is_explicitly_unsupported_cdp(error: WebDriverException) -> bool:
    """Recognize only remote-end responses that explicitly reject CDP."""
    message = str(error).lower()
    return any(marker in message for marker in (
        "unknown command",
        "unsupported operation",
        "method not found",
        "cdp command is not supported",
        "cdp commands are not supported",
    ))


def capture_a11y_dom_snapshot(driver):
    """Capture ``(a11y, DOM, viewport indices)`` for textual-query reads.

    iOS, Safari, and Firefox use the provisioned non-CDP runtime. Other engines
    retain the native CDP route; an unknown engine falls back only when its
    remote end explicitly reports that CDP is unsupported. When the DOM has
    more than 3000 nodes, the original viewport-index math is preserved.
    """
    capabilities = driver.capabilities or {}
    platform = str(capabilities.get("platformName", "") or "").lower()
    browser = str(capabilities.get("browserName", "") or "").lower()
    use_runtime = platform == "ios" or browser in {"safari", "firefox"}
    unknown_engine = platform != "android" and browser not in _CDP_BROWSERS

    if use_runtime:
        a11y_snapshot, dom_snapshot = _capture_runtime_snapshot(driver)
    else:
        try:
            a11y_snapshot, dom_snapshot = _capture_cdp_snapshot(driver)
        except WebDriverException as error:
            if not unknown_engine or not _is_explicitly_unsupported_cdp(error):
                raise
            a11y_snapshot, dom_snapshot = _capture_runtime_snapshot(driver)

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
