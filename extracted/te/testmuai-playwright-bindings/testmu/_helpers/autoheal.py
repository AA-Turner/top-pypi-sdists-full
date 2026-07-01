from __future__ import annotations

"""POST /api/v1/autoheal — given an action description and the current
flat DOM, the v16 controller returns the dom_index of the element that
corresponds to the originally-targeted one. We then synthesize a fresh
selector for that element via CDP and return it to the caller.

Same host as vision (TESTMU_AI_API_HOST). Auth + headers come from the
shared create_session() — Basic LT creds + x-session-id + x-source.

Returns dict on hit, None on any miss/error. NEVER raises — _default_heal
relies on None to write the negative-cache sentinel and let the wrapper
re-raise the original Playwright TimeoutError.
"""
import base64
import logging
import os
from typing import Any

import aiohttp

from testmu import _config
from testmu._helpers._http import create_session
from testmu._helpers._screenshot import take_screenshot
from testmu._helpers._dom_capture import capture_flat_dom
from testmu._helpers._locator_enrichment import enrich_element_locator

_log = logging.getLogger("testmu")

_AUTOHEAL_API_HOST = os.getenv(
    "TESTMU_AI_API_HOST", "https://kaneai-api.lambdatest.com/v16-server"
)
_AUTOHEAL_URL = f"{_AUTOHEAL_API_HOST}/api/v1/autoheal"
_AUTOHEAL_TIMEOUT = aiohttp.ClientTimeout(total=60)

_VALID_ACTION_TYPES = frozenset({"click", "select", "type", "scroll"})


async def autoheal_locator(
    page,
    action_instruction: str,
    action_type: str,
    *,
    include_screenshot: bool = True,
) -> dict[str, Any] | None:
    if not _config.smart:
        return None
    if action_type not in _VALID_ACTION_TYPES:
        _log.debug("[autoheal] unsupported action_type=%s — skipping", action_type)
        return None

    cdp = None
    try:
        cdp, flat_dom = await capture_flat_dom(page)
        if not flat_dom:
            _log.info("[autoheal] empty flat_dom — skipping")
            return None

        body: dict[str, Any] = {
            "action_instruction": action_instruction,
            "action_type": action_type,
            "full_dom_list": flat_dom,
        }
        if include_screenshot:
            try:
                shot = await take_screenshot(page)
                body["screenshot_b64"] = base64.b64encode(shot).decode()
            except Exception as e:
                _log.warning("[autoheal] screenshot failed (continuing without): %s", e)

        async with create_session() as session:
            async with session.post(
                _AUTOHEAL_URL, json=body, timeout=_AUTOHEAL_TIMEOUT
            ) as resp:
                payload = await resp.json(content_type=None)
                status = resp.status

        if status == 404:
            _log.info("[autoheal] no_match: %s", (payload or {}).get("detail", ""))
            return None
        if status != 200:
            _log.warning("[autoheal] status=%s body=%s", status, payload)
            return None

        dom_index = (payload or {}).get("dom_index")
        reasoning = (payload or {}).get("reasoning", "")
        if dom_index is None:
            _log.warning("[autoheal] 200 with no dom_index: %s", payload)
            return None

        target = next((el for el in flat_dom if el.get("index") == dom_index), None)
        if target is None:
            _log.warning(
                "[autoheal] dom_index=%s not in flat_dom (len=%d)", dom_index, len(flat_dom)
            )
            return None

        enriched = await enrich_element_locator(cdp, target)
        if not enriched:
            _log.info("[autoheal] enrichment produced no locator for index=%s", dom_index)
            return None
        enriched["reasoning"] = reasoning
        _log.info(
            "[autoheal] %s → %s (%s)",
            action_instruction[:60],
            enriched["locator"][:80],
            enriched["locator_type"],
        )
        return enriched

    except aiohttp.ClientError as e:
        _log.warning("[autoheal] transport error: %s", e)
        return None
    except Exception as e:
        _log.warning("[autoheal] unexpected error: %s", e)
        return None
    finally:
        if cdp is not None:
            try:
                await cdp.detach()
            except Exception:
                pass
