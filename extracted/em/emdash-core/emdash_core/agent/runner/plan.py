"""Plan management mixin for the agent runner.

This module provides plan approval/rejection functionality as a mixin class.
"""

from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..toolkit import AgentToolkit


class PlanMixin:
    """Mixin class providing plan management methods for AgentRunner.

    This mixin expects the following attributes on the class:
    - _pending_plan: Optional[dict] - stores pending plan
    - toolkit: AgentToolkit - the agent's toolkit
    - emitter: AgentEventEmitter - event emitter
    - system_prompt: str - current system prompt

    And the following methods:
    - run(message: str) -> str - to continue execution
    """

    _pending_plan: Optional[dict]

    def _get_plan_file_path(self) -> str:
        """Get the plan file path.

        Prefers the toolkit's plan_file_path (session-specific in ~/.emdash/sessions/)
        if set, otherwise falls back to repo-local path.

        Returns:
            Path to the plan file
        """
        # Prefer toolkit's session-specific plan_file_path
        if hasattr(self.toolkit, 'plan_file_path') and self.toolkit.plan_file_path:
            return self.toolkit.plan_file_path
        # Fallback to repo-local (should not happen in normal flow)
        repo_root = self.toolkit._repo_root
        return str(repo_root / ".emdash" / "plan.md")

    def _cleanup_plan_file(self) -> None:
        """Delete the plan file after approval.

        This prevents stale plans from persisting between sessions.
        """
        plan_path = Path(self._get_plan_file_path())
        if plan_path.exists():
            try:
                plan_path.unlink()
            except OSError:
                pass  # Ignore cleanup errors

    def has_pending_plan(self) -> bool:
        """Check if there's a plan awaiting approval.

        Returns:
            True if a plan has been submitted and is awaiting approval.
        """
        return self._pending_plan is not None

    def get_pending_plan(self) -> Optional[dict]:
        """Get the pending plan if one exists.

        Returns:
            The pending plan dict, or None if no plan is pending.
        """
        return self._pending_plan

    def approve_plan(self) -> str:
        """Approve the pending plan and transition back to code mode.

        This method should be called after the user approves a submitted plan.
        It transitions the agent from plan mode back to code mode, allowing
        it to implement the approved plan.

        Returns:
            The agent's response after transitioning to code mode.
        """
        if not self._pending_plan:
            return "No pending plan to approve."

        plan_content = self._pending_plan.get("plan", "")
        plan_file_path = None

        # Try to get plan file path for reference in the approval message
        # Use session-specific state for concurrent session isolation
        from ..tools.modes import ModeState, AgentMode
        state = ModeState.get_instance(self._session_id)
        plan_file_path = state.get_plan_file_path()

        self._pending_plan = None  # Clear pending plan

        # Cleanup the plan file now that it's approved
        self._cleanup_plan_file()

        # Reset ModeState singleton to code mode
        state.current_mode = AgentMode.CODE
        state.plan_content = plan_content
        state.plan_file_path = None  # Clear plan file path

        # Import AgentToolkit here to avoid circular imports
        from ..toolkit import AgentToolkit
        from ..prompts import build_system_prompt

        # Rebuild toolkit with plan_mode=False (code mode)
        self.toolkit = AgentToolkit(
            connection=self.toolkit.connection,
            repo_root=self.toolkit._repo_root,
            plan_mode=False,
        )
        self.toolkit.set_emitter(self.emitter)

        # Update system prompt back to code mode
        self.system_prompt = build_system_prompt(self.toolkit)

        # Resume execution with approval message
        plan_reference = f"(Plan file: {plan_file_path})" if plan_file_path else ""
        approval_message = f"""Your plan has been APPROVED. {plan_reference}

You are now in code mode. Implement the following plan:

{plan_content}

Proceed with implementation step by step using the available tools."""

        return self.run(approval_message)

    def reject_plan(self, feedback: str = "") -> str:
        """Reject the pending plan and provide feedback.

        The agent remains in plan mode to revise the plan based on feedback.

        Args:
            feedback: Optional feedback explaining why the plan was rejected.

        Returns:
            The agent's response after receiving the rejection.
        """
        if not self._pending_plan:
            return "No pending plan to reject."

        plan_title = self._pending_plan.get("title", "Untitled")
        self._pending_plan = None  # Clear pending plan (but stay in plan mode)

        rejection_message = f"""Your plan "{plan_title}" was REJECTED.

{f"Feedback: {feedback}" if feedback else "Please revise the plan."}

You are still in plan mode. Please address the feedback and submit a revised plan using exit_plan."""

        return self.run(rejection_message)

    def approve_plan_mode(self) -> str:
        """Approve entering plan mode.

        This method should be called after the user approves a plan mode request
        (triggered by enter_plan_mode tool). It transitions the agent into plan mode.

        Returns:
            The agent's response after entering plan mode.
        """
        # Use session-specific state for concurrent session isolation
        from ..tools.modes import ModeState
        state = ModeState.get_instance(self._session_id)

        if not state.plan_mode_requested:
            return "No pending plan mode request."

        reason = state.plan_mode_reason or ""

        # Set the plan file path before approving
        plan_file_path = self._get_plan_file_path()

        # Cleanup any stale plan file to ensure fresh start
        self._cleanup_plan_file()

        state.set_plan_file_path(plan_file_path)

        # Actually enter plan mode
        state.approve_plan_mode()

        # Import here to avoid circular imports
        from ..toolkit import AgentToolkit
        from ..prompts import build_system_prompt

        # Rebuild toolkit with plan_mode=True and plan_file_path
        self.toolkit = AgentToolkit(
            connection=self.toolkit.connection,
            repo_root=self.toolkit._repo_root,
            plan_mode=True,
            plan_file_path=plan_file_path,
        )
        self.toolkit.set_emitter(self.emitter)

        # Main agent uses normal prompt - it delegates to Plan subagent
        self.system_prompt = build_system_prompt(self.toolkit)

        # Resume execution - tell main agent to spawn Plan subagent
        approval_message = f"""Your request to enter plan mode has been APPROVED.

Reason: {reason}

You are now in plan mode. Follow these steps:

1. **Spawn Plan subagent NOW**:
   `task(subagent_type="Plan", prompt="<your planning request>")`

2. **After the Plan subagent returns**, take its response (the plan content) and:
   a) Write it to `{plan_file_path}` using `write_to_file(path="{plan_file_path}", content=<plan>)`
   b) Call `exit_plan()` to present the plan for user approval

Start by spawning the Plan subagent."""

        return self.run(approval_message)

    def reject_plan_mode(self, feedback: str = "") -> str:
        """Reject entering plan mode.

        The agent remains in code mode and continues with the task.

        Args:
            feedback: Optional feedback explaining why plan mode was rejected.

        Returns:
            The agent's response after rejection.
        """
        # Use session-specific state for concurrent session isolation
        from ..tools.modes import ModeState
        state = ModeState.get_instance(self._session_id)

        if not state.plan_mode_requested:
            return "No pending plan mode request."

        # Reset the request
        state.reject_plan_mode()

        rejection_message = f"""Your request to enter plan mode was REJECTED.

{f"Feedback: {feedback}" if feedback else "The user prefers to proceed without detailed planning."}

You are still in code mode. Please proceed with the task directly, or ask for clarification if needed."""

        return self.run(rejection_message)
