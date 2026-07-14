"""Workflow submission HTTP service (aiohttp).

A small, world-agnostic HTTP service that accepts workflow scripts, compiles them
for fast-fail feedback, and runs them one at a time (FIFO). The service never
imports world code. Two wiring shapes are supported:

* **Component wiring** (what the workflow world uses): pass ``backend`` +
  ``journal_dir`` (and optionally ``cost_source`` / ``default_budget_usd`` /
  ``max_concurrent_envs`` / ``max_total_calls``) and the service builds a fresh
  journal + budget + runtime per submission, with the budget baseline captured
  from the cost source at workflow start (serve-mode delta accounting) and a
  :class:`~plato.workflows.budget.BudgetRefresher` running for the duration of
  each workflow.
* **Runtime-factory injection** (tests, custom worlds): pass ``runtime_factory``,
  a callable that, given a :class:`WorkflowSubmission`, builds a fully-wired
  :class:`WorkflowExecution`. The service only drives that execution and reports
  on it.

Endpoints (bearer-token auth on all except ``/healthz``):

* ``POST /workflows`` — ``{script, args?, name?, budget_usd?, workflow_id?}`` ->
  ``422`` with a line-remapped compile error, or ``{workflow_id, status}``.
* ``GET  /workflows/{id}`` -> ``{workflow_id, status, phase, stats, spent_usd, result?}``.
* ``GET  /workflows/{id}/result`` -> ``202`` while running/queued, else ``{result, ...}``.
* ``GET  /workflows/{id}/events?after_seq=N`` -> ``{events: [...], next_seq}``.
* ``POST /workflows/{id}/cancel`` -> ``{workflow_id, status}``.
* ``GET  /healthz`` (no auth) -> ``{status: "ok"}``.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import logging
import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from aiohttp import web

from plato.otel import get_tracer
from plato.workflows.backend import AgentBackend
from plato.workflows.budget import Budget, BudgetRefresher, CostSource
from plato.workflows.errors import WorkflowCancelledError, WorkflowScriptError
from plato.workflows.journal import Journal
from plato.workflows.runtime import WorkflowRuntime
from plato.workflows.script import compile_workflow_script

if TYPE_CHECKING:
    from plato.workflows.script import CompiledWorkflow

logger = logging.getLogger("plato.workflows.service")
tracer = get_tracer("plato.workflows")

# Terminal statuses — a workflow in one of these never runs again in-process.
_TERMINAL = frozenset({"complete", "error", "cancelled"})

# On-disk submission-record schema version (journal_dir/<id>/submission.json).
_SUBMISSION_VERSION = 1

# Journal ``workflow_result`` status -> service-facing status.
_JOURNAL_STATUS_TO_SERVICE = {"ok": "complete", "cancelled": "cancelled", "error": "error"}

# Error surfaced for a rehydrated entry whose journal has no workflow_result
# (the session crashed/restarted mid-run). Resubmitting identical content
# re-enqueues it — journal replay makes the re-run cheap.
_INTERRUPTED_ERROR = "interrupted by session crash/restart (resubmit identical content to re-run from replay cache)"


def _canonical_json(value: Any) -> str:
    """Deterministic JSON encoding for content hashing (shared with the journal key rule)."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def default_workflow_id(script: str, args: Any) -> str:
    """Content-addressed default id: ``wf-`` + sha256(script + canonical_json(args))[:12]."""
    digest = hashlib.sha256((script + _canonical_json(args)).encode("utf-8")).hexdigest()
    return f"wf-{digest[:12]}"


@dataclass
class WorkflowSubmission:
    """Immutable description of a submitted workflow handed to the runtime factory.

    The ``cancel_event`` is owned by the service and MUST be wired into the
    :class:`~plato.workflows.runtime.WorkflowRuntime` the factory builds so that
    ``POST /workflows/{id}/cancel`` propagates into the running workflow.
    """

    workflow_id: str
    script: str
    args: Any
    name: str | None
    budget_usd: float | None
    cancel_event: asyncio.Event


@dataclass
class WorkflowExecution:
    """The wired-up execution the runtime factory returns for a submission."""

    runtime: WorkflowRuntime
    journal: Journal
    budget: Budget
    events_path: Path  # path to the journal.jsonl the events endpoint pages over


# The world injects this. Given a submission, build (do not yet run) the execution.
RuntimeFactory = Callable[[WorkflowSubmission], Awaitable[WorkflowExecution]]


@dataclass
class _WorkflowEntry:
    """Mutable in-memory record tracking one workflow across its lifecycle."""

    submission: WorkflowSubmission
    compiled: CompiledWorkflow
    status: str = "queued"  # queued | running | complete | error | cancelled
    result: Any = None
    error: str | None = None
    execution: WorkflowExecution | None = None
    events_path: Path | None = None
    lint_warnings: list[str] = field(default_factory=list)
    # True only for an entry rehydrated after a restart whose journal had no
    # workflow_result (crashed mid-run). Such an entry reports status="error"
    # but an identical resubmission RE-ENQUEUES it instead of returning that
    # error (cheap journal replay). Cleared once a fresh entry replaces it.
    interrupted: bool = False


class WorkflowService:
    """FIFO, one-at-a-time workflow HTTP service.

    Parameters
    ----------
    token:
        Bearer token required on every endpoint except ``/healthz``.
    host / port:
        Bind address. The advertised, agent-VM-reachable URL uses the stable
        ``runtime.plato.internal`` hostname (written into every agent VM's
        ``/etc/hosts``), see :attr:`public_url`.
    runtime_factory:
        Optional injected coroutine that builds a :class:`WorkflowExecution` for
        a submission. When omitted, the service builds executions itself from
        ``backend`` + ``journal_dir`` (component wiring, see module docstring).
    backend / journal_dir:
        Required for component wiring (i.e. when ``runtime_factory`` is None).
    cost_source:
        Optional absolute-session-spend source. When set, each workflow's budget
        baseline is captured at start (delta accounting) and a
        :class:`BudgetRefresher` keeps the budget current while it runs.
    default_budget_usd:
        Ceiling applied to submissions that do not carry their own ``budget_usd``.
    max_concurrent_envs / max_total_calls:
        Per-workflow runtime limits (component wiring only).
    schema_retries:
        Accepted for config parity; structured-output retry wiring lives in the
        agent backend, so the service does not consume it.
    checkpoint_requested:
        Optional non-blocking durability signal the owning world wires to its
        checkpoint machinery. Called with a label when a workflow reaches a
        terminal status, and passed through to each runtime so phase boundaries
        and merged call results also request prompt journal checkpoints.
    """

    def __init__(
        self,
        *,
        token: str,
        host: str = "0.0.0.0",
        port: int = 8722,
        runtime_factory: RuntimeFactory | None = None,
        backend: AgentBackend | None = None,
        cost_source: CostSource | None = None,
        journal_dir: Path | str | None = None,
        default_budget_usd: float | None = None,
        max_concurrent_envs: int = 30,
        max_total_calls: int = 1000,
        schema_retries: int = 2,
        checkpoint_requested: Callable[[str], None] | None = None,
    ) -> None:
        if runtime_factory is None and (backend is None or journal_dir is None):
            raise ValueError("WorkflowService requires either runtime_factory or backend + journal_dir")
        self._runtime_factory = runtime_factory if runtime_factory is not None else self._default_runtime_factory
        self._backend = backend
        self._cost_source = cost_source
        self._journal_dir = Path(journal_dir) if journal_dir is not None else None
        self._default_budget_usd = default_budget_usd
        self._max_concurrent_envs = max_concurrent_envs
        self._max_total_calls = max_total_calls
        self._schema_retries = schema_retries
        self._checkpoint_requested = checkpoint_requested
        self.token = token
        self.host = host
        self.port = port

        self._workflows: dict[str, _WorkflowEntry] = {}
        self._queue: asyncio.Queue[str] = asyncio.Queue()
        self._running_id: str | None = None
        self._executor_task: asyncio.Task[None] | None = None
        self._rehydrated = False

        self._runner: web.AppRunner | None = None
        self._app: web.Application | None = None

    async def _default_runtime_factory(self, submission: WorkflowSubmission) -> WorkflowExecution:
        """Component wiring: fresh journal + budget + runtime per submission."""
        assert self._backend is not None and self._journal_dir is not None  # guarded in __init__
        journal = Journal(self._journal_dir, submission.workflow_id)
        replayable = journal.load()
        if replayable:
            logger.info("workflow %s: %d replayable journal record(s)", submission.workflow_id, replayable)

        baseline = 0.0
        if self._cost_source is not None:
            try:
                baseline = await self._cost_source.refresh()
            except Exception:
                logger.warning(
                    "workflow %s: budget baseline refresh failed; starting at 0.0",
                    submission.workflow_id,
                    exc_info=True,
                )
        total = submission.budget_usd if submission.budget_usd is not None else self._default_budget_usd
        budget = Budget(total, baseline_usd=baseline)

        runtime = WorkflowRuntime(
            backend=self._backend,
            journal=journal,
            budget=budget,
            args=submission.args,
            max_concurrent_envs=self._max_concurrent_envs,
            max_total_calls=self._max_total_calls,
            cancel_event=submission.cancel_event,
            checkpoint_requested=self._checkpoint_requested,
        )
        return WorkflowExecution(runtime=runtime, journal=journal, budget=budget, events_path=journal.path)

    # ------------------------------------------------------------------ lifecycle

    @property
    def public_url(self) -> str:
        """Agent-VM-reachable base URL for this service."""
        return f"http://runtime.plato.internal:{self.port}"

    @property
    def endpoint_info(self) -> dict[str, str]:
        """Payload for the ``.workflow-endpoint.json`` discovery file."""
        return {"url": self.public_url, "token": self.token}

    def write_endpoint_file(self, path: str | Path) -> None:
        """Write the endpoint discovery file (url + token) to ``path``."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.endpoint_info))

    def make_app(self) -> web.Application:
        """Build the aiohttp application (used by both :meth:`start` and unit tests).

        The FIFO executor is tied to the app's startup/cleanup signals so an
        in-process aiohttp ``TestClient`` gets a fully functional executor too.
        """
        app = web.Application(middlewares=[self._auth_middleware])
        app.router.add_get("/healthz", self._handle_healthz)
        app.router.add_post("/workflows", self._handle_submit)
        app.router.add_get("/workflows/{workflow_id}", self._handle_status)
        app.router.add_get("/workflows/{workflow_id}/result", self._handle_result)
        app.router.add_get("/workflows/{workflow_id}/events", self._handle_events)
        app.router.add_post("/workflows/{workflow_id}/cancel", self._handle_cancel)
        app.on_startup.append(self._on_startup)
        app.on_cleanup.append(self._on_cleanup)
        self._app = app
        return app

    async def start(self) -> None:
        """Bind and serve the app on ``host:port``."""
        app = self.make_app()
        # access_log=None: orchestrator --watch polling emits a request every
        # ~2s; per-request access lines flood serve-mode session logs with zero
        # diagnostic value (errors still log through the normal channels).
        self._runner = web.AppRunner(app, access_log=None)
        await self._runner.setup()
        site = web.TCPSite(self._runner, self.host, self.port)
        await site.start()
        logger.info("workflow service listening on %s:%s (public %s)", self.host, self.port, self.public_url)

    async def stop(self) -> None:
        """Stop serving and cancel any in-flight workflow."""
        if self._runner is not None:
            await self._runner.cleanup()  # triggers on_cleanup -> executor shutdown
            self._runner = None

    def active_count(self) -> int:
        """Number of workflows currently queued or running (serve-loop idle signal)."""
        return sum(1 for entry in self._workflows.values() if entry.status not in _TERMINAL)

    def dirty_journals(self) -> list[Journal]:
        """Journals with records appended since their last checkpoint.

        The serve-mode world sweeps this to decide when the journal workspace
        needs a checkpoint — and which journals to ``mark_checkpointed()``
        afterwards. Covers running AND terminal workflows (a completed
        workflow's journal stays dirty until it has been checkpointed once).
        """
        journals: list[Journal] = []
        for entry in self._workflows.values():
            execution = entry.execution
            if execution is not None and execution.journal.dirty:
                journals.append(execution.journal)
        return journals

    async def _on_startup(self, app: web.Application) -> None:
        # Rehydrate persisted submissions BEFORE serving requests (this hook runs
        # during AppRunner.setup(), i.e. inside start(), before the socket accepts
        # traffic) so a relaunched service reports prior workflows' terminal
        # outcomes and can re-enqueue crash-interrupted ones on resubmission.
        self._rehydrate()
        if self._executor_task is None:
            self._executor_task = asyncio.create_task(self._executor_loop())

    async def _on_cleanup(self, app: web.Application) -> None:
        # Signal every workflow to cancel, then tear down the executor.
        for entry in self._workflows.values():
            entry.submission.cancel_event.set()
        if self._executor_task is not None:
            self._executor_task.cancel()
            try:
                await self._executor_task
            except asyncio.CancelledError:
                pass
            self._executor_task = None

    # ------------------------------------------------------------------- executor

    async def _executor_loop(self) -> None:
        while True:
            workflow_id = await self._queue.get()
            try:
                await self._run_one(workflow_id)
            except asyncio.CancelledError:
                raise
            except Exception:  # defensive: a run must never kill the executor
                logger.exception("workflow executor failed for %s", workflow_id)
            finally:
                self._queue.task_done()

    async def _run_one(self, workflow_id: str) -> None:
        entry = self._workflows.get(workflow_id)
        if entry is None:
            return
        if entry.submission.cancel_event.is_set() or entry.status in _TERMINAL:
            if entry.status not in _TERMINAL:
                entry.status = "cancelled"
            return

        entry.status = "running"
        self._running_id = workflow_id
        refresher: BudgetRefresher | None = None
        try:
            execution = await self._runtime_factory(entry.submission)
            entry.execution = execution
            entry.events_path = execution.events_path
            if self._cost_source is not None:
                refresher = BudgetRefresher(execution.budget, self._cost_source)
                await refresher.start()
                # Forced refresh after every completed agent call so the next
                # dispatch's budget.check() never runs against poll-stale spend.
                execution.runtime.on_call_complete = refresher.refresh_now
            # Same trace shape as script mode: every submitted workflow is one
            # workflow.run node so phases/calls nest under it in the viewer.
            with tracer.start_as_current_span("workflow.run") as span:
                span.set_attribute("plato.workflow.id", workflow_id)
                span.set_attribute("plato.workflow.mode", "serve")
                result = await execution.runtime.run(entry.compiled)
            entry.result = result
            entry.status = "cancelled" if entry.submission.cancel_event.is_set() else "complete"
        except WorkflowCancelledError:
            entry.status = "cancelled"
        except asyncio.CancelledError:
            entry.status = "cancelled"
            raise
        except Exception as exc:
            entry.status = "error"
            entry.error = f"{type(exc).__name__}: {exc}"
            logger.exception("workflow %s failed", workflow_id)
        finally:
            if refresher is not None:
                await refresher.stop()
            self._running_id = None
            if entry.status in _TERMINAL:
                self._notify_checkpoint(f"workflow_{entry.status}")

    # --------------------------------------------------------- persistence / rehydrate

    def _write_submission_file(self, submission: WorkflowSubmission) -> None:
        """Persist a submission so a post-crash restart can rehydrate it.

        Atomic (write tmp + ``os.replace``). Best-effort: a write failure only
        costs crash-resume of THIS submission, so it logs and returns rather than
        failing an otherwise-valid POST. No-op under runtime-factory injection
        (no ``journal_dir``); ``args`` is always JSON there in component wiring
        (it arrived as request JSON)."""
        if self._journal_dir is None:
            return
        sub_dir = self._journal_dir / submission.workflow_id
        payload = {
            "version": _SUBMISSION_VERSION,
            "workflow_id": submission.workflow_id,
            "script": submission.script,
            "args": submission.args,
            "name": submission.name,
            "budget_usd": submission.budget_usd,
            "submitted": True,
        }
        try:
            sub_dir.mkdir(parents=True, exist_ok=True)
            tmp = sub_dir / "submission.json.tmp"
            tmp.write_text(json.dumps(payload), encoding="utf-8")
            os.replace(tmp, sub_dir / "submission.json")
        except (OSError, TypeError, ValueError):
            logger.warning(
                "failed to persist submission.json for %s; crash-resume unavailable for it",
                submission.workflow_id,
                exc_info=True,
            )

    @staticmethod
    def _read_terminal_result(events_path: Path) -> dict[str, Any] | None:
        """Return the journal's ``workflow_result`` record dict, or None.

        None means the workflow never wrote a terminal record — it crashed
        mid-run. A truncated final line (an interrupted, un-fsynced append) is
        skipped, so a half-written ``workflow_result`` correctly reads as absent.
        """
        if not events_path.exists():
            return None
        terminal: dict[str, Any] | None = None
        with open(events_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(record, dict) and record.get("type") == "workflow_result":
                    terminal = record
        return terminal

    def _rehydrate(self) -> None:
        """Rebuild in-memory entries from persisted ``submission.json`` files.

        Runs once, before the service accepts traffic. For each
        ``journal_dir/<id>/submission.json`` with no live entry: compile the
        stored script (its fingerprint must match for the 409/idempotency logic),
        then set the entry's terminal status from the journal's
        ``workflow_result`` record. A journal with no ``workflow_result`` crashed
        mid-run: the entry is marked ``interrupted`` (status="error") so an
        identical resubmission re-enqueues via the normal path.
        """
        if self._rehydrated:
            return
        self._rehydrated = True
        if self._journal_dir is None or not self._journal_dir.exists():
            return

        for sub_dir in sorted(self._journal_dir.iterdir()):
            submission_path = sub_dir / "submission.json"
            if not sub_dir.is_dir() or not submission_path.exists():
                continue
            try:
                data = json.loads(submission_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                logger.warning("rehydrate: unreadable submission file %s", submission_path, exc_info=True)
                continue
            if not isinstance(data, dict) or data.get("version") != _SUBMISSION_VERSION:
                logger.warning(
                    "rehydrate: skipping unsupported submission file %s (version=%r)",
                    submission_path,
                    data.get("version") if isinstance(data, dict) else None,
                )
                continue

            workflow_id = data.get("workflow_id") or sub_dir.name
            if workflow_id in self._workflows:
                continue  # a live entry already owns this id
            script = data.get("script")
            if not isinstance(script, str):
                logger.warning("rehydrate: submission %s missing 'script'", submission_path)
                continue
            try:
                compiled = compile_workflow_script(script)
            except Exception:
                logger.warning(
                    "rehydrate: stored script for %s no longer compiles; skipping",
                    workflow_id,
                    exc_info=True,
                )
                continue

            budget_usd = data.get("budget_usd")
            name = data.get("name")
            submission = WorkflowSubmission(
                workflow_id=workflow_id,
                script=script,
                args=data.get("args"),
                name=name if isinstance(name, str) else None,
                budget_usd=float(budget_usd) if isinstance(budget_usd, (int, float)) else None,
                cancel_event=asyncio.Event(),
            )
            entry = _WorkflowEntry(
                submission=submission,
                compiled=compiled,
                lint_warnings=list(compiled.lint_warnings),
            )
            # The events endpoint pages over the journal on disk (same layout the
            # default runtime factory uses), so rehydrated entries stay queryable.
            journal_path = sub_dir / "journal.jsonl"
            entry.events_path = journal_path

            terminal = self._read_terminal_result(journal_path)
            if terminal is None:
                entry.status = "error"
                entry.error = _INTERRUPTED_ERROR
                entry.interrupted = True
            else:
                entry.status = _JOURNAL_STATUS_TO_SERVICE.get(terminal.get("status"), "error")
                if entry.status == "complete":
                    payload = terminal.get("payload")
                    entry.result = payload.get("result") if isinstance(payload, dict) else None
                elif entry.status == "error":
                    entry.error = terminal.get("error") or "workflow failed"
            self._workflows[workflow_id] = entry
            logger.info(
                "rehydrated workflow %s as %s%s",
                workflow_id,
                entry.status,
                " (interrupted)" if entry.interrupted else "",
            )

    def _notify_checkpoint(self, label: str) -> None:
        """Best-effort durability signal to the owning world (never raises)."""
        if self._checkpoint_requested is None:
            return
        try:
            self._checkpoint_requested(label)
        except Exception:
            logger.warning("checkpoint request hook failed (label=%s)", label, exc_info=True)

    # --------------------------------------------------------------- auth / util

    @web.middleware
    async def _auth_middleware(self, request: web.Request, handler: Callable) -> web.StreamResponse:
        if request.path == "/healthz":
            return await handler(request)
        if not self._check_bearer(request.headers.get("Authorization", "")):
            return web.json_response({"error": "unauthorized"}, status=401)
        return await handler(request)

    def _check_bearer(self, header: str) -> bool:
        prefix = "Bearer "
        if not header.startswith(prefix):
            return False
        # Compare as bytes: compare_digest handles unequal lengths fine but
        # raises TypeError on non-ASCII str inputs — a crafted header must be
        # a 401, never a 500.
        return hmac.compare_digest(header[len(prefix) :].encode("utf-8"), self.token.encode("utf-8"))

    def _stats_dict(self, execution: WorkflowExecution | None) -> dict[str, Any]:
        if execution is None:
            return {"calls_total": 0, "calls_cached": 0, "calls_failed": 0, "phases": []}
        stats = execution.runtime.stats
        return {
            "calls_total": stats.calls_total,
            "calls_cached": stats.calls_cached,
            "calls_failed": stats.calls_failed,
            "phases": list(stats.phases),
        }

    def _spent_usd(self, execution: WorkflowExecution | None) -> float:
        if execution is None:
            return 0.0
        try:
            return float(execution.budget.spent())
        except Exception:
            return 0.0

    @staticmethod
    def _current_phase(stats: dict[str, Any]) -> str | None:
        phases = stats.get("phases") or []
        return phases[-1] if phases else None

    @staticmethod
    def _read_events(events_path: Path | None, after_seq: int) -> tuple[list[dict[str, Any]], int]:
        """Page journal records with ``seq > after_seq``; tolerate a truncated final line."""
        events: list[dict[str, Any]] = []
        max_seq = after_seq
        if events_path is None or not events_path.exists():
            return events, max_seq
        with open(events_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue  # truncated/partial trailing line — skip it
                seq = record.get("seq")
                if not isinstance(seq, int):
                    continue
                if seq > max_seq:
                    max_seq = seq
                if seq > after_seq:
                    events.append(record)
        events.sort(key=lambda r: r["seq"])
        return events, max_seq

    # ---------------------------------------------------------------- handlers

    async def _handle_healthz(self, request: web.Request) -> web.StreamResponse:
        return web.json_response({"status": "ok"})

    async def _handle_submit(self, request: web.Request) -> web.StreamResponse:
        try:
            body = await request.json()
        except (json.JSONDecodeError, ValueError):
            return web.json_response({"error": "request body must be valid JSON"}, status=400)
        if not isinstance(body, dict):
            return web.json_response({"error": "request body must be a JSON object"}, status=400)

        script = body.get("script")
        if not isinstance(script, str) or not script.strip():
            return web.json_response({"error": "'script' is required and must be a non-empty string"}, status=400)

        args = body.get("args")
        name = body.get("name")
        budget_usd = body.get("budget_usd")
        if budget_usd is not None:
            try:
                budget_usd = float(budget_usd)
            except (TypeError, ValueError):
                return web.json_response({"error": "'budget_usd' must be a number"}, status=400)

        # Compile immediately for fast-fail feedback (line numbers already remapped
        # to the user's coordinates by compile_workflow_script).
        try:
            compiled = compile_workflow_script(script)
        except WorkflowScriptError as exc:
            payload: dict[str, Any] = {"error": str(exc)}
            if exc.lineno is not None:
                payload["lineno"] = exc.lineno
            if exc.excerpt is not None:
                payload["excerpt"] = exc.excerpt
            return web.json_response(payload, status=422)
        except Exception as exc:  # any other compile-time failure
            return web.json_response({"error": str(exc)}, status=422)

        workflow_id = body.get("workflow_id") or default_workflow_id(script, args)

        existing = self._workflows.get(workflow_id)
        if existing is not None:
            if existing.status not in _TERMINAL:
                return web.json_response(
                    {"error": "workflow already running", "workflow_id": workflow_id, "status": existing.status},
                    status=409,
                )
            # Reusing an explicit workflow_id with a different script or args is a
            # conflict, not a cache hit — silently serving the stored result would
            # hide that the new submission never ran.
            same_script = existing.compiled.fingerprint == compiled.fingerprint
            same_args = _canonical_json(existing.submission.args) == _canonical_json(args)
            if not (same_script and same_args):
                return web.json_response(
                    {
                        "error": "workflow_id already used with different script/args; "
                        "pick a new workflow_id or omit it (content-hashed default)",
                        "workflow_id": workflow_id,
                        "status": existing.status,
                    },
                    status=409,
                )
            # Identical content. A crash-interrupted rehydrated entry (no
            # workflow_result on disk) is NOT settled: re-enqueue it below —
            # replacing the entry — so the journal-replay re-run happens through
            # the exact same FIFO/journal/runtime-factory path as a fresh
            # submission. Any other terminal status is a true idempotent hit.
            if not existing.interrupted:
                return web.json_response({"workflow_id": workflow_id, "status": existing.status})

        submission = WorkflowSubmission(
            workflow_id=workflow_id,
            script=script,
            args=args,
            name=name if isinstance(name, str) else None,
            budget_usd=budget_usd,
            cancel_event=asyncio.Event(),
        )
        entry = _WorkflowEntry(submission=submission, compiled=compiled, lint_warnings=list(compiled.lint_warnings))
        # Persist BEFORE enqueue so a crash between accept and run can still be
        # rehydrated (and re-enqueued on identical resubmission).
        self._write_submission_file(submission)
        self._workflows[workflow_id] = entry
        await self._queue.put(workflow_id)
        return web.json_response(
            {"workflow_id": workflow_id, "status": "queued", "lint_warnings": entry.lint_warnings},
            status=201,
        )

    async def _handle_status(self, request: web.Request) -> web.StreamResponse:
        entry = self._workflows.get(request.match_info["workflow_id"])
        if entry is None:
            return web.json_response({"error": "workflow not found"}, status=404)
        stats = self._stats_dict(entry.execution)
        payload: dict[str, Any] = {
            "workflow_id": entry.submission.workflow_id,
            "status": entry.status,
            "phase": self._current_phase(stats),
            "stats": stats,
            "spent_usd": self._spent_usd(entry.execution),
        }
        if entry.status == "complete":
            payload["result"] = entry.result
        if entry.status == "error":
            payload["error"] = entry.error
        return web.json_response(payload)

    async def _handle_result(self, request: web.Request) -> web.StreamResponse:
        entry = self._workflows.get(request.match_info["workflow_id"])
        if entry is None:
            return web.json_response({"error": "workflow not found"}, status=404)
        if entry.status in ("queued", "running"):
            return web.json_response({"status": entry.status}, status=202)
        payload: dict[str, Any] = {"status": entry.status, "result": entry.result}
        if entry.status == "error":
            payload["error"] = entry.error
        return web.json_response(payload)

    async def _handle_events(self, request: web.Request) -> web.StreamResponse:
        entry = self._workflows.get(request.match_info["workflow_id"])
        if entry is None:
            return web.json_response({"error": "workflow not found"}, status=404)
        try:
            after_seq = int(request.query.get("after_seq", "-1"))
        except ValueError:
            return web.json_response({"error": "'after_seq' must be an integer"}, status=400)
        events, next_seq = self._read_events(entry.events_path, after_seq)
        return web.json_response({"events": events, "next_seq": next_seq})

    async def _handle_cancel(self, request: web.Request) -> web.StreamResponse:
        entry = self._workflows.get(request.match_info["workflow_id"])
        if entry is None:
            return web.json_response({"error": "workflow not found"}, status=404)
        entry.submission.cancel_event.set()
        if entry.status == "queued":
            entry.status = "cancelled"
        return web.json_response({"workflow_id": entry.submission.workflow_id, "status": entry.status})
