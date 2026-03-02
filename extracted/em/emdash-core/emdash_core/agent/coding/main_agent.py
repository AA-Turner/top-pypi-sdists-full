"""Coding main agent implementation.

This module provides the CodingMainAgent - a full-featured coding assistant
that inherits from BaseAgent and adds coding-specific functionality like
file operations, plan mode, and checkpoints.
"""

import json
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from ...utils.logger import log
from ..base import BaseAgent
from ..toolkit import AgentToolkit
from ..prompts import build_system_prompt
from ..events import AgentEventEmitter
from ..providers.factory import DEFAULT_MODEL
from ..tools.base import ToolResult
from ..tools.tasks import TaskState
from ..tools.modes import ModeState, AgentMode
from ...checkpoint import CheckpointManager

if TYPE_CHECKING:
    from ..toolkits.base import BaseToolkit


class CodingMainAgent(BaseAgent):
    """Main agent for coding tasks.

    Extends BaseAgent with:
    - Full CodingToolkit (file ops, execution, search)
    - Plan mode support
    - Git checkpoint creation
    - Code-specific sub-agents (Explorer, Planner, Bash)

    Example:
        agent = CodingMainAgent(
            repo_root=Path.cwd(),
        )
        response = agent.run("Add authentication to the API")
    """

    def __init__(
        self,
        repo_root: Optional[Path] = None,
        model: str = DEFAULT_MODEL,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = 100,
        verbose: bool = False,
        enable_thinking: Optional[bool] = None,
        checkpoint_manager: Optional[CheckpointManager] = None,
        session_id: Optional[str] = None,
        plan_mode: bool = False,
        plan_file_path: Optional[str] = None,
    ):
        """Initialize the coding main agent.

        Args:
            repo_root: Repository root path. Defaults to cwd.
            model: LLM model to use.
            emitter: Event emitter for streaming output.
            max_iterations: Maximum tool call iterations.
            verbose: Whether to print verbose output.
            enable_thinking: Enable extended thinking.
            checkpoint_manager: Optional checkpoint manager for git checkpoints.
            session_id: Session ID for plan file isolation.
            plan_mode: Start in plan mode.
            plan_file_path: Path for plan file in plan mode.
        """
        self.repo_root = repo_root or Path.cwd()
        self._plan_mode = plan_mode
        self._plan_file_path = plan_file_path

        # Checkpoint manager
        self._checkpoint_manager = checkpoint_manager
        self._tools_used_this_run: set[str] = set()

        # Plan state
        self._pending_plan: Optional[dict] = None

        # Todo state tracking
        self._last_todo_snapshot: str = ""

        # Initialize base agent (calls _get_toolkit and _build_system_prompt)
        super().__init__(
            model=model,
            emitter=emitter,
            max_iterations=max_iterations,
            verbose=verbose,
            enable_thinking=enable_thinking,
            session_id=session_id,
        )

    def _get_toolkit(self) -> "BaseToolkit":
        """Return the CodingToolkit."""
        return AgentToolkit(
            repo_root=self.repo_root,
            plan_mode=self._plan_mode,
        )

    def _build_system_prompt(self) -> str:
        """Build the coding-focused system prompt."""
        return build_system_prompt(self.toolkit)

    def _get_available_subagents(self) -> dict[str, str]:
        """Return available coding sub-agents."""
        return {
            "Explore": "Fast codebase exploration - searches files, reads code, finds patterns",
            "Plan": "Designs implementation plans - analyzes architecture, creates step-by-step plans",
            "Bash": "Command execution specialist - runs shell commands",
        }

    @property
    def name(self) -> str:
        """Return the display name for this agent."""
        return "Emdash Code"

    @property
    def agent_type(self) -> str:
        """Return the agent type identifier."""
        return "coding"

    # -------------------------------------------------------------------------
    # Plan mode support
    # -------------------------------------------------------------------------

    def _get_plan_file_path(self) -> str:
        """Get the plan file path."""
        if hasattr(self.toolkit, 'plan_file_path') and self.toolkit.plan_file_path:
            return self.toolkit.plan_file_path
        return str(self.repo_root / ".emdash" / "plan.md")

    def _cleanup_plan_file(self) -> None:
        """Delete the plan file after approval."""
        plan_path = Path(self._get_plan_file_path())
        if plan_path.exists():
            try:
                plan_path.unlink()
            except OSError:
                pass

    def has_pending_plan(self) -> bool:
        """Check if there's a plan awaiting approval."""
        return self._pending_plan is not None

    def get_pending_plan(self) -> Optional[dict]:
        """Get the pending plan if one exists."""
        return self._pending_plan

    def approve_plan(self) -> str:
        """Approve the pending plan and transition to code mode."""
        if not self._pending_plan:
            return "No pending plan to approve."

        plan_content = self._pending_plan.get("plan", "")
        # Use session-specific state for concurrent session isolation
        state = ModeState.get_instance(self._session_id)
        plan_file_path = state.get_plan_file_path()

        self._pending_plan = None
        self._cleanup_plan_file()

        # Reset to code mode
        state.current_mode = AgentMode.CODE
        state.plan_content = plan_content
        state.plan_file_path = None

        # Rebuild toolkit
        self.toolkit = AgentToolkit(
            repo_root=self.repo_root,
            plan_mode=False,
        )
        self.toolkit.set_emitter(self.emitter)
        self.system_prompt = build_system_prompt(self.toolkit)

        plan_reference = f"(Plan file: {plan_file_path})" if plan_file_path else ""
        approval_message = f"""Your plan has been APPROVED. {plan_reference}

You are now in code mode. Implement the following plan:

{plan_content}

Proceed with implementation step by step."""

        return self.run(approval_message)

    def reject_plan(self, feedback: str = "") -> str:
        """Reject the pending plan."""
        if not self._pending_plan:
            return "No pending plan to reject."

        plan_title = self._pending_plan.get("title", "Untitled")
        self._pending_plan = None

        rejection_message = f"""Your plan "{plan_title}" was REJECTED.

{f"Feedback: {feedback}" if feedback else "Please revise the plan."}

You are still in plan mode. Submit a revised plan using exit_plan."""

        return self.run(rejection_message)

    def approve_plan_mode(self) -> str:
        """Approve entering plan mode."""
        # Use session-specific state for concurrent session isolation
        state = ModeState.get_instance(self._session_id)

        if not state.plan_mode_requested:
            return "No pending plan mode request."

        reason = state.plan_mode_reason or ""
        plan_file_path = self._get_plan_file_path()
        self._cleanup_plan_file()
        state.set_plan_file_path(plan_file_path)
        state.approve_plan_mode()

        # Rebuild toolkit
        self.toolkit = AgentToolkit(
            repo_root=self.repo_root,
            plan_mode=True,
            plan_file_path=plan_file_path,
        )
        self.toolkit.set_emitter(self.emitter)
        self.system_prompt = build_system_prompt(self.toolkit)

        approval_message = f"""Your request to enter plan mode has been APPROVED.

Reason: {reason}

You are now in plan mode. Spawn the Plan subagent to create your plan, then call exit_plan."""

        return self.run(approval_message)

    def reject_plan_mode(self, feedback: str = "") -> str:
        """Reject entering plan mode."""
        # Use session-specific state for concurrent session isolation
        state = ModeState.get_instance(self._session_id)

        if not state.plan_mode_requested:
            return "No pending plan mode request."

        state.reject_plan_mode()

        rejection_message = f"""Your request to enter plan mode was REJECTED.

{f"Feedback: {feedback}" if feedback else "Proceed without detailed planning."}

You are still in code mode. Proceed with the task directly."""

        return self.run(rejection_message)

    # -------------------------------------------------------------------------
    # Hooks
    # -------------------------------------------------------------------------

    def _on_tool_result(self, tool_name: str, result: ToolResult) -> None:
        """Handle coding-specific tool results."""
        self._tools_used_this_run.add(tool_name)

    def _on_run_complete(self, response: str) -> None:
        """Create checkpoint after successful run."""
        if not self._checkpoint_manager:
            return

        try:
            self._checkpoint_manager.create_checkpoint(
                messages=self._messages,
                model=self.model,
                system_prompt=self.system_prompt,
                tools_used=list(self._tools_used_this_run),
                token_usage={
                    "input": self._total_input_tokens,
                    "output": self._total_output_tokens,
                    "thinking": self._total_thinking_tokens,
                },
            )
        except Exception as e:
            log.warning(f"Failed to create checkpoint: {e}")
        finally:
            self._tools_used_this_run.clear()

    # -------------------------------------------------------------------------
    # Todo state helpers
    # -------------------------------------------------------------------------

    def _get_todo_snapshot(self) -> str:
        """Get current todo state for comparison."""
        state = TaskState.get_instance()
        return json.dumps(state.get_all_tasks(), sort_keys=True)

    def _format_todo_reminder(self) -> str:
        """Format current todos as reminder."""
        state = TaskState.get_instance()
        tasks = state.get_all_tasks()
        if not tasks:
            return ""

        counts = {"pending": 0, "in_progress": 0, "completed": 0}
        lines = []
        for t in tasks:
            status = t.get("status", "pending")
            counts[status] = counts.get(status, 0) + 1
            icon = {"pending": "[ ]", "in_progress": "[>]", "completed": "[x]"}.get(status, "?")
            lines.append(f'  {t["id"]}. {icon} {t["title"]}')

        header = f'Tasks: {counts["completed"]} done, {counts["in_progress"]} active, {counts["pending"]} pending'
        return f"<todo-state>\n{header}\n" + "\n".join(lines) + "\n</todo-state>"

    # -------------------------------------------------------------------------
    # Clarification handling
    # -------------------------------------------------------------------------

    def answer_clarification(self, answer: str) -> str:
        """Answer a pending clarification question."""
        state = TaskState.get_instance()
        pending_question = state.pending_question

        state.pending_question = None
        state.user_response = answer

        if pending_question:
            context_message = f"[User answered the clarification]\nQuestion: {pending_question}\nAnswer: {answer}"
        else:
            context_message = f"[User response]: {answer}"

        return self.chat(context_message)

    def answer_choice_questions(self, responses: list[dict]) -> str:
        """Answer pending choice questions."""
        state = TaskState.get_instance()
        pending_choices = state.pending_choices
        context = state.choice_context or "approach"

        state.clear_pending_choices()
        state.choice_responses = responses

        if pending_choices:
            lines = [f"[User made {context} selections]"]
            for i, resp in enumerate(responses):
                question = resp.get("question", f"Choice {i+1}")
                answer = resp.get("answer", "")
                lines.append(f"- {question}: {answer}")
            context_message = "\n".join(lines)
        else:
            context_message = f"[User selections]: {responses}"

        return self.chat(context_message)

    # -------------------------------------------------------------------------
    # Properties for backwards compatibility
    # -------------------------------------------------------------------------

    @property
    def connection(self):
        """Get database connection from toolkit."""
        return getattr(self.toolkit, 'connection', None)

    @property
    def plan_mode(self) -> bool:
        """Check if in plan mode."""
        return self._plan_mode
