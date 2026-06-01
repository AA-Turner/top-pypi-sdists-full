"""
Aigie Plugin for Google ADK.

Extends Google ADK's BasePlugin to provide automatic tracing for all agents
in a Runner without requiring manual callback registration.
"""

import logging
from typing import TYPE_CHECKING, Any, Optional

from ..._legacy_stubs import get_error_detector  # legacy autonomous-mode shim
from .config import GoogleADKConfig
from .handler import GoogleADKHandler

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    try:
        from google.adk.agents.callback_context import CallbackContext
        from google.adk.agents.invocation_context import InvocationContext
        from google.adk.models.llm_request import LlmRequest
        from google.adk.models.llm_response import LlmResponse
        from google.adk.plugins.base_plugin import BasePlugin
        from google.adk.tools.base_tool import BaseTool
        from google.adk.tools.tool_context import ToolContext
    except ImportError:
        pass


# ADK 2.0 added a pydantic `isinstance(BasePlugin)` validator on `App.plugins`,
# so AigiePlugin must subclass BasePlugin when google-adk is installed. Fall
# back to `object` so this module is importable without the optional extra.
_PluginBase: type
try:
    from google.adk.plugins.base_plugin import BasePlugin

    _PluginBase = BasePlugin
except ImportError:  # pragma: no cover - exercised only when google-adk missing
    _PluginBase = object


class AigiePlugin(_PluginBase):
    """Aigie tracing plugin for Google ADK.

    Extends Google ADK's Plugin system to automatically trace all agents
    running within a Runner: per-invocation trace creation, agent /
    LLM / tool span emission with token+cost tracking, event-stream
    monitoring, and error detection.

    Example:
        >>> from google.adk import Runner, LlmAgent
        >>> from aigie.integrations.google_adk import AigiePlugin
        >>> agent = LlmAgent(name="assistant", model="gemini-2.5-flash")
        >>> plugin = AigiePlugin(trace_name="My Agent")
        >>> runner = Runner(agent=agent, session_service=session_service,
        ...                plugins=[plugin])
        >>> async for event in runner.run_async(...):
        ...     process(event)
    """

    def __init__(
        self,
        config: GoogleADKConfig | None = None,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        name: str = "aigie",
    ):
        """
        Initialize AigiePlugin.

        Args:
            config: Configuration for tracing behavior
            trace_name: Name for the trace
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
            name: Plugin name (default: "aigie")
        """
        # Defer to BasePlugin.__init__ when google-adk is installed (it sets
        # self.name); otherwise assign directly.
        if _PluginBase is object:
            self.name = name
        else:
            super().__init__(name=name)
        self.config = config or GoogleADKConfig.from_env()
        self._base_plugin_class = _PluginBase if _PluginBase is not object else None
        self._pending_user_message: str | None = None

        # Create the underlying handler
        self._handler = GoogleADKHandler(
            config=self.config,
            trace_name=trace_name,
            metadata=metadata,
            tags=tags,
            user_id=user_id,
            session_id=session_id,
        )

    # ========================================================================
    # Runner Lifecycle Callbacks
    # ========================================================================

    async def on_user_message_callback(
        self,
        *,
        invocation_context: "InvocationContext",
        user_message: Any,
    ) -> None:
        """
        Called when a user message is received.

        This is called before the run starts, allowing capture of the initial input.

        Args:
            invocation_context: The invocation context
            user_message: The user's message content
        """
        if not self.config.enabled:
            return

        # Store the user message for the run start - extract text from Content/Part objects
        if user_message:
            from .handler import _extract_text_from_contents

            self._pending_user_message = _extract_text_from_contents(user_message)
        else:
            self._pending_user_message = None

    async def before_run_callback(
        self,
        *,
        invocation_context: "InvocationContext",
    ) -> None:
        """
        Called before a Runner.run_async() begins.

        Creates the trace and top-level run span.

        Args:
            invocation_context: The invocation context
        """
        if not self.config.enabled:
            return

        user_message = getattr(self, "_pending_user_message", None)
        await self._handler.handle_run_start(invocation_context, user_message)
        self._pending_user_message = None

    async def after_run_callback(
        self,
        *,
        invocation_context: "InvocationContext",
    ) -> None:
        """
        Called after a Runner.run_async() completes.

        Completes the trace with aggregated metrics.

        Args:
            invocation_context: The invocation context
        """
        if not self.config.enabled:
            return

        await self._handler.handle_run_end(invocation_context)

    async def on_event_callback(
        self,
        *,
        invocation_context: "InvocationContext",
        event: Any,
    ) -> None:
        """
        Called for each event emitted during the run.

        Args:
            invocation_context: The invocation context
            event: The event object
        """
        if not self.config.enabled or not self.config.trace_events:
            return

        await self._handler.handle_event(invocation_context, event)

    # ========================================================================
    # Agent Lifecycle Callbacks
    # ========================================================================

    async def before_agent_callback(
        self,
        *,
        agent: Any,
        callback_context: "CallbackContext",
    ) -> None:
        """
        Called before an agent executes.

        Creates an agent span.

        Args:
            agent: The agent instance
            callback_context: The callback context
        """
        if not self.config.enabled or not self.config.trace_agents:
            return

        await self._handler.handle_agent_start(agent, callback_context)

    async def after_agent_callback(
        self,
        *,
        agent: Any,
        callback_context: "CallbackContext",
    ) -> None:
        """
        Called after an agent completes execution.

        Completes the agent span.

        Args:
            agent: The agent instance
            callback_context: The callback context
        """
        if not self.config.enabled or not self.config.trace_agents:
            return

        await self._handler.handle_agent_end(agent, callback_context)

    # ========================================================================
    # Model Lifecycle Callbacks
    # ========================================================================

    async def before_model_callback(
        self,
        *,
        callback_context: "CallbackContext",
        llm_request: "LlmRequest",
    ) -> Optional["LlmResponse"]:
        """
        Called before an LLM/model call.

        Creates an LLM span.

        Args:
            callback_context: The callback context
            llm_request: The LLM request object

        Returns:
            Always None — we observe but never short-circuit the model call.
        """
        if not self.config.enabled or not self.config.trace_llm_calls:
            return None

        await self._handler.handle_llm_start(callback_context, llm_request)
        return None  # Don't modify the request

    async def after_model_callback(
        self,
        *,
        callback_context: "CallbackContext",
        llm_response: "LlmResponse",
    ) -> Optional["LlmResponse"]:
        """
        Called after an LLM/model call completes successfully.

        Completes the LLM span with token/cost data.

        Args:
            callback_context: The callback context
            llm_response: The LLM response object

        Returns:
            The (optionally modified) LLM response, or None to use original
        """
        if not self.config.enabled or not self.config.trace_llm_calls:
            return None

        await self._handler.handle_llm_end(callback_context, llm_response)
        return None  # Don't modify the response

    async def on_model_error_callback(
        self,
        *,
        callback_context: "CallbackContext",
        llm_request: "LlmRequest",
        error: Exception,
    ) -> None:
        """
        Called when an LLM/model call fails.

        Completes the LLM span with error status.

        Args:
            callback_context: The callback context
            llm_request: The LLM request that failed
            error: The exception that occurred
        """
        if not self.config.enabled or not self.config.trace_llm_calls:
            return

        await self._handler.handle_llm_end(callback_context, None, error=error)

    # ========================================================================
    # Tool Lifecycle Callbacks
    # ========================================================================

    async def before_tool_callback(
        self,
        *,
        tool: "BaseTool",
        tool_args: dict[str, Any],
        tool_context: "ToolContext",
    ) -> dict[str, Any] | None:
        """
        Called before a tool execution.

        Creates a tool span. In autonomous mode, checks for gateway
        interventions that may modify args or delay execution.

        Returns:
            Modified tool args if intervention applies, None otherwise.
        """
        if not self.config.enabled or not self.config.trace_tools:
            return None

        await self._handler.handle_tool_start(tool, tool_args, tool_context)

        # Check for pre-tool interception (modify args, delay, etc.)
        try:
            aigie = self._handler._get_aigie()
            if aigie and aigie._initialized:
                intercept = await aigie.intercept_before_tool(
                    tool_name=getattr(tool, "name", "unknown_tool"),
                    tool_args=tool_args or {},
                    trace_id=self._handler.trace_id,
                )
                modified_args = intercept.get("modified_args")
                if intercept.get("decision") == "modify" and modified_args:
                    logger.info(
                        f"[AIGIE] Pre-tool: modifying args for {getattr(tool, 'name', '?')}"
                    )
                    return dict(modified_args)
        except Exception as e:
            logger.debug("[AIGIE] before_tool_callback fail-open: %s", e)

        return None

    async def after_tool_callback(
        self,
        *,
        tool: "BaseTool",
        tool_args: dict[str, Any],
        tool_context: "ToolContext",
        result: Any,
    ) -> Any | None:
        """
        Called after a tool execution completes successfully.

        Completes the tool span. In autonomous mode, may modify the result
        with remediation guidance if an error pattern is detected.

        Returns:
            Modified result if remediation applies, None otherwise.
        """
        if not self.config.enabled or not self.config.trace_tools:
            return None

        await self._handler.handle_tool_end(tool, tool_args, tool_context, result)

        # Check for post-tool fixes (error patterns, remediation guidance)
        try:
            aigie = self._handler._get_aigie()
            if aigie and aigie._initialized:
                tool_name = getattr(tool, "name", "unknown_tool")

                # Use the proper ErrorDetector for pattern-based detection

                detector = get_error_detector()
                detected = detector.detect_from_tool_result(
                    tool_name=tool_name,
                    tool_use_id="",
                    result=result,
                )

                if detected:
                    # `raw_error` exists on integration-local DetectedError but
                    # not on the legacy stub — fall back to `message`.
                    error_text = getattr(detected, "raw_error", None) or detected.message
                    post = await aigie.intercept_after_tool(
                        tool_name=tool_name,
                        result=result,
                        error=error_text,
                        trace_id=self._handler.trace_id,
                    )
                    if post.get("modified_result"):
                        logger.info(f"[AIGIE] Post-tool: modified result for {tool_name}")
                        return post["modified_result"]
        except Exception as e:
            logger.debug("[AIGIE] after_tool_callback fail-open: %s", e)

        return None

    async def on_tool_error_callback(
        self,
        *,
        tool: "BaseTool",
        tool_args: dict[str, Any],
        tool_context: "ToolContext",
        error: Exception,
    ) -> None:
        """
        Called when a tool execution fails.

        Completes the tool span with error status.

        Args:
            tool: The tool that failed
            tool_args: Arguments passed to the tool
            tool_context: The tool context
            error: The exception that occurred
        """
        if not self.config.enabled or not self.config.trace_tools:
            return

        await self._handler.handle_tool_end(tool, tool_args, tool_context, None, error=error)

    # ========================================================================
    # Plugin Lifecycle
    # ========================================================================

    async def close(self) -> None:
        """
        Close the plugin and flush any pending data.

        Called when the Runner is being shut down.
        """
        try:
            aigie = self._handler._get_aigie()
            if aigie and hasattr(aigie, "_buffer") and aigie._buffer:
                await aigie._buffer.flush()
                logger.debug("[AIGIE] Plugin closed, buffer flushed")
        except Exception as e:
            logger.warning(f"[AIGIE] Error closing plugin: {e}")

    # ========================================================================
    # Properties for Access
    # ========================================================================

    @property
    def trace_id(self) -> str | None:
        """Get the current trace ID."""
        return self._handler.trace_id

    @property
    def total_cost(self) -> float:
        """Get the total cost so far."""
        return self._handler._total_cost

    @property
    def total_tokens(self) -> int:
        """Get the total tokens used so far."""
        return self._handler._total_input_tokens + self._handler._total_output_tokens

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of the tracing data."""
        return {
            "trace_id": self._handler.trace_id,
            "total_model_calls": self._handler._total_model_calls,
            "total_tool_calls": self._handler._total_tool_calls,
            "total_input_tokens": self._handler._total_input_tokens,
            "total_output_tokens": self._handler._total_output_tokens,
            "total_tokens": self._handler._total_input_tokens + self._handler._total_output_tokens,
            "total_cost": self._handler._total_cost,
            "error_count": len(self._handler._detected_errors),
        }

    def __repr__(self) -> str:
        return (
            f"AigiePlugin("
            f"name={self.name}, "
            f"trace_id={self._handler.trace_id}, "
            f"enabled={self.config.enabled})"
        )
