"""Workflow transcript rendering using Anteroom chat renderer patterns (#1112)."""

from __future__ import annotations

import json
from typing import Any

from rich.markup import escape

from anteroom.cli import renderer

# Transcript event type to display role mapping
TRANSCRIPT_ROLES: dict[str, str] = {
    "transcript_assistant": "assistant",
    "transcript_tool_call": "tool_call",
    "transcript_tool_result": "tool_result",
    "transcript_stdout": "stdout",
    "transcript_stderr": "stderr",
    "transcript_usage": "usage",
}


def render_run_replay(
    console: Any,
    events: list[dict[str, Any]],
    steps: list[dict[str, Any]] | None = None,
) -> None:
    """Render a full run-level replay stitching transcript and lifecycle events."""
    if not events:
        console.print("[dim]No replay data.[/]")
        return

    current_step: str | None = None
    total_tokens = 0

    for event in events:
        etype = event.get("event_type", "")
        step_id = event.get("step_id")
        payload = event.get("payload") or {}

        # Step boundary header
        if step_id != current_step and step_id is not None:
            current_step = step_id
            step_info = ""
            if steps:
                for s in steps:
                    if s.get("step_id") == step_id:
                        stype = s.get("step_type", "")
                        runner = s.get("runner_type", "")
                        step_info = f" ({stype}"
                        if runner:
                            step_info += f": {runner}"
                        step_info += ")"
                        break
            console.print(f"\n[bold]{'─' * 50}[/]")
            console.print(f"[bold]  Step: {escape(step_id)}{step_info}[/]")
            console.print(f"[bold]{'─' * 50}[/]")

        # Lifecycle events
        if etype == "step_started":
            continue  # boundary header already shown
        elif etype == "step_finished":
            status = payload.get("result_status", "")
            duration = payload.get("duration_ms", 0)
            color = (
                "green"
                if status == "success"
                else "yellow"
                if status == "blocked"
                else "red"
                if status == "failed"
                else "dim"
            )
            dur_str = f"{duration / 1000:.1f}s" if duration >= 1000 else f"{duration}ms"
            icon = "\u2713" if status == "success" else "\u2717"
            console.print(f"  [{color}]{icon} {status}[/{color}] [dim]({dur_str})[/]")
        elif etype == "step_failed":
            err = payload.get("error", "")[:100]
            console.print(f"  [red]\u2717 failed \u2014 {escape(err)}[/]")
        else:
            # Transcript events — delegate to existing renderer
            if etype == "transcript_usage":
                total_tokens += payload.get("total_tokens", 0)
            render_transcript_entry(console, event)

    # Run summary footer
    console.print(f"\n[bold]{'═' * 50}[/]")
    step_count = len({e.get("step_id") for e in events if e.get("step_id")})
    console.print(f"  [bold]Replay complete[/]: {step_count} steps, {total_tokens:,} tokens")
    console.print(f"[bold]{'═' * 50}[/]")


def render_step_transcript(
    console: Any,
    events: list[dict[str, Any]],
    *,
    show_usage: bool = True,
    step_header: str | None = None,
) -> None:
    """Render transcript events for a single workflow step.

    Uses the existing chat renderer helpers from renderer.py for tool calls
    and assistant output, adding step context and usage annotations.
    """
    if step_header:
        console.print(f"\n[bold]── {escape(step_header)} ──[/bold]")

    for event in events:
        render_transcript_entry(console, event, show_usage=show_usage)


def render_transcript_entry(
    console: Any,
    event: dict[str, Any],
    *,
    show_usage: bool = True,
) -> None:
    """Render a single transcript event using chat-style formatting."""
    etype = event.get("event_type", "")
    payload = event.get("payload") or {}

    if etype == "transcript_assistant":
        content = payload.get("content", "")
        if content:
            # Route through the assistant-prose hierarchy helper (#1370) so
            # workflow replay and live REPL output share the same lane.
            renderer.render_assistant_prose(content)

    elif etype == "transcript_tool_call":
        tool_name = payload.get("tool_name", "unknown")
        args = payload.get("arguments", "")
        # render_tool_call_start expects a dict; parse if we received a JSON string
        if isinstance(args, str):
            try:
                args_dict: dict[str, Any] = json.loads(args)
            except (json.JSONDecodeError, ValueError):
                args_dict = {"_raw": args}
        else:
            args_dict = args if isinstance(args, dict) else {"_raw": str(args)}
        renderer.render_tool_call_start(tool_name, args_dict)

    elif etype == "transcript_tool_result":
        tool_name = payload.get("tool_name", "unknown")
        status = payload.get("status", "")
        output = payload.get("output", "")
        renderer.render_tool_call_end(tool_name, status, output)

    elif etype == "transcript_stdout":
        content = payload.get("content", "")
        if content:
            renderer.render_system_message("info", content)

    elif etype == "transcript_stderr":
        content = payload.get("content", "")
        if content:
            renderer.render_system_message("error", content)

    elif etype == "transcript_usage" and show_usage:
        tokens = payload.get("total_tokens", 0)
        elapsed = payload.get("elapsed_ms", 0)
        parts = []
        if tokens:
            parts.append(f"{tokens:,} tokens")
        if elapsed:
            if elapsed >= 1000:
                parts.append(f"{elapsed / 1000:.1f}s")
            else:
                parts.append(f"{elapsed}ms")
        if parts:
            console.print(f"[dim]  {' · '.join(parts)}[/dim]")
