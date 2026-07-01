"""High-level type action — find element, type value, heal on failure."""
# noqa: A001 — `type` deliberately shadows builtin; only used as
# testmu_selenium.type via module-attr access.

from selenium.webdriver.common.actions.action_builder import ActionBuilder

from testmu_selenium._action_engine import _ActionSpec, _run_action


def _type_runner(element, ctx):
    return element.input_value(
        ctx['driver'],
        ctx['value'],
        ctx.get('strategy', 'se_js_ac'),
        ctx.get('timeout', 10),
        ctx.get('coords'),
        ctx.get('multiple_inputs', False),
        ctx.get('manual_interaction_tag', ''),
    )


# Coordinate-tier fallback. Heal cascade exhausted every selector tier and
# returned viewport pixel coords (e.g. a canvas/vision target that has no DOM
# node). Perform a REAL pointer click at those coords, then deliver the value
# through the keyboard input source.
#
# Why a real click and not elementFromPoint(x, y).focus(): a pure <canvas> is not
# focusable, so .focus() is a no-op AND the canvas' own click handler never fires,
# leaving its internal focus/active state unset — keystrokes are then silently
# dropped (works in authoring/playground only because they replay at the same
# viewport; breaks in exported code at a different viewport). A real pointer click
# fires the handler exactly as the V2 visual-fallback path and _clear_coord_runner
# do. Strategy/multiple_inputs/manual_interaction_tag are not honoured on the
# coord fallback — visual-location typing only.
def _type_coord_runner(driver, x, y, ctx):
    click = ActionBuilder(driver)
    click.pointer_action.move_to_location(x, y)
    click.pointer_action.click()
    click.perform()

    keyboard = ActionBuilder(driver)
    keyboard.key_action.send_keys(ctx['value'])
    keyboard.perform()
    return True


# Recoverable set inherits the engine default. This now also covers
# ElementClickInterceptedException — a strict superset of prior behavior:
# if a type's underlying click is intercepted, retry+heal will fire.
_TYPE_SPEC = _ActionSpec(runner=_type_runner, coord_runner=_type_coord_runner)


def type(driver, selector, value, *, strategy='se_js_ac', timeout=10,  # noqa: A001
         coords=None, multiple_inputs=False, manual_interaction_tag='',
         description='', tiers=None, autoheal=True,
         max_attempts=4, retry_delay=0.5, search_root=None,
         fallback_coordinates=None):
    """Find element and type a value into it, retrying with heal on recoverable errors.

    search_root: optional WebElement (e.g. a shadow-root child) to resolve the
    selector against for shadow-DOM piercing. Only the element lookup uses it;
    the type/send_keys is always dispatched via driver. None = top-level lookup.

    fallback_coordinates: recorded authoring-time (x, y) used as the absolute last
    resort if the heal cascade exhausts (API returned [0,0]). Only honoured on
    AutohealExhausted — never short-circuits a fresh resolve (spec §3.4).
    """
    return _run_action(
        driver, _TYPE_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        fallback_coordinates=fallback_coordinates,
        value=value, strategy=strategy, timeout=timeout,
        coords=coords, multiple_inputs=multiple_inputs,
        manual_interaction_tag=manual_interaction_tag,
    )
