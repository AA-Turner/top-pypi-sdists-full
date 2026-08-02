"""ToolCallHandler — index-based replay with divergence detection.

Mirrors createToolCallHandlers() from typescript-sandbox/run-tool-code.ts.

Key difference from TS: tool calls return asyncio.Future objects.
- Replay hit  -> future resolved immediately (code continues without suspending)
- New call    -> future left pending (coroutine suspends, triggers deadlock detection)
"""

import asyncio
import uuid
from collections.abc import Callable
from typing import Any

from .types import (
    PendingTool,
    RejectedTool,
    ResolvedTool,
    ToolCallFunction,
    ToolDefinition,
    ToolState,
)


class ToolRejectedError(Exception):
    """Raised when replaying a rejected tool call."""

    def __init__(self, error: Any):
        self.error = error
        super().__init__(str(error))


class ToolCallHandler:
    """Index-based tool call replay with divergence detection.

    Each call_tool() returns an asyncio.Future:
    - Replay match: resolved immediately with cached result
    - Replay reject: resolved immediately with exception
    - New call: left unresolved (triggers deadlock detection)

    call_internal() is synchronous — for deterministic shims
    (time.time, random.random).
    """

    def __init__(
        self,
        tools: list[ToolDefinition],
        tool_states: list[ToolState],
        loop: asyncio.AbstractEventLoop,
    ):
        self.tools = {t.function.name: t for t in tools}
        self.tool_states = tool_states
        self.loop = loop
        self.index = 0
        self.diverged = False
        self.output: list[ToolState] = []
        self.pending_count = 0

    def _lookup(self, name: str, args: dict) -> tuple[str, ToolState | None]:
        """Check whether this call matches the replay log at current index.

        Returns ("replay", state) | ("new", None) | ("mismatch", None).
        """
        if self.index >= len(self.tool_states):
            return ("new", None)

        current = self.tool_states[self.index]
        if isinstance(current, PendingTool):
            return ("mismatch", None)

        if current.function.name == name and current.function.arguments == args:
            return ("replay", current)

        return ("mismatch", None)

    def call_tool(self, name: str, args: dict | None) -> asyncio.Future[Any]:
        """Call an external tool. Returns a Future.

        On replay: future is already resolved/rejected.
        On new call: future stays pending (deadlock trigger).
        """
        args = args or {}

        if not self.diverged:
            kind, state = self._lookup(name, args)

            if kind == "replay" and state is not None:
                self.output.append(state)
                self.index += 1
                future: asyncio.Future[Any] = self.loop.create_future()
                if isinstance(state, ResolvedTool):
                    future.set_result(state.result)
                elif isinstance(state, RejectedTool):
                    future.set_exception(ToolRejectedError(state.error))
                return future

            if kind == "mismatch":
                self.diverged = True

        # New call — future stays unresolved
        self.index += 1
        tool_id = uuid.uuid4().hex[:8]
        self.output.append(
            PendingTool(
                id=tool_id,
                function=ToolCallFunction(name=name, arguments=args),
            )
        )
        self.pending_count += 1
        return self.loop.create_future()  # unresolved

    def call_internal(self, name: str, produce_fn: Callable[[], Any]) -> Any:
        """Synchronous replay for deterministic shims.

        On replay: returns cached value.
        On first run: calls produce_fn(), caches result.
        """
        args: dict[str, Any] = {}

        if not self.diverged:
            kind, state = self._lookup(name, args)
            if kind == "replay" and isinstance(state, ResolvedTool):
                self.output.append(state)
                self.index += 1
                return state.result
            if kind == "mismatch":
                self.diverged = True

        value = produce_fn()
        self.index += 1
        self.output.append(
            ResolvedTool(
                id=uuid.uuid4().hex[:8],
                function=ToolCallFunction(name=name, arguments=args),
                result=value,
            )
        )
        return value
