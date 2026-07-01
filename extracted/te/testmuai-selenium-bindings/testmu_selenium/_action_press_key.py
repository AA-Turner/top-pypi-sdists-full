"""High-level press_key action — find the target element and send a key to it,
healing on failure (selector → coordinate).

Mirrors the clear/click/type verbs: the wrapper threads through the shared
find+heal engine (_run_action) so a failing selector locate triggers the
DESKTOP_LOCATE heal cascade before delivering the keystroke.

When the cascade resolves to viewport pixel coordinates rather than a new
selector (e.g. a canvas or shadow-DOM target with no xpath derivable), the
coord_runner takes over: it focuses the element at (x, y) via a real pointer
click (ActionBuilder), then delivers the key through the keyboard input source.
This mirrors _type_coord_runner and the V2 enter-at-coordinate path.

Discriminator (spec contract): this action is only emitted when a selector IS
present on the node — a selectorless global press keeps the current global
ActionChains path and does NOT use this binding. No selectorless DOM-first
shortcut is needed here (unlike set_input_files).
"""
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from testmu_selenium._action_engine import _ActionSpec, _run_action


def _press_key_runner(element, ctx):
    """Send the key to the located element.

    Selenium delivers the keystroke to the element directly (element.send_keys),
    which focuses the element then sends the key — the same path V2 used for
    targeted Enter/Tab/etc.
    """
    element.send_keys(ctx['key'])
    return None


def _press_key_coord_runner(driver, x, y, ctx):
    """DESKTOP_LOCATE-tier path: focus the element at (x, y) via a real pointer
    click, then deliver the key via the keyboard input source.

    Two separate ActionBuilder instances mirror _type_coord_runner: the first
    performs a real pointer click at the healed coordinate (fires any click
    handler + sets browser focus), the second sends the key to whatever element
    is now focused. A synthetic elementFromPoint(x,y).focus() is NOT used because
    a pure <canvas> target is not focusable and its click handler would not fire.
    """
    ab_click = ActionBuilder(driver)
    ab_click.pointer_action.move_to_location(x, y)
    ab_click.pointer_action.click()
    ab_click.perform()

    ab_key = ActionBuilder(driver)
    ab_key.key_action.send_keys(ctx['key'])
    ab_key.perform()

    return True


_PRESS_KEY_SPEC = _ActionSpec(
    runner=_press_key_runner,
    coord_runner=_press_key_coord_runner,
)


def press_key(driver, selector, key, *, description='', tiers=None,
              autoheal=True, max_attempts=4, retry_delay=0.5,
              search_root=None, fallback_coordinates=None):
    """Find element and press a key on it, retrying with heal cascade on failure.

    Args:
        driver: Selenium WebDriver instance.
        selector: Locator list (same format as click/type). Must be present —
            a selectorless global press keeps the bare ActionChains path and
            does not use this binding.
        key: Key string to send (e.g. a ``Keys.*`` constant or a plain character).
            Passed verbatim to ``element.send_keys(key)``.
        description: Human-readable description used by the heal cascade for
            vision-based relocation. Defaults to empty string.
        tiers: Heal tiers to use. None defers to the engine's default
            (DESKTOP_LOCATE only).
        autoheal: Whether to run the heal cascade on element-find failure.
        max_attempts: Maximum find+act attempts before raising.
        retry_delay: Seconds to sleep between heal attempts.
        search_root: Optional WebElement (e.g. a shadow-root child) to scope
            the selector lookup. None = top-level document.
        fallback_coordinates: Authoring-time (x, y) used as the absolute last
            resort when the heal cascade exhausts (spec §3.4).
    """
    return _run_action(
        driver, _PRESS_KEY_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        fallback_coordinates=fallback_coordinates,
        key=key,
    )
