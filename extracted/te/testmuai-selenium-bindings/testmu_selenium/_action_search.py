"""High-level search action — find input, type value, submit Enter, heal on failure.

Mirrors the V2 SearchAction shape: clear → type → press Enter. The IR currently
lowers SearchAction into FindElement → FillNode → PressKeyNode(Enter); this
wrapper composes the same primitives behind one call so codegen can collapse
the trio into a single line.
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.keys import Keys

from testmu_selenium._action_engine import _ActionSpec, _run_action


def _search_runner(element, ctx):
    element.input_value(
        ctx['driver'],
        ctx['value'],
        ctx.get('strategy', 'se_js_ac'),
        ctx.get('timeout', 10),
        None,
        False,
        '',
    )
    ActionChains(ctx['driver']).send_keys(Keys.ENTER).perform()
    return True


# Coordinate-tier fallback (canvas/vision target with no DOM node). REAL-click at
# the resolved coords — not elementFromPoint().focus(), which is a no-op on a
# bare <canvas> and leaves keystrokes undelivered (see _action_type for the full
# rationale) — then type the value and submit with Enter via the keyboard source.
def _search_coord_runner(driver, x, y, ctx):
    click = ActionBuilder(driver)
    click.pointer_action.move_to_location(x, y)
    click.pointer_action.click()
    click.perform()

    keyboard = ActionBuilder(driver)
    keyboard.key_action.send_keys(ctx['value'])
    keyboard.key_action.send_keys(Keys.ENTER)
    keyboard.perform()
    return True


_SEARCH_SPEC = _ActionSpec(runner=_search_runner, coord_runner=_search_coord_runner)


def search(driver, selector, value, *, strategy='se_js_ac', timeout=10,
           description='', tiers=None, autoheal=True,
           max_attempts=4, retry_delay=0.5, search_root=None):
    """Find input element, type ``value``, then press Enter — with heal cascade.

    Args:
        driver: Selenium WebDriver.
        selector: Primary selector (list of dicts) or healed selector list.
        value: Text to type before submitting.
        strategy: Click/input strategy passed to underlying input_value.
        timeout: Per-attempt timeout (seconds) for input_value.
        description: Human-readable step name for heal/logging.
        tiers: Override heal-tier order; None uses _DEFAULT_HEAL_TIERS.
        autoheal: Disable cascade entirely if False.
        max_attempts: Total attempts including healed retries.
        retry_delay: Sleep between healed retries (seconds).
    """
    return _run_action(
        driver, _SEARCH_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        value=value, strategy=strategy, timeout=timeout,
    )
