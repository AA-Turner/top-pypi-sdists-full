"""Portable (non-CDP) perception bound to this mode's types.

The mechanics live once in the shared ``testmu._aria_perception``; this module
re-exports them with the mode's ``AxNode`` / ``FrameForest`` types filled in,
so callers keep the one-argument signatures (``capture_tree_portable(page)``).
Code that only needs a page's backend should use ``_v4._helpers._perception``.
"""
from __future__ import annotations

import functools

from testmu import _aria_perception as _shared
from testmu._aria_perception import *  # noqa: F401,F403 — the shared API, unchanged
from testmu._aria_perception import ModeTypes  # noqa: F401
from testmu._aria_perception._parse import reattach_frames  # noqa: F401


@functools.cache
def mode_types() -> ModeTypes:
    # Imported on first use: these modules import this one lazily too.
    from testmu._v4._helpers._dom_structured import AxNode
    from testmu._v4._helpers.ax_tree._actionable import annotate_pointer_tree
    from testmu._v4._helpers.ax_tree._constants import INTERACTIVE_ROLES
    from testmu._v4._helpers.ax_tree._frame_capture import FrameCapture, FrameForest
    from testmu._v4._helpers.ax_tree._serializer import serialize_ax_tree

    return ModeTypes(
        AxNode=AxNode,
        FrameCapture=FrameCapture,
        FrameForest=FrameForest,
        serialize_ax_tree=serialize_ax_tree,
        interactive_roles=frozenset(INTERACTIVE_ROLES),
        annotate_pointer=annotate_pointer_tree,
    )


def parse_ai_snapshot(text: str):
    return _shared.parse_ai_snapshot(text, mode_types())


async def capture_frame_forest_portable(page, *, viewport_width: float = 1280,
                                        viewport_height: float = 800):
    return await _shared.capture_frame_forest_portable(
        page, mode_types(), viewport_width=viewport_width, viewport_height=viewport_height,
    )


async def capture_ax_document_portable(page):
    return await _shared.capture_ax_document_portable(page, mode_types())


async def capture_tree_portable(page):
    return await _shared.capture_tree_portable(page, mode_types())


async def enrich_point_locator(page, element: dict) -> dict:
    return await _shared.enrich_point_locator(page, element, mode_types())
