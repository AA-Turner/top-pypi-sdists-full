"""V3 click-gesture validation + executors for the selenium-python binding.

Reproduces V2 click-modifier semantics — gestures
long_press / multi_click / right_click. STRICTLY orthogonal to keyboard `modifiers`
(held only by right_click during context_click; never carried inside click_modifier).
"""
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.keys import Keys

from testmu_selenium._helpers.click import _MODIFIER_KEY_MAP

# Bounds mirror the V2 source exactly.
_LONG_PRESS_MIN = 0.1
_LONG_PRESS_MAX = 30
_MULTI_CLICK_MIN = 2
_MULTI_CLICK_MAX = 20
# Hidden buffers (V2 parity). The +0.1s long-press buffer is applied AFTER
# validation so a real hold can reach 30.1s; gap defaults to 0.1s.
_LONG_PRESS_BUFFER = 0.1
_DEFAULT_GAP = 0.1


def validate_click_modifier(click_modifier):
    """Normalize + bounds-check a click_modifier dict (V2 source).

    Operates on the ALREADY-RESOLVED scalar (duration/frequency). Resolving a
    data-driven `variables` carrier is the job of the public
    resolve_click_modifier_variables, which every caller runs FIRST — this
    function never touches `variables`.

    Returns a normalized dict, or None when the gesture collapses to a plain
    click (multi_click frequency==1). Raises ValueError on out-of-bounds /
    malformed input (incl. a missing required scalar) — an authoring/generation
    error, surfaced loudly (uncaught).
    """
    if not click_modifier:
        return None
    click_modifier = dict(click_modifier)
    kind = click_modifier.get("kind")

    if kind == "long_press":
        duration = click_modifier.get("duration")
        if duration is None:
            raise ValueError("long_press requires a 'duration' scalar")
        duration = float(duration)
        if not (_LONG_PRESS_MIN <= duration <= _LONG_PRESS_MAX):
            raise ValueError(
                f"long_press duration {duration} out of bounds "
                f"[{_LONG_PRESS_MIN}, {_LONG_PRESS_MAX}]"
            )
        click_modifier["duration"] = duration
        return click_modifier

    if kind == "multi_click":
        frequency = click_modifier.get("frequency")
        if frequency is None:
            raise ValueError("multi_click requires a 'frequency' scalar")
        if isinstance(frequency, bool):
            raise ValueError(f"multi_click frequency must be a whole number, got {frequency!r}")
        if isinstance(frequency, str):
            frequency = float(frequency)
        if isinstance(frequency, float):
            if not frequency.is_integer():
                raise ValueError(f"multi_click frequency must be a whole number, got {frequency!r}")
            frequency = int(frequency)
        if not isinstance(frequency, int):
            raise ValueError(f"multi_click frequency must be a whole number, got {frequency!r}")
        if frequency == 1:
            return None  # collapse to plain click
        if not (_MULTI_CLICK_MIN <= frequency <= _MULTI_CLICK_MAX):
            raise ValueError(
                f"multi_click frequency {frequency} out of bounds "
                f"[{_MULTI_CLICK_MIN}, {_MULTI_CLICK_MAX}]"
            )
        click_modifier["frequency"] = frequency
        return click_modifier

    if kind == "right_click":
        if "duration" in click_modifier or "frequency" in click_modifier:
            raise ValueError("right_click does not accept duration/frequency")
        return click_modifier

    raise ValueError(f"unknown click_modifier kind: {kind!r}")


def do_long_press(element, driver, duration, modifiers=None):
    """Press-and-hold then release (V2 _do_long_press). The +0.1s buffer is
    applied here, post-validation, so a real hold can reach 30.1s. long_press
    does not consume keyboard modifiers (orthogonal; only right_click holds them)."""
    ActionChains(driver).click_and_hold(element).pause(
        duration + _LONG_PRESS_BUFFER
    ).release(element).perform()
    return True


def do_multi_click(element, driver, frequency, gap=_DEFAULT_GAP, modifiers=None):
    """frequency==2 -> native double_click; frequency>2 -> loop of single clicks
    spaced by `gap` (V2 multi_click). gap applies BETWEEN clicks, not after last."""
    if frequency == 2:
        ActionChains(driver).double_click(element).perform()
        return True
    for i in range(frequency):
        ActionChains(driver).click(element).perform()
        if i < frequency - 1:
            time.sleep(gap)
    return True


def do_right_click(element, driver, modifiers=None):
    """context_click, holding any keyboard `modifiers` across it (LIFO release).
    Meta aliases to CONTROL for macOS via _MODIFIER_KEY_MAP."""
    mod_attrs = [_MODIFIER_KEY_MAP.get(m, m.upper()) for m in (modifiers or [])]
    chain = ActionChains(driver)
    for attr in mod_attrs:
        chain = chain.key_down(getattr(Keys, attr))
    chain = chain.context_click(element)
    for attr in reversed(mod_attrs):
        chain = chain.key_up(getattr(Keys, attr))
    chain.perform()
    return True


def dispatch_gesture(element, driver, click_modifier, modifiers=None):
    """Route an ALREADY-VALIDATED click_modifier dict to its executor.

    `modifiers` (keyboard) are held only by right_click — orthogonal at every hop.
    Caller is responsible for validate_click_modifier (None => plain click, no
    gesture)."""
    kind = click_modifier["kind"]
    if kind == "long_press":
        return do_long_press(element, driver, click_modifier["duration"], modifiers)
    if kind == "multi_click":
        gap = click_modifier.get("duration", _DEFAULT_GAP)
        return do_multi_click(element, driver, click_modifier["frequency"], gap, modifiers)
    if kind == "right_click":
        return do_right_click(element, driver, modifiers)
    raise ValueError(f"unknown click_modifier kind: {kind!r}")


def do_gesture_at_coordinate(driver, x, y, click_modifier, modifiers=None):
    """Coordinate-tier gesture (canvas / no-DOM visual target). Real pointer
    actions via ActionBuilder at the resolved viewport pixel coords — mirrors the
    plain coord click in _click_coord_runner.

    FULL held-keys-coord support: the right_click branch holds any keyboard
    `modifiers` (Shift/Control/Alt/Meta; Meta -> CONTROL via _MODIFIER_KEY_MAP)
    across the context_click, mirroring the element-path do_right_click and the
    Java coord executor. Held keys ride right_click only (spec §2); long_press /
    multi_click never receive them.

    Keyed right_click is driven through ActionChains, NOT raw ActionBuilder: raw
    ActionBuilder does NOT pad idle device ticks, so a key_up queued straight
    after context_click lands on the SAME tick as the button-down — the modifier
    releases before the right-click fires. ActionChains pads every tick, so key_up
    lands strictly after the pointer-up and the key is held across the whole
    context_click (single manual key_action.pause covers the direct pointer move).

    Expects an ALREADY-VALIDATED dict (None => plain click handled by the caller)."""
    kind = click_modifier["kind"]

    if kind == "right_click":
        mod_attrs = [_MODIFIER_KEY_MAP.get(m, m.upper()) for m in (modifiers or [])]
        if mod_attrs:
            # Single atomic ActionChains perform — pointer location is unambiguous
            # and every tick is padded (see docstring). LIFO key release.
            chain = ActionChains(driver)
            chain.w3c_actions.pointer_action.move_to_location(x, y)
            chain.w3c_actions.key_action.pause()  # pad the (un-padded) move tick
            for attr in mod_attrs:
                chain = chain.key_down(getattr(Keys, attr))
            chain = chain.context_click()
            for attr in reversed(mod_attrs):
                chain = chain.key_up(getattr(Keys, attr))
            chain.perform()
            return True

    ab = ActionBuilder(driver)
    ab.pointer_action.move_to_location(x, y)
    if kind == "long_press":
        ab.pointer_action.click_and_hold()
        ab.pointer_action.pause(click_modifier["duration"] + _LONG_PRESS_BUFFER)
        ab.pointer_action.release()
    elif kind == "multi_click":
        frequency = click_modifier["frequency"]
        if frequency == 2:
            ab.pointer_action.double_click()
        else:
            gap = click_modifier.get("duration", _DEFAULT_GAP)
            for i in range(frequency):
                ab.pointer_action.click()
                if i < frequency - 1:
                    ab.pointer_action.pause(gap)
    elif kind == "right_click":
        # No held modifiers — plain pointer context_click (no key device).
        ab.pointer_action.context_click()
    else:
        raise ValueError(f"unknown click_modifier kind: {kind!r}")
    ab.perform()
    return True


def resolve_click_modifier_variables(click_modifier):
    """Resolve data-driven gesture params against the binding variable store.

    A data-driven long_press/multi_click carries the raw {{var}}/${param} text
    under click_modifier['variables'] ({'frequency'|'duration': template}); the
    scalar field holds a Layer-1 placeholder. Resolve each template via var() —
    the V3 export resolver, whose store is populated by the generated set_var
    calls — write the result back onto frequency/duration, and drop the carrier
    so the downstream validator/executor sees a plain resolved dict. Call this
    BEFORE validate_click_modifier in the gesture dispatch. Mirrors the V2
    source _handle_click_modifier.
    """
    from testmu_selenium._vars import var
    if not isinstance(click_modifier, dict):
        return click_modifier
    variables = click_modifier.get('variables')
    if isinstance(variables, dict) and variables:
        for field, template in variables.items():
            resolved = var(template)
            if field == 'frequency':
                click_modifier['frequency'] = resolved
            elif field == 'duration':
                click_modifier['duration'] = resolved
        click_modifier.pop('variables', None)
    return click_modifier
