"""
Chat capture — wire the event spine into chat endpoints.

Wraps the agent loop and emits events:

    chat.session_start      when the turn begins (also captures user message)
    chat.tool_call          on tool_start
    chat.tool_result        on tool_result (with duration_ms)
    chat.assistant_message  on done (with total tokens + duration)
    chat.error              on exception
    chat.session_end        when the stream finishes

All captures are best-effort — they never raise to the caller. Capture
happens in the asyncio loop's thread (not the agent thread) to avoid
contention with the agent's I/O.

Usage from gateway/chat.py::

    from cvc.events.chat_capture import ChatCapture

    cap = ChatCapture(
        workspace=workspace_path,
        channel="web",          # or "telegram", "tui", etc.
        actor="Jai",
        session_id=session_id,
        turn_id=turn_id,
    )
    cap.session_start(user_message=user_message, model=model, provider=provider)

    # inside the SSE loop:
    async for event in stream:
        if event["type"] == "tool_start":
            cap.tool_call(name=event["name"], call_id=event["call_id"], args=event.get("args"))
        elif event["type"] == "tool_result":
            cap.tool_result(name=event["name"], call_id=event["call_id"], output=event.get("output"))
        elif event["type"] == "done":
            cap.assistant_message(text=event["content"], tokens_in=..., tokens_out=...)
        elif event["type"] == "error":
            cap.error(message=event["message"])
        yield event

    cap.session_end()
"""
from __future__ import annotations

import logging
import time
from typing import Any

from cvc.events.spine import capture

logger = logging.getLogger("cvc.events.chat_capture")


class ChatCapture:
    """Per-turn event capture. Stateful but cheap — all data on the instance."""

    def __init__(
        self,
        *,
        workspace: str | None,
        channel: str = "web",
        actor: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        branch: str | None = None,
    ) -> None:
        self.workspace = workspace
        self.channel = channel
        self.actor = actor
        self.session_id = session_id
        self.turn_id = turn_id
        self.provider = provider
        self.model = model
        self.branch = branch
        self._start = time.time()
        self._tool_started: dict[str, float] = {}
        self._last_assistant_id: str | None = None
        # Build event parents so tool events chain to the user message,
        # assistant_message chains to the last tool_result, etc.
        self._parent_id: str | None = None

    # ── Lifecycle ────────────────────────────────────────────

    def session_start(
        self,
        *,
        user_message: str,
        model: str | None = None,
        provider: str | None = None,
    ) -> None:
        """Capture the start of a chat turn + the user message itself."""
        if model:
            self.model = model
        if provider:
            self.provider = provider

        # Session start
        self._parent_id = capture(
            kind="chat.session_start",
            workspace=self.workspace,
            channel=self.channel,
            actor=self.actor,
            summary=f"session {self.session_id or '?'} started",
            session_id=self.session_id,
            provider=self.provider,
            model=self.model,
            branch=self.branch,
            channel_detail=f"turn:{self.turn_id}" if self.turn_id else None,
        )
        # User message
        if user_message:
            capture(
                kind="chat.user_message",
                workspace=self.workspace,
                channel=self.channel,
                actor=self.actor,
                summary=user_message,
                data={"text_length": len(user_message)},
                session_id=self.session_id,
                provider=self.provider,
                model=self.model,
                branch=self.branch,
                parent_event_id=self._parent_id,
                channel_detail=f"turn:{self.turn_id}" if self.turn_id else None,
            )

    def session_end(self, *, status: str = "ok") -> None:
        """Capture the end of a chat turn."""
        duration_ms = int((time.time() - self._start) * 1000)
        capture(
            kind="chat.session_end",
            workspace=self.workspace,
            channel=self.channel,
            actor=self.actor,
            summary=f"turn finished ({status})",
            session_id=self.session_id,
            provider=self.provider,
            model=self.model,
            branch=self.branch,
            duration_ms=duration_ms,
            status=status,
            parent_event_id=self._parent_id,
            channel_detail=f"turn:{self.turn_id}" if self.turn_id else None,
        )

    # ── Per-event ────────────────────────────────────────────

    def tool_call(
        self,
        *,
        name: str,
        call_id: str,
        args: dict[str, Any] | None = None,
    ) -> None:
        self._tool_started[call_id] = time.time()
        # Compact args — large payloads bloat the spine
        compact_args: dict[str, Any] = {}
        if args:
            for k, v in list(args.items())[:6]:
                s = str(v)
                compact_args[k] = s if len(s) <= 200 else s[:197] + "..."
        capture(
            kind="chat.tool_call",
            workspace=self.workspace,
            channel=self.channel,
            actor=self.actor,
            summary=f"{name}({', '.join(list(compact_args.keys())[:3])})",
            data={"name": name, "call_id": call_id, "args": compact_args},
            session_id=self.session_id,
            provider=self.provider,
            model=self.model,
            branch=self.branch,
            parent_event_id=self._parent_id,
            channel_detail=f"turn:{self.turn_id}" if self.turn_id else None,
        )

    def tool_result(
        self,
        *,
        name: str,
        call_id: str,
        output: str | None = None,
        status: str = "ok",
        error: str | None = None,
    ) -> None:
        started_at = self._tool_started.pop(call_id, None)
        duration_ms = int((time.time() - started_at) * 1000) if started_at else 0
        # Compact output
        compact_output: str | None = None
        if output is not None:
            compact_output = output if len(output) <= 500 else output[:497] + "..."
        capture(
            kind="chat.tool_result",
            workspace=self.workspace,
            channel=self.channel,
            actor=self.actor,
            summary=f"{name} → {status}",
            data={
                "name": name,
                "call_id": call_id,
                "output": compact_output,
            },
            session_id=self.session_id,
            provider=self.provider,
            model=self.model,
            branch=self.branch,
            parent_event_id=self._parent_id,
            duration_ms=duration_ms,
            status=status,
            error=error,
            channel_detail=f"turn:{self.turn_id}" if self.turn_id else None,
        )

    def assistant_message(
        self,
        *,
        text: str,
        tokens_in: int = 0,
        tokens_out: int = 0,
        status: str = "ok",
        error: str | None = None,
    ) -> None:
        duration_ms = int((time.time() - self._start) * 1000)
        # Compact text — full text can be huge
        summary_text = text if len(text) <= 200 else text[:197] + "..."
        self._last_assistant_id = capture(
            kind="chat.assistant_message",
            workspace=self.workspace,
            channel=self.channel,
            actor="assistant",
            summary=summary_text,
            data={"text_length": len(text)},
            session_id=self.session_id,
            provider=self.provider,
            model=self.model,
            branch=self.branch,
            parent_event_id=self._parent_id,
            duration_ms=duration_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            status=status,
            error=error,
            channel_detail=f"turn:{self.turn_id}" if self.turn_id else None,
        )

    def error(self, *, message: str) -> None:
        capture(
            kind="chat.error",
            workspace=self.workspace,
            channel=self.channel,
            actor=self.actor,
            summary=message[:200],
            data={"message": message},
            session_id=self.session_id,
            provider=self.provider,
            model=self.model,
            branch=self.branch,
            parent_event_id=self._parent_id,
            status="err",
            error=message,
            channel_detail=f"turn:{self.turn_id}" if self.turn_id else None,
        )

    # ── Context-manager style (optional) ─────────────────────

    def __enter__(self) -> "ChatCapture":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_val is not None:
            self.error(message=f"{exc_type.__name__}: {exc_val}")
            self.session_end(status="err")
        else:
            self.session_end(status="ok")