"""
Host-injection registry for matrx-scheduler.

The package is standalone; the host application (aidream) wires concrete
implementations via `configure(...)` at startup. Inside the package, code
reads back via `get_ext(key)` which raises if the host hasn't configured.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_registry: dict[str, Any] = {}
_configured = False

# Host-injected matrx-orm Model / manager-Base classes, keyed by registry
# name (e.g. "SchTask" -> db.models.scheduler.SchTask). Separate from
# `_registry` / `configure(...)` above: wired declaratively by the generated
# `aidream/_generated/package_db_wiring.py` (see db_requirements.py in this
# package), not part of the host's manual configure() call. Consumers use
# `get_db_model(name)`, never a direct `db.models` import (package boundary).
_db_models: dict[str, Any] = {}
_db_bases: dict[str, Any] = {}


class SchedulerNotConfiguredError(RuntimeError):
    pass


def configure_db(
    *, models: dict[str, Any] | None = None, db_bases: dict[str, Any] | None = None
) -> None:
    """Wire host-generated matrx-orm Model (+ manager Base) classes by name.
    Called by the generated package wiring (`wire_package_db()`), separate
    from the main `configure(...)` call (which requires
    `supabase_client`/`surface` and is not appropriate for the DB-model
    injection seam). `db_bases` is accepted because the manifest's
    schema-rule form (`db_requirements.py`) emits a Base per table
    unconditionally — unused today, kept for a future single-table manager."""
    if models:
        _db_models.update(models)
    if db_bases:
        _db_bases.update(db_bases)


def get_db_model(name: str) -> Any:
    """Look up a host-injected matrx-orm Model class by registry name.
    Raises if the host hasn't wired it (no `wire_package_db()` call, or a
    stale manifest) — never a silent None."""
    try:
        return _db_models[name]
    except KeyError:
        raise SchedulerNotConfiguredError(
            f"matrx-scheduler DB model '{name}' is not registered. "
            "Call matrx_scheduler.configure_db(models=...) (normally via the "
            "generated aidream/_generated/package_db_wiring.py::wire_package_db()) "
            "before accessing DB functionality."
        ) from None


async def report_operational_failure(
    exc: BaseException,
    *,
    operation: str,
    context: dict[str, Any] | None = None,
) -> None:
    """Send a non-run scheduler failure through the host's durable sink."""
    sink = _registry.get("failure_sink")
    if sink is None:
        return
    try:
        await sink(
            {
                "run_id": (context or {}).get("run_id"),
                "status": "operational_failed",
                "error_message": str(exc),
                "error_type": type(exc).__name__,
                "operation": operation,
                "result_metadata": context or {},
            }
        )
    except Exception:
        # Observability can never break scheduler recovery/finalization.
        return


def configure(
    *,
    supabase_client: Any,
    surface: str,
    agent_runner: Any | None = None,
    tool_runner: Any | None = None,
    get_app_context: Any | None = None,
    emitter_factory: Any | None = None,
    user_supabase_factory: Callable[[str], Any] | None = None,
    scan_interval_seconds: float = 5.0,
    lease_seconds: int = 600,
    db_schema: str = "scheduler",
    database: str | None = None,
    rls_session: Callable[..., Any] | None = None,
    call_function: Callable[..., Any] | None = None,
    retry_on_transient: Callable[..., Any] | None = None,
    escalation_sink: Callable[..., Any] | None = None,
    failure_sink: Callable[..., Any] | None = None,
    repeat_guard_thresholds: Callable[..., Any] | None = None,
    continuation_limit: Callable[..., Any] | None = None,
    heartbeat: Callable[..., Any] | None = None,
    transaction: Callable[..., Any] | None = None,
    backlog_task_validator: Callable[..., Any] | None = None,
) -> None:
    """
    Wire host-supplied dependencies. Call once at app startup.

    Args:
        supabase_client: SERVICE-ROLE client (or equivalent privileged
            client) used by the SCANNER to read sch_task across users
            and update lease state. Never used by the user-facing API
            routes -- those build a per-request client from the caller's
            JWT instead. Async-compatible (Python supabase v2 client).
        surface: the string this host identifies as in `sch_task.surfaces`
            (e.g. 'server' for aidream). Used by the scanner's WHERE clause.
        agent_runner: callable that runs an agent (kind='agent' tasks).
            Receives an AgentRunInput and returns an AgentRunResult.
            matrx-ai provides one -- host wires.
        tool_runner: callable that runs a tool (kind='tool' tasks).
            Receives a ToolRunInput and returns an AgentRunResult.
            Optional -- hosts that don't claim kind='tool' tasks (e.g.
            aidream itself, which forwards tool kinds to other surfaces
            via wake hints) leave this unset; tool kinds then finalize
            with a clear "no tool_runner registered" error_message.
        get_app_context: callable returning the current AppContext, used to
            propagate user_id / emitter into the runner.
        emitter_factory: callable that produces a fresh emitter per run.
        user_supabase_factory: callable that takes a user JWT and returns
            a per-request Supabase client whose Authorization header is
            the caller's bearer token (so PostgREST RLS sees auth.uid()
            = caller). Used by the API routes for user-scoped CRUD. If
            not provided, the package falls back to an env-based factory
            keyed on SUPABASE_MATRIX_URL + SUPABASE_MATRIX_PUBLISHABLE_KEY
            (see ``api.per_request.default_user_supabase_factory``).
        heartbeat: async callable the scanner awaits after EVERY tick, so a
            host can record "the platform's scanner is alive" somewhere durable
            (aidream: a ``workflow.worker_heartbeat`` row under its own role).
            Signature ``heartbeat(*, alive: bool, status: dict) -> None``;
            ``alive=False`` is the loop's last act on the way out. Optional —
            unconfigured, the scanner runs exactly as before and the host simply
            has no liveness signal. 🚨 Earned 2026-09-15: the scanner's asyncio
            task stopped inside a healthy API process and ALL scheduled work on
            the platform stopped for 17+ minutes with nothing to look at — the
            only health surface was in-process, so "the scheduler is dead" and
            "you asked an instance that never runs it" returned the same answer.
        scan_interval_seconds: how often the scanner ticks. Default 5s.
        lease_seconds: how long a claim lasts before another surface can
            re-claim. Default 600s. Should be >= max_runtime_seconds for
            most tasks.
        db_schema: Postgres schema holding the sch_* tables. Default
            ``scheduler`` (canonical after the 2026 schema reorg).
        database: the registered matrx-orm database/project name (e.g.
            aidream's ``PRIMARY_DATABASE``) used by the RLS-scoped ORM
            queries in ``api.user_queries``. Package boundary rule: this
            package MUST NOT import ``matrx_orm`` itself (it isn't a
            declared dependency — matrx-scheduler stays installable without
            an ORM), so the host injects the resolved name as a plain
            string, not a live connection.
        rls_session: the host's ``matrx_orm.rls_session`` context-manager
            factory, injected so ``api.user_queries`` never imports
            ``matrx_orm`` directly. Required for the ``/scheduler/*`` HTTP
            routes' user-scoped CRUD; unused by the scanner.
        call_function: the host's ``matrx_orm.call_function`` primitive,
            injected for the same reason — used by
            ``api.user_queries.enqueue_manual_run`` to call the
            ``sch_enqueue_manual_run`` RPC.
        retry_on_transient: the host's ``matrx_orm.retry_on_transient``
            primitive. Read-only RLS transactions use it to retry their whole
            transaction once after a command timeout; the package does not
            import matrx-orm directly.
        escalation_sink: async callable receiving a
            ``repeat_guard.FailureStreak`` when a task has failed
            ``MAX_CONSECUTIVE_FAILURES`` times in a row the same way. The
            package always SCREAMS to the log; this sink is how the host
            hands the give-up to a person on its own surface (aidream raises
            a ``platform.assists`` chip). Optional — without it the guard
            still detects and logs, it just cannot reach anyone.
    """
    global _configured
    _registry["supabase_client"] = supabase_client
    _registry["surface"] = surface
    _registry["agent_runner"] = agent_runner
    _registry["tool_runner"] = tool_runner
    _registry["get_app_context"] = get_app_context
    _registry["emitter_factory"] = emitter_factory
    _registry["user_supabase_factory"] = user_supabase_factory
    _registry["scan_interval_seconds"] = scan_interval_seconds
    _registry["lease_seconds"] = lease_seconds
    _registry["db_schema"] = db_schema
    _registry["database"] = database
    _registry["rls_session"] = rls_session
    _registry["call_function"] = call_function
    _registry["retry_on_transient"] = retry_on_transient
    _registry["escalation_sink"] = escalation_sink
    _registry["failure_sink"] = failure_sink
    _registry["repeat_guard_thresholds"] = repeat_guard_thresholds
    _registry["heartbeat"] = heartbeat
    # The atomic backlog primitive deliberately receives its transaction and
    # registered-tool validation from the host.  matrx-scheduler remains
    # installable without matrx-orm or aidream's tool registry.
    _registry["transaction"] = transaction
    _registry["backlog_task_validator"] = backlog_task_validator
    # async () -> int: continuations one scheduled fire may get after its worker
    # goes away (``continuation.py``). aidream reads the knob
    # scheduler.continuation.max_continuations_per_fire; without a resolver the
    # package mirror MAX_CONTINUATIONS_PER_FIRE applies.
    _registry["continuation_limit"] = continuation_limit
    _configured = True


def is_configured() -> bool:
    return _configured


def has_ext(key: str) -> bool:
    """True if `key` has been configured (and is not None)."""
    return _registry.get(key) is not None


def get_ext(key: str, *, required: bool = True) -> Any:
    if key in _registry:
        return _registry[key]
    if required:
        raise SchedulerNotConfiguredError(
            f"matrx-scheduler dependency '{key}' is not configured. "
            "Call matrx_scheduler.configure(...) at host startup."
        )
    return None


def get_optional_ext(key: str) -> Any:
    """Read an ext that the host may legitimately leave unset. Never raises."""
    return _registry.get(key)
