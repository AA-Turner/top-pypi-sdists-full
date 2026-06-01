"""
OpenAI Agents SDK Handler for Aigie integration.

Provides event-driven tracing for OpenAI Agents SDK workflows.
"""

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from ...context_manager import merge_metadata

logger = logging.getLogger(__name__)


def _utc_isoformat() -> str:
    return datetime.now(timezone.utc).isoformat()


class OpenAIAgentsHandler:
    """Handler for OpenAI Agents SDK tracing integration.

    This handler provides lifecycle methods for tracing agent workflows,
    generations, tool calls, handoffs, and guardrails.

    Example:
        handler = OpenAIAgentsHandler(trace_name="Agent Workflow")
        handler.set_trace_context(trace)

        # Track workflow
        workflow_id = await handler.handle_workflow_start("main_workflow")

        # Track agent
        agent_id = await handler.handle_agent_start("assistant", model="gpt-4o")

        # Track generation
        gen_id = await handler.handle_generation_start("gpt-4o", messages)
        await handler.handle_generation_end(gen_id, response, tokens)

        # Track tool call
        tool_id = await handler.handle_tool_start("search", args)
        await handler.handle_tool_end(tool_id, result)

        await handler.handle_agent_end(agent_id, output)
        await handler.handle_workflow_end(workflow_id)
    """

    def __init__(
        self,
        trace_name: str = "OpenAI Agents Workflow",
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        """Initialize the handler.

        Args:
            trace_name: Name for the trace
            metadata: Additional metadata to attach
            tags: Tags for filtering
            user_id: User identifier
            session_id: Session identifier
        """
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id

        # State tracking
        self.trace_id: str | None = None
        self.span_map: dict[str, dict[str, Any]] = {}
        self._current_span_id: str | None = None
        self._trace_context: Any = None
        self._aigie: Any = None

        # Statistics
        self.total_tokens = 0
        self.total_cost = 0.0
        self.generation_count = 0
        self.tool_call_count = 0
        self.handoff_count = 0
        self.agent_count = 0

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    def set_trace_context(self, trace: Any) -> None:
        """Set the trace context for this handler."""
        self._trace_context = trace
        if hasattr(trace, "id"):
            self.trace_id = trace.id

    async def handle_workflow_start(
        self,
        workflow_name: str,
        agents: list[str] | None = None,
        input_data: Any | None = None,
    ) -> str:
        """Handle workflow start event.

        Args:
            workflow_name: Name of the workflow
            agents: List of agent names in the workflow
            input_data: Initial input to the workflow

        Returns:
            Workflow span ID
        """
        workflow_id = str(uuid.uuid4())

        span_data = {
            "name": f"workflow:{workflow_name}",
            "type": "chain",
            "start_time": time.time(),
            "metadata": merge_metadata(
                {
                    "workflow_name": workflow_name,
                    "agents": agents or [],
                    "agent_count": len(agents) if agents else 0,
                }
            ),
        }

        if input_data:
            span_data["input"] = self._safe_str(input_data)

        self.span_map[workflow_id] = span_data
        self._current_span_id = workflow_id

        logger.debug(f"Started workflow trace: {workflow_name}")

        # Create span via aigie if available
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                payload = {
                    "id": workflow_id,
                    "trace_id": self.trace_id,
                    "name": span_data["name"],
                    "type": span_data["type"],
                    "input": span_data.get("input"),
                    "metadata": span_data["metadata"],
                    "status": "pending",
                    "start_time": _utc_isoformat(),
                    "created_at": _utc_isoformat(),
                }
                await aigie._buffer.add(EventType.SPAN_CREATE, payload)
            except Exception as e:
                logger.debug(f"Error creating workflow span: {e}")

        return workflow_id

    async def handle_workflow_end(
        self,
        workflow_id: str,
        output: Any | None = None,
        error: str | None = None,
    ) -> None:
        """Handle workflow end event.

        Args:
            workflow_id: Workflow span ID
            output: Workflow output
            error: Error message if failed
        """
        if workflow_id not in self.span_map:
            return

        span_data = self.span_map[workflow_id]
        span_data["end_time"] = time.time()
        span_data["duration"] = span_data["end_time"] - span_data["start_time"]

        if output is not None:
            span_data["output"] = self._safe_str(output)
        if error:
            span_data["error"] = error
            span_data["status"] = "error"
        else:
            span_data["status"] = "success"

        # Add statistics
        span_data["metadata"].update(
            {
                "total_tokens": self.total_tokens,
                "total_cost": self.total_cost,
                "generation_count": self.generation_count,
                "tool_call_count": self.tool_call_count,
                "handoff_count": self.handoff_count,
                "agent_count": self.agent_count,
            }
        )

        logger.debug(f"Ended workflow trace: {span_data['name']}")

        # Update span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                duration = span_data.get("duration", 0)
                payload = {
                    "id": workflow_id,
                    "output": span_data.get("output"),
                    "metadata": span_data["metadata"],
                    "status": span_data.get("status", "success"),
                    "end_time": _utc_isoformat(),
                    "duration_ns": int(duration * 1_000_000_000),
                }
                if span_data.get("error"):
                    payload["error"] = span_data["error"]
                    payload["error_message"] = span_data["error"]
                await aigie._buffer.add(EventType.SPAN_UPDATE, payload)
            except Exception as e:
                logger.debug(f"Error updating workflow span: {e}")

        if workflow_id in self.span_map:
            del self.span_map[workflow_id]

    async def handle_agent_start(
        self,
        agent_name: str,
        model: str | None = None,
        instructions: str | None = None,
        tools: list[str] | None = None,
        handoffs: list[str] | None = None,
        parent_span_id: str | None = None,
        tool_definitions: list[dict[str, Any]] | None = None,
    ) -> str:
        """Handle agent start event.

        Args:
            agent_name: Name of the agent
            model: Model used by the agent
            instructions: Agent instructions
            tools: List of available tool names
            handoffs: List of possible handoff targets
            parent_span_id: Parent span ID
            tool_definitions: Full tool/function schemas for available tools

        Returns:
            Agent span ID
        """
        agent_id = str(uuid.uuid4())
        self.agent_count += 1

        span_data = {
            "name": f"agent:{agent_name}",
            "type": "agent",
            "start_time": time.time(),
            "parent_span_id": parent_span_id or self._current_span_id,
            "metadata": merge_metadata(
                {
                    "agent_name": agent_name,
                    "model": model,
                    "tools": tools or [],
                    "tool_count": len(tools) if tools else 0,
                    "handoffs": handoffs or [],
                    "handoff_count": len(handoffs) if handoffs else 0,
                }
            ),
        }

        if instructions:
            span_data["metadata"]["system_prompt"] = instructions

        if tool_definitions:
            span_data["metadata"]["available_tools"] = tool_definitions

        self.span_map[agent_id] = span_data
        self._current_span_id = agent_id

        logger.debug(f"Started agent trace: {agent_name}")

        # Create span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                payload = {
                    "id": agent_id,
                    "trace_id": self.trace_id,
                    "parent_id": span_data.get("parent_span_id"),
                    "name": span_data["name"],
                    "type": "agent",
                    "metadata": span_data["metadata"],
                    "status": "pending",
                    "start_time": _utc_isoformat(),
                    "created_at": _utc_isoformat(),
                }
                await aigie._buffer.add(EventType.SPAN_CREATE, payload)
            except Exception as e:
                logger.debug(f"Error creating agent span: {e}")

        return agent_id

    async def handle_agent_end(
        self,
        agent_id: str,
        output: Any | None = None,
        error: str | None = None,
    ) -> None:
        """Handle agent end event."""
        if agent_id not in self.span_map:
            return

        span_data = self.span_map[agent_id]
        span_data["end_time"] = time.time()
        span_data["duration"] = span_data["end_time"] - span_data["start_time"]

        if output is not None:
            span_data["output"] = self._safe_str(output)
        if error:
            span_data["error"] = error
            span_data["status"] = "error"
        else:
            span_data["status"] = "success"

        # Restore parent span as current
        self._current_span_id = span_data.get("parent_span_id")

        logger.debug(f"Ended agent trace: {span_data['name']}")

        # Update span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                duration = span_data.get("duration", 0)
                payload = {
                    "id": agent_id,
                    "output": span_data.get("output"),
                    "metadata": span_data["metadata"],
                    "status": span_data.get("status", "success"),
                    "end_time": _utc_isoformat(),
                    "duration_ns": int(duration * 1_000_000_000),
                }
                if span_data.get("error"):
                    payload["error"] = span_data["error"]
                    payload["error_message"] = span_data["error"]
                await aigie._buffer.add(EventType.SPAN_UPDATE, payload)
            except Exception as e:
                logger.debug(f"Error updating agent span: {e}")

        if agent_id in self.span_map:
            del self.span_map[agent_id]

    async def handle_generation_start(
        self,
        model: str,
        messages: list[dict[str, Any]] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        parent_span_id: str | None = None,
        top_p: float | None = None,
        generation_kwargs: dict[str, Any] | None = None,
    ) -> str:
        """Handle LLM generation start event.

        Args:
            model: Model name
            messages: Input messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            parent_span_id: Parent span ID
            top_p: Top-p sampling parameter
            generation_kwargs: Additional generation kwargs to extract params from

        Returns:
            Generation span ID
        """
        gen_id = str(uuid.uuid4())
        self.generation_count += 1

        # Extract model parameters from explicit args and generation_kwargs
        model_parameters = {}
        if temperature is not None:
            model_parameters["temperature"] = temperature
        if max_tokens is not None:
            model_parameters["max_tokens"] = max_tokens
        if top_p is not None:
            model_parameters["top_p"] = top_p
        if generation_kwargs:
            for key in (
                "temperature",
                "top_p",
                "top_k",
                "max_tokens",
                "stop",
                "stop_sequences",
                "presence_penalty",
                "frequency_penalty",
            ):
                val = generation_kwargs.get(key)
                if val is not None and key not in model_parameters:
                    model_parameters[key] = val

        span_data = {
            "name": f"llm:{model}",
            "type": "llm",
            "start_time": time.time(),
            "parent_span_id": parent_span_id or self._current_span_id,
            "metadata": merge_metadata(
                {
                    "model": model,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "message_count": len(messages) if messages else 0,
                }
            ),
        }

        if model_parameters:
            span_data["metadata"]["model_parameters"] = model_parameters

        if messages:
            span_data["input"] = self._format_messages(messages)

        self.span_map[gen_id] = span_data

        logger.debug(f"Started generation trace: {model}")

        # Create span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                payload = {
                    "id": gen_id,
                    "trace_id": self.trace_id,
                    "parent_id": span_data.get("parent_span_id"),
                    "name": span_data["name"],
                    "type": "llm",
                    "input": span_data.get("input"),
                    "metadata": span_data["metadata"],
                    "model": model,
                    "status": "pending",
                    "start_time": _utc_isoformat(),
                    "created_at": _utc_isoformat(),
                }
                await aigie._buffer.add(EventType.SPAN_CREATE, payload)
            except Exception as e:
                logger.debug(f"Error creating generation span: {e}")

        return gen_id

    async def handle_generation_end(
        self,
        gen_id: str,
        response: str | None = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float = 0.0,
        tool_calls: list[dict[str, Any]] | None = None,
        error: str | None = None,
        finish_reason: str | None = None,
    ) -> None:
        """Handle LLM generation end event."""
        if gen_id not in self.span_map:
            return

        span_data = self.span_map[gen_id]
        span_data["end_time"] = time.time()
        span_data["duration"] = span_data["end_time"] - span_data["start_time"]

        # Update tokens
        self.total_tokens += input_tokens + output_tokens
        self.total_cost += cost

        # Infer finish_reason from tool_calls if not explicitly provided
        if not finish_reason:
            if tool_calls:
                finish_reason = "tool_use"
            elif error:
                finish_reason = "error"

        span_data["metadata"].update(
            {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "cost": cost,
                "tool_calls_count": len(tool_calls) if tool_calls else 0,
            }
        )

        if finish_reason:
            span_data["metadata"]["finish_reason"] = finish_reason

        if response:
            span_data["output"] = self._safe_str(response)
        if error:
            span_data["error"] = error
            span_data["status"] = "error"
        else:
            span_data["status"] = "success"

        logger.debug(f"Ended generation trace: {span_data['name']}")

        # Update span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                duration = span_data.get("duration", 0)
                payload = {
                    "id": gen_id,
                    "output": span_data.get("output"),
                    "metadata": span_data["metadata"],
                    "status": span_data.get("status", "success"),
                    "end_time": _utc_isoformat(),
                    "duration_ns": int(duration * 1_000_000_000),
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                }
                if cost > 0:
                    payload["total_cost"] = cost
                if span_data.get("error"):
                    payload["error"] = span_data["error"]
                    payload["error_message"] = span_data["error"]
                await aigie._buffer.add(EventType.SPAN_UPDATE, payload)
            except Exception as e:
                logger.debug(f"Error updating generation span: {e}")

        if gen_id in self.span_map:
            del self.span_map[gen_id]

    async def handle_tool_start(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        parent_span_id: str | None = None,
    ) -> str:
        """Handle tool call start event.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            parent_span_id: Parent span ID

        Returns:
            Tool span ID
        """
        tool_id = str(uuid.uuid4())
        self.tool_call_count += 1

        span_data = {
            "name": f"tool:{tool_name}",
            "type": "tool",
            "start_time": time.time(),
            "parent_span_id": parent_span_id or self._current_span_id,
            "metadata": merge_metadata(
                {
                    "tool_name": tool_name,
                }
            ),
        }

        if arguments:
            span_data["input"] = self._safe_str(arguments)
            span_data["metadata"]["arg_count"] = len(arguments)

        self.span_map[tool_id] = span_data

        logger.debug(f"Started tool trace: {tool_name}")

        # Create span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                payload = {
                    "id": tool_id,
                    "trace_id": self.trace_id,
                    "parent_id": span_data.get("parent_span_id"),
                    "name": span_data["name"],
                    "type": "tool",
                    "input": span_data.get("input"),
                    "metadata": span_data["metadata"],
                    "status": "pending",
                    "start_time": _utc_isoformat(),
                    "created_at": _utc_isoformat(),
                }
                await aigie._buffer.add(EventType.SPAN_CREATE, payload)
            except Exception as e:
                logger.debug(f"Error creating tool span: {e}")

        return tool_id

    async def handle_tool_end(
        self,
        tool_id: str,
        result: Any | None = None,
        error: str | None = None,
    ) -> None:
        """Handle tool call end event."""
        if tool_id not in self.span_map:
            return

        span_data = self.span_map[tool_id]
        span_data["end_time"] = time.time()
        span_data["duration"] = span_data["end_time"] - span_data["start_time"]

        if result is not None:
            span_data["output"] = self._safe_str(result)
        if error:
            span_data["error"] = error
            span_data["status"] = "error"
        else:
            span_data["status"] = "success"

        logger.debug(f"Ended tool trace: {span_data['name']}")

        # Update span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                duration = span_data.get("duration", 0)
                payload = {
                    "id": tool_id,
                    "output": span_data.get("output"),
                    "metadata": span_data["metadata"],
                    "status": span_data.get("status", "success"),
                    "end_time": _utc_isoformat(),
                    "duration_ns": int(duration * 1_000_000_000),
                }
                if span_data.get("error"):
                    payload["error"] = span_data["error"]
                    payload["error_message"] = span_data["error"]
                await aigie._buffer.add(EventType.SPAN_UPDATE, payload)
            except Exception as e:
                logger.debug(f"Error updating tool span: {e}")

        if tool_id in self.span_map:
            del self.span_map[tool_id]

    async def handle_handoff_start(
        self,
        source_agent: str,
        target_agent: str,
        reason: str | None = None,
        context: dict[str, Any] | None = None,
        parent_span_id: str | None = None,
    ) -> str:
        """Handle agent handoff start event.

        Args:
            source_agent: Agent initiating handoff
            target_agent: Agent receiving handoff
            reason: Reason for handoff
            context: Context being passed
            parent_span_id: Parent span ID

        Returns:
            Handoff span ID
        """
        handoff_id = str(uuid.uuid4())
        self.handoff_count += 1

        span_data = {
            "name": f"handoff:{source_agent}->{target_agent}",
            "type": "chain",
            "start_time": time.time(),
            "parent_span_id": parent_span_id or self._current_span_id,
            "metadata": merge_metadata(
                {
                    "source_agent": source_agent,
                    "target_agent": target_agent,
                    "reason": reason,
                    "handoff_depth": self.handoff_count,
                }
            ),
        }

        if context:
            span_data["input"] = self._safe_str(context)

        self.span_map[handoff_id] = span_data

        logger.debug(f"Started handoff trace: {source_agent} -> {target_agent}")

        # Create span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                payload = {
                    "id": handoff_id,
                    "trace_id": self.trace_id,
                    "parent_id": span_data.get("parent_span_id"),
                    "name": span_data["name"],
                    "type": "chain",
                    "input": span_data.get("input"),
                    "metadata": span_data["metadata"],
                    "status": "pending",
                    "start_time": _utc_isoformat(),
                    "created_at": _utc_isoformat(),
                }
                await aigie._buffer.add(EventType.SPAN_CREATE, payload)
            except Exception as e:
                logger.debug(f"Error creating handoff span: {e}")

        return handoff_id

    async def handle_handoff_end(
        self,
        handoff_id: str,
        success: bool = True,
        error: str | None = None,
    ) -> None:
        """Handle agent handoff end event."""
        if handoff_id not in self.span_map:
            return

        span_data = self.span_map[handoff_id]
        span_data["end_time"] = time.time()
        span_data["duration"] = span_data["end_time"] - span_data["start_time"]

        if error:
            span_data["error"] = error
            span_data["status"] = "error"
        else:
            span_data["status"] = "success" if success else "error"

        logger.debug(f"Ended handoff trace: {span_data['name']}")

        # Update span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                duration = span_data.get("duration", 0)
                payload = {
                    "id": handoff_id,
                    "metadata": span_data["metadata"],
                    "status": span_data.get("status", "success"),
                    "end_time": _utc_isoformat(),
                    "duration_ns": int(duration * 1_000_000_000),
                }
                if span_data.get("error"):
                    payload["error"] = span_data["error"]
                    payload["error_message"] = span_data["error"]
                await aigie._buffer.add(EventType.SPAN_UPDATE, payload)
            except Exception as e:
                logger.debug(f"Error updating handoff span: {e}")

        if handoff_id in self.span_map:
            del self.span_map[handoff_id]

    async def handle_guardrail_start(
        self,
        guardrail_name: str,
        guardrail_type: str = "validation",
        input_data: Any | None = None,
        parent_span_id: str | None = None,
    ) -> str:
        """Handle guardrail check start event.

        Args:
            guardrail_name: Name of the guardrail
            guardrail_type: Type (input/output/validation)
            input_data: Data being validated
            parent_span_id: Parent span ID

        Returns:
            Guardrail span ID
        """
        guardrail_id = str(uuid.uuid4())

        span_data = {
            "name": f"guardrail:{guardrail_name}",
            "type": "tool",
            "start_time": time.time(),
            "parent_span_id": parent_span_id or self._current_span_id,
            "metadata": merge_metadata(
                {
                    "guardrail_name": guardrail_name,
                    "guardrail_type": guardrail_type,
                }
            ),
        }

        if input_data:
            span_data["input"] = self._safe_str(input_data)

        self.span_map[guardrail_id] = span_data

        logger.debug(f"Started guardrail trace: {guardrail_name}")

        # Create span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                payload = {
                    "id": guardrail_id,
                    "trace_id": self.trace_id,
                    "parent_id": span_data.get("parent_span_id"),
                    "name": span_data["name"],
                    "type": "tool",
                    "input": span_data.get("input"),
                    "metadata": span_data["metadata"],
                    "status": "pending",
                    "start_time": _utc_isoformat(),
                    "created_at": _utc_isoformat(),
                }
                await aigie._buffer.add(EventType.SPAN_CREATE, payload)
            except Exception as e:
                logger.debug(f"Error creating guardrail span: {e}")

        return guardrail_id

    async def handle_guardrail_end(
        self,
        guardrail_id: str,
        passed: bool = True,
        result: Any | None = None,
        error: str | None = None,
    ) -> None:
        """Handle guardrail check end event."""
        if guardrail_id not in self.span_map:
            return

        span_data = self.span_map[guardrail_id]
        span_data["end_time"] = time.time()
        span_data["duration"] = span_data["end_time"] - span_data["start_time"]

        span_data["metadata"]["passed"] = passed

        if result is not None:
            span_data["output"] = self._safe_str(result)
        if error:
            span_data["error"] = error
            span_data["status"] = "error"
        else:
            span_data["status"] = "success" if passed else "error"

        logger.debug(f"Ended guardrail trace: {span_data['name']} (passed={passed})")

        # Update span via aigie
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                duration = span_data.get("duration", 0)
                payload = {
                    "id": guardrail_id,
                    "output": span_data.get("output"),
                    "metadata": span_data["metadata"],
                    "status": span_data.get("status", "success"),
                    "end_time": _utc_isoformat(),
                    "duration_ns": int(duration * 1_000_000_000),
                }
                if span_data.get("error"):
                    payload["error"] = span_data["error"]
                    payload["error_message"] = span_data["error"]
                await aigie._buffer.add(EventType.SPAN_UPDATE, payload)
            except Exception as e:
                logger.debug(f"Error updating guardrail span: {e}")

        if guardrail_id in self.span_map:
            del self.span_map[guardrail_id]

    def _safe_str(self, value: Any, max_length: int = 2000) -> str:
        """Safely convert value to string with length limit."""
        try:
            if value is None:
                return ""
            s = str(value)
            if len(s) > max_length:
                return s[:max_length] + "..."
            return s
        except Exception:
            return "<error converting to string>"

    def _format_messages(self, messages: list[dict[str, Any]]) -> str:
        """Format messages for tracing."""
        try:
            formatted = []
            for msg in messages[-5:]:  # Last 5 messages
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                if isinstance(content, str):
                    preview = content[:200] + "..." if len(content) > 200 else content
                else:
                    preview = str(content)[:200]
                formatted.append(f"{role}: {preview}")
            return "\n".join(formatted)
        except Exception:
            return str(messages)[:1000]

    def get_statistics(self) -> dict[str, Any]:
        """Get current tracing statistics."""
        return {
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "generation_count": self.generation_count,
            "tool_call_count": self.tool_call_count,
            "handoff_count": self.handoff_count,
            "agent_count": self.agent_count,
            "span_count": len(self.span_map),
        }
