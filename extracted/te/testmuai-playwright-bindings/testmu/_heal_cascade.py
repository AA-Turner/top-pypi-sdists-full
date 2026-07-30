"""Heal cascade for V3 Playwright.

Behavioural parity with Selenium's testmu_selenium._heal_cascade._heal_cascade,
simplified for Playwright:

- Drops LIST_XPATHS tier (Playwright's selector engine subsumes the
  "re-rank xpaths against current DOM" use case).
- Drops COORDINATE (POST /v1/heal/coordinates); replaced by DESKTOP_LOCATE
  (POST /v2/locate/desktop on {AUTOMIND_URL}) which takes a viewport screenshot
  and returns image-space coordinates scaled to CSS viewport pixels. DESKTOP_LOCATE
  is the primary default tier; VISION_QUERY (POST /v1/heal/vision) survives via
  per-verb tier overrides (e.g. scroll_into_view) or when listed alongside
  DESKTOP_LOCATE in a verb's tiers tuple.

Per-verb tier overrides live in the verb specs (scroll_into_view uses
VISION_QUERY only; set_input_files uses DESKTOP_LOCATE + VISION_QUERY).
"""
from __future__ import annotations

import asyncio
import base64
import logging
import os
import uuid
from dataclasses import dataclass
from typing import Optional

import aiohttp

from testmu._errors import AutohealExhausted
from testmu._helpers._coordinate_resolver import resolve_coordinate
from testmu._helpers._http import create_session
from testmu._helpers._png import _png_dimensions
from testmu._helpers.vision import (
    _capture_full_page_screenshot_b64,
    _capture_screenshot_b64,
    get_v3_vision_target,
)

_log = logging.getLogger("testmu.heal_cascade")

# Locate is on AUTOMIND_URL (NOT the TESTMU_AI_API_HOST vision stack).
# Fallback mirrors auteur's get_automind_url default (utils/constants.py AUTEUR_AUTOMIND).
_AUTOMIND_FALLBACK = "https://kaneai-api.lambdatest.com"
_LOCATE_TIMEOUT = aiohttp.ClientTimeout(total=120)

# Viewport dims in one round-trip: [innerWidth, innerHeight]
_VIEWPORT_JS = "() => [window.innerWidth, window.innerHeight]"

_DEFAULT_HEAL_TIERS: tuple[str, ...] = ("DESKTOP_LOCATE",)

# Maximum number of attempts before giving up. Each attempt takes a fresh
# screenshot + viewport dims + POST so a transient infra blip can recover.
_MAX_LOCATE_ATTEMPTS = 3

# Aspect-ratio tolerance: warn when image and viewport ratios differ by more
# than this fraction (2 % covers typical rounding at unusual DPR values).
_ASPECT_RATIO_TOLERANCE = 0.02


@dataclass(frozen=True)
class HealResult:
    """Output of a successful heal tier.

    Three valid shapes (a hit always sets at least one field):

    - ``selector_xpath`` only — VISION_QUERY hit.
    - ``coordinates`` only — DESKTOP_LOCATE hit where the resolver could not
      derive a verified xpath (shadow DOM / iframe / verification failure).
    - Both — DESKTOP_LOCATE hit with a resolver-derived verified xpath
      (spec §3.2). Consumer (_run_verb) prefers ``selector_xpath``, keeping
      ``coordinates`` as the in-round fallback for the next recoverable
      failure without re-entering the cascade.
    """
    tier_used: str
    selector_xpath: Optional[str] = None
    coordinates: Optional[tuple[int, int]] = None
    frame_info: Optional[dict] = None


def _resolve_automind_url() -> str:
    """Resolve AUTOMIND_URL from the environment, with the host runtime fallback."""
    return os.environ.get("AUTOMIND_URL", "") or _AUTOMIND_FALLBACK


async def get_v3_desktop_locate_target(
    page, description: str, method_name: str = "click", *, drop_aware: bool = False
) -> Optional[tuple[int, int]]:
    """DESKTOP_LOCATE client — POST to {AUTOMIND_URL}/v2/locate/desktop.

    Takes a VIEWPORT screenshot (not full-page), validates the PNG before
    posting, posts a lean body per the locked design contract, and scales the
    returned image-space coordinate to viewport CSS pixels.

    Returns (css_x, css_y) — clamped to [0, viewport_dim-1] — on hit, or
    None on miss / non-200 / transport error.

    Retry behaviour:
    - Up to _MAX_LOCATE_ATTEMPTS=3 attempts; each attempt takes a fresh
      screenshot + viewport dims + POST.
    - Transport exceptions (aiohttp.ClientError, asyncio.TimeoutError, OSError)
      and 5xx responses are retried after asyncio.sleep(1).
    - 4xx responses are never retried — return None immediately.
    - An invalid PNG screenshot is never retried — the path is deterministic.
    - Never raises; always returns Optional[tuple[int, int]].

    Miss detection: the /v2/locate/desktop endpoint returns HTTP 200 with
    ``coordinate==[0,0]`` on not-found (NOT 404). Missing/null/[0,0]/len<2
    are all treated as miss → None.

    Auth: LT Basic auth via create_session() (NOT _v3_auth_headers/vision-host
    auth). Base URL from AUTOMIND_URL env var, same as scroll_until_element.

    Note: ``method_name`` is accepted for API symmetry with Selenium's heal
    helper but is NOT transmitted in the lean request body — the endpoint
    only needs intent + image + fixed metadata fields.

    ``drop_aware`` (default False) threads into the POST body's ``drop_aware``
    field. The single-element heal callers (click/fill/...) leave it False; the
    drag-drop heal sets it True when locating a drag TARGET (drop zone) so the
    model resolves the droppable rather than the dragged item (selenium parity,
    spec §10.1). Non-breaking: existing call sites keep the False default.
    """
    # Short-circuit on empty description — no screenshot, no HTTP call.
    if not description:
        _log.warning("[heal desktop_locate] empty description — skipping locate call")
        return None

    for attempt in range(_MAX_LOCATE_ATTEMPTS):
        try:
            # --- Fresh screenshot + viewport dims each attempt -----------------
            # (so a page mutation between retries is reflected in the payload)
            # Capture via CDP (Page.captureScreenshot) rather than
            # page.screenshot(): the high-level API blocks on
            # document.fonts.ready + animation-frame stability and hangs behind
            # the LambdaTest grid proxy ("Page.screenshot: Timeout 10000ms
            # exceeded"). See vision._capture_screenshot_b64.
            image_b64 = await _capture_screenshot_b64(page)
            screenshot_bytes = base64.b64decode(image_b64)

            # Validate PNG BEFORE the POST; a garbage screenshot must not
            # burn the API call. This path is deterministic — no retry.
            try:
                image_width, image_height = _png_dimensions(screenshot_bytes)
            except ValueError as e:
                _log.warning(
                    "[heal desktop_locate] invalid PNG screenshot for %r: %s",
                    description[:80], e,
                )
                return None

            dims = await page.evaluate(_VIEWPORT_JS)
            viewport_width, viewport_height = int(dims[0]), int(dims[1])

            # Warn when image and viewport aspect ratios diverge by more
            # than the tolerance. This is a diagnostic hint (e.g. DPR mismatch
            # between capture and render context) — never blocks.
            if viewport_width > 0 and viewport_height > 0 and image_height > 0:
                img_ratio = image_width / image_height
                vp_ratio = viewport_width / viewport_height
                if abs(img_ratio - vp_ratio) / vp_ratio > _ASPECT_RATIO_TOLERANCE:
                    _log.warning(
                        "[heal desktop_locate] aspect ratio mismatch for %r: "
                        "image=%.4f viewport=%.4f",
                        description[:80], img_ratio, vp_ratio,
                    )

            # --- Build and POST payload ----------------------------------------
            endpoint = f"{_resolve_automind_url()}/v2/locate/desktop"
            payload = {
                "intent": description,
                "image": image_b64,
                "os": "desktop",
                "platform": "web",
                "screen_width": viewport_width,
                "screen_height": viewport_height,
                "drop_aware": drop_aware,
                "request_id": uuid.uuid4().hex[:16],
                "a11y_flatten": [],
            }

            result = None
            async with create_session() as session:
                async with session.post(
                    endpoint, json=payload, timeout=_LOCATE_TIMEOUT
                ) as resp:
                    status = resp.status
                    if 400 <= status < 500:
                        # 4xx: client error — retrying won't help.
                        _log.warning(
                            "[heal desktop_locate] 4xx status=%d for %r — not retrying",
                            status, description[:80],
                        )
                        return None
                    if status != 200:
                        # 5xx or unexpected: transient infra issue — schedule retry.
                        _log.warning(
                            "[heal desktop_locate] non-200 status=%d for %r "
                            "(attempt %d/%d)",
                            status, description[:80], attempt + 1, _MAX_LOCATE_ATTEMPTS,
                        )
                    else:
                        result = await resp.json()

            if result is None:
                if attempt < _MAX_LOCATE_ATTEMPTS - 1:
                    await asyncio.sleep(1)
                continue

            # --- Miss detection -----------------------------------------------
            # /v2/locate/desktop returns 200+[0,0] for "not found" (NOT 404).
            coordinate = result.get("coordinate")
            if (
                not coordinate
                or len(coordinate) < 2
                or list(coordinate) == [0, 0]
            ):
                _log.info(
                    "[heal desktop_locate] MISS for %r (coordinate=%r)",
                    description[:80], coordinate,
                )
                return None

            raw_x, raw_y = float(coordinate[0]), float(coordinate[1])

            # --- Scale image-space → viewport CSS pixels ----------------------
            # image_width/height from PNG IHDR (= device-pixel dimensions);
            # dividing by them converts image pixels → CSS pixels via viewport dims.
            css_x = int(raw_x * viewport_width / max(image_width, 1))
            css_y = int(raw_y * viewport_height / max(image_height, 1))

            # Clamp to valid viewport range so downstream mouse.click
            # never fires outside the window bounds.
            css_x = max(0, min(css_x, viewport_width - 1))
            css_y = max(0, min(css_y, viewport_height - 1))

            _log.info(
                "[heal desktop_locate] HIT image=(%s,%s) image_dims=(%d,%d) "
                "viewport=(%d,%d) css=(%d,%d) confidence=%r",
                raw_x, raw_y, image_width, image_height,
                viewport_width, viewport_height, css_x, css_y,
                result.get("confidence"),
            )
            return css_x, css_y

        except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as e:
            # Transport-level failure — worth retrying (server restart, blip).
            _log.warning(
                "[heal desktop_locate] transport error for %r "
                "(attempt %d/%d): %s",
                description[:80], attempt + 1, _MAX_LOCATE_ATTEMPTS, e,
            )
            if attempt < _MAX_LOCATE_ATTEMPTS - 1:
                await asyncio.sleep(1)
        except Exception as e:
            # Unexpected error (e.g. page closed, JS evaluation failure) —
            # not retryable, return None so the cascade can fall to next tier.
            _log.warning(
                "[heal desktop_locate] unexpected error for %r: %s",
                description[:80], e,
            )
            return None

    _log.warning(
        "[heal desktop_locate] all %d attempts exhausted for %r",
        _MAX_LOCATE_ATTEMPTS, description[:80],
    )
    return None


async def _run_desktop_locate_tier(page, description: str, verb_name: str) -> Optional[HealResult]:
    """DESKTOP_LOCATE tier — POST /v2/locate/desktop (AUTOMIND_URL), viewport
    screenshot, image-space coordinate scaled to CSS viewport pixels. After a
    successful locate, attempts to derive a verified XPath via resolve_coordinate
    so the engine can act with full element semantics (spec §3.2). Coordinates
    are always populated when the tier hits — they are the in-round fallback
    when the xpath attempt fails. Returns None on miss so the cascade can try
    the next tier."""
    coords = await get_v3_desktop_locate_target(page, description, method_name=verb_name)
    if coords is None:
        return None
    resolved = await resolve_coordinate(page, coords[0], coords[1])
    if resolved is not None:
        _log.info("    [heal] DESKTOP_LOCATE derived_xpath=%s", resolved.xpath)
    else:
        _log.info("    [heal] DESKTOP_LOCATE derived_xpath=None")
    return HealResult(
        tier_used="DESKTOP_LOCATE",
        selector_xpath=(resolved.xpath if resolved is not None else None),
        coordinates=coords,
    )


async def get_v3_desktop_locate_full_page_target(
    page, description: str
) -> Optional[tuple[int, int]]:
    """DESKTOP_LOCATE_FULL_PAGE client — full-page screenshot, POST to {AUTOMIND_URL}/v2/locate/desktop.

    Unlike DESKTOP_LOCATE (viewport screenshot), this captures the entire page once
    (reused across retries — expensive capture) and sends it with screen_width=0/
    screen_height=0 per the full-page image contract. Returns page-space (CSS pixel)
    coordinates; the tier dispatcher is responsible for scrolling into view and
    converting to viewport coords.

    Returns (page_x, page_y) — clamped to [0, page_dim-1] — on hit, or
    None on miss / non-200 / transport error / invalid PNG.

    Retry behaviour mirrors DESKTOP_LOCATE:
    - Up to _MAX_LOCATE_ATTEMPTS=3 attempts; screenshot is taken ONCE and reused.
    - Transport exceptions (aiohttp.ClientError, asyncio.TimeoutError, OSError)
      and non-4xx non-200 responses are retried after asyncio.sleep(1).
    - 4xx responses are never retried — return None immediately.
    - An invalid PNG screenshot is never retried — path is deterministic.
    - Never raises; always returns Optional[tuple[int, int]].
    """
    # Short-circuit on empty description — no screenshot, no HTTP call.
    if not description:
        _log.warning("[heal desktop_locate_full_page] empty description — skipping")
        return None

    # Full-page screenshot once — expensive capture, reused across retries.
    # CDP bypass (Page.captureScreenshot + captureBeyondViewport) instead of
    # page.screenshot(full_page=True): the high-level API blocks on
    # document.fonts.ready and hangs behind the LambdaTest grid proxy
    # ("Page.screenshot: Timeout ... exceeded"). See
    # vision._capture_full_page_screenshot_b64.
    image_b64 = await _capture_full_page_screenshot_b64(page)
    screenshot_bytes = base64.b64decode(image_b64)

    # Validate PNG BEFORE any POST — deterministic path, no retry.
    try:
        image_width, image_height = _png_dimensions(screenshot_bytes)
    except ValueError as e:
        _log.warning(
            "[heal desktop_locate_full_page] invalid PNG screenshot for %r: %s",
            description[:80], e,
        )
        return None

    # Page dims from full document scroll dimensions.
    dims = await page.evaluate(
        "() => [document.documentElement.scrollWidth, document.documentElement.scrollHeight]"
    )
    page_width, page_height = int(dims[0]), int(dims[1])

    for attempt in range(_MAX_LOCATE_ATTEMPTS):
        try:
            endpoint = f"{_resolve_automind_url()}/v2/locate/desktop"
            # screen_width=0, screen_height=0 per full-page image contract.
            payload = {
                "intent": description,
                "image": image_b64,
                "os": "desktop",
                "platform": "web",
                "screen_width": 0,
                "screen_height": 0,
                "drop_aware": False,
                "request_id": uuid.uuid4().hex[:16],
                "a11y_flatten": [],
            }

            result = None
            async with create_session() as session:
                async with session.post(
                    endpoint, json=payload, timeout=_LOCATE_TIMEOUT
                ) as resp:
                    status = resp.status
                    if 400 <= status < 500:
                        _log.warning(
                            "[heal desktop_locate_full_page] 4xx status=%d for %r — not retrying",
                            status, description[:80],
                        )
                        return None
                    if status != 200:
                        _log.warning(
                            "[heal desktop_locate_full_page] non-200 status=%d for %r "
                            "(attempt %d/%d)",
                            status, description[:80], attempt + 1, _MAX_LOCATE_ATTEMPTS,
                        )
                    else:
                        result = await resp.json()

            if result is None:
                if attempt < _MAX_LOCATE_ATTEMPTS - 1:
                    await asyncio.sleep(1)
                continue

            # Miss detection — /v2/locate/desktop returns 200+[0,0] for not-found.
            coordinate = result.get("coordinate")
            if (
                not coordinate
                or len(coordinate) < 2
                or list(coordinate) == [0, 0]
            ):
                _log.info(
                    "[heal desktop_locate_full_page] MISS for %r (coordinate=%r)",
                    description[:80], coordinate,
                )
                return None

            raw_x, raw_y = float(coordinate[0]), float(coordinate[1])

            # Scale image-space → page CSS pixels.
            page_x = int(raw_x * page_width / max(image_width, 1))
            page_y = int(raw_y * page_height / max(image_height, 1))

            # Clamp to valid page range.
            page_x = max(0, min(page_x, page_width - 1))
            page_y = max(0, min(page_y, page_height - 1))

            _log.info(
                "[heal desktop_locate_full_page] HIT image=(%s,%s) image_dims=(%d,%d) "
                "page_dims=(%d,%d) page_css=(%d,%d) confidence=%r",
                raw_x, raw_y, image_width, image_height,
                page_width, page_height, page_x, page_y,
                result.get("confidence"),
            )
            return page_x, page_y

        except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as e:
            _log.warning(
                "[heal desktop_locate_full_page] transport error for %r "
                "(attempt %d/%d): %s",
                description[:80], attempt + 1, _MAX_LOCATE_ATTEMPTS, e,
            )
            if attempt < _MAX_LOCATE_ATTEMPTS - 1:
                await asyncio.sleep(1)
        except Exception as e:
            _log.warning(
                "[heal desktop_locate_full_page] unexpected error for %r: %s",
                description[:80], e,
            )
            return None

    _log.warning(
        "[heal desktop_locate_full_page] all %d attempts exhausted for %r",
        _MAX_LOCATE_ATTEMPTS, description[:80],
    )
    return None


async def _run_desktop_locate_full_page_tier(
    page, description: str, verb_name: str
) -> Optional[HealResult]:
    """DESKTOP_LOCATE_FULL_PAGE tier — full-page screenshot, scroll-into-viewport,
    xpath derivation (spec §9).

    1. Calls get_v3_desktop_locate_full_page_target to get page-space coordinates.
       Miss (None) → return None immediately, before any scroll or resolver side effect.
    2. Scrolls to center the target in the viewport.
    3. Reads back scroll offsets to compute viewport-relative coordinates.
    4. Attempts to derive a verified XPath via resolve_coordinate.

    Returns None on miss so the cascade can try the next tier.
    """
    coords = await get_v3_desktop_locate_full_page_target(page, description)
    if coords is None:
        return None

    page_x, page_y = coords

    # Get viewport dims.
    vp = await page.evaluate("() => [window.innerWidth, window.innerHeight]")
    vw, vh = int(vp[0]), int(vp[1])

    # Scroll to center the target in the viewport.
    await page.evaluate(
        "([px, py, vw, vh]) => window.scrollTo(Math.max(0, px - Math.floor(vw/2)), Math.max(0, py - Math.floor(vh/2)))",
        [page_x, page_y, vw, vh],
    )

    # Settle after scroll.
    await asyncio.sleep(0.15)

    # Read back scroll offsets.
    scroll = await page.evaluate("() => [window.scrollX, window.scrollY]")
    scroll_x, scroll_y = int(scroll[0]), int(scroll[1])

    # Compute viewport-relative coordinates.
    vx = max(0, min(page_x - scroll_x, vw - 1))
    vy = max(0, min(page_y - scroll_y, vh - 1))

    # Derive verified xpath.
    resolved = await resolve_coordinate(page, vx, vy)
    if resolved is not None:
        _log.info(
            "    [heal] DESKTOP_LOCATE_FULL_PAGE page=(%d,%d) viewport=(%d,%d) derived_xpath=%s",
            page_x, page_y, vx, vy, resolved.xpath,
        )
    else:
        _log.info(
            "    [heal] DESKTOP_LOCATE_FULL_PAGE page=(%d,%d) viewport=(%d,%d) derived_xpath=None",
            page_x, page_y, vx, vy,
        )

    return HealResult(
        tier_used="DESKTOP_LOCATE_FULL_PAGE",
        selector_xpath=(resolved.xpath if resolved is not None else None),
        coordinates=(vx, vy),
    )


async def _run_vision_query_tier(page, description: str, verb_name: str) -> Optional[HealResult]:
    """VISION_QUERY tier — posts to the vision heal endpoint, reads ``value``
    or ``xpath``. Mirrors Selenium _heal_cascade.py selector reading.
    Returns None on miss."""
    resp = await get_v3_vision_target(page, description, method_name=verb_name)
    if not isinstance(resp, dict):
        return None
    if resp.get("error"):
        return None
    raw = resp.get("value") or resp.get("xpath")
    if not isinstance(raw, str) or not raw.strip():
        return None
    return HealResult(tier_used="VISION_QUERY", selector_xpath=raw.strip())


_TIER_DISPATCHERS = {
    "DESKTOP_LOCATE": _run_desktop_locate_tier,
    "DESKTOP_LOCATE_FULL_PAGE": _run_desktop_locate_full_page_tier,
    "VISION_QUERY": _run_vision_query_tier,
}


async def _heal_cascade(
    *,
    page,
    description: str,
    verb_name: str,
    current_selector: Optional[str] = None,
    tiers: Optional[tuple[str, ...]] = None,
    last_exception: Optional[Exception] = None,
) -> HealResult:
    """Run heal tiers in order until one returns an actionable result.

    Raises AutohealExhausted if every tier misses. The ``last_exception``
    chains via ``from`` so the original locator timeout (or whatever) stays
    on the traceback.

    Args:
        page: Playwright page.
        description: Human-readable element intent (carried in payload
            current_action.operation_intent and operation_dict.queried_value).
        verb_name: Method that triggered the heal — forwarded as
            current_action.operation_type so the LLM understands intent.
        current_selector: Selector that just failed. Reserved for future
            payload enhancements; not transmitted today (mirrors Selenium
            binding usage which sends selector: []).
        tiers: Tier order override. Default: DESKTOP_LOCATE only.
        last_exception: The exception that triggered the heal. Chained via
            ``from`` onto AutohealExhausted so the original failure stays
            visible.
    """
    _ = current_selector  # reserved for future use

    if tiers is None:
        tiers = _DEFAULT_HEAL_TIERS

    # Entering the cascade means the authored locator didn't resolve, so flag the step as auto-healing now (even if the cascade later exhausts).
    # Local import avoids an import cycle with _step.
    from testmu._step import mark_autoheal
    mark_autoheal()

    for tier in tiers:
        dispatcher = _TIER_DISPATCHERS.get(tier)
        if dispatcher is None:
            _log.warning("[heal] unknown tier %r — skipping", tier)
            continue
        _log.info("[heal] tier=%s for %r", tier, description[:80])
        try:
            result = await dispatcher(page, description, verb_name)
        except Exception as e:
            _log.warning("[heal] tier=%s raised: %s", tier, e)
            result = None
        if result is not None:
            _log.info(
                "[heal] tier=%s HIT (selector=%r, coords=%s)",
                tier, result.selector_xpath, result.coordinates,
            )
            return result
        _log.info("[heal] tier=%s MISS", tier)

    raise AutohealExhausted(
        f"heal cascade exhausted for {description!r} ({verb_name})"
    ) from last_exception
