"""Context Manager — append-only history with auto-compaction.

Like Claude Code CLI: history grows, auto-compacts when approaching limits.
No external mutation. Thread-safe compaction.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field


@dataclass
class Message:
    role: str
    content: str
    tool_call_id: str | None = None
    tool_calls: list | None = None
    name: str | None = None


class ContextManager:
    """Manages conversation history with auto-compaction."""

    def __init__(self, system_prompt: str, use_native_tool_messages: bool = True):
        self._system = Message(role="system", content=system_prompt)
        self._messages: list[Message] = []
        self._compaction_threshold = 25
        self._token_threshold = 60_000
        self._compaction_summary: str | None = None
        self._compaction_lock = threading.Lock()
        self._compacting = False
        self._use_native_tool_messages = use_native_tool_messages

    @property
    def message_count(self) -> int:
        return len(self._messages)

    def append_user(self, text: str) -> None:
        self._messages.append(Message(role="user", content=text))

    def append_assistant(self, text: str, tool_calls: list | None = None) -> None:
        self._messages.append(Message(role="assistant", content=text, tool_calls=tool_calls))

    def append_tool_result(self, tool_call_id: str, name: str, content: str) -> None:
        self._messages.append(Message(
            role="tool",
            content=content,
            tool_call_id=tool_call_id,
            name=name,
        ))

    def append_nudge(self, lang: str = "en") -> None:
        nudges = {
            "ko": "⚠️ 도구를 호출하지 않으면 세션이 종료됩니다. bash_exec/http_request를 즉시 호출하거나, 발견 내용을 보고하세요.",
            "zh": "⚠️ 必须调用工具，否则会话将结束。立即调用 bash_exec/http_request，或报告已发现的内容。",
            "en": "⚠️ You MUST call a tool or the session ends. Call bash_exec/http_request NOW, or report your findings.",
        }
        self._messages.append(Message(role="user", content=nudges.get(lang, nudges["en"])))

    def build_messages(self) -> list[Message]:
        self._apply_compaction_if_ready()
        return [self._system] + list(self._messages)

    def needs_compaction(self) -> bool:
        if self._compacting:
            return False
        est_tokens = sum(len(m.content) for m in self._messages) // 4
        return len(self._messages) > self._compaction_threshold or est_tokens > self._token_threshold

    def set_compaction_summary(self, summary: str) -> None:
        with self._compaction_lock:
            self._compaction_summary = summary
            self._compacting = False

    def mark_compacting(self) -> list[Message]:
        self._compacting = True
        keep_recent = 8
        to_compact = self._messages[:-keep_recent] if len(self._messages) > keep_recent else []
        return to_compact

    def _apply_compaction_if_ready(self) -> None:
        with self._compaction_lock:
            if self._compaction_summary is None:
                return
            summary = self._compaction_summary
            self._compaction_summary = None

        keep_recent = 8
        recent = self._messages[-keep_recent:] if len(self._messages) > keep_recent else list(self._messages)
        # Trim orphaned tool messages from the head of the slice.
        # When compaction discards the paired assistant(tool_calls) message,
        # the tool result at the start of `recent` has no preceding tool_calls —
        # DeepSeek and other providers reject this with a 400 error.
        while recent and recent[0].role == "tool":
            recent.pop(0)
        compact_msg = Message(role="user", content=f"[CONTEXT SUMMARY]\n{summary}")
        self._messages = [compact_msg] + recent
