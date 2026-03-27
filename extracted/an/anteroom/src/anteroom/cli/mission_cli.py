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
        console.print("Usage: aroom mission {create,list,status,talk,update,revisions,cancel}")
        return

    from ..db import get_db

    db = get_db(config.app.data_dir / "chat.db")

    if action == "create":
        _handle_create(config, db, args)
    elif action == "list":
        _handle_list(db, args)
    elif action == "status":
        _handle_status(db, args)
    elif action == "talk":
        _handle_talk(config, db, args)
    elif action == "update":
        _handle_update(config, db, args)
    elif action == "revisions":
        _handle_revisions(db, args)
    elif action == "cancel":
        _handle_cancel(db, args)
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
        plan = _compile_from_prompt_sync(config, prompt, defaults, execution_profile=profile)
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

    launch = getattr(args, "launch", False)
    if not launch:
        try:
            answer = input("Launch? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        if answer not in ("y", "yes"):
            console.print("Aborted")
            return

    # Compute lane_limits from profile for session persistence
    lane_limits: dict[str, int] | None = None
    if profile and profile.lane_limits:
        lane_limits = dict(profile.lane_limits)

    source_type = "spec" if spec_fqn else "prompt"
    try:
        session = apply_plan(db, plan, source_type=source_type, source_fqn=spec_fqn, lane_limits=lane_limits)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    console.print(f"[green]Mission created:[/green] {session['id']}")
    if session.get("title"):
        console.print(f"[bold]Title:[/bold] {session['title']}")


def _create_ai(config: AppConfig) -> Any:
    from ..services.ai_service import create_ai_service

    return create_ai_service(config.ai)


def _compile_from_prompt_sync(
    config: AppConfig,
    prompt: str,
    defaults: Any,
    *,
    execution_profile: Any | None = None,
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
            compile_from_prompt(prompt, ai_service, adapter_defaults=defaults, execution_profile=execution_profile)
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
        table.add_column("Status")
        table.add_column("Priority", justify="right")
        table.add_column("Lane")
        table.add_column("Adapter")
        table.add_column("Depends On")
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
            table.add_row(
                item["id"][:8],
                item["summary"],
                item["status"],
                str(item["priority"]),
                item.get("lane") or "-",
                item["adapter_type"],
                ", ".join(dep_labels) if dep_labels else "-",
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
                    reasons.append("eligible (awaiting scheduler)")
                console.print(f"  {item['id'][:8]} {item['summary']}: {'; '.join(reasons)}")
    else:
        console.print("\n[dim]No items.[/dim]")


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
    console.print(f"[green]Mission {session_id[:8]}... cancelled[/green]")
