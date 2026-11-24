"""The `task` tool — list/get/create/update/delete on projects.tasks.

EVERY ACTION RUNS AS THE PERSON. Each action opens the caller's RLS session
(``matrx_ai.tools.person_session.as_the_person``) around its ORM work, so
Postgres row-level security decides which tasks exist for them and which they
may change. This module never re-implements access. A task the caller may not
see answers ``not_found`` naming its id; one they can see but may not change
answers ``no_access``.
"""

from __future__ import annotations

import time
import traceback
from typing import Any

from matrx_utils.row_access import publish_columns, reconcile_row_access, stated_row_access
from pydantic import ValidationError

from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only
from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import TaskArgs
from matrx_ai.tools.implementations.kind_shared import is_uuid
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.person_session import acts_as_the_person
from matrx_ai.utils.carried_failure import carried_exception


def _read_only_result(tool_name: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(refusal=True, error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=ctx.call_id,
    )


_ACCESS_ERROR_TYPES = frozenset({"not_found", "no_access"})


def _manager_error_type(result: dict[str, Any], default: str) -> str:
    """Carry the manager's access answer (not_found / no_access) through unchanged."""
    error_type = result.get("error_type")
    return error_type if error_type in _ACCESS_ERROR_TYPES else default


#: The task fields that hold another row's id. Postgres refuses anything but a UUID there, so a model that
#: writes a name or a role ("staff", "me", a project's title) used to reach the database and come back as an
#: execution failure filed as a platform error (voice agent, 2026-11-19: assignee_id='staff').
_ID_FIELDS: tuple[str, ...] = ("project_id", "parent_task_id", "assignee_id")


def _malformed_id_refusal(
    args: dict[str, Any], tool_name: str, ctx: ToolContext, started_at: float
) -> ToolResult | None:
    """A refusal the model can correct when an id field holds something that is not an id; None when all fit."""
    for field in _ID_FIELDS:
        value = args.get(field)
        if value in (None, ""):
            continue
        if is_uuid(str(value)):
            continue
        # A refusal, never an exception: the tool decided not to act (guard
        # tests/package_host_contracts/test_tool_error_declarations.py).
        return ToolResult(
            success=False,
            error=ToolError(
                refusal=True,
                error_type="validation",
                message=f"{field} must be an id (a UUID), not {str(value)[:80]!r}.",
                suggested_action=(
                    f"Leave {field} out, or pass the id read from a list or get call. "
                    "Never a name, a role or a title."
                ),
            ),
            started_at=started_at, completed_at=time.time(),
            tool_name=tool_name, call_id=ctx.call_id,
        )
    return None


#: The task fields the record Action writes (its rules judge these). The access columns
#: (``published_to_web`` + stamps, ``shown_to``) are not record fields: the tool reconciles them and
#: writes them through its own manager, in the same person session.
_RECORD_FIELDS: tuple[str, ...] = (
    "title", "description", "status", "priority", "due_date", "due_time",
    "project_id", "parent_task_id", "assignee_id",
)


def _because(args: dict[str, Any]) -> dict[str, Any]:
    """The ``because`` the agent gave (source pointer + the person's exact words), for the host's record
    writer: it carries them to the run and the task rules read them. Absent → nothing is passed."""
    because = args.get("because")
    return {"because": dict(because)} if isinstance(because, dict) and because else {}


def _access_landed(saved: dict[str, Any], access_columns: dict[str, Any]) -> bool:
    """True when the saved row holds the access the tool asked for (its stamps move on their own)."""
    return all(
        str(saved.get(k)) == str(v) for k, v in access_columns.items() if k in ("published_to_web", "shown_to")
    )


def _refused_write(
    exc: Any, tool_name: str, task_id: str | None, seen: bool, ctx: ToolContext, started_at: float
) -> ToolResult:
    """The host's refusal (``RecordWriteRefused``) as the tool's answer.

    A row the writer could not find that the person COULD read a moment ago is one they may
    see but not change: ``no_access``, in the manager's own words."""
    error_type, message = exc.error_type, exc.message
    if error_type == "not_found" and seen and task_id:
        error_type = "no_access"
        message = f"You can view task {task_id} but you do not have permission to change it."
    elif error_type == "not_found" and task_id:
        message = f"Task {task_id} was not found, or you do not have access to it."
    return ToolResult(
        success=False,
        error=ToolError(refusal=True, error_type=error_type, message=message, suggested_action=exc.suggested_action),
        started_at=started_at, completed_at=time.time(),
        tool_name=tool_name, call_id=ctx.call_id,
    )


def _acts_as_the_person(tool_name: str):
    """The shared ``acts_as_the_person`` wrapper (``matrx_ai.tools.person_session``)."""
    return acts_as_the_person(tool_name, subject="your tasks")


def _hhmm(value: Any) -> str | None:
    """A stored time of day as HH:MM (the column is a Postgres time; the manager may hand back a time or text)."""
    return str(value)[:5] if value else None


def _iso(value: Any) -> str | None:
    """A stored date or timestamp as ISO text."""
    if value is None:
        return None
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def _task_record(t: dict[str, Any]) -> dict[str, Any]:
    """EVERY field a task write accepts, read back from the saved row — the one shape get, create and update
    answer with. A tool that accepts a field shows it back: an omitted due_time made models tell people a saved
    time had not saved (2026-11-18). Guard: tests/test_task_tool_shows_back_every_field.py."""
    return {
        "id": t.get("id"),
        "title": t.get("title"),
        "description": t.get("description"),
        "status": t.get("status"),
        "priority": t.get("priority"),
        "due_date": _iso(t.get("due_date")),
        "due_time": _hhmm(t.get("due_time")),
        "project_id": t.get("project_id"),
        "parent_task_id": t.get("parent_task_id"),
        "assignee_id": t.get("assignee_id"),
        "published_to_web": bool(t.get("published_to_web")),
        "shown_to": t.get("shown_to"),
        "organization_id": t.get("organization_id"),
        "created_at": _iso(t.get("created_at")),
        "updated_at": _iso(t.get("updated_at")),
    }


@_acts_as_the_person("task_get")
async def task_get(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    task_id = args.get("task_id", "").strip()
    if not task_id:
        return ToolResult(
            success=False,
            error=ToolError(refusal=True, error_type="validation", message="task_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_get", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        result = await tasks_manager_instance.get_task(task_id)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError.declared(
                    _manager_error_type(result, "execution"),
                    result.get("error") or f"Task {task_id} could not be read.",
                    exc=carried_exception(result),
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_get", call_id=ctx.call_id,
            )
        t = result["task"]
        return ToolResult(
            success=True,
            output=_task_record(t),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_get", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_get", call_id=ctx.call_id,
        )


_FINISHED = frozenset({"completed", "cancelled", "dismissed"})
_DATE_FILTERS = ("due_on", "due_from", "due_to", "overdue_as_of")


def _compact_task(t: dict[str, Any], names: dict[str, str] | None = None) -> dict[str, Any]:
    """A planner list row — what Today / Upcoming / a project view draw: enough to pick and to act on a day's
    tasks (due date and time, priority, project id AND name, parent). Use task_get for the full record."""
    project_id = t.get("project_id")
    return {
        "id": t.get("id"),
        "title": t.get("title"),
        "status": t.get("status"),
        "priority": t.get("priority"),
        "due_date": _iso(t.get("due_date")),
        "due_time": _hhmm(t.get("due_time")),
        "project_id": project_id,
        "project_name": (names or {}).get(str(project_id)) if project_id else None,
        "parent_task_id": t.get("parent_task_id"),
    }


def _date_filters(args: dict[str, Any]) -> dict[str, str] | str:
    """The list's date filters as ISO dates, or the sentence naming the one that is not a date."""
    import datetime as _dt

    out: dict[str, str] = {}
    for key in _DATE_FILTERS:
        raw = str(args.get(key) or "").strip()
        if not raw:
            continue
        try:
            out[key] = _dt.date.fromisoformat(raw).isoformat()
        except ValueError:
            return f"{key} must be a date written YYYY-MM-DD (got {raw!r}); work out the date from today first."
    return out


def _matches(t: dict[str, Any], f: dict[str, str]) -> bool:
    """A date filter keeps unfinished tasks with a due date inside it (ISO dates compare as text)."""
    due = t.get("due_date")
    if not due or t.get("status") in _FINISHED:
        return False
    if "due_on" in f and due != f["due_on"]:
        return False
    if "due_from" in f and due < f["due_from"]:
        return False
    if "due_to" in f and due > f["due_to"]:
        return False
    if "overdue_as_of" in f and not due < f["overdue_as_of"]:
        return False
    return True


@_acts_as_the_person("task_list")
async def task_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Returns planner list rows — id, title, status, priority, due date/time, project id and name, parent.
    Scope to project_id or parent_task_id if provided; otherwise returns the
    tasks the current person created across every organization they work in
    (the active organization is never a list filter). ``due_on`` / ``due_from`` / ``due_to`` /
    ``overdue_as_of`` (YYYY-MM-DD) narrow to a day, a range or overdue, unfinished tasks only.
    Use task_get for full details on a specific task. Capped at 200 rows; the response reports the true `count`.
    """
    started_at = time.time()
    project_id = (args.get("project_id") or "").strip()
    parent_task_id = (args.get("parent_task_id") or "").strip()
    filters = _date_filters(args)
    if isinstance(filters, str):
        return ToolResult(
            success=False,
            error=ToolError(refusal=True, error_type="validation", message=filters),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_list", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        from matrx_ai.tools.output_caps import TOOL_LIST_DEFAULT_LIMIT, cap_list

        limit = TOOL_LIST_DEFAULT_LIMIT
        # ``limit`` (a smaller page) and ``open_only`` (unfinished tasks only): a voice call passes both by default
        # (aidream realtime door ``VOICE_ARG_DEFAULTS``) — a spoken list is the short, current one.
        asked = args.get("limit")
        if isinstance(asked, int) and not isinstance(asked, bool) and 0 < asked < limit:
            limit = asked
        open_only = args.get("open_only") is True

        if parent_task_id:
            # A parent the caller cannot see is an honest not-found naming it —
            # never an empty "no subtasks" success.
            parent = await tasks_manager_instance.get_task(parent_task_id)
            if not parent.get("success"):
                return ToolResult(
                    success=False,
                    error=ToolError.declared(
                        _manager_error_type(parent, "execution"),
                        parent.get("error")
                        or f"Task {parent_task_id} could not be read.",
                        exc=carried_exception(parent),
                    ),
                    started_at=started_at, completed_at=time.time(),
                    tool_name="task_list", call_id=ctx.call_id,
                )
            result = await tasks_manager_instance.list_subtasks(parent_task_id)
            tasks_key = "subtasks"
        elif project_id:
            result = await tasks_manager_instance.list_tasks_for_project(project_id)
            tasks_key = "tasks"
        else:
            # A list is a read of the person's own tasks across every organization
            # they work in; the active organization is never a list filter.
            result = await tasks_manager_instance.list_tasks_for_user(ctx.user_id)
            tasks_key = "tasks"

        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError.declared("execution", result.get("error", "Failed to list tasks."), exc=carried_exception(result)),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_list", call_id=ctx.call_id,
            )
        # The manager returned FULL task rows; project to the promised compact
        # shape (the docstring's contract was never honored) and cap the count.
        found = [
            t for t in result.get(tasks_key, [])
            if (not filters or _matches(t, filters)) and not (open_only and t.get("status") in _FINISHED)
        ]
        if filters:
            found.sort(key=lambda t: (t.get("due_date") or "", t.get("due_time") or "99"))
        names = await tasks_manager_instance.project_names([t.get("project_id") for t in found if t.get("project_id")])
        rows = [_compact_task(t, names) for t in found]
        rows, info = cap_list(rows, limit=limit)
        output: dict[str, Any] = {"tasks": rows, "count": info.total, "shown": info.shown}
        if info.truncated:
            output["truncated"] = True
            output["note"] = (
                f"showing {info.shown} of {info.total}"
                + ("" if not open_only else " unfinished")
                + "; scope by project_id/parent_task_id or a due date to narrow."
            )
        return ToolResult(
            success=True,
            output=output,
            output_self_capped=True,  # compact rows + count cap ⇒ bounded result
            started_at=started_at, completed_at=time.time(),
            tool_name="task_list", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_list", call_id=ctx.call_id,
        )


@_acts_as_the_person("task_create")
async def task_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    title = args.get("title", "").strip()
    if not title:
        return ToolResult(
            success=False,
            error=ToolError(refusal=True, error_type="validation", message="title is required.", suggested_action="Provide a title for the task."),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_create", call_id=ctx.call_id,
        )
    malformed = _malformed_id_refusal(args, "task_create", ctx, started_at)
    if malformed is not None:
        return malformed
    from matrx_ai.tools.organization_hold import (
        carried_organization_id,
        organization_required_result,
    )

    organization_id = carried_organization_id(ctx)
    if not organization_id:
        return organization_required_result(
            what="create a task", tool_name="task_create", ctx=ctx, started_at=started_at
        )
    access = reconcile_row_access(
        published_to_web=args.get("published_to_web"),
        shown_to=args.get("shown_to") or None,
        boundary="tool task.create",
    )
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        from matrx_ai.tools.record_writer import RecordWriteRefused, host_record_writer

        given = {
            f: args[f] for f in _RECORD_FIELDS
            if f != "title" and args.get(f) not in (None, "")
        }
        writer = host_record_writer()
        if writer is not None:
            # THE RECORD ACTION (task.create): the server's task rules run (a task with no status
            # lands in the inbox, or is planned with a date or a project; a timed task takes the
            # person's zone). The access the tool reconciled rides the SAME write as trusted
            # columns: one insert, one version, one action run.
            access_columns = publish_columns(access.published_to_web, ctx.user_id)
            if access.shown_to:
                access_columns["shown_to"] = access.shown_to
            try:
                row = await writer(
                    operation="create", noun="task", data={"title": title, **given},
                    organization_id=organization_id, trusted=access_columns, **_because(args),
                )
            except RecordWriteRefused as exc:
                return _refused_write(exc, "task_create", None, False, ctx, started_at)
            result = await tasks_manager_instance.get_task(str((row or {}).get("id")))
        else:
            # A CLIENT host has no record Action: the manager writes the row as before.
            result = await tasks_manager_instance.create_task(
                user_id=ctx.user_id,
                organization_id=organization_id,
                title=title,
                published_to_web=access.published_to_web,
                shown_to=access.shown_to,
                **given,
            )
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError.declared("execution", result.get("error", "Failed to create task."), exc=carried_exception(result)),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_create", call_id=ctx.call_id,
            )
        t = result["task"]
        return ToolResult(
            success=True,
            output={
                **_task_record(t),
                # Undo of a create is a delete: there is no earlier version to restore.
                "version": t.get("version"),
                "previous_version": None,
            },
            started_at=started_at, completed_at=time.time(),
            tool_name="task_create", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=False),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_create", call_id=ctx.call_id,
        )


def _task_text(task: dict[str, Any], fields: list[str]) -> str:
    """A task as the person reads it: title as a heading, then each changed field."""
    parts = [f"# {task.get('title') or ''}"]
    for f in fields:
        if f == "title":
            continue
        value = task.get(f)
        parts.append(f"{f}:\n{value}" if f == "description" else f"{f}: {value}")
    return "\n\n".join(parts)


def _task_surface_write(
    result: ToolResult,
    prior: dict[str, Any],
    after: dict[str, Any],
    updates: dict[str, Any],
    task_id: str,
) -> ToolResult:
    """Before → after of the fields this update touched (title, description, status…)."""
    from matrx_ai.tools.surface_write import attach_surface_write

    fields = [k for k in updates if prior.get(k) != after.get(k)]
    if not fields:
        return result
    return attach_surface_write(
        result,
        before=_task_text(prior, fields),
        after=_task_text(after, fields),
        target_type="task",
        target_id=task_id,
        target_label=str(after.get("title") or prior.get("title") or ""),
        mode="overwrite",
        content_format="markdown",
    )


@_acts_as_the_person("task_update")
async def task_update(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    task_id = args.get("task_id", "").strip()
    if not task_id:
        return ToolResult(
            success=False,
            error=ToolError(refusal=True, error_type="validation", message="task_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )
    if is_resource_read_only(task_id):
        return _read_only_result("task_update", started_at, ctx)
    malformed = _malformed_id_refusal(args, "task_update", ctx, started_at)
    if malformed is not None:
        return malformed
    updates = {k: v for k, v in args.items() if k not in ("task_id", "because")}
    published, shown_to = stated_row_access(
        published_to_web=updates.pop("published_to_web", None),
        shown_to=updates.pop("shown_to", None) or None,
        boundary="tool task.update",
    )
    if published is not None:
        updates.update(publish_columns(published, ctx.user_id))
    if shown_to is not None:
        updates["shown_to"] = shown_to
    if not updates:
        return ToolResult(
            success=False,
            error=ToolError(
                refusal=True,
                error_type="validation",
                message="At least one field to update is required.",
                suggested_action="Provide one or more of: title, description, status, priority, due_date, due_time, project_id, parent_task_id, assignee_id, published_to_web, shown_to.",
            ),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        from matrx_ai.tools.record_writer import RecordWriteRefused, host_record_writer

        prior_read = await tasks_manager_instance.get_task(task_id)
        prior = prior_read.get("task") if prior_read.get("success") else None
        writer = host_record_writer()
        if writer is None:
            # A CLIENT host has no record Action: the manager writes the row as before.
            result = await tasks_manager_instance.update_task(task_id, **updates)
        elif prior is None:
            # Not there for this person: the manager's own answer (not_found naming the id).
            result = prior_read
        else:
            # THE RECORD ACTION (task.update): the task's rules run (completing a repeating task
            # rolls it to its next occurrence; a timed task takes the person's zone) as one action
            # run, the access the tool reconciled riding the same write as trusted columns.
            fields = {k: v for k, v in updates.items() if k in _RECORD_FIELDS}
            access_columns = {k: v for k, v in updates.items() if k not in _RECORD_FIELDS}
            if fields:
                try:
                    await writer(
                        operation="update", noun="task", data={**fields, "id": task_id},
                        trusted=access_columns or None, **_because(args),
                    )
                except RecordWriteRefused as exc:
                    return _refused_write(exc, "task_update", task_id, True, ctx, started_at)
                result = await tasks_manager_instance.get_task(task_id)
                saved = result.get("task") if result.get("success") else None
                if access_columns and isinstance(saved, dict) and not _access_landed(saved, access_columns):
                    # Every record field already held its value, so the Action wrote nothing and
                    # took no access columns: they are the only change, written once here.
                    result = await tasks_manager_instance.update_task(task_id, **access_columns)
            else:
                # Only access changed: no task rule reads it, and this is the one write.
                result = await tasks_manager_instance.update_task(task_id, **access_columns)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError.declared(
                    _manager_error_type(result, "execution"),
                    result.get("error") or f"Task {task_id} was not updated.",
                    exc=carried_exception(result),
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_update", call_id=ctx.call_id,
            )
        t = result["task"]
        out: dict[str, Any] = {
            # The whole saved task (project_id is what the turn's card strip folds by).
            **_task_record(t),
            # UNDO (Matrx Planner PS2): projects.tasks is version-captured (history.row_versions); an app restores
            # the replaced row with platform.version_restore('task', id, previous_version). `previous` holds the
            # old value of each field this write changed.
            "version": t.get("version"),
            "previous_version": prior.get("version") if isinstance(prior, dict) else None,
            "previous": (
                {k: prior.get(k) for k in updates if k in prior and prior.get(k) != t.get(k)}
                if isinstance(prior, dict) else None
            ),
        }
        if result.get("warning_stripped_immutable"):
            out["warning"] = f"Ignored immutable fields: {result['warning_stripped_immutable']}"
        done = ToolResult(
            success=True, output=out,
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )
        if isinstance(prior, dict):
            done = _task_surface_write(done, prior, t, updates, task_id)
        return done
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )


@_acts_as_the_person("task_delete")
async def task_delete(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    task_id = args.get("task_id", "").strip()
    if not task_id:
        return ToolResult(
            success=False,
            error=ToolError(refusal=True, error_type="validation", message="task_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_delete", call_id=ctx.call_id,
        )
    if is_resource_read_only(task_id):
        return _read_only_result("task_delete", started_at, ctx)
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        from matrx_ai.tools.record_writer import RecordWriteRefused, host_record_writer

        prior_read = await tasks_manager_instance.get_task(task_id)
        prior = prior_read.get("task") if isinstance(prior_read, dict) and prior_read.get("success") else None
        writer = host_record_writer()
        if writer is None:
            # A CLIENT host has no record Action: the manager archives the row as before.
            result = await tasks_manager_instance.delete_task(task_id)
        elif prior is None:
            result = prior_read
        else:
            # THE RECORD ACTION (task.delete): archives the row (soft delete), one action run.
            try:
                await writer(operation="delete", noun="task", data={"id": task_id})
            except RecordWriteRefused as exc:
                return _refused_write(exc, "task_delete", task_id, True, ctx, started_at)
            result = {"success": True, "task_id": task_id, "archived": True}
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError.declared(
                    _manager_error_type(result, "execution"),
                    result.get("error") or f"Task {task_id} was not deleted.",
                    exc=carried_exception(result),
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_delete", call_id=ctx.call_id,
            )
        return ToolResult(
            success=True,
            # UNDO: the archived row's last version, for platform.version_restore('task', id, previous_version).
            output={
                "deleted": True, "archived": True, "task_id": task_id,
                "previous_version": prior.get("version") if isinstance(prior, dict) else None,
            },
            started_at=started_at, completed_at=time.time(),
            tool_name="task_delete", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=False),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_delete", call_id=ctx.call_id,
        )


# ---------------------------------------------------------------------------
# task — unified action dispatcher
# ---------------------------------------------------------------------------

# Valid `task` actions are enforced by the TaskArgs discriminated union
# (arg_models/dispatcher_args.py) + tool_def.parameters."$variants" — the source of truth.


def _task_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "task"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _task_validation_error(message: str, started_at: float, ctx: ToolContext, *, exc: BaseException | None = None) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError.declared("validation", message, exc=exc),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="task",
        call_id=ctx.call_id,
    )


async def task(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        parsed = TaskArgs.model_validate(args).root
    except ValidationError as exc:
        return _task_validation_error(format_args_error(exc), started_at, ctx, exc=exc)

    action = parsed.action
    inner_args = parsed.model_dump(exclude={"action"}, exclude_unset=True)

    impl = {
        "list": task_list,
        "get": task_get,
        "create": task_create,
        "update": task_update,
        "delete": task_delete,
    }[action]

    from matrx_ai.tools.kind_stamp import stamp_result_kind
    from matrx_ai.tools.kinds.workbench import TaskToolResult

    return stamp_result_kind(
        _task_stamp(await impl(inner_args, ctx), started_at, ctx), TaskToolResult
    )
