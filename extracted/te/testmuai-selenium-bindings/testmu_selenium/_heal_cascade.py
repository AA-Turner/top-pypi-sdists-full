"""V3-native kwarg-based dispatcher over the Heal class.

Public:
    _heal_cascade(*, description, current_selector, current_frame_info, tiers,
                   exception, driver=None, current_action=None) -> HealResult
    HealResult dataclass

Raises AutohealExhausted when all configured tiers miss.
"""
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Optional

from testmu_selenium._heal import Heal
from testmu_selenium._errors import AutohealExhausted, HealTierMiss
from testmu_selenium._helpers._coordinate_resolver import resolve_coordinate, resolve_coordinate_read

_log = logging.getLogger(__name__)


@dataclass
class HealResult:
    selectors: list[dict]
    frame_info: list | None = None
    selector_payload: dict | None = None
    tier_used: str = ""
    latency_ms: int = 0
    attempts_used: int = 0  # parity with the heal framework's HealResult shape
    # DESKTOP_LOCATE resolution path. A DESKTOP_LOCATE hit ALWAYS populates
    # coordinates (viewport CSS pixels from Automind). When the coordinate
    # resolver also derived a verified xpath, `selectors` is populated too —
    # the engine prefers the selector path and keeps coordinates as the
    # in-round fallback. When the
    # resolver returns None, selectors stays [] and the engine dispatches via
    # spec.coord_runner(driver, x, y, ctx) rather than feeding a synthetic
    # placeholder back into findElement. None for selector-only tiers.
    coordinates: tuple[int, int] | None = None


def _synthesize_current_action(description: str, current_selector: list, op_type: str = "click") -> dict:
    """Phase 1: build a minimal current_action dict from the V3 cascade kwargs.
    Future phase (Path α): codegen emits a richer current_action dict explicitly."""
    return {
        "operation_type": op_type,
        "operation_intent": description,
        "instruction_id": "",
        "operation_id": "",
        "use_query_v2": True,
        "version": "v3",
        "selector": current_selector,
        "frame_info": [],
        # The automind /v1/heal endpoints read the query from
        # sub_instruction_obj.operation_dict.queried_value (the same shape the
        # vision_query / textual_query helpers send). Without it the VISION_QUERY
        # tier 500s with KeyError 'operation_dict' server-side, so every
        # selectorless heal (click/clear/upload/...) exhausts the cascade
        # (observed on dev cluster during integration testing).
        "sub_instruction_obj": {
            "operation_dict": {
                "queried_value": description,
            },
        },
    }


def _heal_cascade(
    *,
    description: str,
    current_selector: list,
    current_frame_info: list | None,
    tiers: list[str],
    exception: Exception,
    driver=None,
    current_action: dict | None = None,
    automind_url: Optional[str] = None,
    op_type: str = "click",
) -> HealResult:
    """Run the V3 autoheal cascade across the given tiers.

    Returns HealResult on first successful tier. Raises AutohealExhausted
    if all tiers miss. Driver argument is required when used standalone;
    the host runtime can pre-fill it via the exec namespace. `automind_url`
    overrides the env-var fallback chain inside Heal.__init__ — the host
    threads its canonical AUTEUR_AUTOMIND mapping here so the bindings
    client doesn't 401 against the wrong base URL on dev clusters.
    """
    if driver is None:
        raise ValueError("_heal_cascade: driver argument is required")

    if current_action is None:
        current_action = _synthesize_current_action(description, current_selector, op_type=op_type)

    healer = Heal(current_action, driver, automind_url=automind_url)

    last_miss: Exception | None = None
    start = time.time()

    for tier in tiers:
        _log.info("    [heal] tier=%s attempt", tier)
        try:
            if tier == "LIST_XPATHS":
                resp = healer.list_xpaths()
                payload = json.loads(resp.text)
                xpaths = payload.get("xpaths") or []
                if not xpaths:
                    raise HealTierMiss(tier, "no xpaths returned")
                return HealResult(
                    selectors=[{"selector": x, "isXPath": True, "score": 50} for x in xpaths],
                    frame_info=payload.get("frameInformation"),
                    selector_payload=payload,
                    tier_used=tier,
                    latency_ms=int((time.time() - start) * 1000),
                )

            elif tier == "VISION_QUERY":
                resp = healer.vision_query_v2()
                payload = json.loads(resp.text)
                if payload.get("error"):
                    raise HealTierMiss(tier, payload.get("message", payload["error"]))
                # /v1/heal/vision returns the relocate selector in value/xpath;
                # `vision_query` is a boolean ANSWER field (presence), NOT a
                # selector — never feed it to findElement (it crashes Chrome with
                # InvalidArgumentException: 'value' must be a string). Require a
                # non-empty string selector, else miss so the cascade falls
                # through to the next tier.
                vq = payload.get("value") or payload.get("xpath")
                if not isinstance(vq, str) or not vq.strip():
                    raise HealTierMiss(tier, "no usable selector in response")
                return HealResult(
                    selectors=[{"selector": vq, "isXPath": True, "score": 40}],
                    selector_payload=payload,
                    tier_used=tier,
                    latency_ms=int((time.time() - start) * 1000),
                )

            elif tier == "DESKTOP_LOCATE":
                # desktop_locate() returns (css_x, css_y) or raises HealTierMiss.
                # HealTierMiss (e.g. [0,0] API miss) must occur BEFORE any resolver call.
                css_x, css_y = healer.desktop_locate()
                resolved = resolve_coordinate(driver, css_x, css_y)
                if resolved:
                    _log.info("    [heal] DESKTOP_LOCATE derived_xpath=%s", resolved.xpath)
                    selectors = [{"selector": resolved.xpath, "isXPath": True, "score": 45}]
                else:
                    _log.info("    [heal] DESKTOP_LOCATE derived_xpath=None")
                    selectors = []
                return HealResult(
                    selectors=selectors,
                    coordinates=(css_x, css_y),
                    tier_used=tier,
                    latency_ms=int((time.time() - start) * 1000),
                )

            elif tier == "DESKTOP_LOCATE_FULL_PAGE":
                # Full-page locate tier (spec §9): captures entire page, scales coords to
                # page-CSS space, scrolls target into viewport, then resolves xpath.
                # desktop_locate_full_page() raises HealTierMiss on [0,0]/non-200 BEFORE
                # any scroll or resolver call.
                t0 = time.time()
                page_x, page_y = healer.desktop_locate_full_page()
                # Scroll the target to viewport center.
                vw, vh = driver.execute_script("return [window.innerWidth, window.innerHeight]")
                driver.execute_script(
                    "window.scrollTo(arguments[0], arguments[1])",
                    max(0, page_x - vw // 2),
                    max(0, page_y - vh // 2),
                )
                time.sleep(0.15)
                # Read back actual scroll offsets after the scroll settles.
                scroll_x, scroll_y = driver.execute_script("return [window.scrollX, window.scrollY]")
                # Compute viewport-relative coords, clamped to valid range.
                vx = max(0, min(page_x - scroll_x, vw - 1))
                vy = max(0, min(page_y - scroll_y, vh - 1))
                resolved = resolve_coordinate(driver, vx, vy)
                latency_ms = int((time.time() - t0) * 1000)
                if resolved:
                    _log.info(
                        "    [heal] DESKTOP_LOCATE_FULL_PAGE page=(%d,%d) viewport=(%d,%d) "
                        "xpath=%s latency=%dms",
                        page_x, page_y, vx, vy, resolved.xpath, latency_ms,
                    )
                    selectors = [{"selector": resolved.xpath, "isXPath": True, "score": 45}]
                else:
                    _log.info(
                        "    [heal] DESKTOP_LOCATE_FULL_PAGE page=(%d,%d) viewport=(%d,%d) "
                        "xpath=None latency=%dms",
                        page_x, page_y, vx, vy, latency_ms,
                    )
                    selectors = []
                return HealResult(
                    selectors=selectors,
                    coordinates=(vx, vy),
                    tier_used="DESKTOP_LOCATE_FULL_PAGE",
                    latency_ms=latency_ms,
                )

            elif tier == "DESKTOP_LOCATE_FULL_PAGE_READ":
                # READ-tuned twin of DESKTOP_LOCATE_FULL_PAGE (spec §9): identical full-page
                # locate + scroll-into-view (THE crux that beats the server's
                # selected_attribute='color' viewport clip), but derives the xpath with the
                # NO-CLIMB read resolver so a non-interactable <div>/<span>/<p> read lands on
                # the exact element (correct for non-inherited CSS like background-color).
                t0 = time.time()
                page_x, page_y = healer.desktop_locate_full_page()
                vw, vh = driver.execute_script("return [window.innerWidth, window.innerHeight]")
                driver.execute_script(
                    "window.scrollTo(arguments[0], arguments[1])",
                    max(0, page_x - vw // 2), max(0, page_y - vh // 2),
                )
                time.sleep(0.15)
                scroll_x, scroll_y = driver.execute_script("return [window.scrollX, window.scrollY]")
                vx = max(0, min(page_x - scroll_x, vw - 1))
                vy = max(0, min(page_y - scroll_y, vh - 1))
                resolved = resolve_coordinate_read(driver, vx, vy)
                latency_ms = int((time.time() - t0) * 1000)
                selectors = (
                    [{"selector": resolved.xpath, "isXPath": True, "score": 45}] if resolved else []
                )
                _log.info("    [heal] DESKTOP_LOCATE_FULL_PAGE_READ page=(%d,%d) viewport=(%d,%d) "
                          "xpath=%s latency=%dms", page_x, page_y, vx, vy,
                          resolved.xpath if resolved else None, latency_ms)
                return HealResult(
                    selectors=selectors, coordinates=(vx, vy),
                    tier_used="DESKTOP_LOCATE_FULL_PAGE_READ", latency_ms=latency_ms,
                )

            else:
                raise ValueError(f"unknown heal tier: {tier}")

        except HealTierMiss as miss:
            _log.info("    [heal] tier=%s MISS — %s", tier, miss)
            last_miss = miss
            continue
        except Exception as e:
            # Other failures (HTTP timeout, malformed JSON) — treat as miss for this tier
            _log.warning("    [heal] tier=%s ERROR — %s: %s", tier, type(e).__name__, e)
            last_miss = HealTierMiss(tier, str(e))
            continue

    _log.error("    [heal] cascade exhausted — original=%s last_miss=%s", type(exception).__name__, last_miss)
    raise AutohealExhausted(original=exception, last_miss=last_miss)
