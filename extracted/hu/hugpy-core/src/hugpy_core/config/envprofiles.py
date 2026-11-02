"""ENV PROFILES for the console's Environments panel: per-model Python envs
(an overlay on a box's engine venv, or isolated), built on the boxes that serve
them. DECLARED in hugpy_core.env_profiles (the operator's rows overlay the
wrapper's code defaults); STATE is each box's own (its front door's /profiles,
reached through the box's hugpy_worker). Read when the panel opens — no polling."""
from __future__ import annotations
from hugpy_core.imports import constants as _C

import json
import os
import urllib.error
import urllib.request
from typing import Optional

from hugpy_core.registry import registry



def _db():
    import psycopg
    from psycopg.rows import dict_row
    from hugpy_core.imports.functions import core_dsn
    return psycopg.connect(core_dsn(), autocommit=True, connect_timeout=5, row_factory=dict_row)


def _declared_rows() -> dict:
    try:
        with _db() as c:
            return {r["name"]: {"base": r["base"], "packages": r["packages"] or []}
                    for r in c.execute("SELECT name, base, packages FROM env_profiles").fetchall()}
    except Exception:  # noqa: BLE001 — the table is created by the wrapper's DDL
        return {}


def _tests() -> dict:
    # An env "▶ test" IS a call (derivation-map AUDIT 6): no side table — the
    # result is the latest env-test call per (profile, box) in the wrapper log,
    # read through calllog.py (the one reader).
    try:
        from hugpy_core.calllog import calllog
        return calllog.env_tests()
    except Exception:  # noqa: BLE001
        return {}


def _box_report(worker: dict) -> dict:
    try:
        with urllib.request.urlopen(worker["url"].rstrip("/") + "/profiles", timeout=5) as r:
            return json.loads(r.read().decode("utf-8") or "{}").get("profiles") or {}
    except Exception:  # noqa: BLE001 — an unreachable box shows as not reported
        return {}


def env_profiles_list():
    rows = _declared_rows()
    tests = _tests()
    out: dict = {n: {"name": n, "base": d["base"], "packages": d["packages"], "status": "approved",
                     "source": "db", "workers": []} for n, d in rows.items()}
    for w in registry.all_workers():
        if not registry.is_online(w) or not w.get("url"):
            continue
        for name, st in _box_report(w).items():
            p = out.setdefault(name, {"name": name, "base": st.get("base"), "packages": st.get("packages") or [],
                                      "status": "approved", "source": "default", "workers": []})
            if not p["packages"] and st.get("packages"):
                p["packages"] = st["packages"]
            p["workers"].append({"worker_id": w["id"], "worker": w.get("name"), "state": st.get("state"),
                                 "error": st.get("error"), "lock": st.get("lock") or [],
                                 "materialized_at": st.get("materialized_at"),
                                 "test": tests.get((name, w["id"]))})
    return {"bases": ["worker", "isolated"], "profiles": sorted(out.values(), key=lambda p: p["name"])}


def env_profiles_save(name=None, packages=None, base=None):
    """Declare (or replace) a profile: {name, packages:[...], base: worker|isolated}.
    Every box overlays it on its code defaults and builds it on first use."""
    name = str(name or "").strip()
    pkgs = packages or []
    base = base or "worker"
    if not name or not isinstance(pkgs, list) or not all(isinstance(p, str) and p.strip() for p in pkgs) \
            or base not in ("worker", "isolated"):
        return {"error": "need name, packages (list of pip specs), base worker|isolated"}
    from psycopg.types.json import Jsonb
    with _db() as c:
        c.execute("INSERT INTO env_profiles (name, base, packages, updated_at) VALUES (%s,%s,%s,now()) "
                  "ON CONFLICT (name) DO UPDATE SET base=EXCLUDED.base, packages=EXCLUDED.packages, updated_at=now()",
                  (name, base, Jsonb([p.strip() for p in pkgs])))
    return {"ok": True, "name": name, "base": base, "packages": pkgs}


def env_profiles_approve(name=None):
    # a declaration is the operator's: every stored profile is approved
    return {"ok": True, "name": name, "status": "approved"}


# ── "▶ test": one minimal real call of the model's task, pinned to that box ──
# (the model runs in its attributed environment there; the result is stored per
# box on the profile row and shown on the worker chip). Inputs are the smallest
# valid request per route — a protocol table, not model choices.
def _silence_wav_b64(seconds: float = 0.5, rate: int = 16000) -> str:
    import base64
    import io
    import wave
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00" * int(seconds * rate))
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _probe(task: str, model: str, worker_name: str, metadata: dict) -> "tuple[str, dict]":
    # metadata carries intent 'env-test' + the (profile, worker_id) it belongs to
    # so the call_log row IS the stored result (calllog.env_tests reads it back).
    pin = {"worker": worker_name}
    if task in ("text-generation", "image-text-to-text"):
        return "/v1/chat/completions", {"model": model, "messages": [{"role": "user", "content": "hi"}],
                                        "max_tokens": 1, "alloc": pin, "metadata": metadata}
    from hugpy_engine.task_endpoints import TASK_ROUTES
    route = (TASK_ROUTES.get(task) or (None,))[0]
    if route is None:
        raise ValueError(f"no test request for task {task!r}")
    body = {"model": model, "alloc": pin, "metadata": metadata}
    if route == "/v1/audio/transcriptions":
        body.update(file_b64=_silence_wav_b64(), filename="test.wav")
    elif route in ("/v1/images/generations", "/v1/videos/generations"):
        body.update(prompt="test")
    else:
        body.update(input="A short test sentence for the environment check.")
    return route, body


def run_test(name: str, worker: dict, model: str, *, base: Optional[str] = None,
             extra_metadata: Optional[dict] = None, timeout: float = 1800) -> dict:
    """ONE minimal real call of the model's task, pinned to ``worker`` — the model
    runs in its attributed environment there. The call itself (metadata intent
    'env-test' + the profile + worker) is the record (calllog.env_tests). Used by
    the ▶ test route and by the brain's fix ladder (fix_ladder.py)."""
    import time
    base = (base or os.environ.get(_C.ENV_SELF_BASE) or _C.DEFAULT_SELF_BASE).rstrip("/")
    try:
        from hugpy_engine.config.models.models_config import MODEL_REGISTRY, refresh_registry
        refresh_registry()
        cfg = MODEL_REGISTRY.get(model)
        task = getattr(cfg, "primary_task", None) if cfg else None
        if isinstance(task, (list, tuple)):
            task = task[0] if task else None
        metadata = {"intent": "env-test", "env_profile": name, "worker_id": worker["id"],
                    **(extra_metadata or {})}
        route, body = _probe(task or "text-generation", model, worker.get("name"), metadata)
        req = urllib.request.Request(base + route, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                status, out = r.status, r.read()[:4000].decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            status, out = exc.code, exc.read()[:4000].decode("utf-8", "replace")
        ok = 200 <= status < 300
        return {"ok": ok, "model": model, "task": task, "route": route, "status": status,
                "error": None if ok else out[:2000], "at": time.time()}
    except Exception as exc:  # noqa: BLE001 — the result IS the report
        return {"ok": False, "model": model, "error": f"{type(exc).__name__}: {exc}", "at": time.time()}


def env_profiles_test(name=None, worker=None, model=None):
    wid, model = str(worker or "").strip(), str(model or "").strip()
    w = registry.lookup_worker(wid) if wid else None
    if not w or not model:
        return {"error": "need worker (id) and model"}
    # run_test defaults its base to the configured core self base (HUGPY_SELF_BASE)
    # when none is passed — the convention's views do not read ``request``.
    # No side table: the probe call (metadata intent 'env-test') is logged to the
    # wrapper's call_log by the normal intake, and calllog.env_tests reads it back
    # as the per-(profile, box) result — the call is the single record.
    return run_test(name, w, model)
