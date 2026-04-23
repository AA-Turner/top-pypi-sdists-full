"""CLI handlers for runtime hook developer tooling (#1495).

Commands:
  aroom hook list      — list all configured hooks with trust status
  aroom hook validate  — validate hook config against the resolved snapshot
  aroom hook replay    — dry-run replay of a hook event (no audit emission)
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse

    from ..config import AppConfig


def _run_hook_list(config: AppConfig) -> None:
    """Print all configured hooks as a Rich table."""
    from rich.console import Console
    from rich.table import Table

    hooks = config.hooks
    all_entries = [("pre_tool", e) for e in hooks.pre_tool] + [("post_tool", e) for e in hooks.post_tool]

    console = Console()
    if not all_entries:
        console.print("[dim]No hooks configured.[/dim]")
        return

    table = Table(title="Configured Hooks", show_lines=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Event")
    table.add_column("Matcher")
    table.add_column("Runner")
    table.add_column("Trust Source")
    table.add_column("Executable")

    for event, entry in all_entries:
        matcher_str = entry.matcher.tool_name
        if entry.matcher.arguments:
            matcher_str += f" {entry.matcher.arguments}"
        if entry.runner.type == "command":
            cmd_preview = entry.runner.command[:50]
            runner_str = f"command: {cmd_preview}{'…' if len(entry.runner.command) > 50 else ''}"
        elif entry.runner.type == "webhook":
            runner_str = f"webhook: {entry.runner.url}"
        else:
            runner_str = entry.runner.type
        exec_str = "[green]yes[/green]" if entry.is_executable else "[yellow]no (pack)[/yellow]"
        table.add_row(entry.id, event, matcher_str, runner_str, entry.trust_source, exec_str)

    console.print(table)


def run_hook_validate_standalone(team_config_path: Path | None = None) -> None:
    """Validate hook config before the normal config load pipeline.

    Reads both personal and team config raw YAML directly so that invalid
    entries (unknown runner type, empty command/url) are reported per-hook
    instead of causing a generic "Configuration error" exit from
    _load_config_or_exit().  If both layers are valid, loads config normally
    (honoring team_config_path) and shows trust/executability for the resolved
    snapshot.

    team_config_path mirrors the --team-config CLI flag so that hooks defined
    only in a team file are also validated.
    """
    import yaml
    from rich.console import Console

    from ..config import _get_config_path
    from ..services.config_validator import validate_config
    from ..services.team_config import discover_team_config, load_team_config

    console = Console()
    config_path = _get_config_path()
    raw: dict[str, Any] = {}

    # Collect hook errors from personal config layer.
    from ..services.config_validator import ConfigError

    hook_errors: list[ConfigError] = []
    if config_path.exists():
        with open(config_path, encoding="utf-8-sig") as fh:
            raw = yaml.safe_load(fh) or {}
        result = validate_config(raw)
        hook_errors.extend(e for e in result.errors if e.path.startswith("hooks.") and e.severity == "error")

    # Collect hook errors from team config layer (same discovery logic as _load_config_or_exit).
    _personal_team_path = raw.get("team_config_path")
    team_path = discover_team_config(
        cli_path=team_config_path,
        env_path=os.environ.get("AI_CHAT_TEAM_CONFIG"),
        personal_path=_personal_team_path,
    )
    if team_path and team_path.exists():
        try:
            team_raw, _ = load_team_config(team_path, interactive=False)
        except ValueError:
            team_raw = {}
        if team_raw:
            team_result = validate_config(team_raw)
            hook_errors.extend(e for e in team_result.errors if e.path.startswith("hooks.") and e.severity == "error")

    if not config_path.exists() and not team_path:
        console.print("[dim]No config file found — no hooks to validate.[/dim]")
        return

    if hook_errors:
        console.print("[bold red]Hook configuration errors:[/bold red]")
        for err in hook_errors:
            console.print(f"  [red]✗[/red] {err.path}: {err.message}")
        sys.exit(1)

    # Both layers are valid — load normally and show resolved snapshot.
    try:
        from ..config import load_config

        config, _ = load_config(team_config_path=team_config_path)
    except ValueError as exc:
        console.print(f"[red]Configuration error:[/red] {exc}")
        sys.exit(1)

    _run_hook_validate(config)


def _run_hook_validate(config: AppConfig) -> None:
    """Report trust/executability for every entry in the resolved hook snapshot.

    By the time this is called the config is already valid (config_validator
    rejected bad runner types / empty command / empty url before load).  This
    function only reports which resolved entries will actually execute at
    runtime and which are present but non-executable (pack trust boundary).
    """
    from rich.console import Console

    console = Console()
    hooks = config.hooks
    all_entries = list(hooks.pre_tool) + list(hooks.post_tool)

    if not all_entries:
        console.print("[dim]No hooks configured — nothing to validate.[/dim]")
        return

    for entry in all_entries:
        prefix = f"[cyan]{entry.id}[/cyan]"
        console.print(f"[green]✓[/green] {prefix} ({entry.event}, {entry.runner.type})")

        if not entry.is_executable:
            console.print(
                f"  [yellow]⚠[/yellow] {prefix}: trust_source={entry.trust_source!r} — "
                f"present but not executable (phase-1: only personal/team hooks run)"
            )


def _run_hook_replay(config: AppConfig, args: argparse.Namespace) -> None:
    """Replay a hook event in dry-run mode and print the decision trace."""
    from rich.console import Console
    from rich.table import Table

    from ..services.hooks import replay_hook_event

    event: str = args.hook_event
    if event not in ("pre_tool", "post_tool"):
        print(f"error: event must be pre_tool or post_tool, got {event!r}", file=sys.stderr)
        sys.exit(1)

    tool_name: str = getattr(args, "tool", "*")
    raw_args: str = getattr(args, "arguments", "{}") or "{}"
    raw_output: str | None = getattr(args, "output", None)

    try:
        _args_parsed = json.loads(raw_args)
    except json.JSONDecodeError as exc:
        print(f"error: --args is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(_args_parsed, dict):
        print("error: --args must be a JSON object, not a scalar or array", file=sys.stderr)
        sys.exit(1)
    tool_arguments: dict[str, Any] = _args_parsed

    tool_output: dict[str, Any] | None = None
    if raw_output:
        try:
            _output_parsed = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            print(f"error: --output is not valid JSON: {exc}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(_output_parsed, dict):
            print("error: --output must be a JSON object, not a scalar or array", file=sys.stderr)
            sys.exit(1)
        tool_output = _output_parsed

    result = asyncio.run(
        replay_hook_event(
            config.hooks,
            event,
            tool_name,
            tool_arguments,
            tool_output,
            allowed_domains=list(config.ai.allowed_domains),
            block_localhost=config.ai.block_localhost_api,
        )
    )

    console = Console()
    console.print(f"\n[bold]Hook replay:[/bold] {event} / {tool_name}")
    console.print("[dim]Dry-run — no audit events emitted[/dim]\n")

    if not result.entries:
        console.print("[dim]No hooks configured for this event.[/dim]")
        return

    table = Table(show_lines=True)
    table.add_column("Hook ID", style="cyan", no_wrap=True)
    table.add_column("Trust")
    table.add_column("Matched")
    table.add_column("Ran")
    table.add_column("Decision")
    table.add_column("Message")
    table.add_column("ms", justify="right")

    for entry in result.entries:
        matched_str = "[green]yes[/green]" if entry.matched else "[dim]no[/dim]"

        if entry.skipped_reason == "not_executable":
            ran_str = "[yellow]skipped (pack)[/yellow]"
        elif entry.skipped_reason == "no_match":
            ran_str = "[dim]—[/dim]"
        else:
            ran_str = "[green]yes[/green]"

        if entry.decision is not None:
            outcome = entry.decision.outcome
            _outcome_styles = {
                "allow": "[green]allow[/green]",
                "deny": "[red]deny[/red]",
                "ask": "[yellow]ask[/yellow]",
            }
            decision_str = _outcome_styles.get(outcome, outcome)
            if entry.decision.error_type:
                decision_str += f" [dim]({entry.decision.error_type})[/dim]"
            raw_msg = entry.decision.message
            msg = raw_msg[:60] + ("…" if len(raw_msg) > 60 else "")
            ms_str = f"{entry.execution_ms:.0f}"
        else:
            decision_str = "[dim]—[/dim]"
            msg = ""
            ms_str = "—"

        table.add_row(entry.hook_id, entry.trust_source, matched_str, ran_str, decision_str, msg, ms_str)

    console.print(table)
    console.print()

    final = result.final_decision
    if final.outcome == "allow":
        console.print("[green]Final decision: allow[/green]")
    elif final.outcome == "deny":
        console.print(f"[red]Final decision: deny[/red]  {final.message}")
    else:
        console.print(f"[yellow]Final decision: {final.outcome}[/yellow]  {final.message}")


def _run_hook(config: AppConfig, args: argparse.Namespace) -> None:
    """Dispatch aroom hook subcommands."""
    action: str | None = getattr(args, "hook_action", None)
    if action == "list":
        _run_hook_list(config)
    elif action == "validate":
        run_hook_validate_standalone()
    elif action == "replay":
        _run_hook_replay(config, args)
    else:
        print("usage: aroom hook {list,validate,replay}", file=sys.stderr)
        sys.exit(1)
