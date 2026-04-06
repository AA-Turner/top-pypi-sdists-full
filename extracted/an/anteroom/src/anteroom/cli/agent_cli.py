"""CLI handlers for /agent subcommands (#1314)."""

from __future__ import annotations

from typing import Any

from rich.table import Table


def handle_agent_list(db: Any, conversation_id: str, renderer: Any) -> None:
    """List detached agent runs for the current conversation."""
    from ..services.detached_subagent_manager import DetachedSubagentManager

    # Use a temporary manager just for the DB query
    mgr = DetachedSubagentManager(db=db)
    runs = mgr.list_runs(conversation_id)
    if not runs:
        renderer.console.print("[dim]No detached agent runs in this conversation.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", width=10)
    table.add_column("Status", width=12)
    table.add_column("Title", max_width=50)
    table.add_column("Duration", width=10)

    for run in runs:
        rid = run["id"][:8]
        status = run.get("status", "?")
        title = (run.get("title") or "")[:50]
        dur_ms = run.get("duration_ms")
        dur = f"{dur_ms / 1000:.1f}s" if dur_ms else "-"
        style = "green" if status == "completed" else "red" if status == "failed" else "dim"
        table.add_row(rid, f"[{style}]{status}[/{style}]", title, dur)

    renderer.console.print(table)


def handle_agent_status(db: Any, run_id: str, renderer: Any) -> None:
    """Show detailed status of a detached agent run."""
    from ..services import storage

    # Resolve prefix
    rows = db.execute_fetchall(
        "SELECT id FROM agent_runs WHERE kind = 'detached_subagent' AND id LIKE ? LIMIT 2",
        (f"{run_id}%",),
    )
    if not rows:
        renderer.console.print(f"[red]Agent run not found: {run_id}[/red]")
        return
    if len(rows) > 1:
        renderer.console.print(f"[red]Ambiguous prefix: {run_id} (matches {len(rows)} runs)[/red]")
        return

    full_id = rows[0]["id"]
    run = storage.get_agent_run(db, full_id)
    if run is None:
        renderer.console.print(f"[red]Agent run not found: {run_id}[/red]")
        return

    renderer.console.print(f"[bold]Run {full_id[:8]}[/bold] — {run.get('status', '?')}")
    renderer.console.print(f"  Title:     {run.get('title', '-')}")
    renderer.console.print(f"  Started:   {run.get('started_at', '-')}")
    renderer.console.print(f"  Completed: {run.get('completed_at', '-')}")
    if run.get("duration_ms"):
        renderer.console.print(f"  Duration:  {run['duration_ms'] / 1000:.1f}s")
    if run.get("parent_run_id"):
        renderer.console.print(f"  Retry of:  {run['parent_run_id'][:8]}")

    meta = run.get("metadata") or {}
    if meta.get("output"):
        renderer.console.print(f"\n  Output preview:\n  {meta['output'][:500]}")
    if meta.get("error"):
        renderer.console.print(f"\n  [red]Error: {meta['error']}[/red]")
    if meta.get("tool_calls_made"):
        renderer.console.print(f"  Tools used: {', '.join(meta['tool_calls_made'][:10])}")


def handle_agent_cancel(db: Any, run_id: str, renderer: Any) -> bool:
    """Cancel a running detached agent."""
    from ..cli.repl import _detach_manager_ref

    mgr = _detach_manager_ref[0]
    if mgr is None:
        renderer.console.print("[red]No detached agent manager available.[/red]")
        return False

    # Resolve prefix
    rows = db.execute_fetchall(
        "SELECT id FROM agent_runs WHERE kind = 'detached_subagent' AND id LIKE ? LIMIT 2",
        (f"{run_id}%",),
    )
    if not rows:
        renderer.console.print(f"[red]Agent run not found: {run_id}[/red]")
        return False
    if len(rows) > 1:
        renderer.console.print(f"[red]Ambiguous prefix: {run_id}[/red]")
        return False

    full_id = rows[0]["id"]
    if mgr.cancel(full_id):
        renderer.console.print(f"[green]Cancelled agent run {full_id[:8]}[/green]")
        return True
    renderer.console.print(f"[yellow]Could not cancel {full_id[:8]} (may not be running)[/yellow]")
    return False


def handle_agent_retry(db: Any, run_id: str, renderer: Any, **start_kwargs: Any) -> dict[str, Any] | None:
    """Retry a failed/cancelled detached agent."""
    from ..cli.repl import _detach_manager_ref

    mgr = _detach_manager_ref[0]
    if mgr is None:
        renderer.console.print("[red]No detached agent manager available.[/red]")
        return None

    # Resolve prefix
    rows = db.execute_fetchall(
        "SELECT id FROM agent_runs WHERE kind = 'detached_subagent' AND id LIKE ? LIMIT 2",
        (f"{run_id}%",),
    )
    if not rows:
        renderer.console.print(f"[red]Agent run not found: {run_id}[/red]")
        return None
    if len(rows) > 1:
        renderer.console.print(f"[red]Ambiguous prefix: {run_id}[/red]")
        return None

    full_id = rows[0]["id"]
    try:
        result = mgr.retry(full_id, **start_kwargs)
        renderer.console.print(f"[green]Retrying as new run {result['run_id'][:8]} (retry of {full_id[:8]})[/green]")
        return result
    except ValueError as exc:
        renderer.console.print(f"[red]{exc}[/red]")
        return None
