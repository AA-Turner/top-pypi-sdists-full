"""The `project` tool — list/get/create/update on projects.projects (the twin of `task`).

EVERY ACTION RUNS AS THE PERSON (``matrx_ai.tools.person_session.acts_as_the_person``): Postgres
row-level security decides which projects exist for them and which they may change. A project the
caller may not see answers ``not_found`` naming its id; one they can see but may not change answers
``no_access``. Create writes into the CARRIED organization only (``carried_organization_id``) and
refuses without one. There is no delete action. Tasks go in a project through the `task` tool's
``project_id``.
"""

from __future__ import annotations

import time
from typing import Any

from pydantic import ValidationError

from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only
from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import ProjectArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.person_session import acts_as_the_person
from matrx_ai.utils.carried_failure import carried_exception

_ACCESS_ERROR_TYPES = frozenset({"not_found", "no_access"})


def _done(output: dict[str, Any], name: str, started_at: float, ctx: ToolContext, **extra: Any) -> ToolResult:
    return ToolResult(
        success=True, output=output, started_at=started_at, completed_at=time.time(),
        tool_name=name, call_id=ctx.call_id, **extra,
    )


def _refused(
    name: str, error_type: str, message: str, started_at: float, ctx: ToolContext, **error: Any
) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(refusal=True, error_type=error_type, message=message, **error),
        started_at=started_at, completed_at=time.time(), tool_name=name, call_id=ctx.call_id,
    )


def _failed(name: str, result: dict[str, Any], fallback: str, started_at: float, ctx: ToolContext) -> ToolResult:
    """Carry the manager's access answer (not_found / no_access) through unchanged."""
    error_type = result.get("error_type")
    return ToolResult(
        success=False,
        error=ToolError.declared(
            error_type if error_type in _ACCESS_ERROR_TYPES else "execution",
            result.get("error") or fallback,
            exc=carried_exception(result),
        ),
        started_at=started_at, completed_at=time.time(), tool_name=name, call_id=ctx.call_id,
    )


def _crashed(name: str, exc: Exception, started_at: float, ctx: ToolContext, *, retryable: bool) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError.from_exception(exc, error_type="execution", is_retryable=retryable),
        started_at=started_at, completed_at=time.time(), tool_name=name, call_id=ctx.call_id,
    )


def _refused_write(
    name: str, exc: Any, project_id: str | None, seen: bool, started_at: float, ctx: ToolContext
) -> ToolResult:
    """The host's refusal (``RecordWriteRefused``) as the tool's answer. A project the person could
    read a moment ago that the writer could not change is ``no_access``, in the manager's words."""
    error_type, message = exc.error_type, exc.message
    if error_type == "not_found" and seen and project_id:
        error_type = "no_access"
        message = f"You can view project {project_id} but you do not have permission to change it."
    return _refused(name, error_type, message, started_at, ctx, suggested_action=exc.suggested_action)


def _manager() -> Any:
    from matrx_ai.db.content_types.projects import projects_manager_instance

    return projects_manager_instance


def _tasks_manager() -> Any:
    from matrx_ai.db.content_types.tasks import tasks_manager_instance

    return tasks_manager_instance


def _acts_as_the_person(tool_name: str):
    return acts_as_the_person(tool_name, subject="your projects")


@_acts_as_the_person("project_list")
async def project_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Every project the person can reach across their organizations (never filtered by the active one)."""
    started_at = time.time()
    try:
        from matrx_ai.tools.output_caps import TOOL_LIST_DEFAULT_LIMIT, cap_list

        result = await _manager().list_projects()
        if not result.get("success"):
            return _failed("project_list", result, "Failed to list projects.", started_at, ctx)
        rows = [
            {k: p.get(k) for k in ("id", "name", "status", "priority", "target_date", "organization_id")}
            for p in result.get("projects", [])
        ]
        rows, info = cap_list(rows, limit=TOOL_LIST_DEFAULT_LIMIT)
        output: dict[str, Any] = {"projects": rows, "count": info.total, "shown": info.shown}
        if info.truncated:
            output["truncated"] = True
        return _done(output, "project_list", started_at, ctx, output_self_capped=True)
    except Exception as e:
        return _crashed("project_list", e, started_at, ctx, retryable=True)


@_acts_as_the_person("project_get")
async def project_get(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The full project plus its tasks as planner rows (id, title, status, priority, due date and time, parent)."""
    started_at = time.time()
    project_id = (args.get("project_id") or "").strip()
    if not project_id:
        return _refused("project_get", "validation", "project_id is required.", started_at, ctx)
    try:
        result = await _manager().get_project(project_id)
        if not result.get("success"):
            return _failed("project_get", result, f"Project {project_id} could not be read.", started_at, ctx)
        output = dict(result["project"])
        tasks = await _tasks_manager().list_tasks_for_project(project_id)
        if tasks.get("success"):
            from matrx_ai.tools.implementations.tasks import _compact_task
            from matrx_ai.tools.output_caps import TOOL_LIST_DEFAULT_LIMIT, cap_list

            # The same planner row task.list answers with — due time included (a field a task write accepts
            # is shown back wherever the task is read).
            rows = [_compact_task(t) for t in tasks.get("tasks", [])]
            rows, info = cap_list(rows, limit=TOOL_LIST_DEFAULT_LIMIT)
            output["tasks"] = rows
            output["task_count"] = info.total
        return _done(output, "project_get", started_at, ctx)
    except Exception as e:
        return _crashed("project_get", e, started_at, ctx, retryable=True)


def _project_record(p: dict[str, Any]) -> dict[str, Any]:
    """Every field a project write accepts, read back from the saved row (a tool that accepts a field shows it back)."""

    def iso(v: Any) -> Any:
        return v.isoformat() if hasattr(v, "isoformat") else v

    return {
        "id": p["id"],
        "name": p["name"],
        "description": p.get("description"),
        "status": p.get("status"),
        "priority": p.get("priority"),
        "start_date": iso(p.get("start_date")),
        "target_date": iso(p.get("target_date")),
    }


@_acts_as_the_person("project_create")
async def project_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    name = (args.get("name") or "").strip()
    if not name:
        return _refused(
            "project_create", "validation", "name is required.", started_at, ctx,
            suggested_action="Call project with action='create' and name='<project name>'.",
        )
    from matrx_ai.tools.organization_hold import (
        carried_organization_id,
        organization_required_result,
    )

    organization_id = carried_organization_id(ctx)
    if not organization_id:
        return organization_required_result(
            what="create a project", tool_name="project_create", ctx=ctx, started_at=started_at
        )
    try:
        fields = {k: v for k, v in args.items() if k != "name"}
        from matrx_ai.tools.record_writer import RecordWriteRefused, host_record_writer

        writer = host_record_writer()
        if writer is None:
            # A CLIENT host has no record Action: the manager writes the row as before.
            result = await _manager().create_project(
                ctx.user_id, name, organization_id=organization_id, **fields
            )
        else:
            # THE RECORD ACTION (project.create): the project's rules run and the write is one
            # action run. The slug stays the manager's (unique within the organization).
            from matrx_ai.db.content_types._projects_impl import _slugify

            data = {
                "name": name,
                "slug": await _manager()._unique_slug(organization_id, _slugify(name)),
                **{k: v for k, v in fields.items() if v not in (None, "")},
            }
            try:
                row = await writer(
                    operation="create", noun="project", data=data, organization_id=organization_id
                )
            except RecordWriteRefused as exc:
                return _refused_write("project_create", exc, None, False, started_at, ctx)
            result = await _manager().get_project(str((row or {}).get("id")))
        if not result.get("success"):
            return _failed("project_create", result, "Failed to create project.", started_at, ctx)
        p = result["project"]
        return _done(
            {
                **_project_record(p),
                "organization_id": p.get("organization_id"),
                "created_at": p.get("created_at"),
                # Undo of a create is an archive: there is no earlier version to restore.
                "version": p.get("version"),
                "previous_version": None,
            },
            "project_create", started_at, ctx,
        )
    except Exception as e:
        return _crashed("project_create", e, started_at, ctx, retryable=False)


@_acts_as_the_person("project_update")
async def project_update(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    project_id = (args.get("project_id") or "").strip()
    if not project_id:
        return _refused("project_update", "validation", "project_id is required.", started_at, ctx)
    if is_resource_read_only(project_id):
        return _refused("project_update", "read_only", READ_ONLY_TOOL_MESSAGE, started_at, ctx)
    updates = {k: v for k, v in args.items() if k != "project_id"}
    if not updates:
        return _refused(
            "project_update", "validation", "At least one field to update is required.", started_at, ctx,
            suggested_action="Provide one or more of: name, description, status, priority, start_date, target_date.",
        )
    try:
        from matrx_ai.tools.record_writer import RecordWriteRefused, host_record_writer

        writer = host_record_writer()
        if writer is None:
            # A CLIENT host has no record Action: the manager writes the row as before.
            result = await _manager().update_project(project_id, **updates)
        else:
            # THE RECORD ACTION (project.update), one action run; the prior read answers
            # not_found for a project this person cannot see, exactly as the manager did.
            seen = await _manager().get_project(project_id)
            if not seen.get("success"):
                return _failed("project_update", seen, f"Project {project_id} was not updated.", started_at, ctx)
            try:
                await writer(operation="update", noun="project", data={**updates, "id": project_id})
            except RecordWriteRefused as exc:
                return _refused_write("project_update", exc, project_id, True, started_at, ctx)
            after = await _manager().get_project(project_id)
            result = {**after, "prior": seen["project"]} if after.get("success") else after
        if not result.get("success"):
            return _failed("project_update", result, f"Project {project_id} was not updated.", started_at, ctx)
        p, prior = result["project"], result.get("prior") or {}
        return _done(
            {
                **_project_record(p),
                "updated_at": p.get("updated_at"),
                # UNDO: platform.version_restore('project', id, previous_version); `previous` = old values.
                "version": p.get("version"),
                "previous_version": prior.get("version"),
                "previous": {k: prior.get(k) for k in updates if k in prior and prior.get(k) != p.get(k)},
            },
            "project_update", started_at, ctx,
        )
    except Exception as e:
        return _crashed("project_update", e, started_at, ctx, retryable=True)


async def project(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        parsed = ProjectArgs.model_validate(args).root
    except ValidationError as exc:
        return ToolResult(
            success=False,
            error=ToolError.declared("validation", format_args_error(exc), exc=exc),
            started_at=started_at, completed_at=time.time(), tool_name="project", call_id=ctx.call_id,
        )
    impl = {
        "list": project_list,
        "get": project_get,
        "create": project_create,
        "update": project_update,
    }[parsed.action]
    result = await impl(parsed.model_dump(exclude={"action"}, exclude_unset=True), ctx)
    result.tool_name = "project"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result
