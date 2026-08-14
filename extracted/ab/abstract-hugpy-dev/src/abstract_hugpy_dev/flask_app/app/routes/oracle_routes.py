"""Oracle routes: GET /oracle/capabilities (k90) + POST /oracle/route (k91).

THIN adapters in the comms_routes style: parse HTTP, call the oracle package,
jsonify. All behavior lives in ``abstract_hugpy_dev.oracle`` (catalog, router,
runtime, scorecard); if a route here grows logic, it's in the wrong file. The
oracle imports are lazy inside the handlers so app boot never pays for (or
breaks on) a registry read.

POST /oracle/route is the route-to-best-result core. JSON body::

    {"prompt": str,                       # required unless capability is set
     "inputs": [{"kind": "text|image|video|audio|url",
                 "uri": str | "b64": str | "text": str, "label"?: str}],
     "capability"?: "audio.transcribe",   # explicit wins over inference
     "quality"?: "preview|balanced|best",
     "model_id"?: str,
     "evaluate"?: bool,   # k92 judge; default true for image.generate/
                          # image.transform/text.summarize, false otherwise
     "repair"?: bool}     # k92 one bounded repair; default true when evaluate
                          # ran or a technical check failed

A repaired run answers with the SECOND attempt's artifacts/receipt/scorecard
plus additive keys: ``repair`` (the RepairDecision) and ``receipts`` (both
attempts, in order).

Responses (scorecard MANDATORY on all of them, operator ruling 2026-08-05):
  200 executed  -> {ok, goal, route, artifacts, receipt, scorecard}
  202 deferred  -> video.*: {ok, routed, execution:"deferred", reason,
                   binding/alternatives, scorecard}
  422 gap       -> typed CAPABILITY_GAP: {ok:false, goal, route, scorecard}
  400 malformed -> {ok:false, error} (typed message, never a traceback)
"""
from __future__ import annotations

import logging
import os

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

oracle_bp = Blueprint("oracle_bp", __name__)


@oracle_bp.route("/oracle/capabilities", methods=["GET"])
def oracle_capabilities():
    """The unified capability catalog. Optional ``?capability=<name>`` filter
    returns just that view (404 with the known names when it doesn't exist)."""
    from abstract_hugpy_dev.oracle import catalog

    name = (request.args.get("capability") or "").strip()
    try:
        if name:
            view = catalog.get_capability(name)
            if view is None:
                return jsonify({
                    "ok": False,
                    "error": f"unknown capability {name!r}",
                    "known": sorted(v.name for v in catalog.list_capabilities()),
                }), 404
            return jsonify({"ok": True, "count": 1,
                            "capabilities": [view.to_dict()]})
        views = catalog.list_capabilities()
        return jsonify({"ok": True, "count": len(views),
                        "capabilities": [v.to_dict() for v in views]})
    except Exception as exc:  # noqa: BLE001 — a catalog fault answers honestly, not 500-blank
        logger.exception("GET /oracle/capabilities failed")
        return jsonify({"ok": False, "error": str(exc)}), 500


# ---------------------------------------------------------------------------
# POST /oracle/route (k91)
# ---------------------------------------------------------------------------

# b64 inputs are materialized to files so downstream (dispatch builders,
# hashing, decode checks) sees one shape: a server path.
_B64_EXT = {"image": ".png", "audio": ".wav", "video": ".mp4", "text": ".txt"}


def _uploads_home() -> str:
    try:
        from ..functions import UPLOADS_HOME  # same constant /uploads uses
        return UPLOADS_HOME
    except Exception:  # noqa: BLE001 — same fallback as ml_routes
        return os.path.join(os.environ.get("DEFAULT_ROOT", "/tmp"), "uploads")


def _materialize_b64(b64: str, kind: str) -> str:
    import base64
    import uuid
    raw = base64.b64decode(b64.split(",", 1)[-1] if b64.startswith("data:") else b64)
    home = _uploads_home()
    os.makedirs(home, exist_ok=True)
    dest = os.path.join(home,
                        f"oracle_{uuid.uuid4().hex[:8]}{_B64_EXT.get(kind, '.bin')}")
    with open(dest, "wb") as fh:
        fh.write(raw)
    return dest


def _parse_inputs(raw: list) -> list:
    """Body inputs -> typed InputRefs (b64 payloads land as upload files)."""
    from abstract_hugpy_dev.oracle.contracts import InputKind, InputRef
    refs = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"inputs[{i}] must be an object")
        try:
            kind = InputKind(item.get("kind"))
        except ValueError:
            raise ValueError(
                f"inputs[{i}].kind must be one of "
                f"{[k.value for k in InputKind]}, got {item.get('kind')!r}")
        ref = item.get("text") or item.get("uri") or item.get("ref")
        if not ref and item.get("b64"):
            ref = _materialize_b64(item["b64"], kind.value)
        if not ref:
            raise ValueError(f"inputs[{i}] needs one of uri | b64 | text")
        refs.append(InputRef(kind=kind, ref=ref, label=item.get("label", "")))
    return refs


@oracle_bp.route("/oracle/route", methods=["POST"])
def oracle_route():
    """Route-to-best-result: infer/accept a capability, resolve the best
    eligible model via the k90 catalog, execute through the existing dispatch,
    and answer with artifact(s) + ExecutionReceipt + a mandatory Scorecard."""
    from abstract_hugpy_dev.oracle import router as oracle_router
    from abstract_hugpy_dev.oracle import runtime as oracle_runtime
    from abstract_hugpy_dev.oracle import scorecard as oracle_scorecard
    from abstract_hugpy_dev.oracle.catalog import (
        LEGACY_TASK_CAPABILITY, LEGACY_TASK_EXCLUDED)
    from abstract_hugpy_dev.oracle.contracts import GoalSpec, QualityProfile

    body = request.get_json(silent=True) or {}
    if not body and request.files:
        # Multipart one-shot: reuse the /ml upload helper; the file part becomes
        # an input whose kind the caller names via form field `kind` (default
        # image). Everything else rides in form fields.
        from .ml_routes import _save_multipart_upload
        saved = _save_multipart_upload()
        if saved is not None:
            body = dict(request.form.to_dict())
            existing = body.get("inputs")
            body["inputs"] = list(existing) if isinstance(existing, list) else []
            body["inputs"].append({"kind": request.form.get("kind", "image"),
                                   "uri": saved})

    prompt = (body.get("prompt") or "").strip()
    capability = (body.get("capability") or "").strip() or None

    # A bare legacy task string is folded to its namespaced capability; a task
    # string mapped to NEITHER table is the drift case the k90 handoff names:
    # it must come back as the typed CAPABILITY_GAP shape, never a KeyError.
    if capability and "." not in capability:
        mapped = LEGACY_TASK_CAPABILITY.get(capability)
        if mapped is None:
            reason = LEGACY_TASK_EXCLUDED.get(
                capability,
                f"task string {capability!r} is mapped to no capability "
                f"(oracle catalog: unmapped task)")
            route = oracle_router.RouteDecision(
                capability=f"unmapped.{capability}", execution="gap",
                reasons=(reason,))
            return jsonify({
                "ok": False, "error": "capability gap",
                "route": route.to_dict(),
                "scorecard": oracle_scorecard.build_gap_scorecard(route).to_dict(),
            }), 422
        capability = mapped

    if not prompt and not capability:
        return jsonify({"ok": False,
                        "error": "body needs at least one of prompt | capability"}), 400

    try:
        goal = GoalSpec(
            objective=prompt or f"run {capability}",
            raw_prompt=prompt or f"run {capability}",
            inputs=tuple(_parse_inputs(body.get("inputs") or [])),
            capability=capability,
            quality=QualityProfile(body.get("quality") or "balanced"),
        )
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    try:
        route = oracle_router.resolve_route(
            goal, requested_model=body.get("model_id") or None)
    except oracle_router.RouteRefusal as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001 — a routing fault answers honestly
        logger.exception("POST /oracle/route: routing failed")
        return jsonify({"ok": False, "error": f"{type(exc).__name__}: {exc}"}), 500

    if route.execution == "gap":
        return jsonify({
            "ok": False, "error": "capability gap",
            "goal": goal.to_dict(), "route": route.to_dict(),
            "scorecard": oracle_scorecard.build_gap_scorecard(route).to_dict(),
        }), 422

    if route.execution == "deferred":
        return jsonify({
            "ok": True,
            "routed": route.capability,
            "execution": "deferred",
            "reason": "; ".join(route.reasons) or
                      "video capabilities execute through the studio job pipeline",
            "binding": {"model_id": route.model_id,
                        "model_ids": list(route.model_ids)},
            "alternatives": route.alternatives,
            "goal": goal.to_dict(), "route": route.to_dict(),
            "scorecard": oracle_scorecard.build_deferred_scorecard(route).to_dict(),
        }), 202

    try:
        artifacts, receipt = oracle_runtime.execute_route(goal, route)
    except oracle_runtime.GoalShapeError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001 — typed, never a traceback
        logger.exception("POST /oracle/route: execution wrapper failed")
        return jsonify({"ok": False, "error": f"{type(exc).__name__}: {exc}"}), 500

    # k92: judge evaluation + one bounded repair. Defaults per the operator
    # ruling — evaluate on for the judged capabilities, repair on when a judge
    # ran or a technical check failed; explicit booleans in the body win.
    from abstract_hugpy_dev.oracle import evaluation as oracle_evaluation
    from abstract_hugpy_dev.oracle import repair as oracle_repair

    evaluate_on = body.get("evaluate") if isinstance(body.get("evaluate"), bool) \
        else route.capability in oracle_evaluation.DEFAULT_EVALUATED

    card = oracle_scorecard.build_technical_scorecard(goal, route, artifacts, receipt)
    technical_failed = not card.hard_pass
    if evaluate_on:
        card = oracle_evaluation.evaluate(goal, route, artifacts, receipt, card)

    repair_on = body.get("repair") if isinstance(body.get("repair"), bool) \
        else (evaluate_on or technical_failed)

    repair_info = None
    receipts = None
    if repair_on and not card.hard_pass:
        decision = oracle_repair.attempt_repair(goal, route, card)
        repair_info = decision.to_dict()
        if decision.action != "none":
            try:
                artifacts2, receipt2, route2 = oracle_repair.execute_repair(
                    goal, route, decision)
            except Exception:  # noqa: BLE001 — a broken repair keeps attempt 1
                logger.exception("POST /oracle/route: repair attempt failed; "
                                 "keeping the first attempt's answer")
            else:
                card2 = oracle_scorecard.build_technical_scorecard(
                    goal, route2, artifacts2, receipt2)
                if evaluate_on:
                    card2 = oracle_evaluation.evaluate(
                        goal, route2, artifacts2, receipt2, card2)
                receipts = [receipt.to_dict(), receipt2.to_dict()]
                artifacts, receipt, route = artifacts2, receipt2, route2
                card = oracle_repair.annotate_repaired(card2, decision)

    resp = {
        "ok": True,
        "goal": goal.to_dict(),
        "route": route.to_dict(),
        "artifacts": artifacts,
        "receipt": receipt.to_dict(),
        "scorecard": card.to_dict(),
    }
    if repair_info is not None:
        resp["repair"] = repair_info
    if receipts is not None:
        resp["receipts"] = receipts
    return jsonify(resp)
