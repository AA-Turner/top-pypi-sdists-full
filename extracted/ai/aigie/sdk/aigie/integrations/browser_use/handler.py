"""
Browser-Use callback handler for Aigie SDK.

Provides automatic tracing for browser-use Agent executions,
similar to LangGraphHandler and AigieCallbackHandler.
"""

import uuid
from datetime import datetime, timezone
from typing import Any

from ...buffer import EventType
from ...context_manager import merge_metadata


def _utc_isoformat() -> str:
    return datetime.now(timezone.utc).isoformat()


class BrowserUseHandler:
    """
    Browser-Use callback handler for Aigie.

    Automatically traces browser-use workflow executions including:
    - Agent steps
    - LLM calls with tokens/cost
    - Browser actions
    - Screenshots (optional)

    Example:
        >>> from browser_use import Agent, ChatBrowserUse
        >>> from aigie.integrations.browser_use import BrowserUseHandler
        >>>
        >>> handler = BrowserUseHandler(
        ...     trace_name='web-automation',
        ...     metadata={'task_type': 'research'}
        ... )
        >>>
        >>> agent = Agent(task="...", llm=ChatBrowserUse())
        >>> result = await agent.run()
    """

    def __init__(
        self,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        capture_screenshots: bool = True,
        capture_dom: bool = False,
    ):
        """
        Initialize Browser-Use handler.

        Args:
            trace_name: Name for the trace
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
            capture_screenshots: Whether to capture screenshots
            capture_dom: Whether to capture DOM state
        """
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id
        self.capture_screenshots = capture_screenshots
        self.capture_dom = capture_dom

        # State tracking
        self.trace_id: str | None = None
        self.step_map: dict[int, dict[str, Any]] = {}  # step_num -> {spanId, startTime}
        self.action_map: dict[
            str, dict[str, Any]
        ] = {}  # action_id -> {spanId, startTime, parentSpanId}
        self.llm_call_map: dict[
            str, dict[str, Any]
        ] = {}  # call_id -> {spanId, startTime, parentSpanId}

        # Current span tracking for parent relationships
        self._current_step_span_id: str | None = None
        self._aigie = None
        self._trace_context: Any | None = None

        # Statistics
        self.total_steps = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.total_actions = 0

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    def set_trace_context(self, trace_context: Any) -> None:
        """Set an existing trace context to use."""
        self._trace_context = trace_context
        if hasattr(trace_context, "id"):
            self.trace_id = str(trace_context.id)

    async def handle_task_start(
        self,
        task: str,
        max_steps: int,
        llm_info: dict[str, Any] | None = None,
    ) -> None:
        """
        Called when the browser-use task starts.

        Args:
            task: The task description
            max_steps: Maximum number of steps allowed
            llm_info: Information about the LLM being used
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        # Generate trace ID if not set
        if not self.trace_id:
            if self._trace_context and hasattr(self._trace_context, "id"):
                self.trace_id = str(self._trace_context.id)
            else:
                self.trace_id = str(uuid.uuid4())

        # Build trace name
        task_snippet = task[:50] + "..." if len(task) > 50 else task
        trace_name = self.trace_name or f"Browser Task: {task_snippet}"

        # Build metadata
        trace_metadata = merge_metadata(
            {
                **self.metadata,
                "task": task,
                "max_steps": max_steps,
                "framework": "browser-use",
            }
        )
        if llm_info:
            trace_metadata["llm"] = llm_info

        # Only create trace if we don't have a trace context
        if not self._trace_context:
            trace_data = {
                "id": self.trace_id,
                "name": trace_name,
                "type": "chain",
                "input": {"task": task},
                "status": "pending",
                "tags": [*self.tags, "browser-use", "web-automation"],
                "metadata": merge_metadata(trace_metadata),
                "start_time": _utc_isoformat(),
                "created_at": _utc_isoformat(),
            }

            if self.user_id:
                trace_data["user_id"] = self.user_id
            if self.session_id:
                trace_data["session_id"] = self.session_id

            # Send trace via buffer
            if aigie._buffer:
                await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)
            else:
                try:
                    if aigie.client:
                        await aigie.client.post(
                            f"{aigie.api_url}/v1/traces",
                            json=trace_data,
                            headers={"X-API-Key": aigie.api_key},
                            timeout=5.0,
                        )
                except Exception:
                    pass

    async def handle_task_end(
        self,
        success: bool,
        result: Any | None = None,
        error: str | None = None,
    ) -> None:
        """
        Called when the browser-use task completes.

        Args:
            success: Whether the task succeeded
            result: The task result
            error: Error message if failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        end_time = datetime.now(timezone.utc)

        update_data = {
            "id": self.trace_id,
            "status": "success" if success else "failed",
            "output": {
                "success": success,
                "total_steps": self.total_steps,
                "total_tokens": self.total_tokens,
                "total_cost": self.total_cost,
                "total_actions": self.total_actions,
            },
            "end_time": end_time.isoformat(),
        }

        if result:
            update_data["output"]["result"] = str(result)[:1000]
        if error:
            update_data["error"] = error
            update_data["error_message"] = error

        # Send update via buffer
        if aigie._buffer:
            await aigie._buffer.add(EventType.TRACE_UPDATE, update_data)

    async def handle_step_start(
        self,
        step_number: int,
        browser_state: dict[str, Any] | None = None,
    ) -> str:
        """
        Called when an agent step starts.

        Args:
            step_number: The step number
            browser_state: Current browser state (URL, title, etc.)

        Returns:
            The span ID for this step
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_steps = step_number
        span_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)

        self.step_map[step_number] = {
            "spanId": span_id,
            "startTime": start_time,
        }

        # Parent is previous step (for sequential flow)
        parent_id = self._current_step_span_id

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"step:{step_number}",
            "type": "chain",
            "input": {
                "step_number": step_number,
                "browser_state": browser_state,
            }
            if browser_state
            else {"step_number": step_number},
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "stepNumber": step_number,
                    "stepType": "browser_use_step",
                    "framework": "browser-use",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        # Update current step for parent tracking
        self._current_step_span_id = span_id

        # Send span via buffer
        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_step_end(
        self,
        step_number: int,
        action_taken: str | None = None,
        reasoning: str | None = None,
        is_done: bool = False,
    ) -> None:
        """
        Called when an agent step completes.

        Args:
            step_number: The step number
            action_taken: Description of action taken
            reasoning: The agent's reasoning
            is_done: Whether the task is complete
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        step_data = self.step_map.get(step_number)
        if not step_data:
            return

        end_time = datetime.now(timezone.utc)
        duration = (end_time - step_data["startTime"]).total_seconds()

        update_data = {
            "id": step_data["spanId"],
            "output": {
                "action": action_taken,
                "reasoning": reasoning[:500] if reasoning else None,
                "is_done": is_done,
            },
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.step_map[step_number]

    async def handle_step_error(self, step_number: int, error: str) -> None:
        """Called when a step encounters an error."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        step_data = self.step_map.get(step_number)
        if not step_data:
            return

        end_time = datetime.now(timezone.utc)
        duration = (end_time - step_data["startTime"]).total_seconds()

        update_data = {
            "id": step_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.step_map[step_number]

    async def handle_llm_start(
        self,
        call_id: str,
        model: str,
        messages: Any,
        parent_step: int | None = None,
    ) -> str:
        """
        Called when an LLM call starts.

        Args:
            call_id: Unique ID for this call
            model: Model name
            messages: Input messages
            parent_step: Parent step number

        Returns:
            The span ID for this LLM call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)

        # Get parent span ID from step
        parent_id = None
        if parent_step and parent_step in self.step_map:
            parent_id = self.step_map[parent_step]["spanId"]
        elif self._current_step_span_id:
            parent_id = self._current_step_span_id

        self.llm_call_map[call_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "parentSpanId": parent_id,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"llm:{model}",
            "type": "llm",
            "input": self._serialize_messages(messages),
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "model": model,
                    "framework": "browser-use",
                }
            ),
            "model": model,
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_llm_end(
        self,
        call_id: str,
        output: Any,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float = 0.0,
    ) -> None:
        """
        Called when an LLM call completes.

        Args:
            call_id: Unique ID for this call
            output: LLM output
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Cost of this call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        call_data = self.llm_call_map.get(call_id)
        if not call_data:
            return

        # Track totals
        self.total_tokens += input_tokens + output_tokens
        self.total_cost += cost

        end_time = datetime.now(timezone.utc)
        duration = (end_time - call_data["startTime"]).total_seconds()

        update_data = {
            "id": call_data["spanId"],
            "output": self._serialize_output(output),
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        }

        if cost > 0:
            update_data["total_cost"] = cost

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.llm_call_map[call_id]

    async def handle_llm_error(self, call_id: str, error: str) -> None:
        """Called when an LLM call fails."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        call_data = self.llm_call_map.get(call_id)
        if not call_data:
            return

        end_time = datetime.now(timezone.utc)
        duration = (end_time - call_data["startTime"]).total_seconds()

        update_data = {
            "id": call_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.llm_call_map[call_id]

    async def handle_action_start(
        self,
        action_type: str,
        action_id: str,
        params: dict[str, Any] | None = None,
        parent_step: int | None = None,
    ) -> str:
        """
        Called when a browser action starts.

        Args:
            action_type: Type of action (click, type, navigate, etc.)
            action_id: Unique ID for this action
            params: Action parameters (selector, text, url, etc.)
            parent_step: Parent step number

        Returns:
            The span ID for this action
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_actions += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)

        # Get parent span ID from step
        parent_id = None
        if parent_step and parent_step in self.step_map:
            parent_id = self.step_map[parent_step]["spanId"]
        elif self._current_step_span_id:
            parent_id = self._current_step_span_id

        self.action_map[action_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "parentSpanId": parent_id,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"action:{action_type}",
            "type": "tool",
            "input": params or {},
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "actionType": action_type,
                    "actionId": action_id,
                    "framework": "browser-use",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_action_end(
        self,
        action_id: str,
        success: bool,
        result: Any | None = None,
        screenshot_b64: str | None = None,
    ) -> None:
        """
        Called when a browser action completes.

        Args:
            action_id: Unique ID for this action
            success: Whether the action succeeded
            result: Action result
            screenshot_b64: Base64 encoded screenshot (optional)
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        action_data = self.action_map.get(action_id)
        if not action_data:
            return

        end_time = datetime.now(timezone.utc)
        duration = (end_time - action_data["startTime"]).total_seconds()

        update_data = {
            "id": action_data["spanId"],
            "output": {"success": success, "result": str(result)[:500] if result else None},
            "status": "success" if success else "failed",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        # Add screenshot to metadata if provided and enabled
        if screenshot_b64 and self.capture_screenshots:
            update_data["metadata"] = {"screenshot": screenshot_b64}

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.action_map[action_id]

    async def handle_action_error(self, action_id: str, error: str) -> None:
        """Called when a browser action fails."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        action_data = self.action_map.get(action_id)
        if not action_data:
            return

        end_time = datetime.now(timezone.utc)
        duration = (end_time - action_data["startTime"]).total_seconds()

        update_data = {
            "id": action_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.action_map[action_id]

    def _serialize_messages(self, messages: Any) -> Any:
        """Serialize messages for tracing."""
        if isinstance(messages, list):
            return [self._serialize_message(m) for m in messages]
        return self._serialize_message(messages)

    def _serialize_message(self, message: Any) -> Any:
        """Serialize a single message."""
        if isinstance(message, dict):
            return message
        if hasattr(message, "model_dump"):
            return message.model_dump()
        if hasattr(message, "dict"):
            return message.dict()
        if hasattr(message, "content"):
            return {
                "role": getattr(message, "role", "unknown"),
                "content": str(message.content)[:1000],
            }
        return str(message)[:1000]

    def _serialize_output(self, output: Any) -> Any:
        """Serialize output for tracing."""
        if isinstance(output, str):
            return output[:2000]
        if hasattr(output, "model_dump"):
            return output.model_dump()
        if hasattr(output, "dict"):
            return output.dict()
        return str(output)[:2000]

    def __repr__(self) -> str:
        return (
            f"BrowserUseHandler("
            f"trace_id={self.trace_id}, "
            f"steps={self.total_steps}, "
            f"tokens={self.total_tokens}, "
            f"cost=${self.total_cost:.4f})"
        )
