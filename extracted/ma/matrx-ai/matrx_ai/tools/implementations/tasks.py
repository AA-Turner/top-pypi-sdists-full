"""The `task` tool — list/get/create/update/delete on workspace.tasks.

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
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.person_session import acts_as_the_person


def _read_only_result(tool_name: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
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


def _acts_as_the_person(tool_name: str):
    """The shared ``acts_as_the_person`` wrapper (``matrx_ai.tools.person_session``)."""
    return acts_as_the_person(tool_name, subject="your tasks")


@_acts_as_the_person("task_get")
async def task_get(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    task_id = args.get("task_id", "").strip()
    if not task_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="task_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_get", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        result = await tasks_manager_instance.get_task(task_id)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type=_manager_error_type(result, "execution"),
                    message=result.get("error") or f"Task {task_id} could not be read.",
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_get", call_id=ctx.call_id,
            )
        t = result["task"]
        return ToolResult(
            success=True,
            output={
                "id": t.get("id"),
                "title": t.get("title"),
                "description": t.get("description"),
                "status": t.get("status"),
                "priority": t.get("priority"),
                "due_date": t.get("due_date"),
                "project_id": t.get("project_id"),
                "parent_task_id": t.get("parent_task_id"),
                "assignee_id": t.get("assignee_id"),
                "published_to_web": bool(t.get("published_to_web")),
                "shown_to": t.get("shown_to"),
                "organization_id": t.get("organization_id"),
                "created_at": t.get("created_at"),
                "updated_at": t.get("updated_at"),
            },
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


def _compact_task(t: dict[str, Any]) -> dict[str, Any]:
    """The promised compact row — enough to pick, not the whole record. Use
    task_get for full details on one task."""
    return {
        "id": t.get("id"),
        "title": t.get("title"),
        "status": t.get("status"),
        "priority": t.get("priority"),
    }


@_acts_as_the_person("task_list")
async def task_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Returns a compact task list — id, title, status, priority only.
    Scope to project_id or parent_task_id if provided; otherwise returns the
    tasks the current person created in the organization this conversation
    carries (held with ``organization_required`` when it carries none).  Use task_get for full details on a specific task.
    Capped at 200 rows; the response reports the true `count`.
    """
    started_at = time.time()
    project_id = args.get("project_id", "").strip()
    parent_task_id = args.get("parent_task_id", "").strip()
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        from matrx_ai.tools.output_caps import TOOL_LIST_DEFAULT_LIMIT, cap_list

        limit = TOOL_LIST_DEFAULT_LIMIT

        if parent_task_id:
            # A parent the caller cannot see is an honest not-found naming it —
            # never an empty "no subtasks" success.
            parent = await tasks_manager_instance.get_task(parent_task_id)
            if not parent.get("success"):
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type=_manager_error_type(parent, "execution"),
                        message=parent.get("error")
                        or f"Task {parent_task_id} could not be read.",
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
            from matrx_ai.tools.organization_hold import (
                carried_organization_id,
                organization_required_result,
            )

            organization_id = carried_organization_id(ctx)
            if not organization_id:
                return organization_required_result(
                    what="list your tasks", tool_name="task_list", ctx=ctx, started_at=started_at
                )
            result = await tasks_manager_instance.list_tasks_for_user(
                ctx.user_id, organization_id=organization_id
            )
            tasks_key = "tasks"

        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(error_type="execution", message=result.get("error", "Failed to list tasks.")),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_list", call_id=ctx.call_id,
            )
        # The manager returned FULL task rows; project to the promised compact
        # shape (the docstring's contract was never honored) and cap the count.
        rows = [_compact_task(t) for t in result.get(tasks_key, [])]
        rows, info = cap_list(rows, limit=limit)
        output: dict[str, Any] = {"tasks": rows, "count": info.total, "shown": info.shown}
        if tasks_key == "tasks" and not project_id:
            # Say which organization the list is filtered to.
            output["organization_id"] = result.get("organization_id")
        if info.truncated:
            output["truncated"] = True
            output["note"] = (
                f"showing {info.shown} of {info.total}; scope by project_id/"
                "parent_task_id to narrow."
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
            error=ToolError(error_type="validation", message="title is required.", suggested_action="Provide a title for the task."),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_create", call_id=ctx.call_id,
        )
    from matrx_ai.tools.organization_hold import (
        carried_organization_id,
        organization_required_result,
    )

    organization_id = carried_organization_id(ctx)
    if not organization_id:
        return organization_required_result(
            what="create a task", tool_name="task_create", ctx=ctx, started_at=started_at
        )
    # The tool_def row still offers the retiring single level word; reconcile it once here.
    access = reconcile_row_access(
        legacy_level=args.get("visibility") or None,  # T-13 transitional wire input
        boundary="tool task.create",
    )
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        result = await tasks_manager_instance.create_task(
            user_id=ctx.user_id,
            organization_id=organization_id,
            title=title,
            description=args.get("description", ""),
            project_id=args.get("project_id") or None,
            parent_task_id=args.get("parent_task_id") or None,
            status=args.get("status", "incomplete"),
            priority=args.get("priority") or None,
            due_date=args.get("due_date") or None,
            assignee_id=args.get("assignee_id") or None,
            published_to_web=access.published_to_web,
            shown_to=access.shown_to,
        )
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(error_type="execution", message=result.get("error", "Failed to create task.")),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_create", call_id=ctx.call_id,
            )
        t = result["task"]
        return ToolResult(
            success=True,
            output={
                "id": t.get("id"),
                "title": t.get("title"),
                "status": t.get("status"),
                "project_id": t.get("project_id"),
                "organization_id": t.get("organization_id"),
                "published_to_web": bool(t.get("published_to_web")),
                "shown_to": t.get("shown_to"),
                "created_at": t.get("created_at"),
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
            error=ToolError(error_type="validation", message="task_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )
    if is_resource_read_only(task_id):
        return _read_only_result("task_update", started_at, ctx)
    updates = {k: v for k, v in args.items() if k != "task_id"}
    # The tool_def row still offers the retiring single level word; reconcile it once here.
    legacy_level = updates.pop("visibility", None)  # T-13 transitional wire input
    if legacy_level:
        published, shown_to = stated_row_access(legacy_level=legacy_level, boundary="tool task.update")
        if published is not None:
            updates.update(publish_columns(published, ctx.user_id))
        if shown_to is not None:
            updates["shown_to"] = shown_to
    if not updates:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="At least one field to update is required.",
                suggested_action="Provide one or more of: title, description, status, priority, due_date, project_id, parent_task_id, assignee_id.",
            ),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        prior_read = await tasks_manager_instance.get_task(task_id)
        prior = prior_read.get("task") if prior_read.get("success") else None
        result = await tasks_manager_instance.update_task(task_id, **updates)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type=_manager_error_type(result, "execution"),
                    message=result.get("error") or f"Task {task_id} was not updated.",
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_update", call_id=ctx.call_id,
            )
        t = result["task"]
        out: dict[str, Any] = {
            "id": t.get("id"),
            "title": t.get("title"),
            "status": t.get("status"),
            "priority": t.get("priority"),
            "updated_at": t.get("updated_at"),
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
            error=ToolError(error_type="validation", message="task_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_delete", call_id=ctx.call_id,
        )
    if is_resource_read_only(task_id):
        return _read_only_result("task_delete", started_at, ctx)
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        result = await tasks_manager_instance.delete_task(task_id)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type=_manager_error_type(result, "execution"),
                    message=result.get("error") or f"Task {task_id} was not deleted.",
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_delete", call_id=ctx.call_id,
            )
        return ToolResult(
            success=True,
            output={"deleted": True, "archived": True, "task_id": task_id},
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


def _task_validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
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
        return _task_validation_error(format_args_error(exc), started_at, ctx)

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
