"""Picker execution over the platform-keyed "picker" registry row.

A platform's row entries are zero-arg providers returning immutable picker
mechanics: the mode → runner map, the picker-list resource id, the
widget-class → mode detection table with its default, and the attributes a
wheel's displayed value is read from. A mode listed in ``_DEFERRED_MODES`` is deferred only where its platform row has
no runner for it: ``wheel_column`` is the shape iOS pickers actually take, and the
same name is still unbuilt on Android.
"""

import math
import re
import time
from types import MappingProxyType

from testmu_appium import _config
from testmu_appium._errors import PickerModeNotSupported
from testmu_appium._helpers import _adapters
from testmu_appium._helpers._strategy import compile_picker_options
from testmu_appium._helpers.gesture import drag_gesture, scroll_area

SELECT_MODES = ("auto", "spinner", "number_picker", "slider", "wheel_column",
                "dial", "date_wheels", "stepper", "picker_wheels")

_DEFERRED_MODES = {
    "wheel_column": "wheel-column picker",
    "dial": "clock-face dial picker",
}
_NUMBER_PICKER_MAX_ROUNDS = 40
_NUMBER_PICKER_SCROLL_PERCENT = 0.3

#: How long a stepper's reported value gets to catch up with a tap, and how
#: often it is re-read while waiting.
_STEPPER_SETTLE_S = 1.0
_STEPPER_POLL_S = 0.1

#: How long a spinner's options list gets to render after the opening tap,
#: and how often it is re-read while waiting.
_SPINNER_OPTIONS_SETTLE_S = 5.0
_SPINNER_OPTIONS_POLL_S = 0.15

#: Taps a stepper run may spend reaching its target. UIStepper values move one
#: step per tap, so this is also the largest reachable distance; a target
#: further away than this fails the same bounded way the number picker does.
_STEPPER_MAX_TAPS = 40


def _picker_data(operation: str):
    """One entry's value from the configured platform's picker row provider."""
    return _adapters.adapter("picker", operation, "picker execution")()


def _require_value(target, widget: str) -> str:
    text = target.data_text
    if not text:
        raise ValueError(
            f"select(index=...) is not meaningful for a {widget}: its options are a "
            f"value range, not a list — record value= or label= instead"
        )
    return text


def _detect_mode(element) -> str:
    """Which mode this element wants, read from its widget class.

    The attribute NAME is the platform's, resolved from the row: Android
    publishes the widget class as `class` (with `className` as an alias);
    XCUITest publishes it as `type` and raises on `class` — asking with the
    Android word made every iOS auto-detection silently fall through to the
    default, so no iOS picker runner was ever reached on a device.
    """
    cls = ""
    for attribute in _picker_data("class_attributes"):
        try:
            cls = element.get_attribute(attribute) or ""
        except Exception:  # noqa: BLE001 — an unserved attribute name is a miss
            continue
        if cls:
            break
    for marker, mode in _picker_data("mode_classes"):
        if marker in cls:
            return mode
    return _picker_data("default_mode")


def _displayed_value(element) -> str:
    for attribute in _picker_data("value_attributes"):
        try:
            value = element.get_attribute(attribute)
        except Exception:  # noqa: BLE001
            continue
        if value:
            return str(value).strip()
    return ""


def _as_number(value: str):
    match = re.search(r"-?\d+(?:\.\d+)?", str(value or ""))
    return float(match.group()) if match else None


def _spinner_options(driver, by, value):
    """The opened picker's option rows, re-read while the list renders.

    The options live in a window the opening tap creates, so a read in the
    same instant can land before the draw; an empty read is retried until
    the settle budget expires. A non-empty read is final — ambiguity or a
    missing row is answered from it, never polled away.
    """
    deadline = time.monotonic() + _SPINNER_OPTIONS_SETTLE_S
    options = driver.find_elements(by, value)
    while not options and time.monotonic() < deadline:
        time.sleep(_SPINNER_OPTIONS_POLL_S)
        options = driver.find_elements(by, value)
    return options


def _select_spinner(driver, element, target) -> bool:
    element.click()
    text = target.visible_text
    if not text:
        by, value = compile_picker_options(
            _config.platform(), list_resource_id=_picker_data("list_id")
        )
        options = _spinner_options(driver, by, value)
        if not 0 <= target.index < len(options):
            raise ValueError(
                f"spinner index {target.index} is out of range; the opened picker "
                f"has {len(options)} option(s)"
            )
        options[target.index].click()
        return True

    by, value = compile_picker_options(_config.platform(), text=text)
    options = _spinner_options(driver, by, value)
    if len(options) != 1:
        raise ValueError(
            f"spinner option {text!r} matched {len(options)} entries after "
            f"opening the picker; expected exactly 1"
        )
    options[0].click()
    return True


def _select_number_picker(driver, element, target) -> bool:
    value = _require_value(target, "NumberPicker")
    target_number = _as_number(value)
    rect = element.rect
    area = (int(rect["x"]), int(rect["y"]), int(rect["width"]), int(rect["height"]))

    previous = None
    for _ in range(_NUMBER_PICKER_MAX_ROUNDS):
        current = _displayed_value(element)
        if current == str(value).strip():
            return True
        current_number = _as_number(current)
        if (
            target_number is not None
            and current_number is not None
            and current_number == target_number
        ):
            return True
        if current == previous:
            break
        previous = current
        direction = "down"
        if (
            target_number is not None
            and current_number is not None
            and current_number > target_number
        ):
            direction = "up"
        scroll_area(driver, *area, direction, _NUMBER_PICKER_SCROLL_PERCENT)

    raise ValueError(
        f"NumberPicker did not reach {value!r} within {_NUMBER_PICKER_MAX_ROUNDS} rounds "
        f"(stopped at {_displayed_value(element)!r})"
    )


def _select_slider(driver, element, target) -> bool:
    value = _require_value(target, "slider")
    percent = _as_number(value)
    if percent is None:
        raise ValueError(f"slider value {value!r} is not a percentage")
    if percent > 1:
        percent /= 100.0
    percent = max(0.0, min(1.0, percent))

    rect = element.rect
    x, y = int(rect["x"]), int(rect["y"])
    w, h = int(rect["width"]), int(rect["height"])
    track_y = y + h // 2
    drag_gesture(driver, (x, track_y), (x + int(w * percent), track_y))
    return True


def _constant(value):
    """A zero-arg provider returning one immutable picker-row value."""
    return lambda: value


def _ios_select_wheel(driver, element, target) -> bool:
    """Set a PickerWheel to a value.

    A wheel is not a list of tappable rows — the options are a spun value, and
    XCUITest sets one by assigning to the element rather than by finding a row.
    `select(index=...)` therefore has no meaning here, which `_require_value`
    says in those words.
    """
    element.send_keys(_require_value(target, "PickerWheel"))
    return True


def _ios_select_picker_wheels(driver, element, target) -> bool:
    """Set a Picker through the wheel(s) it contains.

    The Picker is the NAMED shell — its identifier names the control, so
    recorded selectors land here — while the wheel child's own name is whatever
    row is currently selected. One wheel takes the lone-wheel assignment;
    several take one value per wheel exactly as a DatePicker does; none means
    this Picker is not showing wheels, and the tap-then-choose flow is what
    remains.
    """
    from appium.webdriver.common.appiumby import AppiumBy  # noqa: PLC0415

    wheels = element.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypePickerWheel")
    if len(wheels) == 1:
        return _ios_select_wheel(driver, wheels[0], target)
    if wheels:
        return _ios_select_date_wheels(driver, element, target)
    return _select_spinner(driver, element, target)


def _ios_stepper_buttons(element):
    """A stepper's (decrement, increment) child buttons.

    Labels first: UIKit names the two children "Decrement"/"Increment" (the
    system accessibility labels), and the match is a case-insensitive substring
    so a localized build that KEEPS the English identifiers still resolves.
    Geometry second: a stepper always renders decrement left of increment in
    LTR, so when the labels are localized away the x-order still says which is
    which.
    """
    from appium.webdriver.common.appiumby import AppiumBy  # noqa: PLC0415

    buttons = element.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeButton")
    if len(buttons) < 2:
        raise RuntimeError(
            f"the stepper exposes {len(buttons)} button child(ren); "
            "expected its decrement and increment pair")

    def _label(button):
        try:
            return str(button.get_attribute("name") or "").lower()
        except Exception:  # noqa: BLE001 — an unreadable label falls to geometry
            return ""

    decrement = next((b for b in buttons if "decrement" in _label(b)), None)
    increment = next((b for b in buttons if "increment" in _label(b)), None)
    if decrement is not None and increment is not None:
        return decrement, increment
    ordered = sorted(buttons, key=lambda b: int(b.rect["x"]))
    return ordered[0], ordered[-1]


def _ios_select_stepper(driver, element, target) -> bool:
    """Walk a stepper to its target by tapping its own buttons.

    The step size is the control's secret — 1 for a quantity, 0.5 for a rating —
    so nothing is computed from it: tap, re-read, repeat, exactly as a person
    does. Every iteration is verified against the element's own `value`, and a
    tap that changes nothing is the control saying no (its min or max), reported
    as that rather than looping the budget out against a wall.
    """
    wanted = _as_number(_require_value(target, "Stepper"))
    if wanted is None:
        raise ValueError(
            f"stepper value {target.data_text!r} is not a number")

    def _current() -> float:
        raw = element.get_attribute("value")
        number = _as_number(raw)
        if number is None:
            raise RuntimeError(
                f"the stepper's value reads {raw!r}, which is not a number "
                "this run can walk toward a target")
        return number

    decrement, increment = _ios_stepper_buttons(element)
    for _ in range(_STEPPER_MAX_TAPS):
        current = _current()
        if math.isclose(current, wanted, rel_tol=0.0, abs_tol=1e-9):
            return True
        (increment if wanted > current else decrement).click()
        # The accessibility value can lag the tap by a refresh; conclude "the
        # control refused" only after the report has had a moment to change,
        # or a working stepper reads as stuck at its limit.
        stop_at = time.monotonic() + _STEPPER_SETTLE_S
        while (math.isclose(_current(), current, rel_tol=0.0, abs_tol=1e-9)
               and time.monotonic() < stop_at):
            time.sleep(_STEPPER_POLL_S)
        if math.isclose(_current(), current, rel_tol=0.0, abs_tol=1e-9):
            raise RuntimeError(
                f"the stepper stopped at {current:g} on the way to {wanted:g}; "
                "a tap changed nothing, which is the control's own limit")
    raise RuntimeError(
        f"the stepper did not reach {wanted:g} within {_STEPPER_MAX_TAPS} taps")


def _ios_select_date_wheels(driver, element, target) -> bool:
    """Set a wheels-style date picker, one value per wheel, in on-screen order.

    A DatePicker is a COMPOSITE: each column is its own PickerWheel child, and
    each is set with the same assignment a lone wheel gets. The recorded value
    carries one part per wheel, ``|``-separated — "March|15|2025" for a
    month/day/year picker — because a date's own punctuation is ambiguous and
    the wheels' order is what the screen shows.

    The COMPACT style (iOS 14's default) renders a calendar, not wheels, and
    refuses here by name: tapping calendar cells is ordinary element work the
    agent can already do, not a wheel assignment to half-imitate.
    """
    from appium.webdriver.common.appiumby import AppiumBy  # noqa: PLC0415

    wheels = element.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypePickerWheel")
    if not wheels:
        raise PickerModeNotSupported(
            "date_wheels",
            "compact-style date picker: it renders a calendar, not wheels — "
            "tap its date cells as ordinary elements instead")

    value = _require_value(target, "DatePicker")
    parts = [part.strip() for part in str(value).split("|")]
    if len(parts) != len(wheels):
        raise ValueError(
            f"the date picker shows {len(wheels)} wheel(s) and the value "
            f"carries {len(parts)} part(s); record one value per wheel in "
            f"on-screen order, '|'-separated — e.g. 'March|15|2025'")
    for wheel, part in zip(wheels, parts):
        wheel.send_keys(part)
    return True


def _ios_select_slider(driver, element, target) -> bool:
    """Set a slider to a fraction of its travel.

    XCUITest takes the normalized position directly, so unlike Android's row this
    needs no drag across the track — and cannot miss it. The recorded value may be
    a percentage or a fraction; both normalize to 0..1 as they do on Android.
    """
    value = _require_value(target, "slider")
    percent = _as_number(value)
    if percent is None:
        raise ValueError(f"slider value {value!r} is not a percentage")
    if percent > 1:
        percent /= 100.0
    element.send_keys(str(max(0.0, min(1.0, percent))))
    return True


_adapters.register("picker", {
    "android": {
        "modes": _constant(MappingProxyType({
            "spinner": _select_spinner,
            "number_picker": _select_number_picker,
            "slider": _select_slider,
        })),
        "list_id": _constant("android:id/select_dialog_listview"),
        "mode_classes": _constant((
            ("NumberPicker", "number_picker"),
            ("SeekBar", "slider"),
            ("Slider", "slider"),
        )),
        "default_mode": _constant("spinner"),
        "value_attributes": _constant(("text", "content-desc")),
        "class_attributes": _constant(("class", "className")),
    },
    "ios": {
        # `spinner` is shared outright: iOS's tap-then-choose sheet has the same
        # shape as an Android dialog, and the option lookup underneath it is
        # already platform-keyed in _strategy.
        "modes": _constant(MappingProxyType({
            "spinner": _select_spinner,
            "wheel_column": _ios_select_wheel,
            "slider": _ios_select_slider,
            "date_wheels": _ios_select_date_wheels,
            "stepper": _ios_select_stepper,
            "picker_wheels": _ios_select_picker_wheels,
        })),
        # No resource ids on iOS. The container is named by TYPE, which the iOS
        # picker-option compiler turns into a class chain.
        "list_id": _constant("XCUIElementTypeSheet"),
        "mode_classes": _constant((
            ("PickerWheel", "wheel_column"),
            # Both classified to modes the runners row does NOT serve, so they
            # refuse by name (see _DEFERRED_MODES) instead of half-running:
            # one value at a multi-wheel composite, or a 0..1 coordinate at a
            # control that increments.
            ("DatePicker", "date_wheels"),
            ("Slider", "slider"),
            ("Stepper", "stepper"),
            # LAST on purpose: matching is substring, and "Picker" is inside
            # both "PickerWheel" and "DatePicker" — those must win first.
            ("Picker", "picker_wheels"),
        )),
        "default_mode": _constant("spinner"),
        # A wheel's current selection is its `value`; `label` names the control.
        "value_attributes": _constant(("value", "label")),
        # XCUITest publishes the widget class as `type` and RAISES on `class`.
        "class_attributes": _constant(("type",)),
    },
})


def select_picker(driver, element, target, mode: str) -> bool:
    """Execute one picker interaction through the platform row's mode runners,
    resolving the row before any mechanics run."""
    runners = _picker_data("modes")
    mode = mode or "auto"
    if mode in _DEFERRED_MODES and mode not in runners:
        # Deferred BY PLATFORM, not globally: a wheel column is the ordinary iOS
        # picker and still unbuilt on Android, so the row decides, not this list.
        raise PickerModeNotSupported(mode, _DEFERRED_MODES[mode])
    if mode not in SELECT_MODES:
        raise ValueError(f"unknown select mode {mode!r}; expected one of {list(SELECT_MODES)}")
    if mode == "auto":
        mode = _detect_mode(element)
    if mode not in runners:
        # Whatever the reason — deferred everywhere, or served only by the
        # other platform's row (number_picker on iOS, date_wheels on Android)
        # — a mode this row cannot run refuses BY NAME, never as a KeyError.
        raise PickerModeNotSupported(
            mode, _DEFERRED_MODES.get(mode, "not served on this platform"))
    return runners[mode](driver, element, target)
