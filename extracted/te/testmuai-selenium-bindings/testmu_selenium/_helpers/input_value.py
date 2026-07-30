"""Selenium input_value helper — web-only port of the V2 helper.

Mirrors the pure-function + monkey-patch pattern used by click.py. Ported
from the V2 source with every mobile / tagify / canvas autoheal / iframe-drill
branch stripped per the T2b TYPE-slice spec.

Per-op correlation (operation_index in V2) is now carried by
BaseAction.action_id on the V3 runtime side and is intentionally absent
from this helper.
"""

import logging
import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.ui import WebDriverWait

_log = logging.getLogger(__name__)


SET_SELECTION_RANGE_ELIGIBLE_INPUT = ["text", "password", "search", "tel", "url"]


def _coerce_scalar_to_str(value):
    """Coerce a type-preserving scalar to str for typing.

    execute_js/set_var/var() keep values as their native type, so an int/float/
    bool can reach here and break the string ops below (value[-4:], len(value),
    send_keys char iteration). int/float/bool -> str (bool -> "True"/"False");
    str/None pass through; dict/list are left unchanged so a structural value
    fails loudly downstream rather than being silently stringified.
    """
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (int, float)):
        return str(value)
    return value


def _coerce_fill_value(value):
    """Normalize a user-supplied value at the typing boundary.

    Scalars are stringified; a structural dict/list is rejected loudly because
    ``send_keys`` would otherwise iterate it — typing a dict's KEY NAMES into
    the field — instead of failing.

    Every path that delivers a value to the keyboard must go through here.
    ``input_value`` is only one of them: the coordinate-tier fallbacks in
    ``_action_type``/``_action_search`` bypass ``input_value`` entirely and
    talk to ``ActionBuilder.key_action`` directly, so without this shared
    boundary the same step behaved differently depending on which heal tier
    resolved the element.
    """
    value = _coerce_scalar_to_str(value)
    if isinstance(value, (dict, list)):
        raise TypeError(
            f"cannot type a structural {type(value).__name__} value into an "
            f"input; expected a scalar (str/int/float/bool)."
        )
    return value


def input_value(
    element,
    driver,
    value,
    order="se_js_ac",
    timeout=10,
    coords=None,
    multiple_inputs=False,
    manual_interaction_tag="",
):
    """Fill an input with V2-parity semantics (web-only).

    Args:
        element: Target WebElement (monkey-patched to self when called as method).
        driver: WebDriver instance.
        value: Text to type into the field.
        order: Click cascade order for the focus step (e.g. "se_js_ac").
        timeout: WebDriverWait seconds for the focused-element wait.
        coords: Optional (x, y) viewport coordinates — triggers coordinate
            click + backspace-clear path instead of element focus.
        multiple_inputs: When True, skips the js-native fallback write-back
            check (used for multi-value inputs where send_keys value diverges
            from field value by design).
        manual_interaction_tag: Non-empty tag combined with type=date routes
            to direct JS value-set (locale-sensitive date formatting).

    Returns:
        None on success. Re-raises on uncaught errors.
    """
    # Normalize at the entry so every downstream branch (month split, per-char,
    # coords, send_keys) sees a string, and a structural value fails loudly.
    value = _coerce_fill_value(value)
    try:
        if coords is not None:
            x, y = coords
            # Coordinate click via ActionChains (viewport absolute).
            ac = ActionChains(driver)
            ac.w3c_actions.pointer_action.move_to_location(x, y)
            ac.w3c_actions.pointer_action.click()
            ac.perform()
            time.sleep(0.5)

            # Clear via 50x BACKSPACE (works on both native inputs and
            # contenteditable).
            clear_action = ActionBuilder(driver)
            clear_action.key_action.send_keys(Keys.BACKSPACE * 50)
            clear_action.perform()

            # Type value.
            keyboard_actions = ActionBuilder(driver)
            keyboard_actions.key_action.send_keys(value)
            keyboard_actions.perform()
            return

        # Element path.
        _clear(driver, element)

        try:
            # Reuse monkey-patched clickElement from click.py for the
            # focus-cascade (se/js/ac fallback).
            element.clickElement(driver, order)
        except Exception as e:
            _log.warning("Error clicking on element: %s\n continuing with the next step", e.__str__())

        wait = WebDriverWait(driver, timeout)
        try:
            focused_element = wait.until(_element_to_be_input_and_text)

            focused_element_pattern = focused_element.get_attribute("pattern")
            element_type = element.get_attribute("type")
            max_length = focused_element.get_attribute("maxlength")

            _move_to_start_of_input(driver, element, focused_element, element_type=element_type)

            if manual_interaction_tag != "" and element_type == "date":
                driver.execute_script(
                    "arguments[0].value = arguments[1];", focused_element, value
                )
            elif element_type == "month":
                # MMYYYY → send month, TAB, send year.
                year = value[-4:]
                month = value[:-4]
                focused_element.send_keys(month)
                focused_element.send_keys(Keys.TAB)
                focused_element.send_keys(year)
            elif (focused_element_pattern and "[0-9]{2}" in focused_element_pattern) or (
                max_length == "1" and len(value) > 1
            ):
                # Char-by-char send_keys, following auto-advance focus between
                # fields. Covers numeric-segment inputs (pattern "[0-9]{2}") and
                # multi-box OTP/PIN widgets where each box is maxlength=1 and the
                # widget moves focus to the next box on input.
                for index, char in enumerate(value):
                    focused_element.send_keys(char)
                    if index == len(value) - 1:
                        break
                    try:
                        focused_element = wait.until(_element_to_be_input_and_text)
                    except TimeoutException:
                        # Focus left the input group before all chars were sent
                        # (e.g. the widget jumped to a submit button). Stop here
                        # rather than falling through to the destructive js-native
                        # write-back in the outer except.
                        break
            else:
                focused_element.send_keys(value)

                tag_name = focused_element.get_attribute("tagName")
                is_input_class = tag_name.lower() in ["input", "textarea"] if tag_name else False
                after_input = focused_element.get_attribute("value")
                if (
                    is_input_class
                    and after_input is not None
                    and not multiple_inputs
                    and after_input != value
                ):
                    _log.warning(
                        "Input value after send_keys: '%s' does not match expected input: '%s'. Using js native input as fallback.",
                        after_input, value,
                    )
                    _perform_js_native_input(driver, focused_element, "")
                    _perform_js_native_input(driver, focused_element, value)

        except Exception as e:
            _log.warning(
                "Error sending keys to focused element. Falling back to js for send keys in input / type events: %s",
                e.__str__(),
            )
            _perform_js_native_input(driver, element, "")
            _perform_js_native_input(driver, element, value)

    except Exception as e:
        _log.warning("Error in input_value: %s", e.__str__())
        raise


def add_input_value_to_webelement():
    """Monkey-patch WebElement class to add input_value method."""
    from selenium.webdriver.remote.webelement import WebElement

    def input_value_method(
        self,
        driver,
        value,
        order="se_js_ac",
        timeout=10,
        coords=None,
        multiple_inputs=False,
        manual_interaction_tag="",
    ):
        return input_value(
            self,
            driver,
            value,
            order,
            timeout,
            coords,
            multiple_inputs,
            manual_interaction_tag,
        )

    WebElement.input_value = input_value_method


def _is_numeric_input(text):
    """True if text is phone/card/date-like (digits + [+-/.] only)."""
    return bool(text) and bool(re.fullmatch(r"[\d\+\-\/\.]+", text))


def _clear(driver, element):
    """Focus element, then backspace-clear value; handle contenteditable via range+DELETE."""
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)

    current_value = driver.execute_script("return arguments[0].value;", element)

    try:
        if current_value:
            try:
                driver.execute_script(
                    "arguments[0].setSelectionRange(arguments[0].value.length, arguments[0].value.length);",
                    element,
                )
            except Exception:
                pass
            for _ in range(len(current_value)):
                element.send_keys(Keys.BACKSPACE)

        if element.get_attribute("contenteditable") == "true":
            driver.execute_script(
                """
                const element = arguments[0];
                const range = document.createRange();
                range.selectNodeContents(element);
                const selection = window.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);
                """,
                element,
            )
            element.send_keys(Keys.DELETE)

    except Exception as e:
        _log.warning("Error clearing element: %s", e)
        try:
            driver.execute_script("arguments[0].value = '';", element)
        except Exception as e2:
            _log.warning("Error setting value to empty: %s", e2)


def _move_to_start_of_input(driver, element, focused_element=None, element_type=None):
    """Move caret to start of input — setSelectionRange for simple inputs, 10x ARROW_LEFT for date/time/autocomplete-placeholder inputs."""
    target_element = focused_element if focused_element else element

    target_attrs = driver.execute_script(
        """
        var el = arguments[0];
        return {
            tagName: el.tagName ? el.tagName.toLowerCase() : '',
            type: el.type || ''
        };
        """,
        target_element,
    )

    if (
        target_attrs["tagName"] == "input"
        and target_attrs["type"] in SET_SELECTION_RANGE_ELIGIBLE_INPUT
    ):
        driver.execute_script("arguments[0].setSelectionRange(0, 0);", target_element)
        return

    element_attrs = driver.execute_script(
        """
        var el = arguments[0];
        return {
            placeholder: el.getAttribute('placeholder') || '',
            autocomplete: el.getAttribute('autocomplete') || ''
        };
        """,
        element,
    )

    el_type = element_type if element_type is not None else (element.get_attribute("type") or "")

    if (
        any(s in el_type for s in ("date", "time"))
        or all(part in element_attrs["placeholder"].lower() for part in ["dd", "mm", "yy"])
        or element_attrs["autocomplete"] != ""
    ):
        for _ in range(10):
            if focused_element:
                focused_element.send_keys(Keys.ARROW_LEFT)
            else:
                element.send_keys(Keys.ARROW_LEFT)


def _element_to_be_input_and_text(driver):
    """ExpectedCondition callable — returns focused element if it's an input/textarea/contenteditable."""
    focused_element = driver.execute_script(
        """
        var el = document.activeElement;
        try {
            while (el && el.shadowRoot && el.shadowRoot.activeElement) {
                el = el.shadowRoot.activeElement;
            }
        } catch(e) {
            console.warn('[input_value] shadowRoot.activeElement traversal failed:', e);
        }
        return el;
        """
    )
    tag = focused_element.tag_name.lower() if focused_element else ""
    if tag == "input" or tag == "textarea" or focused_element.get_attribute("contenteditable") == "true":
        return focused_element
    return False


def _perform_js_native_input(driver, element, input_text):
    """Use the DOM prototype's native value setter + dispatch input/change events.

    Needed for React/Vue controlled inputs where send_keys bypasses the
    framework's synthetic event system and the state stays out-of-sync.
    """
    try:
        driver.execute_script(
            """
            const elementPrototype = Object.getPrototypeOf(arguments[0]);
            const nativeSetter = Object.getOwnPropertyDescriptor(
                elementPrototype,
                "value"
            ).set;

            nativeSetter.call(arguments[0], arguments[1]);

            arguments[0].dispatchEvent(new Event("input", { bubbles: true, composed: true }));
            arguments[0].dispatchEvent(new Event("change", { bubbles: true, composed: true }));
            """,
            element,
            input_text,
        )
    except Exception as e:
        _log.error("Error in perform_js_native_input: %s", e.__str__())
