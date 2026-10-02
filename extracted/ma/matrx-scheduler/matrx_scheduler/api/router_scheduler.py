"""
HTTP API surface for matrx-scheduler.

Depends on: matrx_connect (AppContext, context_dep), fastapi, pydantic
            supabase + httpx (only when the default per_request factory is used)

Routes are mounted under ``/scheduler`` by default (see
``matrx_scheduler.api.include_routers``). Aidream's existing
``/scheduling/*`` routes are intentionally distinct so both can coexist
without conflict.

Auth model:
  - Every write goes through a per-request Supabase client built from
    the caller's JWT. RLS is the single line of authority on row
    ownership.
  - The service-role client (used by the scanner) is never used here.
  - ``ctx`` is validated by ``matrx_connect``'s context_dep; the user_id
    on the AppContext is used to stamp inserted rows (RLS will reject
    if it doesn't match auth.uid()).
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from matrx_connect import AppContext, authenticated_resource_bootstrap, context_dep
from matrx_connect.org_hold import OrganizationRequired

from matrx_scheduler import (
    cron_helpers,
    duplicate_guard,
    scanner,
)
from matrx_scheduler import (
    next_due as next_due_module,
)
from matrx_scheduler.api import schemas, user_queries
from matrx_scheduler.api.per_request import user_client_dep

router = APIRouter()
log = logging.getLogger(__name__)


VALID_KINDS = {"agent", "tool", "ping"}


# ── Helpers ─────────────────────────────────────────────────────────────


def _require_organization(ctx: AppContext, what: str) -> str:
    """The organization a new schedule belongs to: the request's, or the hold.

    ``sch_task`` / ``sch_trigger`` carry ``organization_id`` NOT NULL with no
    default — nothing may choose one for the caller (Data Doctrine, 2026-09-19).
    """
    if not ctx.organization_id:
        raise OrganizationRequired(what=what, user_id=ctx.user_id)
    return str(ctx.organization_id)


def _require_owner_match(row: dict[str, Any], ctx: AppContext) -> None:
    """
    Defensive owner check on top of RLS.

    RLS guarantees the caller can only read their own rows; if a row
    came back at all, the caller owns it. This is an extra belt to
    catch any future RLS misconfiguration -- if the user_id on the row
    doesn't match the AppContext user_id, refuse the response.
    """
    row_user = row.get("user_id")
    if row_user and ctx.user_id and row_user != ctx.user_id:
        # A cross-owner request is an expected authorization refusal, not an
        # application failure. Keep it visible without promoting routine
        # hostile/stale-client traffic to ERROR telemetry.
        log.warning(
            "owner mismatch: row.user_id=%s ctx.user_id=%s",
            row_user,
            ctx.user_id,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="forbidden",
        )


def _serialize_dt(value: Any) -> str | None:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _classify_supabase_error(exc: Exception) -> tuple[int, str]:
    """
    Map a Supabase error to an HTTP status + message.

    Errors from the supabase-py async client typically carry a JSON
    body with ``code`` / ``message``. We pattern-match on the
    stringified exception for the common cases.
    """
    msg = str(exc)
    lower = msg.lower()
    if "row level security" in lower or "rls" in lower or "permission denied" in lower:
        return (status.HTTP_403_FORBIDDEN, "forbidden")
    if "not found" in lower or "no rows" in lower or "pgrst116" in lower:
        return (status.HTTP_404_NOT_FOUND, "not found")
    if "authentication" in lower or "jwt" in lower:
        return (status.HTTP_401_UNAUTHORIZED, "auth required")
    return (status.HTTP_400_BAD_REQUEST, "request failed")


def _validate_kind(kind: str) -> None:
    if kind not in VALID_KINDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"invalid kind '{kind}'; must be one of {sorted(VALID_KINDS)}",
        )


def _validate_task_create(body: schemas.TaskCreateRequest) -> None:
    _validate_kind(body.kind)
    if body.kind == "tool" and not (body.taxonomy_node_id or "").strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                "Tool schedules require a Feature Registry taxonomy_node_id; "
                "name-only system jobs are not allowed."
            ),
        )
    if body.kind != "agent":
        return
    if body.agent_task is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="agent schedules require agent_task with an agent_id or mandate_key",
        )
    if not ((body.agent_task.agent_id or "").strip() or (body.agent_task.mandate_key or "").strip()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                "Choose an agent or Mandate before creating this schedule. "
                "There is no platform default selection."
            ),
        )


async def _require_runnable_agent_task(
    sb: Any,
    task_id: str,
    *,
    task_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    task = task_row if task_row is not None else await user_queries.get_task(sb, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found",
        )
    if task.get("kind") != "agent":
        return task
    agent_task = await user_queries.get_agent_task(sb, task_id)
    if agent_task is None or not (
        str(agent_task.get("agent_id") or "").strip()
        or str(agent_task.get("mandate_key") or "").strip()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                "Choose an agent or Mandate before enabling or running this schedule. "
                "There is no platform default selection."
            ),
        )
    return task


async def _find_existing_twin(sb: Any, fingerprint: str) -> str | None:
    """The caller's oldest live schedule with this fingerprint, if any.

    Fails OPEN: if the lookup itself breaks, this returns None so the create
    proceeds normally. A guard against accidental duplicates must never become
    the reason a user cannot create a schedule at all -- the cost of a missed
    duplicate is a duplicate; the cost of a false block is a broken product.
    """
    try:
        rows = await user_queries.load_task_fingerprints(sb)
    except Exception:  # noqa: BLE001 — fail OPEN, loudly
        log.exception(
            "[scheduler-duplicate-guard] could not read existing schedules to check "
            "for duplicates; allowing the create to proceed unchecked."
        )
        return None
    matches = [r for r in rows if r.get("fingerprint") == fingerprint and r.get("can_fire", True)]
    if not matches:
        return None
    matches.sort(key=lambda r: (str(r.get("created_at") or ""), str(r.get("id"))))
    return str(matches[0]["id"])


async def _hydrate_task(sb: Any, task_id: str) -> schemas.TaskDetailResponse | None:
    """Load a task with its agent_task and triggers, in the create-response shape."""
    task_row = await user_queries.get_task(sb, task_id)
    if task_row is None:
        return None
    agent_task_row = await user_queries.get_agent_task(sb, task_id)
    trigger_rows = await user_queries.list_triggers_for_task(sb, task_id)
    return schemas.TaskDetailResponse(
        task=schemas.TaskResponse(**task_row),
        agent_task=(schemas.AgentTaskResponse(**agent_task_row) if agent_task_row else None),
        triggers=[schemas.TriggerResponse(**t) for t in trigger_rows],
        recent_runs=[],
    )


# ── Task CRUD ───────────────────────────────────────────────────────────


@router.post(
    "/tasks",
    response_model=schemas.TaskDetailResponse,
    status_code=status.HTTP_201_CREATED,
    # 200 is a REAL outcome of this route, not a theoretical one: an identical
    # create returns the existing schedule instead of inserting a twin (THE
    # SCHEDULER DUPLICATE GUARD). Declared so the generated OpenAPI tells the
    # truth — clients are generated from it, and a spec that documents only 201
    # invites a consumer that treats the deduplicated success as an error.
    responses={
        200: {
            "model": schemas.TaskDetailResponse,
            "description": (
                "An identical live schedule already existed; it is returned "
                "unchanged with `deduplicated: true` and nothing was created."
            ),
        }
    },
)
async def create_task(
    body: schemas.TaskCreateRequest,
    response: Response,
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.TaskDetailResponse:
    """
    Create a task, optionally with an attached agent_task and trigger.

    All three rows live in one logical creation, but each is its own
    Supabase insert. If a downstream insert fails, the task row is
    rolled back (best effort -- a hard crash between inserts is
    possible; the FE should treat orphan tasks as benign and cleanable).

    IDEMPOTENT on identity (THE SCHEDULER DUPLICATE GUARD). If the caller
    already owns a live schedule doing the same work on the same trigger,
    this returns THAT schedule with ``deduplicated=true`` and HTTP 200
    instead of inserting a twin. A double-click, or an MCP retry whose
    first attempt actually succeeded, therefore cannot produce two
    always-on schedules billing for one job -- the failure measured live on
    2026-08-14, where an identical pair ran hourly for five days unnoticed.

    Pass ``force=true`` to create anyway when a second similar schedule is
    genuinely wanted; the guard then still raises the alarm so the pair is
    visible rather than silent.
    """
    if not ctx.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="auth required",
        )
    _validate_task_create(body)
    organization_id = _require_organization(ctx, "create a schedule")

    # Only a schedule that can actually FIRE can duplicate another one. A paused
    # task, or one created with no enabled trigger, bills nothing — checking it
    # would risk blocking a legitimate create to prevent an imaginary cost.
    incoming_can_fire = duplicate_guard.can_fire(
        {"enabled": body.enabled},
        [{"enabled": body.trigger.enabled}] if body.trigger is not None else [],
    )
    incoming_fingerprint = duplicate_guard.task_fingerprint(
        kind=body.kind,
        queue=body.queue,
        agent_id=(body.agent_task.agent_id if body.agent_task else None),
        mandate_key=(body.agent_task.mandate_key if body.agent_task else None),
        prompt=(body.agent_task.prompt if body.agent_task else None),
        variables=(body.agent_task.variables if body.agent_task else None),
        # A trigger arriving disabled cannot fire, so it is not part of identity.
        triggers=(
            [{"type": body.trigger.type, "config": body.trigger.config}]
            if body.trigger is not None and body.trigger.enabled
            else []
        ),
    )
    existing_twin = (
        await _find_existing_twin(sb, incoming_fingerprint) if incoming_can_fire else None
    )

    if existing_twin is not None and not body.force:
        # Refusing to create a SECOND thing. Nothing is deleted, nothing is
        # overwritten -- the caller gets the schedule that already does this.
        log.warning(
            "[scheduler-duplicate-guard] create refused for user %s: fingerprint %s "
            "already belongs to sch_task %s. Returning the existing schedule.",
            ctx.user_id,
            incoming_fingerprint,
            existing_twin,
        )
        detail = await _hydrate_task(sb, existing_twin)
        if detail is not None:
            response.status_code = status.HTTP_200_OK
            detail.deduplicated = True
            return detail
        # The twin vanished between the check and the read (deleted concurrently).
        # Falling through to a normal create is the correct answer: the thing we
        # were protecting no longer exists.
        log.warning(
            "[scheduler-duplicate-guard] sch_task %s disappeared before it could be "
            "returned; proceeding with a normal create.",
            existing_twin,
        )

    # Computed next_due_at for the trigger (if any).
    computed_next_due_iso: str | None = None
    if body.trigger is not None:
        next_at = next_due_module.compute_next_due_at(body.trigger.type, body.trigger.config)
        if next_at is not None:
            computed_next_due_iso = next_at.isoformat()

    expires_iso = body.expires_at.isoformat() if body.expires_at else None

    try:
        task_row = await user_queries.insert_task(
            sb,
            user_id=ctx.user_id,
            kind=body.kind,
            title=body.title,
            description=body.description,
            queue=body.queue,
            surfaces=body.surfaces,
            enabled=body.enabled,
            expires_at=expires_iso,
            tags=body.tags,
            taxonomy_node_id=body.taxonomy_node_id,
            organization_id=organization_id,
        )
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        log.exception("sch_task insert failed")
        raise HTTPException(status_code=code, detail=detail) from exc

    task_id = task_row["id"]
    agent_task_row: dict[str, Any] | None = None
    trigger_row: dict[str, Any] | None = None

    try:
        if body.agent_task is not None:
            agent_task_row = await user_queries.upsert_agent_task(
                sb,
                task_id=task_id,
                organization_id=task_row["organization_id"],
                agent_id=body.agent_task.agent_id,
                mandate_key=body.agent_task.mandate_key,
                prompt=body.agent_task.prompt,
                variables=body.agent_task.variables,
                persistent_conversation_id=(body.agent_task.persistent_conversation_id),
                auth_mode=body.agent_task.auth_mode,
                max_runtime_seconds=body.agent_task.max_runtime_seconds,
                max_concurrent=body.agent_task.max_concurrent,
            )

        if body.trigger is not None:
            trigger_row = await user_queries.insert_trigger(
                sb,
                user_id=ctx.user_id,
                task_id=task_id,
                type=body.trigger.type,
                config=body.trigger.config,
                enabled=body.trigger.enabled,
                next_due_at=computed_next_due_iso,
                organization_id=task_row["organization_id"],
            )
    except Exception as exc:
        # Best-effort rollback: archive the task row we just created
        # (deleted_at + enabled=false) so it never fires and never lists.
        # Delete means archive — even for a rollback. RLS gates the write
        # to our own row, so this is safe.
        log.exception("child insert failed; rolling back task %s", task_id)
        try:
            await user_queries.soft_delete_task(sb, task_id)
        except Exception:
            log.exception("rollback delete of task %s also failed", task_id)
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc

    if existing_twin is not None:
        # force=true: the user asked for a second one and got it. The guard does
        # not overrule that -- it makes the pair VISIBLE, which is the whole
        # failure being fixed. Silence is what cost five days of doubled runs.
        await duplicate_guard.note_duplicate(
            duplicate_guard.DuplicateFinding(
                fingerprint=incoming_fingerprint,
                user_id=str(ctx.user_id or ""),
                task_ids=(existing_twin, task_id),
                titles=(body.title, body.title),
                existing_task_id=existing_twin,
                reason=(
                    f"a new schedule {task_id} ({body.title!r}) was created with "
                    f"force=true even though {existing_twin} already runs the same "
                    f"work on the same trigger. Both will fire."
                ),
                evidence={
                    "fingerprint": incoming_fingerprint,
                    "task_ids": [existing_twin, task_id],
                    "forced": True,
                },
            )
        )

    return schemas.TaskDetailResponse(
        task=schemas.TaskResponse(**task_row),
        agent_task=(schemas.AgentTaskResponse(**agent_task_row) if agent_task_row else None),
        triggers=[schemas.TriggerResponse(**trigger_row)] if trigger_row else [],
        recent_runs=[],
    )


@router.get("/tasks", response_model=schemas.TaskListResponse, dependencies=[Depends(authenticated_resource_bootstrap)])
async def list_tasks(
    kind: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.TaskListResponse:
    """List the caller's tasks (RLS-scoped)."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")
    if kind is not None:
        _validate_kind(kind)

    try:
        rows = await user_queries.list_tasks(
            sb, kind=kind, enabled=enabled, limit=limit, offset=offset
        )
        total = await user_queries.count_tasks(sb, kind=kind, enabled=enabled)
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        log.exception("list_tasks failed")
        raise HTTPException(status_code=code, detail=detail) from exc

    return schemas.TaskListResponse(
        tasks=[schemas.TaskResponse(**row) for row in rows],
        total=total,
    )


@router.get("/tasks/duplicates", response_model=schemas.DuplicateScheduleResponse, dependencies=[Depends(authenticated_resource_bootstrap)])
async def list_duplicate_schedules(
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.DuplicateScheduleResponse:
    """The caller's schedules that duplicate each other (THE SCHEDULER DUPLICATE GUARD).

    Grouped by what a schedule DOES -- agent, prompt, variables, queue, and
    enabled triggers -- deliberately ignoring title and description, because two
    differently-named schedules running the same agent on the same cron cost
    exactly as much as two identically-named ones.

    Declared BEFORE ``/tasks/{task_id}`` so the literal path wins the match;
    FastAPI resolves routes in declaration order and would otherwise read
    "duplicates" as a task id.
    """
    if not ctx.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="auth required",
        )
    rows = await user_queries.load_task_fingerprints(sb)
    by_id = {str(r["id"]): r for r in rows}
    groups: list[schemas.DuplicateScheduleGroup] = []
    for finding in duplicate_guard.group_duplicates(rows):
        members = [
            schemas.DuplicateScheduleMember(
                id=tid,
                title=by_id.get(tid, {}).get("title"),
                enabled=bool(by_id.get(tid, {}).get("enabled", True)),
                created_at=by_id.get(tid, {}).get("created_at"),
                is_original=(index == 0),
            )
            for index, tid in enumerate(finding.task_ids)
        ]
        groups.append(
            schemas.DuplicateScheduleGroup(
                fingerprint=finding.fingerprint,
                members=members,
                redundant_count=finding.redundant_count,
                enabled_count=sum(1 for m in members if m.enabled),
            )
        )
    return schemas.DuplicateScheduleResponse(groups=groups)


@router.get("/tasks/{task_id}", response_model=schemas.TaskDetailResponse, dependencies=[Depends(authenticated_resource_bootstrap)])
async def get_task(
    task_id: str,
    runs_limit: int = Query(default=10, ge=0, le=100),
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.TaskDetailResponse:
    """
    Fetch a single task with its agent_task, triggers, and recent runs.
    Each piece is loaded with its own query so the failure mode for any
    one is isolated.
    """
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")

    try:
        task_row = await user_queries.get_task(sb, task_id)
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc

    if not task_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    _require_owner_match(task_row, ctx)

    try:
        agent_task_row = await user_queries.get_agent_task(sb, task_id)
        trigger_rows = await user_queries.list_triggers_for_task(sb, task_id)
        run_rows = (
            await user_queries.list_runs(sb, task_id=task_id, limit=runs_limit)
            if runs_limit
            else []
        )
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        log.exception("get_task hydration failed")
        raise HTTPException(status_code=code, detail=detail) from exc

    return schemas.TaskDetailResponse(
        task=schemas.TaskResponse(**task_row),
        agent_task=(schemas.AgentTaskResponse(**agent_task_row) if agent_task_row else None),
        triggers=[schemas.TriggerResponse(**t) for t in trigger_rows],
        recent_runs=[schemas.RunResponse(**r) for r in run_rows],
    )


@router.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def patch_task(
    task_id: str,
    body: schemas.TaskPatchRequest,
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.TaskResponse:
    """Patch a subset of task fields, preserving explicit nullable clears."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")

    if body.enabled is True:
        try:
            task_row = await _require_runnable_agent_task(sb, task_id)
        except HTTPException:
            raise
        except Exception as exc:
            code, detail = _classify_supabase_error(exc)
            raise HTTPException(status_code=code, detail=detail) from exc
        _require_owner_match(task_row, ctx)

    patch: dict[str, Any] = {}
    for field_name in (
        "title",
        "queue",
        "surfaces",
        "enabled",
        "tags",
    ):
        value = getattr(body, field_name)
        if value is not None:
            patch[field_name] = value
    # `description` and `expires_at` are nullable columns. Pydantic's value is
    # None for both "omitted" and "explicitly clear", so membership in
    # model_fields_set is the only honest PATCH distinction. Dropping explicit
    # null here made the API report success while leaving the old value intact.
    if "description" in body.model_fields_set:
        patch["description"] = body.description
    if "expires_at" in body.model_fields_set:
        patch["expires_at"] = (
            body.expires_at.isoformat() if body.expires_at is not None else None
        )

    try:
        row = await user_queries.update_task(sb, task_id, patch)
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc

    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    _require_owner_match(row, ctx)
    return schemas.TaskResponse(**row)


@router.delete("/tasks/{task_id}", response_model=schemas.DeletedResponse)
async def delete_task(
    task_id: str,
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.DeletedResponse:
    """
    Soft-delete (set enabled=false). Hard-delete is not exposed --
    sch_run references task_id, so cascading deletes would lose run
    history. To permanently remove a task, an admin route or a manual
    DB op is required.
    """
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")

    try:
        ok = await user_queries.soft_delete_task(sb, task_id)
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc

    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    return schemas.DeletedResponse(deleted=True, soft=True)


# ── Run now ─────────────────────────────────────────────────────────────


@router.post("/tasks/{task_id}/run-now", response_model=schemas.RunNowResponse)
async def run_now(
    task_id: str,
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.RunNowResponse:
    """
    Enqueue a manual run via the sch_enqueue_manual_run RPC. The RPC
    enforces task ownership inside Postgres -- a misbehaving FE cannot
    fire someone else's task.
    """
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")

    try:
        task_row = await _require_runnable_agent_task(sb, task_id)
        _require_owner_match(task_row, ctx)
        run_id = await user_queries.enqueue_manual_run(sb, task_id)
    except HTTPException:
        raise
    except Exception as exc:
        msg = str(exc).lower()
        if "task not found" in msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="task not found"
            ) from exc
        if "forbidden" in msg:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden") from exc
        code, detail = _classify_supabase_error(exc)
        log.exception("run-now RPC failed for task %s", task_id)
        raise HTTPException(status_code=code, detail=detail) from exc

    return schemas.RunNowResponse(run_id=run_id)


# ── Trigger CRUD ────────────────────────────────────────────────────────


@router.get("/triggers", response_model=schemas.TriggerListResponse, dependencies=[Depends(authenticated_resource_bootstrap)])
async def list_triggers(
    task_id: str = Query(..., description="parent task id"),
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.TriggerListResponse:
    """List triggers belonging to a specific task (RLS-scoped)."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")
    try:
        rows = await user_queries.list_triggers_for_task(sb, task_id)
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc
    return schemas.TriggerListResponse(triggers=[schemas.TriggerResponse(**t) for t in rows])


@router.post(
    "/triggers",
    response_model=schemas.TriggerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_trigger(
    body: schemas.TriggerCreateRequest,
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.TriggerResponse:
    """Create a trigger attached to an existing task."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")

    if body.enabled:
        try:
            task_row = await _require_runnable_agent_task(sb, body.task_id)
        except HTTPException:
            raise
        except Exception as exc:
            code, detail = _classify_supabase_error(exc)
            raise HTTPException(status_code=code, detail=detail) from exc
        _require_owner_match(task_row, ctx)
    else:
        task_row = await user_queries.get_task(sb, body.task_id)
        if task_row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    # A trigger is a CHILD of its task and inherits the task's organization.
    task_organization_id = task_row.get("organization_id")
    if not task_organization_id:
        raise OrganizationRequired(
            what=f"add a trigger to task {body.task_id}",
            user_id=ctx.user_id,
            remedy="The task carries no organization; recreate it from an organization.",
        )

    next_at = next_due_module.compute_next_due_at(body.type, body.config)
    next_iso = next_at.isoformat() if next_at else None

    try:
        row = await user_queries.insert_trigger(
            sb,
            user_id=ctx.user_id,
            task_id=body.task_id,
            type=body.type,
            config=body.config,
            enabled=body.enabled,
            next_due_at=next_iso,
            organization_id=task_organization_id,
        )
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        log.exception("trigger insert failed for task %s", body.task_id)
        raise HTTPException(status_code=code, detail=detail) from exc
    return schemas.TriggerResponse(**row)


@router.patch("/triggers/{trigger_id}", response_model=schemas.TriggerResponse)
async def patch_trigger(
    trigger_id: str,
    body: schemas.TriggerPatchRequest,
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.TriggerResponse:
    """Patch a trigger. If type or config changed, recomputes next_due_at."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")

    patch: dict[str, Any] = {}
    if body.type is not None:
        patch["type"] = body.type
    if body.config is not None:
        patch["config"] = body.config
    if body.enabled is not None:
        patch["enabled"] = body.enabled

    # If type/config changed or this patch enables dispatch, load the parent
    # once so invalid agent schedules cannot be made runnable through a child.
    if "type" in patch or "config" in patch or body.enabled is True:
        try:
            existing = await user_queries.get_trigger(sb, trigger_id)
        except Exception as exc:
            code, detail = _classify_supabase_error(exc)
            raise HTTPException(status_code=code, detail=detail) from exc
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="trigger not found")
        _require_owner_match(existing, ctx)
        if body.enabled is True:
            try:
                task_row = await _require_runnable_agent_task(sb, str(existing["task_id"]))
            except HTTPException:
                raise
            except Exception as exc:
                code, detail = _classify_supabase_error(exc)
                raise HTTPException(status_code=code, detail=detail) from exc
            _require_owner_match(task_row, ctx)
        if "type" in patch or "config" in patch:
            new_type = patch.get("type", existing.get("type"))
            new_config = patch.get("config", existing.get("config") or {})
            next_at = next_due_module.compute_next_due_at(new_type, new_config)
            patch["next_due_at"] = next_at.isoformat() if next_at else None

    try:
        row = await user_queries.update_trigger(sb, trigger_id, patch)
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="trigger not found")
    _require_owner_match(row, ctx)
    return schemas.TriggerResponse(**row)


@router.delete("/triggers/{trigger_id}", response_model=schemas.DeletedResponse)
async def delete_trigger(
    trigger_id: str,
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.DeletedResponse:
    """Soft-delete a trigger (``deleted_at`` set, ``enabled`` cleared together)."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")
    try:
        ok = await user_queries.delete_trigger(sb, trigger_id)
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="trigger not found")
    return schemas.DeletedResponse(deleted=True, soft=True)


# ── Runs (read-only) ────────────────────────────────────────────────────


@router.get("/runs", response_model=schemas.RunListResponse, dependencies=[Depends(authenticated_resource_bootstrap)])
async def list_runs(
    task_id: str | None = Query(default=None),
    run_status: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.RunListResponse:
    """List run history (RLS-scoped). Filter by task_id and/or status."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")
    try:
        rows = await user_queries.list_runs(
            sb, task_id=task_id, status=run_status, limit=limit, offset=offset
        )
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc
    return schemas.RunListResponse(runs=[schemas.RunResponse(**r) for r in rows])


@router.get("/runs/{run_id}", response_model=schemas.RunResponse, dependencies=[Depends(authenticated_resource_bootstrap)])
async def get_run(
    run_id: str,
    sb: Any = Depends(user_client_dep),
    ctx: AppContext = Depends(context_dep),
) -> schemas.RunResponse:
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")
    try:
        row = await user_queries.get_run(sb, run_id)
    except Exception as exc:
        code, detail = _classify_supabase_error(exc)
        raise HTTPException(status_code=code, detail=detail) from exc
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="run not found")
    _require_owner_match(row, ctx)
    return schemas.RunResponse(**row)


# ── Cron + next-due (pure compute, no DB) ───────────────────────────────


@router.post("/cron/validate", response_model=schemas.ValidateCronResponse)
async def validate_cron(
    body: schemas.ValidateCronRequest,
    ctx: AppContext = Depends(context_dep),
) -> schemas.ValidateCronResponse:
    """Validate a cron expression and preview the next N fires."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")
    err = cron_helpers.validate_cron(body.expression, body.tz)
    if err:
        return schemas.ValidateCronResponse(valid=False, error=err)
    try:
        fires = cron_helpers.next_n_fires(body.expression, body.tz, body.next_n)
    except Exception as exc:
        return schemas.ValidateCronResponse(valid=False, error=str(exc))
    return schemas.ValidateCronResponse(
        valid=True,
        next_fires_utc=[f.isoformat() for f in fires],
    )


@router.post("/cron/preview-fires", response_model=schemas.PreviewFiresResponse)
async def preview_fires(
    body: schemas.PreviewFiresRequest,
    ctx: AppContext = Depends(context_dep),
) -> schemas.PreviewFiresResponse:
    """
    Preview next-fire times for any trigger config (cron, interval,
    heartbeat, one-shot). Event-driven triggers (manual, dependency,
    event, context-match) return an empty list with event_driven=True.
    """
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")

    trigger_type = body.trigger_type
    config = body.config or {}

    if trigger_type == "cron":
        expression = config.get("expression")
        tz_name = config.get("tz", "UTC")
        if not expression:
            return schemas.PreviewFiresResponse(next_fires_utc=[])
        try:
            fires = cron_helpers.next_n_fires(expression, tz_name, body.n)
        except Exception as exc:
            log.warning("preview-fires cron parse failed: %s", exc)
            return schemas.PreviewFiresResponse(next_fires_utc=[])
        return schemas.PreviewFiresResponse(next_fires_utc=[f.isoformat() for f in fires])

    if trigger_type in ("interval", "heartbeat"):
        first = next_due_module.compute_next_due_at(trigger_type, config)
        if first is None:
            return schemas.PreviewFiresResponse(next_fires_utc=[])
        try:
            every = int(config.get("every_seconds", 0))
        except (TypeError, ValueError):
            return schemas.PreviewFiresResponse(next_fires_utc=[first.isoformat()])
        from datetime import timedelta

        fires = [first + timedelta(seconds=every * i) for i in range(body.n)]
        return schemas.PreviewFiresResponse(next_fires_utc=[f.isoformat() for f in fires])

    if trigger_type == "one-shot":
        first = next_due_module.compute_next_due_at(trigger_type, config)
        if first is None:
            return schemas.PreviewFiresResponse(next_fires_utc=[])
        return schemas.PreviewFiresResponse(next_fires_utc=[first.isoformat()])

    # Event-driven triggers.
    return schemas.PreviewFiresResponse(next_fires_utc=[], event_driven=True)


@router.post("/compute-next-due-at", response_model=schemas.ComputeNextDueResponse)
async def compute_next_due_at(
    body: schemas.ComputeNextDueRequest,
    ctx: AppContext = Depends(context_dep),
) -> schemas.ComputeNextDueResponse:
    """Compute next_due_at for a trigger config (single value)."""
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")
    next_at = next_due_module.compute_next_due_at(body.trigger_type, body.config)
    return schemas.ComputeNextDueResponse(
        next_due_at=next_at.isoformat() if next_at else None,
        event_driven=next_at is None,
    )


# ── Scanner status (admin) ──────────────────────────────────────────────


@router.get("/status", response_model=schemas.ScannerStatusResponse, dependencies=[Depends(authenticated_resource_bootstrap)])
async def get_status(
    ctx: AppContext = Depends(context_dep),
) -> schemas.ScannerStatusResponse:
    """
    Scanner health. Admin-only -- non-admins receive 403. The error
    message is truncated to 200 chars to avoid leaking internal detail
    to clients that can see this endpoint.
    """
    if not ctx.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth required")
    if not ctx.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin only")

    st = scanner.status()
    safe_error = st.error_message[:200] if st.error_message else None
    return schemas.ScannerStatusResponse(
        running=st.running,
        started_at=_serialize_dt(st.started_at),
        last_tick_at=_serialize_dt(st.last_tick_at),
        last_tick_duration_ms=st.last_tick_duration_ms,
        last_tick_claimed=st.last_tick_claimed,
        last_tick_expired_sweeps=st.last_tick_expired_sweeps,
        last_tick_manual_claimed=st.last_tick_manual_claimed,
        total_runs_dispatched=st.total_runs_dispatched,
        in_flight_count=st.in_flight_count,
        consecutive_errors=st.consecutive_errors,
        error_message=safe_error,
    )
