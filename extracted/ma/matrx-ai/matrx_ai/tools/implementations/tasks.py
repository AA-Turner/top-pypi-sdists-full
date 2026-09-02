from __future__ import annotations

import time
import traceback
from typing import Any

from pydantic import ValidationError

from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only
from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import TaskArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult


def _read_only_result(tool_name: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=ctx.call_id,
    )


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
                error=ToolError(error_type="not_found", message=result.get("error", "Task not found.")),
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
                "is_public": t.get("is_public"),
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


async def task_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Returns a compact task list — id, title, status, priority only.
    Scope to project_id or parent_task_id if provided; otherwise returns all
    tasks for the current user.  Use task_get for full details on a specific task.
    Capped at 200 rows; the response reports the true `count`.
    """
    started_at = time.time()
    project_id = args.get("project_id", "").strip()
    parent_task_id = args.get("parent_task_id", "").strip()
    try:
        from matrx_ai.tools.output_caps import TOOL_LIST_DEFAULT_LIMIT, cap_list

        from matrx_ai.db.content_types.tasks import tasks_manager_instance

        limit = TOOL_LIST_DEFAULT_LIMIT

        if parent_task_id:
            result = await tasks_manager_instance.list_subtasks(parent_task_id)
            tasks_key = "subtasks"
        elif project_id:
            result = await tasks_manager_instance.list_tasks_for_project(project_id)
            tasks_key = "tasks"
        else:
            result = await tasks_manager_instance.list_tasks_for_user(ctx.user_id)
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
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        result = await tasks_manager_instance.create_task(
            user_id=ctx.user_id,
            title=title,
            description=args.get("description", ""),
            project_id=args.get("project_id") or None,
            parent_task_id=args.get("parent_task_id") or None,
            status=args.get("status", "incomplete"),
            priority=args.get("priority") or None,
            due_date=args.get("due_date") or None,
            assignee_id=args.get("assignee_id") or None,
            is_public=args.get("is_public", False),
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
    if not updates:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="At least one field to update is required.",
                suggested_action="Provide one or more of: title, description, status, priority, due_date, project_id, parent_task_id, assignee_id, is_public.",
            ),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.tasks import tasks_manager_instance
        result = await tasks_manager_instance.update_task(task_id, **updates)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(error_type="execution", message=result.get("error", "Update failed.")),
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
        return ToolResult(
            success=True, output=out,
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="task_update", call_id=ctx.call_id,
        )


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
                error=ToolError(error_type="execution", message=result.get("error", "Delete failed.")),
                started_at=started_at, completed_at=time.time(),
                tool_name="task_delete", call_id=ctx.call_id,
            )
        return ToolResult(
            success=True,
            output={"deleted": True, "task_id": task_id},
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
