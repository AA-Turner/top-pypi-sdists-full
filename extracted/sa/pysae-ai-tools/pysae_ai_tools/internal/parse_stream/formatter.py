"""Format Claude Code stream-json events into readable CI logs.

Pure formatting functions — no I/O, fully testable.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Any

# ─── Constants ────────────────────────────────────────────────────────────────

SEPARATOR = "════════════════════════════════════════════════════════════"
THIN_SEPARATOR = "────────────────────────────────────────────────────────────"

MAX_CONTENT_CHARS = 500
MAX_CONTENT_LINES = 20
TAIL_LINES = 5

PREFIX_TEXT = "◇ "
PREFIX_TOOL_CALL = "▸ "
PREFIX_OK = "✓ "
PREFIX_ERR = "✗ "
INDENT = "  "


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _indent_multiline(text: str, prefix: str) -> str:
    """Prefix the first line, indent subsequent lines."""
    lines = text.split("\n")
    if len(lines) <= 1:
        return f"{prefix}{text}\n"
    first = f"{prefix}{lines[0]}\n"
    rest = "\n".join(f"{INDENT}{line}" for line in lines[1:])
    return f"{first}{rest}\n"


def _truncate_multiline(text: str, prefix: str) -> str:
    """Prefix + truncate with head/tail preservation for multiline content."""
    lines = text.split("\n")
    is_long_chars = len(text) > MAX_CONTENT_CHARS
    is_long_lines = len(lines) > MAX_CONTENT_LINES
    truncated = is_long_chars or is_long_lines

    if not truncated:
        return _indent_multiline(text, prefix)

    # Single-line: cut at MAX_CONTENT_CHARS
    if len(lines) <= 1:
        return f"{prefix}{text[:MAX_CONTENT_CHARS]} ... (truncated)\n"

    # Multi-line: head + ... + last TAIL_LINES
    total = len(lines)
    head_count = max(total - 15, 1)
    head = lines[:head_count]
    tail = lines[-TAIL_LINES:]
    skipped = total - head_count - TAIL_LINES

    parts: list[str] = []
    parts.append(f"{prefix}{head[0]}\n")
    if len(head) > 1:
        parts.append("\n".join(f"{INDENT}{line}" for line in head[1:]) + "\n")
    parts.append(f"{INDENT}... ({skipped} lines truncated)\n")
    parts.append("\n".join(f"{INDENT}{line}" for line in tail) + "\n")
    return "".join(parts)


def _tool_call_summary(name: str, input_data: dict[str, Any]) -> str:
    """One-line summary for a tool call."""
    detail = ""
    if "command" in input_data:
        detail = f": {str(input_data['command'])[:120]}"
    elif "pattern" in input_data:
        detail = f": {input_data['pattern']}"
    elif "file_path" in input_data:
        detail = f": {input_data['file_path']}"
    elif "skill" in input_data:
        detail = f": {input_data['skill']}"
    elif "prompt" in input_data:
        detail = f": {str(input_data['prompt'])[:80]}"
    return f"{PREFIX_TOOL_CALL}{name}{detail}\n"


def _format_tokens(total: int) -> str:
    """Format token count with k/M suffix."""
    if total >= 1_000_000:
        return f"{total / 1_000_000:.1f}M"
    if total >= 1_000:
        return f"{total / 1_000:.1f}k"
    return str(total)


# ─── Stateful formatter ──────────────────────────────────────────────────────


@dataclass
class StreamFormatter:
    """Stateful formatter for Claude Code stream-json events.

    Tracks whether we are inside a streaming text block to correctly
    prefix and indent streamed text deltas.
    """

    skip_assistant_text: bool = False
    _streaming: bool = field(default=False, init=False, repr=False)
    _stream_line_started: bool = field(default=False, init=False, repr=False)
    _had_action: bool = field(default=False, init=False, repr=False)
    tool_call_count: int = field(default=0, init=False, repr=False)
    num_turns: int = field(default=0, init=False, repr=False)
    is_error: bool = field(default=False, init=False, repr=False)
    response_chunks: list[str] = field(default_factory=list, init=False, repr=False)

    def format_event(self, event: dict[str, Any]) -> str:
        """Format a single stream-json event. Returns empty string to skip."""
        event_type = event.get("type")

        if event_type == "system":
            return self._format_system(event)
        if event_type == "assistant":
            return self._format_assistant(event)
        if event_type == "user":
            return self._format_user(event)
        if event_type == "stream_event":
            return self._format_stream_delta(event)
        if event_type == "rate_limit_event":
            return self._format_rate_limit(event)
        if event_type == "result":
            return self._format_result(event)
        # Show unhandled events as JSON so errors are never silently swallowed
        return f"[{event_type}] {json.dumps(event, default=str)}\n"

    # ── Event handlers ────────────────────────────────────────────────────

    def _format_system(self, event: dict[str, Any]) -> str:
        subtype = event.get("subtype", "unknown")
        if subtype == "status":
            # Transient harness state (e.g. status="requesting") — not log-worthy.
            return ""
        if subtype == "init":
            tools = event.get("tools") or []
            mcp_servers = event.get("mcp_servers") or []
            connected = [s["name"] for s in mcp_servers if isinstance(s, dict) and s.get("status") == "connected"]
            skills = event.get("skills") or []
            return (
                "=== Claude session ===\n"
                f"Model: {event.get('model', 'unknown')}\n"
                f"Tools: {len(tools)}\n"
                f"MCP servers: {', '.join(connected)}\n"
                f"Skills: {', '.join(skills)}\n"
                f"{THIN_SEPARATOR}\n\n"
            )
        # Other system events
        msg = event.get("message") or event.get("error") or event.get("reason") or json.dumps(event)
        return f"[SYSTEM:{subtype}] {msg}\n"

    def _format_assistant(self, event: dict[str, Any]) -> str:
        message = event.get("message") or {}
        contents: list[dict[str, Any]] = message.get("content") or []
        parts: list[str] = [self._end_streaming()]
        for block in contents:
            if block.get("type") == "text":
                text = str(block.get("text", ""))
                if not self.skip_assistant_text:
                    self.response_chunks.append(text)
                    parts.append(self._action_sep())
                    parts.append(_indent_multiline(text, PREFIX_TEXT))
            elif block.get("type") == "tool_use":
                self.tool_call_count += 1
                parts.append(self._action_sep())
                parts.append(_tool_call_summary(str(block.get("name", "")), block.get("input") or {}))
        return "".join(parts)

    def _format_user(self, event: dict[str, Any]) -> str:
        message = event.get("message") or {}
        contents: list[dict[str, Any]] = message.get("content") or []
        parts: list[str] = [self._end_streaming()]
        for block in contents:
            if block.get("type") == "tool_result":
                is_error = bool(block.get("is_error"))
                prefix = PREFIX_ERR if is_error else PREFIX_OK
                content = str(block.get("content") or "")
                content = re.sub(r"\[result-id: \w+\]\s*", "", content).strip()
                if not content:
                    continue
                parts.append(_truncate_multiline(content, prefix))
        return "".join(parts)

    def _format_stream_delta(self, event: dict[str, Any]) -> str:
        inner = event.get("event") or {}
        if not isinstance(inner, dict):
            return ""
        if inner.get("type") != "content_block_delta":
            return ""
        delta = inner.get("delta") or {}
        if not isinstance(delta, dict):
            return ""
        if delta.get("type") != "text_delta":
            return ""

        text = str(delta.get("text", ""))
        if not text:
            return ""

        self.response_chunks.append(text)
        parts: list[str] = []
        for ch in text:
            if ch == "\n":
                parts.append(f"\n{INDENT}")
                self._stream_line_started = False
            else:
                if not self._streaming or not self._stream_line_started:
                    if not self._streaming:
                        parts.append(self._action_sep())
                        parts.append(PREFIX_TEXT)
                        self._streaming = True
                    self._stream_line_started = True
                parts.append(ch)
        return "".join(parts)

    def _format_rate_limit(self, event: dict[str, Any]) -> str:
        info = event.get("rate_limit_info") or {}
        if not isinstance(info, dict):
            return ""
        status = info.get("status", "")
        if status in ("allowed", "allowed_warning", "throttled"):
            return ""
        # "rejected" = hard block (no credits, plan limit reached)
        self.is_error = True
        return (
            f"\u26a0 [RATE LIMIT] {status} "
            f"— {info.get('rateLimitType', 'unknown')}, "
            f"resets at {info.get('resetsAt', '?')}\n"
        )

    def _format_result(self, event: dict[str, Any]) -> str:
        closing = self._end_streaming()
        is_error = bool(event.get("is_error", False))
        self.is_error = self.is_error or is_error
        status = "FAILED ✗" if is_error else "SUCCESS ✓"
        cost = round(float(event.get("total_cost_usd") or 0), 4)
        duration_ms = event.get("duration_ms") or 0
        duration_s = float(str(duration_ms)) / 1000
        if duration_s >= 60:
            duration_str = f"{int(duration_s // 60)}m {int(duration_s % 60)}s"
        else:
            duration_str = f"{int(round(duration_s))}s"
        turns = event.get("num_turns") or 0
        self.num_turns = int(str(turns))
        usage = event.get("usage") or {}
        input_tokens = int(usage.get("input_tokens") or 0)
        output_tokens = int(usage.get("output_tokens") or 0)
        cache_read = int(usage.get("cache_read_input_tokens") or 0)
        cache_create = int(usage.get("cache_creation_input_tokens") or 0)
        total_tokens = input_tokens + output_tokens + cache_read + cache_create
        tokens_str = _format_tokens(total_tokens)
        return (
            f"{closing}\n{SEPARATOR}\n"
            f"Result: {status}\n"
            f"Cost: ${cost} · Duration: {duration_str} · Turns: {turns} · Tokens: {tokens_str}\n"
            f"{SEPARATOR}\n"
        )

    # ── Internal ──────────────────────────────────────────────────────────

    def _action_sep(self) -> str:
        """Return a blank line separator between actions (skip before first)."""
        if self._had_action:
            return "\n"
        self._had_action = True
        return ""

    def _end_streaming(self) -> str:
        """Close an active streaming text block."""
        if self._streaming:
            self._streaming = False
            self._stream_line_started = False
            return "\n"
        return ""
