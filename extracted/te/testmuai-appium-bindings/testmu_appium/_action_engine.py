"""Find + act + heal engine shared by every element verb.

Public API to the rest of the package: `_ActionSpec`, `_run_action`, `run_driver`.
Public API of the package: the per-verb wrappers in `_action_<verb>.py` — the only
thing codegen and human authors see.

`_ActionSpec.target_mode` splits the two worlds:
- "element" → optionally settle → find → act, with the failure routing below.
              Explicit native tree grounding skips the global page-source settle:
              its selector walk is the narrower readiness check, and stale/blocked
              recovery still protects the action itself.
- "driver"  → the verb acts on the session; find and heal are skipped entirely and
              a selector set is a generation error, not something to ignore

An element-mode call with NO selectors is the third recorded shape: a
COORDINATE-RECORDED action, which the generator emits as `selectors=None` plus a
complete `fallback_coordinates` basis. Nothing was ever recorded to find, so there is
no strategy walk to exhaust and no instruction for heal to resolve — the recorded
ratio is the whole locator. It replays through the verb's own coord_runner, gated on
the same orientation check as the fallback path. Selectorless WITHOUT a complete basis
(or on a verb with no coord_runner) stays a generation error.

The strategy walk is polled until `default_action_timeout_ms` expires, so a
late-rendering element is waited for rather than healed for: exhaustion is the heal
trigger, and declaring it after one pass turns "not there yet" into "not there". The
walk that is NOT waited out is the one where every strategy matched SEVERAL elements:
that screen has rendered, and polling a recycled view id cannot make it unique.

ACTION SCHEDULING BUDGET. Every phase of ONE verb call shares ONE monotonic deadline,
created at entry (`_Deadline`). Its budget is the sum of the three configured
timeouts — `settle_timeout_ms + default_action_timeout_ms + heal_timeout_ms`, 73s at
the shipped defaults — and each phase gets `min(its own configured budget, whatever
is left)`. No new poll, heal request, recapture or heal retry starts after expiry.
The HTTP heal attempts/backoff are wall-clock bounded. An Appium/ADB/CDP command
already in flight is synchronous and cannot be cancelled here, so it can finish at
its own transport timeout after this scheduling budget expires.

Element-mode failure routing:
- StaleElementReference → the element moved/was recreated; re-find via the RECORDED
  strategies and retry. Not a heal trigger: the recorded locator is still correct.
- intercepted / not-interactable → the element is present but covered or disabled.
  Heal cannot help (a fresh locator finds the same covered element) and coordinates
  would punch straight through the overlay, so this is a bounded stability retry and
  then a failure.
- every strategy exhausted (zero or only-ambiguous everywhere) → semantic heal.
- heal hit → act on the re-found element. Authoritative miss (a server 404) →
  native actions may use their gated recorded-coordinate fallback; web actions
  fail because a stale web point is never a locator. A heal answer that arrived
  but did not resolve LOCALLY to one live element gets one fresh-perception retry
  and then fails; it does not unlock coordinates. Non-authoritative heal failure
  (transport/protocol) does NOT unlock coordinates either: nothing has established
  that the element is actually gone.
"""
import hashlib
import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidElementStateException,
    StaleElementReferenceException,
)

from testmu_appium import _action_web, _config
from testmu_appium._helpers import _screen
from testmu_appium._errors import (
    CoordinateFallbackUnavailable, ElementBlocked, ElementNotFound,
)
from testmu_appium._heal import (
    CACHE_ABSENT, HEAL_SOURCE, VALID_ACTION_TYPES, HealHit, HealNoMatch,
    HealDisabled, HealUnavailable, HealUnresolved, WebHealHit, autoheal, autoheal_web,
    cache_key, invalidate_cache, read_cache, write_cache,
)
from testmu_appium._helpers import _tree
from testmu_appium._helpers.authoring_web_surface import (
    consume_authoring_web_surface,
)
from testmu_appium._helpers._strategy import compile_selector, order_by_score
from testmu_appium._helpers.foreground import foreground_app
from testmu_appium._helpers.vision_coordinates import get_vision_coordinates
from testmu_appium._step import mark_autohealed, record_interacted_element
from testmu_appium._timing import (
    action_timing as _action_timing,
    count as _timing_count,
    phase as _timing_phase,
    set_detail as _set_timing_detail,
    set_route as _set_timing_route,
)

_log = logging.getLogger("testmu_appium")

TARGET_MODES = ("element", "driver")

#: Which reader found the element, and therefore which lookup replays it. Native is
#: the accessibility tree via Appium; web is the DOM over the device's debug channel.
#: Both ACT through Appium — the surface changes where the element is looked up, not
#: what performs the gesture.
SURFACE_NATIVE = "native"
SURFACE_WEB = "web"
SURFACES = (SURFACE_NATIVE, SURFACE_WEB)

#: A stale element is re-found and retried this many times before giving up.
_STALE_RETRIES = 2

#: A blocked element gets this many settle-and-retry rounds, spaced by the delay below.
_BLOCKED_RETRIES = 2
_BLOCKED_RETRY_DELAY_S = 0.5

#: Gap between strategy-walk passes while waiting for a late-rendering element.
_FIND_POLL_INTERVAL_S = 0.15

#: How many consecutive walks may come back "every strategy matched SEVERAL
#: elements" before the walk stops instead of spending the rest of its budget. The
#: first can be a list still animating a row into place; by the second the duplicate
#: is the app's own, and no amount of polling makes a recycled view id unique.
_AMBIGUOUS_PASSES = 2

#: Present, and possibly actionable in a moment: an overlay can be dismissed, an
#: element scrolled into view or enabled. These earn the settle-and-retry rounds.
_BLOCKED_EXCEPTIONS = (
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

#: Present, and the answer will not change. "Invalid state for this command" is a
#: property of the element rather than of the moment — sendKeys to a LinearLayout
#: is refused because a LinearLayout holds no text, and settling does not make one
#: editable. Retrying spends the blocked budget on a verdict already delivered.
_DETERMINISTIC_EXCEPTIONS = (InvalidElementStateException,)


@dataclass(frozen=True)
class _ActionSpec:
    """How to run a single verb.

    runner:       element mode → runner(element, ctx); driver mode → runner(driver, ctx).
                  ctx carries 'driver' plus the wrapper's own kwargs.
    target_mode:  "element" | "driver".
    op_type:      the heal action_type this verb maps onto (click/type/select/scroll).
                  Empty for driver-mode verbs, which never heal.
    coord_runner: coord_runner(driver, x, y, ctx) — the recorded-ratio fallback. A verb
                  without one cannot fall back; the scroll-family verbs deliberately
                  omit it.
    vision_runner: vision_runner(driver, x, y, ctx) — act at a point resolved from
                   the recorded description on the live screen. This is deliberately
                   separate from coord_runner: clear may be vision-grounded but must
                   never wipe whatever happens to occupy a remembered ratio.
    allow_inert_heal: whether semantic heal may return a non-interactive row. False
                      for ordinary element actions; true only for draggable content.
    """

    runner: Callable[[Any, dict], Any]
    target_mode: str = "element"
    op_type: str = "click"
    coord_runner: Optional[Callable[[Any, int, int, dict], Any]] = None
    vision_runner: Optional[Callable[[Any, int, int, dict], Any]] = None
    allow_inert_heal: bool = False

    def __post_init__(self):
        if self.target_mode not in TARGET_MODES:
            raise ValueError(
                f"unknown target_mode {self.target_mode!r}; expected one of {list(TARGET_MODES)}"
            )


def _timeout_ms(key: str, default: int) -> int:
    """A configured millisecond timeout, floored at zero."""
    return max(0, int(_config.get(key, default) or 0))


class _Deadline:
    """The one monotonic start-budget every phase of a single verb call shares.

    Monotonic, not wall clock, so an NTP correction landing mid-gesture cannot cut a
    step short or extend it.

    `phase_end` is how a phase that carries its own configured budget asks when to
    stop — it gets that budget or whatever is left of the verb, whichever runs out
    first. A phase with a zero budget therefore still means "exactly one pass", which
    is the behaviour of an unset `default_action_timeout_ms`.

    This prevents starting another phase after expiry. It cannot interrupt a
    synchronous Appium/ADB/CDP command already dispatched to an external process.
    """

    def __init__(self):
        budget_ms = (
            _timeout_ms("settle_timeout_ms", 3000)
            + _timeout_ms("default_action_timeout_ms", 0)
            + _timeout_ms("heal_timeout_ms", 60000)
        )
        self.expires_at = time.monotonic() + budget_ms / 1000.0

    def remaining_s(self) -> float:
        return max(0.0, self.expires_at - time.monotonic())

    def phase_end(self, budget_ms: int) -> float:
        return min(time.monotonic() + max(0, int(budget_ms or 0)) / 1000.0, self.expires_at)


def _settle(driver, deadline: _Deadline) -> Optional[str]:
    """Wait until the screen stops changing, bounded by settle_timeout_ms.

    Compares consecutive page-source digests: two identical captures mean the
    transition/animation has finished. Best-effort — a driver that cannot produce a
    page source proceeds rather than failing the verb here.

    Settling is the FIRST claim on the verb's shared deadline, so a screen that never
    stops moving spends only the settle budget.

    Returns the page source it settled on, or None when it read none. That document
    is the screen as of now, and re-reading it costs ~2.4s on the reference device.
    """
    budget_ms = _timeout_ms("settle_timeout_ms", 3000)
    if budget_ms <= 0:
        return None
    stop_at = deadline.phase_end(budget_ms)
    previous = None
    source = None
    while time.monotonic() < stop_at:
        try:
            _timing_count("page_source_reads")
            with _timing_phase("page_source"):
                source = driver.page_source
        except Exception as e:  # noqa: BLE001 — settling is an optimisation, not a gate
            _log.debug("[settle] page source unavailable (%s); proceeding", e)
            return None
        digest = hashlib.sha1(source.encode("utf-8", "ignore")).hexdigest()
        if digest == previous:
            return source
        previous = digest
        with _timing_phase("settle_wait"):
            time.sleep(0.15)
    return source


def _find_one(driver, selectors, platform):
    """Try each recorded strategy in score order.

    Returns (element, by, value, tried, ambiguous_only) — the element on the first
    strategy with EXACTLY one match. A strategy matching several elements cannot
    identify the target, so it is skipped like a miss.

    `ambiguous_only` says every strategy matched SEVERAL elements and none matched
    none. The target is on screen and no recorded locator separates it from its
    neighbours, which is the one miss waiting cannot change: a recycled view id
    does not become unique because the caller polled it again.
    """
    tried = []
    matched_several = False
    matched_nothing = False
    _timing_count("find_passes")
    for selector in order_by_score(selectors):
        _timing_count("selector_attempts")
        with _timing_phase("selector_compile"):
            by, value = compile_selector(selector, platform)
        tried.append(selector.get("strategy"))
        try:
            with _timing_phase("element_lookup"):
                matches = driver.find_elements(by, value)
        except StaleElementReferenceException:
            matched_nothing = True
            continue
        if len(matches) == 1:
            _set_timing_detail("winning_strategy", str(selector.get("strategy") or ""))
            return matches[0], by, value, tried, False
        if matches:
            matched_several = True
            _log.info(
                "    [find] strategy %s matched %d elements — ambiguous, trying the next",
                selector.get("strategy"), len(matches),
            )
        else:
            matched_nothing = True
    return None, None, None, tried, matched_several and not matched_nothing


def locate_selectors_rect(driver, selectors, platform):
    """The live rect of the single element the recorded `selectors` name now.

    Re-finds a target through the SAME ranked strategy walk grounding uses
    (`_find_one`): the first recorded selector matching exactly one live element
    wins and its rect is returned. A targeted find — one selector query, no
    page_source dump — so re-measuring one element after a gesture is cheap.

    Returns None when the target is UNRESOLVED — no recorded selector isolates it
    (absent, or only ever ambiguous), or it detached between the find and the rect
    read (a scrolled-away RecyclerView row, whose `.rect` raises). None never means
    "found at the old rect": the caller must not read the absence as movement.
    """
    element, _by, _value, _tried, _ambiguous_only = _find_one(driver, selectors, platform)
    if element is None:
        return None
    try:
        return element.rect
    except StaleElementReferenceException:
        # `.rect` is a second WebDriver call: a target detached since the find
        # (a recycled list row) resolves to None, not an exception.
        return None


def _poll_until(lookup, deadline: _Deadline, give_up=None):
    """Run `lookup` until it yields an element or the find budget runs out.

    The find budget is `default_action_timeout_ms`, capped by whatever is left of the
    verb's shared deadline — the same rule every find and re-find follows. Returns
    None when the budget expires.

    `give_up` is asked after each miss whether waiting could still change the answer;
    when it says no, polling stops there and the rest of the budget is left to the
    phases after it.
    """
    stop_at = deadline.phase_end(_timeout_ms("default_action_timeout_ms", 0))
    while True:
        element = lookup()
        if element is not None:
            return element
        if give_up is not None and give_up():
            return None
        if time.monotonic() >= stop_at:
            return None
        with _timing_phase("find_wait"):
            time.sleep(_FIND_POLL_INTERVAL_S)


def _ambiguity_is_final(seen):
    """A `give_up` predicate that stops a walk which is only ever ambiguous.

    Counts CONSECUTIVE all-ambiguous passes: a pass in which some strategy matched
    nothing is the late-render case and resets the count, because that is the case
    the poll exists for.
    """
    state = {"passes": 0}

    def give_up():
        if not seen or not seen[0][3]:
            state["passes"] = 0
            return False
        state["passes"] += 1
        if state["passes"] < _AMBIGUOUS_PASSES:
            return False
        _log.info(
            "    [find] every recorded strategy matched several elements on %d passes; "
            "the target is on screen and no recorded locator separates it from its "
            "neighbours, so waiting cannot resolve it", state["passes"],
        )
        return True

    return give_up


def _find_within_timeout(driver, selectors, platform, deadline: _Deadline):
    """Poll the strategy walk until `default_action_timeout_ms` (or the verb) runs out.

    Exhaustion is declared only once the budget is spent, so an element that renders
    late — a list that has just finished binding, a fragment mid-transition — is
    waited for rather than healed for. `_settle` narrows that window but does not
    close it: it watches the page source stop changing, which a screen can do while
    still being repopulated.

    Zero (or a negative) budget means exactly one pass. A walk in which every
    strategy matched SEVERAL elements stops after `_AMBIGUOUS_PASSES`, whatever the
    budget: what it found was the target's neighbours, not a screen yet to render.
    """
    tried_seen = []

    def once():
        element, by, value, tried, ambiguous_only = _find_one(driver, selectors, platform)
        tried_seen[:] = [(by, value, tried, ambiguous_only)]
        return element

    element = _poll_until(once, deadline, _ambiguity_is_final(tried_seen))
    by, value, tried, _ = tried_seen[0]
    if element is None:
        return None, None, None, tried
    return element, by, value, tried


def _recorded_refinder(driver, selectors, platform, deadline: _Deadline):
    """Re-find via the RECORDED strategies, for an element that was found that way and
    then went stale.

    Polled on the shared deadline rather than looked up once: the screen rebuild that
    invalidated the handle is usually still in flight when the re-find runs.
    """

    def refind():
        seen = []

        def once():
            element, by, value, tried, ambiguous_only = _find_one(
                driver, selectors, platform)
            seen[:] = [(by, value, tried, ambiguous_only)]
            return element

        element = _poll_until(once, deadline, _ambiguity_is_final(seen))
        return element, seen[0][1]

    return refind


def _healed_refinder(driver, by, value, deadline: _Deadline):
    """Re-find via the HEALED (by, value) pair.

    A healed element was found because every recorded strategy missed, so the healed
    lookup is the only locator known to resolve it.

    Polled on the shared deadline, like the recorded re-finder.
    """

    def once():
        try:
            _timing_count("healed_refind_attempts")
            with _timing_phase("element_lookup"):
                matches = driver.find_elements(by, value)
        except Exception as e:  # noqa: BLE001 — a lookup that errors is a miss
            _log.debug("[retry] healed re-find failed: %s", e)
            return None
        return matches[0] if len(matches) == 1 else None

    def refind():
        return _poll_until(once, deadline), value

    return refind


def _record_telemetry(element, locator: str) -> None:
    """Record the interacted-element payload the LT step-end hook carries.

    The key names are the legacy runtime's `interacted_element_info` names:
    `original_locator`, `bounds`, `center`.

    Two intentional divergences from that payload:
    1. `original_locator` is the COMPILED locator string that actually found the
       element, not the raw recorded locator LIST legacy stores.
    2. `element_class` and `is_coordinates_used_for_interaction` are not emitted. The
       coordinate-fallback path records its own payload with an empty locator and a
       zero-area box.

    Best-effort: an element that goes stale between the act and the read must not
    turn a successful step into a failure.
    """
    try:
        rect = element.rect
        x, y = int(rect["x"]), int(rect["y"])
        w, h = int(rect["width"]), int(rect["height"])
        record_interacted_element({
            "original_locator": locator,
            "bounds": [x, y, x + w, y + h],
            "center": [x + w // 2, y + h // 2],
        })
    except Exception as e:  # noqa: BLE001
        _log.debug("[telemetry] element bounds unavailable: %s", e)


def _live_orientation(driver) -> tuple[str, int, int]:
    """The live orientation, derived from the window rather than driver.orientation.

    The window size is needed anyway to scale the ratios, so this costs one round trip
    instead of two.

    A SQUARE window (width == height) is called "landscape", always. This value is
    compared against the recorded orientation to decide whether a coordinate fallback
    may run, so the tie must break the same way every time.
    """
    size = _screen.window_size(driver)
    width, height = size[0], size[1]
    return ("portrait" if width < height else "landscape"), width, height


#: The keys a recorded coordinate basis must carry to be replayable at all. `window`
#: rides along for provenance and is deliberately not required: the ratios are scaled
#: onto the LIVE window, so the recorded one is not an input to the replay.
_BASIS_KEYS = ("x_ratio", "y_ratio", "orientation")


def _basis_is_complete(basis) -> bool:
    """Whether a recorded basis carries every key the ratio replay needs."""
    return bool(basis) and all(basis.get(key) is not None for key in _BASIS_KEYS)


def _coordinates_from_basis(driver, basis: dict) -> tuple[int, int]:
    """Scale a recorded ratio pair onto the live window.

    Raises CoordinateFallbackUnavailable when the basis is incomplete or was recorded
    in a different orientation: replaying a portrait ratio on a landscape screen taps
    a confidently wrong place, which is worse than failing.
    """
    required = _BASIS_KEYS
    missing = [key for key in required if basis.get(key) is None]
    if missing:
        raise CoordinateFallbackUnavailable(
            f"recorded coordinate basis is incomplete (missing {missing}); "
            f"refusing to guess at a tap location"
        )

    live_orientation, width, height = _live_orientation(driver)
    if live_orientation != str(basis["orientation"]).lower():
        raise CoordinateFallbackUnavailable(
            f"recorded coordinate basis orientation is {basis['orientation']!r} but the "
            f"device is {live_orientation!r}; the ratio would land somewhere else"
        )

    return int(float(basis["x_ratio"]) * width), int(float(basis["y_ratio"]) * height)


def run_driver(driver, spec: _ActionSpec, **params):
    """Run a driver-mode verb: no find, no heal, no selectors."""
    if spec.target_mode != "driver":
        raise ValueError(f"run_driver requires target_mode='driver', got {spec.target_mode!r}")
    ctx = {"driver": driver, **params}
    surface = str(params.get("surface") or SURFACE_NATIVE)
    with _action_timing(
        spec.op_type or "driver_action", target_mode="driver", surface=surface
    ):
        _set_timing_route("driver")
        _timing_count("gesture_attempts")
        with _timing_phase("device_action"):
            return spec.runner(driver, ctx)


def _run_action(
    driver,
    spec: _ActionSpec,
    selectors,
    *,
    description: str = "",
    fallback_coordinates: Optional[dict] = None,
    surface: str = SURFACE_NATIVE,
    frame_path: str = "",
    grounded_by: str = "",
    **params,
):
    """Element-mode entry: settle → find → act, with the routing described above."""
    if spec.target_mode == "driver":
        return _run_action_impl(
            driver, spec, selectors, description=description,
            fallback_coordinates=fallback_coordinates, surface=surface,
            frame_path=frame_path, grounded_by=grounded_by, **params,
        )
    with _action_timing(
        spec.op_type or "action", target_mode="element", surface=surface,
        grounded_by=grounded_by,
    ):
        return _run_action_impl(
            driver, spec, selectors, description=description,
            fallback_coordinates=fallback_coordinates, surface=surface,
            frame_path=frame_path, grounded_by=grounded_by, **params,
        )


def _run_action_impl(
    driver,
    spec: _ActionSpec,
    selectors,
    *,
    description: str = "",
    fallback_coordinates: Optional[dict] = None,
    surface: str = SURFACE_NATIVE,
    frame_path: str = "",
    grounded_by: str = "",
    **params,
):
    """Implementation behind the opt-in action timing boundary."""
    if spec.target_mode == "driver":
        if selectors:
            raise ValueError(
                f"driver-mode verb received {len(selectors)} selectors; driver-mode verbs "
                f"act on the session and never take a locator"
            )
        return run_driver(driver, spec, **params)

    if grounded_by not in ("", "tree", "vision"):
        raise ValueError(
            f"unknown grounded_by {grounded_by!r}; expected '', 'tree', or 'vision'"
        )
    if surface not in SURFACES:
        raise ValueError(
            f"unknown surface {surface!r}; expected one of {list(SURFACES)}. The surface "
            f"names the reader an element was recorded through, and defaulting an "
            f"unrecognised one to the native walk would look for a DOM element in the "
            f"view hierarchy"
        )

    platform = _config.platform()
    ctx = {"driver": driver, "description": description, **params}

    if grounded_by == "vision":
        if selectors:
            raise ValueError(
                "grounded_by='vision' cannot carry selectors: replay must reproduce "
                "the vision path authoring used"
            )
        if fallback_coordinates:
            raise ValueError(
                "grounded_by='vision' cannot carry fallback_coordinates: the "
                "recording must re-resolve its intent, not remember a point"
            )
        if surface != SURFACE_NATIVE or frame_path:
            raise ValueError(
                "grounded_by='vision' is a native visible-target action and cannot "
                "carry a web surface or frame_path"
            )
        if not description.strip():
            raise ValueError(
                "grounded_by='vision' needs description: the words are its only "
                "durable locator"
            )
        if spec.vision_runner is None:
            raise ValueError(
                f"verb {spec.op_type!r} does not support vision grounding"
            )
    elif grounded_by == "tree":
        if not selectors:
            raise ValueError(
                "grounded_by='tree' needs selectors: the recording says the tree "
                "found the target and carries nothing to find it with"
            )
        if fallback_coordinates:
            raise ValueError(
                "grounded_by='tree' cannot carry fallback_coordinates: selector "
                "failure must not degrade to a remembered point"
            )

    # Explicit native tree grounding already carries selectors whose live, unique
    # resolution is the readiness condition. Requiring the entire page source to be
    # byte-identical first is both broader and much slower, and unrelated dynamic
    # nodes can prevent it from ever settling. Keep page-source settlement for web
    # placement, vision, recorded coordinates, and legacy calls; stale/blocked
    # selector recovery below remains unchanged.
    deadline = _Deadline()
    prepared_web_surface = (
        consume_authoring_web_surface()
        if surface == SURFACE_WEB
        and grounded_by == "tree"
        and bool(selectors)
        else None
    )
    target_scoped_settle = (
        surface == SURFACE_NATIVE
        and grounded_by == "tree"
        and bool(selectors)
    )
    if prepared_web_surface is not None:
        ctx["_prepared_web_surface"] = prepared_web_surface
        ctx["_page_source"] = None
        _set_timing_detail("settle_strategy", "prepared_web_target")
    elif target_scoped_settle:
        ctx["_page_source"] = None
        _set_timing_detail("settle_strategy", "target_scoped")
    else:
        ctx["_page_source"] = _settle(driver, deadline)
        _set_timing_detail("settle_strategy", "page_source")
    ctx["_deadline"] = deadline

    if grounded_by == "vision":
        _set_timing_route("vision")
        _timing_count("vision_attempts")
        with _timing_phase("vision_lookup"):
            x, y = get_vision_coordinates(driver, description, spec.op_type or "click")
        _log.info("    [vision] %s at (%d, %d)", spec.op_type or "action", x, y)
        record_interacted_element({
            "original_locator": "",
            "bounds": [x, y, x, y],
            "center": [x, y],
        })
        _timing_count("gesture_attempts")
        with _timing_phase("device_action"):
            return spec.vision_runner(driver, x, y, ctx)

    if not selectors:
        # A recording with no selectors still NAMES its target, and that name is a
        # locator: heal resolves it against the screen in front of it and returns a
        # live element. The recorded ratio cannot — it is recomputed against the
        # live window, so it survives a rescaled screen but not a reflowed one, and
        # it carries nothing that would notice it had landed on the wrong thing.
        # So heal is asked first here exactly as it is when recorded selectors run
        # out, and the ratio stays what its kwarg calls it: a fallback.
        if description.strip() and spec.op_type in VALID_ACTION_TYPES:
            _set_timing_route("heal_or_fallback")
            return _heal_or_fall_back(
                driver, spec, ctx, selectors, description, [],
                fallback_coordinates, deadline,
            )
        _set_timing_route("recorded_coordinates")
        return _run_recorded_coordinates(driver, spec, ctx, fallback_coordinates)

    if surface == SURFACE_WEB:
        _set_timing_route("web_selector")
        return _run_web_action(
            driver, spec, ctx, selectors, description, frame_path, deadline)

    element, _, value, tried = _find_within_timeout(driver, selectors, platform, deadline)

    if element is not None:
        _set_timing_route("native_selector")
        return _act_with_retries(
            driver, spec, ctx, element, value,
            _recorded_refinder(driver, selectors, platform, deadline), deadline,
        )

    _set_timing_route("heal_or_fallback")
    return _heal_or_fall_back(
        driver, spec, ctx, selectors, description, tried, fallback_coordinates, deadline
    )


def _open_web_surface(driver, page_source=None):
    """The page on screen, placed against the device's own tree.

    The native tree is read here rather than inside the web module because it is
    what the origin is solved against: the OS's geometry for elements the DOM also
    describes is the only thing that says where the web content sits.

    `page_source` is the document settling already read. A page source costs ~2.4 s
    on the reference device, so a web action that re-read it would pay for the
    screen three times over.
    """
    _, width, height = _live_orientation(driver)
    # Through the platform dispatcher, NOT `_tree` directly. `_tree` is the
    # Android producer; handed an XCUITest document it finds nothing, so no DOM
    # label has a native twin, the origin cannot be solved, and the action fails
    # with "no web page on this screen could be read and placed" — on a screen
    # whose page perception had just read and placed a moment earlier.
    # Imported here rather than at module scope: `perception` is the public
    # surface and imports back into this package's action modules.
    from testmu_appium.perception import parse_tree as _parse_tree

    native = _parse_tree(page_source or driver.page_source, width, height,
                         platform=_config.platform())
    return _action_web.open_web_surface(native, foreground_app(driver))


def _prepared_web_surface_for(driver, envelope):
    """Return a fresh one-action handoff only while its device context matches."""
    if not isinstance(envelope, dict) or envelope.get("surface") is None:
        return None
    try:
        if time.monotonic() - float(envelope.get("prepared_at")) > 3.0:
            return None
    except (TypeError, ValueError):
        return None

    expected_session = envelope.get("session_id")
    if expected_session is not None and getattr(driver, "session_id", None) != expected_session:
        return None
    expected_package = str(envelope.get("package") or "")
    if expected_package and foreground_app(driver) != expected_package:
        return None
    expected_window = list(envelope.get("window") or [])
    if len(expected_window) != 2:
        return None
    try:
        # Through the reader chain, not the raw W3C call: xcuitest-driver 9.x
        # cannot serve get_window_size at all, so the direct call made this
        # validation fail on EVERY iOS action — silently disabling the
        # prepared-surface handoff it exists to allow.
        live = _screen.window_size(driver)
        if [int(live[0]), int(live[1])] != [
            int(expected_window[0]), int(expected_window[1]),
        ]:
            return None
    except Exception:  # noqa: BLE001 — incomplete validation takes the safe path
        return None
    return envelope["surface"]


def _run_web_action(driver, spec, ctx, selectors, description, frame_path, deadline):
    """Locate over the debug channel, act with the gesture the native path uses.

    The verb's `coord_runner` is the actor: a web element resolves to a point, and
    a point is what a gesture takes. A verb without one cannot serve a web action —
    the scroll family deliberately has none, and scrolling web content is the
    screen gesture it already was.

    When the recorded selectors are exhausted, the normal autoheal endpoint sees
    the canonical generated tree. Its returned index maps to a private DOM
    descriptor, which is re-resolved against a fresh capture before any gesture.
    """
    tried = [selector.get("strategy") for selector in order_by_score(selectors)]
    if spec.coord_runner is None:
        raise ValueError(
            f"verb {spec.op_type!r} was given a web-surface action but cannot act on a "
            f"point; only the verbs with a coordinate runner can drive web content"
        )

    found = {"surface": None, "element": None}
    settled = ctx.pop("_page_source", None)
    prepared = ctx.pop("_prepared_web_surface", None)

    def once():
        nonlocal settled, prepared
        _timing_count("web_lookup_attempts")
        with _timing_phase("web_lookup"):
            surface = _prepared_web_surface_for(driver, prepared)
            if prepared is not None:
                prepared = None
                element = (
                    _action_web.locate(
                        surface.elements,
                        selectors,
                        frame_path,
                        strict_path=True,
                        action_type=spec.op_type,
                        allow_inert=spec.allow_inert_heal,
                    )
                    if surface is not None
                    else None
                )
                if (
                    element is not None
                    and _action_web.prepared_target_is_current(surface, element)
                ):
                    _set_timing_detail("web_surface_source", "prepared")
                    found.update(surface=surface, element=element)
                    return element

                # The handoff is only a fast path.  Once it fails validation,
                # recover through the exact pre-existing settle/read/calibrate
                # path before considering heal or another action attempt.
                settled = _settle(driver, deadline)
                _set_timing_detail(
                    "settle_strategy", "prepared_web_fallback_page_source"
                )

            surface = _open_web_surface(driver, settled)
            if surface is None:
                return None
            element = _action_web.locate(
                surface.elements,
                selectors,
                frame_path,
                strict_path=True,
                action_type=spec.op_type,
                allow_inert=spec.allow_inert_heal,
            )
        found.update(surface=surface, element=element)
        return element

    def once_then_fresh():
        nonlocal settled
        element = once()
        settled = None
        return element

    element = _poll_until(once_then_fresh, deadline)
    surface = found["surface"]
    if surface is None:
        raise ElementNotFound(
            description, tried,
            "no web page on this screen could be read and placed: either the device "
            "publishes no debug socket for it, or nothing it shows also appears in the "
            "device's own tree, which is what locates the page on screen")
    if element is None:
        surface, element = _heal_web_or_fail(
            driver, spec, selectors, description, frame_path, tried, deadline
        )

    return _act_on_web_point(driver, spec, ctx, surface, element)


def _act_on_web_point(driver, spec, ctx, surface, element):
    with _timing_phase("coordinate_resolution"):
        x, y = _action_web.point_for(surface, element)
    _log.info("    [web] %s -> (%d, %d)",
              element.get("css") or element.get("label", "")[:40], x, y)
    record_interacted_element({
        "original_locator": element.get("css", ""),
        "bounds": list(_action_web.device_bounds(surface, element)),
        "center": [x, y],
    })
    # TYPE-family verbs only, twice over. The clear was gated on the element
    # alone, and every web verb's ctx lacks the `clear_first` key — so a web
    # CLICK on a pre-filled editable wiped it through the page before the
    # click even landed. The verb's own op_type is the boundary.
    is_type = spec.op_type == "type" and element.get("editable")
    # Clear through the page, not through native focus. The coordinate runner
    # would use `switch_to.active_element`, which cannot see a focused WKWebView
    # field and raises instead. Only when the page confirms it emptied the field
    # is the native clear stood down, so a surface that cannot answer keeps
    # exactly today's behaviour.
    if is_type and ctx.get("clear_first", True):
        if _action_web.clear_value(surface, element):
            ctx = {**ctx, "clear_first": False}
    # The page can say where it stands between the focus tap and the keys —
    # which editable holds focus, and whether the tap NAVIGATED. Handed to the
    # runner as a probe rather than called here, because only the runner knows
    # the moment between its tap and its keystrokes.
    if is_type:
        before = _action_web.focus_state(surface)
        if before is not None:
            ctx = {**ctx,
                   "web_focus_state": lambda: _action_web.focus_state(surface),
                   "web_href_before": before.get("href", "")}
            # `web_prefocus` fires any redraw-on-focus through the page, with
            # no click in flight to steal. WEBKIT ONLY, by protocol marker:
            # Blink delivers a click to the touch-start node, so Chrome cannot
            # be stolen this way — gating here is what keeps Android's typing
            # exactly as it is on the base branch.
            if not getattr(surface.channel, "cdp_rpc", True):
                ctx = {**ctx, "web_prefocus":
                       lambda: _action_web.prefocus_point(surface, element)}
    _timing_count("gesture_attempts")
    with _timing_phase("device_action"):
        return spec.coord_runner(driver, x, y, ctx)


def _web_cache_key(spec, selectors, frame_path):
    return (
        "web", spec.op_type, frame_path or "", spec.allow_inert_heal,
        *cache_key(selectors),
    )


def _resolve_web_descriptor(driver, descriptor, deadline=None):
    """Freshly resolve and, if needed, scroll one private web descriptor."""
    if deadline is not None and deadline.remaining_s() <= 0:
        return None
    surface = _open_web_surface(driver)
    if surface is None:
        return None
    element = _action_web.resolve_descriptor(surface.all_elements, descriptor)
    if element is None:
        return None
    if not _action_web.in_view(surface, element):
        if deadline is not None and deadline.remaining_s() <= 0:
            return None
        try:
            verdict = _action_web.scroll_descriptor(surface.channel, descriptor)
        except Exception as e:  # noqa: BLE001 — becomes an unresolved heal answer
            _log.info("    [AutoHeal] healed web scroll failed (%s)", e)
            return None
        if verdict == "missing":
            return None
        # Scrolling invalidates every rectangle and the calibration that placed it.
        if deadline is not None and deadline.remaining_s() <= 0:
            return None
        surface = _open_web_surface(driver)
        if surface is None:
            return None
        element = _action_web.resolve_descriptor(surface.all_elements, descriptor)
        if element is None or not _action_web.in_view(surface, element):
            return None
    return surface, element


def _consult_web_heal(driver, spec, surface, description, deadline):
    """Consult and strictly re-resolve, with one fresh-perception retry."""
    current = surface
    last_reason = ""
    for attempt in range(2):
        if deadline.remaining_s() <= 0:
            return HealUnavailable("action deadline was exhausted during web autoheal")
        _timing_count("heal_attempts")
        with _timing_phase("heal"):
            outcome = autoheal_web(
                driver,
                current,
                description,
                spec.op_type,
                budget_s=deadline.remaining_s(),
                allow_inert=spec.allow_inert_heal,
            )
        if not isinstance(outcome, WebHealHit):
            return outcome
        if deadline.remaining_s() <= 0:
            return HealUnavailable("action deadline was exhausted during web autoheal")
        with _timing_phase("heal_resolution"):
            resolved = _resolve_web_descriptor(driver, outcome.descriptor, deadline)
        if resolved is not None:
            return outcome, resolved
        last_reason = (
            f"web descriptor for dom_index {outcome.dom_index} did not resolve "
            "to one visible element in its original frame and shadow context"
        )
        if attempt == 0:
            if deadline.remaining_s() <= 0:
                return HealUnavailable(
                    "action deadline was exhausted before web autoheal retry"
                )
            _log.info(
                "    [AutoHeal] %s; one fresh-perception retry", last_reason
            )
            current = _open_web_surface(driver)
            if current is None:
                break
    return HealUnresolved(last_reason or "the healed web descriptor could not be resolved")


def _heal_web_or_fail(
    driver, spec, selectors, description, frame_path, tried, deadline
):
    # A web action is selector-grounded by construction. It must surface the
    # recorded selector failure when deterministic mode is requested; an old point
    # is never a safe substitute for a web element.
    if not _config.heal:
        raise ElementNotFound(
            description, tried,
            "recorded web selectors did not resolve and autoheal is off (TESTMU_HEAL)",
        )
    if not (description or "").strip():
        raise ElementNotFound(
            description,
            tried,
            "recorded web selectors failed and no action description was supplied "
            "for autoheal",
        )

    key = _web_cache_key(spec, selectors, frame_path)
    cached = read_cache(key)
    if cached is None:
        raise ElementNotFound(
            description, tried, "autoheal previously reported no matching web element"
        )

    if cached is not CACHE_ABSENT:
        resolved = _resolve_web_descriptor(driver, cached, deadline)
        if resolved is not None:
            mark_autohealed(HEAL_SOURCE)
            return resolved
        invalidate_cache(key)

    if deadline.remaining_s() <= 0:
        raise ElementNotFound(
            description, tried,
            "action deadline was exhausted before web autoheal recapture",
        )
    surface = _open_web_surface(driver)
    if surface is None:
        raise ElementNotFound(
            description, tried,
            "the web page could not be recaptured for autoheal",
        )
    result = _consult_web_heal(driver, spec, surface, description, deadline)
    if isinstance(result, tuple):
        outcome, resolved = result
        write_cache(key, outcome.descriptor)
        mark_autohealed(outcome.source)
        return resolved
    if isinstance(result, HealNoMatch):
        # Unlike native healing, a web miss never licenses replay of an old point.
        write_cache(key, None)
        raise ElementNotFound(description, tried, result.reason)
    if isinstance(result, HealUnresolved):
        raise ElementNotFound(
            description, tried,
            f"heal answered but its web descriptor did not resolve: {result.reason}",
        )
    if isinstance(result, HealDisabled):
        raise ElementNotFound(
            description, tried,
            "recorded web selectors did not resolve and autoheal is off (TESTMU_HEAL)",
        )
    cause = (
        getattr(result, "cause", None)
        or getattr(result, "detail", None)
        or getattr(result, "reason", "")
    )
    raise ElementNotFound(description, tried, f"heal could not be consulted: {cause}")


def _run_recorded_coordinates(driver, spec, ctx, basis):
    """Replay a coordinate-recorded action: the recorded ratio IS the locator.

    Reached only when the generator emitted no selectors at all, which it does for an
    action the recorder captured as a point on the screen rather than as an element.
    There is nothing to find, nothing to poll for and nothing for heal to resolve.

    The orientation gate is the same one the fallback path uses: a portrait ratio
    replayed on a landscape screen taps a confidently wrong place. A selectorless call
    WITHOUT a complete basis, or on a verb that has no coord_runner, raises ValueError
    rather than ElementNotFound — it is producer/binding skew, not a runtime condition.
    """
    if spec.coord_runner is None or not _basis_is_complete(basis):
        raise ValueError(
            f"element-mode verb received no selectors; the only selectorless shape is a "
            f"coordinate-recorded action, which needs a complete recorded basis "
            f"{list(_BASIS_KEYS)} and a verb that can replay one "
            f"(basis={basis!r}, coord_runner={'present' if spec.coord_runner else 'absent'})"
        )

    with _timing_phase("coordinate_resolution"):
        x, y = _coordinates_from_basis(driver, basis)
    _log.info("    [coordinates] recorded-ratio action at (%d, %d)", x, y)
    record_interacted_element({
        "original_locator": "",
        "bounds": [x, y, x, y],
        "center": [x, y],
    })
    _timing_count("gesture_attempts")
    with _timing_phase("device_action"):
        return spec.coord_runner(driver, x, y, ctx)


def _act_with_retries(driver, spec, ctx, element, locator, refind, deadline: _Deadline):
    """Run the verb, absorbing staleness by re-finding and blockage by settling.

    `refind` is the callable that knows HOW this element was located — recorded
    strategies or a healed locator — and returns a fresh (element, locator) pair.
    """
    stale_left, blocked_left = _STALE_RETRIES, _BLOCKED_RETRIES
    while True:
        try:
            _timing_count("gesture_attempts")
            with _timing_phase("device_action"):
                result = spec.runner(element, ctx)
            _timing_count("telemetry_reads")
            with _timing_phase("element_telemetry"):
                _record_telemetry(element, locator or "")
            return result
        except StaleElementReferenceException:
            _timing_count("stale_retries")
            if stale_left <= 0:
                raise
            stale_left -= 1
            _log.info("    [retry] element went stale; re-finding")
            element, locator = refind()
            if element is None:
                raise
        except _DETERMINISTIC_EXCEPTIONS as exc:
            raise ElementBlocked(ctx.get("description", ""), exc) from exc
        except _BLOCKED_EXCEPTIONS as exc:
            _timing_count("blocked_retries")
            if blocked_left <= 0:
                raise ElementBlocked(ctx.get("description", ""), exc) from exc
            blocked_left -= 1
            _log.info(
                "    [retry] element present but blocked (%s); settling", type(exc).__name__
            )
            with _timing_phase("retry_wait"):
                time.sleep(_BLOCKED_RETRY_DELAY_S)
            _settle(driver, deadline)


def _replay_cached_remap(driver, cached):
    """Re-run a cached healed lookup. Returns the element, or None when it no longer
    resolves to exactly one live match (including when the lookup itself errors)."""
    by, value = cached
    try:
        _timing_count("healed_refind_attempts")
        with _timing_phase("element_lookup"):
            matches = driver.find_elements(by, value)
    except Exception as e:  # noqa: BLE001 — a lookup that errors is a miss, not a crash
        _log.info("    [AutoHeal] cached remap lookup failed (%s); re-healing", e)
        return None
    if len(matches) == 1:
        return matches[0]
    _log.info(
        "    [AutoHeal] cached remap now matches %d elements; re-healing", len(matches)
    )
    return None


def _heal_cache_key(spec, selectors, description):
    """What identifies a heal answer within a step.

    Recorded selectors identify the target whenever there are any. A selectorless
    recording carries only its description, and `cache_key` folds every one of them
    to the same empty tuple — so the description stands in, or the second
    selectorless action in a step reads the first one's answer.
    """
    identity = cache_key(selectors) or (("description", description),)
    return (spec.allow_inert_heal, *identity)


def _heal_or_fall_back(driver, spec, ctx, selectors, description, tried, basis, deadline):
    """Every recorded strategy missed — or there were none. Heal, then — only on an
    authoritative miss — the recorded-ratio coordinate fallback."""
    # Explicit heal-off is deterministic, not a failed heal attempt. Reuse only
    # the provenance the recording supplied: point-grounded calls have no selectors
    # and can execute their orientation-gated point; tree-grounded calls must expose
    # the selector miss so the host can re-plan rather than blindly tapping pixels.
    if not _config.heal:
        outcome = HealDisabled("autoheal is off (TESTMU_HEAL)")
        if not selectors:
            return _coordinate_fallback(driver, spec, ctx, description, tried, basis, outcome)
        raise ElementNotFound(
            description, tried,
            "recorded selectors did not resolve and autoheal is off (TESTMU_HEAL)",
        )

    key = _heal_cache_key(spec, selectors, description)
    cached = read_cache(key)

    if cached is None:
        # Negative sentinel: heal already answered "not here" for this locator in this
        # step. Re-asking cannot produce a different answer and costs a screenshot,
        # a page source and a round trip.
        _log.info("    [AutoHeal] skipped — authoritative miss already cached for this step")
        outcome = HealNoMatch("cached authoritative miss for this step")
    elif cached is not CACHE_ABSENT:
        element = _replay_cached_remap(driver, cached)
        if element is not None:
            mark_autohealed(HEAL_SOURCE)
            return _act_with_retries(
                driver, spec, ctx, element, cached[1],
                _healed_refinder(driver, *cached, deadline=deadline), deadline,
            )
        # The remap went stale (the screen moved on). Only a server 404 is evidence
        # that the element is gone, so the entry is dropped and heal is asked again
        # rather than the negative sentinel being written here.
        invalidate_cache(key)
        outcome = _consult_heal(driver, spec, description, deadline)
    else:
        outcome = _consult_heal(driver, spec, description, deadline)

    if isinstance(outcome, HealHit):
        write_cache(key, (outcome.by, outcome.value))
        mark_autohealed(outcome.source)
        return _act_with_retries(
            driver, spec, ctx, outcome.element, outcome.value,
            _healed_refinder(driver, outcome.by, outcome.value, deadline), deadline,
        )

    if isinstance(outcome, HealNoMatch):
        write_cache(key, None)
        return _coordinate_fallback(driver, spec, ctx, description, tried, basis, outcome)

    if isinstance(outcome, HealDisabled):
        if not selectors:
            return _coordinate_fallback(driver, spec, ctx, description, tried, basis, outcome)
        raise ElementNotFound(
            description, tried,
            "recorded selectors did not resolve and autoheal is off (TESTMU_HEAL)",
        )

    if isinstance(outcome, HealUnresolved):
        # The server answered and the retry below already re-perceived the screen; the
        # answer still would not resolve to one live element. Not cached and not a
        # RECORDED-coordinate unlock: only a 404 says the element is gone.
        centre = _healed_centre(spec, outcome)
        if centre is not None:
            return _act_at_healed_centre(driver, spec, ctx, *centre)
        raise ElementNotFound(
            description, tried,
            f"heal answered but its answer did not resolve to a live element: "
            f"{outcome.reason}",
        )

    # HealUnavailable / HealProtocolError: not authoritative, not cached, and NOT a
    # licence to tap recorded coordinates — nothing established that the element is
    # actually gone.
    cause = getattr(outcome, "cause", None) or getattr(outcome, "detail", "")
    raise ElementNotFound(description, tried, f"heal could not be consulted: {cause}")


def _consult_heal(driver, spec, description, deadline: _Deadline):
    """Ask heal, allowing ONE retry after a non-authoritative unresolved answer.

    Every heal call captures its own fresh perception, so the retry is a new look at
    the screen rather than a re-send of the same snapshot. Bounded at one retry.

    `budget_s` caps the HTTP timeout at what is left of the verb, so a heal request
    cannot outlive the step it belongs to.
    """
    kwargs = {"budget_s": deadline.remaining_s()}
    if spec.allow_inert_heal:
        kwargs["allow_inert"] = True
    _timing_count("heal_attempts")
    with _timing_phase("heal"):
        outcome = autoheal(driver, description, spec.op_type, **kwargs)
    if not isinstance(outcome, HealUnresolved):
        return outcome
    _log.info(
        "    [AutoHeal] answer did not resolve locally (%s); one fresh-perception retry",
        outcome.reason,
    )
    kwargs["budget_s"] = deadline.remaining_s()
    _timing_count("heal_attempts")
    with _timing_phase("heal"):
        return autoheal(driver, description, spec.op_type, **kwargs)


def _healed_centre(spec, outcome):
    """Where heal's own answer sat, as (x, y), or None when that cannot be acted on.

    The descriptor carries the centre from the SAME parse the server's dom_index
    refers to — the recorded description resolved against the live screen, which is
    what `vision_runner` names. It is not the recorded ratio: that one is
    authoring-time and stays behind an authoritative 404.

    None when the verb has no point runner (select opens a picker, an element scroll
    needs its container), when the descriptor kept no centre, or when the lookup
    matched SEVERAL elements — that is an ambiguity signal, and `disambiguate_by_centre`
    already weighed this same centre against live geometry and declined.
    """
    if spec.vision_runner is None or outcome.matched:
        return None
    descriptor = outcome.descriptor or {}
    centre = descriptor.get("centre") or descriptor.get("center")
    if not centre or len(centre) != 2:
        return None
    try:
        return int(centre[0]), int(centre[1])
    except (TypeError, ValueError):
        return None


def _act_at_healed_centre(driver, spec, ctx, x, y):
    """Act where heal said the element was, having failed to re-find it live.

    Android draws a dropdown's option rows in a child Pop-Up Window: they are in the
    captured tree — the server selects them by dom_index — and no UiSelector reaches
    them, so the re-find can only ever return zero. The centre is the one piece of
    evidence that survives that.
    """
    _log.info(
        "    [AutoHeal] answer did not re-find; acting at its captured centre (%d, %d)",
        x, y,
    )
    mark_autohealed(HEAL_SOURCE)
    record_interacted_element({
        "original_locator": "",
        "bounds": [x, y, x, y],
        "center": [x, y],
    })
    _set_timing_route("healed_centre")
    _timing_count("gesture_attempts")
    with _timing_phase("device_action"):
        return spec.vision_runner(driver, x, y, ctx)


def _coordinate_fallback(driver, spec, ctx, description, tried, basis, outcome):
    if not basis or spec.coord_runner is None:
        raise ElementNotFound(description, tried, outcome.reason)
    try:
        with _timing_phase("coordinate_resolution"):
            x, y = _coordinates_from_basis(driver, basis)
    except CoordinateFallbackUnavailable as exc:
        raise ElementNotFound(description, tried, outcome.reason) from exc
    _log.info("    [AutoHeal] authoritative miss; recorded-ratio fallback at (%d, %d)", x, y)
    record_interacted_element({
        "original_locator": "",
        "bounds": [x, y, x, y],
        "center": [x, y],
    })
    _set_timing_route("coordinate_fallback")
    _timing_count("gesture_attempts")
    with _timing_phase("device_action"):
        return spec.coord_runner(driver, x, y, ctx)
