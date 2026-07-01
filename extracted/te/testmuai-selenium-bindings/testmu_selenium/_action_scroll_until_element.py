"""High-level scroll_until_element action — V3 vision-agent SCROLL_UNTIL_ELEMENT.

Emitted by V3 code-export for an off-screen target with no selector:

    testmu_selenium.scroll_until_element(driver, description='verify code button')

This MIRRORS the vision agent's record-time Step-1 locate flow
(full-page locate → scroll to centre), NOT the heal
cascade / LIST_XPATHS tier (that xpath tier was retired).

Step-1 flow:
  1. Full-page screenshot (CDP captureBeyondViewport) via capture_full_page_screenshot.
  2. Read page + viewport dims from the live DOM.
  3. POST to {AUTOMIND_URL}/v2/locate/desktop (lean locate body; Basic auth header).
  4. Scale the returned image-space coordinate to page space using the decoded
     full-page image dims.
  5. window.scrollTo() so the target is centred in the viewport (clamped at 0).

The vision agent's Step-2 (viewport re-locate + DOM probe -> persisted xpath) is intentionally
SKIPPED: it only persists a selector at record time. Centering the viewport is the
action outcome at runtime.

On not-found ([0,0] / missing coordinate) or a non-200 locate response, raises
NoSuchElementException — consistent with the empty-selector heal contract and what
generated test.py catches. Never silently passes.
"""
from __future__ import annotations

import base64
import logging
import os

from selenium.common.exceptions import NoSuchElementException

from testmu_selenium._helpers._http import make_http_request_with_retry
from testmu_selenium._helpers._png import _png_dimensions as _shared_png_dimensions
from testmu_selenium._helpers._screenshot import capture_full_page_screenshot

_log = logging.getLogger(__name__)


def _png_dimensions(data: bytes) -> tuple:
    """(width, height) of a PNG from its IHDR header — delegates to _helpers._png.

    Preserves the pre-existing NoSuchElementException contract for this module:
    scroll_until_element callers (and generated test.py code) expect
    NoSuchElementException, not ValueError. The shared helper raises ValueError;
    we translate here so the public interface is unchanged.
    """
    try:
        return _shared_png_dimensions(data)
    except ValueError:
        raise NoSuchElementException(
            "scroll_until_element: screenshot is not a valid PNG"
        )

# JS to read page + viewport dimensions in one round-trip.
_DIMS_SCRIPT = (
    "return [document.documentElement.scrollWidth, "
    "document.documentElement.scrollHeight, "
    "window.innerWidth, window.innerHeight]"
)


def _resolve_automind_url() -> str:
    """Read the binding's single config value for the automind URL.

    The value is initialized at import from env (AUTEUR_AUTOMIND > AUTOMIND_URL >
    prod default) and is overridable by configure(automind_url=...) so the host
    can inject the correct URL without mutating os.environ.
    """
    from testmu_selenium import _config
    return _config.get("automind_url")


def _build_auth_headers() -> dict:
    """Basic auth from LT_USERNAME:LT_ACCESS_KEY — mirrors _heal._make_auth_headers."""
    username = os.getenv("LT_USERNAME", "")
    accesskey = os.getenv("LT_ACCESS_KEY", "")
    token = base64.b64encode(f"{username}:{accesskey}".encode()).decode()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {token}",
    }


def _build_locate_desktop_payload(intent: str, image_base64: str) -> dict:
    """Lean locate body — matches the /v2/locate/desktop request format.

    NOTE: field names are screen_height/screen_width (per locate API spec), not height/width.
    """
    return {
        "intent": intent,
        "image": image_base64,
        "os": "desktop",
        "platform": "web",
        "screen_height": 0,
        "screen_width": 0,
        "drop_aware": False,
    }


def scroll_until_element(driver, *, description: str = "") -> None:
    """Scroll the viewport until the described off-screen element is centred.

    Args:
        driver: Selenium WebDriver.
        description: Natural-language description of the target element (the
            vision-agent intent). This is the only locator available — there is
            no selector for SCROLL_UNTIL_ELEMENT.

    Raises:
        NoSuchElementException: if automind cannot locate the target ([0,0] /
            missing coordinate) or the locate API returns a non-200 status.
    """
    intent = description or ""
    _log.info("scroll_until_element: intent=%r", intent)

    # 1. Full-page screenshot (captureBeyondViewport).
    image_base64 = capture_full_page_screenshot(driver)

    # 2. Page + viewport dims from the live DOM.
    dims = driver.execute_script(_DIMS_SCRIPT)
    page_width, page_height, viewport_width, viewport_height = (
        int(dims[0]), int(dims[1]), int(dims[2]), int(dims[3])
    )
    _log.info(
        "scroll_until_element: page %sx%s viewport %sx%s",
        page_width, page_height, viewport_width, viewport_height,
    )

    # 3. POST to /v2/locate/desktop.
    endpoint = f"{_resolve_automind_url()}/v2/locate/desktop"
    headers = _build_auth_headers()
    payload = _build_locate_desktop_payload(intent, image_base64)

    response = make_http_request_with_retry(
        "POST", url=endpoint, headers=headers, json_data=payload,
    )
    if response.status_code != 200:
        raise NoSuchElementException(
            f"scroll_until_element: locate API returned status "
            f"{response.status_code} for intent {intent!r}: {response.text}"
        )

    api_resp = response.json()
    coordinate = api_resp.get("coordinate", [0, 0]) or [0, 0]
    if not isinstance(coordinate, (list, tuple)) or len(coordinate) < 2 or list(coordinate[:2]) == [0, 0]:
        raise NoSuchElementException(
            f"scroll_until_element: element not found for intent {intent!r} "
            f"(coordinate={coordinate!r}, reason={api_resp.get('reason', '')!r})"
        )

    raw_x, raw_y = coordinate[0], coordinate[1]

    # 4. Scale image-space coordinate to page space using the SAME image dims,
    #    read from the PNG header (no Pillow dependency — keep the bundle slim).
    img_b64 = image_base64.split(",", 1)[1] if "," in image_base64 else image_base64
    image_width, image_height = _png_dimensions(base64.b64decode(img_b64))

    scale_x = page_width / max(image_width, 1)
    scale_y = page_height / max(image_height, 1)
    page_x = int(raw_x * scale_x)
    page_y = int(raw_y * scale_y)
    _log.info(
        "scroll_until_element: image=(%s,%s) page=(%s,%s) scale=(%.3f,%.3f)",
        raw_x, raw_y, page_x, page_y, scale_x, scale_y,
    )

    # 5. Scroll to centre the target (clamped at 0).
    target_x = max(0, page_x - viewport_width // 2)
    target_y = max(0, page_y - viewport_height // 2)
    driver.execute_script(
        "window.scrollTo(arguments[0], arguments[1])", target_x, target_y
    )
    _log.info("scroll_until_element: scrollTo(%s, %s)", target_x, target_y)
    return None
