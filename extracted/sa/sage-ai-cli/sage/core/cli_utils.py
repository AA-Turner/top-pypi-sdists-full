"""
CLI utilities and UX enhancements for SAGE.

P2-61: Unify help system across all CLIs
P2-62: Add context-aware command suggestions
P2-63: Implement built-in output pager
P2-64: Add command typo detection and suggestions
P2-65: Create interactive config wizard
P2-66: Add config validation with repair suggestions
P2-67: Implement per-project config overrides (.sagecrc)
P2-68: Add machine-readable output modes (--json, --csv)
P2-69: Implement verbosity levels (--quiet, --verbose, --debug)
P2-70: Add color toggle (--no-color, --force-color)
P2-71: Create model selector with search/filter
P2-72: Add history browser with fuzzy search
P2-73: Implement multi-select for batch operations
P2-74: Add analytics dashboard (command frequency, success rates)
P2-75-80: Various UX improvements
"""

from __future__ import annotations

import difflib
import json
import re
import shutil
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

# =============================================================================
# Output Modes (P2-68, P2-69, P2-70)
# =============================================================================


class OutputMode(Enum):
    """Output format modes."""

    RICH = "rich"  # Rich formatting (default)
    PLAIN = "plain"  # Plain text
    JSON = "json"  # JSON output
    CSV = "csv"  # CSV output
    MARKDOWN = "markdown"  # Markdown


class VerbosityLevel(Enum):
    """Verbosity levels."""

    QUIET = 0
    NORMAL = 1
    VERBOSE = 2
    DEBUG = 3


@dataclass
class OutputConfig:
    """Configuration for output handling."""

    mode: OutputMode = OutputMode.RICH
    verbosity: VerbosityLevel = VerbosityLevel.NORMAL
    color: bool = True
    pager: bool = False
    width: int | None = None


class OutputHandler:
    """
    Handles output in multiple formats.

    P2-68: Add machine-readable output modes
    P2-69: Implement verbosity levels
    P2-70: Add color toggle
    """

    def __init__(self, config: OutputConfig | None = None):
        self.config = config or OutputConfig()
        self._console: Console | None = None

    @property
    def console(self) -> Console:
        """Get configured console."""
        if self._console is None:
            self._console = Console(
                force_terminal=self.config.color if self.config.mode == OutputMode.RICH else False,
                no_color=not self.config.color,
                width=self.config.width,
            )
        return self._console

    def print(self, message: str, level: VerbosityLevel = VerbosityLevel.NORMAL) -> None:
        """Print message if verbosity allows."""
        if level.value > self.config.verbosity.value:
            return

        if self.config.mode == OutputMode.JSON:
            print(json.dumps({"message": message}))
        elif self.config.mode == OutputMode.PLAIN:
            # Strip rich markup
            clean = re.sub(r"\[/?[^\]]+\]", "", message)
            print(clean)
        else:
            self.console.print(message)

    def print_data(self, data: Any, title: str | None = None) -> None:
        """Print structured data in configured format."""
        if self.config.mode == OutputMode.JSON:
            print(json.dumps(data, indent=2, default=str))
            return

        if self.config.mode == OutputMode.CSV:
            self._print_csv(data)
            return

        if self.config.mode == OutputMode.MARKDOWN:
            self._print_markdown(data, title)
            return

        # Rich output
        if isinstance(data, list) and data and isinstance(data[0], dict):
            self._print_table(data, title)
        elif isinstance(data, dict):
            self._print_dict(data, title)
        else:
            self.console.print(data)

    def _print_table(self, data: list[dict], title: str | None) -> None:
        """Print list of dicts as table."""
        if not data:
            return

        table = Table(title=title)
        for key in data[0].keys():
            table.add_column(str(key))

        for row in data:
            table.add_row(*[str(v) for v in row.values()])

        self.console.print(table)

    def _print_dict(self, data: dict, title: str | None) -> None:
        """Print dict as key-value pairs."""
        table = Table(title=title, show_header=False)
        table.add_column("Key", style="cyan")
        table.add_column("Value")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        self.console.print(table)

    def _print_csv(self, data: Any) -> None:
        """Print data as CSV."""
        import csv
        import io

        output = io.StringIO()
        if isinstance(data, list) and data:
            if isinstance(data[0], dict):
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(output)
                for row in data:
                    writer.writerow([row] if not isinstance(row, (list, tuple)) else row)
        print(output.getvalue())

    def _print_markdown(self, data: Any, title: str | None) -> None:
        """Print data as Markdown."""
        if title:
            print(f"# {title}\n")

        if isinstance(data, list) and data and isinstance(data[0], dict):
            # Table
            headers = list(data[0].keys())
            print("| " + " | ".join(headers) + " |")
            print("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in data:
                print("| " + " | ".join(str(v) for v in row.values()) + " |")
        elif isinstance(data, dict):
            for key, value in data.items():
                print(f"- **{key}**: {value}")
        else:
            print(str(data))


# =============================================================================
# Unified Help System (P2-61)
# =============================================================================


@dataclass
class CommandHelp:
    """Help information for a command."""

    name: str
    description: str
    usage: str
    examples: list[str] = field(default_factory=list)
    options: list[tuple[str, str]] = field(default_factory=list)
    related: list[str] = field(default_factory=list)


class HelpSystem:
    """
    Unified help system.

    P2-61: Unify help system across all CLIs
    """

    def __init__(self, console: Console | None = None):
        self.console = console or Console()
        self._commands: dict[str, CommandHelp] = {}

    def register(self, cmd: CommandHelp) -> None:
        """Register a command's help."""
        self._commands[cmd.name] = cmd

    def show(self, command: str | None = None) -> None:
        """Show help for a command or all commands."""
        if command:
            self._show_command_help(command)
        else:
            self._show_all_help()

    def _show_command_help(self, command: str) -> None:
        """Show detailed help for a command."""
        cmd = self._commands.get(command)
        if not cmd:
            self.console.print(f"[red]Unknown command: {command}[/red]")
            self._suggest_similar(command)
            return

        # Title
        self.console.print(f"\n[bold cyan]{cmd.name}[/bold cyan]")
        self.console.print(f"[dim]{cmd.description}[/dim]\n")

        # Usage
        self.console.print("[bold]Usage:[/bold]")
        self.console.print(f"  {cmd.usage}\n")

        # Options
        if cmd.options:
            self.console.print("[bold]Options:[/bold]")
            for opt, desc in cmd.options:
                self.console.print(f"  [cyan]{opt:20}[/cyan] {desc}")
            self.console.print()

        # Examples
        if cmd.examples:
            self.console.print("[bold]Examples:[/bold]")
            for ex in cmd.examples:
                self.console.print(f"  [green]$[/green] {ex}")
            self.console.print()

        # Related
        if cmd.related:
            self.console.print(f"[dim]See also: {', '.join(cmd.related)}[/dim]")

    def _show_all_help(self) -> None:
        """Show help for all commands."""
        self.console.print("\n[bold]SAGE Commands[/bold]\n")

        for name, cmd in sorted(self._commands.items()):
            self.console.print(f"  [cyan]{name:15}[/cyan] {cmd.description}")

        self.console.print("\n[dim]Run 'sage help <command>' for detailed help[/dim]")

    def _suggest_similar(self, command: str) -> None:
        """Suggest similar commands."""
        similar = difflib.get_close_matches(command, self._commands.keys(), n=3, cutoff=0.6)
        if similar:
            self.console.print(f"\n[yellow]Did you mean: {', '.join(similar)}?[/yellow]")


# =============================================================================
# Command Suggestions (P2-62, P2-64)
# =============================================================================


class CommandSuggester:
    """
    Suggests commands based on context and typos.

    P2-62: Add context-aware command suggestions
    P2-64: Add command typo detection and suggestions
    """

    def __init__(self, known_commands: list[str]):
        self.known_commands = known_commands
        self._history: list[str] = []
        self._context: dict[str, Any] = {}

    def set_context(self, key: str, value: Any) -> None:
        """Set context for smarter suggestions."""
        self._context[key] = value

    def record_command(self, command: str) -> None:
        """Record a command in history."""
        self._history.append(command)

    def suggest_for_typo(self, typo: str) -> list[str]:
        """Suggest corrections for a typo."""
        return difflib.get_close_matches(typo, self.known_commands, n=5, cutoff=0.5)

    def suggest_next(self) -> list[str]:
        """Suggest next likely commands based on context."""
        suggestions = []

        # Based on recent history
        if self._history:
            last_cmd = self._history[-1]
            if "run" in last_cmd:
                suggestions.extend(["test", "lint", "build"])
            elif "test" in last_cmd:
                suggestions.extend(["fix", "run"])

        # Based on project context
        if self._context.get("has_tests"):
            suggestions.append("test")
        if self._context.get("has_errors"):
            suggestions.append("fix")

        return list(dict.fromkeys(suggestions))[:5]  # Unique, max 5


# =============================================================================
# Config Wizard (P2-65, P2-66, P2-67)
# =============================================================================


class ConfigWizard:
    """
    Interactive configuration wizard.

    P2-65: Create interactive config wizard
    P2-66: Add config validation with repair suggestions
    P2-67: Implement per-project config overrides (.sagecrc)
    """

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    def run(self) -> dict[str, Any]:
        """Run the interactive config wizard."""
        self.console.print("\n[bold cyan]SAGE Configuration Wizard[/bold cyan]\n")

        config = {}

        # Model selection
        self.console.print("[bold]Step 1: Select default model[/bold]")
        model_options = [
            "ollama:llama3.2 (local — requires Ollama)",
            "gemini:gemini-2.0-flash (cloud — requires API key)",
            "local GGUF (use after sage pull)",
        ]
        for i, opt in enumerate(model_options, 1):
            self.console.print(f"  {i}. {opt}")

        choice = Prompt.ask("Select model", choices=["1", "2", "3"], default="1")
        model_map = {
            "1": "ollama:llama3.2",
            "2": "gemini:gemini-2.0-flash",
            "3": "local",
        }
        config["default_model"] = model_map[choice]

        # API keys
        self.console.print("\n[bold]Step 2: API Keys (optional)[/bold]")
        if Confirm.ask("Configure Gemini API key?", default=False):
            key = Prompt.ask("Enter Gemini API key", password=True)
            config.setdefault("api_keys", {})["gemini"] = key

        # Temperature
        self.console.print("\n[bold]Step 3: Generation settings[/bold]")
        temp = Prompt.ask("Temperature (0.0-2.0)", default="0.2")
        config["temperature"] = float(temp)

        # Max tokens
        tokens = Prompt.ask("Max tokens", default="16384")
        config["max_tokens"] = int(tokens)

        # Confirmation
        self.console.print("\n[bold]Configuration Summary:[/bold]")
        self._print_config(config)

        if Confirm.ask("\nSave this configuration?", default=True):
            return config
        else:
            return {}

    def _print_config(self, config: dict) -> None:
        """Print config summary."""
        for key, value in config.items():
            if key == "api_keys":
                self.console.print(f"  {key}: [dim]{'configured' if value else 'not set'}[/dim]")
            else:
                self.console.print(f"  {key}: {value}")

    def validate(self, config: dict) -> list[tuple[str, str, str]]:
        """
        Validate configuration.

        Returns list of (field, issue, suggestion) tuples.
        """
        issues = []

        # Check required fields
        if "default_model" not in config:
            issues.append(("default_model", "Missing", "Run 'sage config wizard'"))

        # Check temperature range
        temp = config.get("temperature", 0.2)
        if not 0 <= temp <= 2:
            issues.append(("temperature", f"Out of range: {temp}", "Should be 0.0-2.0"))

        # Check max_tokens
        tokens = config.get("max_tokens", 16384)
        if tokens < 100:
            issues.append(("max_tokens", f"Too low: {tokens}", "Minimum recommended: 1000"))

        return issues

    def load_project_config(self, project_dir: Path) -> dict[str, Any]:
        """Load project-specific config (.sagecrc)."""
        config_files = [
            project_dir / ".sagecrc",
            project_dir / ".sage" / "config.json",
            project_dir / "sage.config.json",
        ]

        for config_file in config_files:
            if config_file.exists():
                return json.loads(config_file.read_text(encoding="utf-8", errors="replace"))

        return {}


# =============================================================================
# Model Selector (P2-71)
# =============================================================================


class ModelSelector:
    """
    Interactive model selector with filtering.

    P2-71: Create model selector with search/filter
    """

    def __init__(self, models: list[dict[str, Any]], console: Console | None = None):
        self.models = models
        self.console = console or Console()

    def select(self, filter_text: str | None = None) -> str | None:
        """Interactive model selection."""
        filtered = self._filter_models(filter_text) if filter_text else self.models

        if not filtered:
            self.console.print("[yellow]No models found[/yellow]")
            return None

        # Display models
        self.console.print("\n[bold]Available Models:[/bold]\n")
        for i, model in enumerate(filtered, 1):
            name = model.get("name", "Unknown")
            provider = model.get("provider", "")
            size = model.get("size", "")
            self.console.print(f"  {i:2}. [cyan]{name:30}[/cyan] {provider:15} {size}")

        # Selection
        self.console.print()
        choice = Prompt.ask(
            "Select model number (or 'q' to cancel)",
            default="1",
        )

        if choice.lower() == "q":
            return None

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(filtered):
                return filtered[idx].get("name")
        except ValueError:
            pass

        self.console.print("[red]Invalid selection[/red]")
        return None

    def _filter_models(self, filter_text: str) -> list[dict[str, Any]]:
        """Filter models by search text."""
        filter_lower = filter_text.lower()
        return [
            m
            for m in self.models
            if filter_lower in m.get("name", "").lower()
            or filter_lower in m.get("provider", "").lower()
        ]


# =============================================================================
# History Browser (P2-72)
# =============================================================================


class HistoryBrowser:
    """
    Browse command history with fuzzy search.

    P2-72: Add history browser with fuzzy search
    """

    def __init__(self, history_file: Path | None = None):
        self.history_file = history_file or Path.home() / ".sage" / "history"
        self._history: list[tuple[float, str]] = []
        self._load_history()

    def _load_history(self) -> None:
        """Load history from file."""
        if self.history_file.exists():
            for line in self.history_file.read_text(encoding="utf-8", errors="replace").splitlines():
                try:
                    ts, cmd = line.split("|", 1)
                    self._history.append((float(ts), cmd))
                except ValueError:
                    continue

    def add(self, command: str) -> None:
        """Add command to history."""
        self._history.append((time.time(), command))
        self._save_history()

    def _save_history(self) -> None:
        """Save history to file."""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, "w", encoding="utf-8") as f:
            for ts, cmd in self._history[-1000:]:  # Keep last 1000
                f.write(f"{ts}|{cmd}\n")

    def search(self, query: str, max_results: int = 20) -> list[str]:
        """Fuzzy search history."""
        commands = [cmd for _, cmd in self._history]
        return difflib.get_close_matches(query, commands, n=max_results, cutoff=0.3)

    def recent(self, count: int = 10) -> list[str]:
        """Get recent commands."""
        return [cmd for _, cmd in self._history[-count:]]


# =============================================================================
# Analytics Dashboard (P2-74)
# =============================================================================


@dataclass
class UsageStats:
    """Usage statistics."""

    command_counts: dict[str, int] = field(default_factory=dict)
    success_counts: dict[str, int] = field(default_factory=dict)
    error_counts: dict[str, int] = field(default_factory=dict)
    total_duration: float = 0.0
    session_count: int = 0


class AnalyticsDashboard:
    """
    Analytics dashboard for usage insights.

    P2-74: Add analytics dashboard
    """

    def __init__(self, storage_path: Path | None = None):
        self.storage_path = storage_path or Path.home() / ".sage" / "analytics.json"
        self.stats = self._load_stats()

    def _load_stats(self) -> UsageStats:
        """Load stats from storage."""
        if self.storage_path.exists():
            data = json.loads(self.storage_path.read_text(encoding="utf-8", errors="replace"))
            return UsageStats(**data)
        return UsageStats()

    def _save_stats(self) -> None:
        """Save stats to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(
            json.dumps(
                {
                    "command_counts": self.stats.command_counts,
                    "success_counts": self.stats.success_counts,
                    "error_counts": self.stats.error_counts,
                    "total_duration": self.stats.total_duration,
                    "session_count": self.stats.session_count,
                },
                indent=2,
            )
        )

    def record_command(
        self,
        command: str,
        success: bool,
        duration: float,
    ) -> None:
        """Record a command execution."""
        self.stats.command_counts[command] = self.stats.command_counts.get(command, 0) + 1

        if success:
            self.stats.success_counts[command] = self.stats.success_counts.get(command, 0) + 1
        else:
            self.stats.error_counts[command] = self.stats.error_counts.get(command, 0) + 1

        self.stats.total_duration += duration
        self._save_stats()

    def start_session(self) -> None:
        """Record session start."""
        self.stats.session_count += 1
        self._save_stats()

    def render(self, console: Console | None = None) -> None:
        """Render analytics dashboard."""
        console = console or Console()

        console.print("\n[bold cyan]SAGE Analytics Dashboard[/bold cyan]\n")

        # Summary
        total_commands = sum(self.stats.command_counts.values())
        total_success = sum(self.stats.success_counts.values())
        success_rate = total_success / total_commands if total_commands > 0 else 0

        console.print("[bold]Summary[/bold]")
        console.print(f"  Total commands: {total_commands}")
        console.print(f"  Success rate: {success_rate:.1%}")
        console.print(f"  Total sessions: {self.stats.session_count}")
        console.print(f"  Total time: {self.stats.total_duration / 60:.1f} minutes")

        # Top commands
        console.print("\n[bold]Top Commands[/bold]")
        sorted_cmds = sorted(
            self.stats.command_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        table = Table()
        table.add_column("Command")
        table.add_column("Count", justify="right")
        table.add_column("Success Rate", justify="right")

        for cmd, count in sorted_cmds:
            success = self.stats.success_counts.get(cmd, 0)
            rate = success / count if count > 0 else 0
            color = "green" if rate > 0.8 else "yellow" if rate > 0.5 else "red"
            table.add_row(cmd, str(count), f"[{color}]{rate:.0%}[/{color}]")

        console.print(table)


# =============================================================================
# Output Pager (P2-63)
# =============================================================================


class OutputPager:
    """
    Built-in output pager.

    P2-63: Implement built-in output pager
    """

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    def page(self, content: str, title: str | None = None) -> None:
        """Display content with paging."""
        lines = content.splitlines()
        terminal_height = shutil.get_terminal_size().lines - 2

        if len(lines) <= terminal_height:
            # No paging needed
            if title:
                self.console.print(f"[bold]{title}[/bold]\n")
            self.console.print(content)
            return

        # Page through content
        current = 0
        while current < len(lines):
            self.console.clear()
            if title:
                self.console.print(
                    f"[bold]{title}[/bold] [dim](lines {current + 1}-{min(current + terminal_height, len(lines))} of {len(lines)})[/dim]\n"
                )

            chunk = "\n".join(lines[current : current + terminal_height])
            self.console.print(chunk)

            self.console.print("\n[dim]Press Enter for next page, 'q' to quit[/dim]")
            response = input()
            if response.lower() == "q":
                break
            current += terminal_height


# =============================================================================
# Multi-select (P2-73)
# =============================================================================


class MultiSelect:
    """
    Multi-select interface for batch operations.

    P2-73: Implement multi-select for batch operations
    """

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    def select(
        self,
        options: list[str],
        title: str = "Select items",
        min_selections: int = 0,
        max_selections: int | None = None,
    ) -> list[str]:
        """Run multi-select interface."""
        self.console.print(f"\n[bold]{title}[/bold]")
        self.console.print("[dim]Enter numbers separated by commas, or 'a' for all[/dim]\n")

        for i, opt in enumerate(options, 1):
            self.console.print(f"  {i}. {opt}")

        self.console.print()
        response = Prompt.ask("Selection")

        if response.lower() == "a":
            return options

        try:
            indices = [int(x.strip()) - 1 for x in response.split(",")]
            selected = [options[i] for i in indices if 0 <= i < len(options)]

            if len(selected) < min_selections:
                self.console.print(
                    f"[yellow]Please select at least {min_selections} items[/yellow]"
                )
                return self.select(options, title, min_selections, max_selections)

            if max_selections and len(selected) > max_selections:
                self.console.print(f"[yellow]Please select at most {max_selections} items[/yellow]")
                return self.select(options, title, min_selections, max_selections)

            return selected
        except (ValueError, IndexError):
            self.console.print("[red]Invalid selection[/red]")
            return self.select(options, title, min_selections, max_selections)
