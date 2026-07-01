"""High-level hover action — find element, hover via ActionChains, heal on failure.

V2 reference (canvas-coordinate path).
The selector-tier path uses ActionChains(driver).move_to_element(el).perform();
the COORDINATE-tier fallback uses ActionBuilder.pointer_action.move_to_location(x, y).
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from testmu_selenium._action_engine import _ActionSpec, _run_action


def _hover_runner(element, ctx):
    ActionChains(ctx['driver']).move_to_element(element).perform()
    return True


def _hover_coord_runner(driver, x, y, ctx):
    ab = ActionBuilder(driver)
    ab.pointer_action.move_to_location(x, y)
    ab.perform()
    return True


# Recoverable set inherits the engine default — see _DEFAULT_RECOVERABLE
# in _action_engine. Keeps hover in lockstep with future additions/removals.
_HOVER_SPEC = _ActionSpec(runner=_hover_runner, coord_runner=_hover_coord_runner)


def hover(driver, selector, *, description='', tiers=None, autoheal=True,
          max_attempts=4, retry_delay=0.5, search_root=None,
          fallback_coordinates=None):
    """Find element and hover, retrying with heal cascade on recoverable errors."""
    return _run_action(
        driver, _HOVER_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        fallback_coordinates=fallback_coordinates,
    )
