"""Shared constants and utilities for the binding's AX-tree capture.

Ported verbatim (the four symbols the frame-aware capture needs) from the
reference accessibility-capture implementation this module originates
from — ``FRAME_ROLE``, ``INTERACTIVE_ROLES``, ``is_visible``,
``is_in_viewport`` — so the capture port (``_accessibility.py`` /
``_frame_capture.py``) and the serializer (``_serializer.py``) share a
single home for each, exactly as the original does (no duplication/drift).
This is the shared source of truth on the binding side, verified
byte-identical in behavior against the original.
"""

from __future__ import annotations

# The AX role Chrome assigns an <iframe>/<frame> element (always compared
# lowercased, like every other role comparison in the frame-capture/
# serializer modules). Single shared home for both walkers (frame_capture.py
# discovery-side, ax_serializer.py merge-side) — previously duplicated as
# a private `_FRAME_ROLE` constant in each.
FRAME_ROLE = "iframe"

INTERACTIVE_ROLES: frozenset[str] = frozenset({
    "button",
    "link",
    "textbox",
    "combobox",
    "listbox",
    "checkbox",
    "radio",
    "slider",
    "spinbutton",
    "searchbox",
    "switch",
    "tab",
    "menuitem",
    "menuitemcheckbox",
    "menuitemradio",
    "option",
    "treeitem",
})


def is_visible(bounding_box: dict[str, float] | None) -> bool | None:
    """Check if an element is visible (has positive dimensions).

    Args:
        bounding_box: Element's bounding box with x, y, width, height.

    Returns:
        True if element has positive width and height (is rendered),
        False if dimensions are zero (hidden), None if bounding_box unavailable.
    """
    if bounding_box is None:
        return None

    width = bounding_box.get("width", 0)
    height = bounding_box.get("height", 0)

    return width > 0 and height > 0


def is_in_viewport(
    bounding_box: dict[str, float] | None,
    viewport_width: float,
    viewport_height: float,
) -> bool | None:
    """Check if an element's bounding box is within the viewport.

    Args:
        bounding_box: Element's bounding box with x, y, width, height.
        viewport_width: Viewport width in pixels.
        viewport_height: Viewport height in pixels.

    Returns:
        True if element is at least partially visible in viewport,
        False if completely outside, None if bounding_box is unavailable.
    """
    if bounding_box is None:
        return None

    x = bounding_box.get("x", 0)
    y = bounding_box.get("y", 0)
    width = bounding_box.get("width", 0)
    height = bounding_box.get("height", 0)

    if x + width < 0 or x > viewport_width:
        return False
    if y + height < 0 or y > viewport_height:
        return False

    return True
