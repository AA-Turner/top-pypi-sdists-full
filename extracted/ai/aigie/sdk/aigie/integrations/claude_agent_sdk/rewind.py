"""Claude Agent SDK rewind support via fork-and-steer."""

from __future__ import annotations

import dataclasses
import json
import logging
from dataclasses import dataclass
from typing import Any

from aigie.rewind.protocol import Corrective, RewindHandle, RewindOutcome, ToolCallOverride

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ClaudeForkPoint:
    client: Any
    session_id: str
    options: Any = None


def _extract_session_id(message: Any) -> str | None:
    """Extract a session id from SDK messages."""
    sid = getattr(message, "session_id", None)
    if sid:
        return str(sid)
    if getattr(message, "subtype", None) == "init":
        data = getattr(message, "data", {}) or {}
        sid = data.get("session_id") or data.get("sessionId")
        return str(sid) if sid else None
    return None


def _tool_call_directive(override: ToolCallOverride) -> str:
    """Render a tool redirect as a fork-and-steer instruction.

    A rename can only be stated, not applied: the fork point carries no tool
    args, so there is nothing here to rename. The forked session still holds the
    original call, so the model is told which keys to rename and left to do it.
    """
    # Name the replaced tool when we know it: "the one you called" is ambiguous
    # once a turn has made several parallel calls.
    replaced = f"`{override.source_tool}`" if override.source_tool else "the one you called"
    parts = [f"Use the `{override.name}` tool instead of {replaced}."]
    if override.args is not None:
        rendered = json.dumps(override.args, default=str, sort_keys=True)
        parts.append(f"Call it with exactly these arguments: {rendered}")
    elif override.arg_mapping:
        renames = ", ".join(
            f"`{old}` -> `{new}`" for old, new in sorted(override.arg_mapping.items())
        )
        parts.append(
            f"Reuse the arguments from your previous call, renaming {renames}. "
            "Keep every other argument unchanged."
        )
    return " ".join(parts)


def _steering_query(corrective: Corrective | None) -> str | None:
    if corrective is None:
        return None
    parts = [corrective.prompt] if corrective.prompt else []
    if corrective.tool_call is not None:
        parts.append(_tool_call_directive(corrective.tool_call))
    return "\n\n".join(parts) if parts else None


class ClaudeAgentSDKRewindCapability:
    framework = "claude_agent_sdk"

    def build_handle(
        self, span_id: str, trace_id: str, client: Any, session_id: str | None
    ) -> RewindHandle | None:
        if client is None or not session_id:
            return None
        payload = ClaudeForkPoint(
            client=client, session_id=str(session_id), options=getattr(client, "options", None)
        )
        return RewindHandle(
            framework=self.framework, trace_id=trace_id, span_id=span_id, payload=payload
        )

    def supports(self, handle: RewindHandle) -> bool:
        payload = handle.payload
        if not isinstance(payload, ClaudeForkPoint):
            return False
        return payload.client is not None and bool(payload.session_id)

    async def capture(self, span_id: str, trace_id: str, context: Any) -> RewindHandle | None:
        if not isinstance(context, dict):
            return None
        return self.build_handle(
            span_id, trace_id, context.get("client"), context.get("session_id")
        )

    async def rewind(self, handle: RewindHandle, corrective: Corrective | None) -> RewindOutcome:
        query = _steering_query(corrective)
        if query is None:
            return RewindOutcome.unsupported(reason="nothing to steer (no prompt or tool_call)")
        payload: ClaudeForkPoint = handle.payload
        options = self._fork_options(payload)
        forked = await self._spawn_fork(options)
        try:
            await forked.query(query)
            forked_session_id = await self._drive(forked, payload.session_id)
        finally:
            await self._disconnect(forked)
        if not forked_session_id:
            return RewindOutcome.failed("fork produced no forked session id", handle=handle)
        return RewindOutcome.ok(handle, result={"forked_session_id": forked_session_id})

    def _fork_options(self, payload: ClaudeForkPoint) -> Any:
        from claude_agent_sdk import ClaudeAgentOptions

        if dataclasses.is_dataclass(payload.options) and not isinstance(payload.options, type):
            return dataclasses.replace(
                payload.options,
                continue_conversation=False,
                session_id=None,
                resume=payload.session_id,
                fork_session=True,
            )
        return ClaudeAgentOptions(resume=payload.session_id, fork_session=True)

    async def _spawn_fork(self, options: Any) -> Any:
        from claude_agent_sdk import ClaudeSDKClient

        client = ClaudeSDKClient(options=options)
        client._aigie_skip_instrumentation = True  # type: ignore[attr-defined]
        await client.connect()
        return client

    async def _drive(self, forked: Any, original_session_id: str) -> str | None:
        forked_session_id: str | None = None
        async for message in forked.receive_response():
            sid = _extract_session_id(message)
            if sid and sid != original_session_id:
                forked_session_id = sid
        return forked_session_id

    async def _disconnect(self, forked: Any) -> None:
        try:
            await forked.disconnect()
        except Exception:  # noqa: BLE001 — cleanup must never break a run
            logger.debug("rewind fork disconnect failed", exc_info=True)
