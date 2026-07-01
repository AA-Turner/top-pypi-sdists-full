"""High-level clear action — find element, clear field, heal on failure.

V2 reference (canvas-coordinate path).
The selector-tier path uses element.clear() (Selenium native);
the COORDINATE-tier fallback uses 3 sequential ActionBuilder instances:
    1. move_to_location(x, y) + click + perform
    2. key_down(CTRL) + send_keys('a') + key_up(CTRL) + perform
    3. send_keys(Keys.DELETE) + perform
"""
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.keys import Keys

from testmu_selenium._action_engine import _ActionSpec, _run_action


def _clear_runner(element, ctx):
    try:
        element.clear()
    except InvalidElementStateException:
        # Native clear() enforces the W3C is-editable precondition and rejects
        # masked/readonly inputs. Fall back to keystroke clearing (Ctrl+A +
        # Delete) — the same select-all/delete sequence the COORDINATE tier
        # uses, which the browser routes to the focused element without the
        # editability gate.
        _keystroke_clear(ctx['driver'], element)
    return None


def _keystroke_clear(driver, element):
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].focus();", element)

    ab1 = ActionBuilder(driver)
    ab1.key_action.key_down(Keys.CONTROL)
    ab1.key_action.send_keys('a')
    ab1.key_action.key_up(Keys.CONTROL)
    ab1.perform()

    ab2 = ActionBuilder(driver)
    ab2.key_action.send_keys(Keys.DELETE)
    ab2.perform()


def _clear_coord_runner(driver, x, y, ctx):
    ab1 = ActionBuilder(driver)
    ab1.pointer_action.move_to_location(x, y)
    ab1.pointer_action.click()
    ab1.perform()

    ab2 = ActionBuilder(driver)
    ab2.key_action.key_down(Keys.CONTROL)
    ab2.key_action.send_keys('a')
    ab2.key_action.key_up(Keys.CONTROL)
    ab2.perform()

    ab3 = ActionBuilder(driver)
    ab3.key_action.send_keys(Keys.DELETE)
    ab3.perform()

    return True


_CLEAR_SPEC = _ActionSpec(runner=_clear_runner, coord_runner=_clear_coord_runner)


def clear(driver, selector, *, description='', tiers=None, autoheal=True,
          max_attempts=4, retry_delay=0.5, search_root=None,
          fallback_coordinates=None):
    """Find element and clear it, retrying with heal cascade on recoverable errors."""
    return _run_action(
        driver, _CLEAR_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        fallback_coordinates=fallback_coordinates,
    )
