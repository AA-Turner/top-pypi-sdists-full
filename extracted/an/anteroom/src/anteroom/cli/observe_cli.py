"""Unified CLI observation surface for mission sessions and workflow runs."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


@dataclass
class _ResolutionResult:
    kind: str | None = None
    resolved_id: str | None = None
    error: str | None = None


def _resolve_mission_session_id(db: Any, session_ref: str) -> str:
    from ..services.mission_storage import resolve_session_id

    return resolve_session_id(db, session_ref)


def _resolve_workflow_run_id(db: Any, run_ref: str) -> str:
    from ..services.workflow_storage import resolve_workflow_run_id

    return resolve_workflow_run_id(db, run_ref)


def _try_resolve(target: str, resolver: Any, kind: str, db: Any) -> _ResolutionResult:
    try:
        return _ResolutionResult(kind=kind, resolved_id=resolver(db, target))
    except ValueError as exc:
        return _ResolutionResult(kind=kind, error=str(exc))


def _resolve_target(db: Any, target: str) -> tuple[str | None, str | None, str | None]:
    mission = _try_resolve(target, _resolve_mission_session_id, "mission", db)
    workflow = _try_resolve(target, _resolve_workflow_run_id, "workflow", db)

    mission_ok = mission.resolved_id is not None
    workflow_ok = workflow.resolved_id is not None

    if mission_ok and workflow_ok:
        return (
            None,
            None,
            (
                f"Ambiguous ID '{target}': matches mission session {mission.resolved_id} "
                f"and workflow run {workflow.resolved_id}"
            ),
        )
    if mission_ok:
        return "mission", mission.resolved_id, None
    if workflow_ok:
        return "workflow", workflow.resolved_id, None

    ambiguous_errors = [err for err in (mission.error, workflow.error) if err and "Ambiguous" in err]
    if ambiguous_errors:
        return None, None, ambiguous_errors[0]

    return None, None, f"Target not found: {target}"


def _build_workflow_payload(db: Any, run_id: str) -> dict[str, Any]:
    from ..services.workflow_storage import (
        count_checkpoints,
        get_workflow_run,
        list_pending_approvals,
        list_pending_decisions,
        list_workflow_steps,
    )

    run = get_workflow_run(db, run_id)
    assert run is not None
    steps = list_workflow_steps(db, run_id)
    pending_approvals = list_pending_approvals(db, run_id)
    pending_decisions = list_pending_decisions(db, run_id)

    return {
        "kind": "workflow",
        "run": run,
        "steps": steps,
        "checkpoint_count": count_checkpoints(db, run_id),
        "pending_approvals": pending_approvals,
        "pending_decisions": pending_decisions,
    }


def _mission_item_blockers(db: Any, item: dict[str, Any], item_map: dict[str, dict[str, Any]]) -> list[str]:
    from ..services.mission_storage import get_dependencies

    reasons: list[str] = []
    if item.get("hold_requested"):
        reasons.append("held")
    deps = get_dependencies(db, item["id"])
    waiting = []
    for dep_id in deps:
        dep = item_map.get(dep_id)
        if dep and dep.get("status") != "completed":
            waiting.append(f"{dep['summary']} ({dep['status']})")
    if waiting:
        reasons.append(f"waiting on: {', '.join(waiting)}")
    return reasons


def _linked_workflow_summary(db: Any, adapter_ref: str | None) -> dict[str, Any] | None:
    if not adapter_ref:
        return None

    from ..services.workflow_storage import (
        get_workflow_run,
        list_pending_approvals,
        list_pending_decisions,
    )

    run = get_workflow_run(db, adapter_ref)
    if not run:
        return {
            "run_id": adapter_ref,
            "missing": True,
        }

    return {
        "run_id": run["id"],
        "status": run["status"],
        "current_step_id": run.get("current_step_id"),
        "stop_reason": run.get("stop_reason"),
        "pending_approvals": list_pending_approvals(db, run["id"]),
        "pending_decisions": list_pending_decisions(db, run["id"]),
    }


def _build_mission_payload(db: Any, session_id: str) -> dict[str, Any]:
    from ..services.mission_storage import get_latest_execution, get_session, list_events, list_items_by_session

    session = get_session(db, session_id)
    assert session is not None
    items = list_items_by_session(db, session_id)
    item_map = {item["id"]: item for item in items}

    enriched_items = []
    for item in items:
        latest_execution = get_latest_execution(db, item["id"])
        blockers = _mission_item_blockers(db, item, item_map)
        linked_workflow = _linked_workflow_summary(
            db,
            latest_execution.get("adapter_ref") if latest_execution else None,
        )
        if linked_workflow:
            if linked_workflow.get("pending_approvals"):
                blockers.append("waiting on linked workflow approval")
            if linked_workflow.get("pending_decisions"):
                blockers.append("waiting on linked workflow input")
            stop_reason = linked_workflow.get("stop_reason")
            if stop_reason:
                blockers.append(f"stop_reason: {stop_reason}")
        if not blockers and item.get("status") in {"pending", "blocked"}:
            blockers.append("eligible")

        enriched_items.append(
            {
                **item,
                "latest_execution": latest_execution,
                "linked_workflow": linked_workflow,
                "blockers": blockers,
            }
        )

    reconciled_events = list_events(db, session_id, event_type="item_reconciled")

    return {
        "kind": "mission",
        "session": session,
        "items": enriched_items,
        "reconciled_events": reconciled_events,
    }


def _render_workflow(payload: dict[str, Any]) -> None:
    from ..cli.workflow_fmt import status_color, status_icon

    run = payload["run"]
    console.print(f"\n[bold]Workflow:[/bold] {run['id'][:12]}...")
    console.print(f"[bold]Workflow ID:[/bold] {run['workflow_id']} v{run.get('workflow_version', '?')}")
    console.print(f"[bold]Target:[/bold] {run['target_kind']}:{run['target_ref']}")
    console.print(f"[bold]Status:[/bold] {run['status']}")
    if run.get("current_step_id"):
        console.print(f"[bold]Current step:[/bold] {run['current_step_id']}")
    if run.get("stop_reason"):
        console.print(f"[bold]Stop reason:[/bold] {run['stop_reason']}")
    console.print(f"[bold]Checkpoints:[/bold] {payload['checkpoint_count']}")
    pending_approvals = payload.get("pending_approvals") or []
    if pending_approvals:
        console.print("[bold]Pending approvals:[/bold]")
        for approval in pending_approvals:
            console.print(f"  - {approval['tool_name']} ({approval['risk_tier']})")
    pending_decisions = payload.get("pending_decisions") or []
    if pending_decisions:
        console.print("[bold]Pending inputs:[/bold]")
        for decision in pending_decisions:
            console.print(f"  - {decision['prompt']}")

    steps = payload["steps"]
    if steps:
        table = Table(title="Steps")
        table.add_column("Step")
        table.add_column("Type")
        table.add_column("Status")
        table.add_column("Result")
        for step in steps:
            step_status = step["status"]
            result_status = step.get("result_status") or "-"
            sc = status_color(step_status)
            si = status_icon(step_status)
            table.add_row(
                step["step_id"],
                step["step_type"],
                f"[{sc}]{si} {step_status}[/{sc}]",
                result_status,
            )
        console.print(table)


def _render_mission(payload: dict[str, Any]) -> None:
    from ..cli.workflow_fmt import status_color, status_icon

    session = payload["session"]
    console.print(f"\n[bold]Mission:[/bold] {session['id'][:12]}...")
    if session.get("title"):
        console.print(f"[bold]Title:[/bold] {session['title']}")
    console.print(f"[bold]Status:[/bold] {session['status']}")

    items = payload["items"]
    completed = sum(1 for item in items if item["status"] == "completed")
    console.print(f"[bold]Progress:[/bold] {completed}/{len(items)} completed")

    table = Table(title="Items")
    table.add_column("ID")
    table.add_column("Item")
    table.add_column("Type")
    table.add_column("Status")
    table.add_column("Latest execution")
    table.add_column("Linked workflow")
    table.add_column("Blockers")
    for item in items:
        latest_execution = item.get("latest_execution")
        exec_summary = "-"
        if latest_execution:
            exec_summary = f"#{latest_execution['attempt_number']} {latest_execution['status']}"
        linked = item.get("linked_workflow")
        linked_summary = "-"
        if linked:
            linked_summary = linked["run_id"][:12]
            if linked.get("status"):
                linked_summary += f" ({linked['status']})"
        item_status = item["status"]
        sc = status_color(item_status)
        si = status_icon(item_status)
        table.add_row(
            item["id"][:8],
            item["summary"],
            item.get("item_type") or "task",
            f"[{sc}]{si} {item_status}[/{sc}]",
            exec_summary,
            linked_summary,
            "; ".join(item.get("blockers") or []) or "-",
        )
    console.print(table)

    reconciled_events = payload.get("reconciled_events") or []
    if reconciled_events:
        item_map = {item["id"]: item for item in items}
        console.print("\n[bold]Reconciled items:[/bold]")
        for ev in reconciled_events:
            detail = ev.get("detail") or {}
            item_summary = "-"
            if ev.get("item_id") and ev["item_id"] in item_map:
                item_summary = item_map[ev["item_id"]]["summary"]
            reason = detail.get("reason", "-")
            from_status = detail.get("from_status", "?")
            to_status = detail.get("to_status", "?")
            console.print(f"  {item_summary}: {from_status} -> {to_status} — {reason}")

    approvals = []
    for item in items:
        linked = item.get("linked_workflow") or {}
        for approval in linked.get("pending_approvals") or []:
            approvals.append((item["summary"], approval))
    if approvals:
        console.print("\n[bold]Pending approvals:[/bold]")
        for summary, approval in approvals:
            console.print(f"  {summary}: {approval['tool_name']} ({approval['risk_tier']})")


def _render_delta_summary(delta: dict[str, Any], since: str) -> None:
    console.print(f"\n[bold]Delta summary[/bold] since {since}")
    console.print(f"Events: {delta['event_count']}")
    console.print(f"Launched: {len(delta['items_launched'])}")
    console.print(f"Completed: {len(delta['items_completed'])}")
    console.print(f"Failed: {len(delta['items_failed'])}")
    if delta.get("session_events"):
        console.print("[bold]Session events:[/bold]")
        for sev in delta["session_events"]:
            console.print(f"  {sev['event_type']} at {sev['created_at'][:19]}")


def _render_retrospective(retro: dict[str, Any]) -> None:
    console.print(f"\n[bold]Retrospective:[/bold] {retro['session_id'][:8]}...")
    if retro.get("title"):
        console.print(f"[bold]Title:[/bold] {retro['title']}")
    console.print(f"[bold]Status:[/bold] {retro['status']}")
    console.print(f"[bold]Completion:[/bold] {retro['completed']}/{retro['total_items']} ({retro['completion_rate']}%)")
    console.print(f"[bold]Duration:[/bold] {retro['duration_seconds']}s")
    if retro.get("failed_summaries"):
        console.print("[bold]Failed items:[/bold]")
        for s in retro["failed_summaries"]:
            console.print(f"  - {s}")
    if retro.get("completed_summaries"):
        console.print("[bold]Completed items:[/bold]")
        for s in retro["completed_summaries"]:
            console.print(f"  - {s}")


def _run_observe(config: Any, args: argparse.Namespace) -> None:
    from ..db import get_db

    db = get_db(config.app.data_dir / "chat.db")
    target = getattr(args, "target", None)
    if not target:
        console.print("[red]Error:[/red] target is required")
        return

    kind, resolved_id, error = _resolve_target(db, target)
    if error:
        console.print(f"[red]Error:[/red] {error}")
        return
    assert kind is not None and resolved_id is not None

    since = getattr(args, "since", None)
    summary = getattr(args, "summary", False)

    if kind == "mission" and (since or summary):
        from ..services.mission_summary import build_delta_summary, build_retrospective

        if since:
            delta = build_delta_summary(db, resolved_id, since=since)
            if getattr(args, "json_output", False):
                print(json.dumps(delta, indent=2))
            else:
                _render_delta_summary(delta, since)
        else:
            retro = build_retrospective(db, resolved_id)
            if getattr(args, "json_output", False):
                print(json.dumps(retro, indent=2))
            else:
                _render_retrospective(retro)
        return

    payload = _build_mission_payload(db, resolved_id) if kind == "mission" else _build_workflow_payload(db, resolved_id)

    if getattr(args, "json_output", False):
        print(json.dumps(payload, indent=2))
        return

    if kind == "mission":
        _render_mission(payload)
    else:
        _render_workflow(payload)
