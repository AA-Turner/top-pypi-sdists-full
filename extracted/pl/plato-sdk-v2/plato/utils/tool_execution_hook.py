"""CLI hook entrypoints for pre-tool execution attribution."""

from __future__ import annotations

import argparse
import base64
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import uuid
from datetime import UTC, datetime
from pathlib import Path

from plato.utils.tool_execution import (
    DEFAULT_TOOL_EXECUTION_CONTEXT_PATH,
    ToolStartRecord,
    append_tool_start_record,
    load_tool_execution_context,
    normalize_tool_input,
)

logger = logging.getLogger(__name__)

_AGENT_BROWSER_SCREENSHOT_TIMEOUT_S = 5.0


def _write_record(mode: str, payload: dict[str, object]) -> None:
    context = load_tool_execution_context(DEFAULT_TOOL_EXECUTION_CONTEXT_PATH)
    if context is None:
        return

    hook_spool_path = Path(context.hook_spool_path)
    record = ToolStartRecord(
        source=mode,
        observed_at=datetime.now(UTC),
        tool_name=str(payload.get("tool_name", "")),
        normalized_tool_input=normalize_tool_input(payload.get("tool_input", {})),
        tool_use_id=(str(payload["tool_use_id"]) if isinstance(payload.get("tool_use_id"), str) else None),
        session_id=str(payload.get("session_id", "")),
        transcript_path=str(payload.get("transcript_path", "")),
        cwd=str(payload.get("cwd", "")),
    )
    append_tool_start_record(hook_spool_path, record)


_SESSION_FLAG_RE = re.compile(r"--session(?:=|\s+)([A-Za-z0-9_.-]+)")


def _parse_browser_session(command: str) -> str | None:
    """Best-effort extraction of ``agent-browser --session <alias>``.

    Returns the alias of the first explicit ``--session`` flag found in the
    command. ``None`` if absent.
    """
    if "agent-browser" not in command:
        return None
    m = _SESSION_FLAG_RE.search(command)
    if m:
        return m.group(1)
    return None


def _capture_post_tool_screenshot(
    *,
    session: str,
    tool_use_id: str,
) -> tuple[bytes, str] | None:
    """Run ``agent-browser screenshot <path>`` and return ``(bytes, mime)``."""
    tmp_dir = Path(tempfile.gettempdir()) / "plato-shots"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    out_path = tmp_dir / f"{tool_use_id}-{uuid.uuid4().hex}.png"

    # Ensure agent-browser resolves on PATH inside the hook subprocess.
    home = os.environ.get("HOME") or "/root"
    env = dict(os.environ)
    env["PATH"] = ":".join([f"{home}/.bun/bin", f"{home}/.local/bin", "/usr/local/bin", env.get("PATH", "")])

    # `agent-browser screenshot` takes the output path as a positional arg,
    # not a flag — the CLI auto-detects "is path vs selector" from the leading
    # char (`/`, `./`, `../` or a known extension all signal a path).
    cmd = ["agent-browser", "--session", session, "screenshot", str(out_path)]
    try:
        result = subprocess.run(
            cmd,
            timeout=_AGENT_BROWSER_SCREENSHOT_TIMEOUT_S,
            capture_output=True,
            check=False,
            env=env,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        logger.debug("agent-browser screenshot failed for %s: %s", session, exc)
        return None
    if result.returncode != 0 or not out_path.exists():
        logger.debug(
            "agent-browser screenshot rc=%d stderr=%s",
            result.returncode,
            (result.stderr or b"").decode(errors="replace")[-200:],
        )
        return None
    try:
        data = out_path.read_bytes()
    finally:
        try:
            out_path.unlink()
        except OSError:
            pass
    return data, "image/png"


def _emit_screenshot_span(
    *,
    tool_use_id: str,
    session: str,
    tool_name: str,
    b64: str,
    mime: str,
) -> None:
    """Emit one screenshot span attributed to the agent's trace.

    Shaped to look like an ``atif.step.<N>`` system step so the Chronos
    trajectory viewer groups it with the agent's other steps (the viewer
    detects "this span belongs to an agent" by the presence of
    ``atif.step.id`` on it). A ``plato.harness.span_kind`` attribute marks it
    as harness-injected so it can be filtered out programmatically.
    """
    context = load_tool_execution_context(DEFAULT_TOOL_EXECUTION_CONTEXT_PATH)
    otlp_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    if context is None or not context.trace_id or not context.span_id or not otlp_endpoint:
        logger.debug(
            "skipping screenshot span emit: context=%s endpoint=%s",
            context is not None,
            bool(otlp_endpoint),
        )
        return

    import hashlib

    from opentelemetry import trace

    from plato.otel import init_tracing

    # Derive a stable synthetic step id from the tool_use_id. Picks a value
    # in the 1e8 – 1e9 range so it's unlikely to collide with the agent's
    # natural step counter (which starts at 1).
    synthetic_step_id = int(hashlib.md5(tool_use_id.encode("utf-8")).hexdigest()[:8], 16) | 0x40000000

    service_name = context.agent_name or "plato-agent"
    init_tracing(
        service_name=service_name,
        session_id=context.session_id,
        otlp_endpoint=otlp_endpoint,
        parent_trace_id=context.trace_id,
        parent_span_id=context.span_id,
    )
    tracer = trace.get_tracer(service_name)
    with tracer.start_as_current_span(f"atif.step.{synthetic_step_id}") as span:
        # Standard atif step attrs — viewer renders these as a system step.
        span.set_attribute("atif.step.id", synthetic_step_id)
        span.set_attribute("atif.step.source", "system")
        span.set_attribute("atif.step.message", f"browser screenshot ({session})")
        span.set_attribute("atif.step.screenshot", b64)
        span.set_attribute("atif.step.screenshot_format", mime)
        # Discriminator: marks this as a harness-injected screenshot span so
        # consumers can filter it out from "real" agent steps.
        span.set_attribute("plato.harness.span_kind", "browser_screenshot")
        # Cross-reference attrs for downstream programmatic use.
        span.set_attribute("plato.browser_screenshot.session", session)
        span.set_attribute("plato.browser_screenshot.tool_use_id", tool_use_id)
        span.set_attribute("plato.browser_screenshot.tool_name", tool_name)


def _handle_claude_posttool_screenshot(payload: dict[str, object]) -> None:
    tool_name = str(payload.get("tool_name") or "")
    if tool_name != "Bash":
        return
    tool_input_raw = payload.get("tool_input")
    if not isinstance(tool_input_raw, dict):
        return
    tool_input: dict[str, object] = tool_input_raw  # type: ignore[assignment]
    command = tool_input.get("command")
    if not isinstance(command, str):
        return
    session = _parse_browser_session(command)
    if not session:
        return
    tool_use_id = str(payload.get("tool_use_id") or "")
    if not tool_use_id:
        return

    captured = _capture_post_tool_screenshot(session=session, tool_use_id=tool_use_id)
    if captured is None:
        return
    data, mime = captured
    b64 = base64.b64encode(data).decode()
    _emit_screenshot_span(
        tool_use_id=tool_use_id,
        session=session,
        tool_name=tool_name,
        b64=b64,
        mime=mime,
    )


def main(argv: list[str] | None = None) -> int:
    """Record pre-tool sidecar data for agent CLIs."""
    parser = argparse.ArgumentParser(description="Record pre-tool execution hook data")
    parser.add_argument(
        "mode",
        choices=(
            "claude-pretooluse",
            "claude-posttool-screenshot",
            "codex-posttool-screenshot",
            "gemini-beforetool",
            "codex-pretooluse",
        ),
    )
    args = parser.parse_args(argv)

    raw_payload = sys.stdin.read()
    if not raw_payload.strip():
        return 0

    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError:
        logger.warning("Failed to parse pre-tool hook payload: %s", raw_payload[:200])
        return 0

    if args.mode in ("claude-posttool-screenshot", "codex-posttool-screenshot"):
        # Both agents' PostToolUse payloads share the fields we need:
        # tool_name, tool_use_id, tool_input.command. The handler is shared.
        try:
            _handle_claude_posttool_screenshot(payload)
        except Exception as exc:
            logger.debug("posttool-screenshot hook failed: %s", exc)
        return 0

    _write_record(args.mode, payload)

    if args.mode == "gemini-beforetool":
        sys.stdout.write("{}\n")
    elif args.mode == "codex-pretooluse":
        sys.stdout.write(json.dumps({"decision": "approve"}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
