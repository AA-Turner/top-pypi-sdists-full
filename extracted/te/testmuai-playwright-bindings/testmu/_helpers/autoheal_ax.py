"""AH2 standalone-binding heal client: capture the live AX tree -> POST
``/api/v1/AH2/autoheal`` -> resolve the returned ``ref`` -> a fresh,
frame-scoped locator.

This runs inside customer CI, where the equivalent live-agent grounding
pipeline is not available, so the whole capture -> heal -> resolve
pipeline has to run in-process here using the shared AX pipeline
(``testmu._helpers.ax_tree``) and the binding's own selector synthesis
(``_locator_enrichment.enrich_element_locator``). Mirrors
``_helpers/autoheal.py`` (request builder/session pattern) and
``_helpers/textual_analyzer/heal.py`` (ref/backend-id -> enrich pattern).

Returns ``{"locator", "locator_type", "confidence", "reasoning"}`` on a hit,
or ``None`` on ANY miss (capture failed, non-200, no ref, confidence below
floor, ref not in the table, enrichment failed, transport/other error).
NEVER raises.
"""
from __future__ import annotations

import contextlib
import logging
import os
from typing import Any

import aiohttp

from testmu import _config
from testmu._helpers._http import create_session
from testmu._helpers._locator_enrichment import enrich_element_locator
from testmu._helpers.ax_tree import (
    capture_frame_forest,
    resolve_session_for_frame,
    serialize_ax_tree,
)

_log = logging.getLogger("testmu")

_HOST = os.getenv("TESTMU_AI_API_HOST", "https://kaneai-api.lambdatest.com/v16-server")
_URL = _HOST.rstrip("/") + "/api/v1/AH2/autoheal"
_TIMEOUT = aiohttp.ClientTimeout(total=60)
_VALID = frozenset({"click", "select", "type", "scroll"})


async def _post_ax_heal(url: str, body: dict[str, Any], timeout: aiohttp.ClientTimeout) -> dict[str, Any] | None:
    async with create_session() as s:
        async with s.post(url, json=body, timeout=timeout) as resp:
            if resp.status != 200:
                _log.info("[autoheal_ax] %s -> %s", url, resp.status)
                return None
            return await resp.json(content_type=None)


def _find_frame_path(frame_captures, target_frame_id: str):
    """DFS the frame forest for the chain of captures from a top-level iframe
    down to the one owning ``target_frame_id``. Returns the ordered list
    (root→leaf) or None when the frame isn't in the forest."""
    for fc in frame_captures or []:
        if getattr(fc, "frame_id", None) == target_frame_id:
            return [fc]
        sub = _find_frame_path(getattr(fc, "children", None), target_frame_id)
        if sub is not None:
            return [fc, *sub]
    return None


async def _build_frame_chain(page, frame_captures, target_frame_id: str):
    """Resolve the ordered iframe locator chain (root→leaf) that scopes
    ``target_frame_id``. Each iframe's owner element is enriched on its PARENT
    frame's session (the first on the main frame). Returns a list of
    ``{"locator", "locator_type"}`` or None on any failure (frame not found,
    missing owner id, or an enrichment miss) so the caller can fail safe."""
    path = _find_frame_path(frame_captures, target_frame_id)
    if not path:
        return None
    chain: list[dict[str, Any]] = []
    parent_frame_id = ""  # the first iframe's owner lives in the main frame
    for fc in path:
        owner = getattr(fc, "owner_backend_node_id", None)
        if owner is None:
            return None
        cdp = await resolve_session_for_frame(page, parent_frame_id)
        try:
            enriched = await enrich_element_locator(cdp, {"backend_dom_node_id": owner})
        finally:
            # A detach failure (e.g. the session's frame went away after a
            # navigation) must not mask a good enrich result — swallow it,
            # matching the JS binding.
            with contextlib.suppress(Exception):
                await cdp.detach()
        if not enriched or not enriched.get("locator"):
            return None
        chain.append({
            "locator": enriched["locator"],
            "locator_type": enriched.get("locator_type", "css"),
        })
        parent_frame_id = fc.frame_id
    return chain


async def run_locator_heal(
    page,
    action_instruction: str,
    action_type: str,
    previous_selectors: str = "",
    *,
    confidence_floor: float = 0.7,
    reprobe: bool = False,
) -> dict[str, Any] | None:
    if not _config.smart or action_type not in _VALID:
        return None
    try:
        forest = await capture_frame_forest(page)
        if forest is None or forest.main_tree is None:
            return None
        doc, ref_table = serialize_ax_tree(forest.main_tree, forest.frame_captures)
        body = {
            "action_instruction": action_instruction,
            "action_type": action_type,
            "dom_snapshot": doc,
            "previous_selectors": previous_selectors or "",
            # Variable-target re-probe: the recorded locator holds a PRIOR run's
            # value, so the server heals on the current target value and treats
            # the locator as role/structure only. Only sent when True.
            "reprobe": reprobe,
        }
        resp = await _post_ax_heal(_URL, body, _TIMEOUT)
        if not resp or not resp.get("ref"):
            return None
        confidence = float(resp.get("confidence", 0.0))
        if confidence < confidence_floor:
            _log.info("[autoheal_ax] confidence %.2f < floor %.2f", confidence, confidence_floor)
            return None
        entry = ref_table.get(resp["ref"])
        if not entry or entry.get("backend_dom_node_id") is None:
            return None
        # Frame-scope: an iframe-resident ref resolves on its OWN frame's CDP
        # session, never the main-frame session (a bare backendNodeId can
        # collide across frames).
        cdp = await resolve_session_for_frame(page, entry.get("frame_id", ""))
        try:
            enriched = await enrich_element_locator(cdp, {"backend_dom_node_id": entry["backend_dom_node_id"]})
        finally:
            # A detach failure (e.g. the session's frame went away after a
            # navigation) must not mask a good enrich result — swallow it,
            # matching the JS binding.
            with contextlib.suppress(Exception):
                await cdp.detach()
        if not enriched or not enriched.get("locator"):
            return None
        # An iframe-resident element's selector is frame-relative and cannot
        # resolve at the top level — rebuild the frame chain so the retry can
        # scope into it. Fail safe (return None) if it can't be reconstructed.
        frame_chain: list[dict[str, Any]] = []
        frame_id = entry.get("frame_id", "")
        if frame_id:
            frame_chain = await _build_frame_chain(page, forest.frame_captures, frame_id)
            if frame_chain is None:
                return None
        return {
            "locator": enriched["locator"],
            "locator_type": enriched.get("locator_type", "css"),
            "frame_chain": frame_chain,
            "confidence": confidence,
            "reasoning": resp.get("reasoning", ""),
        }
    except aiohttp.ClientError as e:
        _log.warning("[autoheal_ax] transport error: %s", e)
        return None
    except Exception as e:  # noqa: BLE001
        _log.warning("[autoheal_ax] unexpected: %s", e)
        return None
