"""Screenshot helpers for Heal/visual flows.

Verbatim ports from a V2 helper module:
- ``get_browser_screenshot_as_base64``  (V2 helper)
- ``capture_full_page_screenshot``      (V2 helper)
- ``make_tagged_screenshot``            (V2 helper, PIL-dependent)
- ``_take_screenshot``                  (V2 helper, adapted from method to free function)

Adapter notes:
- ``execute_cdp_command`` is a private helper required by ``capture_full_page_screenshot``.
  Vendored as a private module-level function.
- ``_take_screenshot`` was originally a method on a class with ``self.session_id``/``self.driver``.
  In the bindings package the CDP fast-path comes from ``selenium_test_agent`` which is only
  available inside the host runtime. The import is guarded; in HyperExecute / standalone we always fall
  back to ``get_browser_screenshot_as_base64``.
"""
from __future__ import annotations

import asyncio
import base64
import colorsys
import io
import json
import logging
import random
import time

from selenium import webdriver

_log = logging.getLogger(__name__)

try:  # PIL is in the bindings deps (Pillow>=11) but keep guarded for parity with source.
    from PIL import Image, ImageDraw, ImageFont
except Exception:  # pragma: no cover
    Image = ImageDraw = ImageFont = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Private helper — required by capture_full_page_screenshot
# ---------------------------------------------------------------------------

def execute_cdp_command(driver: webdriver.Chrome, cmd: str, params: dict = {}):
    """Vendored CDP command helper."""
    platform = driver.capabilities.get('platformName', '').lower()
    if platform in ('android',):
        resource = "/session/%s/goog/cdp/execute" % driver.session_id
    else:
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def get_browser_screenshot_as_base64(driver: webdriver.Chrome) -> str:
    """Get browser screenshot as base64-encoded string."""
    if driver.capabilities.get('platformName', '').lower() == "ios":
        try:
            screenshot_base64 = driver.execute_script("mobile: viewportScreenshot")
            if screenshot_base64:
                return screenshot_base64
        except Exception as e:
            _log.warning("Error getting mobile device screenshot: %s", e)

    return driver.get_screenshot_as_base64()


def capture_full_page_screenshot(driver: webdriver.Chrome) -> str:
    """
    Captures a full-page screenshot using CDP using the underlying driver.

    Args:
        driver: An instance of WebDriver

    Returns:
        Base64-encoded PNG screenshot string
    """

    # Settle the DOM before any capture work. On long, lazy-loading pages the layout
    # (and scrollHeight) is still changing; measuring dimensions, snapshotting scroll, or
    # capturing too early means the post-capture scrollTo restore lands at the wrong visual
    # position (the DOM grew under the saved offset), corrupting the follow-up read. Logged
    # so the settle is observable in run logs (precedes the "Page dimensions" line).
    _log.info("Settling DOM 1s before full-page capture")
    time.sleep(1)

    # Get the full page dimensions via JS
    metrics = driver.execute_script("""
        return {
            width: Math.max(document.body.scrollWidth, document.documentElement.scrollWidth),
            height: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)
        }
    """)

    device_scale_factor = 1024 / metrics["width"]

    _log.info("Page dimensions - Width: %s, Height: %s, Device Scale Factor: %s", metrics['width'], metrics['height'], device_scale_factor)

    # Snapshot scroll on the now-settled layout so the post-capture restore lands at the
    # right visual position and the capture is side-effect-free (belt-and-suspenders).
    scroll_x, scroll_y = driver.execute_script("return [window.scrollX, window.scrollY];")

    # Capture the full page via captureBeyondViewport + an explicit clip at the
    # desired scale. Do NOT resize the emulated viewport to the full scrollHeight
    # (Emulation.setDeviceMetricsOverride): forcing the viewport to the whole page
    # height collapses scrollY to 0 (scroll-to-top) and balloons vh/%-relative
    # layout, which corrupts the screenshot the locate model receives, and leaves
    # the page scrolled to the top for any follow-up read. A clip preserves the
    # page layout; restoring scroll below guarantees no side-effect.
    try:
        screenshot = execute_cdp_command(driver, "Page.captureScreenshot", {
            "format": "png",
            "fromSurface": True,
            "captureBeyondViewport": True,
            "clip": {
                "x": 0,
                "y": 0,
                "width": metrics["width"],
                "height": metrics["height"],
                "scale": device_scale_factor,
            },
        })
    finally:
        time.sleep(1)
        driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", scroll_x, scroll_y)

    return screenshot["data"]  # this is base64 PNG


def make_tagged_screenshot(screenshot_base64, rects, driver):
    """
    Draw colored borders around rectangles and add labeled squares.

    Args:
        screenshot_base64: Screenshot image as base64-encoded string
        rects: Dictionary with keys and rect coordinates {'key': {'left': x, 'top': y, 'width': w, 'height': h}}
        driver: webdriver instance (used to read devicePixelRatio)

    Returns:
        Tuple ``(annotated_base64_jpeg, devicePixelRatio)`` on success, or ``None`` on failure.
    """
    def generate_random_color():
        """Generate a random bright color"""
        # Generate random hue, with high saturation and value for bright colors
        hue = random.random()
        saturation = random.uniform(0.7, 1.0)
        value = random.uniform(0.8, 1.0)

        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return tuple(int(c * 255) for c in rgb)

    def are_rectangles_disjoint(r1, r2):

        def is_inside(inner, outer):
            return (inner[0] >= outer[0] and inner[1] >= outer[1] and inner[2] <= outer[2] and inner[3] <= outer[3])

        if is_inside(r1, r2) or is_inside(r2, r1):
            return False

        if not (r1[2] <= r2[0] or r1[0] >= r2[2] or r1[3] <= r2[1] or r1[1] >= r2[3]):
            return False
        return True

    try:
        # Decode base64 screenshot
        image_data = base64.b64decode(screenshot_base64)
        image = Image.open(io.BytesIO(image_data))
        original_image = image.copy()
        draw = [ImageDraw.Draw(image)]
        ratio = driver.execute_script("return window.devicePixelRatio;")

        # Font paths
        font_paths = [
            "serif.ttf"
        ]

        # Process each rectangle
        tagifified_images = [image]
        image_to_rect_mapping = [[]]
        max_image_num = 1
        for key, rect in rects.items():
            color = generate_random_color()
            left, top, width, height = ((rect['x']) * ratio), ((rect['top']) * ratio), rect['width'] * ratio, rect['height'] * ratio
            x1, y1 = int(left), int(top)
            x2, y2 = int(left + width), int(top + height)

            if left > image.width or top > image.height:
                continue

            image_num = 0
            for index in range(0, max_image_num):
                if index >= len(image_to_rect_mapping):
                    image_to_rect_mapping.append([])
                rects = image_to_rect_mapping[index]
                is_space_available = True
                for rect in rects:
                    if not are_rectangles_disjoint([x1, y1, x2, y2], [rect['x1'], rect['y1'], rect['x2'], rect['y2']]):
                        is_space_available = False
                        break

                if is_space_available or index + 1 == max_image_num:
                    image_num = index
                    image_to_rect_mapping[image_num].append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
                    break
            if image_num >= len(tagifified_images):
                tagifified_images.append(original_image.copy())
                draw.append(ImageDraw.Draw(tagifified_images[image_num]))

            for i in range(3):
                draw[image_num].rectangle([x1 - i, y1 - i, x2 + i, y2 + i], outline=color, fill=None)

            square_width = min(40, width // 2)
            square_height = min(40, height // 2)

            draw[image_num].rectangle([x2 - square_width, y2 - square_height, x2, y2], outline=color, fill=color)

            text_color = (255, 255, 255) if sum(color) < 382 else (0, 0, 0)  # White text for dark bg, black for light bg

            for font_path in font_paths:
                try:
                    draw[image_num].text(
                        xy=(x2 - square_width + 3, y2 - square_height + 3),
                        text=key,
                        fill=text_color,
                        font=ImageFont.truetype(font_path, max(1, min(square_height, square_width) - 5))
                    )
                    break
                except IOError:
                    continue

        with io.BytesIO() as buffer:
            if tagifified_images[0].mode == 'RGBA':
                tagifified_images[0] = tagifified_images[0].convert('RGB')
            tagifified_images[0].save(buffer, format="JPEG", optimize=True, quality=50)
            return base64.b64encode(buffer.getvalue()).decode('utf-8'), ratio

    except Exception as e:
        _log.warning("Error creating annotated image: %s", e)
        return None


def _take_screenshot(driver: webdriver.Chrome) -> str:
    """CDP when available, Selenium fallback.

    Originally a method on an action class that held ``self.session_id``/``self.driver``.
    In the bindings runtime the CDP fast-path lives in ``selenium_test_agent``; we keep
    the try/except guard for compatibility but the Selenium fallback is the standard path.
    """
    try:
        # Optional fast path. ImportError in standalone or HyperExecute.
        from selenium_test_agent.selenium_test.driver_provider import get_cdp  # type: ignore
        session_id = getattr(driver, "session_id", None)
        cdp = get_cdp(session_id)
        if cdp and cdp._bound_loop and cdp._bound_loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                cdp.capture_screenshot(), cdp._bound_loop
            )
            screenshot = future.result(timeout=30)
            return screenshot.data
    except Exception:
        pass
    return get_browser_screenshot_as_base64(driver)
