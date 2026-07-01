"""scroll_until_element — vision-agent SCROLL_UNTIL_ELEMENT verb (no selector).

The generated test code emits, for an off-screen target with no resolvable selector:

    await testmu.scroll_until_element(page, 'verify code button')

This mirrors the record-time locate flow:

1. Capture a FULL-PAGE screenshot.
2. Read page + viewport dims.
3. POST to the locate endpoint (AUTOMIND_URL) with LT Basic auth → image-space
   coordinate.
4. Scale the image-space coordinate to page space using the full-page image
   dims (PNG header).
5. Scroll the viewport so the target is centred.

Step-2 DOM-probe → xpath is intentionally skipped: it only persists a
selector, which a scroll does not need.

This verb is NOT smart-gated — it is a locate/AUTOMIND_URL verb (a sibling of
execute_db), not a TESTMU_AI_API_HOST vision verb. It always performs the work
and raises on a not-found / error result; it never silently passes.
"""
import base64
import logging
import os

import aiohttp

from testmu._helpers._http import create_session
from testmu._helpers._png import _png_dimensions as _shared_png_dimensions

_log = logging.getLogger("testmu")

# locate is on AUTOMIND_URL (NOT the TESTMU_AI_API_HOST vision stack). Fallback
# is the production locate API host.
_AUTOMIND_FALLBACK = "https://kaneai-api.lambdatest.com"
_LOCATE_TIMEOUT = aiohttp.ClientTimeout(total=120)

# Page + viewport dims in one round-trip:
# [scrollWidth, scrollHeight, innerWidth, innerHeight]
_DIMS_JS = (
    "() => [document.documentElement.scrollWidth, "
    "document.documentElement.scrollHeight, window.innerWidth, window.innerHeight]"
)


def _resolve_automind_url() -> str:
    """Resolve AUTOMIND_URL from the environment, with a built-in fallback."""
    return os.environ.get("AUTOMIND_URL", "") or _AUTOMIND_FALLBACK


def _png_dimensions(data: bytes) -> tuple:
    """(width, height) of a PNG from its IHDR header — no Pillow dependency.

    Delegates to the shared _helpers/_png.py reader; re-raises with the
    scroll_until_element context message so callers see a coherent error.
    """
    try:
        return _shared_png_dimensions(data)
    except ValueError:
        raise RuntimeError("scroll_until_element: screenshot is not a valid PNG")


def _build_locate_desktop_payload(description: str, image_b64: str) -> dict:
    """Build the locate endpoint request body.

    Field names and fixed values match the locate API contract: os="desktop",
    platform="web", screen_height/screen_width (NOT height/width).
    """
    return {
        "intent": description,
        "image": image_b64,
        "os": "desktop",
        "platform": "web",
        "screen_height": 0,
        "screen_width": 0,
        "drop_aware": False,
    }


async def scroll_until_element(page, description: str) -> None:
    """Scroll the page until the described (off-screen) element is centred.

    Uses the locate API to find the element's coordinates. Raises on a not-found or
    error result (never silently passes).

    Args:
        page: Playwright page object.
        description: Natural-language description of the target element.

    Raises:
        RuntimeError: When the locate service returns no coordinate ([0,0] / missing),
            on a non-200 response, or on any network/decode failure.
    """
    from testmu._vars import var
    description = var(description)

    _log.info("    [scroll_until_element] target=%s", description[:80])

    # 1. Full-page screenshot via the CDP bypass — page.screenshot(full_page=True)
    #    blocks on document.fonts.ready and hangs behind the LambdaTest grid proxy.
    from testmu._helpers.vision import _capture_full_page_screenshot_b64
    image_b64 = await _capture_full_page_screenshot_b64(page)
    screenshot_bytes = base64.b64decode(image_b64)

    # 2. Page + viewport dims.
    dims = await page.evaluate(_DIMS_JS)
    page_width, page_height, viewport_width, viewport_height = (
        int(dims[0]), int(dims[1]), int(dims[2]), int(dims[3])
    )

    # 3. POST to the locate endpoint.
    endpoint = f"{_resolve_automind_url()}/v2/locate/desktop"
    payload = _build_locate_desktop_payload(description, image_b64)

    try:
        async with create_session() as session:
            async with session.post(endpoint, json=payload, timeout=_LOCATE_TIMEOUT) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise RuntimeError(
                        f"locate API error {resp.status} for {description!r}: {text}"
                    )
                result = await resp.json()
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"scroll_until_element locate failed for {description!r}: {e}") from e

    # The locate API defaults a missing coordinate to [0,0]; both the
    # missing key and an explicit [0,0] mean "not found".
    coordinate = result.get("coordinate", [0, 0])
    if not coordinate or list(coordinate) == [0, 0]:
        raise RuntimeError(
            f"scroll_until_element: element not found for {description!r} "
            f"(coordinate={coordinate}, reason={result.get('reason', '')})"
        )

    raw_x, raw_y = int(coordinate[0]), int(coordinate[1])

    # 4. Read full-page image dims (PNG header) → scale image-space → page-space.
    image_width, image_height = _png_dimensions(screenshot_bytes)
    scale_x = page_width / max(image_width, 1)
    scale_y = page_height / max(image_height, 1)
    page_x = int(raw_x * scale_x)
    page_y = int(raw_y * scale_y)
    _log.info(
        "    [scroll_until_element] image=(%d,%d) page=(%d,%d) scale=(%.3f,%.3f)",
        raw_x, raw_y, page_x, page_y, scale_x, scale_y,
    )

    # 5. Scroll so the target is centred in the viewport (clamp to >= 0).
    target_x = max(0, page_x - viewport_width // 2)
    target_y = max(0, page_y - viewport_height // 2)
    await page.evaluate("([x, y]) => window.scrollTo(x, y)", [target_x, target_y])
    _log.info("    [scroll_until_element] scrolled to (%d,%d)", target_x, target_y)
