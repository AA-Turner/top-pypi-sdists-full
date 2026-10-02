"""type / search / clear — text entry verbs.

All three share the focus-then-act shape: a mobile field must be focused before it
accepts keys, so the verb taps it first unless the recording says otherwise.

Two independent things decide whether the field is cleared:

- `clear_first` is recorded ON THE ACTION — it describes the field ("this is a
  replace, not an append").
- `multiple_inputs` / `manual_interaction_tag` are recorded about the SEQUENCE —
  another step already put text in this field, or the author typed into it by
  hand. Either one overrides `clear_first`, because clearing would destroy what
  the previous step just entered.

`delay_ms` replays a recorded per-keystroke delay, for fields whose autocomplete
or input mask drops characters delivered as one blob.
"""
import logging
import time

from selenium.common.exceptions import NoSuchElementException

from testmu_appium._action_engine import _ActionSpec, _run_action
from testmu_appium._errors import ElementBlocked, ElementNotFound
from testmu_appium._helpers.gesture import tap, type_text
from testmu_appium._helpers.keyevent import keyevent
from testmu_appium._timing import action_phase as _action_phase, count as _timing_count
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

DEFAULT_SUBMIT_KEY = "Enter"

#: How long the coordinate clear waits for the tap to focus a field, and how
#: often it re-reads while waiting.
_FOCUS_POLL_BUDGET_S = 2.0
_FOCUS_POLL_INTERVAL_S = 0.2


def _send(element, text: str, delay_ms: int) -> None:
    """Send the text, one character at a time when a keystroke delay was recorded."""
    if delay_ms <= 0:
        _timing_count("send_keys_commands")
        with _action_phase("send_keys"):
            element.send_keys(text)
        return
    for index, character in enumerate(text):
        _timing_count("send_keys_commands")
        with _action_phase("send_keys"):
            element.send_keys(character)
        if index < len(text) - 1:
            with _action_phase("typing_delay"):
                time.sleep(delay_ms / 1000)


def _focus_and_type(element, ctx) -> bool:
    """Focus the field, empty it when asked, then send the text.

    The click comes first: clearing is destructive, and a field that is not
    focused is not necessarily the one the keys will reach.
    """
    text = var(ctx.get("text") or "")
    _timing_count("focus_commands")
    with _action_phase("focus"):
        element.click()
    if ctx.get("clear_first", True):
        _timing_count("clear_commands")
        with _action_phase("clear"):
            element.clear()
    _send(element, text, int(ctx.get("delay_ms", 0) or 0))
    return True


def _type_runner(element, ctx):
    return _focus_and_type(element, ctx)


def _search_runner(element, ctx):
    """Type, then submit with a real key event.

    Android needs the key event: sending "\\n" through send_keys inserts a newline
    into the field instead of submitting.
    """
    _focus_and_type(element, ctx)
    _timing_count("submit_commands")
    with _action_phase("submit"):
        keyevent(ctx["driver"], ctx.get("submit_key") or DEFAULT_SUBMIT_KEY)
    return True


def _clear_runner(element, ctx):
    _timing_count("focus_commands")
    with _action_phase("focus"):
        element.click()
    _timing_count("clear_commands")
    with _action_phase("clear"):
        element.clear()
    return True


def _clear_vision_runner(driver, x, y, ctx):
    """Clear only after vision has freshly resolved the intended field."""
    _timing_count("focus_commands")
    with _action_phase("focus"):
        tap(driver, x, y)
    _clear_at_point(driver, ctx.get("description", ""))
    return True


def _clear_at_point(driver, description: str = "") -> None:
    """Clear the field that the tap just focused.

    There is no element handle on this path — the coordinate fallback runs because the
    locator did not resolve — so the field is reached through the focused element.

    Focus can arrive a beat after the tap, so the read is polled rather than taken
    once. When the budget runs out with nothing focused, the tap opened no text
    field: that raises, because the `mobile: type` that follows would otherwise
    type into the void and report success.

    The legacy runtime's DEL-x50 fallback for a clear that raises is deliberately not
    ported: a field that could not be cleared for any reason would get fifty
    keystrokes sent at whatever now has focus.
    """
    stop_at = time.monotonic() + _FOCUS_POLL_BUDGET_S
    while True:
        try:
            _timing_count("clear_commands")
            with _action_phase("clear"):
                driver.switch_to.active_element.clear()
            return
        except NoSuchElementException as exc:
            if time.monotonic() >= stop_at:
                raise ElementNotFound(
                    description, [],
                    "the tap opened no text field, so there was nothing to clear",
                ) from exc
            with _action_phase("focus_wait"):
                time.sleep(_FOCUS_POLL_INTERVAL_S)


def _without_fragment(href) -> str:
    """A page address with its `#fragment` removed, for navigation compares.

    A fragment change is the SAME page noting its state — Google's search box
    appends `#sbfbu=…` the moment it gains focus — and reading it as "the tap
    navigated" fails a healthy type. A real navigation changes the part before
    the `#`.
    """
    return str(href or "").partition("#")[0]


def _verify_web_focus(driver, x, y, ctx) -> None:
    """Between the focus tap and the keys: is the page ready to receive them?

    A page that redraws on focus can steal the tap's click for whatever now
    occupies the point — measured on Google, where the click landed on a
    trending row, NAVIGATED, and the keys then went to a page that no longer
    existed while the verb reported success. Two answers end the wait:

    - an EDITABLE holds focus → type. Deliberately not "the located node":
      the redraw's replacement field is a different DOM node, and the correct
      one.
    - the page NAVIGATED → raise, naming both locations. No keystroke can be
      right on a page the tap was never aimed at; the caller re-plans from
      what actually happened.

    Anything else gets the focus budget, one re-tap, the budget again — then
    raises rather than typing into the void.
    """
    probe = ctx.get("web_focus_state")
    if probe is None:
        return
    href_before = _without_fragment(ctx.get("web_href_before"))

    def _settled() -> bool:
        stop_at = time.monotonic() + _FOCUS_POLL_BUDGET_S
        while True:
            state = probe()
            if state is None:
                return True  # the page cannot answer; verification stands down
            if _without_fragment(state.get("href")) != href_before:
                raise ElementBlocked(
                    ctx.get("description", "type"),
                    RuntimeError(
                        f"the focus tap navigated the page — {href_before} "
                        f"became {state.get('href')} — so the field this text "
                        f"was meant for is gone; nothing was typed"))
            if state.get("editable"):
                return True
            if time.monotonic() >= stop_at:
                return False
            with _action_phase("focus_wait"):
                time.sleep(_FOCUS_POLL_INTERVAL_S)

    if _settled():
        return
    _log.info("    [web] the tap left no editable focused; tapping (%d, %d) "
              "once more", x, y)
    _timing_count("focus_commands")
    with _action_phase("focus"):
        tap(driver, x, y)
    if not _settled():
        raise ElementBlocked(
            ctx.get("description", "type"),
            RuntimeError(
                "two taps left no editable element focused, so these keys had "
                "nowhere to go; nothing was typed"))


def _type_coord_runner(driver, x, y, ctx):
    # Focus through the PAGE first, where a probe is available: any
    # redraw-on-focus fires now, with no click in flight to steal, and the tap
    # moves to wherever the focused field settled. None keeps today's point.
    prefocus = ctx.get("web_prefocus")
    if prefocus is not None:
        with _action_phase("prefocus"):
            moved = prefocus()
        if moved is not None:
            x, y = moved
        # Re-baseline the navigation check AFTER the prefocus: whatever the
        # page did in response to the script focus (or an unrelated redirect
        # during the settle) must not be blamed on the tap that follows.
        probe = ctx.get("web_focus_state")
        if probe is not None:
            refreshed = probe()
            if refreshed is not None:
                ctx = {**ctx, "web_href_before": refreshed.get("href", "")}
    _timing_count("focus_commands")
    with _action_phase("focus"):
        tap(driver, x, y)
    with _action_phase("focus_verify"):
        _verify_web_focus(driver, x, y, ctx)
    # clear_first describes the FIELD ("this is a replace, not an append"), so it
    # applies just as much when the field was reached by coordinates.
    if ctx.get("clear_first", True):
        _clear_at_point(driver, ctx.get("description", ""))
    _timing_count("send_keys_commands")
    with _action_phase("send_keys"):
        type_text(driver, var(ctx.get("text") or ""))
    return True


def _search_coord_runner(driver, x, y, ctx):
    _type_coord_runner(driver, x, y, ctx)
    _timing_count("submit_commands")
    with _action_phase("submit"):
        keyevent(driver, ctx.get("submit_key") or DEFAULT_SUBMIT_KEY)
    return True


_TYPE_SPEC = _ActionSpec(
    runner=_type_runner, target_mode="element", op_type="type",
    coord_runner=_type_coord_runner, vision_runner=_type_coord_runner,
)
_SEARCH_SPEC = _ActionSpec(
    runner=_search_runner, target_mode="element", op_type="type",
    coord_runner=_search_coord_runner, vision_runner=_search_coord_runner,
)
# clear has no coordinate fallback: a blind tap at a recorded ratio would focus
# whatever is there now and then wipe it.
_CLEAR_SPEC = _ActionSpec(
    runner=_clear_runner, target_mode="element", op_type="type",
    vision_runner=_clear_vision_runner,
)


def _effective_clear(clear_first: bool, multiple_inputs: bool,
                     manual_interaction_tag: bool) -> bool:
    return bool(clear_first) and not (multiple_inputs or manual_interaction_tag)


def _validate_delay(delay_ms) -> int:
    delay = int(delay_ms or 0)
    if delay < 0:
        raise ValueError(f"delay_ms must not be negative, got {delay_ms!r}")
    return delay


def type(driver, *, selectors, text: str, description: str = "",  # noqa: A001
         fallback_coordinates: dict | None = None,
         clear_first: bool = True, delay_ms: int = 0,
         multiple_inputs: bool = False, manual_interaction_tag: bool = False,
         surface: str = "native", frame_path: str = "", grounded_by: str = ""):
    """Focus the element and type `text` into it.

    surface / frame_path: which reader found this element. "native" is the
    accessibility tree, "web" the DOM of a page read over the device's debug
    channel; both act through Appium. frame_path names the frame a web element was
    recorded in, and separates matches that are the same selector in two frames.
    """
    return _run_action(
        driver, _TYPE_SPEC, selectors,
        description=description,
        fallback_coordinates=fallback_coordinates,
        surface=surface,
        frame_path=frame_path,
        grounded_by=grounded_by,
        text=text,
        delay_ms=_validate_delay(delay_ms),
        clear_first=_effective_clear(clear_first, multiple_inputs, manual_interaction_tag),
    )


def search(driver, *, selectors, text: str, description: str = "",
           fallback_coordinates: dict | None = None,
           clear_first: bool = True, submit_key: str = DEFAULT_SUBMIT_KEY,
           delay_ms: int = 0,
           multiple_inputs: bool = False, manual_interaction_tag: bool = False,
           surface: str = "native", frame_path: str = "", grounded_by: str = ""):
    """Type `text` into the element and submit it with `submit_key`.

    surface / frame_path: which reader found this element. "native" is the
    accessibility tree, "web" the DOM of a page read over the device's debug
    channel; both act through Appium. frame_path names the frame a web element was
    recorded in, and separates matches that are the same selector in two frames.
    """
    return _run_action(
        driver, _SEARCH_SPEC, selectors,
        description=description,
        fallback_coordinates=fallback_coordinates,
        surface=surface,
        frame_path=frame_path,
        grounded_by=grounded_by,
        text=text,
        delay_ms=_validate_delay(delay_ms),
        submit_key=submit_key,
        clear_first=_effective_clear(clear_first, multiple_inputs, manual_interaction_tag),
    )


def clear(driver, *, selectors, description: str = "",
          fallback_coordinates: dict | None = None, grounded_by: str = ""):
    """Focus the element and clear its contents."""
    return _run_action(
        driver, _CLEAR_SPEC, selectors,
        description=description,
        fallback_coordinates=fallback_coordinates,
        grounded_by=grounded_by,
    )
