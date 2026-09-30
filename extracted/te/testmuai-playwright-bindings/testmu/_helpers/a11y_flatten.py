"""Flat a11y-tree capture for /v2/locate/desktop grounding (Playwright).

Port of the selenium-python `_helpers/a11y_flatten`, itself a port of
V2 `get_flat_a11y_tree` + the non-CDP branch from V2.
V3 sent `"a11y_flatten": []` on every desktop-locate call, so locate grounded on
the screenshot alone while V2 grounded on screenshot + a11y tree.

The tree logic below is transport-agnostic — it consumes CDP-shaped dicts — so
only the two capture primitives differ from the Selenium port:

  * CDP: a Playwright CDPSession (`context.new_cdp_session`) instead of
    Selenium's `execute_cdp_command`. Chromium only; Playwright raises on
    WebKit/Firefox, which is the whole reason for the route check.
  * non-CDP: the same worker-provisioned aria-snap runtime the vision helper
    already loads, evaluated via `page.evaluate`.

Async because Playwright's API is. Returns a list of sparse dicts in DFS order
with a 1-based `index`, or [] on any unrecoverable error: a locate call must
never fail because of a11y.
"""
import json
import logging
import time

from testmu._helpers.vision import _load_runtime_snapshot_asset

_log = logging.getLogger(__name__)


async def _cdp_send(session, cmd: str, params=None):
    """Send one CDP command on an already-open session."""
    return await session.send(cmd, params or {})


async def _open_cdp(page):
    """Open one CDP session for a whole capture.

    Per-capture rather than cached: the locate path can run against a page that
    was navigated or replaced since the last heal, and a stale CDPSession raises
    "Target closed" instead of reconnecting. Per-capture rather than per-command
    because a capture issues getFrameTree + getFullAXTree-per-frame +
    captureSnapshot + Runtime.evaluate, and session setup on each would be pure
    latency on the heal hot path.
    """
    return await page.context.new_cdp_session(page)


def _supports_cdp(page) -> bool:
    """True when this session can speak CDP (Chromium family only).

    Mirrors the reasoning in _helpers/vision's capture route: the REQUESTED
    browser wins over the local engine identity, because cloud runs go through a
    relay that reports Chromium regardless of the real engine.
    """
    import os

    requested = (os.getenv("smart_browser_name") or "").strip().lower()
    if requested in ("pw-webkit", "pw-firefox", "webkit", "firefox", "safari"):
        return False
    if requested in ("chrome", "chromium", "googlechrome", "microsoftedge",
                     "edge", "msedge", "pw-chromium", "island"):
        return True
    try:
        engine = str(page.context.browser.browser_type.name or "").strip().lower()
    except Exception:  # noqa: BLE001
        engine = ""
    if engine in ("webkit", "firefox"):
        return False
    return True


async def _aria_exec(page, expr):
    """Define the aria-snap runtime (idempotently) and invoke `expr` in one evaluate.

    Single define+invoke because Firefox re-creates the evaluation scope per call,
    so globals from a previous evaluate are gone. Returns None when the runtime
    asset was not provisioned — the caller degrades to [].
    """
    try:
        bundle = _load_runtime_snapshot_asset()
    except Exception as exc:  # noqa: BLE001 — a missing asset must not fail locate
        _log.debug("aria-snap flatten: runtime unavailable (%s)", exc)
        return None
    if not bundle:
        return None
    script = (
        "() => { if (typeof globalThis.__ariaSnapshotCDP !== 'function') {\n"
        + bundle
        + "\n}\nreturn " + expr + "; }"
    )
    return await page.evaluate(script)


_A11Y_SKIP_ROLES = frozenset({"none", "generic", "rootwebarea", "webarea", "inlinetextbox"})
_A11Y_INPUT_LIKE_ROLES = frozenset({"textbox", "combobox", "searchbox", "textarea"})
_A11Y_EDITABLE_VALUES = frozenset({"richtext", "plaintext"})


def _a11y_build_element(node: dict, index: int, bbox, backend_id, frame_url, name_override: str = None,
                        role_override: str = None) -> dict:
    """Build a sparse output element dict from one AX node.

    `name_override`, when non-empty, is used as `name` only if the AX computed
    name is empty — used by the placeholder→name synthesis path so the contract
    "do not overwrite a non-empty computed name" holds.

    `role_override` replaces the AX role — used to surface a contenteditable root
    as "textbox" so it reads as a field rather than a structural container.
    """
    ax_name = _a11y_typed_value(node, "name") or ""
    if (not ax_name) and name_override:
        ax_name = name_override
    element = {
        "index": index,
        "role": role_override or _a11y_role_of(node),
        "name": ax_name,
    }
    value = _a11y_typed_value(node, "value")
    if value:
        element["value"] = value
    description = _a11y_typed_value(node, "description")
    if description:
        element["description"] = description

    properties = node.get("properties", []) or []
    props = {}
    for prop in properties:
        pname = prop.get("name")
        if pname:
            pval = prop.get("value", {})
            props[pname] = pval.get("value") if isinstance(pval, dict) else pval

    if props.get("disabled"): element["disabled"] = True
    if props.get("focused"): element["focused"] = True
    if props.get("required"): element["required"] = True
    if props.get("readonly"): element["readonly"] = True
    for tri in ("checked", "expanded", "selected", "pressed"):
        pv = props.get(tri)
        if pv is not None and pv is not False and pv != "false":
            element[tri] = pv

    if bbox:
        element["bounding_box"] = bbox
    if backend_id is not None:
        element["backend_dom_node_id"] = backend_id
    if frame_url:
        element["frame_url"] = frame_url
    return element


def _a11y_typed_value(node: dict, key: str) -> str:
    """Extract a CDP typed-value field (name/value/description) from an AX node."""
    info = node.get(key, {})
    return info.get("value", "") if isinstance(info, dict) else ""


def _a11y_is_editable(node: dict) -> bool:
    """True when this AX node sits inside a contenteditable region."""
    for prop in node.get("properties", []) or []:
        if prop.get("name") == "editable":
            val = prop.get("value", {})
            v = val.get("value") if isinstance(val, dict) else val
            return v in _A11Y_EDITABLE_VALUES
    return False


def _a11y_role_of(node: dict) -> str:
    """Lowercased role of an AX node, or '' when missing/malformed."""
    info = node.get("role", {})
    return info.get("value", "").strip().lower() if isinstance(info, dict) else ""


async def _a11y_capture_rects_snapshot(session) -> dict:
    """Single CDP call → {backendNodeId: {x, y, width, height, placeholder}}.

    Replaces O(N) sequential DOM.resolveNode + Runtime.callFunctionOn round-trips
    (which dominated wall-time over Selenium's HTTP CDP bridge — 50s+ on
    layout-heavy pages) with one DOMSnapshot.captureSnapshot. Covers all
    same-origin frames in the renderer process; backendNodeId is renderer-globally
    unique so a flat dict suffices.

    Snapshot bounds are document-relative (include the document's scroll). Stage
    4/5 callers expect viewport-relative coordinates — matching the
    getBoundingClientRect contract used elsewhere in this module — so per-doc
    scroll is subtracted here. Iframe owner rects (in the parent doc) and content
    rects (in the child doc) both appear in the returned dict; the cumulative
    offset summation in Stage 4 composes them correctly.

    Elements without a layout box (display:none, detached, etc.) are absent from
    the snapshot. Stage 7's viewport filter previously dropped these too (their
    zero rect failed the bounds check), so the visible output set is unchanged.
    """
    try:
        snap = await _cdp_send(session, "DOMSnapshot.captureSnapshot", {
            "computedStyles": [],
            "includeDOMRects": True,
        })
    except Exception:
        return {}
    # Some Selenium environments (Android `goog/cdp/execute`, occasionally Grid
    # bridges) return a JSON-encoded string instead of a dict. Match the
    # normalization pattern already used in the V2 source so we don't
    # silently drop valid responses.
    if isinstance(snap, str):
        try:
            snap = json.loads(snap)
        except Exception:
            return {}
    if not isinstance(snap, dict):
        return {}

    strings = snap.get("strings", []) or []
    rects = {}
    for doc in snap.get("documents", []) or []:
        nodes = doc.get("nodes", {}) or {}
        layout = doc.get("layout", {}) or {}
        backend_ids = nodes.get("backendNodeId", []) or []
        attrs = nodes.get("attributes", []) or []
        scroll_x = float(doc.get("scrollOffsetX", 0.0) or 0.0)
        scroll_y = float(doc.get("scrollOffsetY", 0.0) or 0.0)

        placeholder_by_node_idx = {}
        for n_idx, arr in enumerate(attrs):
            if not arr:
                continue
            for i in range(0, len(arr) - 1, 2):
                name_idx = arr[i]
                if 0 <= name_idx < len(strings) and strings[name_idx] == "placeholder":
                    val_idx = arr[i + 1]
                    if 0 <= val_idx < len(strings):
                        placeholder_by_node_idx[n_idx] = strings[val_idx] or ""
                    break

        node_indices = layout.get("nodeIndex", []) or []
        bounds_list = layout.get("bounds", []) or []
        for li, n_idx in enumerate(node_indices):
            if not (0 <= n_idx < len(backend_ids)):
                continue
            bid = backend_ids[n_idx]
            if not bid or bid <= 0:
                continue
            if li >= len(bounds_list):
                continue
            b = bounds_list[li]
            if not b or len(b) < 4:
                continue
            rects[bid] = {
                "x": float(b[0]) - scroll_x,
                "y": float(b[1]) - scroll_y,
                "width": float(b[2]),
                "height": float(b[3]),
                "placeholder": placeholder_by_node_idx.get(n_idx, ""),
            }
    return rects


async def _a11y_collect_frames(session):
    """BFS-walk Page.getFrameTree from the main session.

    Returns (frames, main_frame_id) where frames is a list of dicts with
    {frame_id, parent_frame_id, url, depth}. OOPIFs are NOT visible from the
    main session and therefore not enumerated — same-origin only.
    """
    try:
        result = await _cdp_send(session, "Page.getFrameTree", {})
    except Exception:
        return [], None

    frames = []
    main_frame_id = None

    def _walk(node, parent_id, depth):
        nonlocal main_frame_id
        frame = node.get("frame", {})
        fid = frame.get("id", "")
        if fid:
            if main_frame_id is None:
                main_frame_id = fid
            frames.append({
                "frame_id": fid,
                "parent_frame_id": parent_id,
                "url": frame.get("url", ""),
                "depth": depth,
            })
        for child in node.get("childFrames", []) or []:
            _walk(child, fid, depth + 1)

    _walk(result.get("frameTree", {}), None, 0)
    return frames, main_frame_id


def _a11y_flatten_frame(fi, nodes, frame_offset, bounding_boxes, viewport, is_main, elements, counter,
                        empty_input_counter=None, synth_counter=None):
    """DFS emit for one frame.

    raw_bbox is viewport-relative within fi (from getBoundingClientRect), so
    page-space conversion is `raw + frame_offset` — no scroll subtraction
    needed (parent's own scroll is already factored into the parent owner's
    rect, which contributed to frame_offset).

    `empty_input_counter` / `synth_counter` (each a single-element list used as
    a mutable int) track how many input-like nodes had an empty accessible
    name and how many of those got synthesized from the DOM placeholder. Both
    are optional; pass to get the breakdown logged by get_flat_a11y_tree.
    """
    nodes_by_id = {}
    local_root = None
    for node in nodes:
        nid = node.get("nodeId")
        if nid:
            nodes_by_id[nid] = node
        if not node.get("parentId") and local_root is None:
            local_root = node
    if local_root is None and nodes:
        local_root = nodes[0]
    if local_root is None:
        return

    frame_url = fi["url"] if not is_main else None

    def _dfs(node, in_editable=False):
        role = _a11y_role_of(node)
        child_ids = node.get("childIds", [])

        # `editable` is set on every node inside a contenteditable, so only the
        # outermost one is the field; nested ones stay structural.
        is_skipped_role = role in _A11Y_SKIP_ROLES or not role
        editable_root = not in_editable and _a11y_is_editable(node)
        descend_editable = in_editable or editable_root
        # Promote only structural roles: a real input/combobox keeps its own role.
        promote = editable_root and is_skipped_role

        if is_skipped_role and not promote:
            for cid in child_ids:
                child = nodes_by_id.get(cid)
                if child:
                    _dfs(child, descend_editable)
            return

        backend_id = node.get("backendDOMNodeId")
        raw_bbox = bounding_boxes.get((fi["frame_id"], backend_id)) if backend_id else None

        bbox = None
        if raw_bbox is not None:
            bbox = {
                "x": raw_bbox["x"] + frame_offset[0],
                "y": raw_bbox["y"] + frame_offset[1],
                "width": raw_bbox["width"],
                "height": raw_bbox["height"],
            }

        if viewport is not None:
            vp_x, vp_y, vp_w, vp_h = viewport
            if bbox is None:
                for cid in child_ids:
                    child = nodes_by_id.get(cid)
                    if child:
                        _dfs(child, descend_editable)
                return
            node_r = bbox["x"] + bbox["width"]
            node_b = bbox["y"] + bbox["height"]
            if node_r <= vp_x or bbox["x"] >= vp_x + vp_w or node_b <= vp_y or bbox["y"] >= vp_y + vp_h:
                for cid in child_ids:
                    child = nodes_by_id.get(cid)
                    if child:
                        _dfs(child, descend_editable)
                return

        # Placeholder → name synthesis for input-like roles with empty AX name.
        # raw_bbox carries the placeholder string fetched alongside the rect in
        # _a11y_capture_rects_snapshot, so this stays free of extra CDP traffic.
        name_override = None
        if (role in _A11Y_INPUT_LIKE_ROLES or promote) and not (_a11y_typed_value(node, "name") or ""):
            if empty_input_counter is not None:
                empty_input_counter[0] += 1
            placeholder = (raw_bbox.get("placeholder") if raw_bbox else "") or ""
            placeholder = placeholder.strip()
            if placeholder:
                name_override = placeholder
                if synth_counter is not None:
                    synth_counter[0] += 1

        counter[0] += 1
        elements.append(_a11y_build_element(node, counter[0], bbox, backend_id, frame_url,
                                            name_override=name_override,
                                            role_override="textbox" if promote else None))

        for cid in child_ids:
            child = nodes_by_id.get(cid)
            if child:
                _dfs(child, descend_editable)

    _dfs(local_root)


async def _get_flat_a11y_tree_via_js(page, viewport_only: bool = True, logger=None) -> list:
    """Non-CDP flat a11y-tree capture via the injected aria-snap bundle.

    Mirrors the get_flat_a11y_tree output contract (sparse dicts, DFS order,
    1-based index, same skip roles and state keys, frame_url on child-frame
    elements). Known deltas (listed in V2): `ref` replaces
    `backend_dom_node_id`, text leaves inherit the parent's bounding box, and
    placeholder synthesis is unnecessary (the bundle's AccName already falls
    back to it).
    """
    log = logger or logging.getLogger(__name__)
    t_total = time.monotonic()
    try:
        tree = await _aria_exec(page, "globalThis.__ariaSnapshotJSON({ boxes: true })")
        if isinstance(tree, str):
            tree = json.loads(tree)
        if not isinstance(tree, dict):
            log.warning("aria-snap flatten: unexpected snapshot payload (%s)", type(tree).__name__)
            return []

        viewport = None
        if viewport_only:
            try:
                size = await page.evaluate("() => [window.innerWidth, window.innerHeight]")
                # Bundle boxes are viewport-relative CSS px, so the filter rect is (0, 0, w, h).
                viewport = (0.0, 0.0, float(size[0]), float(size[1]))
            except Exception:
                viewport = None

        elements = []
        counter = [0]

        def _to_bbox(node, offset):
            box = node.get("box")
            if not isinstance(box, dict):
                return None
            return {
                "x": float(box.get("x", 0)) + offset[0],
                "y": float(box.get("y", 0)) + offset[1],
                "width": float(box.get("width", 0)),
                "height": float(box.get("height", 0)),
            }

        def _tri(value):
            # CDP tristate properties arrive as strings ('true'/'mixed'); mirror that.
            return "mixed" if value == "mixed" else "true"

        def _dfs(node, offset, parent_bbox, frame_url):
            role = (node.get("role") or "").strip().lower()
            if role == "text":
                role = "statictext"
            children = node.get("children") or []

            # Child document root of a stitched same-origin iframe: its boxes are
            # frame-relative, so shift the offset by the iframe's own box (kept in
            # parent_bbox by the iframe branch below).
            child_offset = offset
            if node.get("frame"):
                frame_url = node.get("frameUrl") or frame_url
                if parent_bbox is not None:
                    child_offset = (parent_bbox["x"], parent_bbox["y"])

            bbox = _to_bbox(node, child_offset if node.get("frame") else offset)
            if bbox is None and role == "statictext":
                bbox = parent_bbox

            skip = role in _A11Y_SKIP_ROLES or role in ("fragment",) or not role
            if not skip and viewport is not None:
                if bbox is None:
                    skip = True
                else:
                    vp_x, vp_y, vp_w, vp_h = viewport
                    if (bbox["x"] + bbox["width"] <= vp_x or bbox["x"] >= vp_x + vp_w or
                            bbox["y"] + bbox["height"] <= vp_y or bbox["y"] >= vp_y + vp_h):
                        skip = True

            if not skip:
                counter[0] += 1
                element = {
                    "index": counter[0],
                    "role": role,
                    "name": node.get("name") or "",
                }
                # Input value surfaces as the single text child (bundle contract).
                if role in _A11Y_INPUT_LIKE_ROLES and len(children) == 1 and \
                        isinstance(children[0], dict) and children[0].get("role") == "text":
                    element["value"] = children[0].get("name") or ""
                if node.get("description"):
                    element["description"] = node["description"]
                if node.get("disabled"):
                    element["disabled"] = True
                if node.get("active"):
                    element["focused"] = True
                if node.get("required"):
                    element["required"] = True
                if node.get("readonly"):
                    element["readonly"] = True
                for tri in ("checked", "expanded", "selected", "pressed"):
                    tri_value = node.get(tri)
                    if tri_value is not None and tri_value is not False and tri_value != "false":
                        element[tri] = _tri(tri_value)
                if bbox:
                    element["bounding_box"] = bbox
                if node.get("ref"):
                    element["ref"] = node["ref"]
                if frame_url:
                    element["frame_url"] = frame_url
                elements.append(element)

            for child in children:
                if isinstance(child, dict):
                    _dfs(child, child_offset, bbox if bbox is not None else parent_bbox, frame_url)

        _dfs(tree, (0.0, 0.0), None, None)
        log.info("aria-snap flatten: %d elements in %.0fms (viewport_only=%s)",
                 len(elements), (time.monotonic() - t_total) * 1000, viewport_only)
        return elements
    except Exception as e:
        log.warning("aria-snap flatten: capture failed (continuing without): %s", e)
        return []


async def get_flat_a11y_tree(page, viewport_only: bool = True, logger=None) -> list:
    """Canonical flat a11y-tree capture for /v2/locate/desktop grounding.

    Same algorithm as ChromeCDP.get_flat_a11y_tree but speaks CDP via
    await _cdp_send(session, ...) so it works both in test-run
    environments (where only the V2 runtime + selenium are present) and in
    authoring (where it's invoked via asyncio.to_thread from instruction.py's
    _capture_a11y_flatten shim).

    OOPIFs are unreachable over Selenium's CDP pass-through (would need
    Target.attachToTarget session routing) and are silently absent from the
    output. Same-origin frames are fully covered.

    Returns a list of sparse dicts in DFS order, 1-based `index`. Returns []
    on any unrecoverable error — the locate call must never fail because of
    a11y.
    """
    log = logger or logging.getLogger(__name__)
    if not _supports_cdp(page):
        # Non-CDP browser: previously returned [] here (Safari sent no a11y at
        # all to /v2/locate); the injected aria-snap bundle now covers it.
        return await _get_flat_a11y_tree_via_js(page, viewport_only=viewport_only, logger=log)
    session = await _open_cdp(page)
    t_total = time.monotonic()
    # Per-stage wall times (ms). The grand total in the summary log = sum(timings.values())
    # + Python overhead. If one stage dominates, optimize there.
    timings = {}
    try:
        # Stage 1: discover same-origin frames.
        t = time.monotonic()
        all_frames, main_frame_id = await _a11y_collect_frames(session)
        timings["s1_frames"] = (time.monotonic() - t) * 1000
        if not all_frames:
            log.warning("a11y_flatten: no frames discovered (Page.getFrameTree empty)")
            return []
        frames_by_id = {f["frame_id"]: f for f in all_frames}

        # Stage 2: AX trees per frame (sequential — typical pages have 1-3 frames).
        t = time.monotonic()
        frame_ax_nodes = {}
        ax_node_count = 0
        for fi in all_frames:
            try:
                params = {"frameId": fi["frame_id"]}
                res = await _cdp_send(session, "Accessibility.getFullAXTree", params)
                nodes = res.get("nodes", []) if isinstance(res, dict) else []
                frame_ax_nodes[fi["frame_id"]] = nodes
                ax_node_count += len(nodes)
            except Exception as e:
                log.debug(f"a11y_flatten: getFullAXTree failed for frame {fi['frame_id']}: {e}")
                frame_ax_nodes[fi["frame_id"]] = []
        timings["s2_axtrees"] = (time.monotonic() - t) * 1000

        # Stage 3: resolve owner backend node id for each non-root frame.
        t = time.monotonic()
        frame_owner = {}
        s3_fallback_calls = 0
        for fi in all_frames:
            if fi["parent_frame_id"] is None:
                continue
            parent_nodes = frame_ax_nodes.get(fi["parent_frame_id"], [])
            owner_bid = None
            for pnode in parent_nodes:
                if pnode.get("frameId") == fi["frame_id"]:
                    owner_bid = pnode.get("backendDOMNodeId")
                    break
            if owner_bid is None:
                s3_fallback_calls += 1
                try:
                    res = await _cdp_send(session, "DOM.getFrameOwner", {"frameId": fi["frame_id"]})
                    owner_bid = res.get("backendNodeId") if isinstance(res, dict) else None
                except Exception:
                    owner_bid = None
            if owner_bid is not None:
                frame_owner[fi["frame_id"]] = owner_bid
        timings["s3_owners"] = (time.monotonic() - t) * 1000

        # Stage 4 + 5 prep: one DOMSnapshot.captureSnapshot replaces O(N) per-node
        # CDP round-trips. Yields a flat {backend_id: rect} map covering all
        # same-origin docs (renderer-global IDs ⇒ no frame_id keying needed).
        t = time.monotonic()
        rects_by_bid = await _a11y_capture_rects_snapshot(session)
        timings["s45_snapshot"] = (time.monotonic() - t) * 1000

        # Stage 4: cumulative page-space offset per frame.
        t = time.monotonic()
        frame_offsets = {}
        if main_frame_id:
            frame_offsets[main_frame_id] = (0.0, 0.0)
        for fi in all_frames:
            if fi["parent_frame_id"] is None:
                continue
            parent_off = frame_offsets.get(fi["parent_frame_id"], (0.0, 0.0))
            owner_bid = frame_owner.get(fi["frame_id"])
            box = rects_by_bid.get(owner_bid) if owner_bid is not None else None
            if box is None:
                frame_offsets[fi["frame_id"]] = parent_off
            else:
                frame_offsets[fi["frame_id"]] = (parent_off[0] + box["x"], parent_off[1] + box["y"])
        timings["s4_offsets"] = (time.monotonic() - t) * 1000

        # Stage 5: re-key snapshot rects by (frame_id, backend_id) so Stage 7's
        # lookup is unchanged. Skip-role filter preserved — same nodes admitted.
        t = time.monotonic()
        bounding_boxes = {}
        candidates = 0
        for fi in all_frames:
            fid = fi["frame_id"]
            for node in frame_ax_nodes.get(fid, []):
                bid = node.get("backendDOMNodeId")
                # Editable nodes keep their rect even on a skipped role: the DFS
                # promotes the contenteditable root to a textbox and needs its box.
                if not bid or (_a11y_role_of(node) in _A11Y_SKIP_ROLES
                               and not _a11y_is_editable(node)):
                    continue
                candidates += 1
                box = rects_by_bid.get(bid)
                if box is not None:
                    bounding_boxes[(fid, bid)] = box
        timings["s5_rekey"] = (time.monotonic() - t) * 1000

        # Stage 6: top-frame viewport for the viewport_only filter. Bounding
        # boxes are viewport-relative (_a11y_capture_rects_snapshot subtracts
        # per-doc scroll), so the filter rect is anchored at (0, 0) — offsetting
        # it by scrollX/scrollY would trim visible elements above the scroll
        # position and admit off-screen ones below it.
        t = time.monotonic()
        viewport = None
        if viewport_only:
            try:
                r = await _cdp_send(session, "Runtime.evaluate", {
                    "expression": "JSON.stringify({w:innerWidth,h:innerHeight})",
                    "returnByValue": True,
                })
                d = json.loads(r.get("result", {}).get("value", "{}")) if isinstance(r, dict) else {}
                viewport = (0.0, 0.0, float(d.get("w", 0)), float(d.get("h", 0)))
            except Exception:
                viewport = None
        timings["s6_viewport"] = (time.monotonic() - t) * 1000

        # Stage 7: DFS flatten.
        t = time.monotonic()
        elements = []
        counter = [0]
        empty_input_counter = [0]
        synth_counter = [0]
        for fi in all_frames:
            nodes = frame_ax_nodes.get(fi["frame_id"], [])
            if not nodes:
                continue
            _a11y_flatten_frame(
                fi, nodes,
                frame_offsets.get(fi["frame_id"], (0.0, 0.0)),
                bounding_boxes, viewport,
                fi["frame_id"] == main_frame_id,
                elements, counter,
                empty_input_counter=empty_input_counter,
                synth_counter=synth_counter,
            )
        timings["s7_dfs"] = (time.monotonic() - t) * 1000

        total_ms = (time.monotonic() - t_total) * 1000
        log.info(
            "a11y_flatten: %d elements across %d frames in %.0fms "
            "(viewport_only=%s, empty_name_inputs=%d, placeholder_synthesized=%d) | "
            "ax_nodes=%d candidates=%d rects=%d s3_fallback=%d | "
            "s1_frames=%.0fms s2_axtrees=%.0fms s3_owners=%.0fms "
            "s45_snapshot=%.0fms s4_offsets=%.0fms s5_rekey=%.0fms "
            "s6_viewport=%.0fms s7_dfs=%.0fms",
            len(elements), len(all_frames), total_ms,
            viewport_only, empty_input_counter[0], synth_counter[0],
            ax_node_count, candidates, len(rects_by_bid), s3_fallback_calls,
            timings["s1_frames"], timings["s2_axtrees"], timings["s3_owners"],
            timings["s45_snapshot"], timings["s4_offsets"], timings["s5_rekey"],
            timings["s6_viewport"], timings["s7_dfs"],
        )
        return elements
    except Exception as e:
        log.warning(f"a11y_flatten: capture failed (continuing without): {e}")
        return []
    finally:
        try:
            await session.detach()
        except Exception:  # noqa: BLE001 — detach failure must not fail the capture
            pass


async def capture_a11y_flatten(page, viewport_only: bool = True, logger=None) -> list:
    """Convenience wrapper — equivalent to get_flat_a11y_tree.

    Name matches V2 so the two implementations stay greppable together.
    """
    return await get_flat_a11y_tree(page, viewport_only=viewport_only, logger=logger)
