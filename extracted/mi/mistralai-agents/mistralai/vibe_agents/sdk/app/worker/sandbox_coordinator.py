"""Coordinate sandbox durability for one Workflow Session."""

from pydantic import JsonValue

from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.hosts.workflows import WorkflowSandboxResource
from mistralai.vibe.harness.runtime.session.commands import (
    ContextMessage,
    SendMessageCommand,
    SessionCommand,
    StartTurnCommand,
    SteerTurnCommand,
)
from mistralai.vibe.harness.runtime.session.conditions import SessionConditionWaiter
from mistralai.vibe.harness.runtime.session.runtime import SessionRuntime
from mistralai.vibe_agents.sdk.app.worker.sandbox_lifecycle import SandboxLifecycle


class WorkflowSandboxCoordinator:
    """Own command invalidation, sandbox replacement, idle checkpoints, and their carried state."""

    def __init__(
        self,
        runtime: SessionRuntime,
        condition_waiter: SessionConditionWaiter,
        lifecycle: SandboxLifecycle | None = None,
        *,
        sandbox: WorkflowSandboxResource | None = None,
    ) -> None:
        self._runtime = runtime
        self._condition_waiter = condition_waiter
        self._lifecycle = lifecycle
        self._sandbox = sandbox
        self._activity_generation = 0

    def command_received(self, *, starts_turn: bool = False) -> None:
        """Invalidate a checkpoint before command preparation or any wait.

        A command that starts a Turn while none runs first replaces an expired sandbox. Commands inside a Turn
        never do: the Turn's work since the last idle checkpoint would be lost.
        """

        if self._lifecycle is None:
            return
        if starts_turn and self._runtime.inspection.active_turn_id is None:
            self._replace_expired_sandbox(self._lifecycle)
        self._activity_generation += 1
        self._lifecycle.activity()
        self._condition_waiter.notify_changed()

    def _replace_expired_sandbox(self, lifecycle: SandboxLifecycle) -> None:
        # Deterministic: Workflow time against carried provider state; the next sandbox operation provisions anew.
        generation = self._sandbox.current_generation if self._sandbox is not None else None
        if self._sandbox is None or generation is None:
            return
        provider_state = self._sandbox.continuation.provider_state
        if provider_state is None or not lifecycle.expired(provider_state):
            return
        self._sandbox.mark_lost(generation)
        # A closed resource, for example during Continue-As-New, keeps its generation: nothing was replaced.
        if self._sandbox.current_generation is None:
            lifecycle.lost()

    def context_messages(self) -> list[ContextMessage]:
        notice = self._lifecycle.notice() if self._lifecycle is not None else None
        if notice is None:
            return []
        return [ContextMessage(content=[core_protocol.TextContentBlock(text=notice)])]

    def context_accepted(self, command: SessionCommand) -> None:
        """Clear the notice once the Runtime accepted a command that carries it."""

        if self._lifecycle is None or not isinstance(command, StartTurnCommand | SteerTurnCommand | SendMessageCommand):
            return
        notice = self._lifecycle.notice()
        if notice is not None and any(
            isinstance(block, core_protocol.TextContentBlock) and block.text == notice
            for message in command.context_messages
            for block in message.content
        ):
            self._lifecycle.notice_delivered(notice)

    async def watch_idle(self) -> None:
        if self._lifecycle is None:
            return
        while True:
            await self._condition_waiter.wait_for_condition(lambda: self._runtime.safely_idle)
            generation = self._activity_generation
            await self._lifecycle.checkpoint(lambda: self._runtime.safely_idle)
            await self._condition_waiter.wait_for_condition(
                lambda: not self._runtime.safely_idle or generation != self._activity_generation
            )

    def durability(self) -> dict[str, JsonValue] | None:
        return self._lifecycle.continuation() if self._lifecycle is not None else None
