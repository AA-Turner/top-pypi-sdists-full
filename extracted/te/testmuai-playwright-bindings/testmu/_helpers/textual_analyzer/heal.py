"""TextualAnalyzer heal: regenerate the WHOLE extraction against a fresh page.

Flow: capture a fresh structured DOM snapshot -> POST the heal endpoint
(/api/v1/textual_analyzer/heal) to regenerate the el(i) code -> resolve each el(i) to a
stable locator -> page.evaluate(wrap(code), handles).

Returns a HealOutcome on success, or None on any miss (no usable code, a locator
that won't resolve, or a null/empty result) — the caller then FAILS the step
(there is no vision fallback for a textual heal).
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

import aiohttp

from testmu._helpers._dom_structured import capture_structured_dom
from testmu._helpers._http import create_session
from testmu._helpers._locator_enrichment import enrich_element_locator
from testmu._helpers.textual_analyzer.extractor import parse_el_references, wrap_extractor_code

_log = logging.getLogger("testmu")

_HEAL_HOST = os.environ.get(
    "TESTMU_AI_API_HOST", "https://kaneai-api.lambdatest.com/v16-server"
)
_HEAL_URL = _HEAL_HOST.rstrip("/") + "/api/v1/textual_analyzer/heal"
_HEAL_TIMEOUT = aiohttp.ClientTimeout(total=60)


@dataclass
class HealOutcome:
    # The recovered value. operator/transforms stay as RECORDED (applied
    # downstream) — a locator drift must not change the comparison semantics — so
    # the regenerated operator/transforms from the heal response are intentionally
    # not surfaced here.
    value: str


async def _post_heal(
    query: str, dom_snapshot: str, expected_value: str | None, needs_unit: bool,
    condition: str | None = None,
) -> dict | None:
    body = {
        "query": query,
        "dom_snapshot": dom_snapshot,
        "expected_value": expected_value,
        "needs_unit_conversion": needs_unit,
        # Checkpoint condition drives in-code derivation on regen; without it the
        # heal would return a raw read for a derived (arithmetic/boolean) step.
        "condition": condition or "",
    }
    try:
        async with create_session() as session:
            async with session.post(_HEAL_URL, json=body, timeout=_HEAL_TIMEOUT) as resp:
                if resp.status != 200:
                    # 404 = no usable code / low confidence -> miss (fail the step).
                    _log.info("[textual_analyzer] heal endpoint %s -> %s", _HEAL_URL, resp.status)
                    return None
                return await resp.json(content_type=None)
    except aiohttp.ClientError as e:
        _log.warning("[textual_analyzer] heal POST failed: %s", e)
        return None


async def run_heal(
    page, query: str, expected_value: str | None, needs_unit_conversion: bool,
    condition: str | None = None,
) -> HealOutcome | None:
    structured = await capture_structured_dom(page)
    if structured is None or not structured.text:
        return None

    resp = await _post_heal(query, structured.text, expected_value, needs_unit_conversion, condition)
    if not resp or not resp.get("code"):
        return None

    code = resp["code"]
    indices = parse_el_references(code)

    handles = []
    cdp = await page.context.new_cdp_session(page)
    try:
        for i in indices:
            bid = structured.index_to_backend_id.get(i)
            if bid is None:
                return None
            enriched = await enrich_element_locator(cdp, {"backend_dom_node_id": bid})
            loc = (enriched or {}).get("locator")
            if not loc:
                return None
            handle = await page.locator(loc).first.element_handle()
            if handle is None:
                return None
            handles.append(handle)
    finally:
        await cdp.detach()

    wrapped = wrap_extractor_code(code, indices)
    try:
        value = await page.evaluate(wrapped, handles)
    except Exception as e:  # noqa: BLE001
        _log.warning("[textual_analyzer] heal evaluate failed: %s", e)
        return None
    if value is None or value == "":
        return None  # regenerated code still couldn't find the value -> miss

    return HealOutcome(value=str(value))
