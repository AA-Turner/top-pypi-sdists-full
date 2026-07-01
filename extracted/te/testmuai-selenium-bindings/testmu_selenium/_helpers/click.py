import logging

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from testmu_selenium._errors import ClickAllMethodsFailed

_log = logging.getLogger(__name__)

MAX_WAIT_UNTILTIME = 10

# Map Playwright-style modifier key names to Selenium Keys attribute names.
# "Meta" aliases to CONTROL for macOS behavior (Cmd+click routes through Keys.CONTROL).
_MODIFIER_KEY_MAP = {
    "Shift": "SHIFT",
    "Control": "CONTROL",
    "Alt": "ALT",
    "Meta": "CONTROL",
}


def clickElement(element, driver=None, order="se_js_ac", modifiers=None, click_modifier=None):
    """
    Click element with three fallback methods based on order preference.

    When `modifiers` is a non-empty list (e.g. ["Shift"], ["Control", "Shift"]),
    routes to an ActionChains key_down -> click -> key_up pattern instead of
    the cascade. Modifiers are held across the click, released in reverse order (LIFO).

    Args:
        element: WebElement to click
        driver: WebDriver instance (required for js, action chain, and modifier clicks)
        order: Order of fallback methods (default: "se_js_ac")
        modifiers: Optional list of modifier-key names
                   (["Shift"] | ["Control"] | ["Alt"] | ["Meta"]) or combinations

    Returns:
        bool: True on success.

    Raises:
        ClickAllMethodsFailed: when all configured fallback tiers exhaust.
        Exception: "Element not found" when element is falsy.
        Exception: "Driver required for modifier-key click" when modifiers given without driver.
    """
    if not element:
        raise Exception("Element not found")

    if click_modifier:
        # Gesture (long_press / multi_click / right_click) takes precedence over a
        # plain keyboard-modifier click — resolve any templated params FIRST, then
        # validate; a None result (multi_click frequency==1) collapses to the plain
        # click cascade below. Lazy import breaks the gesture -> click module cycle.
        from testmu_selenium._helpers.gesture import (
            resolve_click_modifier_variables, validate_click_modifier, dispatch_gesture,
        )
        # Export-path data-driven gestures carry templated duration/frequency under
        # click_modifier['variables']; resolve against the binding store BEFORE the
        # bounds check (Task 25 / X3).
        click_modifier = resolve_click_modifier_variables(click_modifier)
        validated = validate_click_modifier(click_modifier)
        if validated is not None:
            return dispatch_gesture(element, driver, validated, modifiers)

    if modifiers:
        return _modifier_click(element, driver, modifiers)

    methods = {
        "se": lambda: _selenium_click(element, driver),
        "js": lambda: _javascript_click(element, driver),
        "ac": lambda: _action_chain_click(element, driver)
    }

    # Parse the order string to get method sequence
    method_order = order.split("_")

    for method_name in method_order:
        try:
            if methods[method_name]():
                return True
        except Exception as e:
            _log.warning("Click method %s failed: %s", method_name, e)
            continue

    _log.error("All click methods failed")
    raise ClickAllMethodsFailed(
        f"all click fallback tiers ({order}) exhausted for element"
    )


def add_clickElement_to_webelement():
    """
    Monkey patch WebElement class to add clickElement method
    """
    from selenium.webdriver.remote.webelement import WebElement

    def clickElement_method(self, driver=None, order="se_js_ac", modifiers=None, click_modifier=None):
        return clickElement(self, driver, order, modifiers, click_modifier)

    # Add the method to WebElement class
    WebElement.clickElement = clickElement_method


def _modifier_click(element, driver, modifiers):
    """Modifier-key click via ActionChains key_down -> click -> key_up.

    Holds each modifier key before the click, releases them in reverse order
    after the click (LIFO). Meta is aliased to CONTROL for macOS (Cmd+click behavior).
    """
    if driver is None:
        raise Exception("Driver required for modifier-key click")

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    mod_attrs = [_MODIFIER_KEY_MAP.get(m, m.upper()) for m in modifiers]
    chain = ActionChains(driver)
    for attr in mod_attrs:
        chain = chain.key_down(getattr(Keys, attr))
    chain = chain.click(element)
    for attr in reversed(mod_attrs):
        chain = chain.key_up(getattr(Keys, attr))
    chain.perform()
    return True


def _selenium_click(element, driver=None, timeout=MAX_WAIT_UNTILTIME):
    """Standard Selenium click with clickability wait when driver is provided."""
    if driver is not None:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(element)).click()
    else:
        element.click()
    return True


def _javascript_click(element, driver):
    """JavaScript click fallback"""
    if driver is None:
        raise Exception("Driver required for JavaScript click")

    driver.execute_script("arguments[0].click();", element)
    return True


def _action_chain_click(element, driver):
    """Action chain click fallback"""
    if driver is None:
        raise Exception("Driver required for Action chain click")

    from selenium.webdriver.common.action_chains import ActionChains
    action_chains = ActionChains(driver)
    action_chains.move_to_element(element).click().perform()
    return True
