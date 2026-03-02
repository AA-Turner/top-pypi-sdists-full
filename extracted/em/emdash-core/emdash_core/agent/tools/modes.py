"""Agent mode management tools.

Provides tools for entering and exiting modes, following
Claude Code's approach of explicit mode transitions.
"""

import contextvars
from enum import Enum
from typing import Dict, Optional

from .base import BaseTool, ToolResult, ToolCategory


class AgentMode(Enum):
    """Available agent modes."""
    PLAN = "plan"
    CODE = "code"


# Modes that can be entered via enter_mode tool
SUPPORTED_MODES = ["plan"]  # Extensible list

# Context variable to track the current session ID per-coroutine
_current_session_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    'mode_state_session_id', default=None
)


class ModeState:
    """Per-session state for agent mode.

    Uses a dict of instances keyed by session_id to isolate state between
    concurrent sessions. A contextvars-based fallback allows tools to access
    the correct instance without explicitly passing session_id.
    """

    _instances: Dict[str, "ModeState"] = {}
    _default_instance: Optional["ModeState"] = None

    def __init__(self):
        self.current_mode: AgentMode = AgentMode.CODE
        self.plan_content: Optional[str] = None  # Stores the current plan
        self.plan_submitted: bool = False  # Track if exit_plan was called this cycle
        self.plan_mode_requested: bool = False  # Track if enter_plan_mode was called
        self.plan_mode_reason: Optional[str] = None  # Reason for plan mode request
        self.plan_file_path: Optional[str] = None  # Path to the plan file (set when entering plan mode)

    @classmethod
    def set_session_context(cls, session_id: str) -> contextvars.Token:
        """Set the session context for the current coroutine/thread.

        Call this at the start of request handling to establish which session
        is being processed. Tools can then call get_instance() without a
        session_id parameter.

        Returns:
            Token that can be used to reset the context later.
        """
        return _current_session_id.set(session_id)

    @classmethod
    def reset_session_context(cls, token: contextvars.Token) -> None:
        """Reset the session context using the token from set_session_context."""
        _current_session_id.reset(token)

    @classmethod
    def get_instance(cls, session_id: Optional[str] = None) -> "ModeState":
        """Get the ModeState instance for a session.

        Args:
            session_id: Optional session ID. If not provided, uses the session
                       from the current context (set via set_session_context).
                       Falls back to a default instance if no context is set.

        Returns:
            ModeState instance for the session.
        """
        # Try explicit session_id first, then context, then default
        sid = session_id or _current_session_id.get()

        if not sid:
            # Fallback to default instance for backwards compatibility
            # (e.g., CLI usage without sessions)
            if cls._default_instance is None:
                cls._default_instance = cls()
            return cls._default_instance

        if sid not in cls._instances:
            cls._instances[sid] = cls()
        return cls._instances[sid]

    @classmethod
    def reset(cls, session_id: Optional[str] = None) -> None:
        """Reset the ModeState instance for a session.

        Args:
            session_id: Optional session ID. If not provided, resets based on
                       context or the default instance.
        """
        sid = session_id or _current_session_id.get()

        if not sid:
            cls._default_instance = None
        elif sid in cls._instances:
            del cls._instances[sid]

    @classmethod
    def cleanup_session(cls, session_id: str) -> None:
        """Clean up the ModeState for a session when it ends."""
        if session_id in cls._instances:
            del cls._instances[session_id]

    def reset_cycle(self) -> None:
        """Reset per-cycle state (called on new user message)."""
        self.plan_submitted = False
        self.plan_mode_requested = False
        self.plan_mode_reason = None

    def approve_plan_mode(self) -> None:
        """Approve plan mode entry (called when user approves)."""
        self.current_mode = AgentMode.PLAN
        self.plan_content = None
        self.plan_mode_requested = False
        self.plan_mode_reason = None
        # plan_file_path should already be set by the caller

    def reject_plan_mode(self) -> None:
        """Reject plan mode entry (called when user rejects)."""
        self.plan_mode_requested = False
        self.plan_mode_reason = None
        self.plan_file_path = None

    def set_plan_file_path(self, path: str) -> None:
        """Set the plan file path (called when entering plan mode)."""
        self.plan_file_path = path

    def get_plan_file_path(self) -> Optional[str]:
        """Get the current plan file path."""
        return self.plan_file_path


class EnterPlanModeTool(BaseTool):
    """Tool for requesting to enter plan mode - REQUIRES USER CONSENT.

    This follows Claude Code's pattern where entering plan mode is a proposal
    that requires user approval, not an automatic switch.
    """

    name = "enter_plan_mode"
    description = """Request to enter plan mode for implementation planning.

This tool REQUIRES USER APPROVAL before plan mode is activated.

Use this proactively when you're about to start a non-trivial implementation task.
Getting user sign-off on your approach before writing code prevents wasted effort.

When to use:
- New feature implementation requiring architectural decisions
- Multiple valid approaches exist (user should choose)
- Multi-file changes expected (more than 2-3 files)
- Unclear requirements that need exploration first

When NOT to use:
- Single-line or few-line fixes
- Trivial tasks with obvious implementation
- Pure research/exploration (just explore directly)
- Tasks with very specific, detailed instructions already provided

The user will see your reason and can approve or reject entering plan mode."""
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(
        self,
        reason: str = "",
        **kwargs,
    ) -> ToolResult:
        """Request to enter plan mode (requires user approval).

        Args:
            reason: Why you want to enter plan mode (shown to user)

        Returns:
            ToolResult requesting user approval
        """
        state = ModeState.get_instance()

        if state.current_mode == AgentMode.PLAN:
            return ToolResult.error_result(
                "Already in plan mode",
                suggestions=["Use exit_plan to submit your plan for approval"],
            )

        # Check if already requested this cycle
        if state.plan_mode_requested:
            return ToolResult.error_result(
                "Plan mode already requested. Wait for user response.",
                suggestions=["Do not call enter_plan_mode again until user responds."],
            )

        if not reason or not reason.strip():
            return ToolResult.error_result(
                "Reason is required",
                suggestions=["Explain why you need plan mode (helps user decide)"],
            )

        # Mark as requested (not entered - user must approve)
        state.plan_mode_requested = True
        state.plan_mode_reason = reason.strip()

        return ToolResult.success_result(
            data={
                "status": "plan_mode_requested",
                "reason": reason.strip(),
                "message": "Plan mode requested. Waiting for user approval.",
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "reason": {
                    "type": "string",
                    "description": "Why you want to enter plan mode (explain the task complexity)",
                },
            },
            required=["reason"],
        )


class ExitPlanModeTool(BaseTool):
    """Tool for submitting a plan for user approval."""

    name = "exit_plan"
    description = """Submit an implementation plan for user approval.

Use this tool to present a plan to the user for approval. The plan can come from:
1. A Plan sub-agent you spawned via task(subagent_type="Plan", ...)
2. Your own planning (if in plan mode)

Pass the plan content as the 'plan' parameter.

The user will either:
- Approve: You can proceed with implementation
- Reject: You'll receive feedback and can revise"""
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(
        self,
        plan: Optional[str] = None,
        **kwargs,
    ) -> ToolResult:
        """Submit plan for user approval.

        Args:
            plan: The plan content (required in code mode, optional in plan mode).

        Returns:
            ToolResult triggering user approval flow
        """
        state = ModeState.get_instance()

        # Prevent multiple exit_plan calls per cycle
        if state.plan_submitted:
            return ToolResult.error_result(
                "Plan already submitted. Wait for user approval.",
                suggestions=["Do not call exit_plan again until user responds."],
            )

        # Get plan content from parameter or file
        plan_content = plan

        # In plan mode, try to read from plan file if not provided
        if state.current_mode == AgentMode.PLAN:
            if not plan_content or not plan_content.strip():
                plan_file_path = state.get_plan_file_path()
                if plan_file_path:
                    try:
                        from pathlib import Path
                        plan_path = Path(plan_file_path)
                        if plan_path.exists():
                            plan_content = plan_path.read_text()
                    except Exception as e:
                        return ToolResult.error_result(
                            f"Failed to read plan file: {e}",
                            suggestions=[f"Write your plan to {plan_file_path} first"],
                        )

        # In code mode, plan content is required (from Plan subagent)
        if state.current_mode == AgentMode.CODE:
            if not plan_content or not plan_content.strip():
                return ToolResult.error_result(
                    "Plan content is required when submitting from code mode",
                    suggestions=[
                        "Pass the plan from your Plan sub-agent as the 'plan' parameter",
                        "Example: exit_plan(plan=<plan_from_subagent>)",
                    ],
                )

        if not plan_content or not plan_content.strip():
            plan_file_path = state.get_plan_file_path() or "the plan file"
            return ToolResult.error_result(
                "Plan content is required",
                suggestions=[
                    f"Write your plan to {plan_file_path} using write_to_file, then call exit_plan",
                    "Or pass the plan directly as a parameter",
                ],
            )

        # Store plan content for reference and mark as submitted
        state.plan_content = plan_content.strip()
        state.plan_submitted = True

        return ToolResult.success_result({
            "status": "plan_submitted",
            "plan": plan_content.strip(),
            "message": "Plan submitted for user approval. Waiting for user response.",
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "plan": {
                    "type": "string",
                    "description": "Optional: The implementation plan as markdown. If not provided, reads from the plan file.",
                },
            },
            required=[],
        )


class GetModeTool(BaseTool):
    """Tool for getting current agent mode."""

    name = "get_mode"
    description = "Get the current agent operating mode (plan or code)."
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(self, **kwargs) -> ToolResult:
        """Get current mode.

        Returns:
            ToolResult with current mode info
        """
        state = ModeState.get_instance()

        return ToolResult.success_result(
            data={
                "current_mode": state.current_mode.value,
                "has_plan": state.plan_content is not None,
                "available_modes": SUPPORTED_MODES,
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(properties={}, required=[])
