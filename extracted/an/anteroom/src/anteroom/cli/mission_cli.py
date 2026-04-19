"""CLI subcommand handlers for `aroom mission`.

Follows the same dispatch pattern as workflow_cli.py. Pure integration
layer — no core behavior is introduced here.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
from typing import TYPE_CHECKING, Any

from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from ..config import AppConfig

logger = logging.getLogger(__name__)

console = Console()


def _run_mission(config: AppConfig, args: argparse.Namespace) -> None:
    """Top-level dispatcher for `aroom mission` subcommands."""
    action = getattr(args, "mission_action", None)
    if not action:
        console.print(
            "Usage: aroom mission {create,list,status,scheduler,talk,update,revisions,"
            "cancel,reconcile,why,summary,retry,replace}"
        )
        return

    from ..db import get_db

    db = get_db(config.app.data_dir / "chat.db")

    if action == "create":
        _handle_create(config, db, args)
    elif action == "list":
        _handle_list(db, args)
    elif action == "status":
        _handle_status(db, args)
    elif action == "scheduler":
        _handle_scheduler(config, db, args)
    elif action == "talk":
        _handle_talk(config, db, args)
    elif action == "update":
        _handle_update(config, db, args)
    elif action == "revisions":
        _handle_revisions(db, args)
    elif action == "cancel":
        _handle_cancel(db, args)
    elif action == "reconcile":
        _handle_reconcile(config, db, args)
    elif action == "why":
        _handle_why(db, args)
    elif action == "summary":
        _handle_summary(db, args)
    elif action == "retry":
        _handle_retry(db, args)
    elif action == "replace":
        _handle_replace(config, db, args)
    else:
        console.print(f"Unknown mission action: {action}")


def _handle_create(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission create --spec <fqn>` or `--prompt <text>`."""
    from ..services.mission_compiler import AdapterDefaults, apply_plan, compile_from_spec

    spec_fqn = getattr(args, "spec", None)
    prompt = getattr(args, "prompt", None)
    profile_name = getattr(args, "profile", None)

    # Resolve execution profile (if specified)
    profile = None
    if profile_name:
        from ..services.mission_profiles import resolve_profile

        try:
            profile = resolve_profile(profile_name)
        except ValueError as exc:
            console.print(f"[red]Error:[/red] {exc}")
            return

    adapter_type = getattr(args, "adapter", "noop") or "noop"
    workflow_path = getattr(args, "workflow_path", None)
    adapter_config: dict[str, Any] = {}
    if workflow_path:
        adapter_config["workflow_path"] = workflow_path

    # Explicit --adapter/--workflow-path override profile defaults
    defaults: AdapterDefaults | None = None
    if adapter_type != "noop" or workflow_path:
        defaults = AdapterDefaults(adapter_type=adapter_type, adapter_config=adapter_config)

    if prompt:
        plan = _compile_from_prompt_sync(config, prompt, defaults, execution_profile=profile, db=db)
        if plan is None:
            return
    elif spec_fqn:
        try:
            plan = compile_from_spec(db, spec_fqn, adapter_defaults=defaults, execution_profile=profile)
        except ValueError as exc:
            console.print(f"[red]Error:[/red] {exc}")
            return
    else:
        console.print("[red]Error:[/red] --spec or --prompt is required")
        return

    if profile:
        console.print(f"[bold]Profile:[/bold] {profile.name} — {profile.description}")

    table = Table(title="Compiled Plan", show_header=True)
    table.add_column("ID", style="dim")
    table.add_column("Summary")
    table.add_column("Priority", justify="right")
    table.add_column("Adapter")
    table.add_column("Lane")
    table.add_column("Depends On")
    table.add_column("Binding Reason", style="dim")
    for item in plan.items:
        deps = ", ".join(item.depends_on) if item.depends_on else "-"
        reason = item.adapter_config.get("_binding_reason", "") if item.adapter_config else ""
        table.add_row(
            item.temp_id,
            item.summary,
            str(item.priority),
            item.adapter_type,
            item.lane or "-",
            deps,
            reason,
        )
    console.print(table)

    launch_requested = getattr(args, "launch", False)
    if not launch_requested:
        try:
            answer = input("Launch? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        if answer not in ("y", "yes"):
            console.print("Aborted")
            return
        launch_requested = True

    # Compute lane_limits from profile for session persistence
    lane_limits: dict[str, int] | None = None
    if profile and profile.lane_limits:
        lane_limits = dict(profile.lane_limits)

    source_type = "spec" if spec_fqn else "prompt"
    try:
        session = apply_plan(
            db,
            plan,
            source_type=source_type,
            source_fqn=spec_fqn,
            lane_limits=lane_limits,
            session_status="active" if launch_requested else "pending",
        )
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    console.print(f"[green]Mission created:[/green] {session['id']}")
    if session.get("title"):
        console.print(f"[bold]Title:[/bold] {session['title']}")
    if session.get("status") == "active":
        console.print(
            "[dim]Next:[/dim] run `aroom mission scheduler` or start the app runtime"
            " (with `workflow.executor_enabled: true` for workflow-backed missions)."
        )


def _create_ai(config: AppConfig) -> Any:
    from ..services.ai_service import create_ai_service

    return create_ai_service(config.ai)


def _compile_from_prompt_sync(
    config: AppConfig,
    prompt: str,
    defaults: Any,
    *,
    execution_profile: Any | None = None,
    db: Any | None = None,
) -> Any:
    """Create an AI service and compile a plan from a prompt synchronously."""
    from ..services.mission_compiler import compile_from_prompt

    try:
        ai_service = _create_ai(config)
    except Exception as exc:
        console.print(f"[red]Error:[/red] Could not create AI service: {exc}")
        return None

    try:
        return asyncio.run(
            compile_from_prompt(
                prompt,
                ai_service,
                adapter_defaults=defaults,
                execution_profile=execution_profile,
                db=db,
            )
        )
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return None


def _handle_list(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission list [--status <status>]`."""
    from ..services.mission_storage import list_items_by_session, list_sessions

    status_filter = getattr(args, "status", None)
    sessions = list_sessions(db, status=status_filter)

    if not sessions:
        console.print("[dim]No missions found.[/dim]")
        return

    table = Table(title="Missions", show_header=True)
    table.add_column("ID", style="dim", max_width=12)
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Items", justify="right")
    table.add_column("Created")

    for s in sessions:
        items = list_items_by_session(db, s["id"])
        table.add_row(
            s["id"][:8],
            s.get("title") or "-",
            s["status"],
            str(len(items)),
            s["created_at"][:19],
        )

    console.print(table)


def _handle_status(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission status <session_id>`."""
    from ..services.mission_storage import get_dependencies, get_item, get_session, list_items_by_session

    session_id = getattr(args, "session_id", None)
    if not session_id:
        console.print("[red]Error:[/red] session_id is required")
        return

    session = get_session(db, session_id)
    if not session:
        console.print(f"[red]Error:[/red] Mission not found: {session_id}")
        return

    console.print(f"\n[bold]Mission:[/bold] {session['id'][:8]}...")
    if session.get("title"):
        console.print(f"[bold]Title:[/bold] {session['title']}")
    console.print(f"[bold]Status:[/bold] {session['status']}")
    console.print(f"[bold]Created:[/bold] {session['created_at']}")

    if session.get("referenced_artifacts"):
        console.print("[bold]Referenced artifacts:[/bold]")
        for art in session["referenced_artifacts"]:
            fqn = art.get("fqn", "?")
            ver = art.get("version", "?")
            console.print(f"  {fqn} v{ver}")

    items = list_items_by_session(db, session["id"])
    if items:
        completed = sum(1 for i in items if i["status"] == "completed")
        console.print(f"\n[bold]Progress:[/bold] {completed}/{len(items)} completed")

        item_map = {i["id"]: i for i in items}
        table = Table(show_header=True)
        table.add_column("ID", style="dim", max_width=12)
        table.add_column("Summary", max_width=40)
        table.add_column("Type")
        table.add_column("Status")
        table.add_column("Priority", justify="right")
        table.add_column("Lane")
        table.add_column("Adapter")
        table.add_column("Depends On")
        table.add_column("Binding Reason", style="dim")
        for item in items:
            deps = get_dependencies(db, item["id"])
            dep_labels = []
            for dep_id in deps:
                dep_item = item_map.get(dep_id) or get_item(db, dep_id)
                if dep_item:
                    status_icon = "✓" if dep_item["status"] == "completed" else "✗"
                    dep_labels.append(f"{dep_item['summary'][:15]} ({status_icon})")
                else:
                    dep_labels.append(dep_id[:8])
            adapter_config = item.get("adapter_config") or {}
            if isinstance(adapter_config, str):
                import json as _json

                try:
                    adapter_config = _json.loads(adapter_config)
                except (ValueError, TypeError):
                    adapter_config = {}
            binding_reason = adapter_config.get("_binding_reason", "")
            table.add_row(
                item["id"][:8],
                item["summary"],
                item.get("item_type") or "task",
                item["status"],
                str(item["priority"]),
                item.get("lane") or "-",
                item["adapter_type"],
                ", ".join(dep_labels) if dep_labels else "-",
                binding_reason or "-",
            )
        console.print(table)

        blocked = [i for i in items if i["status"] in ("pending", "blocked")]
        if blocked:
            console.print("\n[bold]Blockers:[/bold]")
            for item in blocked:
                reasons: list[str] = []
                if item.get("hold_requested"):
                    reasons.append("held")
                deps = get_dependencies(db, item["id"])
                incomplete_deps = []
                for dep_id in deps:
                    dep_item = item_map.get(dep_id) or get_item(db, dep_id)
                    if dep_item and dep_item["status"] != "completed":
                        incomplete_deps.append(f"{dep_item['summary'][:20]} ({dep_item['status']})")
                if incomplete_deps:
                    reasons.append(f"waiting on: {', '.join(incomplete_deps)}")
                if not reasons:
                    reasons.append(
                        "eligible (run `aroom mission scheduler` or start the app runtime"
                        " with `workflow.executor_enabled: true`)"
                    )
                console.print(f"  {item['id'][:8]} {item['summary']}: {'; '.join(reasons)}")
    else:
        console.print("\n[dim]No items.[/dim]")


async def _run_scheduler_async(
    config: AppConfig,
    db: Any,
    *,
    once: bool,
    poll_interval: float,
) -> None:
    from ..services.mission_runtime import create_mission_adapter_registry, create_workflow_engine_factory
    from ..services.mission_scheduler import MissionSchedulerWorker
    from ..services.workflow_executor import WorkflowExecutorWorker

    workflow_engine_factory = create_workflow_engine_factory(config, db)
    adapter_registry = create_mission_adapter_registry(
        config,
        db,
        workflow_engine_factory=workflow_engine_factory,
    )
    scheduler = MissionSchedulerWorker(
        db=db,
        adapter_registry=adapter_registry,
        poll_interval=poll_interval,
    )

    executor = None
    if config.workflow.enabled:
        executor = WorkflowExecutorWorker(config.workflow, workflow_engine_factory, db)

    if once:
        await scheduler.run_once()
        if executor is not None:
            await executor.run_once()
            await executor.wait_for_idle()
        return

    if executor is not None:
        executor.start()
        console.print("[dim]Workflow executor co-hosted for workflow-backed mission items.[/dim]")
    scheduler.start()
    console.print("[green]Mission scheduler running.[/green] Press Ctrl-C to stop.")
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        scheduler.stop()
        if executor is not None:
            executor.stop()


def _handle_scheduler(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission scheduler`."""
    once = bool(getattr(args, "once", False))
    poll_interval = float(getattr(args, "poll_interval", 5.0))
    try:
        asyncio.run(_run_scheduler_async(config, db, once=once, poll_interval=poll_interval))
    except KeyboardInterrupt:
        console.print("\n[dim]Mission scheduler stopped.[/dim]")
    else:
        if once:
            console.print("[green]Mission scheduler cycle completed.[/green]")


def _handle_talk(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission talk <session_id>`.

    Launches the REPL with mission tools registered via an initial
    ``/mission talk`` prompt that wires the tools into the session.
    """
    from ..services.mission_storage import get_session

    session_id = getattr(args, "session_id", None)
    if not session_id:
        console.print("[red]Error:[/red] session_id is required")
        return

    session = get_session(db, session_id)
    if not session:
        console.print(f"[red]Error:[/red] Mission not found: {session_id}")
        return

    console.print(f"[bold]Attaching to mission:[/bold] {session['id'][:8]}... — {session.get('title', 'untitled')}")
    console.print(f"[bold]Status:[/bold] {session['status']}")
    console.print("Starting chat with mission tools...\n")

    from ..cli.repl import run_cli

    try:
        asyncio.run(run_cli(config, mission_session_id=session_id))
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass


def _handle_update(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission update <session_id> --instruction <text>`."""
    from ..services.mission_compiler import apply_patch, compile_patch
    from ..services.mission_storage import get_session, list_items_by_session

    session_id = getattr(args, "session_id", None)
    instruction = getattr(args, "instruction", None)
    force = getattr(args, "force", False)

    if not session_id or not instruction:
        console.print("[red]Error:[/red] session_id and --instruction are required")
        return

    session = get_session(db, session_id)
    if not session:
        console.print(f"[red]Error:[/red] Mission not found: {session_id}")
        return

    try:
        ai_service = _create_ai(config)
    except Exception as exc:
        console.print(f"[red]Error:[/red] Could not create AI service: {exc}")
        return

    current_items = list_items_by_session(db, session_id)
    items_for_compiler = [
        {
            "id": item["id"],
            "summary": item["summary"],
            "status": item["status"],
            "priority": item["priority"],
            "adapter_type": item["adapter_type"],
            "lane": item.get("lane"),
        }
        for item in current_items
    ]

    artifact_context = session.get("referenced_artifacts") or []
    try:
        patch = asyncio.run(
            compile_patch(instruction, items_for_compiler, ai_service, artifact_context=artifact_context)
        )
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    if not patch.operations:
        console.print("[dim]No operations compiled from instruction.[/dim]")
        return

    console.print(f"\n[bold]Patch preview:[/bold] {len(patch.operations)} operation(s)")
    for op in patch.operations:
        restricted_tag = " [yellow](restricted — targets active item)[/yellow]" if op.restricted else ""
        target = f" → {op.target_item_id[:8]}..." if op.target_item_id else ""
        console.print(f"  {op.op}{target}{restricted_tag}")

    if not force:
        restricted = [op for op in patch.operations if op.restricted]
        if restricted:
            console.print(f"\n[yellow]Warning:[/yellow] {len(restricted)} operation(s) target active items.")
        try:
            answer = input("Apply? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        if answer not in ("y", "yes"):
            console.print("Aborted")
            return

    try:
        apply_patch(db, session_id, patch, allow_restricted=force)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    console.print(f"[green]Patch applied:[/green] {len(patch.operations)} operation(s)")


def _handle_revisions(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission revisions <session_id>`."""
    from ..services.mission_storage import get_session, list_revisions

    session_id = getattr(args, "session_id", None)
    if not session_id:
        console.print("[red]Error:[/red] session_id is required")
        return

    session = get_session(db, session_id)
    if not session:
        console.print(f"[red]Error:[/red] Mission not found: {session_id}")
        return

    revisions = list_revisions(db, session_id)
    if not revisions:
        console.print("[dim]No revisions found.[/dim]")
        return

    table = Table(title=f"Revisions — {session_id[:8]}...", show_header=True)
    table.add_column("Rev #", justify="right")
    table.add_column("Operations")
    table.add_column("Reason")
    table.add_column("Artifacts")
    table.add_column("Created")
    for rev in revisions:
        ops = rev.get("operations", [])
        op_summary = f"{len(ops)} op(s)"
        if ops:
            op_types = set()
            for op in ops:
                if isinstance(op, dict):
                    op_types.add(op.get("op", "?"))
            if op_types:
                op_summary += f" ({', '.join(sorted(op_types))})"

        art_refs = rev.get("referenced_artifacts") or []
        art_summary = "-"
        if art_refs:
            art_parts = []
            for art in art_refs:
                fqn = art.get("fqn", "?")
                ver = art.get("version", "?")
                art_parts.append(f"{fqn} v{ver}")
            art_summary = ", ".join(art_parts)

        table.add_row(
            str(rev["revision_number"]),
            op_summary,
            rev.get("reason") or "-",
            art_summary,
            rev["created_at"][:19],
        )
    console.print(table)


def _handle_retry(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission retry <item_id>`."""
    from ..services.mission_storage import get_item, resolve_item_id, retry_item

    item_id = getattr(args, "item_id", None)
    if not item_id:
        console.print("[red]Error:[/red] item_id is required")
        return

    try:
        resolved_id = resolve_item_id(db, item_id)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    item = get_item(db, resolved_id)
    if not item:
        console.print(f"[red]Error:[/red] Item not found: {resolved_id}")
        return

    if item["status"] != "failed":
        console.print(f"[red]Error:[/red] Item is {item['status']!r}, must be 'failed' to retry.")
        return

    retry_item(db, resolved_id)
    console.print(f"[green]Item {resolved_id[:8]}... reset to pending for retry[/green]")


def _handle_replace(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission replace <item_id>`.

    Cancels the latest execution via the adapter, then resets the item to
    pending so the scheduler re-launches it.
    """
    from ..services.mission_storage import get_item, get_latest_execution, prepare_replace, resolve_item_id

    item_id = getattr(args, "item_id", None)
    if not item_id:
        console.print("[red]Error:[/red] item_id is required")
        return

    try:
        resolved_id = resolve_item_id(db, item_id)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    item = get_item(db, resolved_id)
    if not item:
        console.print(f"[red]Error:[/red] Item not found: {resolved_id}")
        return

    execution = get_latest_execution(db, resolved_id)
    if not execution:
        console.print("[red]Error:[/red] No execution found for this item.")
        return

    adapter_ref = execution.get("adapter_ref")
    adapter_type = item.get("adapter_type", "noop")

    # Cancel via adapter if there is an adapter_ref.
    # Fail closed: if cancellation fails, do NOT proceed with replacement
    # to avoid queuing a new run while the original is still live.
    if adapter_ref:
        from ..services.mission_runtime import create_mission_adapter_registry, create_workflow_engine_factory

        workflow_engine_factory = create_workflow_engine_factory(config, db)
        adapter_registry = create_mission_adapter_registry(
            config,
            db,
            workflow_engine_factory=workflow_engine_factory,
        )
        adapter = adapter_registry.get(adapter_type)
        if adapter is None:
            console.print(
                f"[red]Error:[/red] no adapter registered for type {adapter_type!r}. "
                "Cannot replace without confirming the original execution is cancelled."
            )
            return
        try:
            asyncio.run(adapter.cancel(adapter_ref=adapter_ref))
        except Exception as exc:
            console.print(
                f"[red]Error:[/red] adapter cancel failed: {exc}\n"
                "Cannot replace while the original execution may still be live. "
                "Investigate and cancel manually before retrying."
            )
            return

    prepare_replace(db, resolved_id, execution["id"])
    console.print(f"[green]Item {resolved_id[:8]}... execution cancelled, reset to pending for replacement[/green]")


def _handle_cancel(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission cancel <session_id>`."""
    from ..services.mission_storage import create_event, get_session, update_session

    session_id = getattr(args, "session_id", None)
    if not session_id:
        console.print("[red]Error:[/red] session_id is required")
        return

    session = get_session(db, session_id)
    if not session:
        console.print(f"[red]Error:[/red] Mission not found: {session_id}")
        return

    terminal = {"completed", "failed", "cancelled"}
    if session["status"] in terminal:
        console.print(f"[red]Error:[/red] Mission is already {session['status']}. Cannot cancel.")
        return

    update_session(db, session_id, status="cancelled")
    create_event(db, session_id=session_id, event_type="session_cancelled")

    from ..services.mission_summary import generate_and_store_retrospective

    try:
        generate_and_store_retrospective(db, session_id, is_draft=False)
    except Exception:
        logger.warning("Failed to generate retrospective for cancelled session %s", session_id[:8])

    console.print(f"[green]Mission {session_id[:8]}... cancelled[/green]")


def _handle_reconcile(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission reconcile <session_id> <item_id> --reason <text>`."""
    from ..services.mission_storage import (
        get_item,
        get_latest_execution,
        get_session,
        reconcile_item,
        resolve_item_id,
    )

    session_id = getattr(args, "session_id", None)
    item_id = getattr(args, "item_id", None)
    reason = getattr(args, "reason", None)
    status = getattr(args, "status", "completed") or "completed"
    force = getattr(args, "force", False)

    if not session_id or not item_id:
        console.print("[red]Error:[/red] session_id and item_id are required")
        return

    if not reason:
        console.print("[red]Error:[/red] --reason is required")
        return

    session = get_session(db, session_id)
    if not session:
        console.print(f"[red]Error:[/red] Mission not found: {session_id}")
        return

    try:
        resolved_id = resolve_item_id(db, item_id, session_id=session_id)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    item = get_item(db, resolved_id)
    if not item:
        console.print(f"[red]Error:[/red] Item not found: {resolved_id}")
        return

    if item["session_id"] != session_id:
        console.print("[red]Error:[/red] Item does not belong to this mission session")
        return

    # --force: cancel live child execution via adapter before reconciling
    if force:
        latest = get_latest_execution(db, resolved_id)
        if latest and latest["status"] in ("pending", "running"):
            try:
                _force_cancel_execution(config, db, item, latest)
                console.print(
                    f"[yellow]Cancelled live execution {latest['id'][:8]} "
                    f"(status: {latest['status']}) via adapter[/yellow]"
                )
            except Exception as exc:
                console.print(f"[red]Error:[/red] Failed to cancel live execution: {exc}")
                return

    try:
        updated = reconcile_item(db, resolved_id, status=status, reason=reason)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    console.print(
        f"[green]Reconciled:[/green] {updated['summary']} — {item['status']} -> {updated['status']} ({reason})"
    )


def _force_cancel_execution(config: AppConfig, db: Any, item: dict[str, Any], execution: dict[str, Any]) -> None:
    """Cancel a live execution via the adapter, then mark it cancelled in the DB."""
    from datetime import datetime, timezone

    from ..services.mission_runtime import create_mission_adapter_registry
    from ..services.mission_storage import update_execution

    adapter_type = item.get("adapter_type", "noop")
    adapter_ref = execution.get("adapter_ref")

    registry = create_mission_adapter_registry(config, db)
    adapter = registry.get(adapter_type)
    if adapter is None:
        raise ValueError(f"No adapter registered for type {adapter_type!r}")

    if adapter_ref:
        result = asyncio.run(adapter.cancel(adapter_ref=adapter_ref))
        if result.state not in ("cancelled", "completed"):
            raise RuntimeError(f"Adapter cancel returned unexpected state: {result.state}")

    now = datetime.now(timezone.utc).isoformat()
    update_execution(db, execution["id"], status="cancelled", finished_at=now)


def _handle_summary(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission summary <session_id> [--since <timestamp>]`."""
    from ..services.mission_storage import get_session
    from ..services.mission_summary import build_delta_summary, build_retrospective

    session_id = getattr(args, "session_id", None)
    since = getattr(args, "since", None)
    if not session_id:
        console.print("[red]Error:[/red] session_id is required")
        return

    session = get_session(db, session_id)
    if not session:
        console.print(f"[red]Error:[/red] Mission not found: {session_id}")
        return

    if since:
        summary = build_delta_summary(db, session_id, since=since)
        console.print(f"\n[bold]Delta summary[/bold] since {since}")
        console.print(f"Events: {summary['event_count']}")
        console.print(f"Launched: {len(summary['items_launched'])}")
        console.print(f"Completed: {len(summary['items_completed'])}")
        console.print(f"Failed: {len(summary['items_failed'])}")
        if summary["session_events"]:
            console.print("[bold]Session events:[/bold]")
            for sev in summary["session_events"]:
                console.print(f"  {sev['event_type']} at {sev['created_at'][:19]}")
    else:
        retro = build_retrospective(db, session_id)
        console.print(f"\n[bold]Retrospective:[/bold] {session_id[:8]}...")
        if retro.get("title"):
            console.print(f"[bold]Title:[/bold] {retro['title']}")
        console.print(f"[bold]Status:[/bold] {retro['status']}")
        console.print(
            f"[bold]Completion:[/bold] {retro['completed']}/{retro['total_items']} ({retro['completion_rate']}%)"
        )
        console.print(f"[bold]Duration:[/bold] {retro['duration_seconds']}s")
        if retro["failed_summaries"]:
            console.print("[bold]Failed items:[/bold]")
            for s in retro["failed_summaries"]:
                console.print(f"  - {s}")
        if retro["completed_summaries"]:
            console.print("[bold]Completed items:[/bold]")
            for s in retro["completed_summaries"]:
                console.print(f"  - {s}")


def _handle_why(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom mission why <session_id>`. Concise blocker summary per item."""
    from ..services.mission_storage import (
        get_dependencies,
        get_item,
        get_latest_execution,
        get_session,
        list_items_by_session,
    )

    session_id = getattr(args, "session_id", None)
    if not session_id:
        console.print("[red]Error:[/red] session_id is required")
        return

    session = get_session(db, session_id)
    if not session:
        console.print(f"[red]Error:[/red] Mission not found: {session_id}")
        return

    items = list_items_by_session(db, session_id)
    item_map = {i["id"]: i for i in items}

    terminal_statuses = {"completed", "cancelled", "failed"}
    if session["status"] in terminal_statuses:
        console.print(f"Mission {session_id[:8]}... is [bold]{session['status']}[/bold]. No active blockers.")
        return

    _terminal_item_statuses = {"completed", "dropped"}
    non_completed = [i for i in items if i["status"] not in _terminal_item_statuses]
    if not non_completed:
        dropped_count = sum(1 for i in items if i["status"] == "dropped")
        suffix = f" ({dropped_count} dropped)" if dropped_count else ""
        console.print(f"Mission {session_id[:8]}... — all items completed{suffix}.")
        return

    for item in non_completed:
        item_label = f"{item['id'][:8]} {item['summary']}"

        # Check dependency blockers
        dep_ids = get_dependencies(db, item["id"])
        incomplete_deps = []
        for dep_id in dep_ids:
            dep = item_map.get(dep_id) or get_item(db, dep_id)
            if dep and dep["status"] not in _terminal_item_statuses:
                incomplete_deps.append(f"{dep['summary'][:25]} ({dep['status']})")

        if item.get("hold_requested"):
            console.print(f"[yellow]Held:[/yellow] {item_label}")
            _print_dependents(db, item, item_map)
            continue

        # Check linked workflow run
        latest_exec = get_latest_execution(db, item["id"])
        adapter_ref = latest_exec.get("adapter_ref") if latest_exec else None

        if adapter_ref:
            _diagnose_linked_run(db, item_label, adapter_ref)
        elif incomplete_deps:
            console.print(f"[yellow]Blocked:[/yellow] {item_label} — waiting on: {', '.join(incomplete_deps)}")
        else:
            console.print(f"[cyan]Eligible:[/cyan] {item_label} — ready to run")

        _print_dependents(db, item, item_map)


def _diagnose_linked_run(db: Any, item_label: str, adapter_ref: str) -> None:
    """Diagnose a mission item's linked workflow run."""
    from ..services.workflow_storage import (
        get_workflow_run,
        list_pending_approvals,
        list_pending_decisions,
        list_workflow_events,
        list_workflow_steps,
    )

    run = get_workflow_run(db, adapter_ref)
    if not run:
        console.print(f"[yellow]Blocked:[/yellow] {item_label} — linked run {adapter_ref[:8]} not found")
        return

    status = run.get("status", "unknown")

    if status == "waiting_for_approval":
        approvals = list_pending_approvals(db, run["id"])
        step_ids = ", ".join(a.get("step_id", "?") for a in approvals) if approvals else "unknown"
        console.print(f"[yellow]Waiting:[/yellow] {item_label} — approval needed for step {step_ids}")
        return

    if status == "waiting_for_input":
        decisions = list_pending_decisions(db, run["id"])
        prompts = "; ".join(d.get("prompt", "?") for d in decisions) if decisions else ""
        suffix = f" — {prompts}" if prompts else ""
        console.print(f"[yellow]Waiting:[/yellow] {item_label} — human input needed{suffix}")
        return

    if status in ("completed", "running", "claimed", "pending"):
        console.print(f"[green]OK:[/green] {item_label} — linked run is {status}")
        return

    from ..cli.workflow_cli import _enrich_steps_for_diagnosis
    from ..services.workflow_diagnosis import diagnose

    steps = _enrich_steps_for_diagnosis(list_workflow_steps(db, run["id"]))
    events = list_workflow_events(db, run["id"])
    result = diagnose(run, steps, events)

    console.print(f"[red]Blocked:[/red] {item_label} — {result.what}")
    console.print(f"  [yellow]Because:[/yellow] {result.why}")
    if result.next_actions:
        console.print(f"  [cyan]Next:[/cyan] {result.next_actions[0]}")


def _print_dependents(db: Any, item: dict[str, Any], item_map: dict[str, dict[str, Any]]) -> None:
    """Print items waiting behind this one."""
    from ..services.mission_storage import get_dependents, get_item

    dependent_ids = get_dependents(db, item["id"])
    if not dependent_ids:
        return
    waiting = []
    for dep_id in dependent_ids:
        dep = item_map.get(dep_id) or get_item(db, dep_id)
        if dep and dep["status"] not in ("completed", "dropped"):
            waiting.append(dep["summary"][:25])
    if waiting:
        console.print(f"  [dim]Blocking:[/dim] {', '.join(waiting)}")
