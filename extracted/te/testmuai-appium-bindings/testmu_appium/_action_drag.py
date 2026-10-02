"""drag — a touch path between a source anchor and a target anchor.

Two shapes, chosen by whether selectors reach the call, exactly as `scroll`
decides between a container and the screen:

- **element** — selectors identify the control. It is found (and healed) through
  the ordinary element path, and the gesture is then measured against the screen
  in front of it: the start is the element's live centre for a destination drag,
  its direction-opposite edge for a displacement (see `_element_start`), and a
  displacement target travels a fraction of the room remaining in its direction.
  This is the same move `select`'s slider arm makes, and it is what lets a
  recording replay on a device of another size.
- **driver** — two recorded coordinate bases and no element. Both ends scale onto
  the live window, and both are refused when the recording orientation does not
  match.

An element-mode drag has NO coordinate runner, so a control that cannot be found
fails rather than falling back to the recorded ratios. That is deliberate: the
ratios describe the layout that has just failed to produce the element, and a
drag aimed at the wrong place moves something rather than merely missing it.
"""
import logging

from testmu_appium._action_engine import (
    _ActionSpec,
    _Deadline,
    _consult_heal,
    _coordinates_from_basis,
    _find_within_timeout,
    _live_orientation,
    _run_action,
    _settle,
    run_driver,
)
from testmu_appium import _config
from testmu_appium._errors import ElementNotFound
from testmu_appium._heal import HealHit, HealNoMatch, HealUnresolved
from testmu_appium._helpers.gesture import drag_gesture, element_center
from testmu_appium._helpers.vision_coordinates import get_vision_coordinates

_log = logging.getLogger("testmu_appium")

#: Unit vectors for the directions a displacement can travel.
_AXIS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

#: Kept clear of the screen edge, where a horizontal drag is a system back
#: gesture on Android 10+ rather than anything the app sees. Mirrors the
#: authoring-side inset in v16-runner's mobile gesture tool; the two compute the
#: same path and must agree.
_EDGE_INSET_PX = 24

DEFAULT_FRACTION = 1.0


def _displacement_end(driver, start, direction, fraction):
    """Where a displacement lands, measured on the live screen.

    Travel is a fraction of the room to the edge rather than a recorded number of
    pixels: a slide track's length is a property of the screen, so the same
    gesture needs a different distance on a device of another size.
    """
    dx, dy = _AXIS[direction]
    _, width, height = _live_orientation(driver)
    cx, cy = start
    if dx:
        limit = (width - _EDGE_INSET_PX - cx) if dx > 0 else (cx - _EDGE_INSET_PX)
    else:
        limit = (height - _EDGE_INSET_PX - cy) if dy > 0 else (cy - _EDGE_INSET_PX)
    travel = max(0, int(limit * max(0.0, min(1.0, float(fraction)))))
    return (cx + dx * travel, cy + dy * travel)


def _selector_target(driver, ctx):
    """Resolve the destination selector set within the source action's deadline."""
    deadline = ctx["_deadline"]
    selectors = ctx["target_selectors"]
    description = ctx.get("target_description", "")
    element, _, _, tried = _find_within_timeout(
        driver, selectors, _config.platform(), deadline
    )
    if element is not None:
        return element

    outcome = _consult_heal(driver, _DRAG_ELEMENT_SPEC, description, deadline)
    if isinstance(outcome, HealHit):
        return outcome.element
    if isinstance(outcome, HealNoMatch):
        reason = outcome.reason
    elif isinstance(outcome, HealUnresolved):
        reason = f"heal answer did not resolve locally: {outcome.reason}"
    else:
        reason = (
            getattr(outcome, "cause", None)
            or getattr(outcome, "detail", None)
            or "heal could not be consulted"
        )
    raise ElementNotFound(description, tried, reason)


def _target_end(driver, start, ctx):
    if ctx.get("target_selectors"):
        return element_center(_selector_target(driver, ctx))
    if ctx.get("target_description"):
        return get_vision_coordinates(driver, ctx["target_description"], "click")
    return _displacement_end(driver, start, ctx["direction"], ctx["fraction"])


def _element_start(element, direction):
    """Where the finger lands on the found element.

    A drag with a DESTINATION moves the element somewhere; its centre is the
    one point guaranteed to be inside it, so that stays. A drag with a
    DIRECTION is slide-to-act, and every slide control rests its thumb at the
    origin of the travel — so the finger starts at the element's
    direction-opposite edge, half the cross-axis in (a thumb is a circle about
    as wide as its track is tall). The centre is empty rail there: measured
    across five runs (sessions 20260805-*), every centre-started slide moved
    nothing, and every thumb-started one confirmed. The edge start works
    whether the recording named the track, the thumb, or an arrow on it.
    """
    if direction not in _AXIS:
        return element_center(element)
    rect = element.rect
    x, y = int(rect["x"]), int(rect["y"])
    w, h = int(rect["width"]), int(rect["height"])
    dx, dy = _AXIS[direction]
    if dx:
        inset = min(w, h) // 2
        sx = x + inset if dx > 0 else x + w - inset
        # The same guard the end point gets: a start ON the screen edge is a
        # system gesture (Android back), not a touch the app sees.
        return (max(sx, _EDGE_INSET_PX), y + h // 2)
    inset = min(w, h) // 2
    sy = y + inset if dy > 0 else y + h - inset
    return (x + w // 2, max(sy, _EDGE_INSET_PX))


def _element_runner(element, ctx):
    """Drag the found element, recomputing the whole path from its live bounds.

    The destination is its own anchor and resolves on its own terms: named in
    words it goes to vision, and named as a displacement it is measured from the
    element. How the SOURCE was found says nothing about either.
    """
    driver = ctx["driver"]
    start = _element_start(element, ctx.get("direction"))
    end = _target_end(driver, start, ctx)
    drag_gesture(
        driver, start, end,
        hold_duration_ms=ctx.get("hold_duration_ms"),
        move_duration_ms=ctx.get("move_duration_ms"),
        hold_at_destination_ms=ctx.get("hold_at_destination_ms"),
    )
    _log.info("    [drag] %s → %s", start, end)
    return True


def _driver_runner(driver, ctx):
    start = _coordinates_from_basis(driver, ctx["source_coordinates"])
    end = _coordinates_from_basis(driver, ctx["target_coordinates"])
    drag_gesture(
        driver, start, end,
        hold_duration_ms=ctx.get("hold_duration_ms"),
        move_duration_ms=ctx.get("move_duration_ms"),
        hold_at_destination_ms=ctx.get("hold_at_destination_ms"),
    )
    _log.info("    [drag] %s → %s", start, end)
    return True


def _vision_runner(driver, ctx):
    """Resolve the recorded words to a point, then drag from it.

    Driver mode because there is no element to find: the tree never described
    this control, which is why authoring reached for vision in the first place.

    A named destination is resolved the same way and used as the end point. A
    displacement can only travel TOWARDS a destination — the distance is a guess
    about a place the recording never located — so where the words for one exist,
    they decide the end point rather than a fraction of the screen.
    """
    start = get_vision_coordinates(driver, ctx["source_description"], "click")
    end = _target_end(driver, start, ctx)
    drag_gesture(
        driver, start, end,
        hold_duration_ms=ctx.get("hold_duration_ms"),
        move_duration_ms=ctx.get("move_duration_ms"),
        hold_at_destination_ms=ctx.get("hold_at_destination_ms"),
    )
    _log.info("    [drag/vision] %s → %s", start, end)
    return True


_DRAG_SPEC = _ActionSpec(runner=_driver_runner, target_mode="driver", op_type="")

_DRAG_VISION_SPEC = _ActionSpec(
    runner=_vision_runner, target_mode="driver", op_type=""
)

#: coord_runner stays None: an element-mode drag never replays recorded ratios.
_DRAG_ELEMENT_SPEC = _ActionSpec(
    runner=_element_runner, target_mode="element", op_type="click",
    allow_inert_heal=True,
)


def drag(driver, *, selectors=None, source_coordinates: dict | None = None,
         target_coordinates: dict | None = None, direction: str | None = None,
         fraction: float = DEFAULT_FRACTION, source_description: str = "",
         target_description: str = "", grounded_by: str = "",
         target_selectors=None, target_grounded_by: str = "",
         hold_duration_ms: int | None = None,
         move_duration_ms: int | None = None,
         hold_at_destination_ms: int | None = None, description: str = ""):
    """Drag a control, or drag between two recorded points.

    grounded_by: how the AUTHORING run located this control — "tree" or
        "vision". It, not the presence of selectors, chooses how replay locates
        it: a recording grounded by vision is re-grounded by vision, so replay
        reproduces what authoring did. Selectors on such a recording are ignored
        rather than promoted, because a stale one would replay an element action
        that never happened. Empty means the recording predates the marker and
        falls back to reading selector presence.
    selectors: ranked entries identifying the control to drag.
    direction / fraction: a displacement target — which way to travel, and how
        far as a share of the room available in that direction.
    source_description: what the control is, in words. The handle the vision
        path resolves, and the heal intent for the tree path.
    target_description: where it is going, in words. Resolved the same way as
        the source and used as the end point, in place of a displacement —
        mutually exclusive with direction/fraction, which can only travel
        towards a destination rather than arrive at one.
    source_coordinates / target_coordinates: recorded coordinate bases
        ({"x_ratio", "y_ratio", "orientation", "window"}). The only target when
        the recording carried no identity at all; provenance otherwise.
    """
    if grounded_by not in ("", "tree", "vision"):
        raise ValueError(
            f"unknown grounded_by {grounded_by!r}; expected '', 'tree', or 'vision'"
        )
    if target_grounded_by not in ("", "tree", "vision"):
        raise ValueError(
            "unknown target_grounded_by "
            f"{target_grounded_by!r}; expected '', 'tree', or 'vision'"
        )
    if target_grounded_by == "tree" and not target_selectors:
        raise ValueError("target_grounded_by='tree' needs target_selectors")
    if target_grounded_by == "vision":
        if target_selectors:
            raise ValueError(
                "target_grounded_by='vision' cannot carry target_selectors"
            )
        if not target_description:
            raise ValueError(
                "target_grounded_by='vision' needs target_description"
            )
    if target_selectors and direction is not None:
        raise ValueError(
            "a drag takes target_selectors or a direction, not both"
        )

    if grounded_by == "vision":
        if not source_description:
            raise ValueError(
                "a vision-grounded drag needs source_description: the words are "
                "the only handle it has"
            )
        if target_selectors:
            if not target_description:
                raise ValueError(
                    "a selector-grounded drag destination needs target_description "
                    "for semantic healing"
                )
        elif target_description:
            if direction is not None:
                raise ValueError(
                    "a vision drag takes a target_description or a direction, "
                    "not both: they are two different end points and nothing "
                    "says which the recording meant"
                )
        elif direction not in _AXIS:
            raise ValueError(
                f"a vision drag with no target_description needs a direction, "
                f"one of {sorted(_AXIS)}; got {direction!r}"
            )
        params = dict(
            source_description=source_description,
            target_description=target_description,
            target_selectors=target_selectors,
            target_grounded_by=target_grounded_by,
            direction=direction,
            fraction=fraction,
            hold_duration_ms=hold_duration_ms,
            move_duration_ms=move_duration_ms,
            hold_at_destination_ms=hold_at_destination_ms,
        )
        if target_selectors:
            deadline = _Deadline()
            params["_page_source"] = _settle(driver, deadline)
            params["_deadline"] = deadline
        return run_driver(
            driver, _DRAG_VISION_SPEC,
            **params,
        )

    if selectors:
        if grounded_by == "tree" and (source_coordinates or target_coordinates):
            raise ValueError(
                "grounded_by='tree' cannot carry recorded coordinate bases"
            )
        if target_selectors:
            if not target_description:
                raise ValueError(
                    "a selector-grounded drag destination needs target_description "
                    "for semantic healing"
                )
        elif target_description:
            if direction is not None:
                raise ValueError(
                    "an element drag takes a target_description or a direction, "
                    "not both: they are two different end points and nothing "
                    "says which the recording meant"
                )
        elif direction not in _AXIS:
            raise ValueError(
                f"an element drag with no target_description needs a direction, "
                f"one of {sorted(_AXIS)}; got {direction!r}"
            )
        return _run_action(
            driver, _DRAG_ELEMENT_SPEC, selectors,
            description=source_description or description,
            target_description=target_description,
            target_selectors=target_selectors,
            target_grounded_by=target_grounded_by,
            direction=direction,
            fraction=fraction,
            hold_duration_ms=hold_duration_ms,
            move_duration_ms=move_duration_ms,
            hold_at_destination_ms=hold_at_destination_ms,
        )

    if grounded_by == "tree":
        # Grounded by the tree, and no selectors to find it with. Falling
        # through here would replay two remembered ratios for an action authored
        # against a found element — the mis-aimed drag D5 exists to prevent, and
        # a drag that misses moves something rather than nothing.
        raise ValueError(
            "grounded_by='tree' needs selectors: the recording says the tree "
            "found this control and carries nothing to find it with"
        )
    if not source_coordinates or not target_coordinates:
        raise ValueError("drag requires both source_coordinates and target_coordinates")
    return run_driver(
        driver, _DRAG_SPEC,
        source_coordinates=source_coordinates,
        target_coordinates=target_coordinates,
        hold_duration_ms=hold_duration_ms,
        move_duration_ms=move_duration_ms,
        hold_at_destination_ms=hold_at_destination_ms,
    )
