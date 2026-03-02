"""Task tool for spawning sub-agents.

Follows Claude Code's Task tool pattern - spawns specialized sub-agents
for focused tasks like exploration, planning, and coding.

Uses in-process execution for better UX (real-time events) while
maintaining isolated message histories per sub-agent.

Simple two-layer model:
- Main agent can spawn Explore, Plan, Coder sub-agents
- Sub-agents cannot spawn further (they don't have the task tool)
"""

from pathlib import Path
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ..toolkits import list_agent_types
from ..inprocess_subagent import run_subagent, run_subagent_async
from ..background import BackgroundTaskManager
from ...utils.logger import log


class TaskTool(BaseTool):
    """Spawn a sub-agent to handle complex, multi-step tasks autonomously.

    The Task tool launches specialized agents in-process with isolated
    message histories. Each agent type has specific capabilities:

    - **Explore**: Fast codebase exploration using read_file, glob, grep, semantic_search
    - **Plan**: Design implementation plans, can write to .emdash/plans/*.md
    - **Coder**: Code implementation with full write access (cannot spawn sub-agents)

    Sub-agents run with their own context and tools, returning a summary when done.
    Events are tagged with agent_id to prevent mixing in the UI.
    """

    name = "task"
    description = """Launch a specialized sub-agent for focused tasks.

Use this to spawn lightweight agents for:
- Fast codebase exploration (Explore agent)
- Implementation planning (Plan agent)
- Code implementation (Coder agent)

Sub-agents run autonomously and return structured results.
Multiple sub-agents can be launched in parallel."""
    category = ToolCategory.PLANNING

    def __init__(
        self,
        repo_root: Path,
        connection=None,
        emitter=None,
    ):
        """Initialize with repo root.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used)
            emitter: Optional event emitter for progress events
        """
        self.repo_root = repo_root.resolve()
        self.connection = connection
        self.emitter = emitter

    def execute(
        self,
        description: str = "",
        prompt: str = "",
        subagent_type: str = "Explore",
        model_tier: str = "fast",
        max_turns: int = 10,
        run_in_background: bool = False,
        resume: Optional[str] = None,
        thoroughness: str = "medium",
        **kwargs,
    ) -> ToolResult:
        """Spawn a sub-agent to perform a task.

        Args:
            description: Short (3-5 word) description of the task
            prompt: The task for the agent to perform
            subagent_type: Type of agent (Explore, Plan, Coder)
            model_tier: Model tier (fast, standard, powerful)
            max_turns: Maximum API round-trips
            run_in_background: Run asynchronously
            resume: Agent ID to resume from
            thoroughness: Search thoroughness level (quick, medium, thorough)

        Returns:
            ToolResult with agent results or background task info
        """
        # Validate inputs
        if not prompt:
            return ToolResult.error_result(
                "Prompt is required",
                suggestions=["Provide a clear task description in 'prompt'"],
            )

        available_types = list_agent_types(self.repo_root)
        log.info(f"TaskTool: repo_root={self.repo_root}, available_types={available_types}")
        if subagent_type not in available_types:
            return ToolResult.error_result(
                f"Unknown agent type: {subagent_type}",
                suggestions=[
                    f"Available types: {available_types}",
                    f"Searched in: {self.repo_root / '.emdash' / 'agents'}",
                ],
            )

        # Log current mode for debugging
        from .modes import ModeState
        mode_state = ModeState.get_instance()
        log.info(f"TaskTool: current_mode={mode_state.current_mode}, subagent_type={subagent_type}")

        log.info(
            "Spawning sub-agent type={} model={} prompt={}",
            subagent_type,
            model_tier,
            prompt[:50] + "..." if len(prompt) > 50 else prompt,
        )

        # Emit subagent start event for UI visibility
        if self.emitter:
            from ..events import EventType
            self.emitter.emit(EventType.SUBAGENT_START, {
                "agent_type": subagent_type,
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "description": description,
            })

        if run_in_background:
            return self._run_background(subagent_type, prompt, max_turns, thoroughness, description)
        else:
            return self._run_sync(subagent_type, prompt, max_turns, thoroughness)

    def _run_sync(
        self,
        subagent_type: str,
        prompt: str,
        max_turns: int,
        thoroughness: str = "medium",
    ) -> ToolResult:
        """Run sub-agent synchronously in the same process.

        Args:
            subagent_type: Agent type
            prompt: Task prompt
            max_turns: Maximum API round-trips
            thoroughness: Search thoroughness level

        Returns:
            ToolResult with agent results
        """
        # Plan agents need more turns for thorough exploration and planning
        # Agent stops naturally when done (no more tool calls), this just raises ceiling
        effective_max_turns = max_turns if subagent_type != "Plan" else max(max_turns, 25)

        try:
            result = run_subagent(
                subagent_type=subagent_type,
                prompt=prompt,
                repo_root=self.repo_root,
                emitter=self.emitter,
                max_turns=effective_max_turns,
                thoroughness=thoroughness,
            )

            # Emit subagent end event
            if self.emitter:
                from ..events import EventType
                self.emitter.emit(EventType.SUBAGENT_END, {
                    "agent_type": subagent_type,
                    "success": result.success,
                    "iterations": result.iterations,
                    "files_explored": len(result.files_explored),
                    "execution_time": result.execution_time,
                    "usage": result.usage,
                })

            if result.success:
                # Build result with status=completed to clearly indicate sync completion
                # IMPORTANT: Do NOT include agent_id - it causes the LLM to call task_output
                # unnecessarily thinking there's more data to fetch
                sync_result = {
                    "status": "completed",  # Key: task is DONE, do NOT call task_output
                    "agent_type": result.agent_type,
                    "summary": result.summary,  # The main content
                    "success": result.success,
                    "iterations": result.iterations,
                    "execution_time": result.execution_time,
                    "files_explored": result.files_explored,
                    "tools_used": result.tools_used,
                    "usage": result.usage,  # Token usage from sub-agent
                }

                # For Plan agents, check if a plan file was written
                if subagent_type == "Plan":
                    plan_file = self._check_plan_file()
                    if plan_file:
                        sync_result["plan_file"] = plan_file
                        # Truncate summary for Plan agents - the file has full content
                        if len(result.summary) > 500:
                            sync_result["summary"] = result.summary[:500] + f"\n\n[Full plan in {plan_file}]"

                return ToolResult.success_result(
                    data=sync_result,
                    suggestions=self._generate_suggestions(sync_result, completed=True),
                )
            else:
                return ToolResult.error_result(
                    f"Sub-agent failed: {result.error}",
                    suggestions=["Check the prompt and try again"],
                )

        except Exception as e:
            log.exception("Failed to run sub-agent")
            return ToolResult.error_result(f"Failed to run sub-agent: {e}")

    def _run_background(
        self,
        subagent_type: str,
        prompt: str,
        max_turns: int,
        thoroughness: str = "medium",
        description: str = "",
    ) -> ToolResult:
        """Run sub-agent in background using a thread.

        Args:
            subagent_type: Agent type
            prompt: Task prompt
            max_turns: Maximum API round-trips
            thoroughness: Search thoroughness level
            description: Short task description

        Returns:
            ToolResult with task info
        """
        # Plan agents need more turns for thorough exploration and planning
        effective_max_turns = max_turns if subagent_type != "Plan" else max(max_turns, 25)

        try:
            # Start async execution
            future = run_subagent_async(
                subagent_type=subagent_type,
                prompt=prompt,
                repo_root=self.repo_root,
                emitter=self.emitter,
                max_turns=effective_max_turns,
                thoroughness=thoroughness,
            )

            # Register with BackgroundTaskManager for notification support
            manager = BackgroundTaskManager.get_instance()
            task_id = manager.start_subagent(
                future=future,
                agent_type=subagent_type,
                description=description or prompt[:50],
            )

            log.info(f"Started background agent {task_id}")

            return ToolResult.success_result(
                data={
                    "task_id": task_id,
                    "status": "running",
                    "agent_type": subagent_type,
                    "message": "Sub-agent started in background. Continue with other work - you'll be notified when it completes.",
                },
                suggestions=[
                    "Continue working on other tasks while waiting",
                    f"Only call task_output(task_id='{task_id}') if you need to check progress",
                    f"Use kill_task(task_id='{task_id}') to stop it",
                ],
            )

        except Exception as e:
            log.exception("Failed to start background agent")
            return ToolResult.error_result(f"Failed to start background agent: {e}")

    def _check_plan_file(self) -> str | None:
        """Check if a plan file was recently written by the Plan subagent.

        Returns:
            Path to the most recently modified plan file, or None
        """
        import time

        plans_dir = self.repo_root / ".emdash" / "plans"
        if not plans_dir.exists():
            return None

        # Find plan files modified in the last 2 minutes
        cutoff_time = time.time() - 120
        recent_plans = []

        for plan_file in plans_dir.glob("*.md"):
            try:
                if plan_file.stat().st_mtime > cutoff_time:
                    recent_plans.append(plan_file)
            except OSError:
                continue

        if not recent_plans:
            return None

        # Return the most recently modified plan
        most_recent = max(recent_plans, key=lambda p: p.stat().st_mtime)
        return str(most_recent.relative_to(self.repo_root))

    def _generate_suggestions(self, data: dict, completed: bool = False) -> list[str]:
        """Generate follow-up suggestions based on results.

        Args:
            data: Result data dict
            completed: If True, task completed synchronously (don't suggest task_output)
        """
        suggestions = []

        files = data.get("files_explored", [])
        if files:
            suggestions.append(f"Found {len(files)} relevant files")

        if data.get("agent_type") == "Plan":
            if data.get("plan_file"):
                suggestions.append(f"Plan written to: {data['plan_file']}")
                if completed:
                    suggestions.append("Read the plan file to see full content")
            else:
                suggestions.append("Review the plan in .emdash/plans/")

        # Only suggest agent_id for background tasks (not completed sync tasks)
        if not completed and data.get("agent_id"):
            suggestions.append(f"Agent ID: {data['agent_id']} (use task_output to check status)")

        if completed:
            suggestions.append("Task completed - no need to call task_output")

        return suggestions

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        # Get available agent types dynamically (includes custom agents)
        available_types = list_agent_types(self.repo_root)

        return self._make_schema(
            properties={
                "description": {
                    "type": "string",
                    "description": "Short (3-5 word) description of the task",
                },
                "prompt": {
                    "type": "string",
                    "description": "The task for the agent to perform",
                },
                "subagent_type": {
                    "type": "string",
                    "enum": available_types,
                    "description": f"Type of specialized agent. Available: {', '.join(available_types)}",
                    "default": "Explore",
                },
                "model_tier": {
                    "type": "string",
                    "enum": ["fast", "model"],
                    "description": "Model tier (fast=cheap/quick, model=standard)",
                    "default": "fast",
                },
                "max_turns": {
                    "type": "integer",
                    "description": "Maximum API round-trips",
                    "default": 10,
                },
                "run_in_background": {
                    "type": "boolean",
                    "description": "Run agent asynchronously",
                    "default": False,
                },
                "resume": {
                    "type": "string",
                    "description": "Agent ID to resume from previous execution",
                },
                "thoroughness": {
                    "type": "string",
                    "enum": ["quick", "medium", "thorough"],
                    "description": "Search thoroughness: quick (basic searches), medium (moderate exploration), thorough (comprehensive analysis)",
                    "default": "medium",
                },
            },
            required=["prompt"],
        )
