"""CLI subcommand handlers for `aroom workflow`.

Uses workflow-neutral language throughout. Domain-specific concepts
(issues, PRs) only appear in built-in workflow definitions, not here.
"""

from __future__ import annotations

import argparse
import ast
import asyncio
import json
import logging
import os
import re
import signal
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, TypeVar

from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from ..config import AppConfig

logger = logging.getLogger(__name__)

console = Console()

_T = TypeVar("_T")


def _is_benign_interrupt_teardown(context: dict[str, Any]) -> bool:
    """Detect noisy late stream exceptions emitted during interrupt teardown."""
    if context.get("message") != "Task exception was never retrieved":
        return False

    exc = context.get("exception")
    task = context.get("task") or context.get("future")
    if exc is None or task is None:
        return False

    exc_name = type(exc).__name__
    if exc_name not in {
        "ReadError",
        "CancelledError",
        "ConnectError",
        "ClosedResourceError",
        "BrokenResourceError",
        "APIConnectionError",
    }:
        return False

    try:
        coro_repr = repr(task.get_coro())
    except Exception:
        coro_repr = repr(task)
    return "async_generator_asend" in coro_repr or "__anext__" in coro_repr


async def _run_interruptibly(awaitable: Awaitable[_T]) -> tuple[_T | None, bool]:
    """Run a workflow coroutine with SIGINT handled as a graceful local interrupt."""
    from ..services.async_tasks import cancel_task

    loop = asyncio.get_running_loop()
    previous_handler = loop.get_exception_handler()
    sigint_event = asyncio.Event()
    interrupted = False
    installed_sigint_handler = False

    def _exception_handler(loop_ref: asyncio.AbstractEventLoop, context: dict[str, Any]) -> None:
        if interrupted and _is_benign_interrupt_teardown(context):
            logger.debug("Suppressed async teardown noise during workflow interrupt", exc_info=context.get("exception"))
            return
        if previous_handler is not None:
            previous_handler(loop_ref, context)
        else:
            loop_ref.default_exception_handler(context)

    loop.set_exception_handler(_exception_handler)
    try:
        if hasattr(loop, "add_signal_handler"):
            try:
                loop.add_signal_handler(signal.SIGINT, sigint_event.set)
                installed_sigint_handler = True
            except (NotImplementedError, RuntimeError, ValueError):
                installed_sigint_handler = False

        task = asyncio.create_task(awaitable)
        if not installed_sigint_handler:
            try:
                return await task, False
            except KeyboardInterrupt:
                interrupted = True
                await cancel_task(task, timeout=2.0)
                return None, True

        sigint_wait = asyncio.create_task(sigint_event.wait())
        done, _ = await asyncio.wait({task, sigint_wait}, return_when=asyncio.FIRST_COMPLETED)

        if sigint_wait in done and not task.done():
            interrupted = True
            await cancel_task(task, timeout=2.0)
            return None, True

        await cancel_task(sigint_wait)
        return task.result(), False
    finally:
        if installed_sigint_handler:
            loop.remove_signal_handler(signal.SIGINT)
        loop.set_exception_handler(previous_handler)


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


def _read_diagnosis_output_excerpt(raw_output_path: str, *, max_bytes: int = 4096) -> str | None:
    """Read the tail of a raw output file for diagnosis purposes.

    The tail is usually more useful than the head for tracebacks and command failures.
    """
    path = Path(raw_output_path)
    if not path.is_file():
        return None

    try:
        with path.open("rb") as fh:
            fh.seek(0, 2)
            size = fh.tell()
            if size > max_bytes:
                fh.seek(-max_bytes, 2)
            else:
                fh.seek(0)
            data = fh.read()
    except OSError:
        return None

    text = data.decode("utf-8", errors="replace").strip()
    return text or None


def _enrich_steps_for_diagnosis(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach raw output excerpts used by the diagnosis engine."""
    enriched: list[dict[str, Any]] = []
    for step in steps:
        raw_output_path = step.get("raw_output_path")
        if not raw_output_path:
            enriched.append(step)
            continue

        excerpt = _read_diagnosis_output_excerpt(str(raw_output_path))
        if not excerpt:
            enriched.append(step)
            continue

        step_copy = dict(step)
        step_copy["_diagnosis_output_excerpt"] = excerpt
        enriched.append(step_copy)
    return enriched


def _truncate_text(text: str, max_len: int) -> str:
    """Truncate long transcript fragments to a single compact line."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def _human_count(n: int) -> str:
    """Format counts for compact transcript summaries."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def _short_path(path: str, *, max_len: int = 52) -> str:
    """Prefer readable path tails over giant absolute paths."""
    path = path.strip()
    if not path:
        return ""
    try:
        cwd = str(Path.cwd())
        if path.startswith(cwd + os.sep):
            path = "." + path[len(cwd) :]
    except Exception:
        pass
    if len(path) <= max_len:
        return path
    name = Path(path).name
    if len(name) + 4 <= max_len:
        return f".../{name}"
    return _truncate_text(path, max_len)


def _summarize_text_blob(text: str, *, max_len: int = 100) -> str:
    """Return the first meaningful line plus a compact continuation marker."""
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    summary = lines[0]
    if len(lines) > 1:
        summary += f" (+{len(lines) - 1} lines)"
    return _truncate_text(summary, max_len)


def _format_text_stats(text: str) -> str:
    """Describe large tool payloads without dumping their contents."""
    lines = len(text.splitlines()) or 1
    chars = len(text)
    if lines <= 1:
        return f"{_human_count(chars)} chars"
    return f"{lines} lines, {_human_count(chars)} chars"


def _parse_transcript_object(raw: Any) -> Any | None:
    """Best-effort parse transcript tool payloads from JSON or repr strings."""
    if isinstance(raw, (dict, list)):
        return raw
    if not isinstance(raw, str):
        return None
    text = raw.strip()
    if not text or text[0] not in "{[":
        return None
    try:
        return json.loads(text)
    except Exception:
        pass
    try:
        return ast.literal_eval(text)
    except Exception:
        return None


def _extract_repr_field(raw: str, field: str) -> str:
    """Best-effort extraction for dict-like repr strings that fail to parse."""
    match = re.search(rf"['\"]{re.escape(field)}['\"]:\s*(['\"])(.*?)\1(?=,\s*['\"]\w+['\"]:|\s*}}$)", raw, re.DOTALL)
    if not match:
        return ""
    value = match.group(2)
    try:
        return bytes(value, "utf-8").decode("unicode_escape")
    except Exception:
        return value


def _extract_repr_exit_code(raw: str) -> int | None:
    """Pull exit_code out of a repr string when full parsing fails."""
    match = re.search(r"['\"]exit_code['\"]:\s*(-?\d+)", raw)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def _summarize_tool_call(tool_name: str, arguments: Any) -> str:
    """Compact summaries for common built-in tool calls."""
    parsed = _parse_transcript_object(arguments)
    if isinstance(parsed, dict):
        if tool_name == "bash":
            command = str(parsed.get("command", "")).strip()
            match = re.match(r"^cd\s+(.+?)\s+&&\s+(.+)$", command)
            if match:
                command = match.group(2).strip()
            return _truncate_text(command, 100)
        if tool_name in {"read_file", "write_file", "edit_file"}:
            path = _short_path(str(parsed.get("path", "")))
            return path or _truncate_text(str(parsed), 100)
        if tool_name == "glob_files":
            pattern = str(parsed.get("pattern", "")).strip()
            path = _short_path(str(parsed.get("path", "")).strip())
            if path and pattern:
                return _truncate_text(f"{path} [{pattern}]", 100)
            return _truncate_text(path or pattern or str(parsed), 100)
        if tool_name == "grep":
            pattern = str(parsed.get("pattern", "")).strip()
            path = _short_path(str(parsed.get("path", "")).strip())
            if pattern and path:
                return _truncate_text(f"{pattern} in {path}", 100)
            return _truncate_text(pattern or path or str(parsed), 100)
    return _truncate_text(str(arguments), 100)


def _summarize_tool_result(tool_name: str, output: Any, *, status: str = "") -> str:
    """Compact summaries for common built-in tool results."""
    parsed = _parse_transcript_object(output)
    if isinstance(parsed, dict):
        if tool_name == "bash":
            exit_code = parsed.get("exit_code")
            text = str(parsed.get("stdout", "") or parsed.get("stderr", "") or parsed.get("error", "")).strip()
            if text.startswith(("{", "[")):
                summary = f"JSON output ({_format_text_stats(text)})"
            elif len(text.splitlines()) > 10:
                summary = _format_text_stats(text)
            else:
                summary = _summarize_text_blob(text, max_len=100) if text else ""
            if exit_code not in (None, 0, "0"):
                return f"exit {exit_code}: {summary}" if summary else f"exit {exit_code}"
            return summary or (f"exit {exit_code}" if exit_code is not None else status)
        if tool_name == "read_file":
            path = _short_path(str(parsed.get("path", "")).strip())
            content = str(parsed.get("content", ""))
            stats = _format_text_stats(content) if content else ""
            if path and stats:
                return f"{path} ({stats})"
            return path or stats or _truncate_text(str(parsed), 100)
        if tool_name == "glob_files":
            files = parsed.get("files")
            if isinstance(files, list):
                names = ", ".join(Path(str(f)).name for f in files[:3])
                suffix = f": {names}" if names else ""
                more = f" (+{len(files) - 3})" if len(files) > 3 else ""
                return f"{len(files)} files{suffix}{more}"
        if tool_name == "grep":
            content = str(parsed.get("content", "")).strip()
            if content:
                return _summarize_text_blob(content, max_len=100)
        if tool_name in {"write_file", "edit_file"}:
            path = _short_path(str(parsed.get("path", "")).strip())
            msg = str(parsed.get("message", "")).strip()
            if path and msg:
                return _truncate_text(f"{path} {msg}", 100)
            return _truncate_text(path or msg or str(parsed), 100)
    if tool_name == "bash" and isinstance(output, str):
        stdout = _extract_repr_field(output, "stdout")
        stderr = _extract_repr_field(output, "stderr")
        text = (stdout or stderr or _extract_repr_field(output, "error")).strip()
        exit_code = _extract_repr_exit_code(output)
        if text.startswith(("{", "[")):
            summary = f"JSON output ({_format_text_stats(text)})"
        elif len(text.splitlines()) > 10:
            summary = _format_text_stats(text) if text else ""
        else:
            summary = _summarize_text_blob(text, max_len=100) if text else ""
        if exit_code not in (None, 0):
            return f"exit {exit_code}: {summary}" if summary else f"exit {exit_code}"
        if summary:
            return summary
    return _truncate_text(str(output), 100)


def _describe_transcript_event(event_type: str, payload: dict[str, Any]) -> tuple[str, str, str] | None:
    """Return (label, text, color) for a transcript event."""
    if event_type == "transcript_tool_call":
        tool_name = str(payload.get("tool_name", "")).strip()
        args_str = payload.get("arguments", "")
        if not tool_name and not args_str:
            return None
        summary = _summarize_tool_call(tool_name, args_str)
        return ("tool_call", f"{tool_name}: {summary}" if tool_name else summary, "cyan")

    if event_type == "transcript_tool_result":
        tool_name = str(payload.get("tool_name", "")).strip()
        output = payload.get("output", "")
        status = str(payload.get("status", "")).strip()
        if not tool_name and not output:
            return None
        summary = _summarize_tool_result(tool_name, output, status=status)
        return ("tool_result", f"{tool_name}: {summary}" if tool_name else summary, "cyan")

    if event_type == "transcript_assistant":
        content = str(payload.get("content", "")).strip()
        if not content:
            return None
        return ("assistant", _summarize_text_blob(content, max_len=200), "green")

    if event_type == "transcript_prompt":
        content = str(payload.get("content", "")).strip()
        if not content:
            return None
        summary = _summarize_text_blob(content, max_len=180)
        chars = payload.get("chars")
        if isinstance(chars, int) and chars > len(summary):
            summary = f"{summary} [{_human_count(chars)} chars]"
        return ("prompt", summary, "yellow")

    content = str(payload.get("content", "")).strip()
    if not content:
        return None
    if event_type == "transcript_stderr":
        return ("stderr", _summarize_text_blob(content, max_len=200), "red")
    if event_type == "transcript_stdout":
        return ("stdout", _summarize_text_blob(content, max_len=200), "green")
    return None


def _print_transcript_line(event_type: str, payload: dict[str, Any]) -> None:
    """Print a single transcript event inline under the active step (#1117)."""
    from rich.markup import escape

    described = _describe_transcript_event(event_type, payload)
    if described is None:
        return
    label, text, color = described
    console.print(f"    [{color}]\\[{escape(label)}][/{color}] [{color}]{escape(text)}[/{color}]")


def _summarize_step_reason(payload: dict[str, Any], *, max_len: int = 100) -> str:
    """Extract a compact human-readable reason from a step event payload."""
    for key in ("summary", "error", "reason", "result_summary"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return _summarize_text_blob(value, max_len=max_len)
    return ""


def _make_progress_callback(*, show_transcript: bool = True) -> Any:
    """Build a progress callback for workflow run/resume (#1117).

    Shared between _handle_run and _handle_resume to avoid duplication.
    """
    from .workflow_fmt import format_duration_ms, status_color, status_icon

    def _on_progress(event_type: str, step_id: str | None, payload: dict[str, Any]) -> None:
        if event_type == "step_started" and step_id:
            icon = status_icon("running")
            console.print(f"  [{status_color('running')}]{icon}[/{status_color('running')}] {step_id}")
        elif event_type == "step_finished" and step_id:
            result = payload.get("result_status", "success")
            dur = format_duration_ms(payload.get("duration_ms"))
            icon = status_icon(result)
            color = status_color(result)
            console.print(f"  [{color}]{icon}[/{color}] {step_id}  {dur}")
        elif event_type == "step_continued" and step_id:
            icon = status_icon("failed")
            reason = _summarize_step_reason(payload, max_len=90)
            console.print(
                f"  [{status_color('failed')}]{icon}[/{status_color('failed')}] {step_id}  [yellow](continued)[/yellow]"
            )
            if reason:
                console.print(f"    [yellow]reason:[/yellow] {reason}")
        elif event_type == "step_failed" and step_id:
            icon = status_icon("failed")
            reason = _summarize_step_reason(payload, max_len=90)
            console.print(f"  [{status_color('failed')}]{icon}[/{status_color('failed')}] {step_id}")
            if reason:
                console.print(f"    [red]reason:[/red] {reason}")
        elif event_type == "step_skipped" and step_id:
            icon = status_icon("skipped")
            console.print(f"  [{status_color('skipped')}]{icon}[/{status_color('skipped')}] {step_id}  (skipped)")
        elif show_transcript and event_type.startswith("transcript_"):
            _print_transcript_line(event_type, payload)

    return _on_progress


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
        tool_reg.set_safety_config(config.safety, working_dir=str(Path.cwd()))
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


def _resolve_current_space_id(db: Any) -> str | None:
    """Resolve the current space from the working directory when available."""
    try:
        from ..services.space_storage import resolve_space_by_cwd

        space = resolve_space_by_cwd(db, str(Path.cwd()))
        if space:
            return space["id"]
    except Exception:
        pass
    return None


def _resolve_run_id_or_print(db: Any, run_ref: str | None) -> str | None:
    """Resolve a workflow run ID or unique prefix, printing user-facing errors."""
    if not run_ref:
        console.print("[red]Error:[/red] run_id is required")
        return None

    from ..services.workflow_storage import resolve_workflow_run_id

    try:
        return resolve_workflow_run_id(db, run_ref)
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return None


def _mark_run_interrupted(db: Any, run_id: str) -> dict[str, Any] | None:
    """Convert an interrupted foreground run into a resumable paused state."""
    from datetime import datetime, timezone

    from ..services.workflow_storage import (
        create_workflow_event,
        get_workflow_run,
        list_workflow_steps,
        release_lock,
        update_workflow_run,
        update_workflow_step,
    )

    run = get_workflow_run(db, run_id)
    if not run:
        return None
    if run.get("status") in {"completed", "failed", "cancelled", "blocked", "compensated", "compensation_failed"}:
        return run

    now = datetime.now(timezone.utc).isoformat()
    for step in list_workflow_steps(db, run_id):
        if step.get("status") == "running":
            update_workflow_step(db, step["id"], status="interrupted", completed_at=now)

    updated = update_workflow_run(
        db,
        run_id,
        status="paused",
        stop_reason="cli_interrupted",
        heartbeat_at=now,
    )
    release_lock(db, run_id=run_id)
    create_workflow_event(
        db,
        run_id=run_id,
        event_type="run_interrupted",
        payload={"reason": "cli_interrupt"},
    )
    return updated


def _workflow_run_log_path(config: AppConfig, run_id: str) -> Path:
    log_dir = config.app.data_dir / "logs" / "workflow-runs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"{run_id}.log"


def _spawn_detached_workflow_process(
    config: AppConfig,
    *,
    run_id: str,
    definition_path: Path,
) -> Path:
    """Spawn a detached child process to execute a prepared workflow run."""
    log_path = _workflow_run_log_path(config, run_id)
    cmd = [
        sys.executable,
        "-m",
        "anteroom",
        "workflow",
        "_execute_pending",
        run_id,
        "--definition",
        str(definition_path),
    ]

    kwargs: dict[str, Any] = {
        "cwd": str(Path.cwd()),
        "stdin": subprocess.DEVNULL,
        "stdout": log_path.open("ab"),
        "stderr": subprocess.STDOUT,
        "close_fds": True,
    }
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    else:
        kwargs["start_new_session"] = True

    try:
        proc = subprocess.Popen(cmd, **kwargs)
    finally:
        stdout = kwargs.get("stdout")
        if stdout not in (None, subprocess.DEVNULL):
            stdout.close()

    if proc.poll() is not None:
        raise RuntimeError(f"Detached workflow process exited immediately for run {run_id}")
    return log_path


def _print_run_progress(db: Any, run: dict[str, Any]) -> None:
    """Print timeline-style progress report after a workflow run completes (#1110)."""
    from ..services.workflow_storage import list_workflow_events, list_workflow_steps
    from .workflow_fmt import (
        compute_id_width,
        render_run_header,
        render_step_line,
        status_color,
        status_icon,
    )

    steps = list_workflow_steps(db, run["id"])
    completed = sum(1 for s in steps if s.get("status") in ("completed", "failed", "skipped"))
    header = render_run_header(run, step_count=completed, total_steps=len(steps))
    console.print(f"\n[bold]{header}[/bold]")

    if steps:
        iw = compute_id_width(steps)
        console.print()
        for step in steps:
            step_id = step.get("step_id", "")
            is_nested = "_r" in step_id and step_id.split("_r")[-1].isdigit()
            indent = 1 if is_nested else 0
            line = render_step_line(step, indent=indent, id_width=iw)
            result_status = step.get("result_status") or step.get("status", "pending")
            color = status_color(result_status)
            console.print(f"[{color}]{line}[/{color}]")
            if result_status == "failed":
                reason = _summarize_text_blob(str(step.get("result_summary", "")).strip(), max_len=100)
                if reason:
                    console.print(f"    [red]reason:[/red] {reason}")

    # Diagnosis hint for non-success runs
    run_status = run.get("status", "unknown")
    non_success = {"failed", "blocked", "cancelled", "paused", "compensated", "compensation_failed"}
    if run_status in non_success:
        from ..services.workflow_diagnosis import diagnose

        events = list_workflow_events(db, run["id"])
        dx = diagnose(run, steps, events)
        icon = status_icon(run_status)
        color = status_color(run_status)
        console.print(f"\n  [{color}]{icon} {dx.what}[/{color}]")
        console.print(f"  [dim]{dx.why}[/dim]")
        console.print(f"  [dim]Run: aroom workflow diagnose {run['id'][:8]}[/dim]")
    elif run_status == "completed":
        console.print(f"\n  {status_icon('completed')} Workflow completed successfully")


def _run_workflow(config: AppConfig, args: argparse.Namespace) -> None:
    """Dispatch `aroom workflow` subcommands."""
    action = getattr(args, "workflow_action", None)
    if not action:
        console.print(
            "Usage: aroom workflow {run,status,list,history,transcript,replay,resume,repair,"
            "cancel,approve,deny,respond,watch,diagnose,triggers,schedule,validate,simulate}"
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
    elif action == "transcript":
        _handle_transcript(db, args)
    elif action == "replay":
        _handle_replay(db, args)
    elif action == "resume":
        _handle_resume(config, db, args)
    elif action == "repair":
        _handle_repair(config, db, args)
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
    elif action == "diagnose":
        _handle_diagnose(db, args)
    elif action == "triggers":
        _handle_triggers(config, db, args)
    elif action == "schedule":
        _handle_schedule(config, db, args)
    elif action == "_execute_pending":
        _handle_execute_pending(config, db, args)
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

    current_space_id = _resolve_current_space_id(db)

    # Create engine with AI service dependencies, scoped to current space
    engine, _event_bus = _create_engine(config, db, space_id=current_space_id)

    # Set up real-time progress callback with live transcript (#1110, #1117)
    show_transcript = not getattr(args, "no_transcript", False)
    engine.set_progress_callback(_make_progress_callback(show_transcript=show_transcript))

    console.print(f"\n[bold]Starting workflow:[/bold] {definition.id} v{definition.version}")
    console.print(f"[bold]Target:[/bold] {target_kind}:{target_ref}\n")

    detach = bool(getattr(args, "detach", False))

    async def _prepare_run() -> dict[str, Any]:
        return await engine.prepare_run(
            definition,
            target_kind=target_kind,
            target_ref=target_ref,
            inputs=inputs,
            space_id=current_space_id,
            param_overrides=param_overrides or None,
        )

    try:
        prepared = asyncio.run(_prepare_run())
    except (ValueError, RuntimeError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        _cleanup_event_bus(_event_bus)
        return
    except KeyboardInterrupt:
        console.print("\n[yellow]Workflow start cancelled before execution.[/yellow]")
        _cleanup_event_bus(_event_bus)
        return

    run_id = prepared["id"]
    console.print(f"[dim]Run ID:[/dim] {run_id}")

    if detach:
        try:
            log_path = _spawn_detached_workflow_process(config, run_id=run_id, definition_path=path)
        except Exception as exc:
            from ..services.workflow_storage import update_workflow_run

            update_workflow_run(db, run_id, status="failed", stop_reason="detach_spawn_failed")
            console.print(f"[red]Error:[/red] Could not detach workflow run: {exc}")
            _cleanup_event_bus(_event_bus)
            return

        console.print("[green]Detached[/green]: workflow will continue in the background.")
        console.print(f"[dim]Watch:[/dim] aroom workflow watch {run_id}")
        console.print(f"[dim]Log:[/dim] {log_path}")
        _cleanup_event_bus(_event_bus)
        return

    async def _execute_prepared() -> dict[str, Any]:
        return await engine.execute_pending_run(run_id, definition)

    try:
        run, interrupted = asyncio.run(_run_interruptibly(_execute_prepared()))
    except KeyboardInterrupt:
        updated = _mark_run_interrupted(db, run_id)
        console.print("\n[yellow]Workflow interrupted.[/yellow]")
        if updated is not None:
            console.print(f"[dim]Run paused:[/dim] {run_id}")
            console.print(f"[dim]Resume:[/dim] aroom workflow resume {run_id}")
        _cleanup_event_bus(_event_bus)
        return
    except (ValueError, RuntimeError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        _cleanup_event_bus(_event_bus)
        return

    if interrupted:
        updated = _mark_run_interrupted(db, run_id)
        console.print("\n[yellow]Workflow interrupted.[/yellow]")
        if updated is not None:
            console.print(f"[dim]Run paused:[/dim] {run_id}")
            console.print(f"[dim]Resume:[/dim] aroom workflow resume {run_id}")
        _cleanup_event_bus(_event_bus)
        return

    _print_run_progress(db, run)
    _cleanup_event_bus(_event_bus)


def _handle_status(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow status <run_id>`."""
    from ..services.workflow_storage import count_checkpoints, get_workflow_run, list_workflow_steps

    run_id = _resolve_run_id_or_print(db, getattr(args, "run_id", None))
    if not run_id:
        return

    run = get_workflow_run(db, run_id)
    assert run is not None

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
        from .workflow_fmt import compute_id_width, render_step_line, status_color

        completed = sum(1 for s in steps if s.get("status") in ("completed", "failed", "skipped"))
        iw = compute_id_width(steps)
        console.print(f"\n[bold]Steps ({completed}/{len(steps)}):[/bold]")
        for step in steps:
            step_id = step.get("step_id", "")
            is_nested = "_r" in step_id and step_id.split("_r")[-1].isdigit()
            indent = 1 if is_nested else 0
            line = render_step_line(step, indent=indent, id_width=iw)
            result_status = step.get("result_status") or step.get("status", "pending")
            color = status_color(result_status)
            console.print(f"[{color}]{line}[/{color}]")

    # Compact diagnosis hint for non-success runs (#1103)
    non_success = {"failed", "blocked", "cancelled", "paused", "compensated", "compensation_failed"}
    if run.get("status") in non_success:
        from ..services.workflow_diagnosis import diagnose
        from ..services.workflow_storage import list_workflow_events

        events = list_workflow_events(db, run["id"])
        dx = diagnose(run, steps, events)
        run_id_short = run["id"][:8]
        console.print(f"\n  💡 {dx.what}: {dx.why}")
        console.print(f"  [dim]Run: aroom workflow diagnose {run_id_short}[/dim]")


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
    table.add_column("Run", style="dim", max_width=12)
    table.add_column("Workflow")
    table.add_column("Target", max_width=40)
    table.add_column("State", max_width=28)
    table.add_column("Created")

    for run in runs:
        # Shorten long target refs (e.g., temp file paths from tests)
        target_ref = run["target_ref"]
        if len(target_ref) > 35:
            target_ref = "..." + target_ref[-32:]
        state = run["status"]
        current_step = run.get("current_step_id")
        if current_step and run["status"] not in {"completed", "failed", "cancelled", "compensated"}:
            state = f"{state} · {current_step}"
        table.add_row(
            run["id"][:12],
            run["workflow_id"],
            f"{run['target_kind']}:{target_ref}",
            state,
            run["created_at"][:19],
        )

    console.print(table)
    _cleanup_event_bus(_event_bus)


def _handle_execute_pending(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Execute a prepared pending run from a detached helper process."""
    from ..services.workflow_engine import load_definition
    from ..services.workflow_storage import get_workflow_run
    from ..workflows.gates import register_builtin_gates
    from .workflow_fmt import format_duration_ms, status_icon

    run_id = getattr(args, "run_id", None)
    definition_path = getattr(args, "definition", None)
    if not run_id or not definition_path:
        return

    run = get_workflow_run(db, run_id)
    if not run:
        return

    try:
        definition = load_definition(Path(definition_path))
    except (ValueError, FileNotFoundError) as exc:
        console.print(f"[red]Error loading workflow:[/red] {exc}")
        return

    register_builtin_gates()
    engine, event_bus = _create_engine(config, db, space_id=run.get("space_id"))

    def _on_progress(event_type: str, step_id: str | None, payload: dict) -> None:
        if event_type == "step_started" and step_id:
            print(f"START {step_id}", flush=True)
        elif event_type == "step_finished" and step_id:
            result = payload.get("result_status", "success")
            print(f"{status_icon(result)} {step_id} {format_duration_ms(payload.get('duration_ms'))}", flush=True)
        elif event_type == "step_failed" and step_id:
            print(f"{status_icon('failed')} {step_id} {payload.get('error', '')[:120]}", flush=True)

    engine.set_progress_callback(_on_progress)
    try:
        print(f"Background workflow run {run_id}", flush=True)
        asyncio.run(engine.execute_pending_run(run_id, definition))
    except Exception:
        logger.exception("Detached workflow execution failed for %s", run_id)
    finally:
        _cleanup_event_bus(event_bus)


def _handle_history(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow history <run_id>`."""
    from ..services.workflow_storage import (
        get_workflow_run,
        list_checkpoints,
        list_transcript_events,
        list_workflow_events,
        list_workflow_steps,
    )

    run_id = getattr(args, "run_id", None)
    run_id = _resolve_run_id_or_print(db, run_id)
    if not run_id:
        return

    run = get_workflow_run(db, run_id)
    assert run is not None

    from .workflow_fmt import compute_id_width, format_duration_ms, render_run_header, render_step_line, status_color

    steps = list_workflow_steps(db, run["id"])
    completed = sum(1 for s in steps if s.get("status") in ("completed", "failed", "skipped"))
    header = render_run_header(run, step_count=completed, total_steps=len(steps))
    console.print(f"\n[bold]{header}[/bold]")

    # Timeline overview
    if steps:
        iw = compute_id_width(steps)
        console.print()
        for step in steps:
            step_id = step.get("step_id", "")
            is_nested = "_r" in step_id and step_id.split("_r")[-1].isdigit()
            indent = 1 if is_nested else 0
            line = render_step_line(step, indent=indent, id_width=iw)
            result_status = step.get("result_status") or step.get("status", "pending")
            color = status_color(result_status)
            console.print(f"[{color}]{line}[/{color}]")

    # Detail table
    if steps:
        console.print("\n[bold]Detail:[/bold]")
        has_outputs = any(step.get("result_outputs") for step in steps)
        table = Table(show_header=True)
        table.add_column("Step", style="bold")
        table.add_column("Type")
        table.add_column("Runner")
        table.add_column("Status")
        table.add_column("Result")
        table.add_column("Duration")
        table.add_column("Tokens")
        table.add_column("Idem. Key", max_width=30)
        if has_outputs:
            table.add_column("Outputs", max_width=40)
        table.add_column("Summary", max_width=50)
        for step in steps:
            dur = format_duration_ms(step.get("duration_ms"))
            artifacts = step.get("result_artifacts") or {}
            tokens = _format_tokens(artifacts["total_tokens"]) if artifacts.get("total_tokens") else "-"
            idem_key = step.get("idempotency_key") or "-"
            step_type_display = step["step_type"]
            if artifacts.get("structured_output") is not None:
                step_type_display += " (json)"
            step_id_display = step["step_id"]
            if step.get("is_compensation"):
                step_id_display = f"<- {step_id_display}"
            summary = (step.get("result_summary") or "")[:50]
            if artifacts.get("cache_hit"):
                summary += " (cached)"
            elif artifacts.get("fallback_used"):
                summary += f" (fallback: {artifacts['model']})"
            row: list[str] = [
                step_id_display,
                step_type_display,
                step.get("runner_type") or "-",
                step["status"],
                step.get("result_status") or "-",
                dur,
                tokens,
                idem_key[:30] if len(idem_key) > 30 else idem_key,
            ]
            if has_outputs:
                outputs = step.get("result_outputs") or {}
                outputs_display = ", ".join(f"{k}={v}" for k, v in outputs.items())[:40] if outputs else "-"
                row.append(outputs_display)
            row.append(summary)
            table.add_row(*row)
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

    if getattr(args, "transcript", False):
        from .transcript_renderer import render_step_transcript

        transcript_events = list_transcript_events(db, run["id"])
        if transcript_events:
            render_step_transcript(
                console,
                transcript_events,
                step_header=f"Transcript: {run['id'][:8]}",
            )
        else:
            console.print("\n[dim]No transcript events found.[/dim]")


def _handle_transcript(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow transcript <run_id> [step_id]`."""
    from ..services.workflow_storage import get_workflow_run, list_transcript_events
    from .transcript_renderer import render_step_transcript

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[yellow]Usage: aroom workflow transcript <run_id> [step_id][/]")
        return
    run_id = _resolve_run_id_or_print(db, run_id)
    if not run_id:
        return

    step_id = getattr(args, "step_id", None)

    run = get_workflow_run(db, run_id)
    assert run is not None

    events = list_transcript_events(db, run_id, step_id=step_id)
    if not events:
        console.print("[dim]No transcript events found.[/dim]")
        return

    header = f"Transcript: {run_id[:8]}"
    if step_id:
        header += f" / {step_id}"
    render_step_transcript(console, events, step_header=header)


def _handle_replay(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow replay <run_id>`. Show full run-level replay."""
    from ..cli.transcript_renderer import render_run_replay
    from ..services.workflow_storage import get_run_replay_events, get_workflow_run, list_workflow_steps

    run_id = getattr(args, "run_id", None)
    if not run_id:
        console.print("[yellow]Usage: workflow replay <run_id>[/]")
        return
    run_id = _resolve_run_id_or_print(db, run_id)
    if not run_id:
        return

    run = get_workflow_run(db, run_id)
    assert run is not None

    events = get_run_replay_events(db, run_id)
    steps = list_workflow_steps(db, run_id)
    render_run_replay(console, events, steps=steps)


def _handle_resume(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow resume <run_id>`."""
    from ..services.workflow_engine import load_definition
    from ..services.workflow_storage import check_approval_timeouts, check_decision_timeouts, get_workflow_run

    run_id = _resolve_run_id_or_print(db, getattr(args, "run_id", None))
    if not run_id:
        return

    # On-demand timeout checks
    check_approval_timeouts(db)
    check_decision_timeouts(db)

    # Load run FIRST to extract space_id for scoped registry rebuild (#957)
    run = get_workflow_run(db, run_id)
    assert run is not None

    # Create engine scoped to the run's space_id (#957 resume stability)
    run_space_id = run.get("space_id")
    engine, _event_bus = _create_engine(config, db, space_id=run_space_id)

    # Recover any stale runs first (on-demand recovery)
    asyncio.run(engine.recover_interrupted_runs())

    if run["status"] not in ("paused", "waiting_for_approval", "waiting_for_input", "compensating", "failed"):
        console.print(
            f"[red]Error:[/red] Run is not resumable (status: {run['status']}). "
            "Only paused, waiting_for_approval, waiting_for_input, compensating, or failed runs can be resumed."
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

    # Set up real-time progress callback with live transcript (#1117)
    show_transcript = not getattr(args, "no_transcript", False)
    engine.set_progress_callback(_make_progress_callback(show_transcript=show_transcript))

    console.print(f"\n[bold]Resuming workflow:[/bold] {definition.id}")
    console.print(f"[bold]Run:[/bold] {run_id[:12]}...")
    if from_step:
        console.print(f"[bold]From step:[/bold] {from_step}")
    if force:
        console.print("[yellow]Force mode: definition drift will be overridden[/yellow]")

    try:
        result, interrupted = asyncio.run(
            _run_interruptibly(
                engine.resume_run(
                    run_id,
                    definition,
                    from_step=from_step,
                    force=force,
                )
            )
        )
    except (ValueError, RuntimeError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        _cleanup_event_bus(_event_bus)
        return

    if interrupted:
        updated = _mark_run_interrupted(db, run_id)
        console.print("\n[yellow]Workflow interrupted.[/yellow]")
        if updated is not None:
            console.print(f"[dim]Run paused:[/dim] {run_id}")
            console.print(f"[dim]Resume:[/dim] aroom workflow resume {run_id}")
        _cleanup_event_bus(_event_bus)
        return

    _print_run_progress(db, result)
    _cleanup_event_bus(_event_bus)


def _handle_repair(config: AppConfig, db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow repair <run_id> --field <path> --value <value>`.

    Repairs a field on a paused/waiting run or one of its completed steps.
    Shows before/after diff.
    """
    import json as json_mod

    from ..services.workflow_storage import get_workflow_run

    run_id = getattr(args, "run_id", None)
    run_id = _resolve_run_id_or_print(db, run_id)
    if not run_id:
        return

    field_path = getattr(args, "field", None)
    raw_value = getattr(args, "value", None)
    if not field_path or raw_value is None:
        console.print("[red]Error:[/red] --field and --value are required")
        return

    run = get_workflow_run(db, run_id)
    assert run is not None

    # Parse value as JSON; fall back to string
    try:
        parsed_value = json_mod.loads(raw_value)
    except (json_mod.JSONDecodeError, TypeError):
        parsed_value = raw_value

    # Determine scope: "step.<step_id>.<field>" or "<field>"
    parts = field_path.split(".", 2)
    step_id: str | None = None
    field_name: str

    if len(parts) >= 3 and parts[0] == "step":
        step_id = parts[1]
        field_name = parts[2]
        if not step_id:
            console.print("[red]Error:[/red] Step ID cannot be empty. Use 'step.<step_id>.<field>'.")
            return
    elif len(parts) == 1:
        field_name = parts[0]
    else:
        console.print(
            "[red]Error:[/red] Invalid field path. Use 'inputs' for run fields "
            "or 'step.<step_id>.result_artifacts' for step fields."
        )
        return

    engine, _event_bus = _create_engine(config, db)

    try:
        if step_id:
            # Capture old value for display
            from ..services.workflow_storage import list_workflow_steps

            steps = list_workflow_steps(db, run_id)
            old_step = next((s for s in reversed(steps) if s["step_id"] == step_id), None)
            old_step_value = old_step.get(field_name) if old_step else None
            asyncio.run(engine.repair_step(run_id, step_id, field_name, parsed_value))
            console.print(f"[green]Repaired step {step_id} field '{field_name}'[/green]")
            console.print(f"  [dim]Old:[/dim] {old_step_value}")
            console.print(f"  [dim]New:[/dim] {parsed_value}")
        else:
            old_value = run.get(field_name)
            asyncio.run(engine.repair_run(run_id, field_name, parsed_value))
            console.print(f"[green]Repaired run field '{field_name}'[/green]")
            console.print(f"  [dim]Old:[/dim] {old_value}")
            console.print(f"  [dim]New:[/dim] {parsed_value}")
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
    finally:
        _cleanup_event_bus(_event_bus)


def _handle_cancel(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow cancel <run_id>`. Uses engine request_cancel (#890)."""
    from ..services.workflow_storage import get_workflow_run

    run_id = getattr(args, "run_id", None)
    run_id = _resolve_run_id_or_print(db, run_id)
    if not run_id:
        return

    run = get_workflow_run(db, run_id)
    assert run is not None

    terminal = {"completed", "failed", "cancelled", "blocked", "compensated", "compensation_failed"}
    if run["status"] in terminal:
        console.print(f"[red]Error:[/red] Run is already in terminal status: {run['status']}. Cannot cancel.")
        return

    from ..services.workflow_engine import WorkflowEngine

    try:
        updated = asyncio.run(WorkflowEngine.request_cancel(db, run_id))
    except ValueError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return

    console.print(f"[green]Run {run_id[:12]}... cancel requested (status: {updated['status']})[/green]")


def _handle_approve(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow approve <run_id>`. Approve a pending tool approval request."""
    from ..services.workflow_storage import (
        check_approval_timeouts,
        get_pending_approval,
        get_workflow_run,
        resolve_approval_request,
    )

    run_id = getattr(args, "run_id", None)
    run_id = _resolve_run_id_or_print(db, run_id)
    if not run_id:
        return

    check_approval_timeouts(db)

    run = get_workflow_run(db, run_id)
    assert run is not None

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
    run_id = _resolve_run_id_or_print(db, run_id)
    if not run_id:
        return

    check_approval_timeouts(db)

    run = get_workflow_run(db, run_id)
    assert run is not None

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
    run_id = _resolve_run_id_or_print(db, run_id)
    if not run_id:
        return

    check_decision_timeouts(db)

    run = get_workflow_run(db, run_id)
    assert run is not None

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


def _handle_diagnose(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow diagnose <run_id>`. Explain why a run stopped."""
    from rich.panel import Panel

    from ..services.workflow_diagnosis import diagnose
    from ..services.workflow_storage import get_workflow_run, list_workflow_events, list_workflow_steps
    from .workflow_fmt import compute_id_width, render_diagnosis, render_run_header, render_step_line, status_color

    run_id = _resolve_run_id_or_print(db, getattr(args, "run_id", None))
    if not run_id:
        return

    run = get_workflow_run(db, run_id)
    assert run is not None

    status = run.get("status", "unknown")
    success_statuses = {"completed", "running", "claimed", "pending"}
    if status in success_statuses:
        console.print(f"[green]Run {run_id[:8]} is {status} — no diagnosis needed.[/green]")
        return

    steps = _enrich_steps_for_diagnosis(list_workflow_steps(db, run_id))
    events = list_workflow_events(db, run_id)

    # Show run header + timeline
    completed = sum(1 for s in steps if s.get("status") in ("completed", "failed", "skipped"))
    iw = compute_id_width(steps)
    header = render_run_header(run, step_count=completed, total_steps=len(steps))
    console.print(f"\n[bold]{header}[/bold]\n")
    for step in steps:
        step_id = step.get("step_id", "")
        is_nested = "_r" in step_id and step_id.split("_r")[-1].isdigit()
        indent = 1 if is_nested else 0
        line = render_step_line(step, indent=indent, id_width=iw)
        result_status = step.get("result_status") or step.get("status", "pending")
        color = status_color(result_status)
        console.print(f"[{color}]{line}[/{color}]")

    # Diagnosis
    result = diagnose(run, steps, events)
    diagnosis_text = render_diagnosis(result)
    console.print()
    console.print(Panel(diagnosis_text, title="Diagnosis", border_style="yellow"))


def _handle_watch(db: Any, args: argparse.Namespace) -> None:
    """Handle `aroom workflow watch <run_id>`. Poll and display live timeline with transcript."""
    import collections
    import time

    from rich.live import Live
    from rich.text import Text

    from ..services.workflow_storage import (
        get_workflow_run,
        list_transcript_events,
        list_workflow_steps,
    )
    from .workflow_fmt import (
        compute_id_width,
        format_elapsed,
        render_run_header,
        render_step_line,
        status_color,
        status_icon,
    )

    run_id = _resolve_run_id_or_print(db, getattr(args, "run_id", None))
    if not run_id:
        return

    run = get_workflow_run(db, run_id)
    assert run is not None

    terminal_statuses = {"completed", "failed", "cancelled", "blocked", "compensated", "compensation_failed"}
    max_transcript_lines = 50
    transcript: collections.deque[dict[str, Any]] = collections.deque(maxlen=max_transcript_lines)
    last_output_event_id = 0
    last_transcript_step: str | None = None

    def _build_display(
        run: dict[str, Any],
        steps: list[dict[str, Any]],
        transcript_lines: collections.deque[dict[str, Any]],
    ) -> Text:
        """Build the Rich Text renderable for the current watch state."""
        completed = sum(1 for s in steps if s.get("status") in ("completed", "failed", "skipped"))
        header = render_run_header(run, step_count=completed, total_steps=len(steps))

        text = Text()
        text.append(header + "\n\n", style="bold")

        iw = compute_id_width(steps)
        active_step_id: str | None = None
        for step in steps:
            step_id = step.get("step_id", "")
            is_nested = "_r" in step_id and step_id.split("_r")[-1].isdigit()
            indent = 1 if is_nested else 0
            line = render_step_line(step, indent=indent, id_width=iw)
            result_status = step.get("result_status") or step.get("status", "pending")
            color = status_color(result_status)

            if step.get("status") == "running":
                active_step_id = step_id
                if step.get("started_at"):
                    elapsed = format_elapsed(step["started_at"])
                    line = line.rstrip()
                    line += f"  {elapsed}"

            text.append(line + "\n", style=color if result_status != "pending" else "dim")

        # Transcript section
        if transcript_lines:
            step_label = active_step_id or "output"
            text.append(f"\n  -- transcript ({step_label}) ", style="dim")
            text.append("-" * 30 + "\n", style="dim")
            for entry in transcript_lines:
                ts = entry.get("ts", "")[:8]  # HH:MM:SS
                etype = entry.get("event_type", "transcript_stdout")
                payload = entry.get("payload", {})
                described = _describe_transcript_event(etype, payload)
                if described is None:
                    continue
                label, line_text, color = described
                text.append(f"  {ts}  ", style="dim")
                text.append(f"[{label}] ", style=color)
                text.append(f"{line_text}\n", style=color)

        return text

    status = run.get("status", "unknown")
    if status in terminal_statuses:
        steps = list_workflow_steps(db, run_id)
        display = _build_display(run, steps, transcript)
        console.print(display)
        console.print()
        icon = status_icon(status)
        console.print(f"  {icon} Run {status}")
        if run.get("stop_reason"):
            console.print(f"  Reason: {run['stop_reason']}")
        return

    try:
        with Live(console=console, refresh_per_second=1) as live:
            while True:
                run = get_workflow_run(db, run_id)
                if not run:
                    live.stop()
                    console.print("[red]Run deleted[/red]")
                    break

                steps = list_workflow_steps(db, run_id)

                # Fetch new transcript events since last poll
                new_outputs = list_transcript_events(db, run_id, since_id=last_output_event_id)
                for evt in new_outputs:
                    payload = evt.get("payload") or {}
                    step_id = evt.get("step_id", "")
                    # Clear transcript on step transition
                    if step_id != last_transcript_step and last_transcript_step is not None:
                        transcript.clear()
                    last_transcript_step = step_id
                    transcript.append(
                        {
                            "event_type": evt.get("event_type", "transcript_stdout"),
                            "payload": payload,
                            "ts": evt.get("created_at", ""),
                        }
                    )
                    eid = evt.get("id", 0)
                    if eid > last_output_event_id:
                        last_output_event_id = eid

                display = _build_display(run, steps, transcript)
                live.update(display)

                status = run.get("status", "unknown")
                if status in terminal_statuses:
                    live.stop()
                    console.print()
                    icon = status_icon(status)
                    color = status_color(status)
                    console.print(f"  [{color}]{icon} Run {status}[/{color}]")
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
