"""CLI handlers for /task REPL command.

Displays background task status, output, and management. Follows the
same dispatch pattern as mission REPL handlers in repl.py.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

if TYPE_CHECKING:
    from pathlib import Path

console = Console(stderr=True)


def handle_task_list(bg_manager: Any, conversation_id: str) -> None:
    """Display a table of background tasks."""
    tasks = bg_manager.list_tasks(conversation_id)
    if not tasks:
        console.print("[dim]No background tasks.[/dim]\n")
        return

    table = Table(title="Background Tasks", show_lines=False)
    table.add_column("ID", style="cyan", no_wrap=True, max_width=8)
    table.add_column("Status", style="bold")
    table.add_column("Command", max_width=50)
    table.add_column("Created")

    for t in tasks:
        status = t.get("status", "unknown")
        style = {
            "running": "yellow",
            "completed": "green",
            "failed": "red",
            "cancelled": "dim",
        }.get(status, "")
        table.add_row(
            t["id"][:8],
            f"[{style}]{status}[/{style}]" if style else status,
            (t.get("command", "")[:50] or "-"),
            t.get("created_at", "")[:19],
        )

    console.print(table)
    console.print()


def handle_task_show(bg_manager: Any, task_id: str) -> None:
    """Display detailed information about a single task."""
    task = bg_manager.get_task(task_id)
    if task is None:
        console.print(f"[red]Task '{task_id}' not found.[/red]\n")
        return

    lines = [
        f"[bold]ID:[/bold] {task['id']}",
        f"[bold]Status:[/bold] {task.get('status', 'unknown')}",
        f"[bold]Command:[/bold] {task.get('command', '-')}",
        f"[bold]Created:[/bold] {task.get('created_at', '-')}",
    ]
    if task.get("completed_at"):
        lines.append(f"[bold]Completed:[/bold] {task['completed_at']}")
    if task.get("preview"):
        lines.append(f"[bold]Preview:[/bold]\n{task['preview']}")

    console.print(Panel("\n".join(lines), title="Task Detail", border_style="cyan"))
    console.print()


def handle_task_output(bg_manager: Any, task_id: str, tail_lines: int | None = None) -> None:
    """Display stdout output from a background task."""
    from ..services.task_output import read_task_output, stdout_path

    task = bg_manager.get_task(task_id)
    if task is None:
        console.print(f"[red]Task '{task_id}' not found.[/red]\n")
        return

    conversation_id = task.get("conversation_id", "")
    data_dir: Path = bg_manager.data_dir
    file_path = stdout_path(data_dir, conversation_id, task_id)

    content = read_task_output(file_path, tail_lines=tail_lines)
    if not content:
        console.print("[dim]No output available.[/dim]\n")
        return

    title = f"Task {task_id[:8]} output"
    if tail_lines:
        title += f" (last {tail_lines} lines)"
    console.print(Panel(content.rstrip(), title=title, border_style="green"))
    console.print()


def handle_task_cancel(bg_manager: Any, task_id: str) -> None:
    """Cancel a running background task."""
    task = bg_manager.get_task(task_id)
    if task is None:
        console.print(f"[red]Task '{task_id}' not found.[/red]\n")
        return

    if task.get("status") != "running":
        console.print(f"[yellow]Task is not running (status: {task.get('status')}).[/yellow]\n")
        return

    bg_manager.cancel_task(task_id)
    console.print(f"[green]Task {task_id[:8]} cancel requested.[/green]\n")
