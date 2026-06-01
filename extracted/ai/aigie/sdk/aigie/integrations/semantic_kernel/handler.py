"""
Semantic Kernel callback handler for Aigie SDK.

Provides automatic tracing for Microsoft Semantic Kernel function
invocations, planners, and plugin executions.
"""

import uuid
from datetime import datetime
from typing import Any

from ...buffer import EventType
from ...context_manager import merge_metadata


class SemanticKernelHandler:
    """
    Semantic Kernel handler for Aigie tracing.

    Automatically traces Semantic Kernel executions including:
    - Kernel.invoke() function calls
    - Planner executions (Sequential, Action, Handlebars)
    - Plugin and function invocations
    - Azure OpenAI and OpenAI model usage
    - Token usage and costs

    Example:
        >>> from semantic_kernel import Kernel
        >>> from aigie.integrations.semantic_kernel import SemanticKernelHandler
        >>>
        >>> handler = SemanticKernelHandler(trace_name="enterprise-workflow")
        >>> kernel = Kernel()
        >>> # ... configure kernel with plugins
    """

    def __init__(
        self,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        capture_function_results: bool = True,
        capture_plan_details: bool = True,
    ):
        """
        Initialize Semantic Kernel handler.

        Args:
            trace_name: Name for the trace
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
            capture_function_results: Whether to capture function results
            capture_plan_details: Whether to capture planner details
        """
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id
        self.capture_function_results = capture_function_results
        self.capture_plan_details = capture_plan_details

        # State tracking
        self.trace_id: str | None = None
        self.invoke_span_id: str | None = None
        self.function_map: dict[str, dict[str, Any]] = {}  # invocation_id -> span data
        self.plan_span_id: str | None = None

        # Statistics
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.function_count = 0

        self._aigie = None

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    async def handle_invoke_start(
        self,
        function_name: str,
        plugin_name: str | None = None,
        arguments: dict[str, Any] | None = None,
        kernel_context: dict[str, Any] | None = None,
    ) -> str:
        """
        Called when Kernel.invoke() starts.

        Args:
            function_name: Name of the function being invoked
            plugin_name: Name of the plugin (if any)
            arguments: Function arguments
            kernel_context: Additional kernel context

        Returns:
            The invocation ID for tracking
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return ""

        # Generate trace ID if not set
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())

        self.function_count += 1

        full_name = f"{plugin_name}.{function_name}" if plugin_name else function_name
        trace_name = self.trace_name or f"SK: {full_name}"

        # Build metadata
        trace_metadata = merge_metadata(
            {
                **self.metadata,
                "function_name": function_name,
                "plugin_name": plugin_name,
                "framework": "semantic_kernel",
            }
        )

        # Create trace
        trace_data = {
            "id": self.trace_id,
            "name": trace_name,
            "type": "chain",
            "input": {
                "function": full_name,
                "arguments": arguments or {},
            },
            "status": "pending",
            "tags": [*self.tags, "semantic_kernel"],
            "metadata": merge_metadata(trace_metadata),
            "start_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if self.user_id:
            trace_data["user_id"] = self.user_id
        if self.session_id:
            trace_data["session_id"] = self.session_id

        if aigie._buffer:
            await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)

        # Create invoke span
        self.invoke_span_id = str(uuid.uuid4())
        span_data = {
            "id": self.invoke_span_id,
            "trace_id": self.trace_id,
            "name": f"invoke:{full_name}",
            "type": "chain",
            "input": {
                "function": full_name,
                "arguments": arguments or {},
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(trace_metadata),
            "start_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return self.invoke_span_id

    async def handle_invoke_end(
        self,
        result: Any,
        usage: dict[str, int] | None = None,
        error: str | None = None,
    ) -> None:
        """
        Called when Kernel.invoke() completes.

        Args:
            result: The function result
            usage: Token usage information
            error: Error message if invocation failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        end_time = datetime.now()
        success = error is None

        # Process usage
        if usage:
            self.total_input_tokens += usage.get("prompt_tokens", usage.get("input_tokens", 0))
            self.total_output_tokens += usage.get(
                "completion_tokens", usage.get("output_tokens", 0)
            )

        # Serialize result
        output_data = {}
        if result and self.capture_function_results:
            if isinstance(result, str):
                output_data["result"] = result[:2000]
            elif hasattr(result, "value"):
                output_data["result"] = str(result.value)[:2000]
            else:
                output_data["result"] = str(result)[:2000]

        output_data["function_count"] = self.function_count
        output_data["total_tokens"] = self.total_input_tokens + self.total_output_tokens

        # Update invoke span
        if self.invoke_span_id:
            span_update = {
                "id": self.invoke_span_id,
                "status": "success" if success else "failed",
                "output": output_data,
                "end_time": end_time.isoformat(),
                "prompt_tokens": self.total_input_tokens,
                "completion_tokens": self.total_output_tokens,
                "total_tokens": self.total_input_tokens + self.total_output_tokens,
            }

            if error:
                span_update["error"] = error
                span_update["error_message"] = error

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_UPDATE, span_update)

        # Update trace
        trace_update = {
            "id": self.trace_id,
            "status": "success" if success else "failed",
            "output": output_data,
            "end_time": end_time.isoformat(),
        }

        if error:
            trace_update["error"] = error
            trace_update["error_message"] = error

        if aigie._buffer:
            await aigie._buffer.add(EventType.TRACE_UPDATE, trace_update)

    async def handle_function_start(
        self,
        function_name: str,
        plugin_name: str | None = None,
        arguments: dict[str, Any] | None = None,
    ) -> str:
        """
        Called when a kernel function starts executing.

        Args:
            function_name: Function name
            plugin_name: Plugin name
            arguments: Function arguments

        Returns:
            Span ID for this function
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        full_name = f"{plugin_name}.{function_name}" if plugin_name else function_name

        self.function_map[span_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "functionName": full_name,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self.plan_span_id or self.invoke_span_id,
            "name": f"function:{full_name}",
            "type": "tool",
            "input": {
                "function": full_name,
                "arguments": arguments or {},
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "function_name": function_name,
                    "plugin_name": plugin_name,
                    "framework": "semantic_kernel",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_function_end(
        self,
        span_id: str,
        result: Any,
        error: str | None = None,
    ) -> None:
        """
        Called when a kernel function completes.

        Args:
            span_id: Span ID from handle_function_start
            result: Function result
            error: Error message if function failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        func_data = self.function_map.get(span_id)
        if not func_data:
            return

        end_time = datetime.now()
        duration = (end_time - func_data["startTime"]).total_seconds()
        success = error is None

        output_data = {}
        if result and self.capture_function_results:
            if isinstance(result, str):
                output_data["result"] = result[:1000]
            elif hasattr(result, "value"):
                output_data["result"] = str(result.value)[:1000]
            else:
                output_data["result"] = str(result)[:1000]

        update_data = {
            "id": span_id,
            "output": output_data,
            "status": "success" if success else "failed",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if error:
            update_data["error"] = error
            update_data["error_message"] = error

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.function_map[span_id]

    async def handle_plan_start(
        self,
        planner_type: str,
        goal: str,
        available_functions: list[str] | None = None,
    ) -> str:
        """
        Called when a planner starts creating a plan.

        Args:
            planner_type: Type of planner (Sequential, Action, Handlebars)
            goal: The goal to plan for
            available_functions: List of available functions

        Returns:
            Span ID for the plan
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.plan_span_id = str(uuid.uuid4())
        start_time = datetime.now()

        input_data = {
            "planner_type": planner_type,
            "goal": goal[:1000],
        }
        if available_functions and self.capture_plan_details:
            input_data["available_functions"] = available_functions[:20]

        span_data = {
            "id": self.plan_span_id,
            "trace_id": self.trace_id,
            "parent_id": self.invoke_span_id,
            "name": f"planner:{planner_type}",
            "type": "chain",
            "input": input_data,
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "planner_type": planner_type,
                    "framework": "semantic_kernel",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return self.plan_span_id

    async def handle_plan_end(
        self,
        plan: Any,
        error: str | None = None,
    ) -> None:
        """
        Called when a planner finishes creating a plan.

        Args:
            plan: The generated plan
            error: Error message if planning failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.plan_span_id:
            return

        end_time = datetime.now()
        success = error is None

        output_data = {}
        if plan and self.capture_plan_details:
            if hasattr(plan, "generated_plan"):
                output_data["plan"] = str(plan.generated_plan)[:2000]
            elif hasattr(plan, "description"):
                output_data["plan"] = plan.description[:2000]
            else:
                output_data["plan"] = str(plan)[:2000]

        update_data = {
            "id": self.plan_span_id,
            "output": output_data,
            "status": "success" if success else "failed",
            "end_time": end_time.isoformat(),
        }

        if error:
            update_data["error"] = error
            update_data["error_message"] = error

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

    async def handle_prompt_render(
        self,
        template_name: str,
        rendered_prompt: str,
        variables: dict[str, Any] | None = None,
    ) -> str:
        """
        Called when a prompt template is rendered.

        Args:
            template_name: Name of the template
            rendered_prompt: The rendered prompt text
            variables: Variables used in rendering

        Returns:
            Span ID for the render operation
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self.invoke_span_id,
            "name": f"prompt:{template_name}",
            "type": "chain",
            "input": {
                "template_name": template_name,
                "variables": variables or {},
            },
            "output": {
                "rendered_prompt": rendered_prompt[:2000],
            },
            "status": "success",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "template_name": template_name,
                    "framework": "semantic_kernel",
                }
            ),
            "start_time": datetime.now().isoformat(),
            "end_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    def __repr__(self) -> str:
        return (
            f"SemanticKernelHandler("
            f"trace_id={self.trace_id}, "
            f"functions={self.function_count}, "
            f"tokens={self.total_input_tokens + self.total_output_tokens})"
        )
