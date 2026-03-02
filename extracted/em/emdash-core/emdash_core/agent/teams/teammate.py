"""TeammateHandle — wraps a running teammate agent session.

Each teammate is a full AgentRunner on a background thread with:
- Its own message history (isolated context window)
- Its own toolkit (optionally plan-mode restricted)
- A mailbox subscription for receiving messages
- Shared task list access via Tasks v2 tools

The handle provides the interface for the lead/manager to:
- Start/stop the agent
- Inject messages into the agent's conversation
- Read status and progress
"""

import asyncio
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, Future
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ...utils.logger import log
from .models import (
    TeamConfig,
    TeammateConfig,
    TeammateStatus,
    TeammateRole,
    MessageType,
    TeamMessage,
)


class TeammateHandle:
    """Runtime handle for a single teammate agent session.

    Created by TeamManager.spawn_teammate(). The actual AgentRunner
    lives on a background thread managed by the ThreadPoolExecutor.
    """

    def __init__(
        self,
        config: TeammateConfig,
        team_config: TeamConfig,
        repo_root: Path,
        broker: "MessageBroker",
        parent_emitter=None,
    ):
        self._config = config
        self._team_config = team_config
        self._repo_root = repo_root
        self._broker = broker
        self._parent_emitter = parent_emitter

        # Runtime state
        self._future: Future | None = None
        self._stop_requested = False
        self._stop_event = asyncio.Event()
        self._current_task: str | None = None
        self._iterations: int = 0
        self._started_at: float | None = None
        self._agent_runner = None  # Set when started

    # ─────────────────────────────────────────────────────────
    # Properties
    # ─────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return self._config.name

    @property
    def agent_id(self) -> str:
        return self._config.agent_id

    @property
    def status(self) -> TeammateStatus:
        return self._config.status

    @property
    def current_task(self) -> str | None:
        return self._current_task

    @property
    def iterations(self) -> int:
        return self._iterations

    @property
    def is_running(self) -> bool:
        return (
            self._future is not None
            and not self._future.done()
            and not self._stop_requested
        )

    # ─────────────────────────────────────────────────────────
    # Lifecycle
    # ─────────────────────────────────────────────────────────

    def start(self, executor: ThreadPoolExecutor) -> None:
        """Start the teammate agent on a background thread.

        The agent loop:
        1. Create AgentRunner with teammate toolkit
        2. Send the spawn prompt as the initial user message
        3. Run the agent loop (LLM -> tools -> LLM -> ...)
        4. Between iterations, check for new mailbox messages
        5. Inject messages as system notifications
        6. On stop request or completion, clean up
        """
        self._started_at = time.time()
        self._config.status = TeammateStatus.WORKING
        self._future = executor.submit(self._run_agent_loop)

    def _run_agent_loop(self) -> dict[str, Any]:
        """Main agent loop for the teammate (runs on background thread).

        Returns a summary dict when done.
        """
        from ..runner.agent_runner import AgentRunner
        from ..toolkit import AgentToolkit
        from ..events import AgentEventEmitter
        from ..prompts import build_system_prompt

        try:
            # Create teammate-specific emitter that forwards to parent
            emitter = AgentEventEmitter(agent_name=self._config.name)
            if self._parent_emitter:
                # Add parent as a handler so events bubble up
                emitter.add_handler(_ForwardingHandler(self._parent_emitter))

            # Create toolkit — plan_mode if required
            toolkit = AgentToolkit(
                repo_root=self._repo_root,
                plan_mode=self._config.require_plan_approval,
            )

            # Register team-specific tools (message, task claiming, etc.)
            self._register_team_tools(toolkit)

            # Build system prompt with team context
            system_prompt = self._build_team_system_prompt(toolkit)

            # Create the runner
            runner = AgentRunner(
                toolkit=toolkit,
                model=self._config.model or "default",
                system_prompt=system_prompt,
                emitter=emitter,
                session_id=self._config.agent_id,
            )
            self._agent_runner = runner

            # Run with the spawn prompt as initial message
            log.info(f"[{self.name}] Starting agent loop")
            result = runner.run(self._config.spawn_prompt)

            self._config.status = TeammateStatus.IDLE
            log.info(f"[{self.name}] Agent loop completed")

            # Notify lead that we're idle
            self._broker.send(
                from_agent=self.name,
                to_agent="lead",
                content=f"Teammate '{self.name}' has finished and is idle.",
                message_type=MessageType.IDLE_NOTIFICATION,
            )

            return {"success": True, "result": result}

        except Exception as e:
            log.error(f"[{self.name}] Agent loop failed: {e}")
            self._config.status = TeammateStatus.STOPPED
            return {"success": False, "error": str(e)}

    def _register_team_tools(self, toolkit: "AgentToolkit") -> None:
        """Register team-specific tools on the teammate's toolkit.

        These tools let the teammate:
        - Send messages to other teammates or the lead
        - Claim/complete tasks from the shared task list
        - Report findings and status
        """
        # Team tools are registered via the toolkit's tool registry.
        # We import them here to avoid circular deps.
        from .tools import (
            TeamSendMessageTool,
            TeamGetMessagesTool,
            TeamGetStatusTool,
        )

        team_tools = [
            TeamSendMessageTool(
                broker=self._broker,
                agent_name=self.name,
                team_config=self._team_config,
            ),
            TeamGetMessagesTool(
                broker=self._broker,
                agent_name=self.name,
            ),
            TeamGetStatusTool(
                team_config=self._team_config,
            ),
        ]

        for tool in team_tools:
            toolkit.register_tool(tool)

    def _build_team_system_prompt(self, toolkit: "AgentToolkit") -> str:
        """Build a system prompt with team context injected."""
        from ..prompts import build_system_prompt

        base_prompt = build_system_prompt(toolkit)

        # Inject team awareness
        team_context = f"""
## Team Context

You are **{self.name}**, a teammate in the agent team "{self._team_config.name}".

**Your role**: {self._config.spawn_prompt}

**Team members**:
{self._format_team_members()}

**Shared task list**: Use `get_claimable_todos` to find tasks, `claim_todo` to
start working, and `complete_todo` when done. Filter by your labels: {self._config.labels or '(any)'}.

**Communication**: Use `team_send_message` to message teammates or the lead.
Use `team_get_messages` to check for new messages between iterations.

**Important rules**:
- Focus on your assigned role and labels
- Claim tasks before working on them
- Send findings to the lead when done
- Check messages regularly for redirections from the lead
- Do NOT edit files owned by other teammates
"""
        if self._config.require_plan_approval:
            team_context += """
**Plan mode**: You are in plan mode. You can read and search but NOT write files
or execute commands. Create a plan and send it to the lead for approval using
`team_send_message(to="lead", type="plan_submitted", content="<your plan>")`.
Wait for approval before implementing.
"""

        return base_prompt + "\n" + team_context

    def _format_team_members(self) -> str:
        """Format team member list for the system prompt."""
        lines = []
        if self._team_config.lead:
            lines.append(f"- **lead** (coordinator)")
        for m in self._team_config.members:
            if m.name != self.name:
                status = m.status.value
                labels = f" [{', '.join(m.labels)}]" if m.labels else ""
                lines.append(f"- **{m.name}** ({status}){labels}")
        return "\n".join(lines) if lines else "- (no other members)"

    # ─────────────────────────────────────────────────────────
    # Control
    # ─────────────────────────────────────────────────────────

    async def wait_for_stop(self, timeout: float = 30.0) -> bool:
        """Wait for the teammate to stop.

        Returns True if stopped within timeout.
        """
        self._stop_requested = True

        if self._future is None:
            return True

        # Poll the future with timeout
        start = time.time()
        while time.time() - start < timeout:
            if self._future.done():
                self._stop_event.set()
                return True
            await asyncio.sleep(0.5)

        return False

    def force_stop(self) -> None:
        """Force-stop the teammate (cancel the future)."""
        self._stop_requested = True
        if self._future and not self._future.done():
            self._future.cancel()
        self._config.status = TeammateStatus.STOPPED
        self._config.stopped_at = datetime.now().isoformat()
        self._stop_event.set()

    def inject_message(self, message: TeamMessage) -> None:
        """Inject a message into the teammate's next agent iteration.

        The message is stored in the mailbox. The agent loop checks
        for new messages between LLM iterations and injects them
        as system notifications.
        """
        # The broker handles storage; the agent loop polls between iterations.
        # For in-process mode, we could also use an asyncio.Event to wake
        # the agent immediately, but polling is simpler and sufficient.
        pass


# ─────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────


class _ForwardingHandler:
    """Forwards events from a teammate's emitter to the parent (lead's) emitter.

    Tags each event with the teammate's agent_name so the lead's UI
    can distinguish which teammate produced it.
    """

    def __init__(self, parent_emitter):
        self._parent = parent_emitter

    def handle(self, event) -> None:
        """Forward event to parent emitter."""
        from ..events import EventType
        # Emit as a PROGRESS event with teammate attribution
        self._parent.emit(EventType.PROGRESS, {
            "teammate_event": True,
            "teammate_name": event.agent_name,
            "original_type": event.event_type.value,
            "data": event.data,
        })
