"""Native lifecycle hooks for the OpenAI Agents SDK integration.

The Agents SDK's tracing processor observes spans, while its lifecycle hooks
observe the Runner and Agent callbacks.  This module provides both surfaces so
applications can retain the native ``Runner.run(..., hooks=...)`` and
``Agent(..., hooks=...)`` APIs and still have workflow input/output available
to the Kytte root span.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

try:
    from agents.lifecycle import AgentHooksBase, RunHooksBase
    from agents.tracing import get_current_trace
except ImportError:  # pragma: no cover - optional dependency is not installed

    class RunHooksBase:  # type: ignore[no-redef]
        pass

    class AgentHooksBase:  # type: ignore[no-redef]
        pass

    def get_current_trace() -> Any:  # type: ignore[misc]
        return None


from aigie.integrations._base import get as get_adapter

EventCallback = Callable[[str, dict[str, Any]], Any | Awaitable[Any]]


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool, list, dict)):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "to_input_item"):
        return value.to_input_item()
    return str(value)


def _processor() -> Any | None:
    adapter = get_adapter("openai_agents")
    return getattr(adapter, "processor", None) if adapter is not None else None


def _is_final_llm_response(response: Any) -> bool:
    """Return whether an LLM response has no pending tool invocation."""
    output = getattr(response, "output", None)
    if not output:
        return False
    for item in output:
        if getattr(item, "type", None) in {"function_call", "hosted_tool_call"}:
            return False
        if getattr(item, "tool_calls", None):
            return False
    return True


class _HooksSupport:
    def __init__(self, callback: EventCallback | None = None, input: Any = None) -> None:
        self._callback = callback
        self._input = input
        self._native_llm_active = False

    def _begin_native_llm(self) -> None:
        """Prevent generic provider instrumentation duplicating native Agent spans."""
        if not self._native_llm_active:
            from aigie.auto_instrument.trace import set_callback_context

            set_callback_context(True)
            self._native_llm_active = True

    def _end_native_llm(self) -> None:
        if self._native_llm_active:
            from aigie.auto_instrument.trace import set_callback_context

            set_callback_context(False)
            self._native_llm_active = False

    def _trace_id(self) -> str | None:
        trace = get_current_trace()
        return trace.trace_id if trace is not None else None

    async def _notify(self, event: str, **fields: Any) -> None:
        payload = {key: _jsonable(value) for key, value in fields.items()}
        processor = _processor()
        trace_id = self._trace_id()
        if processor is not None and trace_id is not None:
            if event in {"agent_start", "llm_start"} and (
                self._input is not None or payload.get("input") is not None
            ):
                processor.record_workflow_io(
                    trace_id,
                    input_value=self._input if self._input is not None else payload["input"],
                )
            if event in {"agent_end", "llm_end"} and payload.get("output") is not None:
                processor.record_workflow_io(trace_id, output_value=payload["output"])
            # Only llm_start carries it: the Agents SDK resolves the agent's
            # instructions before the call and hands the result to this hook.
            if event == "llm_start":
                processor.record_system_prompt(trace_id, fields.get("system_prompt"))
        if self._callback is not None:
            result = self._callback(event, payload)
            if hasattr(result, "__await__"):
                await result


class OpenAIAgentsRunHooks(_HooksSupport, RunHooksBase):
    """Runner-level hooks for all Agents SDK lifecycle events."""

    async def on_llm_start(
        self, context: Any, agent: Any, system_prompt: Any, input_items: Any
    ) -> None:
        self._begin_native_llm()
        await self._notify(
            "llm_start", agent=agent.name, system_prompt=system_prompt, input=input_items
        )

    async def on_llm_end(self, context: Any, agent: Any, response: Any) -> None:
        try:
            await self._notify(
                "llm_end",
                agent=agent.name,
                response=response,
                output=response if _is_final_llm_response(response) else None,
            )
        finally:
            self._end_native_llm()

    async def on_agent_start(self, context: Any, agent: Any) -> None:
        await self._notify("agent_start", agent=agent.name, input=getattr(context, "context", None))

    async def on_agent_end(self, context: Any, agent: Any, output: Any) -> None:
        await self._notify("agent_end", agent=agent.name, output=output)

    async def on_handoff(self, context: Any, from_agent: Any, to_agent: Any) -> None:
        await self._notify("handoff", from_agent=from_agent.name, to_agent=to_agent.name)

    async def on_tool_start(self, context: Any, agent: Any, tool: Any) -> None:
        await self._notify("tool_start", agent=agent.name, tool=getattr(tool, "name", tool))

    async def on_tool_end(self, context: Any, agent: Any, tool: Any, result: Any) -> None:
        await self._notify(
            "tool_end", agent=agent.name, tool=getattr(tool, "name", tool), output=result
        )


class OpenAIAgentsAgentHooks(_HooksSupport, AgentHooksBase):
    """Agent-level hooks for the lifecycle of one specific Agent instance."""

    async def on_start(self, context: Any, agent: Any) -> None:
        await self._notify("agent_start", agent=agent.name, input=getattr(context, "context", None))

    async def on_end(self, context: Any, agent: Any, output: Any) -> None:
        await self._notify("agent_end", agent=agent.name, output=output)

    async def on_handoff(self, context: Any, agent: Any, source: Any) -> None:
        await self._notify("handoff", from_agent=source.name, to_agent=agent.name)

    async def on_tool_start(self, context: Any, agent: Any, tool: Any) -> None:
        await self._notify("tool_start", agent=agent.name, tool=getattr(tool, "name", tool))

    async def on_tool_end(self, context: Any, agent: Any, tool: Any, result: Any) -> None:
        await self._notify(
            "tool_end", agent=agent.name, tool=getattr(tool, "name", tool), output=result
        )

    async def on_llm_start(
        self, context: Any, agent: Any, system_prompt: Any, input_items: Any
    ) -> None:
        self._begin_native_llm()
        await self._notify(
            "llm_start", agent=agent.name, system_prompt=system_prompt, input=input_items
        )

    async def on_llm_end(self, context: Any, agent: Any, response: Any) -> None:
        try:
            await self._notify(
                "llm_end",
                agent=agent.name,
                response=response,
                output=response if _is_final_llm_response(response) else None,
            )
        finally:
            self._end_native_llm()


def openai_agents_hooks(
    callback: EventCallback | None = None, *, input: Any = None
) -> OpenAIAgentsRunHooks:
    """Return Runner hooks; pass ``input`` to retain the exact Runner boundary."""
    return OpenAIAgentsRunHooks(callback, input)


def openai_agents_pause(result: Any) -> Any:
    """Mark a pending tool approval paused before resuming its ``RunState``."""
    interruptions = list(getattr(result, "interruptions", ()) or ())
    trace_state = getattr(result, "_trace_state", None)
    trace_id = getattr(trace_state, "trace_id", None)
    processor = _processor()
    if interruptions and trace_id and processor is not None:
        processor.mark_interrupted(trace_id, len(interruptions))
    return result.to_state()


__all__ = [
    "OpenAIAgentsAgentHooks",
    "OpenAIAgentsRunHooks",
    "openai_agents_hooks",
    "openai_agents_pause",
]
