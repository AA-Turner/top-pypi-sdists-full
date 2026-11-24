"""Portable capture: AI snapshot -> FrameForest / AX document / single tree."""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING
from urllib.parse import urljoin

from ._enrich import enrich_editables, enrich_inputs
from ._parse import ParsedSnapshot, parse_ai_snapshot, reattach_frames
from ._refs import ref_locator
from ._snapshot import PlaywrightInternalsError, snapshot_for_ai

if TYPE_CHECKING:
    from ._types import ModeTypes

_log = logging.getLogger("testmu")


def _absolutize_urls(node, base: str) -> None:
    """Chrome reports link URLs resolved; the snapshot carries the raw href."""
    if node.url and base:
        try:
            node.url = urljoin(base, node.url)
        except ValueError:
            pass
    for child in node.children:
        _absolutize_urls(child, base)


def _first_ref(node) -> str | None:
    for child in node.children:
        if child.aria_ref:
            return child.aria_ref
        found = _first_ref(child)
        if found:
            return found
    return None


async def _frame_base(page, tree) -> str:
    """A captured frame's own base URL (its links resolve against it, not
    the page's); "" when unknown."""
    ref = _first_ref(tree)
    if not ref:
        return ""
    try:
        return str(await ref_locator(page, ref).evaluate("e => e.baseURI", timeout=1000) or "")
    except Exception:  # noqa: BLE001
        return ""


async def _capture_parsed(page, types: "ModeTypes") -> ParsedSnapshot:
    text = await snapshot_for_ai(page)
    parsed = parse_ai_snapshot(text, types)
    forest = parsed.forest
    if forest.main_tree is None:
        return parsed
    await enrich_inputs(page, parsed)
    await enrich_editables(page, parsed)
    try:
        base = page.url or ""
    except Exception:  # noqa: BLE001
        base = ""
    if base and not base.startswith("about:"):
        _absolutize_urls(forest.main_tree, base)
    # Frame content resolves against its own document; unknown -> left raw.
    frames = []
    stack = list(forest.frame_captures)
    while stack:
        fc = stack.pop()
        if fc.tree is not None:
            frames.append(fc.tree)
        stack.extend(fc.children)
    if types.annotate_pointer is not None:
        for tree in (forest.main_tree, *frames):
            types.annotate_pointer(tree)
    if frames:
        bases = await asyncio.gather(*(_frame_base(page, t) for t in frames))
        for tree, frame_base in zip(frames, bases):
            if frame_base and not frame_base.startswith("about:"):
                _absolutize_urls(tree, frame_base)
    return parsed


async def capture_frame_forest_portable(page, types: "ModeTypes", *, viewport_width: float = 1280,
                                        viewport_height: float = 800):
    """snapshot_for_ai -> parse_ai_snapshot -> enrich_inputs -> forest.

    Never raises (except ``PlaywrightInternalsError``): on error returns
    ``FrameForest(main_tree=None)`` whose ``error`` attribute names the
    failure (None on success; an empty page is not an error). The returned forest also carries ``nodes_by_handle``
    (handle -> AxNode of the same capture) as an instance attribute, for
    callers that ground refs.
    """
    try:
        parsed = await _capture_parsed(page, types)
    except PlaywrightInternalsError:
        raise
    except Exception as e:  # noqa: BLE001 — capture never raises
        _log.warning("aria_perception: portable capture failed: %s", e)
        forest = types.FrameForest(main_tree=None)
        forest.nodes_by_handle = {}
        forest.error = f"portable AX capture failed: {e or type(e).__name__}"
        return forest
    forest = parsed.forest
    forest.nodes_by_handle = parsed.nodes_by_handle
    forest.error = None
    return forest


async def capture_ax_document_portable(page, types: "ModeTypes") -> tuple[str, dict[str, dict]]:
    """``serialize_ax_tree(forest.main_tree, forest.frame_captures)``; ref_table
    entries are the serializer's ``{backend_dom_node_id: <handle>, role, name,
    frame_id}``. ``("", {})`` when the page is empty.

    Raises:
        RuntimeError: when the capture failed (like the CDP capture, whose
            exception the caller reports as the document's ``error``).
    """
    forest = await capture_frame_forest_portable(page, types)
    if getattr(forest, "error", None):
        raise RuntimeError(forest.error)
    if forest.main_tree is None:
        return "", {}
    return types.serialize_ax_tree(forest.main_tree, forest.frame_captures)


async def capture_tree_portable(page, types: "ModeTypes"):
    """Main tree with iframe content re-attached as children of the iframe
    node (for flat/structured builders). None when nothing was captured."""
    forest = await capture_frame_forest_portable(page, types)
    if forest.main_tree is None:
        return None
    return reattach_frames(forest.main_tree, forest.frame_captures)
