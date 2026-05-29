from __future__ import annotations

import json
import time
from collections.abc import Iterator
from contextlib import contextmanager

from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TextColumn
from rich.rule import Rule
from rich.table import Table
from rich.text import Text


# ── Todo/Progress display ──────────────────────────────────


def print_todos(todos: list[dict]) -> None:
    """Print a minimal todo list showing task progress."""
    from sage.core import renderer
    if not todos:
        return

    if renderer.has_bottom_dock():
        renderer.set_bottom_dock_todos(todos)
        return

    renderer.console.print()
    renderer.console.print("  [bold cyan]📋 Tasks:[/bold cyan]")
    for todo in todos:
        status = todo.get("status", "pending")
        content = todo.get("content", "")
        if status == "completed":
            icon = "[green]✓[/green]"
        elif status == "in_progress":
            icon = "[yellow]►[/yellow]"
        else:
            icon = "[dim]○[/dim]"
        renderer.console.print(f"    {icon} {content}")


def print_step_progress(current: int, total: int, description: str) -> None:
    """Print a minimal step progress indicator."""
    from sage.core import renderer
    if renderer.has_bottom_dock():
        renderer.set_bottom_dock_status(f"Step {current}/{total}: {description}")
    renderer.console.print(f"  [cyan]Step {current}/{total}:[/cyan] {description}")


# ── File operation display ─────────────────────────────────


def print_files_written(files: list[str]) -> None:
    """Print a styled list of written files."""
    from sage.core import renderer
    renderer.console.print()
    renderer.phase("writing", f"{len(files)} file(s)")
    for f in files:
        renderer.console.print(f"    [green]+ {f}[/green]")


def print_files_deleted(files: list[str]) -> None:
    """Print a styled list of deleted files."""
    from sage.core import renderer
    for f in files:
        renderer.console.print(f"    [red]- {f}[/red]")


def print_file_read(filepath: str, line_count: int) -> None:
    """Print a styled file-read indicator."""
    from sage.core import renderer
    renderer.phase("reading", f"{filepath} ({line_count} lines)")


# ── Test result display ────────────────────────────────────


def print_test_results(output: str, passed: bool) -> None:
    """Print test results with pass/fail styling."""
    from sage.core import renderer
    if passed:
        renderer.console.print()
        renderer.phase("done", "All tests passed")
        # Extract summary line if present
        for line in output.splitlines():
            if "passed" in line.lower():
                renderer.console.print(f"    [green]{line.strip()}[/green]")
                break
    else:
        renderer.console.print()
        renderer.phase("error", "Tests failed")
        # Show the failure summary
        in_failures = False
        shown = 0
        for line in output.splitlines():
            if "FAILED" in line or "ERROR" in line:
                renderer.console.print(f"    [red]{line.strip()}[/red]")
                shown += 1
            elif "short test summary" in line.lower():
                in_failures = True
            elif in_failures and line.strip() and shown < 10:
                renderer.console.print(f"    [red]{line.strip()}[/red]")
                shown += 1


def print_validation_start(cmd: str) -> None:
    """Print the start of a validation step."""
    from sage.core import renderer
    renderer.console.print()
    renderer.phase("validating", cmd)


def print_retry(attempt: int, max_retries: int) -> None:
    """Print a retry indicator."""
    from sage.core import renderer
    renderer.console.print()
    renderer.phase("fixing", f"Auto-fixing (attempt {attempt}/{max_retries})")


# ── Command execution display ──────────────────────────────


def print_shell_start(cmd: str) -> None:
    """Print shell command being executed."""
    from sage.core import renderer
    renderer.phase("executing", cmd[:100] + ("..." if len(cmd) > 100 else ""))


def print_shell_output(output: str, max_lines: int = 30) -> None:
    """Print shell output, truncated if too long."""
    from sage.core import renderer
    lines = output.splitlines()
    if len(lines) > max_lines:
        for line in lines[:10]:
            renderer.console.print(f"    [dim]{line}[/dim]")
        renderer.console.print(f"    [dim]... ({len(lines) - 20} lines hidden) ...[/dim]")
        for line in lines[-10:]:
            renderer.console.print(f"    [dim]{line}[/dim]")
    else:
        for line in lines:
            renderer.console.print(f"    [dim]{line}[/dim]")


# ── Existing functions (upgraded) ──────────────────────────


def render_markdown(text: str) -> None:
    """Render a complete response as Rich Markdown with code highlighting."""
    from sage.core import renderer
    content = renderer.strip_thinking_blocks(text) if renderer.suppress_thinking() else text
    if not content.strip():
        return
    renderer.console.print(Markdown(content))


def _synthesize_model_description(m: dict) -> str:
    """Build a best-effort description from name + provider when none is set."""
    name = (m.get("name") or "").strip()
    provider = (m.get("provider") or "").lower()
    is_local = bool(m.get("local"))

    # Extract size hint like "(7b)" or "(0.5b-32b)" from the name
    import re
    size_match = re.search(r"\(([^)]*\b\d[\d.bB\-x +mMkK]*[bB]?[^)]*)\)", name)
    size_hint = size_match.group(1) if size_match else ""

    pieces = []
    if provider == "ollama":
        pieces.append("Local Ollama model" if is_local else "Pullable via Ollama")
    elif provider == "llama_cpp":
        pieces.append("Local GGUF (llama.cpp)")
    elif provider:
        pieces.append(provider.capitalize() + (" model" if not provider.endswith("e") else ""))

    if size_hint:
        pieces.append(size_hint)

    # Detect well-known family keywords for an extra hint
    lower_name = name.lower()
    family_hints = {
        "coder": "code generation",
        "instruct": "instruction-tuned",
        "vision": "multimodal (image + text)",
        "embed": "embedding model",
        "thinking": "step-by-step reasoning",
        "reasoning": "step-by-step reasoning",
        "math": "math + reasoning focus",
        "ocr": "OCR",
    }
    for kw, label in family_hints.items():
        if kw in lower_name:
            pieces.append(label)
            break

    return " · ".join(pieces) if pieces else ""


def print_model_table(
    models: list[dict],
    *,
    max_rows: int = 45,
    filter_hint: str | None = None,
    show_details: bool = False,
    show_all: bool = False,
) -> None:
    """Print a formatted table of available models."""
    from sage.core import renderer
    title = "Available Models"
    if filter_hint:
        title = f"{title} (filter: {filter_hint})"
    table = Table(title=title, show_lines=show_details)
    table.add_column("Model ID", style="cyan bold")
    table.add_column("Provider", style="green")
    table.add_column("Name", style="white")
    table.add_column("Type", style="yellow")
    if show_details:
        table.add_column("Description", style="dim")
    else:
        table.add_column("Description", style="dim", max_width=40)

    effective_max = len(models) if show_all else max_rows
    shown = models[:effective_max]
    for m in shown:
        desc = m.get("description", "")
        if not desc:
            desc = _synthesize_model_description(m)
        if show_details and (m.get("pros") or m.get("cons")):
            pros = m.get("pros", "")
            cons = m.get("cons", "")
            if pros or cons:
                desc_parts = [desc] if desc else []
                if pros:
                    desc_parts.append(f"[green]✓ {pros}[/green]")
                if cons:
                    desc_parts.append(f"[red]✗ {cons}[/red]")
                desc = "\n".join(desc_parts)
        elif len(desc) > 40:
            desc = desc[:37] + "..."
        table.add_row(
            m["id"],
            m["provider"],
            m["name"],
            "local" if m["local"] else "API",
            desc,
        )
    renderer.console.print(table)
    remaining = len(models) - len(shown)
    if remaining > 0:
        renderer.console.print(
            f"[dim]… {remaining} more not shown. "
            "Use [cyan]/models --all[/cyan] to see all, "
            "or [cyan]/models <keyword>[/cyan] to filter.[/dim]"
        )
    if not show_details:
        renderer.console.print("[dim]Use /models --details for full descriptions with pros/cons[/dim]")


def print_catalog_table(models: list[dict], show_status: bool = True) -> None:
    """Print a formatted table of models from the catalog."""
    from sage.core import renderer
    table = Table(title="Downloadable Models", show_lines=False)
    table.add_column("Name", style="cyan bold")
    table.add_column("Size", style="yellow", justify="right")
    table.add_column("Params", style="green")
    table.add_column("Family", style="magenta")
    table.add_column("Description", style="white")
    if show_status:
        table.add_column("Status", style="bold")

    for m in models:
        row = [m["name"], m["size"], m["params"], m["family"], m["description"]]
        if show_status:
            row.append(m.get("status", ""))
        table.add_row(*row)
    renderer.console.print(table)


def print_download_complete(name: str, path: str, size_gb: float) -> None:
    """Print a success message after a model download."""
    from sage.core import renderer
    renderer.console.print()
    renderer.console.print(
        Panel(
            f"[bold green]Downloaded:[/bold green] {name}\n"
            f"[dim]Path:[/dim] {path}\n"
            f"[dim]Size:[/dim] {size_gb:.1f} GB\n\n"
            f"Run with: [bold cyan]sage run --model llama_cpp:{name}[/bold cyan]",
            title="Model Ready",
            border_style="green",
        )
    )


def print_config(data: dict) -> None:
    """Pretty-print config as a panel."""
    from sage.core import renderer
    import json
    text = json.dumps(data, indent=2)
    renderer.console.print(Panel(text, title="~/.sage/config.json", border_style="dim"))


def header(msg: str) -> None:
    """Print a header/title message."""
    from sage.core import renderer
    renderer.console.print(f"[bold cyan]{msg}[/bold cyan]")


def info(msg: str) -> None:
    """Print an info message."""
    from sage.core import renderer
    if not renderer.is_verbose():
        return
    renderer.console.print(f"[dim]{msg}[/dim]")


def success(msg: str) -> None:
    """Print a success message."""
    from sage.core import renderer
    renderer.console.print(f"[green]{msg}[/green]")


def error(msg: str) -> None:
    """Print an error message to stderr."""
    from sage.core import renderer
    renderer.err_console.print(f"[red bold]Error:[/red bold] {msg}")


def warning(msg: str) -> None:
    """Print a warning to stderr."""
    from sage.core import renderer
    renderer.err_console.print(f"[yellow]Warning:[/yellow] {msg}")


def debug_warning(msg: str) -> None:
    """Print a debug warning (only in verbose mode)."""
    from sage.core import renderer
    if not renderer.is_verbose():
        return
    renderer.err_console.print(f"[dim yellow]Debug:[/dim yellow] {msg}")


def print_welcome(model_id: str) -> None:
    """Print the REPL welcome banner."""
    from sage.core import renderer
    renderer.console.print(
        Panel(
            Text.from_markup(
                f"[bold #6ea4ff]SAGE[/bold #6ea4ff]  [dim]local-first AI workspace[/dim]\n"
                f"[dim]Model[/dim]   {model_id}\n"
                f"[dim]Use[/dim]     /help  /clear  /model  /system  /exit\n"
                f'[dim]Input[/dim]   Multi-line with """..."""'
            ),
            border_style="#6ea4ff",
            padding=(0, 2),
        )
    )


def print_help() -> None:
    """Print REPL command reference."""
    from sage.core import renderer
    help_text = (
        "[bold #6ea4ff]REPL commands[/bold #6ea4ff]\n"
        "  [#8bb8ff]/help[/#8bb8ff]           Show this help\n"
        "  [#8bb8ff]/clear[/#8bb8ff]          Clear conversation history\n"
        "  [#8bb8ff]/models[/#8bb8ff]         List all available AI models\n"
        "  [#8bb8ff]/model[/#8bb8ff] [id]     Show or change active model\n"
        "  [#8bb8ff]/system[/#8bb8ff] [text]  Show or set system prompt\n"
        "  [#8bb8ff]/status[/#8bb8ff]         Show chat status (model, turn count)\n"
        "  [#8bb8ff]/history[/#8bb8ff]        Show conversation turn count\n"
        "  [#8bb8ff]/version[/#8bb8ff]        Show current version and check for updates\n"
        "  [#8bb8ff]/update[/#8bb8ff]         Update SAGE AI to the latest CLI version\n"
        "  [#8bb8ff]/exit[/#8bb8ff]           Quit\n"
    )
    renderer.console.print(Panel(help_text, title="SAGE Help", border_style="#6ea4ff"))


def print_agent_welcome(model_id: str, cwd: str, *, is_local: bool = False) -> None:
    """Print the agent-mode welcome banner."""
    from sage.core import renderer
    kind = "local (Ollama / llama.cpp / etc.)" if is_local else "cloud / API"
    renderer.console.print()
    renderer.console.print(
        Panel(
            Text.from_markup(
                f"[bold #6ea4ff]SAGE Code[/bold #6ea4ff]  [dim]interactive coding workspace[/dim]\n"
                f"\n"
                f"[dim]Model[/dim]    [bold]{model_id}[/bold]\n"
                f"[dim]Backend[/dim]  {kind}\n"
                f"[dim]Project[/dim]  {cwd}\n"
                f"\n"
                f"[dim]READ / SEARCH / edit / run with your model catalog, locally or in the cloud.[/dim]\n"
                f"[dim]Switch models with /model and browse them with /models.[/dim]\n"
                f"\n"
                f"[#8bb8ff]Commands[/#8bb8ff]  /help  /models  /model  /autoorg  /think  /test  /read  /files  /compact  /undo  /status  /clear  /exit\n"
                f'[#8bb8ff]Shell[/#8bb8ff]     !<command>    [#8bb8ff]Multi-line[/#8bb8ff] """..."""\n'
                f"[#8bb8ff]Models[/#8bb8ff]    sage pull --list    sage pull <name>\n"
                f"[#8bb8ff]Update[/#8bb8ff]    sage update\n"
                f"\n"
                f"[dim italic]⚠ SAGE can make mistakes. "
                f"Double-check important responses, commands, and file edits.[/dim italic]"
            ),
            border_style="#6ea4ff",
            padding=(0, 2),
        )
    )
    renderer.console.print()


def print_agent_help() -> None:
    """Print agent-mode command reference."""
    from sage.core import renderer
    help_text = (
        "[bold #6ea4ff]Workspace commands[/bold #6ea4ff]\n"
        "  [#8bb8ff]/help[/#8bb8ff]                              Show this help\n"
        "  [#8bb8ff]/models[/#8bb8ff] [--all] [--details]      List AI models (default top 45)\n"
        "         [-p PROVIDER] [-f KEYWORD]      Filter by provider or keyword\n"
        "  [#8bb8ff]/model[/#8bb8ff] [id]                       Show or change the active model\n"
        "  [#8bb8ff]/think[/#8bb8ff] [on|off]                   Enable/disable thinking blocks visibility\n"
        "  [#8bb8ff]/read[/#8bb8ff] <file>                       Read a file into conversation context\n"
        "  [#8bb8ff]/test[/#8bb8ff] [cmd]                       Run tests (default: pytest -v --tb=short)\n"
        "  [#8bb8ff]/files[/#8bb8ff]                             Show written files from this session\n"
        "  [#8bb8ff]/undo[/#8bb8ff]                              Restore files to previous state\n"
        "  [#8bb8ff]/compact[/#8bb8ff]                           Trim conversation state to free context\n"
        "  [#8bb8ff]/clear[/#8bb8ff]                             Clear conversation and file history\n"
        "  [#8bb8ff]/system[/#8bb8ff] [text]                    Show or set system prompt\n"
        "  [#8bb8ff]/status[/#8bb8ff]                            Show agent status (model, files, plan)\n"
        "  [#8bb8ff]/context[/#8bb8ff]                           Show current context telemetry & token usage\n"
        "  [#8bb8ff]/rag[/#8bb8ff] <query|index|status> [args] Query, index, or show status of local RAG\n"
        "  [#8bb8ff]/tdd[/#8bb8ff] [on|off]                     Toggle test-driven development (TDD) mode\n"
        "  [#8bb8ff]/phd[/#8bb8ff] <topic>                      Run PhD-level strategic research on a topic\n"
        "  [#8bb8ff]/expert[/#8bb8ff] <domain> [query]          Consult a domain expert persona\n"
        "  [#8bb8ff]/swarm[/#8bb8ff]                            Coordinate a swarm of simulated/worker sub-agents\n"
        "  [#8bb8ff]/sandbox[/#8bb8ff] [cmd]                    Run command/Python script in Docker sandbox\n"
        "  [#8bb8ff]/autoorg[/#8bb8ff] [task]                   Run multi-step AI orchestration\n"
        "  [#8bb8ff]/autofleet[/#8bb8ff] [task]                 Run fleet (multi-agent) orchestration\n"
        "  [#8bb8ff]/update[/#8bb8ff]                            Update SAGE AI to the latest CLI version\n"
        "  [#8bb8ff]/version[/#8bb8ff]                           Show current version and check for updates\n"
        "  [#8bb8ff]/history[/#8bb8ff]                           Show conversation turn count\n"
        "  [#8bb8ff]/exit[/#8bb8ff] (also /quit, /q)             Quit the REPL\n"
        "\n[bold #6ea4ff]Shell[/bold #6ea4ff]\n"
        "  [#8bb8ff]!<command>[/#8bb8ff]        Run a shell command (e.g. !ls -la)\n"
        "\n[bold #6ea4ff]SAGE phases[/bold #6ea4ff]\n"
        "  [dim]◌ Thinking[/dim]      Analyzing the request\n"
        "  [dim]◎ Planning[/dim]      Breaking the task into steps\n"
        "  [dim]◆ Coding[/dim]        Generating code\n"
        "  [dim]▸ Writing[/dim]       Saving files to disk\n"
        "  [dim]◈ Testing[/dim]       Running tests automatically\n"
        "  [dim]↺ Fixing[/dim]        Recovering from failures\n"
        "  [dim]✓ Done[/dim]          Task complete\n"
        "\n[bold #6ea4ff]Flags[/bold #6ea4ff]\n"
        "  [dim]--output clean|normal|verbose  Terminal verbosity (default: clean)[/dim]\n"
        "  [dim]-v / --verbose                 Same as --output verbose[/dim]\n"
        "  [dim]--no-color                     Disable ANSI colors[/dim]\n"
        "  [dim]--auto-run                     Skip bash execution prompts[/dim]\n"
        "\n[dim italic]⚠ SAGE can make mistakes. "
        "Double-check important responses, commands, and file edits.[/dim italic]\n"
    )
    renderer.console.print(Panel(help_text, title="SAGE Code Help", border_style="#6ea4ff"))


# ── Pull-Update-Delete Cycle Progress Bar ──────────────────


class SyncProgress:
    """Multi-phase progress bar for pull-update-delete sync cycles."""

    _PHASE_ICONS = {
        "pull": ("cyan", "↓"),
        "update": ("yellow", "↻"),
        "delete": ("red", "×"),
    }

    def __init__(self, title: str = "Syncing") -> None:
        self._title = title
        self._progress: Progress | None = None
        self._overall_task: TaskID | None = None
        self._phase_task: TaskID | None = None
        self._current_phase: str | None = None
        self._phases_completed = 0
        self._total_phases = 3

    def __enter__(self) -> SyncProgress:
        from sage.core import renderer
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.description}[/bold]"),
            BarColumn(bar_width=30),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("[dim]{task.fields[status]}[/dim]"),
            console=renderer.console,
            transient=False,
        )
        self._progress.start()

        # Overall progress bar
        self._overall_task = self._progress.add_task(
            f"[bold cyan]{self._title}[/bold cyan]",
            total=self._total_phases,
            status="starting...",
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._progress and self._overall_task is not None:
            if exc_type is None:
                self._progress.update(
                    self._overall_task,
                    completed=self._total_phases,
                    status="[green]complete[/green]",
                )
            else:
                self._progress.update(
                    self._overall_task,
                    status=f"[red]failed ({exc_type.__name__})[/red]",
                )
            self._progress.stop()

    def _start_phase(self, phase: str, total: int, description: str = "") -> None:
        """Start a new phase with its own progress bar."""
        color, icon = self._PHASE_ICONS.get(phase, ("white", "·"))
        desc = description or phase.capitalize()

        if self._phase_task is not None and self._progress:
            self._progress.remove_task(self._phase_task)

        self._current_phase = phase

        if self._progress and self._overall_task is not None:
            self._progress.update(
                self._overall_task,
                status=f"[{color}]{icon} {desc}[/{color}]",
            )

            self._phase_task = self._progress.add_task(
                f"  [{color}]{icon}[/{color}] {desc}",
                total=total,
                status="",
            )

    def _advance_phase(self, amount: int = 1, status: str = "") -> None:
        """Advance the current phase progress."""
        if self._progress and self._phase_task is not None:
            self._progress.update(self._phase_task, advance=amount, status=status)

    def _complete_phase(self) -> None:
        """Mark the current phase as complete."""
        if self._progress and self._phase_task is not None:
            task = self._progress.tasks[self._phase_task]
            self._progress.update(self._phase_task, completed=task.total or 0)

        self._phases_completed += 1
        if self._progress and self._overall_task is not None:
            self._progress.update(self._overall_task, completed=self._phases_completed)

    def start_pull(self, total: int, description: str = "Pulling") -> None:
        self._start_phase("pull", total, description)

    def advance_pull(self, amount: int = 1, item: str = "") -> None:
        status = f"[dim]{item}[/dim]" if item else ""
        self._advance_phase(amount, status)

    def complete_pull(self) -> None:
        self._complete_phase()

    def start_update(self, total: int, description: str = "Updating") -> None:
        self._start_phase("update", total, description)

    def advance_update(self, amount: int = 1, item: str = "") -> None:
        status = f"[dim]{item}[/dim]" if item else ""
        self._advance_phase(amount, status)

    def complete_update(self) -> None:
        self._complete_phase()

    def start_delete(self, total: int, description: str = "Cleaning up") -> None:
        self._start_phase("delete", total, description)

    def advance_delete(self, amount: int = 1, item: str = "") -> None:
        status = f"[dim]{item}[/dim]" if item else ""
        self._advance_phase(amount, status)

    def complete_delete(self) -> None:
        self._complete_phase()


@contextmanager
def sync_progress(title: str = "Syncing") -> Iterator[SyncProgress]:
    sp = SyncProgress(title)
    with sp:
        yield sp


# ── Autopolit Progress Tracking ─────────────────────────────


class AutopolitProgress:
    """Progress tracker for autopolit cycles."""

    def __init__(self, max_cycles: int | None = None):
        self.max_cycles = max_cycles
        self.current_cycle = 0
        self.start_time = time.time()
        self.cycle_stats: list[dict] = []
        self._current_cycle_stats: dict = {}

    def start_cycle(self, cycle: int) -> None:
        from sage.core import renderer
        self.current_cycle = cycle
        self._current_cycle_stats = {
            "cycle": cycle,
            "start_time": time.time(),
            "files_written": [],
            "tests_passed": False,
            "errors": [],
            "phase": "starting",
        }

        max_str = f"/{self.max_cycles}" if self.max_cycles else ""
        elapsed = time.time() - self.start_time
        elapsed_str = f"{elapsed:.0f}s" if elapsed < 60 else f"{elapsed / 60:.1f}m"

        renderer.console.print()
        renderer.console.print(
            Rule(
                f"[bold cyan]Autopolit Cycle {cycle}{max_str}[/bold cyan] "
                f"[dim]({elapsed_str} elapsed)[/dim]",
                style="cyan",
            )
        )

    def update_phase(self, phase: str, detail: str = "") -> None:
        self._current_cycle_stats["phase"] = phase
        _phase(phase, detail)

    def add_file(self, filepath: str) -> None:
        self._current_cycle_stats["files_written"].append(filepath)

    def add_error(self, error: str) -> None:
        self._current_cycle_stats["errors"].append(error)

    def set_tests_passed(self, passed: bool) -> None:
        self._current_cycle_stats["tests_passed"] = passed

    def end_cycle(self) -> None:
        from sage.core import renderer
        self._current_cycle_stats["end_time"] = time.time()
        self._current_cycle_stats["duration"] = (
            self._current_cycle_stats["end_time"] - self._current_cycle_stats["start_time"]
        )
        self.cycle_stats.append(self._current_cycle_stats.copy())

        stats = self._current_cycle_stats
        files = len(stats["files_written"])
        errors = len(stats["errors"])
        duration = stats["duration"]

        status_parts = []
        if files > 0:
            status_parts.append(f"[green]{files} file(s)[/green]")
        if stats["tests_passed"]:
            status_parts.append("[green]tests ✓[/green]")
        elif errors > 0:
            status_parts.append(f"[red]{errors} error(s)[/red]")

        status = " · ".join(status_parts) if status_parts else "[dim]no changes[/dim]"
        renderer.console.print(
            f"  [dim]Cycle {self.current_cycle} completed in {duration:.1f}s[/dim] — {status}"
        )

    def print_summary(self) -> None:
        from sage.core import renderer
        total_time = time.time() - self.start_time
        total_cycles = len(self.cycle_stats)
        total_files = sum(len(s["files_written"]) for s in self.cycle_stats)
        total_errors = sum(len(s["errors"]) for s in self.cycle_stats)
        successful_cycles = sum(1 for s in self.cycle_stats if s["tests_passed"])

        time_str = f"{total_time:.0f}s" if total_time < 60 else f"{total_time / 60:.1f}m"

        renderer.console.print()
        renderer.console.print(Rule("[bold]Autopolit Summary[/bold]", style="cyan"))
        renderer.console.print()

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="dim")
        table.add_column(style="bold")

        table.add_row("Total cycles", str(total_cycles))
        table.add_row("Successful cycles", f"[green]{successful_cycles}[/green]")
        table.add_row("Files written", f"[cyan]{total_files}[/cyan]")
        table.add_row(
            "Errors encountered",
            f"[red]{total_errors}[/red]" if total_errors else "[green]0[/green]",
        )
        table.add_row("Total time", time_str)

        renderer.console.print(table)

        if total_files > 0:
            renderer.console.print()
            renderer.console.print("[dim]Files written:[/dim]")
            all_files = set()
            for s in self.cycle_stats:
                all_files.update(s["files_written"])
            for f in sorted(all_files)[:20]:
                renderer.console.print(f"  [green]+ {f}[/green]")
            if len(all_files) > 20:
                renderer.console.print(f"  [dim]... and {len(all_files) - 20} more[/dim]")

        renderer.console.print()


def _phase(name: str, detail: str = "") -> None:
    """Internal phase printer (avoids name conflict)."""
    from sage.core import renderer
    style, icon = renderer._PHASE_STYLES.get(name, ("dim", "·"))
    detail_str = f"  [dim]{detail}[/dim]" if detail else ""
    renderer.console.print(f"  [{style}]{icon} {name.capitalize()}[/{style}]{detail_str}")
