"""CLI subcommand handlers for `aroom workflow`.

Uses workflow-neutral language throughout. Domain-specific concepts
(issues, PRs) only appear in built-in workflow definitions, not here.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from ..config import AppConfig

logger = logging.getLogger(__name__)

console = Console()


def _format_tokens(n: int) -> str:
    """Format token count as human-readable (e.g. 23K, 1.2M)."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def _format_duration(seconds: int) -> str:
    """Format duration as MM:SS or H:MM:SS."""
    if seconds >= 3600:
        h, remainder = divmod(seconds, 3600)
        m, s = divmod(remainder, 60)
        return f"{h}:{m:02d}:{s:02d}"
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


def _resolve_workflow_path(workflow_id: str) -> Path | None:
    """Resolve a workflow definition by ID or path.

    Delegates to the shared resolution module.
    """
    from ..services.workflow_resolution import resolve_workflow_path

    return resolve_workflow_path(workflow_id)


def _create_engine(config: AppConfig, db: Any, *, space_id: str | None = None) -> tuple[Any, Any]:
    """Create a WorkflowEngine with AI service, credential resolver, and registries.

    When space_id is provided, ArtifactRegistry and SkillRegistry are scoped
    to that space. For resume, pass the run's stored space_id to guarantee
    the same artifact/skill resolution as the original run.

    Returns (engine, event_bus) — caller must call event_bus.stop_polling()
    when done to avoid asyncio task leak warnings on exit.
    """
    from ..services.workflow_engine import WorkflowEngine
    from ..services.workflow_runners import create_default_registry

    ai_service = None
    tool_executor = None
    tools_openai = None
    try:
        from ..services.ai_service import create_ai_service
        from ..tools import ToolRegistry, register_default_tools

        ai_service = create_ai_service(config.ai)
        tool_reg = ToolRegistry()
        register_default_tools(tool_reg, working_dir=str(Path.cwd()))
        tool_executor = tool_reg.call_tool
        tools_openai = tool_reg.get_openai_tools()
    except Exception as exc:
        logger.warning("Could not initialize AI service: %s", exc)
        console.print(
            "[yellow]Warning:[/yellow] AI service not available."
            " Agent runner steps will fail. Shell/script steps will work."
        )

    # Create event bus backed by DB change_log for cross-process SSE delivery.
    event_bus = None
    try:
        from ..db import DatabaseManager
        from ..services.event_bus import EventBus

        event_bus = EventBus()
        db_manager = DatabaseManager()
        db_manager.add("personal", config.app.data_dir / "chat.db")
        event_bus._db_manager = db_manager  # Write-only: no poll loop needed
    except Exception as exc:
        logger.warning("Could not initialize event bus: %s", exc)

    # Build credential resolver (#970)
    credential_resolver = None
    if config.workflow.credentials:
        from ..services.workflow_credentials import CredentialResolver

        credential_resolver = CredentialResolver(config.workflow.credentials)

    # Build artifact and skill registries, scoped by space_id (#957)
    artifact_registry = None
    skill_registry = None
    try:
        from ..cli.skills import SkillRegistry
        from ..services.artifact_registry import ArtifactRegistry

        artifact_registry = ArtifactRegistry()
        artifact_registry.load_from_db(db, space_id=space_id)
        skill_registry = SkillRegistry()
        skill_registry.load()
        skill_registry.load_from_artifacts(artifact_registry)
    except Exception as exc:
        logger.debug("Could not initialize artifact/skill registries: %s", exc)

    # Register spec phase gate conditions (#997)
    try:
        from ..services.spec_gates import register_spec_gates

        register_spec_gates(db)
    except Exception:
        logger.debug("Could not register spec gates")

    registry = create_default_registry()

    audit_writer = None
    try:
        from ..services.audit import create_audit_writer

        audit_writer = create_audit_writer(config)
    except Exception:
        logger.debug("Could not create audit writer for workflow engine")

    engine = WorkflowEngine(
        db,
        config.workflow,
        registry,
        effective_approval_mode=config.safety.approval_mode,
        ai_service=ai_service,
        tool_executor=tool_executor,
        tools_openai=tools_openai,
        event_bus=event_bus,
        egress_allowed_domains=list(config.ai.allowed_domains) if config.ai.allowed_domains else [],
        egress_block_localhost=config.ai.block_localhost_api,
        credential_resolver=credential_resolver,
        artifact_registry=artifact_registry,
        skill_registry=skill_registry,
        model_costs=config.cli.usage.model_costs,
        audit_writer=audit_writer,
    )
    return engine, event_bus


def _cleanup_event_bus(event_bus: Any) -> None:
    """Stop the event bus polling task to avoid asyncio warnings on exit."""
    if event_bus is not None:
        try:
            event_bus.stop_polling()
        except Exception:
            pass


def _print_run_progress(db: Any, run: dict[str, Any]) -> None:
    """Print step-by-step progress report after a workflow run completes."""
    from ..services.workflow_storage import list_workflow_steps

    steps = list_workflow_steps(db, run["id"])
    if steps:
        console.print("\n[bold]Steps:[/bold]")
        for step in steps:
            status = step.get("status", "unknown")
            step_id = step.get("step_id", "?")
            duration = step.get("duration_ms")
            summary = (step.get("result_summary") or "")[:60]
            dur_str = f" ({duration}ms)" if duration else ""

            if status == "completed":
                result_status = step.get("result_status", "success")
                if result_status == "success":
                    icon = "[green]done[/green]"
                elif result_status == "blocked":
                    icon = "[yellow]blocked[/yellow]"
                else:
                    icon = f"[dim]{result_status}[/dim]"
            elif status == "failed":
                icon = "[red]failed[/red]"
            elif status == "interrupted":
                icon = "[yellow]interrupted[/yellow]"
            elif status == "skipped":
                icon = "[dim]skipped[/dim]"
            elif status == "running":
                icon = "[cyan]running[/cyan]"
            else:
                icon = f"[dim]{status}[/dim]"

            prefix = ""
            if step.get("is_compensation"):
                prefix = "[dim]<-[/dim] "
            line = f"  [{icon}] {prefix}{step_id}{dur_str}"
            if summary:
                line += f"  {summary}"
            console.print(line)

    # Final status
    run_status = run.get("status", "unknown")
    if run_status == "completed":
        console.print("\n[green]Workflow completed successfully[/green]")
    elif run_status == "compensated":
        console.print("\n[yellow]Workflow compensated[/yellow] (steps rolled back after failure)")
    elif run_status == "compensation_failed":
        console.print(f"\n[red]Workflow compensation failed:[/red] {run.get('stop_reason', 'unknown')}")
    elif run_status == "compensating":
        console.print("\n[cyan]Compensating...[/cyan] (rolling back completed steps)")
    elif run_status == "blocked":
        console.print(f"\n[yellow]Workflow blocked:[/yellow] {run.get('stop_reason', 'unknown')}")
    elif run_status == "failed":
        stop_reason = run.get("stop_reason", "unknown")
        if stop_reason.startswith("budget_exceeded:"):
            dim = stop_reason.split(":", 1)[1]
            console.print(f"\n[red]Workflow stopped:[/red] Budget exceeded ({dim})")
            budget_usage = run.get("budget_usage")
            budget = run.get("budget")
            if budget_usage and budget:
                console.print(
                    f"  Steps: {budget_usage.get('steps_completed', 0)}/{budget.get('max_steps', 0)}, "
                    f"Tokens: {_format_tokens(budget_usage.get('total_tokens', 0))}"
                    f"/{_format_tokens(budget.get('max_tokens', 0))}, "
                    f"Duration: {_format_duration(budget_usage.get('elapsed_seconds', 0))}"
                    f"/{_format_duration(budget.get('max_duration_seconds', 0))}"
                )
        else:
            console.print(f"\n[red]Workflow failed:[/red] {stop_reason}")
    else:
        console.print(f"\n[dim]Workflow status:[/dim] {run_status}")


def _run_workflow(config: AppConfig, args: argparse.Namespace) -> None:
    """Dispatch `aroom workflow` subcommands."""
    action = getattr(args, "workflow_action", None)
    if not action:
        console.print(
            "Usage: aroom workflow"
            " {run,status,list,history,resume,cancel,approve,deny,respond,watch,triggers,schedule,validate,simulate}"
        )
        return

    if action == "validate":
        _handle_validate(args)
        return
    if action == "simulate":
        _handle_simulate(args)
        return

    from ..db import get_db

    db = get_db(config.app.data_dir / "chat.db")

    if action == "run":
        _handle_run(config, db, args)
    elif action == "status":
        _handle_status(db, args)
    elif action == "list":
        _handle_list(config, db, args)
    elif action == "history":
        _handle_history(db, args)
    elif action == "resume":
        _handle_resume(config, db, args)
    elif action == "cancel":
        _handle_cancel(db, args)
    elif action == "approve":
        _handle_approve(db, args)
    elif action == "deny":
        _handle_deny(db, args)
    elif action == "respond":
        _handle_respond(db, args)
    elif action == "watch":
        _handle_watch(db, args)
    elif action == "triggers":
        _handle_triggers(config, db, args)
    elif action == "schedule":
        _handle_schedule(config, db, args)
    else:
        console.print(f"Unknown workflow action: {action}")


def _handle_run(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow run <workflow_id>`."""
    from ..services.workflow_engine import load_definition

    workflow_id = getattr(args, "workflow_name", None)
    if not workflow_id:
        console.print("[red]Error:[/red] workflow name is required")
        return

    # Resolve definition: filesystem path, reference example, or built-in
    path = _resolve_workflow_path(workflow_id)
    if path is None:
        console.print(f"[red]Error:[/red] Workflow not found: {workflow_id!r}")
        console.print("Provide a path to a YAML workflow definition.")
        return

    try:
        definition = load_definition(path)
    except (ValueError, FileNotFoundError) as exc:
        console.print(f"[red]Error loading workflow:[/red] {exc}")
        return

    # Collect inputs from CLI args
    inputs: dict[str, Any] = {}
    issue_number = getattr(args, "issue", None)
    if issue_number is not None:
        inputs["issue_number"] = issue_number

    # Parse --param key=value overrides (#958)
    param_overrides: dict[str, str] = {}
    for raw_param in getattr(args, "param", []):
        if "=" not in raw_param:
            console.print(f"[red]Error:[/red] --param must be KEY=VALUE, got: {raw_param!r}")
            return
        key, _, value = raw_param.partition("=")
        param_overrides[key.strip()] = value.strip()

    # Determine target from inputs or definition
    target_kind = "workflow"
    target_ref = workflow_id
    if "issue_number" in inputs:
        target_kind = "issue"
        target_ref = str(inputs["issue_number"])

    # Dry run: show plan without executing
    if getattr(args, "dry_run", False):
        console.print(f"\n[bold]Workflow:[/bold] {definition.id} v{definition.version}")
        console.print(f"[bold]Target:[/bold] {target_kind}:{target_ref}")
        console.print(f"[bold]Inputs:[/bold] {inputs}")
        console.print(f"\n[bold]Steps ({len(definition.steps)}):[/bold]")
        for i, step in enumerate(definition.steps, 1):
            label = f"  {i}. [{step.type}] {step.id}"
            if step.runner:
                label += f" ({step.runner})"
            console.print(label)
        return

    # Register gate conditions for reference workflows (e.g., issue_delivery).
    # These are GitHub-specific gates — they live in workflows/gates.py,
    # not in the engine core.
    from ..workflows.gates import register_builtin_gates

    register_builtin_gates()

    # Resolve current space for artifact/skill scoping (#957)
    current_space_id: str | None = None
    try:
        from ..services.space_storage import resolve_space_by_cwd

        space = resolve_space_by_cwd(db, str(Path.cwd()))
        if space:
            current_space_id = space["id"]
    except Exception:
        pass

    # Create engine with AI service dependencies, scoped to current space
    engine, _event_bus = _create_engine(config, db, space_id=current_space_id)

    # Set up real-time progress callback for live CLI output
    def _on_progress(event_type: str, step_id: str | None, payload: dict) -> None:
        if event_type == "step_started" and step_id:
            console.print(f"  [cyan]...[/cyan] {step_id}")
        elif event_type == "step_finished" and step_id:
            dur = payload.get("duration_ms", "")
            dur_str = f" ({dur}ms)" if dur else ""
            status = payload.get("result_status", "success")
            if status == "success":
                console.print(f"  [green]done[/green] {step_id}{dur_str}")
            elif status == "blocked":
                console.print(f"  [yellow]blocked[/yellow] {step_id}{dur_str}")
            else:
                console.print(f"  [dim]{status}[/dim] {step_id}{dur_str}")
        elif event_type == "step_failed" and step_id:
            err = payload.get("error", "")[:60]
            console.print(f"  [red]failed[/red] {step_id}  {err}")

    engine.set_progress_callback(_on_progress)

    # Execute
    console.print(f"\n[bold]Starting workflow:[/bold] {definition.id} v{definition.version}")
    console.print(f"[bold]Target:[/bold] {target_kind}:{target_ref}\n")

    try:
        run = asyncio.run(
            engine.start_run(
                definition,
                target_kind=target_kind,
                target_ref=target_ref,
                inputs=inputs,
                space_id=current_space_id,
                param_overrides=param_overrides or None,
            )
        )
    except (ValueError, RuntimeError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        _cleanup_event_bus(_event_bus)
        return

    # Display step-by-step progress report
    _print_run_progress(db, run)

    console.print(f"[dim]Run ID:[/dim] {run['id']}")
    _cleanup_event_bus(_event_bus)


def _handle_status(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow status <run_id>`."""
    from ..services.workflow_storage import count_checkpoints, get_workflow_run, list_workflow_steps

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[red]Error:[/red] run_id is required")
        return

    run = get_workflow_run(db, run_id)
    if not run:
        console.print(f"[red]Error:[/red] Run not found: {run_id}")
        return

    console.print(f"\n[bold]Run:[/bold] {run['id'][:12]}...")
    console.print(f"[bold]Workflow:[/bold] {run['workflow_id']} v{run.get('workflow_version', '?')}")
    console.print(f"[bold]Target:[/bold] {run['target_kind']}:{run['target_ref']}")
    console.print(f"[bold]Status:[/bold] {run['status']}")
    if run.get("stop_reason"):
        console.print(f"[bold]Stop reason:[/bold] {run['stop_reason']}")
    if run.get("current_step_id"):
        console.print(f"[bold]Current step:[/bold] {run['current_step_id']}")
    if run.get("definition_hash"):
        console.print(f"[bold]Definition hash:[/bold] {run['definition_hash'][:12]}...")
    console.print(f"[bold]Created:[/bold] {run['created_at']}")

    checkpoint_count = count_checkpoints(db, run["id"])
    console.print(f"[bold]Checkpoints:[/bold] {checkpoint_count}")

    # Usage and budget display (#963, #967)
    budget = run.get("budget")
    budget_usage = run.get("budget_usage")
    if budget:
        parts = []
        usage = budget_usage or {}
        if budget.get("max_steps"):
            parts.append(f"{usage.get('steps_completed', 0)}/{budget['max_steps']} steps")
        if budget.get("max_tokens"):
            used_t = usage.get("total_tokens", 0)
            max_t = budget["max_tokens"]
            parts.append(f"{_format_tokens(used_t)}/{_format_tokens(max_t)} tokens")
        if budget.get("max_duration_seconds"):
            elapsed = usage.get("elapsed_seconds", 0)
            max_d = budget["max_duration_seconds"]
            parts.append(f"{_format_duration(elapsed)}/{_format_duration(max_d)}")
        if parts:
            console.print(f"[bold]Budget:[/bold] {', '.join(parts)}")
    if budget_usage:
        usage = budget_usage
        total_t = usage.get("total_tokens", 0)
        if total_t and not budget:
            console.print(
                f"[bold]Tokens:[/bold] {_format_tokens(total_t)} "
                f"({_format_tokens(usage.get('prompt_tokens', 0))} in / "
                f"{_format_tokens(usage.get('completion_tokens', 0))} out)"
            )
        cost = usage.get("estimated_cost_usd", 0.0)
        if cost > 0:
            console.print(f"[bold]Est. cost:[/bold] ${cost:.4f}")

    steps = list_workflow_steps(db, run["id"])
    if steps:
        console.print(f"\n[bold]Steps ({len(steps)}):[/bold]")
        table = Table(show_header=True)
        table.add_column("Step", style="bold")
        table.add_column("Type")
        table.add_column("Status")
        table.add_column("Duration")
        table.add_column("Summary", max_width=60)
        for step in steps:
            dur = f"{step['duration_ms']}ms" if step.get("duration_ms") else "-"
            step_type_display = step["step_type"]
            result_artifacts = step.get("result_artifacts") or {}
            if result_artifacts.get("structured_output") is not None:
                step_type_display += " (json)"
            table.add_row(
                step["step_id"],
                step_type_display,
                step["status"],
                dur,
                (step.get("result_summary") or "")[:60],
            )
        console.print(table)


def _handle_list(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow list`."""
    from ..services.workflow_storage import check_approval_timeouts, check_decision_timeouts, list_workflow_runs

    # On-demand timeout checks
    check_approval_timeouts(db)
    check_decision_timeouts(db)

    # Recover stale runs before listing (on-demand recovery)
    engine, _event_bus = _create_engine(config, db)
    recovered = asyncio.run(engine.recover_interrupted_runs())
    if recovered:
        console.print(f"[yellow]Recovered {len(recovered)} interrupted run(s)[/yellow]")

    status_filter = getattr(args, "status", None)
    workflow_filter = getattr(args, "workflow", None)
    limit = getattr(args, "limit", 20) or 20

    runs = list_workflow_runs(db, status=status_filter, workflow_id=workflow_filter, limit=limit)

    if not runs:
        console.print("[dim]No workflow runs found.[/dim]")
        return

    table = Table(title="Workflow Runs", show_header=True)
    table.add_column("ID", style="dim", max_width=12)
    table.add_column("Workflow")
    table.add_column("Target", max_width=40)
    table.add_column("Status")
    table.add_column("Step")
    table.add_column("Created")

    for run in runs:
        # Shorten long target refs (e.g., temp file paths from tests)
        target_ref = run["target_ref"]
        if len(target_ref) > 35:
            target_ref = "..." + target_ref[-32:]
        table.add_row(
            run["id"][:12],
            run["workflow_id"],
            f"{run['target_kind']}:{target_ref}",
            run["status"],
            run.get("current_step_id") or "-",
            run["created_at"][:19],
        )

    console.print(table)
    _cleanup_event_bus(_event_bus)


def _handle_history(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow history <run_id>`."""
    from ..services.workflow_storage import (
        get_workflow_run,
        list_checkpoints,
        list_workflow_events,
        list_workflow_steps,
    )

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[red]Error:[/red] run_id is required")
        return

    run = get_workflow_run(db, run_id)
    if not run:
        console.print(f"[red]Error:[/red] Run not found: {run_id}")
        return

    console.print(f"\n[bold]Run History:[/bold] {run['id'][:12]}...")
    console.print(f"[bold]Workflow:[/bold] {run['workflow_id']} — Status: {run['status']}")

    steps = list_workflow_steps(db, run["id"])
    if steps:
        console.print("\n[bold]Steps:[/bold]")
        table = Table(show_header=True)
        table.add_column("Step", style="bold")
        table.add_column("Type")
        table.add_column("Runner")
        table.add_column("Status")
        table.add_column("Result")
        table.add_column("Duration")
        table.add_column("Tokens")
        table.add_column("Idem. Key", max_width=30)
        table.add_column("Summary", max_width=50)
        for step in steps:
            dur = f"{step['duration_ms']}ms" if step.get("duration_ms") else "-"
            artifacts = step.get("result_artifacts") or {}
            tokens = _format_tokens(artifacts["total_tokens"]) if artifacts.get("total_tokens") else "-"
            idem_key = step.get("idempotency_key") or "-"
            step_type_display = step["step_type"]
            if artifacts.get("structured_output") is not None:
                step_type_display += " (json)"
            step_id_display = step["step_id"]
            if step.get("is_compensation"):
                step_id_display = f"<- {step_id_display}"
            table.add_row(
                step_id_display,
                step_type_display,
                step.get("runner_type") or "-",
                step["status"],
                step.get("result_status") or "-",
                dur,
                tokens,
                idem_key[:30] if len(idem_key) > 30 else idem_key,
                (step.get("result_summary") or "")[:50],
            )
        console.print(table)

    checkpoints = list_checkpoints(db, run["id"])
    if checkpoints:
        console.print(f"\n[bold]Checkpoints ({len(checkpoints)}):[/bold]")
        cp_table = Table(show_header=True)
        cp_table.add_column("Label", style="bold")
        cp_table.add_column("Step")
        cp_table.add_column("Status")
        cp_table.add_column("Time")
        for cp in checkpoints:
            cp_table.add_row(
                cp["label"],
                cp.get("step_id") or "-",
                cp["run_status"],
                cp["created_at"][:19],
            )
        console.print(cp_table)

    events = list_workflow_events(db, run["id"])
    if events:
        console.print(f"\n[bold]Events ({len(events)}):[/bold]")
        table = Table(show_header=True)
        table.add_column("ID", style="dim")
        table.add_column("Type")
        table.add_column("Step")
        table.add_column("Time")
        for event in events:
            table.add_row(
                str(event["id"]),
                event["event_type"],
                event.get("step_id") or "-",
                event["created_at"][:19],
            )
        console.print(table)


def _handle_resume(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow resume <run_id>`."""
    from ..services.workflow_engine import load_definition
    from ..services.workflow_storage import check_approval_timeouts, check_decision_timeouts, get_workflow_run

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[red]Error:[/red] run_id is required")
        return

    # On-demand timeout checks
    check_approval_timeouts(db)
    check_decision_timeouts(db)

    # Load run FIRST to extract space_id for scoped registry rebuild (#957)
    run = get_workflow_run(db, run_id)
    if not run:
        console.print(f"[red]Error:[/red] Run not found: {run_id}")
        return

    # Create engine scoped to the run's space_id (#957 resume stability)
    run_space_id = run.get("space_id")
    engine, _event_bus = _create_engine(config, db, space_id=run_space_id)

    # Recover any stale runs first (on-demand recovery)
    asyncio.run(engine.recover_interrupted_runs())

    if run["status"] not in ("paused", "waiting_for_approval", "waiting_for_input"):
        console.print(
            f"[red]Error:[/red] Run is not resumable (status: {run['status']}). "
            "Only paused or waiting_for_approval runs can be resumed."
        )
        return

    # Resolve definition
    definition_path = getattr(args, "definition", None)
    workflow_id = run.get("workflow_id", "")

    if definition_path:
        path = Path(definition_path)
    else:
        path = _resolve_workflow_path(workflow_id)

    if not path:
        console.print(
            f"[red]Error:[/red] Cannot find workflow definition for '{workflow_id}'. "
            "Pass --definition <path> for custom workflows."
        )
        return

    try:
        definition = load_definition(path)
    except (ValueError, FileNotFoundError) as exc:
        console.print(f"[red]Error loading workflow:[/red] {exc}")
        return

    from_step = getattr(args, "from_step", None)
    force = getattr(args, "force", False)

    # Register gates
    from ..workflows.gates import register_builtin_gates

    register_builtin_gates()

    console.print(f"\n[bold]Resuming workflow:[/bold] {definition.id}")
    console.print(f"[bold]Run:[/bold] {run_id[:12]}...")
    if from_step:
        console.print(f"[bold]From step:[/bold] {from_step}")
    if force:
        console.print("[yellow]Force mode: definition drift will be overridden[/yellow]")

    try:
        result = asyncio.run(
            engine.resume_run(
                run_id,
                definition,
                from_step=from_step,
                force=force,
            )
        )
    except (ValueError, RuntimeError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        _cleanup_event_bus(_event_bus)
        return

    _print_run_progress(db, result)
    _cleanup_event_bus(_event_bus)


def _handle_cancel(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow cancel <run_id>`. Paused runs only in V1."""
    from ..services.workflow_storage import (
        create_workflow_event,
        get_workflow_run,
        release_lock,
        update_workflow_run,
    )

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[red]Error:[/red] run_id is required")
        return

    run = get_workflow_run(db, run_id)
    if not run:
        console.print(f"[red]Error:[/red] Run not found: {run_id}")
        return

    if run["status"] == "running":
        console.print(
            "[red]Error:[/red] Cannot cancel an active run from another terminal. "
            "Use Ctrl-C in the terminal running the workflow."
        )
        return

    if run["status"] not in ("paused", "waiting_for_approval", "waiting_for_input"):
        console.print(
            f"[red]Error:[/red] Run is not cancellable (status: {run['status']}). "
            "Only paused or waiting_for_approval runs can be cancelled."
        )
        return

    update_workflow_run(db, run_id, status="cancelled")
    release_lock(db, run_id=run_id)
    create_workflow_event(
        db,
        run_id=run_id,
        event_type="run_cancelled",
        payload={"cancelled_from_status": run["status"]},
    )
    console.print(f"[green]Run {run_id[:12]}... cancelled[/green]")


def _handle_approve(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow approve <run_id>`. Approve a pending tool approval request."""
    from ..services.workflow_storage import (
        check_approval_timeouts,
        get_pending_approval,
        get_workflow_run,
        resolve_approval_request,
    )

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[red]Error:[/red] run_id is required")
        return

    check_approval_timeouts(db)

    run = get_workflow_run(db, run_id)
    if not run:
        console.print(f"[red]Error:[/red] Run not found: {run_id}")
        return

    pending = get_pending_approval(db, run_id)
    if not pending:
        console.print(f"[yellow]No pending approval request for run {run_id[:12]}...[/yellow]")
        return

    console.print("\n[bold]Pending tool approval:[/bold]")
    console.print(f"  Tool: {pending['tool_name']}")
    console.print(f"  Risk tier: {pending['risk_tier']}")
    if pending.get("tool_args"):
        import json

        console.print(f"  Args: {json.dumps(pending['tool_args'], indent=2)[:200]}")

    resolved = resolve_approval_request(db, pending["id"], status="approved", resolved_by="operator")
    if resolved:
        console.print(f"\n[green]Approved.[/green] Use 'aroom workflow resume {run_id}' to continue.")
    else:
        console.print("[red]Error:[/red] Could not resolve approval request.")


def _handle_deny(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow deny <run_id>`. Deny a pending tool approval request."""
    from ..services.workflow_storage import (
        check_approval_timeouts,
        get_pending_approval,
        get_workflow_run,
        resolve_approval_request,
        update_workflow_run,
    )

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[red]Error:[/red] run_id is required")
        return

    check_approval_timeouts(db)

    run = get_workflow_run(db, run_id)
    if not run:
        console.print(f"[red]Error:[/red] Run not found: {run_id}")
        return

    pending = get_pending_approval(db, run_id)
    if not pending:
        console.print(f"[yellow]No pending approval request for run {run_id[:12]}...[/yellow]")
        return

    reason = getattr(args, "reason", None) or "denied by operator"
    resolve_approval_request(db, pending["id"], status="denied", resolved_by="operator")
    update_workflow_run(db, run_id, status="paused", stop_reason=f"approval_denied: {reason}")
    console.print(f"[yellow]Denied.[/yellow] Run {run_id[:12]}... moved to paused.")


def _handle_respond(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow respond <run_id>`. Respond to a human gate decision."""
    from ..services.workflow_storage import (
        check_decision_timeouts,
        get_pending_decision,
        get_workflow_run,
        resolve_human_decision,
    )

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[red]Error:[/red] run_id is required")
        return

    check_decision_timeouts(db)

    run = get_workflow_run(db, run_id)
    if not run:
        console.print(f"[red]Error:[/red] Run not found: {run_id}")
        return

    pending = get_pending_decision(db, run_id)
    if not pending:
        console.print(f"[yellow]No pending human decision for run {run_id[:12]}...[/yellow]")
        return

    console.print("\n[bold]Pending decision:[/bold]")
    console.print(f"  {pending['prompt']}")
    if pending.get("context"):
        console.print(f"\n  [dim]Context:[/dim]\n  {pending['context'][:300]}")
    console.print("\n[bold]Options:[/bold]")
    options = pending.get("options", [])
    for i, opt in enumerate(options, 1):
        console.print(f"  {i}. [{opt.get('id')}] {opt.get('label')}")

    option_id = getattr(args, "option", None)
    if not option_id:
        console.print(
            f"\nPass --option <option_id> to respond."
            f" Example: aroom workflow respond {run_id} --option {options[0]['id'] if options else 'approve'}"
        )
        return

    valid_ids = {o["id"] for o in options}
    if option_id not in valid_ids:
        console.print(f"[red]Error:[/red] Invalid option '{option_id}'. Valid: {', '.join(valid_ids)}")
        return

    resolved = resolve_human_decision(db, pending["id"], selected_option=option_id, resolved_by="operator")
    if resolved:
        console.print(f"\n[green]Decision recorded: {option_id}[/green]")
        console.print(f"Use 'aroom workflow resume {run_id}' to continue.")
    else:
        console.print("[red]Error:[/red] Could not resolve decision.")


def _handle_watch(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow watch <run_id>`. Poll and display live progress."""
    import time

    from ..services.workflow_storage import (
        get_workflow_run,
        list_workflow_events,
        list_workflow_steps,
    )

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[red]Error:[/red] run_id is required")
        return

    run = get_workflow_run(db, run_id)
    if not run:
        console.print(f"[red]Error:[/red] Run not found: {run_id}")
        return

    terminal_statuses = {"completed", "failed", "cancelled", "blocked"}
    seen_events: set[int] = set()
    console.print(f"[bold]Watching run {run_id[:12]}...[/bold] (Ctrl+C to stop)\n")

    try:
        while True:
            run = get_workflow_run(db, run_id)
            if not run:
                console.print("[red]Run deleted[/red]")
                break

            steps = list_workflow_steps(db, run_id)
            events = list_workflow_events(db, run_id)

            # Print new events
            for event in events:
                eid = event.get("id", 0)
                if eid not in seen_events:
                    seen_events.add(eid)
                    etype = event.get("event_type", "")
                    step = event.get("step_id") or ""
                    step_str = f" [{step}]" if step else ""
                    console.print(f"  {etype}{step_str}")

            # Show current status
            status = run.get("status", "unknown")
            step_summary = ", ".join(f"{s['step_id']}={s['status']}" for s in steps[-3:]) if steps else "no steps"
            console.print(
                f"  [dim]status={status} | {step_summary}[/dim]",
                end="\r",
            )

            if status in terminal_statuses:
                console.print(f"\n\n[bold]Run {status}[/bold]")
                if run.get("stop_reason"):
                    console.print(f"  Reason: {run['stop_reason']}")
                break

            time.sleep(2)
    except KeyboardInterrupt:
        console.print("\n[yellow]Watch stopped[/yellow]")


def _handle_triggers(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow triggers <subaction>`."""
    import asyncio

    from ..services.workflow_storage import (
        get_schedule,
        list_schedules,
        update_schedule,
    )

    trigger_action = getattr(args, "trigger_action", None)
    if not trigger_action:
        console.print("Usage: aroom workflow triggers {list|fire|enable|disable}")
        return

    if trigger_action == "list":
        schedules = list_schedules(db)
        if not schedules:
            console.print("[dim]No workflow schedules[/dim]")
            return
        console.print("[bold]Workflow Schedules[/bold]\n")
        for s in schedules:
            enabled = "[green]on[/green]" if s.get("enabled") else "[red]off[/red]"
            console.print(
                f"  {s['id'][:12]}...  {enabled}  {s['cron_expr']:<15}  "
                f"{s['workflow_ref']}  next={s.get('next_run_at', 'N/A')}"
            )

    elif trigger_action == "fire":
        schedule_id = getattr(args, "schedule_id", None)
        if not schedule_id:
            console.print("[red]Error:[/red] schedule_id is required")
            return
        sched = get_schedule(db, schedule_id)
        if not sched:
            console.print(f"[red]Error:[/red] Schedule not found: {schedule_id}")
            return

        from ..services.workflow_engine import load_definition
        from ..services.workflow_resolution import resolve_workflow_path

        path = resolve_workflow_path(sched["workflow_ref"])
        if not path:
            console.print(f"[red]Error:[/red] Workflow not found: {sched['workflow_ref']}")
            return
        definition = load_definition(path)
        engine, event_bus = _create_engine(config, db)
        try:
            run = asyncio.run(
                engine.enqueue_run(
                    definition,
                    target_kind=sched.get("target_kind") or "generic",
                    target_ref=sched["target_ref"],
                    inputs=sched.get("inputs"),
                    trigger_source="manual",
                    trigger_meta={"schedule_id": schedule_id},
                )
            )
            console.print(f"[green]Enqueued run {run['id']}[/green] from schedule {schedule_id[:12]}...")
        finally:
            _cleanup_event_bus(event_bus)

    elif trigger_action in ("enable", "disable"):
        schedule_id = getattr(args, "schedule_id", None)
        if not schedule_id:
            console.print("[red]Error:[/red] schedule_id is required")
            return
        enabled = 1 if trigger_action == "enable" else 0
        result = update_schedule(db, schedule_id, enabled=enabled)
        if result:
            state = "enabled" if enabled else "disabled"
            console.print(f"[green]Schedule {schedule_id[:12]}... {state}[/green]")
        else:
            console.print(f"[red]Error:[/red] Schedule not found: {schedule_id}")

    else:
        console.print(f"Unknown trigger action: {trigger_action}")


def _handle_schedule(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow schedule <path>`. Register triggers from a workflow definition."""
    from datetime import datetime, timezone

    from ..services.cron import min_interval_seconds, parse_cron
    from ..services.workflow_engine import load_definition
    from ..services.workflow_resolution import resolve_workflow_path
    from ..services.workflow_storage import create_schedule

    workflow_path = getattr(args, "workflow_path", None)
    if not workflow_path:
        console.print("[red]Error:[/red] workflow path is required")
        return

    path = resolve_workflow_path(workflow_path)
    if not path:
        console.print(f"[red]Error:[/red] Workflow not found: {workflow_path}")
        return

    definition = load_definition(path)
    if not definition.triggers:
        console.print("[yellow]No triggers defined in this workflow[/yellow]")
        return

    min_interval = config.workflow.min_schedule_interval
    now = datetime.now(timezone.utc)

    for trigger in definition.triggers:
        if trigger.type != "schedule":
            console.print(f"[yellow]Skipping non-schedule trigger type: {trigger.type}[/yellow]")
            continue

        if not trigger.cron:
            console.print("[red]Error:[/red] Schedule trigger missing cron expression")
            continue

        try:
            cron = parse_cron(trigger.cron)
        except ValueError as e:
            console.print(f"[red]Error:[/red] Invalid cron: {e}")
            continue

        interval = min_interval_seconds(cron)
        if interval < min_interval:
            console.print(
                f"[red]Error:[/red] Cron {trigger.cron!r} fires every {interval}s, minimum is {min_interval}s"
            )
            continue

        # Determine ref_type
        ref_type = "path" if str(path).endswith((".yaml", ".yml")) else "builtin"
        workflow_ref = str(path) if ref_type == "path" else definition.id

        # Path confinement at registration time — reject paths the scheduler would later reject
        if ref_type == "path":
            from ..services.workflow_scheduler import _confine_path

            try:
                _confine_path(workflow_ref)
            except ValueError as e:
                console.print(f"[red]Error:[/red] {e}")
                continue

        next_at = cron.next_occurrence(now)
        target_ref = trigger.target_ref or "default"
        missed_policy = trigger.missed_policy or "skip"

        schedule = create_schedule(
            db,
            workflow_ref=workflow_ref,
            ref_type=ref_type,
            cron_expr=trigger.cron,
            target_ref=target_ref,
            next_run_at=next_at.isoformat(),
            target_kind=trigger.target_kind or "generic",
            inputs=trigger.inputs,
            missed_policy=missed_policy,
            min_interval_seconds=min_interval,
        )
        console.print(
            f"[green]Schedule created: {schedule['id']}[/green]  cron={trigger.cron}  next={next_at.isoformat()}"
        )


def _handle_validate(args: argparse.Namespace) -> None:
    """Validate a workflow definition without executing it (#968)."""
    from ..services.workflow_simulator import WorkflowSimulator

    path = getattr(args, "workflow_path", None)
    if not path:
        console.print("[red]Usage: aroom workflow validate <workflow_path>[/red]")
        return

    simulator = WorkflowSimulator()
    result = simulator.validate(path)

    if result.is_valid:
        defn = result.definition
        step_count = len(defn.steps) if defn else 0
        console.print(f"[green]Valid[/green]: {path} ({step_count} steps)")
        if result.warnings:
            for w in result.warnings:
                console.print(f"  [yellow]Warning[/yellow]: {w}")
    else:
        console.print(f"[red]Invalid[/red]: {path}")
        for e in result.errors:
            console.print(f"  [red]Error[/red]: {e}")


def _handle_simulate(args: argparse.Namespace) -> None:
    """Simulate a workflow with stub runners (#968)."""
    import yaml

    from ..services.workflow_simulator import WorkflowSimulator

    path = getattr(args, "workflow_path", None)
    if not path:
        console.print("[red]Usage: aroom workflow simulate <workflow_path>[/red]")
        return

    stubs_path = getattr(args, "stubs", None)
    stub_results: dict[str, dict[str, Any]] = {}
    if stubs_path:
        from pathlib import Path

        stubs_file = Path(stubs_path)
        if not stubs_file.exists():
            console.print(f"[red]Stubs file not found: {stubs_path}[/red]")
            return
        with open(stubs_file) as f:
            stub_results = yaml.safe_load(f) or {}

    simulator = WorkflowSimulator(stub_results=stub_results)

    # Validate first
    vr = simulator.validate(path)
    if not vr.is_valid:
        console.print("[red]Definition invalid — cannot simulate[/red]")
        for e in vr.errors:
            console.print(f"  [red]Error[/red]: {e}")
        return

    console.print(f"[blue]Simulating[/blue]: {path}")
    result = simulator.simulate(path)

    for step in result.steps_executed:
        status_color = "green" if step.get("result_status") == "success" else "red"
        step_id = step.get("step_id", "?")
        result_status = step.get("result_status", "?")
        console.print(f"  [{status_color}]{result_status}[/{status_color}] {step_id}")

    status_color = "green" if result.final_status == "completed" else "red"
    console.print(f"\n[{status_color}]Final status: {result.final_status}[/{status_color}]")
    if result.error:
        console.print(f"  [red]Error[/red]: {result.error}")
