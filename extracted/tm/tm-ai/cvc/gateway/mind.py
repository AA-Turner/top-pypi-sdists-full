"""
cvc.gateway.mind — REST surface for the World Model + Counterfactual
self-test loop (Fable5 Phase 5→dashboard wiring).

Same conventions as cvc.gateway.soul: soul-scoped (global, not
workspace-scoped — the world model IS part of the soul), idempotent
GETs, ok/error POST envelopes, non-fatal exception handling with a
structured error response instead of a 500.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Query

logger = logging.getLogger("cvc.gateway.mind")

router = APIRouter()


def _soul_root() -> Path:
    from cvc.operations.soul_singularity import _soul_root as _sr
    return _sr()


def _ensure_soul_migrated() -> None:
    try:
        from cvc.operations.soul_singularity import ensure_migrated
        ensure_migrated()
    except Exception as exc:  # noqa: BLE001
        logger.debug("soul migration failed (non-fatal): %s", exc)


# ---------------------------------------------------------------------------
# World Model
# ---------------------------------------------------------------------------


@router.get("/mind/world-model")
async def get_world_model() -> dict[str, Any]:
    """Full world-model state for the dashboard: values hierarchy,
    reasoning style, uncertainty flags, revision history."""
    try:
        _ensure_soul_migrated()
        from cvc.core.world_model import WorldModelManager

        wm = WorldModelManager(_soul_root())
        state = wm.load_state()
        return {
            "ok": True,
            "values_hierarchy": state.values_hierarchy.model_dump() if state.values_hierarchy else None,
            "reasoning_style": state.reasoning_style.model_dump() if state.reasoning_style else None,
            "uncertainty_flags": [f.model_dump() for f in state.uncertainty_flags if not f.resolved],
            "resolved_flags_count": len([f for f in state.uncertainty_flags if f.resolved]),
            "hierarchy_history": state.hierarchy_history,
            "style_history": state.style_history,
            "injection_preview": wm.get_world_model_injection(),
        }
    except Exception as exc:  # noqa: BLE001
        logger.exception("world-model fetch failed")
        return {"ok": False, "error": str(exc)}


@router.post("/mind/world-model/resolve-flag")
async def resolve_uncertainty_flag(payload: dict[str, Any]) -> dict[str, Any]:
    """Manually resolve an uncertainty flag from the dashboard (owner
    directly tells the soul the answer instead of waiting for a probe)."""
    try:
        _ensure_soul_migrated()
        from cvc.core.world_model import WorldModelManager

        flag_id = str(payload.get("flag_id") or "")
        if not flag_id:
            return {"ok": False, "error": "flag_id required"}

        wm = WorldModelManager(_soul_root())
        resolved = wm.resolve_flag(flag_id, resolved_by="dashboard_manual")
        return {"ok": resolved}
    except Exception as exc:  # noqa: BLE001
        logger.exception("resolve-flag failed")
        return {"ok": False, "error": str(exc)}


# ---------------------------------------------------------------------------
# Counterfactual Probes (self-test loop)
# ---------------------------------------------------------------------------


@router.get("/mind/probes")
async def list_probes(
    status: Optional[str] = Query(default="pending"),
    limit: int = Query(default=20),
) -> dict[str, Any]:
    """List probes. status='pending' (default) or 'graded'."""
    try:
        _ensure_soul_migrated()
        from cvc.operations.counterfactual import CounterfactualEngine

        eng = CounterfactualEngine(_soul_root())
        if status == "graded":
            items = []
            for p in sorted(eng.graded_dir.glob("*.json"), reverse=True)[:limit]:
                try:
                    from cvc.operations.counterfactual import CounterfactualProbe

                    items.append(
                        CounterfactualProbe.model_validate_json(
                            p.read_text(encoding="utf-8")
                        ).model_dump()
                    )
                except Exception:  # noqa: BLE001
                    continue
        else:
            items = [p.model_dump() for p in eng.list_pending(limit=limit)]

        return {"ok": True, "probes": items, "calibration": eng.load_calibration().model_dump(), "summary": eng.calibration_summary()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("list probes failed")
        return {"ok": False, "error": str(exc), "probes": []}


@router.post("/mind/probes/grade")
async def grade_probe(payload: dict[str, Any]) -> dict[str, Any]:
    """Owner grades a pending probe: confirmed | corrected | skipped."""
    try:
        _ensure_soul_migrated()
        from cvc.operations.counterfactual import CounterfactualEngine

        probe_id = str(payload.get("probe_id") or "")
        status = str(payload.get("status") or "")
        owner_response = str(payload.get("owner_response") or "")
        if not probe_id or status not in {"confirmed", "corrected", "skipped"}:
            return {"ok": False, "error": "probe_id and valid status required"}

        eng = CounterfactualEngine(_soul_root())
        probe = eng.grade_probe(probe_id, status, owner_response)
        if probe is None:
            return {"ok": False, "error": "probe not found"}
        return {"ok": True, "probe": probe.model_dump(), "calibration": eng.load_calibration().model_dump()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("grade probe failed")
        return {"ok": False, "error": str(exc)}


@router.post("/mind/probes/generate")
async def generate_probe_now() -> dict[str, Any]:
    """Force-generate one probe on demand (dashboard 'Test me now' button),
    instead of waiting for the next dream cycle."""
    try:
        _ensure_soul_migrated()
        from cvc.operations.counterfactual import run_counterfactual_cycle
        from cvc.core.user_model import UserModelManager

        cvc_root = _soul_root()
        umm = UserModelManager(cvc_root)
        narrative = umm.load_current_model().soul_narrative

        adapter = None
        model = "gpt-4o-mini"
        try:
            from cvc.gateway.soul import _build_chat_default_adapter

            built = _build_chat_default_adapter()
            if built:
                adapter, model, _provider = built
        except Exception as exc:  # noqa: BLE001
            logger.debug("mind: could not build default adapter: %s", exc)

        if adapter is None:
            return {"ok": False, "error": "No LLM adapter configured — set up a provider first."}

        probe = await run_counterfactual_cycle(
            cvc_root=cvc_root, adapter=adapter, model=model, soul_narrative=narrative,
        )
        if probe is None:
            return {"ok": False, "error": "Probe generation skipped (queue full or LLM call failed) — check logs."}
        return {"ok": True, "probe": probe.model_dump()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("generate probe failed")
        return {"ok": False, "error": str(exc)}
