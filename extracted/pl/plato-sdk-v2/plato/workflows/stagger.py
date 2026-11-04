"""Prompt-cache prefix stagger for same-prefix sibling agent calls.

Siblings that share a prompt prefix (same profile, model, effort, workspace)
would otherwise send their first requests together and each pay the uncached
prefix. The first one (the leader) launches at once; siblings reaching the gate
inside its window wait out the rest of it, then read the prefix it cached. The
local Workflow tool does the same (``CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS``).
"""

from __future__ import annotations

import asyncio
import time
from collections import deque
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from enum import StrEnum

#: Matches the local tool's cap. On Chronos a sibling ~2s behind the leader
#: already reads its prefix, so only truly simultaneous launches need holding.
DEFAULT_PREFIX_STAGGER_S = 5.0

#: A released prefix counts as cached for this long (API default TTL is 5 min).
DEFAULT_WARM_TTL_S = 240.0

_MAX_DECISIONS = 1000


class StaggerRole(StrEnum):
    LEADER = "leader"
    FOLLOWER = "follower"
    WARM = "warm"
    DISABLED = "disabled"


@dataclass
class _PrefixGroup:
    leader_call_id: str
    last_launch_at: float
    released: asyncio.Event = field(default_factory=asyncio.Event)
    release_task: asyncio.Task[None] | None = None


@dataclass(frozen=True)
class StaggerDecision:
    """What the gate did for one call."""

    call_id: str
    prefix_key: str
    role: StaggerRole
    leader_call_id: str | None
    held_s: float


class PrefixStagger:
    """Hold same-prefix sibling launches until the leader has warmed the cache."""

    def __init__(
        self,
        window_s: float = DEFAULT_PREFIX_STAGGER_S,
        *,
        warm_ttl_s: float = DEFAULT_WARM_TTL_S,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], Awaitable[object]] = asyncio.sleep,
    ) -> None:
        self._window_s = max(0.0, window_s)
        self._warm_ttl_s = warm_ttl_s
        self._clock = clock
        self._sleep = sleep
        self._groups: dict[str, _PrefixGroup] = {}
        self.decisions: deque[StaggerDecision] = deque(maxlen=_MAX_DECISIONS)

    @property
    def enabled(self) -> bool:
        return self._window_s > 0

    async def gate(self, prefix_key: str, call_id: str) -> StaggerDecision:
        """Wait (if needed) before ``call_id`` launches; returns the decision."""
        if not self.enabled:
            return self._record(StaggerDecision(call_id, prefix_key, StaggerRole.DISABLED, None, 0.0))

        arrived = self._clock()
        group = self._groups.get(prefix_key)
        if group is not None and not group.released.is_set():
            await group.released.wait()
            group.last_launch_at = self._clock()
            held = group.last_launch_at - arrived
            return self._record(StaggerDecision(call_id, prefix_key, StaggerRole.FOLLOWER, group.leader_call_id, held))
        if group is not None and arrived - group.last_launch_at < self._warm_ttl_s:
            group.last_launch_at = arrived
            return self._record(StaggerDecision(call_id, prefix_key, StaggerRole.WARM, group.leader_call_id, 0.0))

        self._drop_cold_groups(arrived)
        group = _PrefixGroup(leader_call_id=call_id, last_launch_at=arrived)
        group.release_task = asyncio.create_task(self._release_after_window(group))
        self._groups[prefix_key] = group
        return self._record(StaggerDecision(call_id, prefix_key, StaggerRole.LEADER, call_id, 0.0))

    async def _release_after_window(self, group: _PrefixGroup) -> None:
        try:
            await self._sleep(self._window_s)
        finally:
            # Also on cancellation: a held follower must never outlive its leader's window.
            group.released.set()

    def _drop_cold_groups(self, now: float) -> None:
        cold = [
            key
            for key, group in self._groups.items()
            if group.released.is_set() and now - group.last_launch_at >= self._warm_ttl_s
        ]
        for key in cold:
            del self._groups[key]

    def _record(self, decision: StaggerDecision) -> StaggerDecision:
        self.decisions.append(decision)
        return decision
