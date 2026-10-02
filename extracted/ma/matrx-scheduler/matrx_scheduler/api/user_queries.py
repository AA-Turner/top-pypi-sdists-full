"""
User-JWT scoped matrx-orm queries for the scheduler API routes.

CRITICAL DISTINCTION:

- ``matrx_scheduler.queries`` uses the host-injected SERVICE-ROLE client
  for the scanner. Reads cross-user, writes lease state.
- This module runs every query/write through matrx-orm's ``rls_session``,
  RLS-scoped to the CALLER's own claims -- rows the caller doesn't own are
  not visible. See "RLS scoping" below for exactly how that's derived.

Functions here are thin matrx-orm wrappers -- no domain logic, no emitter
calls, no AppContext mutations. The router layer handles that. Errors
propagate as matrx-orm / Postgres exceptions; routers map them to HTTP
status codes (``_classify_supabase_error`` pattern-matches the stringified
exception, which still works for a DatabaseError/RLS-denial message).

Package boundary: matrx-scheduler is NOT a declared dependent of matrx-orm
(``pyproject.toml`` only pulls it in under the optional ``host``/``api``
extras) — this module never imports ``matrx_orm`` itself. ``rls_session`` /
``call_function`` / the target database name are injected by the host via
``matrx_scheduler.configure(rls_session=..., call_function=..., database=...)``
(see ``_ext.py``) and read back here with ``get_ext(...)``, which raises
loudly if the host hasn't wired them — the same "capability-within,
injection-without" seam matrx-ai's ``configure()`` uses for its own
provider/DB integrations. DB *models* (``SchTask`` etc.) are a separate,
declarative injection seam (``get_db_model``, wired by the generated
``aidream/_generated/package_db_wiring.py`` from this package's
``db_requirements.py``).

RLS scoping (why signatures are unchanged):
    Every function here still takes ``sb: Any`` — the per-request Supabase
    client built by ``api.per_request.user_client_dep`` — because
    ``api.router_scheduler`` (which this module does not own / is not part
    of this conversion) passes that same ``sb`` positionally into every
    call. Changing the signature to take a JWT string directly would break
    that caller. Instead, ``_claims_from_client`` reads the bearer token
    back OUT of the client's own ``options.headers["Authorization"]`` (the
    exact header ``per_request.py`` bakes in for PostgREST RLS) and decodes
    it into the claims dict ``rls_session`` expects — mirroring
    ``aidream.services.scheduling.admin._claims_from_jwt`` exactly. The
    token was already verified by ``AuthMiddleware`` upstream of
    ``user_client_dep`` (every router here also depends on ``context_dep``
    and checks ``ctx.is_authenticated``), so this is a re-read of already
    -verified claims, not a second trust decision. Every read/write below
    then runs inside ``rls_session(claims, role=claims["role"])`` — the
    IDENTICAL Postgres RLS policies gate it that PostgREST would have
    applied on the old per-request client; no ownership predicate was
    dropped, narrowed, or widened by this conversion.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

from .._ext import get_db_model, get_ext, get_optional_ext

log = logging.getLogger("matrx_scheduler.api.user_queries")


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _database() -> str:
    return get_ext("database")


def _rls_session() -> Any:
    return get_ext("rls_session")


def _call_function() -> Any:
    return get_ext("call_function")


async def _retry_read(factory: Any, *, label: str) -> Any:
    """Retry one whole RLS-scoped read transaction when the host permits it.

    ``rls_session`` is a transaction. The ORM can retry a standalone SELECT,
    but deliberately cannot retry after a command timeout *inside* that
    transaction because it is poisoned. The host injects its opt-in resilience
    primitive so this package stays independent of matrx-orm while a pure read
    can reopen a fresh RLS transaction once.
    """
    retry = get_optional_ext("retry_on_transient")
    if retry is None:
        return await factory()
    return await retry(factory, attempts=2, label=label)


def _jwt_from_client(sb: Any) -> str:
    """Pull the bearer token back out of the per-request client's own
    Authorization header (baked in by ``per_request.py`` for PostgREST
    RLS)."""
    headers = getattr(getattr(sb, "options", None), "headers", None) or {}
    auth = headers.get("Authorization") or headers.get("authorization") or ""
    if not auth.lower().startswith("bearer "):
        raise RuntimeError(
            "per-request Supabase client carries no bearer Authorization header "
            "(expected api.per_request.user_client_dep's output)"
        )
    return auth.split(" ", 1)[1]


def _claims_from_client(sb: Any) -> dict[str, Any]:
    """Decode the caller's already-verified bearer token into the claims
    dict ``rls_session`` expects. Mirrors
    ``aidream.services.scheduling.admin._claims_from_jwt``."""
    import jwt as pyjwt

    token = _jwt_from_client(sb)
    decoded = pyjwt.decode(
        token, options={"verify_signature": False, "verify_exp": False, "verify_aud": False}
    )
    sub = decoded.get("sub")
    if not sub:
        raise RuntimeError("bearer token has no sub claim")
    role = decoded.get("role")
    if role not in ("authenticated", "anon"):
        role = "authenticated"
    claims = dict(decoded)
    claims["sub"] = sub
    claims["role"] = role
    return claims


def _row(data: dict[str, Any]) -> dict[str, Any]:
    """Match PostgREST's JSON-over-the-wire shape: UUID -> str. matrx-orm
    returns native asyncpg types (``uuid.UUID``); every Pydantic response
    model in ``api.schemas`` declares id/user_id/task_id/... as ``str``,
    exactly what PostgREST always produced. ``datetime`` passes through
    unchanged (response fields are typed ``datetime``)."""
    return {k: (str(v) if isinstance(v, uuid.UUID) else v) for k, v in data.items()}


# ── Tasks ────────────────────────────────────────────────────────────────


async def list_tasks(
    sb: Any,
    *,
    kind: str | None = None,
    enabled: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """
    List the caller's tasks (RLS-scoped). Newest first.

    Soft-deleted rows (``deleted_at IS NOT NULL``) are excluded; the user
    pressed "Delete" and expects them gone. Paused rows (enabled=false but
    deleted_at IS NULL) remain visible -- pause is reversible UI state.
    """
    SchTask = get_db_model("SchTask")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        q = SchTask.filter(deleted_at__isnull=True)
        if kind is not None:
            q = q.filter(kind=kind)
        if enabled is not None:
            q = q.filter(enabled=enabled)
        rows = await q.order_by("-created_at").limit(limit).offset(offset).values()
    return [_row(r) for r in rows]


async def count_tasks(
    sb: Any,
    *,
    kind: str | None = None,
    enabled: bool | None = None,
) -> int:
    """Count of the caller's tasks (RLS-scoped)."""
    SchTask = get_db_model("SchTask")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        q = SchTask.filter(deleted_at__isnull=True)
        if kind is not None:
            q = q.filter(kind=kind)
        if enabled is not None:
            q = q.filter(enabled=enabled)
        return await q.count()


async def get_task(sb: Any, task_id: str) -> dict[str, Any] | None:
    """
    Fetch a single task by id. Returns None for non-existent OR
    soft-deleted rows so callers get a clean 404 either way.
    """
    SchTask = get_db_model("SchTask")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        rows = await SchTask.filter(id=task_id, deleted_at__isnull=True).limit(1).values()
    return _row(rows[0]) if rows else None


async def insert_task(
    sb: Any,
    *,
    user_id: str,
    kind: str,
    title: str,
    description: str | None,
    queue: str,
    surfaces: list[str],
    enabled: bool,
    expires_at: str | None,
    tags: list[str],
    taxonomy_node_id: str | None,
    organization_id: str,
) -> dict[str, Any]:
    """
    Insert a new sch_task row. ``organization_id`` is REQUIRED: the task belongs
    to the organization of the request that created it, never a default. The caller's user_id is stamped so RLS
    matches; the user_id is also validated server-side by RLS against
    auth.uid() -- a misbehaving FE cannot insert on behalf of another
    user even if it tries.
    """
    SchTask = get_db_model("SchTask")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    payload: dict[str, Any] = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "organization_id": organization_id,
        "kind": kind,
        "title": title,
        "description": description,
        "queue": queue,
        "surfaces": surfaces,
        "enabled": enabled,
        "tags": tags,
    }
    if taxonomy_node_id is not None:
        payload["taxonomy_node_id"] = taxonomy_node_id
    if expires_at is not None:
        payload["expires_at"] = expires_at
    async with rls_session(claims, role=claims["role"], database=_database()):
        instance = await SchTask.create(**payload)
    return _row(instance.to_dict())


async def update_task(sb: Any, task_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
    """
    Apply a partial update to sch_task. RLS gates ownership. Returns the
    updated row or None if no rows matched (caller doesn't own it, it
    doesn't exist, or it has been soft-deleted).

    The ``deleted_at IS NULL`` filter means PATCH against a soft-deleted
    row returns None (router -> 404) instead of silently reviving a
    deleted task. To intentionally restore a deleted task, use a
    dedicated restore endpoint (not yet exposed).
    """
    if not patch:
        return await get_task(sb, task_id)
    SchTask = get_db_model("SchTask")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        result = await SchTask.update_where(
            {"id": task_id, "deleted_at__isnull": True}, **patch
        )
    return _row(result.updated_rows[0]) if result.updated_rows else None


async def soft_delete_task(sb: Any, task_id: str) -> bool:
    """
    Soft-delete a task: stamp deleted_at = now() and flip enabled = false.

    There is no hard delete of a task anywhere -- delete means archive
    (Arman, 2026-09-27), and sch_run.task_id FK would orphan run history.
    ``router_scheduler.create_task``'s rollback of a half-created task uses
    this same path. The deleted_at column lets the read-path hide the
    row while preserving full run history for audit / debugging.

    Belt-and-suspenders: flipping enabled = false too means the scanner
    (which filters ``enabled = TRUE``) skips the row even in the edge
    case where some future code path forgets to filter on deleted_at.
    """
    SchTask = get_db_model("SchTask")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        result = await SchTask.update_where(
            {"id": task_id, "deleted_at__isnull": True},
            enabled=False,
            deleted_at=_now_iso(),
        )
    return result.rows_affected > 0


async def load_task_fingerprints(sb: Any) -> list[dict[str, Any]]:
    """Every live schedule the caller owns, each with its duplicate fingerprint.

    Three bounded reads inside ONE rls_session — tasks, then the agent_task and
    trigger children of exactly those tasks — instead of N+1 per-task lookups.
    A schedule's identity spans all three tables (``scheduler.duplicate_guard``),
    so none of them can be skipped.

    RLS-scoped, so this can only ever see the caller's own schedules. That is
    also the correct semantic boundary: duplicates are grouped WITHIN one user,
    never across users.
    """
    from matrx_scheduler.duplicate_guard import can_fire, fingerprint_from_rows

    SchTask = get_db_model("SchTask")
    SchAgentTask = get_db_model("SchAgentTask")
    SchTrigger = get_db_model("SchTrigger")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async def _read_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
        async with rls_session(claims, role=claims["role"], database=_database()):
            # Duplicate identity needs only these fields. Keeping this projection
            # narrow avoids pulling arbitrary metadata and descriptions for every
            # schedule into an informational duplicate-check request.
            tasks = await SchTask.filter(deleted_at__isnull=True).values(
                "id", "user_id", "title", "enabled", "created_at", "kind", "queue"
            )
            task_ids = [str(t["id"]) for t in tasks]
            if not task_ids:
                return tasks, [], []
            agent_rows = await SchAgentTask.filter(id__in=task_ids).values(
                "id", "agent_id", "mandate_key", "prompt", "variables"
            )
            trigger_rows = await SchTrigger.filter(task_id__in=task_ids, deleted_at__isnull=True).values(
                "task_id", "type", "config", "enabled"
            )
            return tasks, agent_rows, trigger_rows

    tasks, agent_rows, trigger_rows = await _retry_read(
        _read_rows, label="scheduler.load_task_fingerprints"
    )
    if not tasks:
        return []

    # sch_agent_task.id IS the task id (1:1 FK-as-PK), not a separate column.
    agents = {str(a["id"]): _row(a) for a in agent_rows}
    triggers: dict[str, list[dict[str, Any]]] = {}
    for tr in trigger_rows:
        triggers.setdefault(str(tr["task_id"]), []).append(_row(tr))

    out: list[dict[str, Any]] = []
    for raw in tasks:
        task = _row(raw)
        tid = str(task["id"])
        out.append(
            {
                "id": tid,
                "user_id": str(task.get("user_id") or ""),
                "title": task.get("title"),
                "enabled": task.get("enabled"),
                "created_at": task.get("created_at"),
                "fingerprint": fingerprint_from_rows(
                    task, agents.get(tid), triggers.get(tid, [])
                ),
                "can_fire": can_fire(task, triggers.get(tid, [])),
            }
        )
    return out


# ── Agent task ───────────────────────────────────────────────────────────


async def get_agent_task(sb: Any, task_id: str) -> dict[str, Any] | None:
    """Look up the agent_task row attached to the given task id."""
    SchAgentTask = get_db_model("SchAgentTask")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        rows = await SchAgentTask.filter(id=task_id).limit(1).values()
    return _row(rows[0]) if rows else None


async def upsert_agent_task(
    sb: Any,
    *,
    task_id: str,
    organization_id: str,
    agent_id: str | None,
    mandate_key: str | None,
    prompt: str,
    variables: dict[str, Any],
    persistent_conversation_id: str | None,
    auth_mode: str,
    max_runtime_seconds: int,
    max_concurrent: int,
) -> dict[str, Any]:
    """
    Insert or update the sch_agent_task row paired with a task.

    sch_agent_task.id is a FK to sch_task.id (1:1). RLS enforces that
    the caller owns the parent task before allowing the write.

    ``organization_id`` is the parent task's own organization, passed by the
    caller: the row carries it explicitly and nothing in the database chooses
    it (common-docs/projects/no-db-assigned-org/PLAN.md).
    """
    if not organization_id:
        raise ValueError("upsert_agent_task needs the parent task's organization_id")
    SchAgentTask = get_db_model("SchAgentTask")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    payload: dict[str, Any] = {
        "id": task_id,
        "organization_id": organization_id,
        "agent_id": agent_id,
        "mandate_key": mandate_key,
        "prompt": prompt,
        "variables": variables,
        "persistent_conversation_id": persistent_conversation_id,
        "auth_mode": auth_mode,
        "max_runtime_seconds": max_runtime_seconds,
        "max_concurrent": max_concurrent,
    }
    async with rls_session(claims, role=claims["role"], database=_database()):
        instance = await SchAgentTask.upsert(payload, conflict_fields=["id"])
    return _row(instance.to_dict())


# ── Triggers ─────────────────────────────────────────────────────────────


async def list_triggers_for_task(sb: Any, task_id: str) -> list[dict[str, Any]]:
    SchTrigger = get_db_model("SchTrigger")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        rows = await SchTrigger.filter(
            task_id=task_id, deleted_at__isnull=True
        ).order_by("-created_at").values()
    return [_row(r) for r in rows]


async def get_trigger(sb: Any, trigger_id: str) -> dict[str, Any] | None:
    SchTrigger = get_db_model("SchTrigger")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        rows = await SchTrigger.filter(id=trigger_id, deleted_at__isnull=True).limit(1).values()
    return _row(rows[0]) if rows else None


async def insert_trigger(
    sb: Any,
    *,
    user_id: str,
    task_id: str,
    type: str,
    config: dict[str, Any],
    enabled: bool,
    next_due_at: str | None,
    organization_id: str,
) -> dict[str, Any]:
    """Insert a trigger. It is a CHILD of its task: ``organization_id`` is the
    task row's, passed by the caller that read it — never a default."""
    SchTrigger = get_db_model("SchTrigger")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    payload: dict[str, Any] = {
        "id": str(uuid.uuid4()),
        "task_id": task_id,
        "user_id": user_id,
        "organization_id": organization_id,
        "type": type,
        "config": config,
        "enabled": enabled,
    }
    if next_due_at is not None:
        payload["next_due_at"] = next_due_at
    async with rls_session(claims, role=claims["role"], database=_database()):
        instance = await SchTrigger.create(**payload)
    return _row(instance.to_dict())


async def update_trigger(sb: Any, trigger_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
    if not patch:
        return await get_trigger(sb, trigger_id)
    SchTrigger = get_db_model("SchTrigger")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        result = await SchTrigger.update_where(
            {"id": trigger_id, "deleted_at__isnull": True}, **patch
        )
    return _row(result.updated_rows[0]) if result.updated_rows else None


async def delete_trigger(sb: Any, trigger_id: str) -> bool:
    """Canonical SOFT delete (owner ruling 2026-09-20: anything important is a
    soft delete; db-rules section 8).

    ``scheduler.sch_trigger`` carries ``deleted_at`` and this was a hard
    ``delete_where`` until 2026-09-20: a person removing a schedule's clock
    destroyed the row, so nothing could say what the schedule used to do or put
    it back — while ``matrx_graph``'s workflow triggers beside it had been soft
    deleting since 2026-08-10. ``enabled`` is cleared in the SAME write, because
    a row that is merely marked deleted must not be claimable by any scheduler
    path for the instant before every reader is filtered; both halves land
    together or neither does.

    Every read of this table filters ``deleted_at IS NULL`` — the four sites in
    this module and ``_hydrate_active_trigger`` in ``queries.py``, which is the
    one the cron watcher asks. A soft delete whose readers do not filter is a
    row that vanished from the screen and kept firing.
    """
    SchTrigger = get_db_model("SchTrigger")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        result = await SchTrigger.update_where(
            {"id": trigger_id, "deleted_at__isnull": True},
            deleted_at=datetime.now(UTC),
            enabled=False,
        )
    return bool(getattr(result, "updated_rows", None))


# ── Runs (read-only from API) ───────────────────────────────────────────


async def list_runs(
    sb: Any,
    *,
    task_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    SchRun = get_db_model("SchRun")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        q = SchRun.filter()
        if task_id is not None:
            q = q.filter(task_id=task_id)
        if status is not None:
            q = q.filter(status=status)
        rows = await q.order_by("-created_at").limit(limit).offset(offset).values()
    return [_row(r) for r in rows]


async def get_run(sb: Any, run_id: str) -> dict[str, Any] | None:
    SchRun = get_db_model("SchRun")
    rls_session = _rls_session()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        rows = await SchRun.filter(id=run_id).limit(1).values()
    return _row(rows[0]) if rows else None


# ── Run-now RPC ─────────────────────────────────────────────────────────


async def enqueue_manual_run(sb: Any, task_id: str) -> str:
    """
    Call the sch_enqueue_manual_run RPC. The RPC enforces task ownership
    via RLS and stamps user_id from the task row (not from the caller's
    submission), so a misbehaving FE cannot spoof status / output_ref /
    surface fields.

    Returns the new sch_run.id.
    """
    rls_session = _rls_session()
    call_function = _call_function()
    claims = _claims_from_client(sb)
    async with rls_session(claims, role=claims["role"], database=_database()):
        new_run_id = await call_function(
            _database(), "public", "sch_enqueue_manual_run", task_id, mode="scalar"
        )
    if not new_run_id:
        raise RuntimeError("sch_enqueue_manual_run returned no run id")
    return str(new_run_id)
