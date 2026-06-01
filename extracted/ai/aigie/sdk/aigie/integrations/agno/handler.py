"""
Agno hook handler for Aigie SDK.

Registers pre_hooks and post_hooks on Agno Agent/Team instances to
automatically trace agent invocations, tool calls, and multi-agent teams.

Includes comprehensive error detection and drift monitoring.
"""

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from .error_detection import (
    DetectedError,
    ErrorDetector,
)
from .drift_detection import DriftDetector
from ...buffer import EventType
from ...context_manager import merge_metadata
from .config import AgnoConfig
from .cost_tracking import calculate_agno_cost

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    """Get current time in UTC with timezone info."""
    return datetime.now(timezone.utc)


def _utc_isoformat() -> str:
    """Get current UTC time as ISO format string."""
    return datetime.now(timezone.utc).isoformat()


if TYPE_CHECKING:
    try:
        from agno.agent import Agent
        from agno.team import Team
    except ImportError:
        pass


class AgnoHandler:
    """
    Agno hook handler for Aigie tracing.

    Registers synchronous callables into Agent.pre_hooks and Agent.post_hooks
    (and Team equivalents) to automatically trace:
    - Agent invocations (pre_hook → post_hook)
    - Tool calls (tool_hooks)
    - Team invocations (pre_hook → post_hook on Team)

    The hook callables receive a RunContext argument from Agno. Since the
    Aigie buffer API is async, all buffer operations are scheduled via
    _schedule_async().

    Example:
        >>> from agno.agent import Agent
        >>> from aigie.integrations.agno import AgnoHandler
        >>>
        >>> handler = AgnoHandler()
        >>> agent = Agent(model=..., tools=[...])
        >>> handler.register(agent)
        >>> result = agent.run("What is the capital of France?")
    """

    def __init__(
        self,
        config: AgnoConfig | None = None,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        """
        Initialize Agno handler.

        Args:
            config: Configuration for tracing behavior
            trace_name: Name for the trace (default: agent name)
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
        """
        self.config = config or AgnoConfig.from_env()
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id

        # State tracking
        self.trace_id: str | None = None
        self.agent_span_id: str | None = None
        self.tool_span_map: dict[str, dict[str, Any]] = {}  # tool_name -> {spanId, startTime}

        # Current context
        self._current_parent_span_id: str | None = None
        self._aigie = None

        # Statistics
        self._total_tool_calls = 0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_cost = 0.0

        # Error tracking
        self._has_errors = False
        self._error_messages: list[str] = []

        # Error detection and monitoring
        self._error_detector = ErrorDetector()
        self._drift_detector = DriftDetector()
        self._detected_errors: list[DetectedError] = []
        self._invocation_start_time: datetime | None = None

        # Agent span data stored at pre_hook, completed at post_hook
        self._agent_span_data: dict[str, Any] = {}

        # Real-time remediation engine
        self._remediation_engine = None
        self._intervention_dispatcher = None
        if self.config.enable_realtime_remediation:
            aigie = self._get_aigie()
            if aigie and aigie._initialized:
                api_url = getattr(aigie, "_api_url", None) or getattr(aigie, "api_url", None)
                api_key = getattr(aigie, "_api_key", None) or getattr(aigie, "api_key", None)
                if api_url:
                    from ...realtime.remediation_engine import RemediationEngine

                    self._remediation_engine = RemediationEngine(
                        api_url=api_url,
                        api_key=api_key or "",
                        query_timeout=self.config.remediation_query_timeout,
                    )
                self._intervention_dispatcher = getattr(aigie, "_intervention_dispatcher", None)

    def _get_aigie(self) -> Any | None:
        """Lazy load Aigie client."""
        if self._aigie is None:
            try:
                from ...client import get_aigie

                self._aigie = get_aigie()
            except Exception as e:
                logger.warning(f"[AIGIE] Could not get aigie client: {e}")
        return self._aigie

    def _schedule_async(self, coro: Any) -> None:
        """Schedule an async coroutine from a synchronous hook callback without blocking the agent."""

        async def _safe_run() -> None:
            try:
                await coro
            except Exception as e:
                # Tracing must never raise into the agent.
                logger.debug(f"Background tracing task failed (non-fatal): {e}")

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(_safe_run())
        except RuntimeError:
            # No running loop — run in a daemon thread.
            import threading

            threading.Thread(target=asyncio.run, args=(_safe_run(),), daemon=True).start()

    def register(self, target: Any) -> None:
        """
        Register hooks on an Agno Agent or Team.

        Appends pre/post hook callables to the target's hook lists.
        Avoids registering the same handler twice.

        Args:
            target: An agno Agent or Team instance
        """
        if not self.config.enabled:
            return

        target_type = type(target).__name__

        try:
            # Determine hook attributes based on target type
            is_team = target_type == "Team" or hasattr(target, "members")

            if is_team and self.config.trace_teams:
                self._register_on_target(target, hook_type="team")
            elif not is_team and self.config.trace_agents:
                self._register_on_target(target, hook_type="agent")

        except Exception as e:
            logger.warning(f"[AIGIE] Failed to register hooks on {target_type}: {e}")

    def _register_on_target(self, target: Any, hook_type: str = "agent") -> None:
        """Register pre/post hook callables on a target, avoiding duplicates."""
        # Ensure hook lists exist
        if not hasattr(target, "pre_hooks") or target.pre_hooks is None:
            target.pre_hooks = []
        if not hasattr(target, "post_hooks") or target.post_hooks is None:
            target.post_hooks = []

        # Check for existing registration (avoid double-registering)
        for hook in target.pre_hooks:
            if getattr(hook, "_aigie_handler", None) is self:
                logger.debug(f"[AIGIE] Handler already registered on {hook_type}")
                return

        # Build bound hooks
        if hook_type == "team":
            pre_hook = self._make_team_pre_hook()
            post_hook = self._make_team_post_hook()
        else:
            pre_hook = self._make_agent_pre_hook()
            post_hook = self._make_agent_post_hook()

        # Tag hooks so we can detect double registration
        pre_hook._aigie_handler = self
        post_hook._aigie_handler = self

        target.pre_hooks.append(pre_hook)
        target.post_hooks.append(post_hook)

        # Register tool hooks if configured
        if self.config.trace_tools:
            if not hasattr(target, "tool_hooks") or target.tool_hooks is None:
                target.tool_hooks = []
            tool_pre = self._make_tool_pre_hook()
            tool_post = self._make_tool_post_hook()
            tool_pre._aigie_handler = self
            tool_post._aigie_handler = self
            # Agno iterates tool_hooks as a flat list of callables
            target.tool_hooks.append(tool_pre)
            target.tool_hooks.append(tool_post)

        logger.debug(f"[AIGIE] Registered hooks on {hook_type}")

    # -----------------------------------------------------------------------
    # Hook factory methods — return synchronous callables for agno hook lists
    # -----------------------------------------------------------------------

    def _make_agent_pre_hook(self):
        """Return a synchronous pre-hook callable for agent invocations."""
        handler = self

        def _on_agent_pre_hook(run_context: Any) -> None:
            handler._schedule_async(handler._async_on_agent_pre_hook(run_context))

        return _on_agent_pre_hook

    def _make_agent_post_hook(self):
        """Return a synchronous post-hook callable for agent invocations."""
        handler = self

        def _on_agent_post_hook(run_context: Any) -> None:
            handler._schedule_async(handler._async_on_agent_post_hook(run_context))

        return _on_agent_post_hook

    def _make_team_pre_hook(self):
        """Return a synchronous pre-hook callable for team invocations."""
        handler = self

        def _on_team_pre_hook(run_context: Any) -> None:
            handler._schedule_async(handler._async_on_team_pre_hook(run_context))

        return _on_team_pre_hook

    def _make_team_post_hook(self):
        """Return a synchronous post-hook callable for team invocations."""
        handler = self

        def _on_team_post_hook(run_context: Any) -> None:
            handler._schedule_async(handler._async_on_team_post_hook(run_context))

        return _on_team_post_hook

    def _make_tool_pre_hook(self):
        """Return a synchronous pre-hook callable for tool calls."""
        handler = self

        def _on_tool_pre_hook(run_context: Any) -> None:
            handler._schedule_async(handler._async_on_tool_pre_hook(run_context))

        return _on_tool_pre_hook

    def _make_tool_post_hook(self):
        """Return a synchronous post-hook callable for tool calls."""
        handler = self

        def _on_tool_post_hook(run_context: Any) -> None:
            handler._schedule_async(handler._async_on_tool_post_hook(run_context))

        return _on_tool_post_hook

    # -----------------------------------------------------------------------
    # Async implementation helpers
    # -----------------------------------------------------------------------

    def _extract_agent_name(self, run_context: Any) -> str:
        """Extract agent name from RunContext."""
        agent = getattr(run_context, "agent", None)
        if agent is not None:
            name = getattr(agent, "name", None)
            if name:
                return str(name)
        return "Agno Agent"

    def _extract_model_id(self, run_context: Any) -> str | None:
        """Extract model ID from RunContext or agent."""
        # Check run_response first
        run_response = getattr(run_context, "run_response", None)
        if run_response is not None:
            model = getattr(run_response, "model", None)
            if model:
                return str(model)

        # Check agent
        agent = getattr(run_context, "agent", None)
        if agent is not None:
            model = getattr(agent, "model", None)
            if model is not None:
                model_id = getattr(model, "id", None) or getattr(model, "model_id", None)
                if model_id:
                    return str(model_id)
                return str(model)
        return None

    def _extract_tokens(self, run_context: Any) -> dict[str, int]:
        """Extract token counts from RunContext.run_response.metrics."""
        tokens = {"input_tokens": 0, "output_tokens": 0}

        run_response = getattr(run_context, "run_response", None)
        if run_response is None:
            return tokens

        metrics = getattr(run_response, "metrics", None)
        if isinstance(metrics, dict):
            tokens["input_tokens"] = metrics.get("input_tokens", 0) or 0
            tokens["output_tokens"] = metrics.get("output_tokens", 0) or 0
        elif metrics is not None:
            tokens["input_tokens"] = getattr(metrics, "input_tokens", 0) or 0
            tokens["output_tokens"] = getattr(metrics, "output_tokens", 0) or 0

        return tokens

    def _extract_content(self, run_context: Any) -> str | None:
        """Extract output content from RunContext.run_response."""
        run_response = getattr(run_context, "run_response", None)
        if run_response is None:
            return None

        content = getattr(run_response, "content", None)
        if content is not None:
            return str(content)[: self.config.max_content_length]
        return None

    async def _async_on_agent_pre_hook(self, run_context: Any) -> None:
        """Handle agent pre-hook — create trace and agent span."""
        if not self.config.enabled or not self.config.trace_agents:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            # Generate new trace ID for this invocation
            self.trace_id = str(uuid.uuid4())

            # Reset invocation state
            self._has_errors = False
            self._error_messages = []
            self._total_tool_calls = 0
            self._total_input_tokens = 0
            self._total_output_tokens = 0
            self._total_cost = 0.0
            self.agent_span_id = None
            self.tool_span_map.clear()
            self._current_parent_span_id = None

            # Reset error/drift detection
            self._error_detector = ErrorDetector()
            self._drift_detector = DriftDetector()
            self._detected_errors = []
            self._invocation_start_time = _utc_now()

            agent_name = self._extract_agent_name(run_context)
            trace_name = self.trace_name or agent_name

            # Capture instructions for drift detection
            agent = getattr(run_context, "agent", None)
            if agent is not None:
                instructions = getattr(agent, "instructions", None)
                if instructions:
                    self._drift_detector.capture_system_prompt(str(instructions))
                model_id = self._extract_model_id(run_context)
                if model_id:
                    self._drift_detector.plan.model = model_id

            # Capture available tools from agent definition
            available_tools = []
            try:
                tools = getattr(agent, "tools", None)
                if tools:
                    for tool in tools:
                        tool_name = getattr(tool, "name", getattr(tool, "__name__", ""))
                        if tool_name:
                            tool_def = {"name": tool_name, "type": "tool"}
                            desc = getattr(tool, "description", None)
                            if desc:
                                tool_def["description"] = str(desc)[:500]
                            available_tools.append(tool_def)
            except Exception:
                pass

            # Create trace
            trace_data = {
                "id": self.trace_id,
                "name": trace_name,
                "metadata": merge_metadata(
                    {
                        "framework": "agno",
                        "agent_name": agent_name,
                        **self.metadata,
                    }
                ),
                "tags": self.tags,
                "start_time": self._invocation_start_time.isoformat(),
            }

            if self.user_id:
                trace_data["user_id"] = self.user_id
            if self.session_id:
                trace_data["session_id"] = self.session_id

            if aigie._buffer:
                await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)
                await aigie._buffer.flush()

            # Create agent span (parent for tool child spans)
            self.agent_span_id = str(uuid.uuid4())

            agent_span_metadata: dict = merge_metadata(
                {
                    "framework": "agno",
                    "agent_name": agent_name,
                }
            )
            if available_tools:
                agent_span_metadata["available_tools"] = available_tools

            agent_span = {
                "id": self.agent_span_id,
                "trace_id": self.trace_id,
                "parent_id": None,
                "name": f"Agent: {agent_name}",
                "type": "agent",
                "start_time": self._invocation_start_time.isoformat(),
                "metadata": merge_metadata(agent_span_metadata),
                "tags": self.tags,
                "depth": 0,
            }

            if self.user_id:
                agent_span["user_id"] = self.user_id
            if self.session_id:
                agent_span["session_id"] = self.session_id

            # Capture input
            if self.config.capture_inputs:
                messages = getattr(run_context, "messages", None)
                if messages:
                    input_repr = str(messages)[: self.config.max_content_length]
                    agent_span["input"] = input_repr

            self._agent_span_data = {
                "agent_name": agent_name,
                "start_time": self._invocation_start_time,
            }

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_CREATE, agent_span)

            self._current_parent_span_id = self.agent_span_id

            # Subscribe to gateway push interventions
            if self._intervention_dispatcher and self.trace_id:
                self._intervention_dispatcher.subscribe_trace(self.trace_id)

            logger.debug(f"[AIGIE] Agno trace started: {trace_name} (id={self.trace_id})")

        except Exception as e:
            logger.error(f"[AIGIE] Error in agno pre_hook: {e}", exc_info=True)

    async def _async_on_agent_post_hook(self, run_context: Any) -> None:
        """Handle agent post-hook — complete agent span and trace."""
        if not self.config.enabled or not self.config.trace_agents:
            return

        if not self.agent_span_id or not self.trace_id:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            agent_end_time = _utc_now()
            agent_name = self._agent_span_data.get("agent_name", "Agno Agent")
            invocation_start = self._agent_span_data.get("start_time", agent_end_time)

            # Extract tokens from run_response
            tokens = self._extract_tokens(run_context)
            input_tokens = tokens["input_tokens"]
            output_tokens = tokens["output_tokens"]

            # Use accumulated stats if response tokens are zero
            if input_tokens == 0 and output_tokens == 0:
                input_tokens = self._total_input_tokens
                output_tokens = self._total_output_tokens
            else:
                self._total_input_tokens = input_tokens
                self._total_output_tokens = output_tokens

            # Calculate cost
            model_id = self._extract_model_id(run_context)
            total_cost = 0.0
            if input_tokens > 0 or output_tokens > 0:
                try:
                    total_cost = calculate_agno_cost(
                        model_id=model_id,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                    )
                except Exception as cost_err:
                    logger.warning(f"[AIGIE] Cost calculation failed: {cost_err}")

            self._total_cost = total_cost

            # Determine status
            getattr(run_context, "run_response", None)
            has_error = self._has_errors or bool(self._error_messages)
            status = "error" if has_error else "success"

            error_message = None
            if self._error_messages:
                error_message = "; ".join(self._error_messages[:3])

            # Duration
            duration_ms = (agent_end_time - invocation_start).total_seconds() * 1000

            total_tokens = input_tokens + output_tokens

            complete_agent_span = {
                "id": self.agent_span_id,
                "trace_id": self.trace_id,
                "parent_id": None,
                "name": f"Agent: {agent_name}",
                "type": "agent",
                "start_time": invocation_start.isoformat(),
                "end_time": agent_end_time.isoformat(),
                "duration_ns": int(duration_ms * 1_000_000),
                "status": status,
                "depth": 0,
                "tags": self.tags,
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": total_tokens,
                "total_cost": total_cost,
                "token_usage": {
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "unit": "TOKENS",
                },
                "usage": {
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                },
                "metadata": merge_metadata(
                    {
                        "framework": "agno",
                        "agent_name": agent_name,
                        "model_id": model_id,
                        "total_tool_calls": self._total_tool_calls,
                        "total_input_tokens": input_tokens,
                        "total_output_tokens": output_tokens,
                        "total_tokens": total_tokens,
                        "total_cost": total_cost,
                        **self.metadata,
                    }
                ),
            }

            if error_message:
                complete_agent_span["error"] = error_message

            # Capture output content
            if self.config.capture_outputs:
                content = self._extract_content(run_context)
                if content:
                    complete_agent_span["output"] = content

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_CREATE, complete_agent_span)


            # Complete trace
            trace_update = {
                "id": self.trace_id,
                "end_time": agent_end_time.isoformat(),
                "status": status,
                "total_tokens": total_tokens,
                "total_cost": total_cost,
                "metadata": merge_metadata(
                    {
                        "framework": "agno",
                        "agent_name": agent_name,
                        "model_id": model_id,
                        "total_tool_calls": self._total_tool_calls,
                        **self.metadata,
                    }
                ),
            }

            if error_message:
                trace_update["error"] = error_message

            if aigie._buffer:
                await aigie._buffer.add(EventType.TRACE_UPDATE, trace_update)
                await aigie._buffer.flush()

            logger.debug(
                f"[AIGIE] Agno trace completed: {agent_name} "
                f"(tokens={total_tokens}, cost=${total_cost:.6f}, status={status})"
            )

        except Exception as e:
            logger.error(f"[AIGIE] Error in agno post_hook: {e}", exc_info=True)

    async def _async_on_team_pre_hook(self, run_context: Any) -> None:
        """Handle Team pre-hook — create trace and team span."""
        if not self.config.enabled or not self.config.trace_teams:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            self.trace_id = str(uuid.uuid4())
            self._has_errors = False
            self._error_messages = []
            self._total_tool_calls = 0
            self._total_input_tokens = 0
            self._total_output_tokens = 0
            self._total_cost = 0.0
            self.agent_span_id = None
            self.tool_span_map.clear()
            self._current_parent_span_id = None
            self._invocation_start_time = _utc_now()

            team = getattr(run_context, "team", None) or getattr(run_context, "agent", None)
            team_name = "Agno Team"
            if team is not None:
                team_name = getattr(team, "name", None) or "Agno Team"

            trace_name = self.trace_name or team_name

            trace_data = {
                "id": self.trace_id,
                "name": trace_name,
                "metadata": merge_metadata(
                    {
                        "framework": "agno",
                        "team_name": team_name,
                        **self.metadata,
                    }
                ),
                "tags": self.tags,
                "start_time": self._invocation_start_time.isoformat(),
            }

            if self.user_id:
                trace_data["user_id"] = self.user_id
            if self.session_id:
                trace_data["session_id"] = self.session_id

            if aigie._buffer:
                await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)
                await aigie._buffer.flush()

            # Create team span
            self.agent_span_id = str(uuid.uuid4())
            team_span = {
                "id": self.agent_span_id,
                "trace_id": self.trace_id,
                "parent_id": None,
                "name": f"Team: {team_name}",
                "type": "team",
                "start_time": self._invocation_start_time.isoformat(),
                "metadata": merge_metadata(
                    {
                        "framework": "agno",
                        "team_name": team_name,
                    }
                ),
                "tags": self.tags,
                "depth": 0,
            }

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_CREATE, team_span)

            self._agent_span_data = {
                "agent_name": team_name,
                "start_time": self._invocation_start_time,
            }
            self._current_parent_span_id = self.agent_span_id

            logger.debug(f"[AIGIE] Agno team trace started: {trace_name} (id={self.trace_id})")

        except Exception as e:
            logger.error(f"[AIGIE] Error in agno team pre_hook: {e}", exc_info=True)

    async def _async_on_team_post_hook(self, run_context: Any) -> None:
        """Handle Team post-hook — delegate to agent post hook logic."""
        # Team post hook mirrors agent post hook
        await self._async_on_agent_post_hook(run_context)

    async def _async_on_tool_pre_hook(self, run_context: Any) -> None:
        """Handle tool pre-hook — create a tool span."""
        if not self.config.enabled or not self.config.trace_tools:
            return

        if not self.trace_id or not self.agent_span_id:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            tool_name = "unknown_tool"
            # Agno passes tool name in run_context
            tool = getattr(run_context, "tool", None) or getattr(run_context, "function", None)
            if tool is not None:
                tool_name = (
                    getattr(tool, "name", None) or getattr(tool, "__name__", None) or str(tool)
                )

            tool_span_id = str(uuid.uuid4())
            tool_start_time = _utc_now()

            self.tool_span_map[tool_name] = {
                "span_id": tool_span_id,
                "start_time": tool_start_time,
            }

            tool_span = {
                "id": tool_span_id,
                "trace_id": self.trace_id,
                "parent_id": self._current_parent_span_id,
                "name": f"Tool: {tool_name}",
                "type": "tool",
                "start_time": tool_start_time.isoformat(),
                "metadata": merge_metadata(
                    {
                        "framework": "agno",
                        "tool_name": tool_name,
                    }
                ),
                "depth": 1,
            }

            # Capture tool input
            if self.config.capture_inputs:
                tool_input = getattr(run_context, "tool_input", None) or getattr(
                    run_context, "arguments", None
                )
                if tool_input is not None:
                    tool_span["input"] = str(tool_input)[: self.config.max_tool_result_length]

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_CREATE, tool_span)

        except Exception as e:
            logger.error(f"[AIGIE] Error in agno tool pre_hook: {e}", exc_info=True)

    async def _async_on_tool_post_hook(self, run_context: Any) -> None:
        """Handle tool post-hook — complete the tool span."""
        if not self.config.enabled or not self.config.trace_tools:
            return

        if not self.trace_id:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            tool_name = "unknown_tool"
            tool = getattr(run_context, "tool", None) or getattr(run_context, "function", None)
            if tool is not None:
                tool_name = (
                    getattr(tool, "name", None) or getattr(tool, "__name__", None) or str(tool)
                )

            tool_info = self.tool_span_map.get(tool_name)
            if not tool_info:
                return

            tool_end_time = _utc_now()
            tool_start_time = tool_info["start_time"]
            tool_span_id = tool_info["span_id"]
            duration_ms = (tool_end_time - tool_start_time).total_seconds() * 1000

            self._total_tool_calls += 1

            tool_result = getattr(run_context, "tool_result", None) or getattr(
                run_context, "result", None
            )
            has_error = isinstance(tool_result, Exception)
            status = "error" if has_error else "success"

            complete_tool_span = {
                "id": tool_span_id,
                "trace_id": self.trace_id,
                "parent_id": self._current_parent_span_id,
                "name": f"Tool: {tool_name}",
                "type": "tool",
                "start_time": tool_start_time.isoformat(),
                "end_time": tool_end_time.isoformat(),
                "duration_ns": int(duration_ms * 1_000_000),
                "status": status,
                "depth": 1,
                "metadata": merge_metadata(
                    {
                        "framework": "agno",
                        "tool_name": tool_name,
                        "duration_ms": duration_ms,
                    }
                ),
            }

            # Add tool_category hint for component registry classification
            try:
                from ...tool_category import infer_tool_category

                category = infer_tool_category(tool_name, None)
                if category:
                    complete_tool_span["metadata"]["tool_category"] = category
            except ImportError:
                pass

            if self.config.capture_outputs and tool_result is not None and not has_error:
                complete_tool_span["output"] = str(tool_result)[
                    : self.config.max_tool_result_length
                ]

            if has_error:
                complete_tool_span["error"] = str(tool_result)
                self._has_errors = True
                self._error_messages.append(f"Tool {tool_name} failed: {tool_result}")

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_CREATE, complete_tool_span)


            # Real-time remediation: evaluate errors and report results with before/after data
            if has_error and self._remediation_engine:
                error_msg = str(tool_result)[:2000]
                tool_input = getattr(run_context, "tool_input", None) or getattr(
                    run_context, "arguments", None
                )
                try:
                    rem_result = await self._remediation_engine.evaluate(
                        error_output=error_msg,
                        span_id=tool_span_id,
                        tool_name=tool_name,
                    )
                    if rem_result:
                        rem_result.original_input = (
                            str(tool_input) if tool_input is not None else ""
                        )
                        rem_result.original_output = error_msg
                        await self._report_remediation(tool_span_id, rem_result)
                except Exception as rem_err:
                    logger.debug(f"[AIGIE] Remediation evaluate failed: {rem_err}")

            # Remove from map after completion
            self.tool_span_map.pop(tool_name, None)

        except Exception as e:
            logger.error(f"[AIGIE] Error in agno tool post_hook: {e}", exc_info=True)

    async def _report_remediation(self, span_id: str, result) -> None:
        """Report a remediation result to the platform via SPAN_UPDATE and POST to /remediation/results."""
        try:
            aigie = self._get_aigie()
            if not aigie or not aigie._initialized:
                return

            if aigie._buffer:
                await aigie._buffer.add(
                    EventType.SPAN_UPDATE,
                    {
                        "id": span_id,
                        "trace_id": self.trace_id,
                        "metadata": merge_metadata(
                            {
                                "realtime_remediation": result.to_dict(),
                            }
                        ),
                    },
                )

            if self._remediation_engine:
                await self._remediation_engine.report_result(result, self.trace_id)
        except Exception:
            pass  # Best-effort reporting
