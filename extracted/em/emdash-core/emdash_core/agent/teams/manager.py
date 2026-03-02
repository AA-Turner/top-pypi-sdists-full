"""TeamManager — central orchestrator for agent team lifecycle.

Responsibilities:
  1. Create/load/cleanup team configuration
  2. Spawn and shut down teammate agent sessions
  3. Wire up messaging, task lists, and event bridges
  4. Manage delegate mode for the lead

Design decisions:
  - Server-native: teammates are AgentRunner instances in the same process,
    each on its own thread (matching InProcessSubAgent pattern).
  - Tasks v2 integration: the shared task list IS a Tasks v2 task list,
    so teammates use the existing claim/complete/wait tools.
  - Messaging: file-based mailbox with asyncio.Event notifications for
    in-process delivery and file watching for cross-process.

Usage:
    manager = TeamManager(team_name="pr-review", repo_root=Path("."))
    manager.create_team(lead_agent_id="session-abc")

    handle = manager.spawn_teammate(
        name="security-reviewer",
        prompt="Review auth/ for vulnerabilities",
        model="claude-sonnet-4-5-20250929",
    )

    # Teammate runs autonomously on a background thread
    # Lead communicates via manager.send_message() and shared task list

    manager.shutdown_teammate("security-reviewer")
    manager.cleanup()
"""

import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ...utils.logger import log
from .models import (
    TeamConfig,
    TeamStatus,
    TeammateConfig,
    TeammateRole,
    TeammateStatus,
    TeamEventType,
)
from .teammate import TeammateHandle
from .messaging import MessageBroker
from .events import TeamEventBridge


def is_agent_teams_enabled() -> bool:
    """Check if agent teams feature is enabled.

    Checks in order (first truthy wins):
        1. EMDASH_EXPERIMENTAL_AGENT_TEAMS env var
        2. emdash.config.json → experimental.agent_teams
    """
    from ...core.config import get_config
    return get_config().experimental.agent_teams


def get_teams_dir() -> Path:
    """Get the base directory for team storage."""
    return Path.home() / ".emdash" / "teams"


class TeamManager:
    """Central orchestrator for an agent team.

    One TeamManager per team. The lead's session creates and owns it.
    Teammates are spawned as background threads with their own AgentRunner.
    """

    def __init__(
        self,
        team_name: str,
        repo_root: Path,
        lead_agent_id: str | None = None,
        emitter=None,
    ):
        """Initialize the team manager.

        Args:
            team_name: Unique name for this team (used as directory name).
            repo_root: Working directory for the project.
            lead_agent_id: Agent/session ID of the lead. None if loading existing.
            emitter: AgentEventEmitter from the lead's session.
        """
        self._team_name = team_name
        self._repo_root = repo_root
        self._team_dir = get_teams_dir() / team_name
        self._config_path = self._team_dir / "config.json"
        self._emitter = emitter

        # Runtime state (not persisted — rebuilt on load)
        self._handles: dict[str, TeammateHandle] = {}  # name -> handle
        self._executor = ThreadPoolExecutor(
            max_workers=12, thread_name_prefix=f"team-{team_name}"
        )
        self._broker: MessageBroker | None = None
        self._event_bridge: TeamEventBridge | None = None

        # Load or create config
        if self._config_path.exists():
            self._config = self._load_config()
        elif lead_agent_id:
            self._config = self._create_config(lead_agent_id)
        else:
            raise ValueError(
                f"Team '{team_name}' does not exist and no lead_agent_id provided"
            )

    # ─────────────────────────────────────────────────────────
    # Properties
    # ─────────────────────────────────────────────────────────

    @property
    def config(self) -> TeamConfig:
        return self._config

    @property
    def team_name(self) -> str:
        return self._team_name

    @property
    def task_list_id(self) -> str:
        return self._config.task_list_id

    @property
    def is_delegate_mode(self) -> bool:
        return self._config.delegate_mode

    @property
    def broker(self) -> "MessageBroker":
        if self._broker is None:
            self._broker = MessageBroker(self._team_dir / "mailbox")
        return self._broker

    # ─────────────────────────────────────────────────────────
    # Team lifecycle
    # ─────────────────────────────────────────────────────────

    def _create_config(self, lead_agent_id: str) -> TeamConfig:
        """Create a new team and persist initial config."""
        now = datetime.now().isoformat()

        # Create the shared task list via Tasks v2
        task_list_id = f"team-{self._team_name}"

        lead = TeammateConfig(
            name="lead",
            agent_id=lead_agent_id,
            role=TeammateRole.LEAD,
            status=TeammateStatus.WORKING,
            spawned_at=now,
        )

        config = TeamConfig(
            name=self._team_name,
            status=TeamStatus.CREATING,
            lead=lead,
            task_list_id=task_list_id,
            repo_root=str(self._repo_root),
            created_at=now,
            updated_at=now,
        )

        self._save_config(config)
        self._emit_event(TeamEventType.TEAM_CREATED, {
            "team_name": self._team_name,
            "task_list_id": task_list_id,
        })

        log.info(f"Created agent team '{self._team_name}' with lead {lead_agent_id}")
        return config

    def _load_config(self) -> TeamConfig:
        """Load existing team config from disk."""
        data = json.loads(self._config_path.read_text())
        return TeamConfig.from_dict(data)

    def _save_config(self, config: TeamConfig | None = None) -> None:
        """Persist team config to disk."""
        config = config or self._config
        config.updated_at = datetime.now().isoformat()
        self._team_dir.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(
            json.dumps(config.to_dict(), indent=2) + "\n"
        )

    def activate(self) -> None:
        """Transition team from CREATING to ACTIVE."""
        self._config.status = TeamStatus.ACTIVE
        self._save_config()

    # ─────────────────────────────────────────────────────────
    # Teammate spawning
    # ─────────────────────────────────────────────────────────

    def spawn_teammate(
        self,
        name: str,
        prompt: str,
        model: str = "",
        labels: list[str] | None = None,
        require_plan_approval: bool = False,
        use_worktree: bool = False,
    ) -> TeammateHandle:
        """Spawn a new teammate agent session.

        Args:
            name: Human-readable name (e.g., "security-reviewer").
            prompt: Initial instructions for the teammate.
            model: LLM model override. Empty string = use lead's model.
            labels: Task labels this teammate should work on.
            require_plan_approval: If True, teammate starts in plan mode.
            use_worktree: If True, create a git worktree for isolation.

        Returns:
            TeammateHandle for interacting with the new teammate.

        Raises:
            ValueError: If name already exists or team is at max capacity.
        """
        # Validate
        if self._config.get_member(name):
            raise ValueError(f"Teammate '{name}' already exists in team")

        max_teammates = self._config.settings.get("max_teammates", 10)
        if len(self._config.members) >= max_teammates:
            raise ValueError(
                f"Team is at max capacity ({max_teammates} teammates)"
            )

        # Create teammate config
        agent_id = f"teammate-{name}-{uuid.uuid4().hex[:8]}"
        now = datetime.now().isoformat()

        teammate_config = TeammateConfig(
            name=name,
            agent_id=agent_id,
            role=TeammateRole.TEAMMATE,
            model=model,
            status=TeammateStatus.SPAWNING,
            spawn_prompt=prompt,
            require_plan_approval=require_plan_approval,
            labels=labels or [],
            spawned_at=now,
        )

        # Optionally create git worktree
        worktree_path = None
        if use_worktree:
            worktree_path = self._create_worktree(name)
            teammate_config.worktree_path = str(worktree_path)

        # Register in config
        self._config.members.append(teammate_config)
        self._save_config()

        # Create the runtime handle (does NOT start the agent yet)
        handle = TeammateHandle(
            config=teammate_config,
            team_config=self._config,
            repo_root=Path(worktree_path) if worktree_path else self._repo_root,
            broker=self.broker,
            parent_emitter=self._emitter,
        )
        self._handles[name] = handle

        # Start the agent on a background thread
        handle.start(self._executor)

        self._emit_event(TeamEventType.TEAMMATE_SPAWNED, {
            "name": name,
            "agent_id": agent_id,
            "model": model or "(default)",
            "labels": labels or [],
            "plan_mode": require_plan_approval,
        })

        log.info(f"Spawned teammate '{name}' (agent_id={agent_id})")
        return handle

    def _create_worktree(self, name: str) -> Path:
        """Create a git worktree for a teammate.

        Returns the worktree path.
        """
        import subprocess

        worktree_dir = self._team_dir / "worktrees" / name
        branch_name = f"team/{self._team_name}/{name}"

        subprocess.run(
            ["git", "worktree", "add", "-b", branch_name, str(worktree_dir)],
            cwd=str(self._repo_root),
            check=True,
            capture_output=True,
        )

        log.info(f"Created worktree for '{name}' at {worktree_dir}")
        return worktree_dir

    # ─────────────────────────────────────────────────────────
    # Teammate control
    # ─────────────────────────────────────────────────────────

    def get_handle(self, name: str) -> TeammateHandle | None:
        """Get the runtime handle for a teammate."""
        return self._handles.get(name)

    def get_all_handles(self) -> dict[str, TeammateHandle]:
        """Get all teammate handles."""
        return dict(self._handles)

    def send_message(
        self,
        from_name: str,
        to_name: str,
        content: str,
        message_type: str = "message",
    ) -> str:
        """Send a message between agents.

        Args:
            from_name: Sender name (e.g., "lead", "security-reviewer").
            to_name: Recipient name (or "all" for broadcast).
            content: Message body.
            message_type: Type of message.

        Returns:
            Message ID.
        """
        from .models import MessageType

        msg_type = MessageType(message_type)
        msg_id = self.broker.send(
            from_agent=from_name,
            to_agent=to_name,
            content=content,
            message_type=msg_type,
        )

        self._emit_event(TeamEventType.TEAM_MESSAGE_SENT, {
            "from": from_name,
            "to": to_name,
            "type": message_type,
            "message_id": msg_id,
        })

        return msg_id

    def broadcast(self, from_name: str, content: str) -> list[str]:
        """Broadcast a message to all active teammates.

        Returns list of message IDs (one per recipient).
        """
        msg_ids = []
        for member in self._config.get_active_members():
            if member.name != from_name:
                msg_id = self.send_message(
                    from_name=from_name,
                    to_name=member.name,
                    content=content,
                    message_type="broadcast",
                )
                msg_ids.append(msg_id)
        return msg_ids

    async def shutdown_teammate(self, name: str) -> bool:
        """Request graceful shutdown of a teammate.

        Sends a shutdown request. The teammate can accept or reject.
        Returns True if shutdown was acknowledged.
        """
        handle = self._handles.get(name)
        if not handle:
            log.warning(f"No handle for teammate '{name}'")
            return False

        # Send shutdown request via mailbox
        self.send_message(
            from_name="lead",
            to_name=name,
            content="Shutdown requested by lead.",
            message_type="shutdown_request",
        )

        # Wait for the handle to stop (with timeout)
        stopped = await handle.wait_for_stop(timeout=30.0)

        if stopped:
            member = self._config.get_member(name)
            if member:
                member.status = TeammateStatus.STOPPED
                member.stopped_at = datetime.now().isoformat()
            self._save_config()
            self._emit_event(TeamEventType.TEAMMATE_STOPPED, {"name": name})

        return stopped

    # ─────────────────────────────────────────────────────────
    # Delegate mode
    # ─────────────────────────────────────────────────────────

    def set_delegate_mode(self, enabled: bool) -> None:
        """Toggle delegate mode for the lead.

        In delegate mode, the lead's toolkit is restricted to:
        - spawn_teammate, shutdown_teammate
        - send_message, broadcast
        - create_task, assign_task, update_task_status
        - get_team_status
        No file/code/search tools are available.
        """
        self._config.delegate_mode = enabled
        self._save_config()
        self._emit_event(TeamEventType.DELEGATE_MODE_CHANGED, {
            "enabled": enabled,
        })
        log.info(f"Delegate mode {'enabled' if enabled else 'disabled'}")

    # ─────────────────────────────────────────────────────────
    # Cleanup
    # ─────────────────────────────────────────────────────────

    async def cleanup(self, force: bool = False) -> None:
        """Clean up team resources.

        1. Verify all teammates are stopped (or force-stop them).
        2. Remove worktrees.
        3. Remove team directory.

        Args:
            force: If True, force-stop active teammates instead of failing.
        """
        active = self._config.get_active_members()
        if active and not force:
            names = [m.name for m in active]
            raise RuntimeError(
                f"Cannot clean up: {len(active)} teammates still active: {names}. "
                "Shut them down first or use force=True."
            )

        # Force-stop any remaining
        if force:
            for member in active:
                handle = self._handles.get(member.name)
                if handle:
                    handle.force_stop()

        # Remove worktrees
        self._cleanup_worktrees()

        # Update config
        self._config.status = TeamStatus.CLEANED_UP
        self._save_config()

        # Shut down executor
        self._executor.shutdown(wait=False)

        self._emit_event(TeamEventType.TEAM_CLEANED_UP, {
            "team_name": self._team_name,
        })

        log.info(f"Cleaned up team '{self._team_name}'")

    def _cleanup_worktrees(self) -> None:
        """Remove all git worktrees for this team."""
        import subprocess

        for member in self._config.members:
            if member.worktree_path:
                try:
                    subprocess.run(
                        ["git", "worktree", "remove", "--force", member.worktree_path],
                        cwd=str(self._repo_root),
                        capture_output=True,
                    )
                except Exception as e:
                    log.warning(f"Failed to remove worktree for '{member.name}': {e}")

    # ─────────────────────────────────────────────────────────
    # Status
    # ─────────────────────────────────────────────────────────

    def get_status(self) -> dict[str, Any]:
        """Get current team status for display."""
        members_status = []
        for member in self._config.members:
            handle = self._handles.get(member.name)
            members_status.append({
                "name": member.name,
                "agent_id": member.agent_id,
                "status": member.status.value,
                "model": member.model or "(default)",
                "labels": member.labels,
                "current_task": handle.current_task if handle else None,
                "iterations": handle.iterations if handle else 0,
            })

        return {
            "team_name": self._team_name,
            "status": self._config.status.value,
            "delegate_mode": self._config.delegate_mode,
            "task_list_id": self._config.task_list_id,
            "lead": self._config.lead.to_dict() if self._config.lead else None,
            "members": members_status,
            "active_count": len(self._config.get_active_members()),
            "total_count": len(self._config.members),
        }

    # ─────────────────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────────────────

    def _emit_event(self, event_type: TeamEventType, data: dict[str, Any]) -> None:
        """Emit a team event through the lead's emitter."""
        if self._emitter:
            from ..events import EventType
            # Use PROGRESS event type as carrier, with team-specific data
            self._emitter.emit(EventType.PROGRESS, {
                "team_event": event_type.value,
                **data,
            })
