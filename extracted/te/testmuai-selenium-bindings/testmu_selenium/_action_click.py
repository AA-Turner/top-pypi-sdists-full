"""High-level click action — find element, click with strategy, heal on failure."""
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from testmu_selenium._action_engine import _ActionSpec, _run_action
from testmu_selenium._helpers.gesture import (
    resolve_click_modifier_variables, validate_click_modifier, do_gesture_at_coordinate,
)


def _click_runner(element, ctx):
    return element.clickElement(
        ctx['driver'],
        ctx.get('strategy', 'se_js_ac'),
        ctx.get('modifiers'),
        ctx.get('click_modifier'),
    )


# Coordinate-tier fallback. Heal cascade exhausted all selector-based tiers and
# returned viewport pixel coords — i.e. a canvas/vision target with no DOM node
# (a DOM target heals to a selector and never reaches here). REAL-click at those
# coords via ActionBuilder pointer actions, NOT elementFromPoint(x,y).click():
# a JS .click() synthesizes a MouseEvent with clientX/clientY = 0, so a canvas
# onclick that reads e.clientX grounds to the wrong location. A real pointer
# click carries the true coords. strategy/modifiers are not honoured on the
# coord fallback — visual-location click only.
def _click_coord_runner(driver, x, y, ctx):
    # V3 gesture at coords (canvas/no-DOM): resolve any templated params (Task 25)
    # against the binding store, validate the click_modifier, and replay the gesture
    # via ActionBuilder. A None result (no modifier / freq==1) falls through to the
    # plain visual-location pointer click. FULL held-keys-coord support: the
    # right_click gesture holds ctx['modifiers'] during the context_click.
    click_modifier = resolve_click_modifier_variables(ctx.get('click_modifier'))
    click_modifier = validate_click_modifier(click_modifier)
    if click_modifier is not None:
        return do_gesture_at_coordinate(driver, x, y, click_modifier, ctx.get('modifiers'))
    ab = ActionBuilder(driver)
    ab.pointer_action.move_to_location(x, y)
    ab.pointer_action.click()
    ab.perform()
    return True


# Recoverable set inherits the engine default — see _DEFAULT_RECOVERABLE
# in _action_engine. Keeps click in lockstep with future additions/removals.
_CLICK_SPEC = _ActionSpec(runner=_click_runner, coord_runner=_click_coord_runner)


def click(driver, selector, *, strategy='se_js_ac', modifiers=None,
          description='', tiers=None, autoheal=True,
          max_attempts=4, retry_delay=0.5, search_root=None,
          fallback_coordinates=None, click_modifier=None):
    """Find element and click it, retrying with heal cascade on recoverable errors.

    Equivalent to the codegen-emitted retry-loop pattern but encapsulated.

    search_root: optional WebElement (e.g. a shadow-root child) to resolve the
    selector against for shadow-DOM piercing. Only the element lookup uses it;
    the click is always dispatched via driver. None = top-level document lookup.

    fallback_coordinates: recorded authoring-time (x, y) used as the absolute last
    resort if the heal cascade exhausts (API returned [0,0]). Only honoured on
    AutohealExhausted — never short-circuits a fresh resolve (spec §3.4).
    """
    return _run_action(
        driver, _CLICK_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        fallback_coordinates=fallback_coordinates,
        strategy=strategy, modifiers=modifiers, click_modifier=click_modifier,
    )
