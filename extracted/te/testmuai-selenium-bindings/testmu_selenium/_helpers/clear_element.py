"""Selenium clear_element helper — web-only port of V2 clear_element.

Ported from V2 source. The mobile iOS Tagify branch
(MOBILE_TAGIFY_SCRIPT gate) is intentionally NOT ported — V3 mobile is
a Q4-scoped follow-up initiative.

Mirrors the pure-function + monkey-patch pattern used by click.py and
input_value.py. Generated code calls element.clear_element(driver) via the
WebElement monkey-patch installed by add_clear_element_to_webelement().
"""

import logging

from selenium.webdriver.common.keys import Keys

_log = logging.getLogger(__name__)


def _contenteditable_has_text(driver, element) -> bool:
    """True when a contenteditable holds any text.

    the Selection reset below (selectNodeContents + DELETE) wipes the
    editor's *pending toolbar marks* — a user who clicks Bold on an empty editor
    has formatting armed but no text, and re-selecting the range drops it. On an
    already-empty editor the clear achieves nothing anyway, so skip it.

    A probe failure returns True so the clear still runs: leaving stale text
    behind would corrupt the typed value, which is worse than losing a mark.
    """
    try:
        return bool(driver.execute_script(
            "return ((arguments[0].textContent || '').length > 0);", element))
    except Exception:  # noqa: BLE001 — probe failure must not skip a needed clear
        return True

def clear_element(driver, element):
    """Clear input/textarea/contenteditable element value (web-only V2 parity).

    Strategy mirrors the V2 helper:
      1. Read current_value via get_attribute('value').
      2. Backspace-loop n times where n = len(current_value).
      3. If contenteditable='true': JS selectNodeContents + Keys.DELETE.
      4. On any exception: JS arguments[0].value = '' fallback.

    Mobile iOS branch from V2 (Tagify check + perform_js_native_input) NOT
    ported — see module docstring.

    Args:
        driver: WebDriver instance.
        element: Target WebElement (monkey-patched to self when called as method).
    """
    try:
        current_value = element.get_attribute("value")
        if current_value:
            n = len(current_value)
            for _ in range(n):
                element.send_keys(Keys.BACKSPACE)

        if element.get_attribute("contenteditable") == "true" and \
                _contenteditable_has_text(driver, element):
            driver.execute_script(
                """
                const element = arguments[0];
                const range = document.createRange();
                const selection = window.getSelection();
                range.selectNodeContents(element);
                selection.removeAllRanges();
                selection.addRange(range);
                """,
                element,
            )
            element.send_keys(Keys.DELETE)
    except Exception as e:
        _log.warning("Error clearing element via send keys: %s", e)
        try:
            driver.execute_script("arguments[0].value = ''", element)
        except Exception as e2:
            _log.warning("Error setting value to empty via JS fallback: %s", e2)


def add_clear_element_to_webelement():
    """Monkey-patch WebElement class to add clear_element method.

    Generated code calls element.clear_element(driver) — mirrors the
    add_clickElement_to_webelement / add_input_value_to_webelement pattern.
    """
    from selenium.webdriver.remote.webelement import WebElement

    def clear_element_method(self, driver):
        return clear_element(driver, self)

    WebElement.clear_element = clear_element_method
