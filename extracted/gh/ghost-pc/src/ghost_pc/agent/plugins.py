"""ADK Plugins — global cross-cutting concerns for all agents.

Plugins apply to ALL agents, tools, and LLM calls globally (unlike callbacks
which are per-agent). They intercept the full lifecycle: before/after model,
before/after tool, before/after agent, and error handlers.

All BasePlugin callbacks use keyword-only arguments. The exact signatures are:
  before_tool_callback(*, tool, tool_args, tool_context) -> dict | None
  after_tool_callback(*, tool, tool_args, tool_context, result) -> dict | None
  before_model_callback(*, callback_context, llm_request) -> LlmResponse | None
  after_model_callback(*, callback_context, llm_response) -> LlmResponse | None
  on_tool_error_callback(*, tool, tool_args, tool_context, error) -> dict | None
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import TYPE_CHECKING, Any

from google.adk.plugins import BasePlugin
from google.genai import types

from ghost_pc.agent.confirmation import ConfirmationManager

if TYPE_CHECKING:
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.models.llm_request import LlmRequest
    from google.adk.models.llm_response import LlmResponse
    from google.adk.tools.base_tool import BaseTool
    from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Dangerous command patterns the agent should NEVER execute
# --------------------------------------------------------------------------- #
_BLOCKED_TERMINAL_PATTERNS: set[str] = {
    # Windows cmd destructive
    "del /s",
    "format c:",
    "format d:",
    "rd /s /q c:",
    "del c:\\",
    # Linux/cross-platform destructive
    "rm -rf /",
    "rm -rf ~",
    "rm -rf .",
    # System commands
    "shutdown",
    "bcdedit",
    "diskpart",
    "sfc /scannow",
    # Registry manipulation
    "reg delete",
    # User/group manipulation
    "net user",
    "net localgroup administrators",
    # PowerShell destructive equivalents
    "remove-item -recurse -force c:",
    "remove-item -recurse -force /",
    "clear-content",
    "format-volume",
    "clear-recyclebin",
    # Encoded/obfuscated execution (bypass vectors)
    "powershell -encodedcommand",
    "powershell -enc ",
    "powershell -e ",
    "powershell -ec ",
    # Subprocess wrapping (bypass vectors)
    "cmd /c format",
    "cmd /c del",
    "cmd /c rd",
    "cmd /c shutdown",
    "cmd.exe /c format",
    "cmd.exe /c del",
    # IEX / Invoke-Expression download cradle
    "invoke-expression",
    "iex(",
    "iex ",
    # Disable security
    "set-mppreference -disablerealtimemonitoring",
    "netsh advfirewall set allprofiles state off",
}


def _normalize_command(command: str) -> str:
    """Normalize a command string for safety checking.

    Collapses whitespace, lowercases, strips quotes and backticks
    to prevent trivial bypass via spacing, casing, or quoting.
    """
    import re as _re

    # Lowercase
    cmd = command.lower()
    # Remove backtick escape chars (PowerShell obfuscation: po`wer`shell)
    cmd = cmd.replace("`", "")
    # Remove caret escape chars (cmd obfuscation: po^wer^shell)
    cmd = cmd.replace("^", "")
    # Collapse all whitespace to single spaces
    cmd = _re.sub(r"\s+", " ", cmd).strip()
    return cmd


class SafetyPlugin(BasePlugin):
    """Block dangerous terminal commands and detect stuck loops.

    Hooks:
      - before_tool: blocks dangerous terminal commands, detects repeated actions.
      - on_tool_error: logs errors, prevents crash propagation.
    """

    def __init__(self, max_repeated_actions: int = 3) -> None:
        super().__init__(name="safety_plugin")
        self._max_repeated = max_repeated_actions
        self._action_history: dict[str, list[str]] = defaultdict(list)

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> dict[str, Any] | None:
        """Intercept tool calls globally — block dangerous commands and detect loops."""
        tool_name = tool.name
        invocation_id = tool_context.invocation_id

        # ---- Block dangerous terminal commands ----
        if tool_name == "run_terminal":
            raw_command = str(tool_args.get("command", ""))
            command = _normalize_command(raw_command)
            for pattern in _BLOCKED_TERMINAL_PATTERNS:
                if pattern in command:
                    logger.warning(
                        "SafetyPlugin BLOCKED command: %s (matched: %s)",
                        raw_command,
                        pattern,
                    )
                    return {
                        "status": "blocked",
                        "error": (f"Dangerous command blocked by safety plugin: {pattern!r}"),
                    }

        # ---- Detect stuck loops (3+ identical actions) ----
        action_key = f"{tool_name}:{sorted(tool_args.items())}"
        history = self._action_history[invocation_id]
        history.append(action_key)

        if len(history) > self._max_repeated + 2:
            self._action_history[invocation_id] = history[-(self._max_repeated + 2) :]
            history = self._action_history[invocation_id]

        if len(history) >= self._max_repeated:
            recent = history[-self._max_repeated :]
            if len(set(recent)) == 1:
                logger.warning(
                    "SafetyPlugin detected stuck loop: %s repeated %d times",
                    tool_name,
                    self._max_repeated,
                )
                return {
                    "status": "stuck",
                    "error": (
                        f"You seem stuck — {tool_name} was called "
                        f"{self._max_repeated} times with the same arguments. "
                        "Try a different approach or ask the user."
                    ),
                }

        return None

    async def on_tool_error_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
        error: Exception,
    ) -> dict[str, Any] | None:
        """Log tool errors globally and return structured error for the model."""
        logger.error("Tool %s failed: %s", tool.name, error, exc_info=True)
        return {
            "status": "error",
            "tool": tool.name,
            "error": str(error),
            "hint": "The tool raised an exception. Try a different approach.",
        }


class ConfirmationPlugin(BasePlugin):
    """Intercept sensitive tool calls and require user confirmation.

    Sits between SafetyPlugin and CostTrackingPlugin in the plugin chain.
    When a sensitive action is detected, returns a fake result instructing
    the agent to ask the user for approval. The orchestrator then handles
    the YES/NO reply flow.
    """

    def __init__(self, confirmation_manager: ConfirmationManager) -> None:
        super().__init__(name="confirmation_plugin")
        self._manager = confirmation_manager

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> dict[str, Any] | None:
        """Check if this tool call requires user confirmation."""
        from ghost_pc.agent.confirmation import classify_action

        severity = classify_action(tool.name, tool_args)
        if severity != "sensitive":
            return None

        # Get user_id from invocation context
        inv_ctx = getattr(tool_context, "_invocation_context", None)
        user_id = getattr(inv_ctx, "user_id", None) if inv_ctx else None
        if not user_id:
            return None  # Can't confirm without user_id, allow execution

        # Build human-readable description
        if tool.name == "run_terminal":
            desc = f"Run command: `{tool_args.get('command', '')}`"
        elif tool.name == "kill_process":
            desc = f"Kill process: `{tool_args.get('name', '')}`"
        elif tool.name == "manage_window":
            desc = f"Close window: `{tool_args.get('title', 'active window')}`"
        else:
            desc = f"{tool.name}({tool_args})"

        self._manager.create(user_id, tool.name, tool_args, desc)

        logger.info("ConfirmationPlugin: action requires approval — %s", desc)
        return {
            "status": "confirmation_required",
            "message": (
                f"This action requires user confirmation.\n"
                f"Action: {desc}\n"
                f"Ask the user to reply YES or NO to proceed."
            ),
        }


class CostTrackingPlugin(BasePlugin):
    """Track token usage and tool calls per user for cost monitoring.

    Writes running totals to session state under ``user:`` prefix so they
    persist across sessions (when using DatabaseSessionService).
    Also maintains in-memory totals for the dashboard via ``get_cost_summary()``.
    """

    def __init__(self) -> None:
        super().__init__(name="cost_tracking_plugin")
        self._total_tokens = 0
        self._total_llm_calls = 0
        self._total_tool_calls = 0

    async def after_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_response: LlmResponse,
    ) -> LlmResponse | None:
        """Count tokens from each LLM response and accumulate in state."""
        state = callback_context.state

        tokens_used = 0
        if hasattr(llm_response, "usage_metadata") and llm_response.usage_metadata:
            tokens_used = getattr(llm_response.usage_metadata, "total_token_count", 0) or 0
        elif hasattr(llm_response, "content") and llm_response.content:
            for part in llm_response.content.parts or []:
                if part.text:
                    tokens_used += len(part.text) // 4

        prev_tokens = state.get("user:total_tokens", 0)
        state["user:total_tokens"] = prev_tokens + tokens_used

        prev_calls = state.get("user:total_llm_calls", 0)
        state["user:total_llm_calls"] = prev_calls + 1

        # In-memory aggregate for dashboard
        self._total_tokens += tokens_used
        self._total_llm_calls += 1

        return None

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
        result: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Count tool calls per user."""
        state = tool_context.state
        prev_tool_calls = state.get("user:total_tool_calls", 0)
        state["user:total_tool_calls"] = prev_tool_calls + 1
        self._total_tool_calls += 1
        return None

    def get_cost_summary(self) -> dict[str, int]:
        """Return aggregated cost data for the dashboard."""
        return {
            "total_tokens": self._total_tokens,
            "total_llm_calls": self._total_llm_calls,
            "total_tool_calls": self._total_tool_calls,
        }


class CostBudgetPlugin(BasePlugin):
    """Prevent runaway spending by aborting when a user exceeds a token budget.

    Checks accumulated tokens before each LLM call. If the budget is exceeded
    for the current invocation, returns a canned response instead of calling
    the model.
    """

    def __init__(self, max_tokens_per_invocation: int = 500_000) -> None:
        super().__init__(name="cost_budget_plugin")
        self._max_tokens = max_tokens_per_invocation

    async def before_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_request: LlmRequest,
    ) -> LlmResponse | None:
        """Abort if the user has exceeded the token budget for this session."""
        state = callback_context.state
        total_tokens = state.get("user:total_tokens", 0)

        if total_tokens >= self._max_tokens:
            logger.warning(
                "CostBudgetPlugin: user exceeded budget (%d >= %d tokens), aborting",
                total_tokens,
                self._max_tokens,
            )
            from google.adk.models.llm_response import LlmResponse as _LlmResponse

            return _LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text="I've used a lot of resources on this session. "
                            "Please start a new conversation to continue."
                        )
                    ],
                ),
            )
        return None


class ObservabilityPlugin(BasePlugin):
    """Log every LLM call and tool call with latency for monitoring.

    Lightweight structured-logging plugin. For production, swap
    the logger calls with OpenTelemetry span exports.
    """

    def __init__(self) -> None:
        super().__init__(name="observability_plugin")
        self._model_start_times: dict[str, float] = {}
        self._tool_start_times: dict[str, float] = {}

    async def before_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_request: LlmRequest,
    ) -> LlmResponse | None:
        """Record model call start time."""
        key = callback_context.invocation_id
        self._model_start_times[key] = time.monotonic()
        return None

    async def after_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_response: LlmResponse,
    ) -> LlmResponse | None:
        """Log model call latency."""
        key = callback_context.invocation_id
        start = self._model_start_times.pop(key, None)
        latency_ms = (time.monotonic() - start) * 1000 if start else 0

        tokens = 0
        if hasattr(llm_response, "usage_metadata") and llm_response.usage_metadata:
            tokens = getattr(llm_response.usage_metadata, "total_token_count", 0) or 0

        logger.info(
            "LLM call | agent=%s latency=%.0fms tokens=%d",
            callback_context.agent_name,
            latency_ms,
            tokens,
        )
        return None

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> dict[str, Any] | None:
        """Record tool call start time."""
        key = f"{tool_context.invocation_id}:{tool.name}"
        self._tool_start_times[key] = time.monotonic()
        logger.debug("Tool call START | tool=%s args=%s", tool.name, tool_args)
        return None

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
        result: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Log tool call latency."""
        key = f"{tool_context.invocation_id}:{tool.name}"
        start = self._tool_start_times.pop(key, None)
        latency_ms = (time.monotonic() - start) * 1000 if start else 0

        status = result.get("status", "unknown") if isinstance(result, dict) else "ok"
        logger.info(
            "Tool call | tool=%s status=%s latency=%.0fms",
            tool.name,
            status,
            latency_ms,
        )
        return None
