"""The Predictions view's read-only API (/api/llm/predictions...).

Every call the wrapper serves records, in ``call_log.response_meta.eta_derivation``
(schema ``hugpy.eta.derivation/1``, added by wrapper 0.1.158), the exact scatter
of rows and the Theil-Sen fit the ETA was derived from: the prompt fit
(uncached prompt tokens -> prompt ms), the decode fit (predicted tokens ->
predicted ms), the output-length distribution, and the load fit (uncached bytes
-> load s), each with the call_log ids that entered the fit and the subset
dropped as Tukey outliers.

Core mirrors every wrapper's call_log into its own DB (hugpy_core/intake), keeping
the wrapper's own row id as ``box_id`` and keying each row by (worker, box_id)
(schema sql/021, sql/022). So the derivation's ``ids`` (wrapper call_log.id) resolve
here as (worker, box_id) — the points the UI draws are the real mirrored rows, not
a recomputation. Nothing is written; every read goes through calllog.query (core's
one reader) against core's own Postgres.

The 'actual' processing time of a call is (prompt_ms + predicted_ms)/1000 — the
measured prefill plus decode. inference_started_at is stamped AFTER prefill, so
responded_at - inference_started_at is never used.

Rows older than wrapper 0.1.158 carry no eta_derivation and no predicted_output_s;
they still list, marked honestly ("no derivation recorded"), with the derived
figures reported as null rather than omitted.
"""
from __future__ import annotations

from flask import jsonify

from abstract_flask import spec

from hugpy_core.calllog.calllog import query as _q
from hugpy_core.web.console_routes import _key_forms

# call_log columns added by later migrations / by wrapper 0.1.158. The API works
# whether or not the DB has taken sql/046 yet: a column that is not present is
# selected as SQL NULL and reported null, never guessed.
_OPTIONAL = ("predicted_output_s", "predicted_basis", "load_s", "load_file")
_present_cache: "set | None" = None


def _present() -> set:
    global _present_cache
    if _present_cache is None:
        rows = _q("SELECT column_name FROM information_schema.columns "
                  "WHERE table_name = 'call_log'")
        _present_cache = {r[0] for r in rows}
    return _present_cache


def _col(name: str) -> str:
    """``name`` if call_log has it, else ``NULL AS name`` — the view never 500s on
    a DB that has not applied sql/046, and the absence is explicit (null)."""
    return name if name in _present() else f"NULL AS {name}"


def _f(v):
    return float(v) if v is not None else None


def _epoch(v):
    return float(v) if v is not None else None


def _model_clause(model: str, params: list) -> str:
    forms = _key_forms(model)
    if not forms:
        return ""
    params.append(list(forms))
    return " AND model_name = ANY(%s)"


def _worker_clause(worker: str, params: list) -> str:
    if not worker:
        return ""
    params.append(worker)
    return " AND worker = %s"


# ── point resolution (the real mirrored rows behind a derivation) ────────────

_POINT_COLS = ("box_id", "request_id", "model_name", "prompt_n", "cache_n",
               "prompt_ms", "predicted_n", "predicted_ms", "model_bytes",
               "load_cached_bytes")


def _current_store(worker: str) -> str:
    """The worker's CURRENT wrapper store incarnation = the box_store_id of its
    most recently received mirrored call. A clean-slate resets box ids to 1 under
    a new store id, so without this the live /current fits would resolve their ids
    against stale rows from an earlier generation that happen to share a box_id."""
    if not worker:
        return ""
    rows = _q("SELECT box_store_id FROM call_log WHERE worker = %s AND box_id IS NOT NULL "
              "ORDER BY received_at DESC NULLS LAST, id DESC LIMIT 1", (worker,))
    return (rows[0][0] or "") if rows else ""


def _resolve(worker: str, store_id: str, ids) -> dict:
    """{box_id: row} for the given wrapper call_log ids on ``worker`` within the
    ONE store incarnation ``store_id`` (the mirror keys every call by
    (worker, box_store_id, box_id); box_id alone collides across clean-slate
    generations — sql/035). Rows the mirror does not have are simply absent from
    the map — the caller reports which ids were missing, never drops them
    silently."""
    want = sorted({int(i) for i in (ids or []) if i is not None})
    if not worker or not want:
        return {}
    cols = ", ".join([*_POINT_COLS, _col("load_s"), "extract(epoch FROM received_at) AS rx"])
    rows = _q(f"SELECT {cols} FROM call_log WHERE worker = %s AND box_store_id = %s "
              f"AND box_id = ANY(%s)", (worker, store_id or "", want))
    out = {}
    for r in rows:
        d = dict(zip([*_POINT_COLS, "load_s", "rx"], r))
        out[int(d["box_id"])] = d
    return out


def _uncached_prompt(d: dict):
    pn = d.get("prompt_n")
    if pn is None:
        return None
    return int(pn) - int(d.get("cache_n") or 0)


def _uncached_bytes(d: dict):
    mb, lc = d.get("model_bytes"), d.get("load_cached_bytes")
    if mb is None:
        return None
    return int(mb) - int(lc or 0)


def _block_points(block: dict, resolved: dict, kind: str) -> dict:
    """Shape one derivation block's points from the resolved mirror rows. Returns
    the point list and the ids that could not be resolved (count + list)."""
    if not isinstance(block, dict):
        return {"points": [], "unresolved": {"count": 0, "ids": []}}
    dropped = {int(i) for i in (block.get("dropped_ids") or []) if i is not None}
    ids = [int(i) for i in (block.get("ids") or []) if i is not None]
    points, missing = [], []
    for i in ids:
        d = resolved.get(i)
        if d is None:
            missing.append(i)
            continue
        is_dropped = i in dropped
        if kind == "prompt":
            points.append({"id": i, "x": _uncached_prompt(d), "y": _f(d.get("prompt_ms")),
                           "dropped": is_dropped, "received_at": _epoch(d.get("rx"))})
        elif kind == "decode":
            points.append({"id": i, "x": (int(d["predicted_n"]) if d.get("predicted_n") is not None else None),
                           "y": _f(d.get("predicted_ms")), "dropped": is_dropped,
                           "received_at": _epoch(d.get("rx"))})
        elif kind == "load":
            points.append({"id": i, "x": _uncached_bytes(d), "y": _f(d.get("load_s")),
                           "dropped": is_dropped, "received_at": _epoch(d.get("rx"))})
        elif kind == "out_tokens":
            points.append({"id": i, "value": (int(d["predicted_n"]) if d.get("predicted_n") is not None else None),
                           "dropped": is_dropped, "received_at": _epoch(d.get("rx"))})
    return {"points": points, "unresolved": {"count": len(missing), "ids": missing}}


def _points_for(worker: str, store_id: str, eta: dict) -> dict:
    """Resolve every block of an eta_derivation to its real mirrored points, within
    the ``store_id`` the derivation's ids belong to (the row's own store for a
    stored call, the box's current store for a live /current fit)."""
    blocks = {k: (eta.get(k) if isinstance(eta, dict) else None)
              for k in ("prompt", "decode", "load", "out_tokens")}
    every = set()
    for b in blocks.values():
        if isinstance(b, dict):
            every |= {int(i) for i in (b.get("ids") or []) if i is not None}
    resolved = _resolve(worker, store_id, every)
    return {k: _block_points(blocks[k], resolved, k) for k in blocks}


# ── row shaping (predicted vs actual) ────────────────────────────────────────

def _actual_s(prompt_ms, predicted_ms):
    """The true processing time: (prefill ms + decode ms)/1000. Null unless both
    measured halves are present."""
    if prompt_ms is None or predicted_ms is None:
        return None
    return (float(prompt_ms) + float(predicted_ms)) / 1000.0


def _shape_row(d: dict) -> dict:
    eta = d.get("eta") if isinstance(d.get("eta"), dict) else None
    actual = _actual_s(d.get("prompt_ms"), d.get("predicted_ms"))
    predicted = _f(d.get("predicted_output_s"))
    band = eta.get("output_band_s") if eta else None
    band = band if (isinstance(band, (list, tuple)) and len(band) == 2) else None
    err = None
    if actual is not None and predicted not in (None, 0):
        err = round(100.0 * (actual - predicted) / predicted, 2)
    in_band = None
    if band is not None and actual is not None:
        in_band = bool(band[0] <= actual <= band[1])
    return {
        "id": int(d["box_id"]) if d.get("box_id") is not None else None,
        "request_id": d.get("request_id"),
        "received_at": _epoch(d.get("rx")),
        "model": d.get("model_name"), "worker": d.get("worker"),
        "endpoint": d.get("endpoint"),
        "predicted_output_s": predicted,
        "actual_s": round(actual, 3) if actual is not None else None,
        "error_pct": err,
        "output_band_s": [float(band[0]), float(band[1])] if band else None,
        "in_band": in_band,
        "basis": (eta.get("basis") if eta else None),
        "estimator": (eta.get("estimator") if eta else None),
        "derivation_recorded": bool(eta),
    }


_LIST_COLS = ("box_id", "request_id", "worker", "endpoint", "model_name",
              "prompt_ms", "predicted_ms")


def _list_select() -> str:
    return (", ".join(_LIST_COLS) + ", " + _col("predicted_output_s")
            + ", response_meta -> 'eta_derivation' AS eta"
            + ", extract(epoch FROM received_at) AS rx")


# ── routes ───────────────────────────────────────────────────────────────────

def predictions_list(**kwargs):
    """GET /api/llm/predictions?worker=&model=&limit= — recent calls, newest
    first: predicted vs actual processing time, error %, band membership, and the
    derivation's basis/estimator. Rows without a derivation list honestly
    (estimator null, derivation_recorded false). Never 500."""
    worker = (kwargs.get("worker") or "").strip()
    model = (kwargs.get("model") or "").strip()
    try:
        limit = max(1, min(int(kwargs.get("limit") or 200), 2000))
    except (TypeError, ValueError):
        limit = 200
    params: list = []
    clause = _worker_clause(worker, params) + _model_clause(model, params)
    params.append(limit)
    try:
        # Predictions are wrapper-side calls only. call_log rows with box_id NULL
        # are core's OWN router records; they share the wrapper row's request_id, so
        # listing them separately duplicates each call as id "—". Exclude them here.
        rows = _q(f"SELECT {_list_select()} FROM call_log "
                  f"WHERE box_id IS NOT NULL{clause} "
                  f"ORDER BY id DESC LIMIT %s", tuple(params))
        out = [_shape_row(dict(zip([*_LIST_COLS, "predicted_output_s", "eta", "rx"], r)))
               for r in rows]
        return jsonify({"rows": out, "count": len(out), "worker": worker or None,
                        "model": model or None,
                        "note": None if any(r["derivation_recorded"] for r in out)
                        else "no derivation recorded for any listed call "
                             "(wrapper predates 0.1.158)"})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"rows": [], "count": 0, "error": f"{type(exc).__name__}: {exc}"})


_DETAIL_COLS = ("box_id", "request_id", "worker", "endpoint", "model_name",
                "prompt_n", "cache_n", "prompt_ms", "predicted_n", "predicted_ms",
                "model_bytes", "load_cached_bytes")


def prediction_detail(**kwargs):
    """GET /api/llm/predictions/<worker>/<id> — the call's eta_derivation plus the
    real mirrored points for each block (prompt/decode/load/out_tokens) and the
    call's own actual point, so the UI can show where reality landed relative to
    the fit. Ids the mirror could not resolve are reported, never dropped."""
    worker = (kwargs.get("worker") or "").strip()
    raw_id = kwargs.get("id")
    try:
        box_id = int(raw_id)
    except (TypeError, ValueError):
        return jsonify({"error": f"id must be an integer, got {raw_id!r}"}), 400
    cols = (", ".join(_DETAIL_COLS) + ", box_store_id, " + _col("predicted_output_s") + ", "
            + _col("predicted_basis") + ", " + _col("load_s")
            + ", response_meta -> 'eta_derivation' AS eta"
            + ", extract(epoch FROM received_at) AS rx")
    try:
        # box_id collides across clean-slate store generations (sql/035); the newest
        # received row is the current generation's call. Its box_store_id scopes the
        # derivation-id resolution below so points come from the SAME generation.
        rows = _q(f"SELECT {cols} FROM call_log WHERE worker = %s AND box_id = %s "
                  f"ORDER BY received_at DESC NULLS LAST, id DESC LIMIT 1",
                  (worker, box_id))
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500
    if not rows:
        return jsonify({"error": f"no call (worker={worker!r}, id={box_id}) in the mirror",
                        "worker": worker, "id": box_id}), 404
    d = dict(zip([*_DETAIL_COLS, "box_store_id", "predicted_output_s", "predicted_basis", "load_s", "eta", "rx"], rows[0]))
    eta = d.get("eta") if isinstance(d.get("eta"), dict) else None
    actual = _actual_s(d.get("prompt_ms"), d.get("predicted_ms"))
    predicted = _f(d.get("predicted_output_s"))
    own = {
        "id": box_id, "request_id": d.get("request_id"), "received_at": _epoch(d.get("rx")),
        "prompt": {"x": _uncached_prompt(d), "y": _f(d.get("prompt_ms"))},
        "decode": {"x": (int(d["predicted_n"]) if d.get("predicted_n") is not None else None),
                   "y": _f(d.get("predicted_ms"))},
        "load": {"x": _uncached_bytes(d), "y": _f(d.get("load_s"))},
        "out_tokens": {"value": (int(d["predicted_n"]) if d.get("predicted_n") is not None else None)},
        "predicted_output_s": predicted,
        "actual_s": round(actual, 3) if actual is not None else None,
    }
    points = _points_for(worker, d.get("box_store_id") or "", eta) if eta else {
        k: {"points": [], "unresolved": {"count": 0, "ids": []}}
        for k in ("prompt", "decode", "load", "out_tokens")}
    return jsonify({
        "worker": worker, "id": box_id, "model": d.get("model_name"),
        "endpoint": d.get("endpoint"),
        "eta_derivation": eta,
        "derivation_recorded": bool(eta),
        "note": None if eta else "no derivation recorded for this call "
                                 "(wrapper predates 0.1.158)",
        "points": points, "actual": own,
    })


def predictions_accuracy(**kwargs):
    """GET /api/llm/predictions/accuracy?worker=&model= — per model: n, mean
    absolute % error over every recorded call with a prediction, band coverage,
    and the (received_at, error_pct) series for an accuracy-over-time view."""
    worker = (kwargs.get("worker") or "").strip()
    model = (kwargs.get("model") or "").strip()
    try:
        limit = max(1, min(int(kwargs.get("limit") or 5000), 20000))
    except (TypeError, ValueError):
        limit = 5000
    params: list = []
    clause = _worker_clause(worker, params) + _model_clause(model, params)
    params.append(limit)
    try:
        # wrapper rows only (box_id NULL == core's router records, same request_id)
        # — a router row must never double-count a model's accuracy.
        rows = _q(f"SELECT {_list_select()} FROM call_log "
                  f"WHERE box_id IS NOT NULL{clause} "
                  f"ORDER BY id DESC LIMIT %s", tuple(params))
    except Exception as exc:  # noqa: BLE001
        return jsonify({"models": [], "error": f"{type(exc).__name__}: {exc}"})
    by: dict = {}
    for r in rows:
        row = _shape_row(dict(zip([*_LIST_COLS, "predicted_output_s", "eta", "rx"], r)))
        if row["error_pct"] is None:
            continue  # no prediction on record for this call
        m = by.setdefault(row["model"], {"errs": [], "band_n": 0, "band_hit": 0, "series": []})
        m["errs"].append(abs(row["error_pct"]))
        if row["in_band"] is not None:
            m["band_n"] += 1
            m["band_hit"] += 1 if row["in_band"] else 0
        m["series"].append({"received_at": row["received_at"], "error_pct": row["error_pct"]})
    models = []
    for name, m in by.items():
        n = len(m["errs"])
        models.append({
            "model": name, "n": n,
            "mean_abs_error_pct": round(sum(m["errs"]) / n, 2) if n else None,
            "band_coverage": round(m["band_hit"] / m["band_n"], 4) if m["band_n"] else None,
            "band_n": m["band_n"],
            "series": sorted(m["series"], key=lambda s: (s["received_at"] or 0)),
        })
    models.sort(key=lambda x: (-x["n"], x["model"] or ""))
    return jsonify({"models": models, "count": len(models), "worker": worker or None,
                    "model": model or None,
                    "note": None if models else "no call on record carries a prediction "
                                                "(wrapper predates 0.1.158)"})


def predictions_current(**kwargs):
    """GET /api/llm/predictions/current?worker=&model= — the wrapper's CURRENT ETA
    fits for ``model``, relayed through the existing authenticated box link
    (/v1/telemetry/eta), with its points resolved from the mirror the same way as
    a stored call. Without ``model`` the wrapper lists its models. Uses no new
    credential path — the same _proxy_worker the console's telemetry browser uses."""
    import urllib.parse

    from hugpy_core.web.recovered_surfaces import _proxy_worker

    worker = (kwargs.get("worker") or "").strip()
    model = (kwargs.get("model") or "").strip()
    if not worker:
        return jsonify({"error": "worker is required (the box whose current fits to read)"}), 400
    path = "/v1/telemetry/eta" + (("?model=" + urllib.parse.quote(model, safe="")) if model else "")
    body, status = _proxy_worker(worker, path)
    if status != 200:
        # _proxy_worker already returns a jsonify'd error body with the box's
        # own words; relay it verbatim, never a canned message.
        return body, status
    telemetry = body.get_json(silent=True) if hasattr(body, "get_json") else None
    if not isinstance(telemetry, dict):
        return jsonify({"worker": worker, "model": model or None, "telemetry": None,
                        "error": "box did not return a telemetry object"}), 502
    if not model or "models" in telemetry:
        # the model index — no single-model points to resolve
        return jsonify({"worker": worker, "model": model or None, "telemetry": telemetry,
                        "points": None})
    # the live fit's ids are the box's CURRENT call_log ids — resolve them against
    # that same (current) store generation in the mirror, never an older one.
    points = _points_for(worker, _current_store(worker), telemetry)
    return jsonify({"worker": worker, "model": model or None, "telemetry": telemetry,
                    "points": points})


# Merged into web_bp under /api/llm/predictions beside model-metrics2 and calls
# (same /api auth gate). The <worker>/<id> leaf is two path params that reach the
# handler as kwargs (response="native" — it answers bare JSON itself).
PREDICTIONS_CATEGORIES = {
    "llm": {
        "predictions": {
            "": predictions_list,
            "accuracy": predictions_accuracy,
            "current": predictions_current,
            "<worker>": {"<id>": spec(prediction_detail, "GET", response="native")},
        },
    },
}
