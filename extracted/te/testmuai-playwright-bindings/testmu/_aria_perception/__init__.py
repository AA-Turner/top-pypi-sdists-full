"""Portable (non-CDP) perception for Firefox: Playwright's AI snapshot
plus ``aria-ref`` locators, emitted as the same ``AxNode`` / ``FrameForest``
structures the Chrome CDP path produces.

Element identity is a synthetic integer handle carried in
``backend_dom_node_id`` (see ``_refs``). Stateless: every call takes the
``page``, so concurrent sessions are safe.
"""
from ._actions import (
    clickability_facts,
    element_snapshot,
    enrich_point_locator,
    enrich_ref_locator,
    ground_ref,
    option_click_redirect,
    scroll_offsets,
    scroll_ref_into_view,
    tag_ref,
    viewport_status,
)
from ._capture import (
    capture_ax_document_portable,
    capture_frame_forest_portable,
    capture_tree_portable,
)
from ._engine import (
    Engine,
    engine_of,
    get_browser_engine,
    local_engine,
    page_engine,
    requested_engine,
    session_engine,
    set_browser_engine,
    supports_cdp,
)
from ._enrich import enrich_inputs
from ._parse import ParsedSnapshot, parse_ai_snapshot
from ._refs import (
    OPTION_TAG,
    PORTABLE_TAG,
    anchor_locator,
    aria_ref_to_handle,
    call_on_ref,
    frame_id_for_ref,
    handle_to_aria_ref,
    is_option_handle,
    is_portable_handle,
    option_handle,
    option_parts,
    ref_locator,
)
from ._screenshot import nudge_fonts, screenshot_png_b64
from ._snapshot import snapshot_for_ai
from ._types import ModeTypes

__all__ = [
    "Engine",
    "ModeTypes",
    "engine_of",
    "page_engine",
    "requested_engine",
    "local_engine",
    "session_engine",
    "supports_cdp",
    "set_browser_engine",
    "get_browser_engine",
    "snapshot_for_ai",
    "PORTABLE_TAG",
    "OPTION_TAG",
    "option_handle",
    "option_parts",
    "is_option_handle",
    "anchor_locator",
    "aria_ref_to_handle",
    "handle_to_aria_ref",
    "is_portable_handle",
    "frame_id_for_ref",
    "ref_locator",
    "call_on_ref",
    "ParsedSnapshot",
    "parse_ai_snapshot",
    "capture_frame_forest_portable",
    "capture_ax_document_portable",
    "capture_tree_portable",
    "enrich_inputs",
    "ground_ref",
    "viewport_status",
    "scroll_ref_into_view",
    "scroll_offsets",
    "tag_ref",
    "element_snapshot",
    "clickability_facts",
    "enrich_ref_locator",
    "enrich_point_locator",
    "option_click_redirect",
    "screenshot_png_b64",
    "nudge_fonts",
]
