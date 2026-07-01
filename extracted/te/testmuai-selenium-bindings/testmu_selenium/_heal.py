"""Heal class — AUTOMIND HTTP client for V3-Selenium autoheal cascade.

Extracted from V2 source.
Trimmed to the methods used by the V3 cascade: list_xpaths, get_outer_html,
textual_query_v2, vision_query_v2, desktop_locate.

Constructor refactored: takes current_action: dict explicitly (V2 read it from
the operations_meta_data global via get_meta_data_value(); V3 has no such global).

SIMPLIFICATIONS vs V2 source:
- Constructor: removed get_meta_data_value() / user_data global reads; caller
  passes current_action dict directly; identity/credential fields come from
  explicit kwargs or env vars.
- list_xpaths / get_outer_html: IS_WEBSOCKET_AVAILABLE branch (stop/resume video,
  inject_script for Safari) dropped — those rely on internal WebSocket transport
  infrastructure not available in HyperExecute bindings. Mobile tagify branch
  retained (guarded by self.mobile_tagify truthiness).
- desktop_locate: viewport screenshot (NOT full-page), POST to /v2/locate/desktop
  with lean body, scale returned image-pixel coord to viewport-CSS-px.
  Replaces the legacy browser_coordinate (/v1/heal/coordinates) tier.
- vision_query_v2: duplicate "version" key in V2 payload dict collapsed to single
  entry — second value wins in Python; ported as single entry.
- vision_query_v2: IS_WEBSOCKET_AVAILABLE-gated create_and_upload_screenshot
  post-call (present in vision_query V1) is NOT in vision_query_v2 source; not
  ported.

Guarded imports:
- selenium_test_agent.*: host runtime only, guarded in _helpers._screenshot._take_screenshot
"""
from __future__ import annotations

import base64
import json
import logging
import os
import traceback
import uuid
from typing import Any, Optional

import httpx
from selenium.webdriver.common.by import By

from testmu_selenium import _config
from testmu_selenium._helpers._http import make_http_request_with_retry
from testmu_selenium._helpers._png import _png_dimensions
from testmu_selenium._helpers._screenshot import (
    _take_screenshot,
    capture_full_page_screenshot,
    get_browser_screenshot_as_base64,
    make_tagged_screenshot,
)
from testmu_selenium._helpers._tagify import MOBILE_TAGIFY_SCRIPT
from testmu_selenium._helpers._frame import switch_to_frame_by_xpath
from testmu_selenium._errors import HealTierMiss

_log = logging.getLogger(__name__)


class Heal:
    """AUTOMIND HTTP client for V3-Selenium autoheal cascade.

    Public methods (used by _heal_cascade dispatcher):
        list_xpaths()              — re-rank xpaths against current DOM
        get_outer_html()           — produce outer-HTML snapshot for textual_query
        textual_query_v2(...)      — textual-similarity query
        vision_query_v2()          — vision-based selector inference
        desktop_locate(drop_aware=False) — viewport /v2/locate/desktop → (css_x, css_y)
        desktop_locate_full_page() — full-page /v2/locate/desktop → (page_x, page_y)
    """

    def __init__(
        self,
        current_action: dict,
        driver,
        *,
        test_id: Optional[str] = None,
        username: Optional[str] = None,
        accesskey: Optional[str] = None,
        commit_id: Optional[str] = None,
        org_id: Optional[int] = None,
        automind_url: Optional[str] = None,
    ):
        self.current_action = current_action
        self.driver = driver
        self.session_id = driver.session_id
        self.test_id = test_id if test_id is not None else os.getenv("TEST_ID", "")
        self.username = username if username is not None else os.getenv("LT_USERNAME", "")
        self.accesskey = accesskey if accesskey is not None else os.getenv("LT_ACCESS_KEY", "")
        self.commit_id = commit_id if commit_id is not None else os.getenv("COMMIT_ID", "")
        env_org_id = os.getenv("ORG_ID", "0") or "0"
        self.org_id = int(org_id) if org_id is not None else int(env_org_id)
        # Explicit kwarg wins; otherwise use the binding's single config value
        # _config.get("automind_url"), which is initialized from env at import
        # (AUTEUR_AUTOMIND > AUTOMIND_URL > prod default) and is overridable by
        # configure(automind_url=...) so the host can inject the correct URL
        # without mutating os.environ.
        self.automind_url = automind_url or _config.get("automind_url")
        self.use_query_v2: bool = current_action.get("use_query_v2", True)
        self.version: str = current_action.get("version", "v3")
        self.code_export_id: str = uuid.uuid4().hex[:16]

        # State populated during method calls:
        self.prev_actions: list = []
        self.tagified_image: str = ""
        self.untagged_image_base64: str = ""
        self.xpath_mapping: dict = {}
        self.tags_description: dict = {}
        self.page_source: str = ""
        self.image_base64: str = ""
        self.dimensions: list = []
        self.operation: str = ""
        self.mobile_tagify = MOBILE_TAGIFY_SCRIPT  # None in standalone / HyperExecute

    # ---------------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------------

    def _take_screenshot(self) -> str:
        """CDP when available, Selenium fallback (delegates to module-level helper)."""
        return _take_screenshot(self.driver)

    def _make_auth_headers(self) -> dict:
        auth_token = base64.b64encode(
            f"{self.username}:{self.accesskey}".encode()
        ).decode()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_token}",
        }

    def execute_async_js(self, script: str) -> Any:
        """Execute JS as an async Promise and return the resolved value.

        Verbatim port from V2 source.
        """
        result = self.driver.execute_script(f"""
        return new Promise((resolve) => {{
            (async function() {{
                try {{
                    const result = await {script};
                    resolve(result);
                }} catch (error) {{
                    console.error('Async JS error:', error);
                    resolve(null);
                }}
            }})();
        }});
        """)
        return result

    # ---------------------------------------------------------------------------
    # Tier methods
    # ---------------------------------------------------------------------------

    def list_xpaths(self) -> httpx.Response:
        """POST to /v1/heal/xpaths — re-rank xpaths against current DOM.

        Extracted from V2 source.
        Simplification: IS_WEBSOCKET_AVAILABLE branch (stop/resume video +
        inject_script for Safari) dropped — host runtime only.
        """
        attempt = 1
        max_attempt = 2
        response = None

        while attempt <= max_attempt:
            if self.mobile_tagify:
                self.driver.execute_script(self.mobile_tagify)
                full_page_tagify = "false"
                if self.current_action.get("operation_type", "").lower() == "scroll_until_element":
                    full_page_tagify = "true"
                if "QUERY" in self.current_action.get("operation_type", ""):
                    tagify_response = self.driver.execute_script(
                        f"return tagifyWebpage(false,true,{full_page_tagify});"
                    )
                else:
                    tagify_response = self.driver.execute_script(
                        f"return tagifyWebpage(true,true,{full_page_tagify});"
                    )
                self.xpath_mapping = tagify_response.get("xpaths", {})
                self.tags_description = tagify_response.get("descriptions", {})
                self.untagged_image_base64 = self._take_screenshot()
                self.page_source = tagify_response.get("outerHTML", "")
                tagged = make_tagged_screenshot(
                    screenshot_base64=self.untagged_image_base64,
                    rects=tagify_response.get("rects", {}),
                    driver=self.driver,
                )
                self.tagified_image = tagged[0] if tagged else ""

            else:
                self.untagged_image_base64 = self._take_screenshot()

                op_type = self.current_action.get("operation_type", "")
                if "QUERY" in op_type:
                    self.execute_async_js("tagifyWebpage(false,true)")
                elif op_type.lower() == "scroll_until_element":
                    self.execute_async_js("tagifyWebpage(true,true,true)")
                elif "SCROLL" in op_type:
                    self.execute_async_js("tagifyWebpage(true,false)")
                elif op_type.lower() in ("drag_drop", "click_drag"):
                    self.execute_async_js("tagifyWebpage(true,true,false,0,0,0,true)")
                else:
                    self.execute_async_js("tagifyWebpage()")

                xpath_mapping_raw = self.execute_async_js('fetchJsonData("JSONOutput")')
                self.xpath_mapping = json.loads(xpath_mapping_raw)

                tags_description_raw = self.execute_async_js('fetchJsonData("descOutput")')
                self.tags_description = json.loads(tags_description_raw)

                self.page_source = self.driver.execute_script("return document.body.outerHTML")

                if op_type.lower() == "scroll_until_element":
                    self.tagified_image = capture_full_page_screenshot(self.driver)
                else:
                    self.tagified_image = self._take_screenshot()

                self.execute_async_js("removeLTTags()")
                self.driver.execute_script("annotations = [];JSONOutput = {};nodeData = {};")

            payload = json.dumps({
                "code_export_id": self.code_export_id,
                "current_action": self.current_action,
                "prev_actions": self.prev_actions,
                "xpath_mapping": self.xpath_mapping,
                "tagified_image": self.tagified_image,
                "commit_id": self.commit_id,
                "test_id": self.test_id,
                "username": self.username,
                "accesskey": self.accesskey,
                "tags_description": self.tags_description,
                "org_id": self.org_id,
                "page_source": self.page_source,
                "session_id": self.driver.session_id,
                "use_query_v2": self.use_query_v2,
                "untagged_image_base64": self.untagged_image_base64,
                "version": self.version,
            })

            headers = self._make_auth_headers()
            _log.info("Heal List Xpaths... code_export_id: %s, attempt: %s/%s", self.code_export_id, attempt, max_attempt)
            response = make_http_request_with_retry(
                "POST",
                url=f"{self.automind_url}/v1/heal/xpaths",
                headers=headers,
                data=payload,
            )

            if response.status_code != 200:
                _log.info("Received status code %s, retrying... (attempt %s/%s)", response.status_code, attempt, max_attempt)
                attempt += 1
                continue

            return response

        return response

    def get_outer_html(self) -> str:
        """Build outer-HTML by switching frames per xpath in the xpath_mapping.

        Extracted from V2 source.
        Returns a newline-separated concatenation of each element's outerHTML.
        Precondition: self.xpath_mapping must be populated (e.g., by list_xpaths).
        """
        if self.mobile_tagify:
            self.driver.execute_script(self.mobile_tagify)

        self.execute_async_js("tagifyWebpage(false,true,false)")

        xpath_mapping_raw = self.execute_async_js('fetchJsonData("JSONOutput")')
        xpath_mapping = json.loads(xpath_mapping_raw)

        self.execute_async_js("removeLTTags()")
        self.driver.execute_script("annotations = [];JSONOutput = {};nodeData = {};")

        outer_html_pieces = []
        try:
            for key, value in xpath_mapping.items():
                if not isinstance(value, dict):
                    continue

                xpaths = value.get("xpath", [])
                frame_info = value.get("frameInformation", "")

                # Switch to the appropriate frame/shadow context, if any
                try:
                    if frame_info and frame_info != "":
                        self.driver.switch_to.default_content()
                        _ = switch_to_frame_by_xpath(
                            driver=self.driver,
                            frame_info=json.dumps(frame_info),
                        )
                except Exception:
                    pass

                try:
                    element = self.driver.find_element(By.XPATH, xpaths)
                    outer_html_pieces.append(element.get_attribute("outerHTML"))
                except Exception:
                    continue
        except Exception:
            traceback.print_exc()

        combined_outer_html = "\n\n".join([part for part in outer_html_pieces if part])
        return combined_outer_html

    def textual_query_v2(
        self,
        a11y_snapshot: dict,
        dom_snapshot: dict,
        viewport_node_indices: Optional[list] = None,
    ) -> httpx.Response:
        """POST to /v1/heal/textual_query — textual-similarity query.

        Extracted from V2 source.
        """
        payload_dict: dict = {
            "code_export_id": self.code_export_id,
            "username": self.username,
            "accesskey": self.accesskey,
            "org_id": self.org_id,
            "test_id": self.test_id,
            "commit_id": self.commit_id,
            "current_action": self.current_action,
            "version": self.version,
            "a11y_snapshot": a11y_snapshot,
            "dom_snapshot": dom_snapshot,
            "is_browser": True,
            "is_mobile": self.driver.capabilities.get("platformName", "").lower() in ("android", "ios"),
            "device_os": self.driver.capabilities.get("platformName", "").lower(),
        }
        if viewport_node_indices is not None:
            payload_dict["viewport_node_indices"] = viewport_node_indices

        payload = json.dumps(payload_dict)
        headers = self._make_auth_headers()

        _log.info("Heal Textual Query V2... code_export_id: %s", self.code_export_id)
        response = make_http_request_with_retry(
            "POST",
            f"{self.automind_url}/v1/heal/textual_query",
            headers=headers,
            data=payload,
        )
        return response

    def vision_query_v2(self) -> Optional[httpx.Response]:
        """POST to /v1/heal/vision — vision-based selector inference (V2 path).

        Extracted from V2 source.
        Simplification: duplicate "version" key in V2 payload collapsed to single
        entry — second value wins in Python; ported as single entry.
        """
        attempt = 1
        max_attempt = 2

        while attempt <= max_attempt:
            attempt += 1
            screenshot = self._take_screenshot()

            payload = json.dumps({
                "code_export_id": self.code_export_id,
                "current_action": self.current_action,
                "commit_id": self.commit_id,
                "test_id": self.test_id,
                "username": self.username,
                "accesskey": self.accesskey,
                "version": self.version,
                "org_id": self.org_id,
                "session_id": self.driver.session_id,
                "untagged_image_base64": screenshot,
            })

            headers = self._make_auth_headers()

            _log.info("Heal Vision Query V2... code_export_id: %s", self.code_export_id)
            _log.info("Kane Version: %s", self.version)
            response = make_http_request_with_retry(
                "POST",
                url=f"{self.automind_url}/v1/heal/vision",
                headers=headers,
                data=payload,
            )
            return response

        return None

    def vision_query(self) -> Optional[httpx.Response]:
        """POST to /v1/heal/vision to ANSWER a vision query (presence / visibility
        / visual read) — distinct from vision_query_v2(), which infers a selector.

        Untagged-only: mirrors the vision-query answer path, which answers a
        VISION_QUERY from the untagged viewport screenshot alone (no tagify). The
        answer is returned in the response's ``vision_query`` field. The natural-
        language query travels in current_action.operation_intent with
        operation_type == "VISION_QUERY".
        """
        screenshot = self._take_screenshot()
        payload = json.dumps({
            "code_export_id": self.code_export_id,
            "current_action": self.current_action,
            "commit_id": self.commit_id,
            "test_id": self.test_id,
            "username": self.username,
            "accesskey": self.accesskey,
            "org_id": self.org_id,
            "session_id": self.driver.session_id,
            "untagged_image_base64": screenshot,
            "use_query_v2": True,
            "version": self.version,
        })
        headers = self._make_auth_headers()
        _log.info("Heal Vision Query (answer)... code_export_id: %s", self.code_export_id)
        return make_http_request_with_retry(
            "POST",
            url=f"{self.automind_url}/v1/heal/vision",
            headers=headers,
            data=payload,
        )

    def desktop_locate(self, drop_aware: bool = False) -> tuple[int, int]:
        """POST to /v2/locate/desktop (viewport screenshot) → (css_x, css_y).

        drop_aware: True when locating a drag TARGET (drop zone) — threads into
        the payload's drop_aware field (spec §10.1). Default False matches the
        single-element locate contract.

        Captures a VIEWPORT screenshot (NOT full-page), POSTs a lean body to
        {AUTOMIND_URL}/v2/locate/desktop, then scales the returned image-pixel
        coordinate to viewport-CSS-px:
            css_x = raw_x * viewport_width  / image_width
            css_y = raw_y * viewport_height / image_height
        where image_width/height are read from the PNG IHDR header (= dividing
        by devicePixelRatio). Returns (css_x, css_y) as ints, clamped to
        [0, viewport_dim−1].

        Retry policy (mirrors deleted browser_coordinate tier): up to 3 attempts,
        each taking a FRESH screenshot. On non-200 we continue to the next attempt;
        after exhausting all attempts we raise HealTierMiss with the last status.
        make_http_request_with_retry only retries {408,429,499,502,503,504} and
        transport errors — a plain 500 returns immediately, so we layer our own
        application-level retry around it here.

        PNG validation: the screenshot is decoded and IHDR-checked BEFORE
        the POST so a corrupt screenshot never burns an API call. On invalid PNG
        we raise HealTierMiss immediately (no retry).

        Miss detection: HTTP 200 with coordinate==[0,0] (NOT 404) is a not-found.
        Treats coordinate missing/null/[0,0]/len<2 as miss → raises HealTierMiss.

        Mobile note: this tier hardcodes os:"desktop" and omits the V2
        device-chrome crop. If the session is Android/iOS, coordinates may be off
        — a WARNING is logged but the tier is not blocked.
        """
        # Short-circuit on empty intent before ANY screenshot or HTTP work.
        intent = self.current_action.get("operation_intent", "")
        if not intent:
            raise HealTierMiss("DESKTOP_LOCATE", "empty operation_intent")

        # Read viewport dims once — they don't change between retry attempts.
        viewport = self.driver.execute_script(
            "return [window.innerWidth, window.innerHeight]"
        )
        viewport_width, viewport_height = int(viewport[0]), int(viewport[1])

        # Warn when serving a mobile session — os:"desktop" crops nothing
        # so the returned coordinate may land in the browser chrome area.
        platform_name = self.driver.capabilities.get("platformName", "").lower()
        if platform_name in ("android", "ios"):
            _log.warning(
                "desktop_locate: DESKTOP_LOCATE assumes desktop web; coordinates "
                "may be wrong if the screenshot contains device chrome "
                "(platformName=%r). Proceeding.",
                platform_name,
            )

        # Application-level retry loop — fresh screenshot on every attempt.
        _MAX_ATTEMPTS = 3
        last_status: int | None = None
        response = None
        img_b64: str = ""
        image_width: int = 1
        image_height: int = 1

        for attempt in range(1, _MAX_ATTEMPTS + 1):
            # Take screenshot and validate PNG BEFORE the POST so a corrupt
            # screenshot never burns an API round-trip (2026-06 code review).
            image_base64 = self._take_screenshot()
            # Strip data-URL prefix if present (shouldn't be, but defensive).
            img_b64 = image_base64.split(",", 1)[1] if "," in image_base64 else image_base64
            image_bytes = base64.b64decode(img_b64)
            try:
                image_width, image_height = _png_dimensions(image_bytes)
            except ValueError:
                raise HealTierMiss("DESKTOP_LOCATE", "screenshot is not a valid PNG")

            # Aspect-ratio sanity check — log a warning if image and viewport
            # aspect ratios diverge by more than 2%. The scaling assumes the screenshot
            # maps onto the full viewport; a significant mismatch (e.g. partial
            # screenshot, device-chrome inclusion) means the returned coordinate will
            # be incorrectly scaled. Don't block — surface for post-mortem.
            if viewport_height > 0 and image_height > 0:
                img_ar = image_width / image_height
                vp_ar = viewport_width / viewport_height
                if abs(img_ar - vp_ar) / max(vp_ar, 1e-9) > 0.02:
                    _log.warning(
                        "desktop_locate: aspect ratio mismatch — "
                        "image %.4f (%sx%s) vs viewport %.4f (%sx%s); "
                        "coordinate scaling may be inaccurate",
                        img_ar, image_width, image_height,
                        vp_ar, viewport_width, viewport_height,
                    )

            request_id = uuid.uuid4().hex[:16]
            payload = {
                "intent": intent,
                "image": img_b64,
                "os": "desktop",
                "platform": "web",
                "screen_width": viewport_width,
                "screen_height": viewport_height,
                "drop_aware": drop_aware,
                "request_id": request_id,
                "a11y_flatten": [],
            }
            headers = self._make_auth_headers()
            _log.info(
                "Heal desktop_locate: request_id=%s intent=%r viewport=%sx%s attempt=%s/%s",
                request_id, intent, viewport_width, viewport_height, attempt, _MAX_ATTEMPTS,
            )
            response = make_http_request_with_retry(
                "POST",
                url=f"{self.automind_url}/v2/locate/desktop",
                headers=headers,
                json_data=payload,
            )

            if response.status_code == 200:
                break

            # Non-200: record status, log, and retry with a fresh screenshot.
            last_status = response.status_code
            _log.warning(
                "desktop_locate: attempt %s/%s got status %s; "
                "retrying with fresh screenshot",
                attempt, _MAX_ATTEMPTS, last_status,
            )
        else:
            # Loop completed without a 200 — all attempts exhausted.
            raise HealTierMiss(
                "DESKTOP_LOCATE",
                f"/v2/locate/desktop returned status {last_status} "
                f"after {_MAX_ATTEMPTS} attempts",
            )

        # 200 response — parse and validate coordinate.
        api_resp = response.json()
        coordinate = api_resp.get("coordinate", [0, 0]) or [0, 0]
        if (
            not isinstance(coordinate, (list, tuple))
            or len(coordinate) < 2
            or list(coordinate[:2]) == [0, 0]
        ):
            raise HealTierMiss(
                "DESKTOP_LOCATE",
                f"element not found for intent {intent!r} "
                f"(coordinate={coordinate!r}, reason={api_resp.get('reason', '')!r})",
            )

        raw_x, raw_y = coordinate[0], coordinate[1]

        # Scale image-space coord → viewport-CSS-px using PNG IHDR dims from the
        # successful attempt (already decoded above in the loop).
        css_x = int(raw_x * viewport_width / max(image_width, 1))
        css_y = int(raw_y * viewport_height / max(image_height, 1))

        # Clamp to valid viewport range — out-of-bounds coords crash
        # ActionChains.move_to_element_with_offset in some Selenium versions.
        css_x = max(0, min(css_x, viewport_width - 1))
        css_y = max(0, min(css_y, viewport_height - 1))

        # Log confidence alongside the coordinate so post-mortem traces
        # can assess model certainty without decoding the full response body.
        _log.info(
            "Heal desktop_locate: image=(%s,%s) viewport=(%s,%s) "
            "raw=(%s,%s) css=(%s,%s) confidence=%s",
            image_width, image_height, viewport_width, viewport_height,
            raw_x, raw_y, css_x, css_y, api_resp.get("confidence"),
        )
        return (css_x, css_y)

    def desktop_locate_full_page(self) -> tuple[int, int]:
        """POST to /v2/locate/desktop (full-page screenshot) → (page_css_x, page_css_y).

        Captures a FULL-PAGE screenshot (NOT viewport), POSTs a lean body with
        screen_width=0, screen_height=0 (full-page image contract). Scales the
        returned image-pixel coordinate to page-CSS-px using PNG IHDR dims:
            page_x = raw_x * page_width  / image_width
            page_y = raw_y * page_height / image_height
        where page_width/height are document.documentElement scrollWidth/scrollHeight.

        Returns (page_x, page_y) as ints, clamped to [0, page_dim-1].

        Used by the DESKTOP_LOCATE_FULL_PAGE heal tier for scroll-into-view healing
        (spec §9). The returned page-CSS coordinates are scrolled into viewport
        and then resolved to xpath by the cascade.

        PNG validation: screenshot is decoded and IHDR-checked BEFORE the POST.
        On invalid PNG raises HealTierMiss immediately (no retry, no API call).

        Miss detection: HTTP 200 with coordinate==[0,0] → HealTierMiss. Treats
        coordinate missing/null/[0,0]/len<2 as miss. Also raises HealTierMiss on
        non-200 after 3 attempts. Full-page screenshot captured once and reused
        across retries (expensive capture; page content stable within a single
        heal round).
        """
        intent = self.current_action.get("operation_intent", "")
        if not intent:
            raise HealTierMiss("DESKTOP_LOCATE_FULL_PAGE", "empty operation_intent")

        # Full-page screenshot captured once — reused across all retry attempts.
        image_base64 = capture_full_page_screenshot(self.driver)
        img_b64 = image_base64.split(",", 1)[1] if "," in image_base64 else image_base64
        image_bytes = base64.b64decode(img_b64)

        # Validate PNG BEFORE the POST so a corrupt screenshot never burns an API call.
        try:
            image_width, image_height = _png_dimensions(image_bytes)
        except ValueError:
            raise HealTierMiss("DESKTOP_LOCATE_FULL_PAGE", "screenshot is not a valid PNG")

        # Page dimensions in CSS pixels (scrollWidth × scrollHeight).
        dims = self.driver.execute_script(
            "return [document.documentElement.scrollWidth, document.documentElement.scrollHeight]"
        )
        page_width, page_height = int(dims[0]), int(dims[1])

        _MAX_ATTEMPTS = 3
        last_status: int | None = None
        response = None

        for attempt in range(1, _MAX_ATTEMPTS + 1):
            request_id = uuid.uuid4().hex[:16]
            payload = {
                "intent": intent,
                "image": img_b64,
                "os": "desktop",
                "platform": "web",
                "screen_width": 0,
                "screen_height": 0,
                "drop_aware": False,
                "request_id": request_id,
                "a11y_flatten": [],
            }
            headers = self._make_auth_headers()
            _log.info(
                "Heal desktop_locate_full_page: request_id=%s intent=%r page=%sx%s attempt=%s/%s",
                request_id, intent, page_width, page_height, attempt, _MAX_ATTEMPTS,
            )
            response = make_http_request_with_retry(
                "POST",
                url=f"{self.automind_url}/v2/locate/desktop",
                headers=headers,
                json_data=payload,
            )

            if response.status_code == 200:
                break

            last_status = response.status_code
            _log.warning(
                "desktop_locate_full_page: attempt %s/%s got status %s",
                attempt, _MAX_ATTEMPTS, last_status,
            )
        else:
            raise HealTierMiss(
                "DESKTOP_LOCATE_FULL_PAGE",
                f"/v2/locate/desktop returned status {last_status} "
                f"after {_MAX_ATTEMPTS} attempts",
            )

        # Parse and validate coordinate.
        api_resp = response.json()
        coordinate = api_resp.get("coordinate", [0, 0]) or [0, 0]
        if (
            not isinstance(coordinate, (list, tuple))
            or len(coordinate) < 2
            or list(coordinate[:2]) == [0, 0]
        ):
            raise HealTierMiss(
                "DESKTOP_LOCATE_FULL_PAGE",
                f"element not found for intent {intent!r} "
                f"(coordinate={coordinate!r}, reason={api_resp.get('reason', '')!r})",
            )

        raw_x, raw_y = coordinate[0], coordinate[1]

        # Scale image-space coord → page-CSS-px using IHDR dims from the captured image.
        page_x = int(raw_x * page_width / max(image_width, 1))
        page_y = int(raw_y * page_height / max(image_height, 1))

        # Clamp to valid page range.
        page_x = max(0, min(page_x, page_width - 1))
        page_y = max(0, min(page_y, page_height - 1))

        _log.info(
            "Heal desktop_locate_full_page: image=(%s,%s) page=(%s,%s) "
            "raw=(%s,%s) page_css=(%s,%s)",
            image_width, image_height, page_width, page_height,
            raw_x, raw_y, page_x, page_y,
        )
        return (page_x, page_y)
