"""LLM-callable tools for Agent Teams coordination.

These tools are registered on teammate toolkits (and the lead's toolkit)
so the LLM can coordinate with other agents programmatically.

Tool categories:
  - LEAD-ONLY: spawn_teammate, shutdown_teammate, assign_task, approve_plan
  - ALL AGENTS: team_send_message, team_get_messages, team_get_status
  - TEAMMATES: (use standard Tasks v2 tools: claim_todo, complete_todo, etc.)
"""

from typing import Any, Optional

from ..tools.base import BaseTool, ToolResult, ToolCategory
from .models import TeamConfig, MessageType
from .messaging import MessageBroker


# ─────────────────────────────────────────────────────────────
# Tools available to ALL agents (lead + teammates)
# ─────────────────────────────────────────────────────────────


class TeamSendMessageTool(BaseTool):
    """Send a message to another teammate or the lead."""

    name = "team_send_message"
    description = """Send a message to another agent in your team.

Use this to:
- Share findings with the lead or other teammates
- Ask another teammate a question
- Submit your plan for approval (type="plan_submitted")
- Report task completion details

Examples:
  team_send_message(to="lead", content="Found 3 SQL injection vulnerabilities in auth/")
  team_send_message(to="frontend-dev", content="The API schema changed, see models.py")
  team_send_message(to="lead", content="<plan>...</plan>", type="plan_submitted")
"""
    category = ToolCategory.COMMUNICATION

    def __init__(self, broker: MessageBroker, agent_name: str, team_config: TeamConfig):
        self._broker = broker
        self._agent_name = agent_name
        self._team_config = team_config

    def execute(
        self,
        to: str,
        content: str,
        type: str = "message",
        **kwargs,
    ) -> ToolResult:
        """Send a message.

        Args:
            to: Recipient name ("lead", teammate name, or "all" for broadcast).
            content: Message body (markdown).
            type: Message type (message, plan_submitted, findings_report, task_update).
        """
        if not to or not content:
            return ToolResult.error_result("Both 'to' and 'content' are required")

        # Validate recipient exists
        if to != "all" and to != "lead":
            member = self._team_config.get_member(to)
            if not member:
                available = [m.name for m in self._team_config.members]
                return ToolResult.error_result(
                    f"Unknown recipient '{to}'. Available: {['lead'] + available}"
                )

        try:
            msg_type = MessageType(type)
        except ValueError:
            msg_type = MessageType.MESSAGE

        if to == "all":
            # Broadcast to all except self
            msg_ids = []
            recipients = []
            for member in self._team_config.members:
                if member.name != self._agent_name:
                    msg_id = self._broker.send(
                        from_agent=self._agent_name,
                        to_agent=member.name,
                        content=content,
                        message_type=msg_type,
                    )
                    msg_ids.append(msg_id)
                    recipients.append(member.name)
            # Also send to lead if we're not lead
            if self._agent_name != "lead":
                msg_id = self._broker.send(
                    from_agent=self._agent_name,
                    to_agent="lead",
                    content=content,
                    message_type=msg_type,
                )
                msg_ids.append(msg_id)
                recipients.append("lead")

            return ToolResult.success_result({
                "broadcast": True,
                "recipients": recipients,
                "message_ids": msg_ids,
            })
        else:
            msg_id = self._broker.send(
                from_agent=self._agent_name,
                to_agent=to,
                content=content,
                message_type=msg_type,
            )
            return ToolResult.success_result({
                "message_id": msg_id,
                "to": to,
                "type": type,
            })

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "to": {
                    "type": "string",
                    "description": "Recipient: 'lead', a teammate name, or 'all' for broadcast",
                },
                "content": {
                    "type": "string",
                    "description": "Message body (markdown)",
                },
                "type": {
                    "type": "string",
                    "enum": [
                        "message", "plan_submitted", "findings_report",
                        "task_update", "task_completed",
                    ],
                    "description": "Message type (default: message)",
                    "default": "message",
                },
            },
            required=["to", "content"],
        )


class TeamGetMessagesTool(BaseTool):
    """Check for new messages from other agents."""

    name = "team_get_messages"
    description = """Check your mailbox for new messages from teammates or the lead.

Call this between major steps to stay coordinated.
Messages are marked as read after retrieval.

Returns list of messages with sender, type, and content.
"""
    category = ToolCategory.COMMUNICATION

    def __init__(self, broker: MessageBroker, agent_name: str):
        self._broker = broker
        self._agent_name = agent_name

    def execute(self, **kwargs) -> ToolResult:
        """Get pending messages."""
        messages = self._broker.receive(self._agent_name)

        if not messages:
            return ToolResult.success_result({
                "count": 0,
                "messages": [],
                "note": "No new messages.",
            })

        return ToolResult.success_result({
            "count": len(messages),
            "messages": [
                {
                    "id": m.id,
                    "from": m.from_agent,
                    "type": m.message_type.value,
                    "content": m.content,
                    "timestamp": m.timestamp,
                }
                for m in messages
            ],
        })

    def get_schema(self) -> dict:
        return self._make_schema(properties={}, required=[])


class TeamGetStatusTool(BaseTool):
    """Get current team status: members, tasks, and progress."""

    name = "team_get_status"
    description = """Get the current status of your agent team.

Shows:
- Team members and their status (working, idle, stopped)
- Task list progress (pending, in_progress, completed)
- Per-teammate task assignments

Use this to understand what others are working on before claiming tasks.
"""
    category = ToolCategory.COMMUNICATION

    def __init__(self, team_config: TeamConfig):
        self._team_config = team_config

    def execute(self, **kwargs) -> ToolResult:
        """Get team status."""
        members = []
        for m in self._team_config.members:
            members.append({
                "name": m.name,
                "status": m.status.value,
                "labels": m.labels,
                "role": m.role.value,
            })

        # Get task summary if available
        task_summary = None
        if self._team_config.task_list_id:
            try:
                from .tasks import get_team_task_summary
                task_summary = get_team_task_summary(self._team_config.task_list_id)
            except Exception:
                pass

        return ToolResult.success_result({
            "team_name": self._team_config.name,
            "status": self._team_config.status.value,
            "delegate_mode": self._team_config.delegate_mode,
            "lead": self._team_config.lead.name if self._team_config.lead else None,
            "members": members,
            "tasks": task_summary,
        })

    def get_schema(self) -> dict:
        return self._make_schema(properties={}, required=[])


# ─────────────────────────────────────────────────────────────
# Tools available to LEAD only
# ─────────────────────────────────────────────────────────────


class SpawnTeammateTool(BaseTool):
    """Spawn a new teammate agent session."""

    name = "spawn_teammate"
    description = """Spawn a new teammate to work on part of the task.

Each teammate is an independent agent with its own context window.
Give them a clear, focused role and specific instructions.

Args:
    name: Short name (e.g., "security-reviewer", "frontend-dev")
    prompt: Detailed instructions for what the teammate should do
    model: LLM model to use (optional, defaults to your model)
    labels: Task labels this teammate should focus on (e.g., ["backend", "auth"])
    require_plan_approval: If true, teammate must plan before implementing

Example:
    spawn_teammate(
        name="security-reviewer",
        prompt="Review src/auth/ for security vulnerabilities. Focus on token handling, session management, and input validation.",
        labels=["security", "auth"],
    )
"""
    category = ToolCategory.COMMUNICATION

    def __init__(self, team_manager: "TeamManager"):
        self._manager = team_manager

    def execute(
        self,
        name: str,
        prompt: str,
        model: str = "",
        labels: list[str] | None = None,
        require_plan_approval: bool = False,
        use_worktree: bool = False,
        **kwargs,
    ) -> ToolResult:
        """Spawn a teammate."""
        if not name or not prompt:
            return ToolResult.error_result("Both 'name' and 'prompt' are required")

        try:
            handle = self._manager.spawn_teammate(
                name=name,
                prompt=prompt,
                model=model,
                labels=labels,
                require_plan_approval=require_plan_approval,
                use_worktree=use_worktree,
            )
            return ToolResult.success_result({
                "name": name,
                "agent_id": handle.agent_id,
                "status": "spawned",
                "labels": labels or [],
                "plan_mode": require_plan_approval,
                "message": f"Teammate '{name}' spawned and working.",
            })
        except ValueError as e:
            return ToolResult.error_result(str(e))

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "name": {
                    "type": "string",
                    "description": "Short name for the teammate (e.g., 'security-reviewer')",
                },
                "prompt": {
                    "type": "string",
                    "description": "Detailed instructions for what the teammate should do",
                },
                "model": {
                    "type": "string",
                    "description": "LLM model override (optional)",
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Task labels this teammate should focus on",
                },
                "require_plan_approval": {
                    "type": "boolean",
                    "description": "If true, teammate must plan before implementing",
                    "default": False,
                },
                "use_worktree": {
                    "type": "boolean",
                    "description": "Create a git worktree for file isolation",
                    "default": False,
                },
            },
            required=["name", "prompt"],
        )


class CreateTeamTaskTool(BaseTool):
    """Create a task in the team's shared task list."""

    name = "create_team_task"
    description = """Create a task for the team to work on.

Tasks appear in the shared task list. Teammates claim tasks using
their labels. Use depends_on to express ordering constraints.

Args:
    title: Short task title
    description: Detailed description of what needs to be done
    labels: Labels for categorization (teammates filter by label)
    depends_on: Task IDs that must complete before this task
    priority: Higher = more important
    assigned_to: Teammate name to auto-assign (optional)

Example:
    create_team_task(
        title="Review auth token handling",
        description="Check for token expiry, refresh, and revocation",
        labels=["security", "auth"],
        priority=2,
    )
"""
    category = ToolCategory.PLANNING

    def __init__(self, team_manager: "TeamManager"):
        self._manager = team_manager

    def execute(
        self,
        title: str,
        description: str = "",
        labels: list[str] | None = None,
        depends_on: list[str] | None = None,
        priority: int = 0,
        assigned_to: str | None = None,
        **kwargs,
    ) -> ToolResult:
        """Create a team task."""
        if not title:
            return ToolResult.error_result("Task title is required")

        # Resolve assigned_to name to agent_id
        assigned_agent_id = None
        if assigned_to:
            member = self._manager.config.get_member(assigned_to)
            if member:
                assigned_agent_id = member.agent_id
            else:
                return ToolResult.error_result(f"Unknown teammate: '{assigned_to}'")

        try:
            from .tasks import create_team_task

            result = create_team_task(
                task_list_id=self._manager.task_list_id,
                title=title,
                description=description,
                labels=labels,
                depends_on=depends_on,
                priority=priority,
                assigned_to=assigned_agent_id,
                created_by="lead",
            )

            return ToolResult.success_result(result)
        except Exception as e:
            return ToolResult.error_result(str(e))

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "title": {
                    "type": "string",
                    "description": "Short task title",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description",
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Labels for teammate filtering (e.g., ['backend', 'security'])",
                },
                "depends_on": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Task IDs that must complete before this task",
                },
                "priority": {
                    "type": "integer",
                    "description": "Priority (higher = more important)",
                    "default": 0,
                },
                "assigned_to": {
                    "type": "string",
                    "description": "Teammate name to auto-assign (optional)",
                },
            },
            required=["title"],
        )


class ShutdownTeammateTool(BaseTool):
    """Request a teammate to shut down gracefully."""

    name = "shutdown_teammate"
    description = """Request a teammate to shut down.

The teammate finishes its current operation and stops.
It can reject the request if it has unfinished critical work.

Example: shutdown_teammate(name="security-reviewer")
"""
    category = ToolCategory.COMMUNICATION

    def __init__(self, team_manager: "TeamManager"):
        self._manager = team_manager

    def execute(self, name: str, **kwargs) -> ToolResult:
        """Request shutdown."""
        if not name:
            return ToolResult.error_result("Teammate name is required")

        member = self._manager.config.get_member(name)
        if not member:
            return ToolResult.error_result(f"Unknown teammate: '{name}'")

        # Send shutdown message (async handling deferred to manager)
        self._manager.send_message(
            from_name="lead",
            to_name=name,
            content="Shutdown requested. Please finish current work and stop.",
            message_type="shutdown_request",
        )

        return ToolResult.success_result({
            "name": name,
            "status": "shutdown_requested",
            "message": f"Shutdown request sent to '{name}'.",
        })

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "name": {
                    "type": "string",
                    "description": "Name of the teammate to shut down",
                },
            },
            required=["name"],
        )


class ApprovePlanTool(BaseTool):
    """Approve or reject a teammate's implementation plan."""

    name = "approve_plan"
    description = """Approve or reject a teammate's plan.

When a teammate in plan mode submits a plan via team_send_message,
use this tool to approve it (letting them proceed to implementation)
or reject it with feedback (sending them back to revise).

Args:
    teammate: Name of the teammate whose plan to approve/reject
    approved: True to approve, False to reject
    feedback: Feedback message (required if rejecting)
"""
    category = ToolCategory.COMMUNICATION

    def __init__(self, team_manager: "TeamManager"):
        self._manager = team_manager

    def execute(
        self,
        teammate: str,
        approved: bool = True,
        feedback: str = "",
        **kwargs,
    ) -> ToolResult:
        """Approve or reject a plan."""
        if not teammate:
            return ToolResult.error_result("Teammate name is required")

        if not approved and not feedback:
            return ToolResult.error_result("Feedback is required when rejecting a plan")

        msg_type = "plan_approved" if approved else "plan_rejected"
        content = feedback or "Plan approved. Proceed with implementation."

        self._manager.send_message(
            from_name="lead",
            to_name=teammate,
            content=content,
            message_type=msg_type,
        )

        return ToolResult.success_result({
            "teammate": teammate,
            "approved": approved,
            "feedback": content,
        })

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "teammate": {
                    "type": "string",
                    "description": "Teammate name",
                },
                "approved": {
                    "type": "boolean",
                    "description": "True to approve, False to reject",
                    "default": True,
                },
                "feedback": {
                    "type": "string",
                    "description": "Feedback message (required if rejecting)",
                },
            },
            required=["teammate"],
        )
