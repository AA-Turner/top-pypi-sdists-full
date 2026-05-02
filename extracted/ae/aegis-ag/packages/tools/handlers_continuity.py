"""Continuity-native built-in tool handlers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from packages.contracts.runtime import ExecutionResult, GoalNode
from packages.cron import CronRuntime
from packages.operator import (
    MemoryOperatorDetail,
    MemorySearchHit,
    ProcedureOperatorDetail,
    build_memory_operator_surface,
    render_activity_lines,
    render_memory_lines,
    render_procedure_lines,
    render_profile_lines,
)
from .handler_support import (
    coerce_bool,
    coerce_int,
    optional_string,
    tool_summary,
    truncate,
)
from .runtime import ToolInvocation
from .surfaces import (
    ActivityManagementSurface,
    MemoryManagementSurface,
    ProcedureManagementSurface,
    ProfileManagementSurface,
    RecallSearchSurface,
    TodoItem,
    TodoStore,
)


def run_profile_action(
    invocation: ToolInvocation,
    *,
    surface: ProfileManagementSurface | None,
) -> Mapping[str, Any]:
    if surface is None:
        raise RuntimeError("profile management is not configured for this runtime")
    action = str(invocation.arguments.get("action") or "inspect").strip().lower() or "inspect"
    session_id = invocation.session_id
    if action in {"inspect", "show", "get"}:
        profile_surface = surface.inspect_profile_surface(session_id)
        return tool_summary(
            invocation,
            "\n".join(render_profile_lines(profile_surface)),
            side_effects=("profile", "inspect"),
        )
    if action not in {"patch", "update", "set"}:
        raise ValueError(f"tool.profile.manage does not support action={action!r}")
    payload = {
        key: value
        for key, value in invocation.arguments.items()
        if key != "action"
    }
    if not payload:
        raise ValueError("tool.profile.manage patch requires at least one profile field")
    profile_surface = surface.patch_profile_surface(session_id, payload)
    return tool_summary(
        invocation,
        "\n".join(render_profile_lines(profile_surface)),
        side_effects=("profile", "update"),
    )


def run_activity_action(
    invocation: ToolInvocation,
    *,
    surface: ActivityManagementSurface | None,
) -> Mapping[str, Any]:
    if surface is None:
        raise RuntimeError("activity management is not configured for this runtime")
    raw_action = optional_string(invocation.arguments.get("action"))
    goal_id = optional_string(invocation.arguments.get("goal_id"))
    title = optional_string(invocation.arguments.get("title"))
    parent_goal_id = optional_string(invocation.arguments.get("parent_goal_id"))
    action = (raw_action or "").lower()
    if not action:
        if title is not None or parent_goal_id is not None:
            action = "create"
        elif goal_id is not None:
            action = "inspect"
        else:
            action = "list"
    session_id = invocation.session_id
    if action in {"list", "ls", "show"}:
        activity_surface = surface.inspect_activity_surface(session_id)
        return tool_summary(
            invocation,
            "\n".join(render_activity_lines(activity_surface)),
            side_effects=("activity", "inspect"),
        )
    if action == "inspect":
        if goal_id is None:
            raise ValueError("tool.activity.manage inspect requires 'goal_id'")
        goal = surface.inspect_goal(session_id, goal_id)
        return tool_summary(
            invocation,
            "\n".join(_goal_detail_lines(goal)),
            side_effects=("activity", "inspect"),
        )
    if action == "create":
        if title is None:
            raise ValueError("tool.activity.manage create requires 'title'")
        activate_arg = invocation.arguments.get("activate")
        created = surface.create_goal(
            session_id,
            title=title,
            status=str(invocation.arguments.get("status") or "active"),
            priority=str(invocation.arguments.get("priority") or "medium"),
            owner=str(invocation.arguments.get("owner") or "shared"),
            parent_goal_id=parent_goal_id or goal_id,
            dependency_refs=invocation.arguments.get("dependency_refs") or invocation.arguments.get("dependencies"),
            evidence_refs=invocation.arguments.get("evidence_refs"),
            related_memory_ids=invocation.arguments.get("related_memory_ids"),
            review_checkpoint=optional_string(invocation.arguments.get("review_checkpoint")),
            deadline=invocation.arguments.get("deadline"),
            time_sensitivity=optional_string(invocation.arguments.get("time_sensitivity")),
            reason=optional_string(invocation.arguments.get("reason")),
            activate=None if activate_arg is None else coerce_bool(activate_arg, default=False),
        )
        return tool_summary(
            invocation,
            "\n".join(["Created durable activity item", *_goal_detail_lines(created)]),
            side_effects=("activity", "create"),
        )
    if action in {"focus", "activate"}:
        if goal_id is None:
            raise ValueError("tool.activity.manage focus requires 'goal_id'")
        _, updated, reason = surface.update_goal(
            session_id,
            goal_id,
            status="active",
            reason=str(invocation.arguments.get("reason") or "focused from tool.activity.manage"),
        )
        return tool_summary(
            invocation,
            "\n".join(["Focused durable activity item", f"reason: {reason}", *_goal_detail_lines(updated)]),
            side_effects=("activity", "focus"),
        )
    if action == "update":
        if goal_id is None:
            raise ValueError("tool.activity.manage update requires 'goal_id'")
        _, updated, reason = surface.update_goal(
            session_id,
            goal_id,
            title=title,
            status=optional_string(invocation.arguments.get("status")),
            priority=optional_string(invocation.arguments.get("priority")),
            reason=optional_string(invocation.arguments.get("reason")),
        )
        return tool_summary(
            invocation,
            "\n".join(["Updated durable activity item", f"reason: {reason}", *_goal_detail_lines(updated)]),
            side_effects=("activity", "update"),
        )
    if action in {"drop", "delete"}:
        if goal_id is None:
            raise ValueError(f"tool.activity.manage {action} requires 'goal_id'")
        _, updated = surface.delete_goal(
            session_id,
            goal_id,
            reason=str(invocation.arguments.get("reason") or "dropped from tool.activity.manage"),
        )
        return tool_summary(
            invocation,
            "\n".join(["Dropped durable activity item", *_goal_detail_lines(updated)]),
            side_effects=("activity", "delete"),
        )
    raise ValueError(f"tool.activity.manage does not support action={action!r}")


def run_memory_recall(
    invocation: ToolInvocation,
    *,
    memory_surface: MemoryManagementSurface | None,
    recall_surface: RecallSearchSurface | None,
) -> Mapping[str, Any]:
    if memory_surface is None:
        raise RuntimeError("memory recall is not configured for this runtime")
    raw_action = optional_string(invocation.arguments.get("action"))
    memory_id = optional_string(invocation.arguments.get("memory_id"))
    query = optional_string(invocation.arguments.get("query"))
    action = (raw_action or "").lower()
    if not action:
        if query:
            action = "search"
        elif memory_id:
            action = "inspect"
        else:
            action = "list"
    session_id = invocation.session_id
    memories = tuple(
        MemoryOperatorDetail(
            memory=record,
            state=memory_surface.memory_state(record.memory_id),
            lineage=memory_surface.memory_lineage(record.memory_id),
        )
        for record in memory_surface.inspect_memories(session_id)
    )
    if action in {"list", "ls", "show"}:
        surface = build_memory_operator_surface(session_id=session_id, memories=memories)
        return tool_summary(
            invocation,
            "\n".join(render_memory_lines(surface)),
            side_effects=("memory", "inspect"),
        )
    if action == "inspect":
        if memory_id is None:
            raise ValueError("tool.memory.recall inspect requires 'memory_id'")
        record = memory_surface.inspect_memory(session_id, memory_id)
        detail = MemoryOperatorDetail(
            memory=record,
            state=memory_surface.memory_state(record.memory_id),
            lineage=memory_surface.memory_lineage(record.memory_id),
        )
        surface = build_memory_operator_surface(
            session_id=session_id,
            memories=(detail,),
        )
        return tool_summary(
            invocation,
            "\n".join(render_memory_lines(surface)),
            side_effects=("memory", "inspect"),
        )
    if action == "lineage":
        if memory_id is None:
            raise ValueError("tool.memory.recall lineage requires 'memory_id'")
        lineage = memory_surface.memory_lineage(memory_id)
        state = memory_surface.memory_state(memory_id) or "unknown"
        return tool_summary(
            invocation,
            f"memory_id: {memory_id}\nstate: {state}\nlineage: {lineage or '<none>'}",
            side_effects=("memory", "inspect"),
        )
    if action == "search":
        if recall_surface is None:
            raise RuntimeError("memory search is not configured for this runtime")
        if not query:
            raise ValueError("tool.memory.recall search requires 'query'")
        limit = max(1, min(coerce_int(invocation.arguments.get("limit"), default=5), 20))
        retrieval = recall_surface.recall(session_id, query, limit=limit)
        surface = build_memory_operator_surface(
            session_id=session_id,
            memories=memories,
            search_query=query,
            search_hits=tuple(
                MemorySearchHit(
                    memory=candidate.memory,
                    score=candidate.score,
                    reasons=tuple(reason.detail for reason in candidate.reasons if reason.detail),
                )
                for candidate in retrieval.candidates
            ),
            scope_reason=retrieval.scope_reason,
            index_policy=retrieval.index_policy,
        )
        return tool_summary(
            invocation,
            "\n".join(render_memory_lines(surface)),
            side_effects=("recall", "search"),
        )
    raise ValueError(f"tool.memory.recall does not support action={action!r}")


def run_memory_upload(
    invocation: ToolInvocation,
    *,
    surface: MemoryManagementSurface | None,
) -> Mapping[str, Any]:
    if surface is None:
        raise RuntimeError("memory upload is not configured for this runtime")
    action = str(invocation.arguments.get("action") or "").strip().lower()
    if not action:
        raise ValueError("tool.memory.upload requires an 'action' argument")
    session_id = invocation.session_id
    memory_id = optional_string(invocation.arguments.get("memory_id"))
    if memory_id is None:
        raise ValueError(f"tool.memory.upload action={action!r} requires 'memory_id'")
    if action == "correct":
        corrected_content = str(
            invocation.arguments.get("content") or invocation.arguments.get("corrected_content") or ""
        ).strip()
        if not corrected_content:
            raise ValueError("tool.memory.upload correct requires 'content'")
        original, corrected, reason, lineage = surface.correct_memory(
            session_id,
            memory_id,
            corrected_content=corrected_content,
            reason=str(invocation.arguments.get("reason") or ""),
        )
        original_id = original.memory_id if original is not None else "<missing>"
        corrected_id = corrected.memory_id if corrected is not None else "<missing>"
        return tool_summary(
            invocation,
            "\n".join(
                [
                    f"original: {original_id}",
                    f"corrected: {corrected_id}",
                    f"reason: {reason}",
                    f"lineage: {lineage or '<none>'}",
                ]
            ),
            side_effects=("memory", "correction"),
        )
    if action == "delete":
        original, reason = surface.delete_memory(
            session_id,
            memory_id,
            reason=str(invocation.arguments.get("reason") or ""),
        )
        return tool_summary(
            invocation,
            f"deleted: {original.memory_id}\nreason: {reason or '<none>'}",
            side_effects=("memory", "deletion"),
        )
    if action == "pin":
        record, reason = surface.pin_memory(
            session_id,
            memory_id,
            reason=str(invocation.arguments.get("reason") or ""),
        )
        return tool_summary(
            invocation,
            f"pinned: {record.memory_id}\nreason: {reason}",
            side_effects=("memory", "pin"),
        )
    if action == "unpin":
        record, reason = surface.unpin_memory(
            session_id,
            memory_id,
            reason=str(invocation.arguments.get("reason") or ""),
        )
        return tool_summary(
            invocation,
            f"unpinned: {record.memory_id}\nreason: {reason}",
            side_effects=("memory", "pin"),
        )
    raise ValueError(f"tool.memory.upload does not support action={action!r}")


def run_procedure_inspect(
    invocation: ToolInvocation,
    *,
    surface: ProcedureManagementSurface | None,
) -> Mapping[str, Any]:
    if surface is None:
        raise RuntimeError("procedure inspection is not configured for this runtime")
    action = str(invocation.arguments.get("action") or "list").strip().lower() or "list"
    session_id = invocation.session_id
    procedure_id = optional_string(invocation.arguments.get("procedure_id"))
    minimum_support = max(1, min(coerce_int(invocation.arguments.get("minimum_support"), default=2), 20))
    if action in {"list", "ls", "show"} and procedure_id is None:
        procedure_surface = surface.inspect_procedure_surface(
            session_id,
            minimum_support=minimum_support,
        )
        return tool_summary(
            invocation,
            "\n".join(render_procedure_lines(procedure_surface)),
            side_effects=("procedure", "inspect"),
        )
    if action != "inspect":
        raise ValueError(f"tool.procedure.inspect does not support action={action!r}")
    if procedure_id is None:
        raise ValueError("tool.procedure.inspect inspect requires 'procedure_id'")
    detail = surface.inspect_procedure_detail(session_id, procedure_id)
    return tool_summary(
        invocation,
        "\n".join(_procedure_detail_lines(detail)),
        side_effects=("procedure", "inspect"),
    )


def run_procedure_manage(
    invocation: ToolInvocation,
    *,
    surface: ProcedureManagementSurface | None,
) -> Mapping[str, Any]:
    if surface is None:
        raise RuntimeError("procedure management is not configured for this runtime")
    action = str(invocation.arguments.get("action") or "").strip().lower()
    if not action:
        raise ValueError("tool.procedure.manage requires an 'action' argument")
    session_id = invocation.session_id
    procedure_id = optional_string(invocation.arguments.get("procedure_id"))
    if procedure_id is None:
        raise ValueError(f"tool.procedure.manage action={action!r} requires 'procedure_id'")
    if action in {"patch", "update"}:
        payload = {
            key: value
            for key, value in invocation.arguments.items()
            if key not in {"action", "procedure_id"}
        }
        if "status" in payload:
            payload["status"] = _normalize_procedure_status(payload.get("status"))
        if not payload:
            raise ValueError("tool.procedure.manage patch requires at least one mutable field")
        detail = surface.patch_procedure_surface(session_id, procedure_id, payload)
        return tool_summary(
            invocation,
            "\n".join(_procedure_detail_lines(detail)),
            side_effects=("procedure", "update"),
        )
    if action == "retire":
        detail = surface.retire_procedure_surface(session_id, procedure_id)
        return tool_summary(
            invocation,
            "\n".join(_procedure_detail_lines(detail)),
            side_effects=("procedure", "retire"),
        )
    raise ValueError(f"tool.procedure.manage does not support action={action!r}")


def _normalize_procedure_status(value: object) -> str:
    normalized = str(value or "").strip().lower()
    return normalized if normalized in {"active", "promoted", "verified", "retired"} else "active"


def _normalize_todo_status(value: object, *, default: str = "open") -> str:
    normalized = str(value or "").strip().lower()
    return normalized if normalized in {"open", "done", "promoted"} else default


def run_todo_action(
    invocation: ToolInvocation,
    *,
    store: TodoStore,
    goal_surface: ActivityManagementSurface | None,
) -> Mapping[str, Any]:
    action = str(invocation.arguments.get("action") or "").strip().lower()
    if not action:
        raise ValueError("tool.todo.manage requires an 'action' argument")
    session_id = invocation.session_id
    if action in {"list", "ls"}:
        items = store.list_items(session_id)
        lines = [_todo_line(item) for item in items] or ["<empty>"]
        return tool_summary(invocation, "\n".join(lines), side_effects=("todo", "scratchpad"))
    if action in {"add", "create"}:
        title = str(invocation.arguments.get("title") or "").strip()
        if not title:
            raise ValueError("tool.todo.manage create requires 'title'")
        item = store.upsert_item(
            session_id,
            title=title,
            status=_normalize_todo_status(invocation.arguments.get("status")),
            notes=str(invocation.arguments.get("notes") or ""),
        )
        return tool_summary(invocation, f"created: {_todo_line(item)}", side_effects=("todo", "scratchpad"))
    if action == "clear":
        removed = store.clear(session_id)
        return tool_summary(invocation, f"cleared: {removed}", side_effects=("todo", "scratchpad"))
    item_id = optional_string(invocation.arguments.get("item_id"))
    if item_id is None:
        raise ValueError(f"tool.todo.manage action={action!r} requires 'item_id'")
    if action == "inspect":
        item = store.inspect_item(session_id, item_id)
        return tool_summary(
            invocation,
            "\n".join([_todo_line(item), f"notes: {item.notes or '<none>'}"]),
            side_effects=("todo", "scratchpad"),
        )
    if action in {"update", "complete", "reopen"}:
        current = store.inspect_item(session_id, item_id)
        status = {
            "complete": "done",
            "reopen": "open",
        }.get(action, _normalize_todo_status(invocation.arguments.get("status"), default=current.status))
        item = store.upsert_item(
            session_id,
            item_id=item_id,
            title=optional_string(invocation.arguments.get("title")) or current.title,
            status=status,
            notes=optional_string(invocation.arguments.get("notes")) or current.notes,
            goal_id=current.goal_id,
        )
        return tool_summary(invocation, f"updated: {_todo_line(item)}", side_effects=("todo", "scratchpad"))
    if action in {"remove", "delete"}:
        removed = store.remove_item(session_id, item_id)
        return tool_summary(invocation, f"removed: {_todo_line(removed)}", side_effects=("todo", "scratchpad"))
    if action == "promote":
        if goal_surface is None:
            raise RuntimeError("todo promotion requires configured goal management")
        current = store.inspect_item(session_id, item_id)
        goal = goal_surface.create_goal(
            session_id,
            title=current.title,
            priority="medium",
            reason=current.notes or "promoted from todo scratchpad",
        )
        updated = store.upsert_item(
            session_id,
            item_id=item_id,
            title=current.title,
            status="promoted",
            notes=current.notes,
            goal_id=goal.goal_id,
        )
        return tool_summary(
            invocation,
            f"promoted: {_todo_line(updated)} -> {_goal_line(goal)}",
            side_effects=("todo", "goal"),
        )
    raise ValueError(f"tool.todo.manage does not support action={action!r}")


def run_cron_action(invocation: ToolInvocation, *, runtime: CronRuntime | None) -> ExecutionResult:
    if runtime is None:
        raise RuntimeError("cron runtime is not configured")
    action = str(invocation.arguments.get("action") or "").strip().lower()
    if not action:
        raise ValueError("tool.cron.manage requires an 'action' argument")
    if action in {"list", "ls"}:
        jobs = runtime.list_jobs(
            profile_id=optional_string(invocation.arguments.get("profile_id")),
            clone_id=optional_string(invocation.arguments.get("clone_id")),
        )
        summary = "\n".join(
            f"{job.job_id} | {job.status} | {job.name} | {job.schedule_text} | {job.action_kind}"
            for job in jobs
        ) or "<empty>"
        return ExecutionResult(
            execution_id=invocation.invocation_id,
            session_id=invocation.session_id,
            outcome="success",
            summary=summary,
            side_effects=("cron", "automation"),
        )
    if action == "create":
        name = optional_string(invocation.arguments.get("name")) or "Aegis job"
        schedule = optional_string(invocation.arguments.get("schedule"))
        job_kind = optional_string(invocation.arguments.get("job_kind"))
        if not schedule or not job_kind:
            raise ValueError("cron create requires 'schedule' and 'job_kind'")
        payload = {
            key: value
            for key, value in (
                ("message", optional_string(invocation.arguments.get("message"))),
                ("query", optional_string(invocation.arguments.get("query"))),
                ("prompt", optional_string(invocation.arguments.get("prompt"))),
            )
            if value is not None
        }
        skills = _string_list(invocation.arguments.get("skills"))
        if skills:
            payload["skills"] = list(skills)
        job = runtime.create_job(
            name=name,
            schedule_text=schedule,
            action_kind=job_kind,
            payload=payload,
            profile_id=optional_string(invocation.arguments.get("profile_id")),
            clone_id=optional_string(invocation.arguments.get("clone_id")),
        )
        return ExecutionResult(
            execution_id=invocation.invocation_id,
            session_id=invocation.session_id,
            outcome="success",
            summary=(
                f"created {job.job_id}\n"
                f"name: {job.name}\n"
                f"schedule: {job.schedule_text}\n"
                f"job_kind: {job.action_kind}\n"
                f"skills: {', '.join(skills) if skills else '<none>'}\n"
                f"next_run_at: {job.next_run_at.isoformat() if job.next_run_at is not None else '<none>'}"
            ),
            side_effects=("cron", "automation"),
        )
    job_id = optional_string(invocation.arguments.get("job_id"))
    if not job_id:
        raise ValueError(f"cron action '{action}' requires 'job_id'")
    if action == "inspect":
        job = runtime.inspect_job(job_id)
        return ExecutionResult(
            execution_id=invocation.invocation_id,
            session_id=invocation.session_id,
            outcome="success",
            summary=(
                f"{job.job_id}\n"
                f"name: {job.name}\n"
                f"status: {job.status}\n"
                f"schedule: {job.schedule_text}\n"
                f"job_kind: {job.action_kind}\n"
                f"skills: {', '.join(_string_list(job.payload.get('skills'))) or '<none>'}\n"
                f"next_run_at: {job.next_run_at.isoformat() if job.next_run_at is not None else '<none>'}\n"
                f"last_summary: {job.last_summary or '<none>'}"
            ),
            side_effects=("cron", "automation"),
        )
    if action == "pause":
        job = runtime.pause_job(job_id)
        summary = f"{job.job_id}\nstatus: {job.status}"
    elif action == "resume":
        job = runtime.resume_job(job_id)
        summary = (
            f"{job.job_id}\nstatus: {job.status}\n"
            f"next_run_at: {job.next_run_at.isoformat() if job.next_run_at is not None else '<none>'}"
        )
    elif action in {"remove", "delete"}:
        job = runtime.remove_job(job_id)
        summary = f"{job.job_id}\nstatus: removed"
    else:
        raise ValueError(f"unsupported cron action: {action}")
    return ExecutionResult(
        execution_id=invocation.invocation_id,
        session_id=invocation.session_id,
        outcome="success",
        summary=summary,
        side_effects=("cron", "automation"),
    )


def _string_list(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        raw_items = value.replace("\n", ",").split(",")
    elif isinstance(value, (list, tuple)):
        raw_items = [str(item) for item in value]
    else:
        raw_items = [str(value)]
    normalized = tuple(item.strip() for item in raw_items if item.strip())
    return tuple(dict.fromkeys(normalized))


def _goal_line(goal: GoalNode) -> str:
    parent_part = f" | parent={goal.parent_goal_id}" if goal.parent_goal_id else ""
    return f"{goal.goal_id} | {goal.status} | {goal.priority} | {goal.title}{parent_part}"


def _goal_detail_lines(goal: GoalNode) -> list[str]:
    return [
        f"goal_id: {goal.goal_id}",
        f"title: {goal.title}",
        f"status: {goal.status}",
        f"priority: {goal.priority}",
        f"owner: {goal.owner or '<empty>'}",
        f"parent_goal_id: {goal.parent_goal_id or '<empty>'}",
        f"dependencies: {', '.join(goal.dependencies) or '<empty>'}",
        f"evidence_refs: {', '.join(goal.evidence_refs) or '<empty>'}",
    ]


def _procedure_detail_lines(detail: ProcedureOperatorDetail) -> list[str]:
    procedure = detail.procedure
    verification = detail.verification
    return [
        f"procedure_id: {procedure.procedure_id}",
        f"title: {procedure.title}",
        f"status: {procedure.status}",
        f"summary: {procedure.summary or '<empty>'}",
        f"trigger_refs: {', '.join(procedure.trigger_refs) or '<empty>'}",
        f"verification_bundle_id: {procedure.verification_bundle_id or '<empty>'}",
        f"verification_status: {verification.status if verification is not None else '<none>'}",
    ]


def _todo_line(item: TodoItem) -> str:
    goal_part = f" | goal={item.goal_id}" if item.goal_id else ""
    return f"{item.item_id} | {item.status} | {item.title}{goal_part}"


__all__ = [
    "run_activity_action",
    "run_cron_action",
    "run_memory_recall",
    "run_memory_upload",
    "run_procedure_inspect",
    "run_procedure_manage",
    "run_profile_action",
    "run_todo_action",
]
