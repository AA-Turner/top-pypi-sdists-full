"""Prompt composers for scheduled and delegated CLI runtime turns."""

from __future__ import annotations

from collections.abc import Mapping
from concurrent.futures import Future, ThreadPoolExecutor, as_completed, wait
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
import traceback
from typing import Any
from uuid import uuid4

from packages.contracts.runtime import ExecutionResult
from packages.cron import CronJob
from packages.tools.runtime import ToolInvocation, ToolLifecycleEvent


@dataclass(slots=True)
class _AsyncSubAgentRun:
    run_id: str
    parent_session_id: str
    tasks: tuple[Mapping[str, Any], ...]
    max_concurrency: int
    created_at: datetime
    results: list[Mapping[str, Any] | None]
    futures: tuple[Future, ...] = ()
    executor: ThreadPoolExecutor | None = None
    status: str = "running"
    completed_at: datetime | None = None
    lock: Lock = field(default_factory=Lock)


_ASYNC_SUB_AGENT_RUNS: dict[str, _AsyncSubAgentRun] = {}
_ASYNC_SUB_AGENT_RUNS_LOCK = Lock()


def cron_skill_ids(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        raw_items = value.replace("\n", ",").split(",")
    elif isinstance(value, Mapping):
        raw_items = [str(key) for key, enabled in value.items() if enabled]
    elif isinstance(value, (list, tuple)):
        raw_items = [str(item) for item in value]
    else:
        raw_items = [str(value)]
    return tuple(dict.fromkeys(item.strip() for item in raw_items if item.strip()))


def compose_cron_prompt(runtime: Any, job: CronJob, *, user_prompt: str, session_id: str) -> str:
    skill_sections = _skill_sections(runtime, cron_skill_ids(job.payload.get("skills")), session_id=session_id)
    sections = [
        "[SYSTEM: This turn is running as a scheduled Aegis cron job.]",
        "The scheduler will surface the final response; do not call tool.message.send from this job.",
        "The user may not be present, so avoid interactive clarification and make conservative assumptions.",
        "If there is no useful update, respond exactly [SILENT].",
        "",
        f"Cron job: {job.name} ({job.job_id})",
        f"Schedule: {job.schedule_text}",
    ]
    if skill_sections:
        sections.extend(["", "Scheduled skill references:", "\n\n".join(skill_sections)])
    sections.extend(["", f"Scheduled task:\n{user_prompt}"])
    return "\n".join(sections).strip()


def run_sub_agent_task(
    runtime: Any,
    *,
    session_id: str,
    task: str,
    name: str | None = None,
    skills: tuple[str, ...] = (),
) -> Mapping[str, Any]:
    result = run_sub_agent_tasks(
        runtime,
        session_id=session_id,
        tasks=({"task": task, "name": name, "skills": skills},),
        max_concurrency=1,
    )
    results = tuple(result.get("results") or ())
    if not results:
        return {
            "name": name or "sub-agent",
            "summary": "sub-agent did not return a result",
            "skills": list(skills),
            "status": "failed",
        }
    return results[0]


def run_sub_agent_tasks(
    runtime: Any,
    *,
    session_id: str,
    tasks: tuple[Mapping[str, Any], ...],
    max_concurrency: int = 3,
) -> Mapping[str, Any]:
    if runtime.sub_agent_active:
        raise RuntimeError("nested sub-agent delegation is not allowed")
    normalized = tuple(_normalize_sub_agent_task(item) for item in tasks)
    if not normalized:
        raise ValueError("tool.sub_agents requires at least one task")
    workers = max(1, min(int(max_concurrency or 1), len(normalized), 3))
    prepared = tuple(
        _prepare_sub_agent_child(
            runtime,
            parent_session_id=session_id,
            task=item["task"],
            name=item.get("name"),
            skills=tuple(item.get("skills") or ()),
        )
        for item in normalized
    )
    results: list[Mapping[str, Any] | None] = [None] * len(normalized)
    object.__setattr__(runtime, "sub_agent_active", True)
    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    _run_prepared_sub_agent_child,
                    runtime,
                    prepared_child=item,
                ): index
                for index, item in enumerate(prepared)
            }
            for future in as_completed(futures):
                index = futures[future]
                results[index] = future.result()
    finally:
        object.__setattr__(runtime, "sub_agent_active", False)
    resolved = tuple(item for item in results if item is not None)
    status = _aggregate_sub_agent_status(results)
    summary = "\n".join(
        f"{index + 1}. {item.get('name') or 'sub-agent'}: {item.get('summary') or item.get('status') or 'finished'}"
        for index, item in enumerate(resolved)
    )
    return {
        "summary": summary or "sub-agent pool finished",
        "results": list(resolved),
        "max_concurrency": workers,
        "status": status,
    }


def start_sub_agent_tasks(
    runtime: Any,
    *,
    session_id: str,
    tasks: tuple[Mapping[str, Any], ...],
    max_concurrency: int = 3,
) -> Mapping[str, Any]:
    if runtime.sub_agent_active:
        raise RuntimeError("nested sub-agent delegation is not allowed")
    normalized = tuple(_normalize_sub_agent_task(item) for item in tasks)
    if not normalized:
        raise ValueError("tool.sub_agents requires at least one task")
    workers = max(1, min(int(max_concurrency or 1), len(normalized), 3))
    prepared = tuple(
        _prepare_sub_agent_child(
            runtime,
            parent_session_id=session_id,
            task=item["task"],
            name=item.get("name"),
            skills=tuple(item.get("skills") or ()),
        )
        for item in normalized
    )
    run_id = f"subrun-{uuid4().hex[:12]}"
    executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix=f"aegis-subagents-{run_id[-6:]}")
    run = _AsyncSubAgentRun(
        run_id=run_id,
        parent_session_id=session_id,
        tasks=normalized,
        max_concurrency=workers,
        created_at=datetime.now(timezone.utc),
        results=[None] * len(normalized),
        executor=executor,
    )
    futures: list[Future] = []
    for index, item in enumerate(prepared):
        future = executor.submit(
            _run_prepared_sub_agent_child,
            runtime,
            prepared_child=item,
            run_id=run_id,
            task_index=index,
        )
        future.add_done_callback(lambda completed, task_index=index: _record_async_sub_agent_result(run, task_index, completed))
        futures.append(future)
    run.futures = tuple(futures)
    with _ASYNC_SUB_AGENT_RUNS_LOCK:
        _ASYNC_SUB_AGENT_RUNS[run_id] = run
    return _sub_agent_run_payload(run)


def inspect_sub_agent_run(
    runtime: Any,
    *,
    session_id: str,
    run_id: str,
    wait_timeout_seconds: float | None = None,
) -> Mapping[str, Any]:
    del runtime
    run = _get_async_sub_agent_run(run_id)
    if run.parent_session_id != session_id:
        raise KeyError(f"sub-agent run is not attached to this session: {run_id}")
    if wait_timeout_seconds is not None:
        wait(run.futures, timeout=max(0.0, wait_timeout_seconds))
        _refresh_async_sub_agent_run(run)
    return _sub_agent_run_payload(run)


def list_sub_agent_runs(
    runtime: Any,
    *,
    session_id: str,
) -> Mapping[str, Any]:
    del runtime
    with _ASYNC_SUB_AGENT_RUNS_LOCK:
        runs = tuple(run for run in _ASYNC_SUB_AGENT_RUNS.values() if run.parent_session_id == session_id)
    return {
        "status": "completed",
        "summary": "\n".join(
            f"{run.run_id}: {run.status} ({_completed_sub_agent_count(run)}/{len(run.results)} done)"
            for run in runs
        )
        or "no sub-agent runs",
        "runs": [_sub_agent_run_payload(run) for run in runs],
    }


def _run_one_sub_agent_child(
    runtime: Any,
    *,
    parent_session_id: str,
    task: str,
    name: str | None,
    skills: tuple[str, ...],
) -> Mapping[str, Any]:
    prepared = _prepare_sub_agent_child(
        runtime,
        parent_session_id=parent_session_id,
        task=task,
        name=name,
        skills=skills,
    )
    return _run_prepared_sub_agent_child(runtime, prepared_child=prepared)


def _prepare_sub_agent_child(
    runtime: Any,
    *,
    parent_session_id: str,
    task: str,
    name: str | None,
    skills: tuple[str, ...],
) -> Mapping[str, Any]:
    resume_result = runtime.resume(parent_session_id)
    child_session_id = resume_result.session.session_id
    prompt = _compose_sub_agent_prompt(
        runtime,
        task=task,
        name=name,
        skills=skills,
        session_id=child_session_id,
    )
    return {
        "name": name or "sub-agent",
        "task": task,
        "prompt": prompt,
        "session_id": child_session_id,
        "skills": skills,
    }


def _run_prepared_sub_agent_child(
    runtime: Any,
    *,
    prepared_child: Mapping[str, Any],
    run_id: str | None = None,
    task_index: int | None = None,
) -> Mapping[str, Any]:
    child_session_id = str(prepared_child["session_id"])
    name = str(prepared_child.get("name") or "sub-agent")
    skills = tuple(str(item) for item in prepared_child.get("skills") or ())
    prompt = str(prepared_child.get("prompt") or "")
    started_at = datetime.now(timezone.utc)
    child_runtime = None
    unsubscribe = None
    _emit_sub_agent_event(
        runtime,
        prepared_child=prepared_child,
        phase="execution.started",
        detail=f"started sub-agent {name}",
        run_id=run_id,
        task_index=task_index,
        requested_at=started_at,
    )
    try:
        child_runtime = _create_child_runtime(runtime)
        object.__setattr__(child_runtime, "sub_agent_active", True)
        unsubscribe = _relay_child_tool_events(runtime, child_runtime)
        child_runtime.prepare_session_surface(child_session_id)
        outcome = child_runtime.explain_next_step(session_id=child_session_id, prompt=prompt)
        execution = outcome.execution
        status = "completed" if execution.outcome not in {"error", "failed"} else "failed"
        summary = _bounded_child_text(execution.summary)
        execution_id = execution.execution_id
        exit_code = 0 if status == "completed" else 1
        result_execution = execution
    except Exception as error:
        status = "failed"
        summary = _child_result_summary(
            {
                "summary": f"{type(error).__name__}: {error}",
                "status": status,
                "traceback": traceback.format_exc(limit=8),
            },
            output="",
            status=status,
        )
        execution_id = None
        exit_code = 1
        result_execution = ExecutionResult(
            execution_id=f"{child_session_id}:sub-agent",
            session_id=child_session_id,
            outcome="error",
            summary=summary,
            side_effects=("sub_agents", "delegation"),
        )
    finally:
        if unsubscribe is not None:
            unsubscribe()
        close = getattr(child_runtime, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass
    result = {
        "name": name,
        "summary": summary,
        "skills": list(skills),
        "session_id": child_session_id,
        "status": status,
        "exit_code": exit_code,
        "execution_id": execution_id,
    }
    _emit_sub_agent_event(
        runtime,
        prepared_child=prepared_child,
        phase="execution.completed" if status == "completed" else "execution.failed",
        detail=summary,
        run_id=run_id,
        task_index=task_index,
        requested_at=started_at,
        execution=result_execution,
        status=status,
    )
    return result


def _create_child_runtime(runtime: Any) -> Any:
    return runtime.__class__.create(
        state_dir=runtime.paths.state_dir,
        profile_dir=runtime.paths.profile_dir,
    )


def _relay_child_tool_events(parent_runtime: Any, child_runtime: Any):
    emitter = getattr(parent_runtime.tool_runtime, "_emit_event", None)
    subscribe = getattr(child_runtime.tool_runtime, "subscribe", None)
    if not callable(emitter) or not callable(subscribe):
        return None

    def _observer(event: Any) -> None:
        emitter(event)

    return subscribe(_observer)


def _normalize_sub_agent_task(item: Mapping[str, Any]) -> Mapping[str, Any]:
    task = str(item.get("task") or item.get("prompt") or "").strip()
    if not task:
        raise ValueError("sub-agent tasks require 'task'")
    name = item.get("name")
    name_text = None if name is None else str(name).strip() or None
    skills = cron_skill_ids(item.get("skills"))
    return {"task": task, "name": name_text, "skills": skills}


def _aggregate_sub_agent_status(results: list[Mapping[str, Any] | None]) -> str:
    if any(item is None for item in results):
        return "running"
    if any(str(item.get("status") or "").lower() not in {"completed", "success"} for item in results if item):
        return "failed"
    return "completed"


def _record_async_sub_agent_result(run: _AsyncSubAgentRun, index: int, future: Future) -> None:
    try:
        result = future.result()
    except Exception as error:
        result = {
            "name": f"sub-agent-{index + 1}",
            "summary": f"sub-agent failed:\n{type(error).__name__}: {error}",
            "status": "failed",
            "exit_code": 1,
            "execution_id": None,
        }
    with run.lock:
        run.results[index] = result
        run.status = _aggregate_sub_agent_status(run.results)
        if run.status != "running":
            run.completed_at = datetime.now(timezone.utc)
            executor = run.executor
            run.executor = None
        else:
            executor = None
    if executor is not None:
        executor.shutdown(wait=False)


def _refresh_async_sub_agent_run(run: _AsyncSubAgentRun) -> None:
    for index, future in enumerate(run.futures):
        with run.lock:
            known = run.results[index] is not None
        if known or not future.done():
            continue
        _record_async_sub_agent_result(run, index, future)


def _get_async_sub_agent_run(run_id: str) -> _AsyncSubAgentRun:
    with _ASYNC_SUB_AGENT_RUNS_LOCK:
        run = _ASYNC_SUB_AGENT_RUNS.get(run_id)
    if run is None:
        raise KeyError(f"unknown sub-agent run: {run_id}")
    return run


def _completed_sub_agent_count(run: _AsyncSubAgentRun) -> int:
    with run.lock:
        return sum(1 for item in run.results if item is not None)


def _sub_agent_run_payload(run: _AsyncSubAgentRun) -> Mapping[str, Any]:
    _refresh_async_sub_agent_run(run)
    with run.lock:
        results = list(run.results)
        status = run.status
        completed = sum(1 for item in results if item is not None)
    total = len(results)
    resolved = [item for item in results if item is not None]
    summary_lines = [
        f"sub_agent_run_id: {run.run_id}",
        f"status: {status}",
        f"progress: {completed}/{total}",
    ]
    if status == "running":
        summary_lines.append(f"Use tool.sub_agents action=status run_id={run.run_id} to check progress, or action=join to wait.")
    for index, item in enumerate(resolved):
        summary_lines.append(
            f"{index + 1}. {item.get('name') or 'sub-agent'}: {item.get('summary') or item.get('status') or 'finished'}"
        )
    return {
        "run_id": run.run_id,
        "status": status,
        "summary": "\n".join(summary_lines),
        "results": resolved,
        "max_concurrency": run.max_concurrency,
        "completed_count": completed,
        "total_count": total,
    }


def _emit_sub_agent_event(
    runtime: Any,
    *,
    prepared_child: Mapping[str, Any],
    phase: str,
    detail: str,
    run_id: str | None,
    task_index: int | None,
    requested_at: datetime,
    execution: ExecutionResult | None = None,
    status: str | None = None,
) -> None:
    emitter = getattr(runtime.tool_runtime, "_emit_event", None)
    if not callable(emitter):
        return
    child_session_id = str(prepared_child.get("session_id") or "")
    task = str(prepared_child.get("task") or "")
    name = str(prepared_child.get("name") or "sub-agent")
    invocation = ToolInvocation(
        invocation_id=f"{child_session_id}:tool.sub_agents.child:{run_id or 'run'}:{task_index if task_index is not None else 0}",
        tool_id="tool.sub_agents",
        session_id=child_session_id,
        arguments={
            "name": name,
            "task": task,
            "sub_agent_child": True,
            "run_id": run_id or "",
            "task_index": task_index if task_index is not None else 0,
            "status": status or "",
        },
        requested_at=requested_at,
        requester="model",
    )
    emitter(
        ToolLifecycleEvent(
            event_id=f"{invocation.invocation_id}:{phase}",
            invocation=invocation,
            phase=phase,
            detail=detail,
            execution=execution,
            occurred_at=datetime.now(timezone.utc),
        )
    )


def _child_output_summary(output: str, *, status: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return f"sub-agent {status} with no output"
    selected = lines[-8:]
    summary = _bounded_child_text("\n".join(selected).strip())
    if status == "failed":
        return f"sub-agent failed:\n{summary}"
    return summary


def _child_result_summary(payload: Mapping[str, Any], *, output: str, status: str) -> str:
    summary = str(payload.get("summary") or "").strip()
    if not summary and output:
        summary = _child_output_summary(output, status=status)
    if not summary:
        summary = f"sub-agent {status} with no summary"
    summary = _bounded_child_text(summary)
    if status == "failed" and not summary.startswith("sub-agent failed"):
        return f"sub-agent failed:\n{summary}"
    return summary


def _bounded_child_text(value: str, *, limit: int = 12000) -> str:
    text = value.strip()
    if len(text) <= limit:
        return text
    return f"{text[:limit].rstrip()}\n[truncated]"


def _compose_sub_agent_prompt(
    runtime: Any,
    *,
    task: str,
    name: str | None,
    skills: tuple[str, ...],
    session_id: str,
) -> str:
    sections = [
        "[SYSTEM: You are running as a bounded Aegis sub-agent.]",
        "Return a concise final result for the parent agent.",
        "Do not call tool.sub_agents, tool.clarify, or tool.message.send.",
        "Use tools only when they materially advance this delegated task.",
        f"Sub-agent name: {name or 'sub-agent'}",
    ]
    skill_sections = _skill_sections(runtime, skills, session_id=session_id)
    if skill_sections:
        sections.extend(["", "Sub-agent skill references:", "\n\n".join(skill_sections)])
    sections.extend(["", f"Delegated task:\n{task}"])
    return "\n".join(sections).strip()


def _skill_sections(runtime: Any, skill_ids: tuple[str, ...], *, session_id: str) -> list[str]:
    sections: list[str] = []
    for skill_id in skill_ids:
        try:
            skill = runtime.inspect_skill(skill_id, session_id=session_id)
        except Exception as error:
            sections.append(f"Skill {skill_id}: unavailable ({error}).")
            continue
        sections.append(
            "\n".join(
                (
                    f"Skill: {skill.display_name} ({skill.skill_id})",
                    f"Summary: {skill.summary}",
                    "Full skill body: not injected automatically.",
                )
            )
        )
    return sections
