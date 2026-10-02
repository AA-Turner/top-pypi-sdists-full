"""movement — did a gesture actually move anything on screen?

One perception pass fingerprints the rows currently inside a scrolled surface;
two consecutive equal fingerprints mean the gesture between them moved nothing.
That is the end-of-content signal for loops whose gesture cannot answer the
question itself: iOS has no scroll verb that reports "more to scroll" at all,
and Android's ``scrollGesture`` answer lies on some lists (a Jetpack Compose
``LazyColumn`` reports "cannot scroll" while plainly still scrolling), so
movement — not the gesture's own claim — is what ``scroll_until`` and the edge
scroll stop on.

Every reader here is fail-open: a read that cannot be taken is None, and None
never compares equal to anything (see ``gesture_moved``), so a flaky tree can
only fall back to the caller's bounded budget, never end a scroll early.
"""
from testmu_appium._errors import ScreenshotUnavailable
from testmu_appium._helpers._perception import capture_perception

#: Seconds to let a fling settle before reading the tree to decide whether the
#: gesture moved anything. Short enough not to dominate the per-gesture cost, long
#: enough that an end-of-list overscroll has sprung back and does not read as
#: movement.
MOVE_SETTLE_S = 0.35


def perceive(driver, *, screenshot):
    """One perception pass off the live driver — the SINGLE tree read per gesture.

    ``screenshot=True`` also captures pixels, so the same capture answers a vision
    condition: the loop hands this perception to ``check_until_condition`` instead
    of letting it read the tree a second time. ``screenshot=False`` is the selector
    loop, which reads movement off the rows alone.

    Returns None when the page source cannot be PARSED — a truncated mid-transition
    capture makes ``parse_tree`` raise ``ValueError`` — so a bad read is treated as
    inconclusive and the bounded search keeps going rather than aborting (the same
    resilience the old raw-source hash had). A lost screenshot on the vision path is
    a real failure, not an inconclusive one, and still raises.
    """
    try:
        return capture_perception(
            driver, include_screenshot=screenshot, require_screenshot=screenshot,
        )
    except ScreenshotUnavailable:
        raise
    except Exception:  # noqa: BLE001 — a malformed/truncated tree is inconclusive
        return None


def container_box(container):
    """The scrolled container's device-pixel box (x1, y1, x2, y2), or None."""
    if container is None:
        return None
    try:
        rect = container.rect
    except Exception:  # noqa: BLE001 — an unreadable container degrades to screen scope
        return None
    x, y = int(rect["x"]), int(rect["y"])
    return (x, y, x + int(rect["width"]), y + int(rect["height"]))


def _within(center, box) -> bool:
    cx, cy = center
    x1, y1, x2, y2 = box
    return x1 <= cx <= x2 and y1 <= cy <= y2


def _covers(bounds, box) -> bool:
    """Whether ``bounds`` contains the whole ``box``."""
    x1, y1, x2, y2 = bounds
    bx1, by1, bx2, by2 = box
    return x1 <= bx1 and y1 <= by1 and x2 >= bx2 and y2 >= by2


def box_signature(perception, box):
    """A fingerprint of the rows CURRENTLY inside ``box`` (x1, y1, x2, y2).

    Built from the retained DESCRIPTORS (which carry bounds, centre and identity),
    NOT the sanitized wire entries (index/role/name/states only, no geometry).
    Scoped to the box, so content outside it — the status bar's clock, a battery
    indicator, a neighbouring pane, an app-bar spinner — cannot read as movement.
    Two consecutive signatures that differ mean the last gesture moved the list;
    two that match mean it did not — the reliable end-of-list signal that
    ``scrollGesture``'s own ``canScrollMore`` lies about on some lists.

    A None box scopes to nothing, so every row counts. None (an unreadable tree,
    or no rows inside the box) never compares equal to a real signature, so a
    failed read reads as "moved" via ``gesture_moved`` and the search keeps going
    within its budget rather than stopping short.
    """
    if perception is None:
        return None
    rows = []
    for index in sorted(perception.descriptors):
        descriptor = perception.descriptors[index]
        bounds = descriptor.get("bounds")
        if not bounds or len(bounds) != 4:
            continue
        center = descriptor.get("center")
        if not (center and len(center) == 2):
            center = ((bounds[0] + bounds[2]) // 2, (bounds[1] + bounds[3]) // 2)
        if box is not None and not _within(center, box):
            continue
        if box is not None and _covers(bounds, box):
            # The scrolled surface itself (or a frame around it): its box is
            # fixed by definition, so it cannot evidence movement either way.
            continue
        rows.append((
            descriptor.get("resource_id") or "", descriptor.get("text") or "",
            descriptor.get("content_desc") or "", tuple(bounds),
        ))
    if not rows:
        return None
    return hash(tuple(rows))


def container_signature(perception, container):
    """``box_signature`` scoped to the container's own box.

    An unreadable container (or none at all) degrades to screen scope — every
    row counts — rather than becoming a new way for the read to fail.
    """
    return box_signature(perception, container_box(container))


def gesture_moved(before, after) -> bool:
    """Whether two signatures show the gesture changed the screen.

    Only two real, equal signatures count as "did not move"; a None on either
    side is inconclusive and treated as movement so the bounded loop, not a failed
    read, decides when to stop.
    """
    if before is None or after is None:
        return True
    return before != after
