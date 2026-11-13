"""The engine database's read-only API (/api/llm/engines...).

Wrapper owns this data (fitevict schema 0061 to 0063): which engines the box can run, what a byte and a
token cost on each, what each engine still needs per model, and what every call did against the order of
operations. Core mirrors it (intake/mirror.py, sql/052) and derives nothing. An engine with no recorded
calls has NULL rates and is reported as unmeasured, never given a figure.
"""
from __future__ import annotations

from flask import jsonify

from abstract_flask import spec

from hugpy_core.calllog.calllog import query as _q

_ENGINE_COLS = ("worker", "engine", "runner", "layout", "endpoint", "output", "tasks", "counts_tokens", "note")
_BASELINE_COLS = ("worker", "baseline_id", "engine", "placement", "threads", "weights_bytes_per_ms",
                  "kv_bytes_per_ms", "overhead_ms", "seconds_per_call", "load_bytes_per_s", "samples", "basis")
_PRICE_COLS = ("worker", "model", "baseline_id", "engine", "placement", "threads", "factor", "kappa",
               "ms_per_token_at_no_context", "ms_per_token_per_context_token", "seconds_per_call",
               "out_lo", "out_mid", "out_hi", "samples")
_ALIGN_COLS = ("worker", "engine", "ready", "checks")
_STAGE_COLS = ("worker", "stage_no", "phase", "stage", "owner", "started_at", "finished_at", "predicted_s", "note")
_BREAK_COLS = ("worker", "started_early", "started_after", "by_seconds", "early_owner", "later_owner")


def _rows(cols, sql, params=()):
    return [dict(zip(cols, row)) for row in _q(sql, params)]


def _measured(baseline: dict) -> bool:
    return baseline["weights_bytes_per_ms"] is not None or baseline["seconds_per_call"] is not None


def overview(**kwargs):
    """GET /api/llm/engines?worker= -- each engine with its baselines, every (model, baseline) price, and
    how many models each engine has what it needs for. Never 500."""
    worker = (kwargs.get("worker") or "").strip()
    where, params = ("WHERE worker = %s", (worker,)) if worker else ("", ())
    try:
        engines = _rows(_ENGINE_COLS, f"SELECT {','.join(_ENGINE_COLS)} FROM engines {where} ORDER BY worker, engine", params)
        baselines = _rows(_BASELINE_COLS, f"SELECT {','.join(_BASELINE_COLS)} FROM engine_baselines {where} "
                                          "ORDER BY worker, engine, placement, threads", params)
        prices = _rows(_PRICE_COLS, f"SELECT {','.join(_PRICE_COLS)} FROM engine_prices {where} "
                                    "ORDER BY worker, engine, ms_per_token_at_no_context, seconds_per_call", params)
        alignment = _rows(_ALIGN_COLS, f"SELECT worker, engine, sum(ready), count(*) FROM engine_alignment {where} "
                                       "GROUP BY worker, engine ORDER BY worker, engine", params)
        by_engine: dict = {}
        for base in baselines:
            by_engine.setdefault((base["worker"], base["engine"]), []).append({**base, "measured": _measured(base)})
        for engine in engines:
            engine["baselines"] = by_engine.get((engine["worker"], engine["engine"]), [])
            engine["measured"] = any(b["measured"] for b in engine["baselines"])
        return jsonify({"worker": worker or None, "engines": engines, "prices": prices, "alignment": alignment})
    except Exception as exc:  # noqa: BLE001 -- a console read reports, it does not fail
        return jsonify({"worker": worker or None, "engines": [], "prices": [], "alignment": [],
                        "error": f"{type(exc).__name__}: {exc}"})


def call_stages(request_id="", **kwargs):
    """GET /api/llm/engines/call/<request_id> -- what the call did in the order it really happened, where
    it left the order of operations, and the queue's decision for it."""
    try:
        stages = _rows(_STAGE_COLS, "SELECT c.worker, o.stage_no, o.phase, c.stage, o.owner, c.started_at, c.finished_at, "
                                    "s.predicted_s, s.note FROM call_order c "
                                    "LEFT JOIN call_stages s ON s.worker = c.worker AND s.request_id = c.request_id "
                                    " AND s.stage = c.stage AND s.started_at = c.started_at "
                                    "LEFT JOIN engine_stage_order o ON o.worker = c.worker AND o.stage = c.stage "
                                    "WHERE c.request_id = %s ORDER BY c.started_at, o.stage_no", (request_id,))
        breaks = _rows(_BREAK_COLS, f"SELECT {','.join(_BREAK_COLS)} FROM call_order_breaks WHERE request_id = %s",
                       (request_id,))
        queue = _q("SELECT request_params->'queue' FROM call_log WHERE request_id = %s AND box_id IS NOT NULL LIMIT 1",
                   (request_id,))
        return jsonify({"request_id": request_id, "stages": stages, "order_breaks": breaks,
                        "queue": queue[0][0] if queue else None}), (200 if stages else 404)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"request_id": request_id, "stages": [], "order_breaks": [], "queue": None,
                        "error": f"{type(exc).__name__}: {exc}"}), 200


# Merged into web_bp beside the predictions routes (same /api auth gate).
ENGINES_CATEGORIES = {
    "llm": {
        "engines": {
            "": overview,
            "call": {"<request_id>": spec(call_stages, "GET", response="native")},
        },
    },
}
