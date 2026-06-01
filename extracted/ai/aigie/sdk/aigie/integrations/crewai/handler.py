"""
CrewAI callback handler for Aigie SDK.

Provides automatic tracing for CrewAI crew executions,
including agents, tasks, tool calls, and delegations.
"""

import uuid
from datetime import datetime
from typing import Any

from ...buffer import EventType
from ...context_manager import merge_metadata


class CrewAIHandler:
    """
    CrewAI callback handler for Aigie.

    Automatically traces CrewAI workflow executions including:
    - Crew kickoff and completion
    - Agent step-by-step execution
    - Task execution with context
    - LLM calls with tokens/cost
    - Tool invocations
    - Agent-to-agent delegations

    Example:
        >>> from crewai import Crew, Agent, Task
        >>> from aigie.integrations.crewai import CrewAIHandler
        >>>
        >>> handler = CrewAIHandler(
        ...     trace_name='research-crew',
        ...     metadata={'project': 'analysis'}
        ... )
        >>>
        >>> crew = Crew(agents=[...], tasks=[...])
        >>> result = crew.kickoff()
    """

    def __init__(
        self,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        capture_thoughts: bool = True,
        capture_tool_results: bool = True,
    ):
        """
        Initialize CrewAI handler.

        Args:
            trace_name: Name for the trace
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
            capture_thoughts: Whether to capture agent reasoning
            capture_tool_results: Whether to capture tool results
        """
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id
        self.capture_thoughts = capture_thoughts
        self.capture_tool_results = capture_tool_results

        # State tracking
        self.trace_id: str | None = None
        self.crew_span_id: str | None = None
        self.task_map: dict[str, dict[str, Any]] = {}  # task_id -> {spanId, startTime}
        self.agent_map: dict[
            str, dict[str, Any]
        ] = {}  # agent_role -> {spanId, startTime, taskSpanId}
        self.step_map: dict[
            str, dict[str, Any]
        ] = {}  # step_id -> {spanId, startTime, parentSpanId}
        self.llm_call_map: dict[
            str, dict[str, Any]
        ] = {}  # call_id -> {spanId, startTime, parentSpanId}
        self.tool_call_map: dict[
            str, dict[str, Any]
        ] = {}  # tool_id -> {spanId, startTime, parentSpanId}
        self.delegation_map: dict[str, dict[str, Any]] = {}  # delegation_id -> {spanId, startTime}

        # Current context for parent relationships
        self._current_task_span_id: str | None = None
        self._current_agent_span_id: str | None = None
        self._current_step_span_id: str | None = None
        self._aigie = None
        self._trace_context: Any | None = None

        # Statistics
        self.total_tasks = 0
        self.total_steps = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.total_tool_calls = 0
        self.total_delegations = 0

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

    async def handle_crew_start(
        self,
        crew_name: str,
        agents: list[dict[str, Any]],
        tasks: list[dict[str, Any]],
        process_type: str = "sequential",
        verbose: bool = False,
    ) -> None:
        """
        Called when a crew starts execution.

        Args:
            crew_name: Name of the crew
            agents: List of agent configurations
            tasks: List of task configurations
            process_type: Type of process (sequential, hierarchical)
            verbose: Whether verbose mode is enabled
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
        trace_name = self.trace_name or f"Crew: {crew_name}"

        # Extract agent roles and tools for metadata
        agent_roles = [a.get("role", "unknown") for a in agents]

        # Capture available tools from agent configs
        available_tools = []
        for agent_cfg in agents:
            agent_tools = agent_cfg.get("tools", [])
            for tool in agent_tools:
                tool_def = {}
                if isinstance(tool, dict):
                    tool_def = tool
                elif isinstance(tool, str):
                    tool_def = {"name": tool}
                else:
                    tool_name = getattr(tool, "name", None) or getattr(tool, "__name__", str(tool))
                    tool_def = {"name": tool_name}
                    tool_desc = getattr(tool, "description", None)
                    if tool_desc:
                        tool_def["description"] = tool_desc
                if tool_def and tool_def not in available_tools:
                    available_tools.append(tool_def)

        # Build metadata
        trace_metadata = merge_metadata(
            {
                **self.metadata,
                "crew_name": crew_name,
                "process_type": process_type,
                "agent_count": len(agents),
                "task_count": len(tasks),
                "agent_roles": agent_roles,
                "framework": "crewai",
                "verbose": verbose,
            }
        )

        if available_tools:
            trace_metadata["available_tools"] = available_tools

        # Only create trace if we don't have a trace context
        if not self._trace_context:
            trace_data = {
                "id": self.trace_id,
                "name": trace_name,
                "type": "chain",
                "input": {
                    "crew_name": crew_name,
                    "agents": agent_roles,
                    "task_count": len(tasks),
                },
                "status": "pending",
                "tags": [*self.tags, "crewai", process_type],
                "metadata": merge_metadata(trace_metadata),
                "start_time": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat(),
            }

            if self.user_id:
                trace_data["user_id"] = self.user_id
            if self.session_id:
                trace_data["session_id"] = self.session_id

            # Send trace via buffer
            if aigie._buffer:
                await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)

        # Create crew span
        self.crew_span_id = str(uuid.uuid4())
        crew_span_data = {
            "id": self.crew_span_id,
            "trace_id": self.trace_id,
            "name": f"crew:{crew_name}",
            "type": "chain",
            "input": {
                "process_type": process_type,
                "agents": agents,
                "tasks": [t.get("description", "")[:200] for t in tasks],
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": trace_metadata,
            "start_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, crew_span_data)

    async def handle_crew_end(
        self,
        success: bool,
        result: Any | None = None,
        error: str | None = None,
    ) -> None:
        """
        Called when a crew completes execution.

        Args:
            success: Whether the crew succeeded
            result: The crew result
            error: Error message if failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        end_time = datetime.now()

        # Update crew span
        if self.crew_span_id:
            crew_update = {
                "id": self.crew_span_id,
                "status": "success" if success else "failed",
                "output": {
                    "success": success,
                    "total_tasks": self.total_tasks,
                    "total_steps": self.total_steps,
                    "total_tokens": self.total_tokens,
                    "total_cost": self.total_cost,
                    "total_tool_calls": self.total_tool_calls,
                    "total_delegations": self.total_delegations,
                },
                "end_time": end_time.isoformat(),
            }
            if result:
                crew_update["output"]["result"] = str(result)[:1000]
            if error:
                crew_update["error"] = error
                crew_update["error_message"] = error

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_UPDATE, crew_update)

        # Update trace
        update_data = {
            "id": self.trace_id,
            "status": "success" if success else "failed",
            "output": {
                "success": success,
                "total_tasks": self.total_tasks,
                "total_tokens": self.total_tokens,
                "total_cost": self.total_cost,
            },
            "end_time": end_time.isoformat(),
        }

        if result:
            update_data["output"]["result"] = str(result)[:1000]
        if error:
            update_data["error"] = error
            update_data["error_message"] = error

        if aigie._buffer:
            await aigie._buffer.add(EventType.TRACE_UPDATE, update_data)

    async def handle_task_start(
        self,
        task_id: str,
        description: str,
        agent_role: str,
        expected_output: str | None = None,
        context: list[str] | None = None,
    ) -> str:
        """
        Called when a task starts execution.

        Args:
            task_id: Unique task identifier
            description: Task description
            agent_role: Role of the assigned agent
            expected_output: Expected output description
            context: Context from previous tasks

        Returns:
            The span ID for this task
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_tasks += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        self.task_map[task_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "agentRole": agent_role,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self.crew_span_id,
            "name": f"task:{description[:50]}",
            "type": "chain",
            "input": {
                "description": description,
                "agent_role": agent_role,
                "expected_output": expected_output,
                "context_count": len(context) if context else 0,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "taskId": task_id,
                    "taskType": "crewai_task",
                    "assignedAgent": agent_role,
                    "framework": "crewai",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        self._current_task_span_id = span_id

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_task_end(
        self,
        task_id: str,
        output: str | None = None,
        raw_output: Any | None = None,
    ) -> None:
        """
        Called when a task completes.

        Args:
            task_id: Unique task identifier
            output: Task output string
            raw_output: Raw task output object
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        task_data = self.task_map.get(task_id)
        if not task_data:
            return

        end_time = datetime.now()
        duration = (end_time - task_data["startTime"]).total_seconds()

        # Build output: prefer string output, fall back to raw_output
        task_output = output[:1000] if output else None
        if not task_output and raw_output is not None:
            task_output = str(raw_output)[:1000]

        update_data = {
            "id": task_data["spanId"],
            "output": {
                "output": task_output,
            },
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.task_map[task_id]

    async def handle_task_error(self, task_id: str, error: str) -> None:
        """Called when a task encounters an error."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        task_data = self.task_map.get(task_id)
        if not task_data:
            return

        end_time = datetime.now()
        duration = (end_time - task_data["startTime"]).total_seconds()

        update_data = {
            "id": task_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.task_map[task_id]

    async def handle_agent_step_start(
        self,
        step_id: str,
        agent_role: str,
        step_number: int,
        task_id: str | None = None,
    ) -> str:
        """
        Called when an agent step starts.

        Args:
            step_id: Unique step identifier
            agent_role: Role of the agent
            step_number: Step number within the task
            task_id: Parent task ID

        Returns:
            The span ID for this step
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_steps += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span ID
        parent_id = None
        if task_id and task_id in self.task_map:
            parent_id = self.task_map[task_id]["spanId"]
        elif self._current_task_span_id:
            parent_id = self._current_task_span_id

        self.step_map[step_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "parentSpanId": parent_id,
            "agentRole": agent_role,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"agent:{agent_role}:step_{step_number}",
            "type": "chain",
            "input": {
                "step_number": step_number,
                "agent_role": agent_role,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "stepId": step_id,
                    "stepNumber": step_number,
                    "agentRole": agent_role,
                    "stepType": "crewai_agent_step",
                    "framework": "crewai",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        self._current_step_span_id = span_id
        self._current_agent_span_id = span_id

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_agent_step_end(
        self,
        step_id: str,
        thought: str | None = None,
        action: str | None = None,
        action_input: Any | None = None,
        observation: str | None = None,
        final_answer: str | None = None,
    ) -> None:
        """
        Called when an agent step completes.

        Args:
            step_id: Unique step identifier
            thought: Agent's reasoning
            action: Action taken
            action_input: Input to the action
            observation: Result of the action
            final_answer: Final answer if this is the last step
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        step_data = self.step_map.get(step_id)
        if not step_data:
            return

        end_time = datetime.now()
        duration = (end_time - step_data["startTime"]).total_seconds()

        output = {}
        if self.capture_thoughts and thought:
            output["thought"] = thought[:500]
        if action:
            output["action"] = action
        if action_input:
            output["action_input"] = str(action_input)[:300]
        if observation:
            output["observation"] = observation[:500]
        if final_answer:
            output["final_answer"] = final_answer[:1000]

        update_data = {
            "id": step_data["spanId"],
            "output": output,
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.step_map[step_id]

    async def handle_agent_step_error(self, step_id: str, error: str) -> None:
        """Called when an agent step fails."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        step_data = self.step_map.get(step_id)
        if not step_data:
            return

        end_time = datetime.now()
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

        del self.step_map[step_id]

    async def handle_llm_start(
        self,
        call_id: str,
        model: str,
        messages: Any,
        agent_role: str | None = None,
    ) -> str:
        """
        Called when an LLM call starts.

        Args:
            call_id: Unique ID for this call
            model: Model name
            messages: Input messages
            agent_role: Role of the calling agent

        Returns:
            The span ID for this LLM call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span ID
        parent_id = self._current_step_span_id or self._current_task_span_id

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
                    "agentRole": agent_role,
                    "framework": "crewai",
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
        finish_reason: str | None = None,
    ) -> None:
        """
        Called when an LLM call completes.

        Args:
            call_id: Unique ID for this call
            output: LLM output
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Cost of this call
            finish_reason: Reason the LLM stopped generating
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

        end_time = datetime.now()
        duration = (end_time - call_data["startTime"]).total_seconds()

        update_metadata = {}
        if finish_reason:
            update_metadata["finish_reason"] = finish_reason

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

        if update_metadata:
            update_data["metadata"] = update_metadata

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

        end_time = datetime.now()
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

    async def handle_tool_start(
        self,
        tool_id: str,
        tool_name: str,
        tool_input: Any,
        agent_role: str | None = None,
    ) -> str:
        """
        Called when a tool invocation starts.

        Args:
            tool_id: Unique ID for this tool call
            tool_name: Name of the tool
            tool_input: Input to the tool
            agent_role: Role of the calling agent

        Returns:
            The span ID for this tool call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_tool_calls += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span ID
        parent_id = self._current_step_span_id or self._current_task_span_id

        self.tool_call_map[tool_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "parentSpanId": parent_id,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"tool:{tool_name}",
            "type": "tool",
            "input": self._serialize_tool_input(tool_input),
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "toolName": tool_name,
                    "toolId": tool_id,
                    "agentRole": agent_role,
                    "framework": "crewai",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        # Add tool_category hint for component registry classification
        try:
            from ...tool_category import infer_tool_category

            category = infer_tool_category(tool_name, None)
            if category:
                span_data["metadata"]["tool_category"] = category
        except ImportError:
            pass

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_tool_end(
        self,
        tool_id: str,
        output: Any,
        success: bool = True,
    ) -> None:
        """
        Called when a tool invocation completes.

        Args:
            tool_id: Unique ID for this tool call
            output: Tool output
            success: Whether the tool succeeded
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        tool_data = self.tool_call_map.get(tool_id)
        if not tool_data:
            return

        end_time = datetime.now()
        duration = (end_time - tool_data["startTime"]).total_seconds()

        output_data = {}
        if self.capture_tool_results:
            output_data["result"] = str(output)[:1000] if output else None
        output_data["success"] = success

        update_data = {
            "id": tool_data["spanId"],
            "output": output_data,
            "status": "success" if success else "failed",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.tool_call_map[tool_id]

    async def handle_tool_error(self, tool_id: str, error: str) -> None:
        """Called when a tool invocation fails."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        tool_data = self.tool_call_map.get(tool_id)
        if not tool_data:
            return

        end_time = datetime.now()
        duration = (end_time - tool_data["startTime"]).total_seconds()

        update_data = {
            "id": tool_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.tool_call_map[tool_id]

    async def handle_delegation_start(
        self,
        delegation_id: str,
        from_agent: str,
        to_agent: str,
        task_description: str,
        reason: str | None = None,
    ) -> str:
        """
        Called when an agent delegates to another agent.

        Args:
            delegation_id: Unique delegation identifier
            from_agent: Role of delegating agent
            to_agent: Role of receiving agent
            task_description: Description of delegated task
            reason: Reason for delegation

        Returns:
            The span ID for this delegation
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_delegations += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span ID
        parent_id = self._current_step_span_id or self._current_task_span_id

        self.delegation_map[delegation_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "fromAgent": from_agent,
            "toAgent": to_agent,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"delegation:{from_agent}->{to_agent}",
            "type": "chain",
            "input": {
                "from_agent": from_agent,
                "to_agent": to_agent,
                "task": task_description[:500],
                "reason": reason,
            },
            "status": "pending",
            "tags": [*self.tags, "delegation"],
            "metadata": merge_metadata(
                {
                    "delegationId": delegation_id,
                    "delegationType": "crewai_delegation",
                    "fromAgent": from_agent,
                    "toAgent": to_agent,
                    "framework": "crewai",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_delegation_end(
        self,
        delegation_id: str,
        result: str | None = None,
        success: bool = True,
    ) -> None:
        """
        Called when a delegation completes.

        Args:
            delegation_id: Unique delegation identifier
            result: Result from the delegated task
            success: Whether the delegation succeeded
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        delegation_data = self.delegation_map.get(delegation_id)
        if not delegation_data:
            return

        end_time = datetime.now()
        duration = (end_time - delegation_data["startTime"]).total_seconds()

        update_data = {
            "id": delegation_data["spanId"],
            "output": {
                "result": result[:1000] if result else None,
                "success": success,
            },
            "status": "success" if success else "failed",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.delegation_map[delegation_id]

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

    def _serialize_tool_input(self, tool_input: Any) -> Any:
        """Serialize tool input for tracing."""
        if isinstance(tool_input, dict):
            return {k: str(v)[:500] for k, v in tool_input.items()}
        if isinstance(tool_input, str):
            return tool_input[:1000]
        return str(tool_input)[:1000]

    def __repr__(self) -> str:
        return (
            f"CrewAIHandler("
            f"trace_id={self.trace_id}, "
            f"tasks={self.total_tasks}, "
            f"steps={self.total_steps}, "
            f"tokens={self.total_tokens}, "
            f"cost=${self.total_cost:.4f})"
        )
