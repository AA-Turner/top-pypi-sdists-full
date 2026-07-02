"""The native engine — the default in-process Dreadnode agent loop.

This is a thin delegation to ``Agent._native_run_loop`` (the historical
``_stream`` body). Keeping the loop on ``Agent`` lets the native path stay
byte-for-byte unchanged while ``engine`` becomes a first-class, overridable seam.
The native engine owns the loop, so it enforces every policy facet and dispatches
its events inline (``dispatches_internally = True``).
"""

import typing as t

from dreadnode.agents.engines.base import AgentEngine, EngineContext

if t.TYPE_CHECKING:
    from dreadnode.agents.events import AgentEvent


class NativeEngine(AgentEngine):
    """Runs the standard Dreadnode agent loop in-process."""

    name = "native"
    dispatches_internally = True

    async def run_loop(self, ctx: EngineContext) -> "t.AsyncIterator[AgentEvent]":
        async for event in ctx.agent._native_run_loop(ctx.trajectory):
            yield event
