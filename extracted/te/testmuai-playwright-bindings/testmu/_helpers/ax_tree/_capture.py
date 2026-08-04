"""Frame-aware AX capture entry point (Task A2, AH2 Phase A).

Ties the ported capture (``_frame_capture.capture_frame_forest`` — main tree
+ every eligible iframe as ``AxNode`` trees) to the A1 serializer
(``_serializer.serialize_ax_tree`` — one continuous ``e<N>`` ref space with
iframe content inlined and iframe-resident refs carrying their ``frame_id``).

Produces the same ``(doc, ref_table)`` the runner's v2 grounding produces;
Task A3 repoints the runner to import this shared pipeline and enforces
byte-identical parity.
"""

from __future__ import annotations

from ._frame_capture import capture_frame_forest
from ._serializer import serialize_ax_tree


async def capture_ax_tree(page) -> tuple[str, dict[str, dict]] | None:
    """Capture a page's frame-aware AX document + per-step ref table.

    Returns ``(doc, ref_table)`` — ``doc`` is the greppable serialized tree
    (iframe content inlined under its owning ``iframe`` line), ``ref_table``
    maps each ``e<N>`` ref to ``{backend_dom_node_id, role, name, frame_id}``
    (``frame_id == ""`` for main-frame refs, the content frame id for
    iframe-resident refs). Returns ``None`` when the main tree could not be
    captured at all.
    """
    forest = await capture_frame_forest(page)          # main_tree + frame_captures (AxNode)
    if forest is None or forest.main_tree is None:
        return None
    return serialize_ax_tree(forest.main_tree, forest.frame_captures)
