"""Cron job API — list, add, delete, toggle, run."""


class WebCronMixin:
    GET_ROUTES = {
        "/api/cron": "_get_cron",
    }
    POST_ROUTES = {
        "/api/cron/add": "_post_api_cron_add",
        "/api/cron/delete": "_post_api_cron_delete",
        "/api/cron/toggle": "_post_api_cron_toggle",
        "/api/cron/run": "_post_api_cron_run",
    }

    """Mixin providing cron route handlers."""

    def _get_cron(self):
        """Get cron."""
        if not self._require_auth("user"):
            return
        from salmalm.core import _llm_cron

        self._json({"jobs": _llm_cron.list_jobs() if _llm_cron else []})

# ── FastAPI router ────────────────────────────────────────────────────────────
import asyncio as _asyncio
from fastapi import APIRouter as _APIRouter, Request as _Request, Depends as _Depends, Query as _Query
from fastapi.responses import JSONResponse as _JSON, Response as _Response, HTMLResponse as _HTML, StreamingResponse as _SR, RedirectResponse as _RR
from salmalm.web.fastapi_deps import require_auth as _auth, optional_auth as _optauth

router = _APIRouter()

@router.get("/api/cron")
async def get_cron(_u=_Depends(_auth)):
    from salmalm.core import _llm_cron
    return _JSON(content={"jobs": _llm_cron.list_jobs() if _llm_cron else []})

@router.post("/api/cron/add")
async def post_cron_add(request: _Request, _u=_Depends(_auth)):
    from salmalm.core import _llm_cron
    body = await request.json()
    if not _llm_cron:
        return _JSON(content={"ok": False, "error": "Cron not available"}, status_code=500)
    _uid_ca = _u.get("id")
    _is_admin_ca = _u.get("role") == "admin"
    _MAX_JOBS_PER_USER = 50
    if not _is_admin_ca and _uid_ca is not None:
        user_job_count = sum(1 for j in _llm_cron.jobs if j.get("user_id") == _uid_ca)
        if user_job_count >= _MAX_JOBS_PER_USER:
            return _JSON(content={"ok": False, "error": f"Cron job limit reached ({_MAX_JOBS_PER_USER} max)"}, status_code=400)
    name = str(body.get("name", "untitled"))[:128]
    try:
        interval = max(int(body.get("interval", 3600)), 60)
    except (TypeError, ValueError):
        interval = 3600
    prompt = body.get("prompt", "")
    run_at = body.get("run_at", "")
    if not prompt:
        return _JSON(content={"ok": False, "error": "Prompt required"}, status_code=400)
    if run_at:
        if len(run_at) <= 5:
            schedule = {"kind": "cron", "expr": (lambda _p: f"{_p[1].zfill(2)} {_p[0].zfill(2)} * * *" if len(_p) == 2 else "0 9 * * *")(run_at.split(':', 1))}
        else:
            schedule = {"kind": "at", "time": run_at}
    else:
        schedule = {"kind": "every", "seconds": interval}
    job = _llm_cron.add_job(name, schedule, prompt, user_id=_uid_ca)
    return _JSON(content={"ok": True, "job": job})

@router.post("/api/cron/delete")
async def post_cron_delete(request: _Request, _u=_Depends(_auth)):
    from salmalm.core import _llm_cron
    body = await request.json()
    job_id = body.get("id", "")
    _uid_cdel = _u.get("id") if _u.get("role") != "admin" else None
    if _llm_cron:
        for j in _llm_cron.jobs:
            if j["id"] == job_id:
                if _uid_cdel is not None and j.get("user_id") != _uid_cdel:
                    return _JSON(content={"ok": False, "error": "Forbidden"}, status_code=403)
                break
        if _llm_cron.remove_job(job_id):
            return _JSON(content={"ok": True})
    return _JSON(content={"ok": False, "error": "Job not found"}, status_code=404)

@router.post("/api/cron/toggle")
async def post_cron_toggle(request: _Request, _u=_Depends(_auth)):
    from salmalm.core import _llm_cron
    body = await request.json()
    job_id = body.get("id", "")
    _uid_ctog = _u.get("id") if _u.get("role") != "admin" else None
    if _llm_cron:
        for j in _llm_cron.jobs:
            if j["id"] == job_id:
                if _uid_ctog is not None and j.get("user_id") != _uid_ctog:
                    return _JSON(content={"ok": False, "error": "Forbidden"}, status_code=403)
                j["enabled"] = not j["enabled"]
                _llm_cron.save_jobs()
                return _JSON(content={"ok": True, "enabled": j["enabled"]})
    return _JSON(content={"ok": False, "error": "Job not found"}, status_code=404)

@router.post("/api/cron/run")
async def post_cron_run(request: _Request, _u=_Depends(_auth)):
    import threading
    from salmalm.core import _llm_cron
    body = await request.json()
    job_id = body.get("id", "")
    _uid_crun = _u.get("id") if _u.get("role") != "admin" else None
    if _llm_cron:
        for j in _llm_cron.jobs:
            if j["id"] == job_id:
                if _uid_crun is not None and j.get("user_id") != _uid_crun:
                    return _JSON(content={"ok": False, "error": "Forbidden"}, status_code=403)
                threading.Thread(target=_llm_cron._execute_job, args=(j,), daemon=True).start()
                return _JSON(content={"ok": True, "message": "Job triggered"})
    return _JSON(content={"ok": False, "error": "Job not found"}, status_code=404)
