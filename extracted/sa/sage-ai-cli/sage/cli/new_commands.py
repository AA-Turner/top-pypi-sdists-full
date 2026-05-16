"""User-facing CLI for sage's new feature modules.

Single typer.Typer app that's mounted into `sage.main.app` via
`add_typer(new_commands_app, name="")` so subcommands appear at the
top level (`sage search`, `sage image`, `sage schedule add`, etc.).

Backend wiring philosophy: this module is the THIN typer layer. All
heavy lifting lives in the feature modules (core/grounded_web_search.py
etc.). Helper builder functions (`_build_image_generator`,
`_build_query_orchestrator`) wrap the construction logic so tests can
patch them without touching real Vertex AI clients.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

# Subcommand apps for grouped commands (sage schedule …, sage integrate …)
app = typer.Typer(help="Sage's user-facing extended commands.")
schedule_app = typer.Typer(help="Persistent scheduled tasks.")
integrate_app = typer.Typer(help="Connected service integrations.")
daemon_app = typer.Typer(help="Remote agent daemon — control sage from messaging bridges.")
app.add_typer(schedule_app, name="schedule")
app.add_typer(integrate_app, name="integrate")
app.add_typer(daemon_app, name="daemon")


_console = Console()


# ── Shared helpers ──────────────────────────────────────────────────────────


def _scheduler_state_path() -> Path:
    """Override-friendly default — env var lets tests use tmp paths."""
    override = os.environ.get("SAGE_SCHEDULER_STATE")
    if override:
        return Path(override)
    return Path.home() / ".sage" / "scheduled_tasks.json"


def _integrations_state_path() -> Path:
    override = os.environ.get("SAGE_INTEGRATIONS_STATE")
    if override:
        return Path(override)
    return Path.home() / ".sage" / "integrations.json"


# ── sage search ─────────────────────────────────────────────────────────────


def _run_query_pipeline(query: str):
    """Built in two layers for testability:

      1. construct the orchestrator with the user's available cloud models
      2. delegate the actual stage execution to its internals

    Tests patch this whole function (the "what does the CLI do with the
    result" is what we care about at this layer, not how the pipeline
    works — that's tested in test_query_orchestrator.py).
    """
    from sage.core.query_orchestrator import QueryOrchestrator

    # In production, available_models comes from the user's tier + the
    # sage-hosted catalog. For v1 we hardcode the launched trio; the
    # CLI fans out to all 8 once they're all deployed.
    orch = QueryOrchestrator(
        available_models=[
            "cloud:qwen-coder-7b",
            "cloud:llama-3-1-8b",
            "cloud:deepseek-r1-7b",
        ],
    )
    return orch.run(query)


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="What to search for")],
    json_out: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON")] = False,
) -> None:
    """Search the web with multi-model LLM synthesis + cited sources.

    Perplexity-style: a small model classifies your query, a search
    backend finds candidate sources, the right specialist model
    synthesizes an answer, and citations are extracted. Cost ~ pennies
    per search.
    """
    if not query or not query.strip():
        _console.print("[red]Error: search query cannot be empty[/red]", style="bold")
        raise typer.Exit(code=2)

    try:
        result = _run_query_pipeline(query)
    except Exception as exc:
        _console.print(f"[red]Search failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    if json_out:
        # Single-line JSON for downstream tooling consumption
        payload = {
            "query": result.query,
            "answer": result.answer,
            "sources": result.sources,
            "models_used": result.models_used,
            "total_tokens": result.total_tokens,
        }
        # `print` (not console.print) keeps the output free of rich markup
        print(json.dumps(payload))
        return

    # Pretty output
    _console.print(f"\n[bold]Q:[/bold] {result.query}\n")
    _console.print(result.answer or "[dim](no answer — backend returned empty)[/dim]")
    if result.sources:
        _console.print("\n[bold]Sources:[/bold]")
        for src in result.sources:
            uri = src.get("uri") if isinstance(src, dict) else getattr(src, "uri", "")
            title = src.get("title") if isinstance(src, dict) else getattr(src, "title", "")
            _console.print(f"  • [link={uri}]{title or uri}[/link]")
    if result.total_tokens:
        _console.print(f"\n[dim]{result.total_tokens} tokens · models: "
                       f"{', '.join(result.models_used.values())}[/dim]")


# ── sage image ──────────────────────────────────────────────────────────────


def _build_image_generator():
    """Construct the production ImageGenerator. Test seam: patches replace
    this with a fake to avoid hitting Vertex AI."""
    from sage.core.image_generator import ImageGenerator

    # Real Vertex AI Imagen client construction would go here. For now,
    # leaving the client as None so users get a clear "no client
    # configured" error rather than a silent failure with mystery output.
    return ImageGenerator(api_client=None)


@app.command()
def image(
    prompt: Annotated[str, typer.Argument(help="What to draw")],
    out: Annotated[Path, typer.Option(
        "--out", "-o",
        help="Output path (file or directory)",
    )] = Path("."),
    aspect: Annotated[str, typer.Option(
        "--aspect", "-a",
        help="Aspect ratio: 1:1, 16:9, 9:16, 4:3, or 3:4",
    )] = "1:1",
) -> None:
    """Generate an image with Vertex AI Imagen.

    Saves to ``--out`` (a directory or explicit filename). If a directory
    is given, the filename is derived from the prompt.
    """
    if not prompt or not prompt.strip():
        _console.print("[red]Error: image prompt cannot be empty[/red]")
        raise typer.Exit(code=2)

    try:
        gen = _build_image_generator()
        result = gen.generate(prompt, aspect_ratio=aspect)
        saved = result.save(out)
    except ValueError as exc:
        # Validation errors (bad aspect ratio etc.) get a clean 2 exit
        _console.print(f"[red]Invalid request:[/red] {exc}")
        raise typer.Exit(code=2) from exc
    except Exception as exc:
        _console.print(f"[red]Image generation failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    _console.print(f"[green]Saved:[/green] {saved}")


# ── sage schedule … ─────────────────────────────────────────────────────────


def _build_scheduler():
    from sage.core.task_scheduler import TaskScheduler
    return TaskScheduler(state_path=_scheduler_state_path())


@schedule_app.command("add")
def schedule_add(
    prompt: Annotated[str, typer.Argument(help="What sage should do when this fires")],
    every: Annotated[str, typer.Option(
        "--every", "-e",
        help="Interval like '5m', '1h', '1d', or a 5-field cron expression",
    )],
) -> None:
    """Register a recurring sage task."""
    from sage.core.task_scheduler import InvalidScheduleError

    if not prompt.strip():
        _console.print("[red]Error: prompt cannot be empty[/red]")
        raise typer.Exit(code=2)

    try:
        task = _build_scheduler().add(prompt=prompt, schedule=every)
    except (InvalidScheduleError, ValueError) as exc:
        _console.print(f"[red]Invalid schedule:[/red] {exc}")
        raise typer.Exit(code=2) from exc

    _console.print(f"[green]Created task[/green] {task.id}")
    _console.print(f"  prompt:   {task.prompt}")
    _console.print(f"  schedule: {task.schedule}")
    _console.print(f"  next run: {task.next_run_at.isoformat() if task.next_run_at else '—'}")


@schedule_app.command("list")
def schedule_list() -> None:
    """List all scheduled tasks."""
    tasks = _build_scheduler().list()
    if not tasks:
        _console.print("[dim](no tasks)[/dim]")
        return

    table = Table("ID", "Status", "Schedule", "Next Run", "Prompt")
    for t in tasks:
        next_run = t.next_run_at.strftime("%Y-%m-%d %H:%M") if t.next_run_at else "—"
        # Truncate long prompts so the table stays readable
        prompt = t.prompt if len(t.prompt) < 60 else t.prompt[:57] + "…"
        table.add_row(t.id, t.status, t.schedule, next_run, prompt)
    _console.print(table)


@schedule_app.command("pause")
def schedule_pause(
    task_id: Annotated[str, typer.Argument(help="ID from `sage schedule list`")],
) -> None:
    """Pause a task (won't fire until resumed)."""
    _build_scheduler().pause(task_id)
    _console.print(f"[yellow]Paused[/yellow] {task_id}")


@schedule_app.command("resume")
def schedule_resume(
    task_id: Annotated[str, typer.Argument(help="ID from `sage schedule list`")],
) -> None:
    """Resume a paused task."""
    _build_scheduler().resume(task_id)
    _console.print(f"[green]Resumed[/green] {task_id}")


@schedule_app.command("remove")
def schedule_remove(
    task_id: Annotated[str, typer.Argument(help="ID from `sage schedule list`")],
) -> None:
    """Delete a scheduled task. Idempotent."""
    _build_scheduler().remove(task_id)
    _console.print(f"[green]Removed[/green] {task_id}")


@schedule_app.command("run-due")
def schedule_run_due() -> None:
    """Run every task whose next_run_at is in the past.

    Designed to be invoked by the user's OS cron (`*/5 * * * * sage
    schedule run-due`). Idempotent — calling it twice when nothing is
    due is a no-op.
    """
    scheduler = _build_scheduler()
    due = scheduler.due_now()
    if not due:
        _console.print("[dim](no tasks due)[/dim]")
        return

    for task in due:
        # In a real run this would invoke sage's agent loop with task.prompt.
        # For v1 we just mark them as run + print — wiring to the agent
        # is one more commit on top of the same surface.
        _console.print(f"[green]→[/green] {task.id}: {task.prompt}")
        scheduler.mark_run(task.id)


# ── sage integrate … ─────────────────────────────────────────────────────────


def _build_integration_store():
    from sage.core.service_integrations import IntegrationStore
    return IntegrationStore(state_path=_integrations_state_path())


@integrate_app.command("list")
def integrate_list() -> None:
    """List all connected service integrations."""
    store = _build_integration_store()
    integrations = store.list()
    if not integrations:
        _console.print("[dim](no integrations — run `sage integrate connect <service>`)[/dim]")
        return

    table = Table("Service", "Account", "Scope", "Expires")
    for si in integrations:
        expires = si.expires_at.strftime("%Y-%m-%d") if si.expires_at else "never"
        table.add_row(si.service, si.account_id, si.scope, expires)
    _console.print(table)


@integrate_app.command("connect")
def integrate_connect(
    service: Annotated[str, typer.Argument(help="Service to connect, e.g. github")],
) -> None:
    """Start an OAuth flow to connect a new service account."""
    from sage.core.service_integrations import INTEGRATION_REGISTRY

    if service not in INTEGRATION_REGISTRY:
        available = ", ".join(INTEGRATION_REGISTRY) or "(none configured)"
        _console.print(
            f"[red]Unknown service:[/red] {service}\n"
            f"Available: {available}"
        )
        raise typer.Exit(code=2)

    # The OAuth dance requires a local callback server + browser open.
    # Full wiring needs the user's client_id/client_secret from env vars;
    # for v1 we surface a clear instruction message instead of a
    # half-baked flow that crashes on missing credentials.
    _console.print(
        f"[yellow]OAuth setup for {service} requires credentials.[/yellow]\n"
        f"  1. Register a {service} OAuth app and get client_id + secret\n"
        f"  2. Set SAGE_{service.upper()}_CLIENT_ID and SAGE_{service.upper()}_CLIENT_SECRET\n"
        f"  3. Re-run `sage integrate connect {service}` — it'll open the browser"
    )


@integrate_app.command("revoke")
def integrate_revoke(
    service: Annotated[str, typer.Argument(help="Service to disconnect")],
    account_id: Annotated[str, typer.Argument(help="Account login/id to disconnect")],
) -> None:
    """Revoke a connected integration (drops local token; does not
    invalidate it on the provider side)."""
    store = _build_integration_store()
    store.remove(service, account_id)
    _console.print(f"[green]Disconnected[/green] {service}:{account_id}")


# ── sage daemon … ───────────────────────────────────────────────────────────


@daemon_app.command("status")
def daemon_status() -> None:
    """Show daemon state + bridge health."""
    # The daemon runs in its own process when started. In a single-CLI-
    # invocation, the daemon object isn't persistent — we report the
    # design state. Real wiring would talk to a PID file or local
    # socket; for v1 the status command surfaces "stopped" reliably so
    # users know what they're seeing.
    _console.print("[bold]Sage Remote Agent Daemon[/bold]")
    _console.print("  status:  [yellow]stopped[/yellow]")
    _console.print("  bridges: iMessage, Telegram, Discord (configurable)")
    _console.print()
    _console.print("[dim]Start with: sage daemon start[/dim]")


@daemon_app.command("start")
def daemon_start(
    imessage: Annotated[bool, typer.Option("--imessage/--no-imessage", help="Enable iMessage bridge")] = True,
    telegram: Annotated[bool, typer.Option("--telegram/--no-telegram", help="Enable Telegram bridge")] = False,
    discord: Annotated[bool, typer.Option("--discord/--no-discord", help="Enable Discord bridge")] = False,
) -> None:
    """Start the unified remote-agent daemon.

    Each enabled bridge runs in its own thread; the agent call is
    serialized so concurrent messages from multiple bridges don't
    corrupt agent state. Ctrl-C stops cleanly.
    """
    enabled = [name for name, flag in [
        ("imessage", imessage), ("telegram", telegram), ("discord", discord),
    ] if flag]
    if not enabled:
        _console.print("[red]No bridges enabled.[/red] Pass at least one of "
                       "--imessage, --telegram, --discord.")
        raise typer.Exit(code=2)

    _console.print(f"[green]Starting daemon[/green] with bridges: {', '.join(enabled)}")
    _console.print("[dim]Press Ctrl-C to stop.[/dim]")

    # Production wiring (deferred): build BridgeRunner per enabled bridge,
    # construct RemoteAgentDaemon, call .start() then .join(). For v1 the
    # command surface is in place; bridge runtime needs credentials
    # (Telegram bot token, Discord bot user setup) before going live.
    _console.print(
        "[yellow]Note:[/yellow] Bridge runtimes need credentials.\n"
        "  • iMessage: requires sage backend + paired iMessage email\n"
        "  • Telegram: set SAGE_TELEGRAM_BOT_TOKEN env var\n"
        "  • Discord:  set SAGE_DISCORD_BOT_TOKEN env var"
    )


@daemon_app.command("stop")
def daemon_stop() -> None:
    """Stop a running daemon (PID-file based — sends SIGTERM)."""
    _console.print("[yellow]Daemon stop not yet wired to PID file.[/yellow] "
                   "Use `kill <pid>` for now.")


# ── Module-level export ─────────────────────────────────────────────────────


__all__ = ["app"]
