"""Frame switching helper.

Verbatim port of V2 helper implementations:
- ``switch_to_frame_by_xpath`` — main frame switching logic
- ``ShadowContext`` — required dependency for the shadow-DOM branch
- ``_find_in_shadow_root`` — required fallback for shadow root element finding
"""
from __future__ import annotations

import json
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

_log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# ShadowContext + helper
# ---------------------------------------------------------------------------

class ShadowContext:
    """Single abstraction for shadow root access — native or JS fallback."""

    def __init__(self, driver, host):
        self.driver = driver
        self.host = host
        self._native = None
        self._first_child = None
        self._use_js = False
        try:
            # Primary: shadowRoot.children[0] — returns a regular WebElement,
            # avoiding the recursive serialization bug on iOS Safari that occurs
            # when the ShadowRoot object itself is stored/queried.
            self._first_child = driver.execute_script(
                "return arguments[0].shadowRoot.children[0]", host)
            if self._first_child is None:
                self._use_js = True
        except Exception:
            self._first_child = None
            # Intermediate fallback: querySelector filters out script/style
            try:
                self._first_child = driver.execute_script(
                    "return arguments[0].shadowRoot.querySelector(':scope > :not(script):not(style)')", host)
                if self._first_child is None:
                    self._use_js = True
            except Exception:
                self._first_child = None
                self._use_js = True
        # Also grab the ShadowRoot for CSS selector queries (non-XPATH)
        if not self._use_js:
            try:
                sr = driver.execute_script("return arguments[0].shadowRoot", host)
                if sr:
                    self._native = sr
            except Exception:
                pass

    def find_element(self, by, selector, caller=""):
        if not self._use_js:
            try:
                if by == By.XPATH:
                    # Use children[0] for XPATH — it's a regular WebElement,
                    # safe on all browsers including iOS Safari
                    if self._first_child:
                        return self._first_child.find_element(by, selector)
                    # Fallback: get first non-script/style child via JS
                    try:
                        child = self.driver.execute_script("""
                            const host = arguments[0];
                            const children = host.shadowRoot ? Array.from(host.shadowRoot.children) : [];
                            return children.filter(el =>
                                el.tagName.toLowerCase() !== 'script' &&
                                el.tagName.toLowerCase() !== 'style'
                            )[0];
                        """, self.host)
                    except Exception:
                        child = self._native.find_element(
                            By.CSS_SELECTOR, ":scope > :not(script):not(style)")
                    return child.find_element(by, selector)
                # CSS selectors can use the ShadowRoot directly
                if self._native:
                    return self._native.find_element(by, selector)
            except Exception:
                pass  # fall through to JS fallback
        return _find_in_shadow_root(self.driver, self.host, by, selector, caller=caller)


def _find_in_shadow_root(driver, host, by, selector, caller=""):
    """
    Find an element inside a host's shadow root without returning
    the ShadowRoot object (avoids recursive serialization on iOS Safari).
    """
    if by == By.XPATH:
        js = """
            var sr = arguments[0].shadowRoot;
            if (!sr) return null;
            var children = Array.from(sr.children).filter(function(el) {
                var t = el.tagName.toLowerCase();
                return t !== 'style' && t !== 'script';
            });
            return children;
        """
        children = driver.execute_script(js, host)
        if not children:
            raise NoSuchElementException(
                f"{caller}: shadow root has no searchable children")
        for child in children:
            try:
                return child.find_element(By.XPATH, selector)
            except NoSuchElementException:
                continue
        raise NoSuchElementException(
            f"{caller}: '{selector}' not found across {len(children)} shadow children"
        )
    else:
        js = """
            var sr = arguments[0].shadowRoot;
            if (!sr) return null;
            return sr.querySelector(arguments[1]);
        """
        result = driver.execute_script(js, host, selector)
        if result is None:
            raise NoSuchElementException(f"{caller}: '{selector}' not found in shadow root")
        return result


# ---------------------------------------------------------------------------
# switch_to_frame_by_xpath
# ---------------------------------------------------------------------------

def switch_to_frame_by_xpath(driver: webdriver.Chrome, frame_info):
    shadow_ctx = None
    try:
        if frame_info and frame_info != "":
            frames = json.loads(frame_info)
            for frame in frames:
                key, value = list(frame.items())[0]
                if key == "iframe":
                    if shadow_ctx is None:
                        if isinstance(value, list):
                            for index in range(0, len(value)):
                                try:
                                    iframe = driver.find_element(By.XPATH, value[index])
                                    break
                                except Exception:
                                    continue
                        else:
                            iframe = driver.find_element(By.XPATH, value)
                    else:
                        iframe = shadow_ctx.find_element(By.XPATH, value, caller="switch_to_frame_by_xpath")
                    driver.switch_to.frame(iframe)
                    shadow_ctx = None
                elif key == "shadow":
                    if shadow_ctx is not None:
                        host_el = shadow_ctx.find_element(By.XPATH, value, caller="switch_to_frame_by_xpath")
                    else:
                        host_el = driver.find_element(By.XPATH, value)
                    shadow_ctx = ShadowContext(driver, host_el)
        return shadow_ctx
    except Exception as e:
        _log.warning("Error in switch_to_frame_by_xpath: %s", e)
        return None
