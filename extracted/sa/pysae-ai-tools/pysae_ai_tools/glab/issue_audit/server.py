"""FastAPI server for the GitLab issue audit HTML report.

Usage:
    pysae-ai-tools glab issue-audit-server --port PORT

Flow:
1. Audit script posts results -> GET / shows report
2. User clicks Fix -> POST /api/fix/{project_path}/{iid}
3. Server spawns `claude -p /glab-issue-audit --fix --issue <project>#<iid>`
4. Browser polls GET /api/fix-status/{request_id} for completion
"""

import asyncio
import importlib.resources
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import urllib.error
import urllib.request
import uuid
from collections.abc import AsyncGenerator
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Annotated, Any

import typer
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from starlette.responses import StreamingResponse

from ...common.local_server import LocalServer
from ...common.paths import temp_path
from .models import (
    AuditProgress,
    AuditResults,
    ClientsResponse,
    ErrorResponse,
    FixAllRequest,
    FixAllResponse,
    FixPlan,
    FixPreviewResponse,
    FixTaskState,
    IssuePlan,
    IssueResult,
    PlanResults,
    Status,
    StatusResponse,
)
from .rules import RULES

SHUTDOWN_TIMEOUT = 5 * 60
PID_FILE = temp_path("pysae-audit-server.pid")

app = FastAPI(title="Pysae Issue Audit")

_results: AuditResults | None = None
_results_lock = threading.Lock()
_fix_tasks: dict[str, FixTaskState] = {}  # request_id -> task state

_server = LocalServer(
    app=app,
    module="pysae_ai_tools.glab.issue_audit.server",
    pid_file=PID_FILE,
    health_path="/api/results",
    healthy_statuses={200, 202},
    shutdown_timeout=SHUTDOWN_TIMEOUT,
)
_schedule_shutdown = _server.schedule_shutdown


def _templates_dir() -> Traversable:
    return importlib.resources.files("pysae_ai_tools.glab.issue_audit.templates")


# ---------------------------------------------------------------------------
# Static / HTML
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    tpl = _templates_dir().joinpath("audit.html")
    return HTMLResponse(
        tpl.read_text(encoding="utf-8"), headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )


@app.get("/static/{filename}")
async def static_file(filename: str) -> Response:
    path = _templates_dir().joinpath(filename)
    if not path.is_file():
        return JSONResponse({"error": "not found"}, status_code=404)
    content_types = {".css": "text/css", ".js": "application/javascript"}
    return FileResponse(
        str(path),
        media_type=content_types.get(Path(filename).suffix, "text/plain"),
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
    )


# ---------------------------------------------------------------------------
# Config (derived from rules registry -- single source of truth)
# ---------------------------------------------------------------------------


@app.get("/api/config")
async def get_config() -> dict[str, Any]:
    all_checks = list(RULES.keys())
    check_labels = {name: rule.display_name for name, rule in RULES.items()}
    check_colors = {name: rule.color for name, rule in RULES.items()}
    fix_labels = {}
    for rule in RULES.values():
        fix_labels.update(rule.fix_types)
    return {
        "all_checks": all_checks,
        "check_labels": check_labels,
        "check_colors": check_colors,
        "fix_labels": fix_labels,
    }


# ---------------------------------------------------------------------------
# SSE broadcast (queue-per-client)
# ---------------------------------------------------------------------------

_sse_queues: list[asyncio.Queue[str]] = []
_sse_queues_lock = threading.Lock()


def _broadcast(event_type: str, data: str) -> None:
    """Send an SSE event to all connected clients."""
    msg = f"event: {event_type}\ndata: {data}\n\n"
    with _sse_queues_lock:
        for q in _sse_queues:
            try:
                q.put_nowait(msg)
            except asyncio.QueueFull:
                # Queue full -- drop oldest to make room for critical events
                try:
                    q.get_nowait()
                    q.put_nowait(msg)
                except (asyncio.QueueEmpty, asyncio.QueueFull):
                    pass


_sse_clients = 0
_sse_clients_lock = threading.Lock()


@app.get("/api/events")
async def sse_events() -> StreamingResponse:
    global _sse_clients

    async def event_stream() -> AsyncGenerator[str]:
        global _sse_clients
        queue: asyncio.Queue[str] = asyncio.Queue(maxsize=2000)
        with _sse_queues_lock:
            _sse_queues.append(queue)
        with _sse_clients_lock:
            _sse_clients += 1
        try:
            while True:
                try:
                    msg = await asyncio.wait_for(queue.get(), timeout=30)
                    yield msg
                except asyncio.TimeoutError:
                    yield ":\n\n"  # keepalive
        finally:
            with _sse_queues_lock:
                _sse_queues.remove(queue)
            with _sse_clients_lock:
                _sse_clients -= 1

    return StreamingResponse(
        event_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


@app.get("/api/clients")
async def get_clients() -> ClientsResponse:
    with _sse_clients_lock:
        return ClientsResponse(connected=_sse_clients)


@app.post("/api/keepalive")
async def keepalive() -> StatusResponse:
    _schedule_shutdown()
    return StatusResponse(status=Status.OK)


# ---------------------------------------------------------------------------
# Audit results + incremental updates
# ---------------------------------------------------------------------------

_progress: AuditProgress | None = None
_progress_lock = threading.Lock()


@app.post("/api/progress")
async def post_progress(payload: AuditProgress) -> StatusResponse:
    global _progress
    with _progress_lock:
        _progress = payload
    _broadcast("progress", payload.model_dump_json())
    return StatusResponse(status=Status.OK)


@app.post("/api/results")
async def post_results(payload: AuditResults) -> StatusResponse:
    global _results
    with _results_lock:
        _results = payload
    _broadcast("update", "sync")
    return StatusResponse(status=Status.OK)


@app.post("/api/results/issue")
async def post_results_issue(payload: IssueResult) -> StatusResponse:
    """Upsert an issue result and broadcast it via SSE."""
    with _results_lock:
        if _results is not None:
            replaced = False
            for idx, existing in enumerate(_results.issues):
                if existing.iid == payload.iid and existing.project_id == payload.project_id:
                    _results.issues[idx] = payload
                    replaced = True
                    break
            if not replaced:
                _results.issues.append(payload)
    _broadcast("issue", payload.model_dump_json())
    return StatusResponse(status=Status.OK)


@app.post("/api/plan")
async def post_plan(payload: PlanResults) -> StatusResponse:
    global _results, _progress, _abort_requested
    with _results_lock:
        if _results is not None:
            _results.plan = payload.plan
            _results.plan_perf = payload.perf
    with _progress_lock:
        _progress = None
    with _abort_lock:
        _abort_requested = False
    _broadcast("update", "sync")
    return StatusResponse(status=Status.OK)


@app.post("/api/plan/issue")
async def post_plan_issue_endpoint(payload: IssuePlan) -> StatusResponse:
    """Add/update a single issue plan and broadcast it via SSE."""
    with _results_lock:
        if _results is not None:
            existing = {ip.iid: i for i, ip in enumerate(_results.plan.issues)}
            if payload.iid in existing:
                _results.plan.issues[existing[payload.iid]] = payload
            else:
                _results.plan.issues.append(payload)
    _broadcast("plan_issue", payload.model_dump_json())
    return StatusResponse(status=Status.OK)


@app.get("/api/results", response_model=None)
async def get_results() -> AuditResults | JSONResponse:
    with _results_lock:
        if _results is None:
            return JSONResponse(StatusResponse(status=Status.PENDING).model_dump(), status_code=202)
        return _results


# ---------------------------------------------------------------------------
# Abort
# ---------------------------------------------------------------------------

_abort_requested = False
_abort_lock = threading.Lock()


@app.post("/api/abort")
async def request_abort() -> StatusResponse:
    global _abort_requested
    with _abort_lock:
        _abort_requested = True
    return StatusResponse(status=Status.OK)


@app.get("/api/abort")
async def check_abort() -> JSONResponse:
    with _abort_lock:
        if _abort_requested:
            return JSONResponse({"abort": True})
        return JSONResponse({"abort": False})


@app.delete("/api/abort")
async def reset_abort() -> StatusResponse:
    global _abort_requested
    with _abort_lock:
        _abort_requested = False
    return StatusResponse(status=Status.OK)


@app.post("/api/refresh")
async def refresh_audit() -> StatusResponse:
    """Re-run the audit with the same parameters."""
    global _abort_requested
    with _abort_lock:
        _abort_requested = False
    with _results_lock:
        ctx = _results.context if _results else None
        scopes = _results.active_scopes if _results else None
    args = [sys.executable, "-m", "pysae_ai_tools.glab.issue_audit.audit_issues"]
    if ctx:
        if ctx.project:
            args += ["--project", ctx.project]
        if ctx.user:
            args += ["--user", ctx.user]
        if ctx.search:
            for term in ctx.search.split(", "):
                args += ["--search", term]
    if scopes:
        active = [k for k, v in scopes.items() if v]
        if active:
            args += ["--scope"] + active
    log_path = temp_path("pysae-audit-subprocess.log")
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"\n{'=' * 60}\nAudit subprocess started\n{'=' * 60}\n")
        log.flush()
        subprocess.Popen(args, stdout=log, stderr=log)
    return StatusResponse(status=Status.OK)


# ---------------------------------------------------------------------------
# Fix via plan generation + apply
# ---------------------------------------------------------------------------


def _get_plan_for_issue(iid: int) -> FixPlan | None:
    """Extract the plan for a single issue from the stored results."""
    with _results_lock:
        if _results is None:
            return None
        for issue_plan in _results.plan.issues:
            if issue_plan.iid == iid:
                return FixPlan(issues=[issue_plan])
    return None


def _apply_plan_data(request_id: str, plan: FixPlan) -> None:
    """Apply a plan using the audit_issues --apply mechanism."""
    _fix_tasks[request_id].status = Status.APPLYING
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".plan", delete=False) as f:
            json.dump(plan.model_dump(), f)
            plan_path = f.name

        result = subprocess.run(
            [sys.executable, "-m", "pysae_ai_tools.glab.issue_audit.audit_issues", "--apply", plan_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        _fix_tasks[request_id] = FixTaskState(
            status=Status.DONE if result.returncode == 0 else Status.FAILED,
            output=result.stdout + result.stderr,
        )
    except Exception as e:
        _fix_tasks[request_id] = FixTaskState(status=Status.FAILED, output=str(e))


@app.post("/api/fix/{project_path:path}/{iid}", response_model=None)
async def fix_issue(project_path: str, iid: int) -> FixPreviewResponse | JSONResponse:
    """Get the fix plan preview for an issue (instant, from pre-computed plan)."""
    plan = _get_plan_for_issue(iid)
    if not plan or not plan.issues:
        return JSONResponse(ErrorResponse(error="no plan for this issue").model_dump(), status_code=404)
    request_id = str(uuid.uuid4())[:8]
    _fix_tasks[request_id] = FixTaskState(status=Status.PREVIEW, plan=plan)
    return FixPreviewResponse(request_id=request_id, status=Status.PREVIEW, plan=plan)


@app.post("/api/fix-apply/{request_id}", response_model=None)
async def apply_fix(request_id: str) -> StatusResponse | JSONResponse:
    """Apply the plan (after user confirms preview)."""
    task = _fix_tasks.get(request_id)
    if not task or task.status != Status.PREVIEW:
        return JSONResponse(ErrorResponse(error="no plan to apply").model_dump(), status_code=400)
    if not task.plan:
        return JSONResponse(ErrorResponse(error="no plan data").model_dump(), status_code=400)
    thread = threading.Thread(target=_apply_plan_data, args=(request_id, task.plan), daemon=True)
    thread.start()
    return StatusResponse(status=Status.APPLYING)


@app.post("/api/fix-all", response_model=None)
async def fix_all(req: FixAllRequest) -> FixAllResponse | JSONResponse:
    """Fix all issues in the given list. Format: ['pysae/api#123', 'pysae/op#456']."""
    with _results_lock:
        if _results is None:
            return JSONResponse(ErrorResponse(error="no audit results").model_dump(), status_code=400)
        # Parse issue keys and collect plans
        issue_plans = []
        for key in req.issues:
            try:
                path, iid_str = key.rsplit("#", 1)
                iid = int(iid_str)
            except ValueError:
                continue
            for ip in _results.plan.issues:
                if ip.iid == iid and ip.project_path == path:
                    issue_plans.append(ip)
                    break
    if not issue_plans:
        return JSONResponse(ErrorResponse(error="no fixable issues found").model_dump(), status_code=404)
    plan = FixPlan(issues=issue_plans)
    request_id = str(uuid.uuid4())[:8]
    _fix_tasks[request_id] = FixTaskState(status=Status.APPLYING, plan=plan)
    thread = threading.Thread(target=_apply_plan_data, args=(request_id, plan), daemon=True)
    thread.start()
    return FixAllResponse(request_id=request_id, status=Status.APPLYING, count=len(issue_plans))


@app.get("/api/fix-status/{request_id}", response_model=None)
async def fix_status(request_id: str) -> FixTaskState | JSONResponse:
    task = _fix_tasks.get(request_id)
    if task is None:
        return JSONResponse(ErrorResponse(error="not found").model_dump(), status_code=404)
    return task


@app.post("/api/shutdown")
async def shutdown() -> StatusResponse:
    os.kill(os.getpid(), signal.SIGTERM)
    return StatusResponse(status=Status.OK)


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------

find_free_port = LocalServer.find_free_port
run_server = _server.run
ensure_server = _server.ensure


def post_audit_results(results: dict[str, Any], port: int) -> None:
    data = json.dumps(results).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/api/results",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:2000]
        print(f"Failed to post results to server: {e}\n{body}", file=sys.stderr)
    except urllib.error.URLError as e:
        print(f"Failed to post results to server: {e}", file=sys.stderr)


def post_result_issue(issue: dict[str, Any], port: int) -> None:
    data = json.dumps(issue).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/api/results/issue",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except (urllib.error.URLError, OSError):
        pass


def post_plan_issue(issue_plan: dict[str, Any], port: int) -> None:
    data = json.dumps(issue_plan).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/api/plan/issue",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except (urllib.error.URLError, OSError):
        pass


def post_plan_results(plan: dict[str, Any], port: int) -> None:
    data = json.dumps(plan).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/api/plan",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:2000]
        print(f"Failed to post plan to server: {e}\n{body}", file=sys.stderr)
    except urllib.error.URLError as e:
        print(f"Failed to post plan to server: {e}", file=sys.stderr)


def post_audit_progress(progress: dict[str, Any], port: int) -> None:
    data = json.dumps(progress).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/api/progress",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=2)
    except (urllib.error.URLError, OSError):
        pass


cli = typer.Typer()


@cli.command()
def main(
    port: Annotated[int, typer.Option("--port", help="Port to run the server on")],
) -> None:
    run_server(port)


if __name__ == "__main__":
    cli()
