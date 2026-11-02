"""Session lifetime and idle limits, enforced by the Session Workflow itself.

Temporal's execution timeout only backs these limits up: a Session must end through its own
terminal path, which publishes its state, settles open callbacks, and tells its parent.
"""

from collections.abc import Callable
from dataclasses import dataclass

from mistralai.vibe.harness.runtime.session.conditions import SessionConditionWaiter
from mistralai.vibe.harness.runtime.session.runtime import SessionRuntime
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.app.worker import callbacks as worker_callbacks


@dataclass(frozen=True)
class SessionLimits:
    """The limits one Session run enforces, as Workflow clock times in Unix milliseconds."""

    # When the Session reaches its maximum lifetime; fixed at its first run.
    lifetime_deadline_unix_ms: int
    idle_limit_ms: int
    grace_seconds: float


def session_is_idle(runtime: SessionRuntime, callbacks: worker_callbacks.WorkflowCallbackStore) -> bool:
    """Whether the Session waits only on others.

    A Session is idle when no Turn runs or waits to run, or when every unfinished Action of the
    running Turn waits for the user or the app to answer its callback. One Action still running,
    such as a model call or a tool, keeps the Session busy. It is never idle while one of its
    direct children is starting or running a Turn, because the parent waits for that work.
    """

    if runtime.children_working:
        return False
    if not runtime.turn_in_progress:
        return True
    unfinished = runtime.unfinished_action_ids
    return bool(unfinished) and unfinished <= callbacks.waiting_action_ids


class SessionLimitClock:
    """Track when the Session became idle and report the first limit it reaches."""

    def __init__(
        self,
        limits: SessionLimits,
        *,
        is_idle: Callable[[], bool],
        now_unix_ms: Callable[[], int],
        condition_waiter: SessionConditionWaiter,
        idle_since_unix_ms: int | None = None,
        stopped_by: Callable[[], wire.SessionLimitCause | None] = lambda: None,
    ) -> None:
        self._limits = limits
        self._is_idle = is_idle
        # A limit stop that arrived from outside, such as from a parent that ended at its limit.
        self._stopped_by = stopped_by
        self._now_unix_ms = now_unix_ms
        self._condition_waiter = condition_waiter
        # Carried across Continue-As-New, so a new run does not restart an idle Session's clock.
        self.idle_since_unix_ms = idle_since_unix_ms

    async def wait_for_limit(self) -> wire.SessionLimitCause:
        """Return the first limit the Session reaches; the caller cancels this when it ends first."""

        while True:
            stopped_by = self._stopped_by()
            if stopped_by is not None:
                return stopped_by
            now = self._now_unix_ms()
            idle = self._is_idle()
            if not idle:
                self.idle_since_unix_ms = None
            elif self.idle_since_unix_ms is None:
                self.idle_since_unix_ms = now
            if now >= self._limits.lifetime_deadline_unix_ms:
                return wire.SessionLimitCause.LIFETIME_LIMIT
            deadline = self._limits.lifetime_deadline_unix_ms
            if self.idle_since_unix_ms is not None:
                idle_deadline = self.idle_since_unix_ms + self._limits.idle_limit_ms
                if now >= idle_deadline:
                    return wire.SessionLimitCause.IDLE_LIMIT
                deadline = min(deadline, idle_deadline)
            # Wakes when the Session starts or stops being idle, or at the next deadline.
            await self._condition_waiter.wait_for_condition(
                lambda: self._is_idle() != idle or self._stopped_by() is not None,
                timeout_seconds=max(deadline - now, 0) / 1000,
            )


__all__ = [
    "SessionLimitClock",
    "SessionLimits",
    "session_is_idle",
]
