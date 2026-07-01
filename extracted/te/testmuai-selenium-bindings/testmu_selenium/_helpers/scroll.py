"""Driver-level scroll helper — window or element scrolling.

Maps to the V3 scroll codegen output:
- ScrollType.NONE (scroll-to-extreme): mode='none', direction='top'/'bottom'
- ScrollType.PIXELS: mode='pixels', amount=int (positive int, direction sign applied)
- ScrollType.PERCENTAGE: mode='percentage', amount=float (0-100)
- ScrollType.TIMES: mode='times', amount=int (number of viewport scrolls)

V3 emission reference: the scroll handler in the code generator.
- Window-level: window.scrollTo(0, ...) / window.scrollBy(0, N)
- Element-level: arguments[0].scrollBy(...) / arguments[0].scrollTop = ...

This wrapper consolidates all variants behind one signature.
"""
from __future__ import annotations

import time
from typing import Any


def scroll(
    driver,
    *,
    direction: str = 'down',
    amount: int | float | None = None,
    mode: str = 'pixels',
    element: Any | None = None,
) -> None:
    """Scroll viewport, or element if provided.

    Args:
        driver: Selenium WebDriver.
        direction: 'up' | 'down' | 'left' | 'right' for relative;
                   'top' | 'bottom' when mode='none' for absolute extremes.
        amount: pixels (mode='pixels'), percentage 0-100 (mode='percentage'),
                count (mode='times'). Ignored when mode='none'.
        mode: 'pixels' | 'percentage' | 'times' | 'none'.
        element: WebElement to scroll within. None = window.

    V3 reference: the scroll handlers in the code generator.
    Always emits a brief settle (V3 parity: time.sleep(1) after scroll).
    """
    _DIRECTION_SIGN = {
        'down': 1,
        'right': 1,
        'up': -1,
        'left': -1,
    }

    if mode == 'none':
        _scroll_none(driver, direction, element)
    elif mode == 'pixels':
        _scroll_pixels(driver, direction, amount, element, _DIRECTION_SIGN)
    elif mode == 'percentage':
        _scroll_percentage(driver, direction, amount, element, _DIRECTION_SIGN)
    elif mode == 'times':
        _scroll_times(driver, direction, amount, element, _DIRECTION_SIGN)
    else:
        raise ValueError(f"Unknown scroll mode: {mode!r}")

    time.sleep(1)


# ---------------------------------------------------------------------------
# mode='none' — scroll to absolute extreme (top / bottom of window or element)
# ---------------------------------------------------------------------------

def _scroll_none(driver, direction: str, element) -> None:
    if element is None:
        if direction == 'top':
            driver.execute_script("window.scrollTo(0, 0)")
        else:  # bottom
            driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight)"
            )
    else:
        if direction == 'top':
            driver.execute_script("arguments[0].scrollTop = 0", element)
        else:  # bottom
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", element
            )


# ---------------------------------------------------------------------------
# mode='pixels' — scroll by exact pixel count
# ---------------------------------------------------------------------------

def _scroll_pixels(driver, direction: str, amount, element, sign_map) -> None:
    sign = sign_map.get(direction, 1)
    signed = int(amount * sign)
    is_vertical = direction in ('up', 'down')

    if element is None:
        if is_vertical:
            driver.execute_script(f"window.scrollBy(0, {signed})")
        else:
            driver.execute_script(f"window.scrollBy({signed}, 0)")
    else:
        if is_vertical:
            driver.execute_script(
                "arguments[0].scrollBy(0, arguments[1])", element, signed
            )
        else:
            driver.execute_script(
                "arguments[0].scrollBy(arguments[1], 0)", element, signed
            )


# ---------------------------------------------------------------------------
# mode='percentage' — scroll by percentage of window/element height or width
# ---------------------------------------------------------------------------

def _scroll_percentage(driver, direction: str, amount, element, sign_map) -> None:
    sign = sign_map.get(direction, 1)
    is_vertical = direction in ('up', 'down')

    if element is None:
        if is_vertical:
            height = driver.execute_script("return window.innerHeight")
            delta = int(height * amount / 100 * sign)
            driver.execute_script(f"window.scrollBy(0, {delta})")
        else:
            width = driver.execute_script("return window.innerWidth")
            delta = int(width * amount / 100 * sign)
            driver.execute_script(f"window.scrollBy({delta}, 0)")
    else:
        if is_vertical:
            scroll_dim = driver.execute_script(
                "return arguments[0].scrollHeight", element
            )
            delta = int(scroll_dim * amount / 100 * sign)
            driver.execute_script(
                "arguments[0].scrollBy(0, arguments[1])", element, delta
            )
        else:
            scroll_dim = driver.execute_script(
                "return arguments[0].scrollWidth", element
            )
            delta = int(scroll_dim * amount / 100 * sign)
            driver.execute_script(
                "arguments[0].scrollBy(arguments[1], 0)", element, delta
            )


# ---------------------------------------------------------------------------
# mode='times' — scroll N × viewport/element height
# ---------------------------------------------------------------------------

def _scroll_times(driver, direction: str, amount, element, sign_map) -> None:
    sign = sign_map.get(direction, 1)
    is_vertical = direction in ('up', 'down')
    count = int(amount)

    if element is None:
        if is_vertical:
            height = driver.execute_script("return window.innerHeight")
            delta = int(height * sign)
            for _ in range(count):
                driver.execute_script(f"window.scrollBy(0, {delta})")
        else:
            width = driver.execute_script("return window.innerWidth")
            delta = int(width * sign)
            for _ in range(count):
                driver.execute_script(f"window.scrollBy({delta}, 0)")
    else:
        # V3 element-times path: scrollBy one viewport (element clientHeight/
        # clientWidth) per iteration. A synthetic WheelEvent does not cause
        # the browser to scroll, so scrollBy is used here for parity with the
        # pixels/percentage element modes.
        if is_vertical:
            dim = driver.execute_script("return arguments[0].clientHeight", element)
            delta = int(dim * sign)
            for _ in range(count):
                driver.execute_script(
                    "arguments[0].scrollBy(0, arguments[1])", element, delta
                )
        else:
            dim = driver.execute_script("return arguments[0].clientWidth", element)
            delta = int(dim * sign)
            for _ in range(count):
                driver.execute_script(
                    "arguments[0].scrollBy(arguments[1], 0)", element, delta
                )


__all__ = ["scroll"]
