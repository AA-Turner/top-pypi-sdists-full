"""
cvc.integrations.channels._display — Display helpers for channel adapters.

Ported from Hermes's ``cvc.agent._vendor.hermes.agent.display`` (v2026.07)
into a CVC-native module so channel adapters (Telegram, Slack, Discord, …)
can render tool cards with the same emoji map and one-line preview
generation Hermes uses.

Why a separate module:
    The original CVC telegram adapter had inline ``_format_tool_card_start``
    / ``_format_tool_card_done`` methods with a minimal emoji map. Hermes's
    version is much richer (per-tool emoji + verb + path preview). Porting
    it here lets every channel share the same visible UX without bloating
    the per-channel adapter.

This module is intentionally self-contained: no imports from the Hermes
vendored tree, no cvc.gateway.* deps. Just pure helpers that take a
tool_name + args dict and return strings/numbers for card rendering.

Exports (Hermes parity):
    get_tool_emoji(tool_name)           -> "🔍" / "📄" / "⚡" / "⚙️"
    build_tool_preview(tool_name, args) -> "search \"class AIAgent\""
    get_cute_tool_message(...)          -> "| 🔍 search   ...  0.4s"

v3.5.2 — ported from Hermes agent/display.py.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional


# =========================================================================
# Tool emoji map
# =========================================================================
#
# Hermes resolution order:
#   1. Active skin overrides
#   2. Tool registry per-tool emoji
#   3. CVC native fallback map (below)
#   4. Default "⚡"
#
# We skip the registry step (CVC channels don't read the tool registry
# directly) and inline the fallback map verbatim. The map covers every
# CVC-native tool that ships today.
_CVC_TOOL_EMOJI: Dict[str, str] = {
    # File operations
    "read_file":     "📄",
    "write_file":    "✏️",
    "edit_file":     "🔧",
    "patch":         "🩹",
    "patch_file":    "🩹",
    # Shell
    "terminal":      "⚡",
    "bash":          "⚡",
    "process":       "⚙️",
    # Search & discovery
    "search_files":  "🔍",
    "grep":          "🔍",
    "glob":          "📂",
    "list_dir":      "📁",
    # Web
    "web_search":    "🌐",
    "web_extract":   "📄",
    # CVC time-machine
    "cvc_status":    "📊",
    "cvc_log":       "📜",
    "cvc_commit":    "💾",
    "cvc_branch":    "🌿",
    "cvc_restore":   "⏪",
    "cvc_merge":     "🔀",
    "cvc_search":    "🔮",
    "cvc_diff":      "📐",
    # Documents
    "cvc_ingest_document":  "📚",
    "cvc_document_search": "📖",
    "cvc_list_documents":  "📋",
    # Browser (Hermes parity — channels may surface browser tools)
    "browser_navigate": "🌐",
    "browser_snapshot": "📸",
    "browser_click":    "👆",
    "browser_type":     "⌨️",
    "browser_scroll":   "↕️",
    "browser_back":     "◀️",
    "browser_press":    "⌨️",
    "browser_get_images": "🖼️",
    "browser_vision":   "👁️",
    # Misc
    "image_generate":  "🎨",
    "text_to_speech":  "🔊",
    "vision_analyze":  "👁️",
    "skill_view":      "📘",
    "skills_list":     "📚",
    "skill_manage":    "🛠️",
    "cronjob":         "⏰",
    "execute_code":    "🐍",
    "delegate_task":   "🪆",
    "clarify":         "❓",
    "todo":            "✅",
    "memory":          "🧠",
    "send_message":    "✉️",
    "session_search":  "🔎",
}


def get_tool_emoji(tool_name: str, default: str = "⚡") -> str:
    """Return the display emoji for a tool name. Hermes parity."""
    if not tool_name:
        return default
    return _CVC_TOOL_EMOJI.get(tool_name, default)


# =========================================================================
# Tool preview — one-line summary of a tool call's primary argument
# =========================================================================
#
# Hermes pattern: identify the "primary" arg by tool name, fall back to
# a generic key scan (query/text/command/path/...). Truncate to a max
# length so cards stay readable.

_TOOL_PREVIEW_MAX = 60  # chars — Hermes uses global _tool_preview_max_len
_PRIMARY_ARG_BY_TOOL: Dict[str, str] = {
    "terminal": "command",
    "web_search": "query",
    "web_extract": "urls",
    "read_file": "path",
    "write_file": "path",
    "patch": "path",
    "search_files": "pattern",
    "browser_navigate": "url",
    "browser_click": "ref",
    "browser_type": "text",
    "image_generate": "prompt",
    "text_to_speech": "text",
    "vision_analyze": "question",
    "mixture_of_agents": "user_prompt",
    "skill_view": "name",
    "skills_list": "category",
    "cronjob": "action",
    "execute_code": "code",
    "delegate_task": "goal",
    "clarify": "question",
    "skill_manage": "name",
}


def _oneline(text: str) -> str:
    """Collapse whitespace to a single space and strip."""
    return " ".join(str(text or "").split())


def _truncate(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    return s[: max(0, n - 3)] + "..."


def _delegate_task_goal_parts(tasks: Any, *, per_goal_len: int) -> tuple[int, list[str]]:
    """Extract (count, [goals]) from a delegate_task ``tasks`` arg."""
    if not isinstance(tasks, list):
        return 0, []
    goals: list[str] = []
    for t in tasks:
        if isinstance(t, dict):
            g = t.get("goal") or t.get("context") or ""
        else:
            g = str(t)
        g = _oneline(g)
        if g:
            goals.append(_truncate(g, per_goal_len))
    return len(tasks), goals


def build_tool_preview(
    tool_name: str,
    args: dict,
    max_len: int = _TOOL_PREVIEW_MAX,
) -> Optional[str]:
    """One-line preview of a tool call's primary argument. Hermes parity.

    Returns ``None`` if no meaningful preview can be built.
    """
    if not args:
        return None

    # delegate_task: special-case the multi-task form
    if tool_name == "delegate_task":
        tasks = args.get("tasks")
        if tasks and isinstance(tasks, list):
            count, goals = _delegate_task_goal_parts(tasks, per_goal_len=40)
            if goals:
                preview = f"{count} tasks: " + " | ".join(goals)
            else:
                preview = f"{count} parallel tasks"
            return _truncate(preview, max_len)
        goal = args.get("goal", "")
        if not goal:
            return None
        return _truncate(_oneline(str(goal)), max_len)

    # process: action + session_id + data preview
    if tool_name == "process":
        action = args.get("action", "")
        sid = args.get("session_id", "")
        data = args.get("data", "")
        timeout_val = args.get("timeout")
        parts = [action] if action else []
        if sid:
            parts.append(str(sid)[:16])
        if data:
            parts.append(f'"{_oneline(str(data)[:20])}"')
        if timeout_val and action == "wait":
            parts.append(f"{timeout_val}s")
        return " ".join(parts) if parts else None

    # todo: distinguishes plan vs update
    if tool_name == "todo":
        todos_arg = args.get("todos")
        merge = args.get("merge", False)
        if todos_arg is None:
            return "reading task list"
        if merge:
            return f"updating {len(todos_arg)} task(s)"
        return f"planning {len(todos_arg)} task(s)"

    # session_search: short query preview
    if tool_name == "session_search":
        query = _oneline(args.get("query", ""))
        if not query:
            return None
        return f'recall: "{_truncate(query, 25)}"'

    # memory: action + target + (old or new) content preview
    if tool_name == "memory":
        action = args.get("action", "")
        target = args.get("target", "")
        if action == "add":
            content = _oneline(args.get("content", ""))
            return f'+{target}: "{_truncate(content, 25)}"'
        if action in ("replace", "remove"):
            old = _oneline(args.get("old_text") or "") or "<missing old_text>"
            return f'~{target}: "{_truncate(old, 20)}"'
        return action or None

    # send_message: target + short message
    if tool_name == "send_message":
        target = args.get("target", "?")
        msg = _oneline(args.get("message", ""))
        return f'to {target}: "{_truncate(msg, 20)}"'

    # Generic: pick the primary arg key for this tool, fall back to common keys
    key = _PRIMARY_ARG_BY_TOOL.get(tool_name)
    if not key:
        for fallback_key in ("query", "text", "command", "path", "name",
                             "prompt", "code", "goal"):
            if fallback_key in args:
                key = fallback_key
                break

    if not key or key not in args:
        return None

    value = args[key]
    if isinstance(value, list):
        value = value[0] if value else ""

    preview = _oneline(str(value))
    if not preview:
        return None
    return _truncate(preview, max_len)


# =========================================================================
# Cute tool completion line — Hermes format
# =========================================================================
#
# Format: | {emoji} {verb:9} {detail}  {duration}
# This is what gets rendered in Telegram cards' edit-from-tool_start to
# tool_result transition, and what shows in the streamed text after a
# tool call so the user sees "✓ search_files done in 120ms" mid-stream.

def get_cute_tool_message(
    tool_name: str,
    args: dict,
    duration: float,
    result: Optional[str] = None,
) -> str:
    """Hermes-parity formatted tool completion line."""
    emoji = get_tool_emoji(tool_name, default="⚡")
    dur = f"{duration:.1f}s"

    def _trunc(s: Any, n: int = 40) -> str:
        s = str(s)
        return _truncate(s, n) if len(s) > n else s

    def _path(p: Any, n: int = 35) -> str:
        p = str(p)
        if len(p) <= n:
            return p
        return "..." + p[-(n - 3):]

    if tool_name == "web_search":
        return f"| {emoji} search    {_trunc(args.get('query', ''), 42)}  {dur}"
    if tool_name == "web_extract":
        urls = args.get("urls", [])
        if urls:
            url = urls[0] if isinstance(urls, list) else str(urls)
            domain = (str(url).replace("https://", "")
                      .replace("http://", "").split("/")[0])
            extra = f" +{len(urls) - 1}" if len(urls) > 1 else ""
            return f"| {emoji} fetch     {_trunc(domain, 35)}{extra}  {dur}"
        return f"| {emoji} fetch     pages  {dur}"
    if tool_name == "terminal":
        return f"| 💻 $         {_trunc(args.get('command', ''), 42)}  {dur}"
    if tool_name == "process":
        action = args.get("action", "?")
        sid = str(args.get("session_id", ""))[:12]
        labels = {
            "list": "ls processes", "poll": f"poll {sid}", "log": f"log {sid}",
            "wait": f"wait {sid}", "kill": f"kill {sid}", "write": f"write {sid}",
            "submit": f"submit {sid}",
        }
        return f"| ⚙️ proc      {labels.get(action, f'{action} {sid}')}  {dur}"
    if tool_name == "read_file":
        return f"| {emoji} read      {_path(args.get('path', ''))}  {dur}"
    if tool_name == "write_file":
        return f"| ✍️ write     {_path(args.get('path', ''))}  {dur}"
    if tool_name == "patch":
        return f"| {emoji} patch     {_path(args.get('path', ''))}  {dur}"
    if tool_name == "search_files":
        pattern = _trunc(args.get("pattern", ""), 35)
        target = args.get("target", "content")
        verb = "find" if target == "files" else "grep"
        return f"| 🔎 {verb:9} {pattern}  {dur}"
    if tool_name == "browser_navigate":
        url = args.get("url", "")
        domain = (str(url).replace("https://", "")
                  .replace("http://", "").split("/")[0])
        return f"| 🌐 navigate  {_trunc(domain, 35)}  {dur}"
    if tool_name == "browser_snapshot":
        mode = "full" if args.get("full") else "compact"
        return f"| 📸 snapshot  {mode}  {dur}"
    if tool_name == "browser_click":
        return f"| 👆 click     {args.get('ref', '?')}  {dur}"
    if tool_name == "browser_type":
        return f"| ⌨️ type      \"{_trunc(args.get('text', ''), 30)}\"  {dur}"
    if tool_name == "browser_scroll":
        d = args.get("direction", "down")
        arrow = {"down": "↓", "up": "↑", "right": "→", "left": "←"}.get(d, "↓")
        return f"| {arrow}  scroll    {d}  {dur}"
    if tool_name == "browser_back":
        return f"| ◀️ back      {dur}"
    if tool_name == "browser_press":
        return f"| ⌨️ press     {args.get('key', '?')}  {dur}"
    if tool_name == "browser_get_images":
        return f"| 🖼️ images    extracting  {dur}"
    if tool_name == "browser_vision":
        return f"| 👁️ vision    analyzing page  {dur}"

    # Generic fallback: emoji + name + preview
    preview = build_tool_preview(tool_name, args, max_len=42) or ""
    return f"| {emoji} {tool_name:9} {preview}  {dur}"


# =========================================================================
# Adaptive text-batch delay (Hermes parity)
# =========================================================================
#
# The bottleneck for "feels instant" is the ingress side — when the user
# sends a short Telegram message, the adapter should not wait long
# before flushing it to the agent. Hermes's tiers:
#
#   last chunk ≥ 4000 cp   → 1.0s (continuation almost certain)
#   total ≤ 320 cp         → min(0.3s, 0.18s)  — short, near-instant
#   total ≤ 1024 cp        → min(0.3s, 0.24s)  — medium
#   otherwise              → 0.3s (operator cap)
#
# These come from Hermes's _calc_text_batch_delay. We expose them as a
# pure function so the CVC adapter (and any future channel) can call
# them without re-implementing the tier logic.

_TEXT_BATCH_FAST_LEN = 320
_TEXT_BATCH_FAST_DELAY_S = 0.18
_TEXT_BATCH_SHORT_LEN = 1024
_TEXT_BATCH_SHORT_DELAY_S = 0.24
_TEXT_BATCH_SPLIT_THRESHOLD = 4000
_DEFAULT_TEXT_BATCH_DELAY_S = 0.3


def calc_text_batch_delay(
    total_chars: int,
    last_chunk_chars: int,
    *,
    default_delay_s: float = _DEFAULT_TEXT_BATCH_DELAY_S,
) -> float:
    """Adaptive delay (seconds) before flushing a text batch to the agent.

    Hermes-parity tier logic. Operators can override the cap via
    ``default_delay_s`` (e.g. set 0.10 to make every tier faster).
    """
    if last_chunk_chars >= _TEXT_BATCH_SPLIT_THRESHOLD:
        # Continuation almost certain → wait the split delay
        return 1.0
    if total_chars <= _TEXT_BATCH_FAST_LEN:
        return min(default_delay_s, _TEXT_BATCH_FAST_DELAY_S)
    if total_chars <= _TEXT_BATCH_SHORT_LEN:
        return min(default_delay_s, _TEXT_BATCH_SHORT_DELAY_S)
    return default_delay_s