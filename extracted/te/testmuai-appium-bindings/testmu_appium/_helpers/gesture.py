"""Coordinate-level gesture primitives.

Every gesture is single-finger — the recorded mobile action surface has no multi-touch
anywhere, so there is no pinch/zoom primitive to build on.

Each public verb resolves its platform's adapter from the "gesture" registry and
invokes it. A `mobile:` script is preferred where it can express the gesture:
it takes screen coordinates directly, runs device-side, and answers questions a
composed gesture cannot — Android's `scrollGesture` reports whether anything is
left to scroll, which `scroll_until` stops on.

Where a script cannot express what was asked, the gesture is composed as a W3C
pointer sequence instead, step by step. That is now every iOS drag (its script
lifts on arrival, floors the pickup at 0.5 s, and opens with a pickup overture
of its own) and every iOS scroll (its touch has to settle for less than the long-press
threshold). Android composes only a drag that must HOLD at its destination.
"""
import logging
from dataclasses import dataclass
from typing import Optional

from testmu_appium._helpers import _adapters
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

DEFAULT_LONG_PRESS_MS = 800
DEFAULT_MULTI_CLICK_GAP_S = 0.1

#: The gesture names this binding can replay, under either recorded spelling.
CLICK_GESTURES = ("long_press", "multi_click")


# ── Shared: gestures composed step by step ───────────────────────────────
#
# Both platforms have a `mobile:` script for the common case and reach for a
# composed W3C sequence where that script cannot express what was asked. The
# primitives live here rather than under one platform because they belong to
# neither.

#: Milliseconds a COMPOSED drag spends travelling when the caller does not say.
#: Slow enough that the control is dragged rather than flung at.
_COMPOSED_DRAG_MOVE_MS = 600

#: Floor under a CALLER-STATED travel. A composed move is interpolated into
#: intermediate pointer events, so the duration decides how many the control
#: sees; near zero the finger teleports and a recogniser that reads continuous
#: updates can miss the drag entirely. Only degenerate values are refused — a
#: caller asking for a faster-than-default travel gets it, because the controls
#: this verb drives (a slide track, a tile, a picker thumb) settle where the
#: finger is released and carry no momentum to overshoot with.
_COMPOSED_DRAG_MIN_MOVE_MS = 50

#: Milliseconds a COMPOSED drag presses before it travels, when the caller
#: records no pickup. Both platforms compose with the same value: the scripts
#: they replace each perform a press of their own, so a composed drag that went
#: straight from touch-down to travel would silently stop picking up the
#: controls that arm on a long press.
_COMPOSED_DRAG_PICKUP_MS = 500


def _w3c_touch(driver):
    """A finger, as a W3C pointer input.

    Not `mobile: tap`. Two reasons, one measured and one from the design:
    WebDriverAgent builds in the field do not all serve `/wda/tap` — the one this
    was verified against answers `Unhandled endpoint` — and a synthesized gesture
    is documented NOT to focus a web input, where a real pointer down-up does.
    A W3C pointer is the same primitive on every build.
    """
    from selenium.webdriver.common.actions import interaction
    from selenium.webdriver.common.actions.action_builder import ActionBuilder
    from selenium.webdriver.common.actions.pointer_input import PointerInput
    return ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "finger"))


#: How far the wake-up nudge travels. One point: enough to be an event, too
#: little to move the control off the position it is being held at.
_HOLD_NUDGE_PX = 1


def _hold_in_place(finger, at, hold_ms: int) -> None:
    """Wait out ``hold_ms`` at ``at``, then wake the control before lifting.

    A pause alone holds the touch — the driver keeps the pointer down for its
    whole duration — but it emits NOTHING while it waits, and a control that
    arms on movement callbacks judges the release against the state it last saw
    rather than the state it has since reached. A human finger never sits that
    still, so this only arises under synthesis.

    One event is enough, and it is the LAST one that counts: the control needs
    to hear from the finger after its own timer has fired, not throughout. So
    the dwell is one pause and a single one-point move before the lift, rather
    than one move per interval — each step in an action batch costs device time,
    where the pause itself costs none.
    """
    finger.create_pause(hold_ms / 1000.0)
    finger.create_pointer_move(
        duration=0, x=int(at[0]) + _HOLD_NUDGE_PX, y=int(at[1]))


def _composed_move_ms(move_duration_ms) -> int:
    """The travel a composed drag uses: what the caller asked for, or the default.

    A stated travel is honoured rather than overridden — it is the only way to
    slow a control that rejects a fast swipe, and on iOS it was inexpressible
    until this path existed (`dragFromToForDuration` has one duration and it is
    the pickup). Only a degenerate value is refused; see
    ``_COMPOSED_DRAG_MIN_MOVE_MS``.
    """
    if move_duration_ms is None:
        return _COMPOSED_DRAG_MOVE_MS
    return max(int(move_duration_ms), _COMPOSED_DRAG_MIN_MOVE_MS)


def _w3c_drag(driver, start, end, *, pickup_ms, move_ms, hold_ms,
              nudge_while_holding=False) -> None:
    """One finger, five steps, each carrying its own duration.

        down at start → hold (pickup) → travel → hold (at the destination) → lift

    Composed on the input source because a drag has TWO pauses and they mean
    different things. The pickup is what makes a long-press-then-drag recognised
    — press first, then move, the way an app icon is picked up. The hold at the
    destination is what a slide-and-hold control waits for: it watches the finger
    STAY past its threshold, and reads a release on arrival as an abandon however
    far the thumb travelled.

    ``mobile: dragFromToForDuration`` cannot express the second one at all: its
    single duration is the pickup, and it lifts the instant it arrives. Anything
    that needs the finger to linger has to be built step by step, which is what
    the scroll path already does for its own reasons (see ``_w3c_scroll_drag``).

    Durations follow the selenium API they are handed to: moves are milliseconds,
    pauses are seconds.
    """
    builder = _w3c_touch(driver)
    finger = builder.pointer_action.source
    finger.create_pointer_move(duration=0, x=int(start[0]), y=int(start[1]))
    finger.create_pointer_down(button=0)
    if pickup_ms:
        finger.create_pause(float(pickup_ms) / 1000.0)
    finger.create_pointer_move(
        duration=int(move_ms), x=int(end[0]), y=int(end[1]))
    if hold_ms:
        if nudge_while_holding:
            _hold_in_place(finger, end, int(hold_ms))
        else:
            finger.create_pause(float(hold_ms) / 1000.0)
    finger.create_pointer_up(button=0)
    builder.perform()


def _android_tap(driver, x: int, y: int) -> None:
    driver.execute_script("mobile: clickGesture", {"x": int(x), "y": int(y)})


def _android_type_text(driver, text: str) -> None:
    driver.execute_script("mobile: type", {"text": str(text)})


def _android_long_press(driver, x: int, y: int, duration_ms: int) -> None:
    driver.execute_script(
        "mobile: longClickGesture",
        {"x": int(x), "y": int(y), "duration": int(duration_ms)},
    )


#: Fraction of a full scrollGesture that becomes content travel: the script
#: insets its swipe inside the area, so a percent=1.0 gesture moves the content
#: about three quarters of the area's span.
_ANDROID_SCROLL_TRAVEL = 0.75


def _android_scroll_travel() -> float:
    return _ANDROID_SCROLL_TRAVEL


#: Pixel ratio assumed when the session does not report one. The low end of
#: phone densities: a low guess slows the finger, a high one would speed it up.
_ANDROID_FALLBACK_PIXEL_RATIO = 2.0


def _android_pixel_ratio(driver) -> float:
    """The session's pixel ratio (px per dp), as UiAutomator2 reports it in the
    session capabilities, or the fallback when it is absent or unreadable."""
    try:
        ratio = float((getattr(driver, "capabilities", None) or {}).get("pixelRatio"))
    except (TypeError, ValueError):
        return _ANDROID_FALLBACK_PIXEL_RATIO
    return ratio if ratio > 0 else _ANDROID_FALLBACK_PIXEL_RATIO


#: Finger speed of an Android scroll gesture, in dp per second. The driver's
#: own default is 1500 dp/s, a fling-class swipe.
_ANDROID_SCROLL_SPEED_DPS = 200


def _android_scroll_speed(driver) -> int:
    """The finger speed for a scroll gesture in px/s: the dp/s constant scaled
    by the session's pixel ratio, so the same physical speed reaches every
    density. `mobile: scrollGesture` takes `speed` in px/s."""
    return max(1, int(_ANDROID_SCROLL_SPEED_DPS * _android_pixel_ratio(driver)))


def _android_scroll_args(driver, direction: str, percent: float) -> dict:
    return {
        "direction": direction, "percent": float(percent),
        "speed": _android_scroll_speed(driver),
    }


def _android_scroll_area(driver, left, top, width, height, direction: str, percent: float) -> bool:
    return bool(driver.execute_script("mobile: scrollGesture", {
        "left": int(left), "top": int(top), "width": int(width), "height": int(height),
        **_android_scroll_args(driver, direction, percent),
    }))


def _android_scroll_element(driver, element, direction: str, percent: float) -> bool:
    return bool(driver.execute_script("mobile: scrollGesture", {
        "elementId": element.id, **_android_scroll_args(driver, direction, percent),
    }))


def _android_drag(
    driver, start, end, hold_duration_ms, move_duration_ms,
    hold_at_destination_ms=None,
) -> None:
    """`dragGesture` for the ordinary case, a composed drag to hold on arrival.

    The script releases when the travel ends and has no parameter for staying,
    so a caller that needs the finger to linger is served by ``_w3c_drag``.

    Both paths honour ``move_duration_ms`` — the script as its own
    ``moveDuration``, the composed one as the travel step's duration.
    """
    if hold_at_destination_ms is not None:
        _w3c_drag(
            driver, start, end,
            # `dragGesture` presses before it travels whether or not a hold is
            # named; a composed drag has to be told to, or a control that arms
            # on a long press is never picked up.
            pickup_ms=(
                hold_duration_ms if hold_duration_ms is not None
                else _COMPOSED_DRAG_PICKUP_MS
            ),
            move_ms=_composed_move_ms(move_duration_ms),
            hold_ms=hold_at_destination_ms,
        )
        return
    args = {
        "startX": int(start[0]), "startY": int(start[1]),
        "endX": int(end[0]), "endY": int(end[1]),
    }
    if hold_duration_ms is not None:
        args["holdDuration"] = int(hold_duration_ms)
    if move_duration_ms is not None:
        args["moveDuration"] = int(move_duration_ms)
    driver.execute_script("mobile: dragGesture", args)


# ── iOS ──────────────────────────────────────────────────────────────────────

#: Fraction of a rectangle left untouched at each end of a swipe. A gesture that
#: starts on the very edge lands in the system's own edge-swipe zones — back
#: navigation, notification centre, app switcher — and never reaches the app.
_IOS_SWIPE_INSET = 0.05

#: Fraction of a full swipe that becomes content travel. The drag tracks the
#: finger 1:1, so a percent=1.0 swipe moves the content by the box's span less
#: the inset at each end.
_IOS_SCROLL_TRAVEL = 1.0 - 2 * _IOS_SWIPE_INSET


def _ios_scroll_travel() -> float:
    return _IOS_SCROLL_TRAVEL

#: Seconds a synthesized tap holds between down and up. Long enough for the touch
#: to register as a tap rather than be coalesced away, short enough not to read as
#: a long press.
_TAP_HOLD_S = 0.05

#: Seconds a scroll's touch settles before moving — far below iOS's ~0.5s
#: long-press threshold. At or past that threshold, a keyboard key under the
#: touch opens its accent popup (whose release COMMITS the letter — measured
#: as "rohith" becoming "rohithg" mid-scroll) and a text field opens the
#: selection callout. `dragFromToForDuration` cannot make this choice: its one
#: duration IS the press-hold, floored at exactly 0.5s.
_IOS_SCROLL_SETTLE_S = 0.1

#: Milliseconds the scroll's move takes. Slow enough that the system reads a
#: DRAG — content tracks the finger 1:1 and the recorded distance stays exact —
#: rather than a flick, whose momentum travel depends on velocity physics no
#: recording can replay.
_IOS_SCROLL_MOVE_MS = 600


def _ios_swipe_points(left, top, width, height, direction: str, percent: float):
    """Start and end points for a swipe that scrolls `direction` by `percent`.

    Sign convention follows UiAutomator2's, because the recorded action means the
    same thing on both platforms: `direction="down"` means SCROLL DOWN — reveal the
    content below — which the finger performs by moving UP. Getting this backwards
    is invisible in a passing unit test and scrolls every list the wrong way on a
    device.
    """
    left, top, width, height = float(left), float(top), float(width), float(height)
    travel = max(0.0, min(1.0, float(percent))) * (1.0 - 2 * _IOS_SWIPE_INSET)
    cx, cy = left + width / 2, top + height / 2

    if direction in ("down", "up"):
        half = height * travel / 2
        near, far = cy + half, cy - half
        return ((cx, near), (cx, far)) if direction == "down" else ((cx, far), (cx, near))

    half = width * travel / 2
    near, far = cx + half, cx - half
    return ((near, cy), (far, cy)) if direction == "right" else ((far, cy), (near, cy))


def _ios_tap(driver, x: int, y: int) -> None:
    builder = _w3c_touch(driver)
    builder.pointer_action.move_to_location(int(x), int(y)).pointer_down().pause(
        _TAP_HOLD_S).pointer_up()
    builder.perform()


def _ios_type_text(driver, text: str) -> None:
    """Hand the string to whatever holds focus, on either surface.

    Typed at the SESSION, not at an element, and that is the whole point. The
    obvious spelling — `switch_to.active_element.send_keys(...)` — works on a
    native field and fails silently-in-the-wrong-place on a web one, because
    XCUITest only knows about NATIVE focus. With the caret inside a WKWebView it
    answers:

        driver.switch_to.active_element -> NoSuchElementException
                "unable to find an element using '(null)', value '(null)'"
        document.activeElement          -> TEXTAREA name=q ph="Ask Google"

    The page holds the focus and the native tree has no element to name for it,
    so the tap lands correctly in the page and the text then goes somewhere else
    entirely — in practice the app's own URL bar, which is the nearest native
    field. The user sees the caret jump out of the page as it types.

    W3C key actions carry no element, so they go wherever the OS is directing
    keystrokes, which is the same place the on-screen keyboard is typing.
    Verified on a device against both surfaces, with the DOM read back to confirm:

        focus in a WKWebView   ActionChains(driver).send_keys("C")  -> textarea 'ABC'
        focus in a native field  same call                          -> field 'hello'

    `mobile: keys` also reaches both and is NOT used: it is a driver extension
    whose availability varies by xcuitest-driver version, where this is the same
    W3C primitive the tap already uses.
    """
    from selenium.webdriver.common.action_chains import ActionChains

    ActionChains(driver).send_keys(str(text)).perform()


def _ios_long_press(driver, x: int, y: int, duration_ms: int) -> None:
    driver.execute_script(
        "mobile: touchAndHold",
        {"x": int(x), "y": int(y), "duration": float(duration_ms) / 1000.0},
    )


def _ios_scroll_area(driver, left, top, width, height, direction, percent) -> bool:
    """Swipe inside a rectangle. ALWAYS reports that more may remain.

    UiAutomator2's scrollGesture answers "could anything still scroll?"; XCUITest
    has no equivalent, and none of its scroll verbs takes a rectangle either — so
    this is a drag over the given box.

    Returning True is the deliberate choice. `scroll_until` treats False as "the
    list ended" and stops early, so a wrong False abandons a search one scroll in.
    A wrong True only spends the caller's remaining scroll budget before failing
    the way it would have anyway. The bounded loop, not this return value, is what
    guarantees termination on iOS.
    """
    start, end = _ios_swipe_points(left, top, width, height, direction, percent)
    _w3c_scroll_drag(driver, start, end)
    return True


def drag_scroll(driver, start, end, *, move_ms: int | None = None) -> None:
    """A finger scroll from ``start`` to ``end`` on either platform: touch,
    settle below the long-press threshold, drag slowly, lift. The scroll a
    caller aims at a point rather than at a container. ``move_ms`` slows the
    on-glass move below the default so a long drag is tracked, not flung."""
    _w3c_scroll_drag(driver, start, end, move_ms=move_ms)


def _w3c_scroll_drag(driver, start, end, *, move_ms: int | None = None) -> None:
    """One finger: touch, settle briefly, drag slowly, lift.

    Not `mobile: dragFromToForDuration`: its one duration is a press-hold
    floored at 0.5s — iOS's long-press threshold — so it long-pressed
    whatever sat under the start point. A sub-threshold touch that moves is
    a human scroll: a key under it cancels on slide-off, and a field never
    sees a tap. (The drag verb keeps the hold — there it is the pickup.)

    Composed on the input source so each action carries its own duration:
    the positioning hover is instant, only the on-glass move is slow.
    """
    builder = _w3c_touch(driver)
    finger = builder.pointer_action.source
    finger.create_pointer_move(duration=0, x=int(start[0]), y=int(start[1]))
    finger.create_pointer_down(button=0)
    finger.create_pause(_IOS_SCROLL_SETTLE_S)
    finger.create_pointer_move(
        duration=int(move_ms or _IOS_SCROLL_MOVE_MS), x=int(end[0]), y=int(end[1]))
    finger.create_pointer_up(button=0)
    builder.perform()


def _ios_scroll_element(driver, element, direction, percent) -> bool:
    """Scroll a named element by swiping over the box it occupies.

    `mobile: scroll` would take the element directly, but it accepts no distance —
    so `percent` would be silently discarded and a caller asking for a nudge would
    get a full page. Dragging over the element's own rectangle keeps the recorded
    distance meaningful. Same always-True contract, for the same reason.
    """
    rect = element.rect
    start, end = _ios_swipe_points(
        rect["x"], rect["y"], rect["width"], rect["height"], direction, percent)
    _w3c_scroll_drag(driver, start, end)
    return True


def _ios_drag_gesture(
    driver, start, end, hold_duration_ms, move_duration_ms,
    hold_at_destination_ms=None,
) -> None:
    """Every iOS drag is composed, step by step.

    ``mobile: dragFromToForDuration`` served this for a long time and no longer
    does. Three things it cannot do: it lifts the instant it arrives, so a
    slide-and-hold control abandons whatever dwell was asked for; its single
    duration is floored at 0.5 s, so a shorter pickup is inexpressible; and it
    opens with XCTest's own pickup overture — a small move, a hover, then the
    travel — which is visible on screen and belongs to no recording. Composing
    the same drag costs no more device time than the script did.

    The pickup survives the move, because that is what it is for: a drag-and-drop
    is picked up before it travels, the way an icon is. It is simply a pause now
    rather than the only duration on offer.
    """
    _w3c_drag(
        driver, start, end,
        # The composed path keeps the script call's own default hold, so moving
        # between the two changes what was ASKED for and nothing else.
        pickup_ms=(
            hold_duration_ms if hold_duration_ms is not None
            else _COMPOSED_DRAG_PICKUP_MS
        ),
        move_ms=_composed_move_ms(move_duration_ms),
        hold_ms=hold_at_destination_ms,
        # A motionless finger is invisible to a SwiftUI drag recogniser: the hold
        # timer arms, but the closure that reads it only runs on a movement event,
        # so the dwell expires unseen and the release reads as an abandon. One 1px
        # move just before lifting delivers that event.
        nudge_while_holding=True,
    )


def _ios_click_target(driver, element):
    """SwiftUI publishes a Toggle as ONE switch element spanning the whole row,
    and only the small capsule inside that row answers taps — `element.click()`
    lands on the element's center, which is the label, and nothing happens.
    The capsule is a nested (non-accessible) switch child; clicking it instead
    taps the control wherever the layout put it. Anything that is not a switch,
    and a switch with no nested child (already capsule-sized), is clicked as
    found."""
    if element.tag_name != "XCUIElementTypeSwitch":
        return element
    from appium.webdriver.common.appiumby import AppiumBy

    nested = element.find_elements(AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeSwitch")
    return nested[0] if nested else element


def _android_click_target(driver, element):
    """A switch node's bounds are the capsule itself, so its center is tappable."""
    return element


#: Containers UiAutomator reports as scrollable, in document order.
_ANDROID_SCROLLABLE_QUERY = "new UiSelector().scrollable(true)"


def _android_scrollable_containers(driver) -> list:
    from appium.webdriver.common.appiumby import AppiumBy

    return driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, _ANDROID_SCROLLABLE_QUERY)


_adapters.register("gesture", {
    "android": {
        "tap": _android_tap,
        "type_text": _android_type_text,
        "long_press": _android_long_press,
        "scroll_area": _android_scroll_area,
        "scroll_element": _android_scroll_element,
        "scroll_travel": _android_scroll_travel,
        "scrollable_containers": _android_scrollable_containers,
        "drag": _android_drag,
        "click_target": _android_click_target,
    },
    "ios": {
        "tap": _ios_tap,
        "type_text": _ios_type_text,
        "long_press": _ios_long_press,
        "scroll_area": _ios_scroll_area,
        "scroll_element": _ios_scroll_element,
        "scroll_travel": _ios_scroll_travel,
        "drag": _ios_drag_gesture,
        "click_target": _ios_click_target,
    },
})


def click_target(driver, element):
    """The element a click should actually land on, for the configured platform."""
    return _adapters.adapter("gesture", "click_target", "element click")(driver, element)


def tap(driver, x: int, y: int) -> None:
    _adapters.adapter("gesture", "tap", "coordinate tap")(driver, x, y)


def type_text(driver, text: str) -> None:
    """Type into the focused field through the platform gesture seam."""
    _adapters.adapter("gesture", "type_text", "coordinate text entry")(driver, text)


def long_press(driver, x: int, y: int, duration_ms: int = DEFAULT_LONG_PRESS_MS) -> None:
    _adapters.adapter("gesture", "long_press", "coordinate long press")(
        driver, x, y, duration_ms
    )


def scroll_area(driver, left, top, width, height, direction: str, percent: float) -> bool:
    """Swipe inside a rectangle. Returns whether anything could still be scrolled.

    For a screen-level scroll, where there is no element to name.
    """
    return _adapters.adapter("gesture", "scroll_area", "scroll gesture")(
        driver, left, top, width, height, direction, percent
    )


def scrollable_containers(driver) -> list:
    """Every container on screen the platform reports as scrollable.

    For a screen-level scroll, which has no element to name and must work out
    what a gesture at a point would reach.
    """
    return _adapters.adapter(
        "gesture", "scrollable_containers", "scrollable container lookup",
    )(driver)


def scroll_travel() -> float:
    """Fraction of a percent=1.0 scroll gesture that becomes content travel.

    The factor a distance in pixels is divided by to become the percent one
    gesture is asked for, on the configured platform.
    """
    return _adapters.adapter("gesture", "scroll_travel", "scroll gesture")()


def scroll_element(driver, element, direction: str, percent: float) -> bool:
    """Scroll an element. Returns whether anything could still be scrolled.

    Naming the element is not the same request as passing the rectangle it
    occupies: a rectangle only says where to swipe, and a container that does not
    take a synthesized touch at those coordinates stays put and truthfully
    reports that nothing scrolled.
    """
    return _adapters.adapter("gesture", "scroll_element", "scroll gesture")(
        driver, element, direction, percent
    )


def drag_gesture(
    driver, start, end, *, hold_duration_ms=None, move_duration_ms=None,
    hold_at_destination_ms=None,
) -> None:
    """Press-hold-move-release between two points.

    ``hold_duration_ms`` holds BEFORE the move — the pickup a long-press-then-drag
    needs. ``hold_at_destination_ms`` holds AFTER it, before the finger lifts,
    which is what a slide-and-hold control waits for: it watches the thumb STAY
    past its threshold and reads a release on arrival as an abandon however far
    the thumb travelled. Two pauses, two different meanings; neither substitutes
    for the other.
    """
    _adapters.adapter("gesture", "drag", "drag gesture")(
        driver, start, end, hold_duration_ms, move_duration_ms,
        hold_at_destination_ms,
    )


def element_center(element) -> tuple[int, int]:
    rect = element.rect
    return (
        int(rect["x"]) + int(rect["width"]) // 2,
        int(rect["y"]) + int(rect["height"]) // 2,
    )


def resolve_click_modifier(modifier):
    """Resolve `{{var}}` tokens inside a click_modifier dict at EXECUTION time.

    The AST carries modifier dict interiors as plain strings — resolution is
    deliberately the binding's job, so a modifier can reference a variable produced
    earlier in the same test.
    """
    if not modifier:
        return None
    resolved = {}
    for key, value in modifier.items():
        resolved[key] = var(value) if isinstance(value, str) else value
    return resolved


@dataclass(frozen=True)
class ClickModifier:
    """One recorded click gesture, in the single vocabulary the primitives take.

    duration_ms stays None when nothing was recorded, so the long-press default is
    applied at the point of use rather than being baked in here — an explicitly
    recorded 0 has to stay 0 (see `_duration_ms`).
    """

    gesture: str
    duration_ms: Optional[int] = None
    frequency: int = 1
    gap_s: float = DEFAULT_MULTI_CLICK_GAP_S


def _duration_ms(modifier: dict) -> Optional[int]:
    """The long-press duration in milliseconds, from either recorded spelling.

    Both keys are read with `is None`, not for truthiness, so a recorded 0 (or "0")
    stays an explicit zero-millisecond duration rather than falling back to the 800ms
    default.
    """
    if modifier.get("duration_ms") is not None:
        return int(float(modifier["duration_ms"]))
    if modifier.get("duration") is not None:
        # The legacy web spelling carries SECONDS; the mobile recorder carries
        # milliseconds. Converting here is the whole reason both are read in one place.
        return int(float(modifier["duration"]) * 1000)
    return None


def _frequency(modifier: dict) -> int:
    """How many taps a multi-click makes, from either recorded spelling."""
    raw = modifier.get("frequency")
    if raw is None:
        raw = modifier.get("count")
    return int(float(raw or 1) or 1)


def _gap_s(modifier: dict) -> float:
    """The pause between multi-click taps in seconds, from either recorded spelling."""
    if modifier.get("gap_ms") is not None:
        return max(0.0, float(modifier["gap_ms"]) / 1000.0)
    if modifier.get("gap") is not None:
        return max(0.0, float(modifier["gap"]))
    return DEFAULT_MULTI_CLICK_GAP_S


def normalize_click_modifier(modifier) -> Optional[ClickModifier]:
    """Resolve `{{var}}` tokens, then map a recorded modifier onto one vocabulary.

    TWO PRODUCERS write this dict and they do not agree on a single key name:

      recorded (mobile AST/cgf)  {"gesture": "long_press",  "duration_ms": 1500}
                                 {"gesture": "multi_click", "count"|"frequency": n,
                                  "gap_ms": ms}
      legacy web (V3 gesture IR) {"kind":    "long_press",  "duration": <seconds>}
                                 {"kind":    "multi_click", "frequency": n,
                                  "gap": <seconds>}

    Both spellings are accepted here, at the binding boundary, so nothing downstream
    has to know there are two.

    Returns None when there is no modifier to apply.
    """
    modifier = resolve_click_modifier(modifier)
    if not modifier:
        return None

    gesture = str(modifier.get("gesture") or modifier.get("kind") or "").lower()
    if gesture not in CLICK_GESTURES:
        raise ValueError(
            f"unknown click_modifier gesture {gesture or None!r}; "
            f"expected one of {list(CLICK_GESTURES)} under key 'gesture' (recorded) "
            f"or 'kind' (legacy)"
        )

    return ClickModifier(
        gesture=gesture,
        duration_ms=_duration_ms(modifier),
        frequency=_frequency(modifier),
        gap_s=_gap_s(modifier),
    )


def apply_click_modifier(driver, element, modifier) -> bool:
    """Run a modified click on an element. Returns False when there is no modifier to
    apply and the caller should fall through to a plain tap."""
    x, y = element_center(element)
    return apply_click_modifier_at(driver, x, y, modifier)


def apply_click_modifier_at(driver, x: int, y: int, modifier) -> bool:
    """Run a modified click at a live point.

    This is shared by web, legacy-coordinate and vision-grounded actions. Keeping
    the modifier handling here prevents those point-backed paths from silently
    turning a recorded double-click into one tap.
    """
    resolved = normalize_click_modifier(modifier)
    if resolved is None:
        return False

    if resolved.gesture == "long_press":
        long_press(
            driver, x, y,
            DEFAULT_LONG_PRESS_MS if resolved.duration_ms is None else resolved.duration_ms,
        )
        return True

    if resolved.frequency <= 1:
        # A single-click "multi click" is a plain tap; running the multi-click path
        # would add a pointless inter-click delay.
        return False

    import time

    for index in range(resolved.frequency):
        tap(driver, x, y)
        if index < resolved.frequency - 1:
            time.sleep(resolved.gap_s)
    return True
