"""Episodes run in sandboxes, as many at once as asked, each task once."""

import asyncio
import contextlib
import math
import uuid
from collections.abc import Awaitable, Callable, Iterator, Mapping
from time import monotonic
from typing import ClassVar, TypeVar

from labqoat.json_document import JsonValue
from labqoat.rl.episode_ledger import EpisodeLedger
from labqoat.rl.episode_record import EpisodeRecord
from labqoat.rl.rollout_report import RolloutReport
from labqoat.rl.sandbox_template import SandboxTemplate
from labqoat.sandbox.sandbox import Sandbox
from labqoat.sandbox.sandbox_client import SandboxClient
from labqoat.sandbox.sandbox_error import SandboxError
from labqoat.sandbox.sandbox_file_not_found_error import SandboxFileNotFoundError
from labqoat.sandbox.sandbox_not_found_error import SandboxNotFoundError
from labqoat.sandbox.sandbox_platform import SandboxPlatform
from labqoat.sandbox.sandbox_reach import SandboxReach
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError

TaskT = TypeVar("TaskT")
Outcome = float | tuple[float, JsonValue]
Episode = Callable[[Sandbox, TaskT], Awaitable[Outcome]]


class Rollouts:
    """Run one episode per task, each in a fresh sandbox that is terminated whatever happens.

    Sandboxes start on the function's own host when it declares one, and otherwise wherever the platform places
    them, from a laptop as from any run; ``client`` chooses explicitly. An episode is an awaitable function of a
    sandbox and a task. It returns the reward, or the reward and JSON
    to keep with it. At most ``concurrency`` episodes run at once and each waits up to ``capacity_wait``
    seconds for room on the host. What an episode comes to decides what happens next:

    - A reward is recorded, durably when there is a ledger, and a later rollout over that ledger skips the task.
    - A lost host or sandbox starts the episode again in a new sandbox, ``attempts`` times at most.
    - Any other sandbox failure, or more than ``episode_timeout`` seconds, leaves a record without a reward.
      A command that exits non-zero is a result, not a failure.
    - A template the host refuses, or any other exception, stops the rollout with that error.
    """

    LIFETIME_MARGIN_SECONDS: ClassVar[float] = 60.0
    LONGEST_LIFETIME_SECONDS: ClassVar[float] = 86_400.0

    def __init__(
        self,
        client: SandboxClient | SandboxPlatform | None = None,
        template: SandboxTemplate | None = None,
        *,
        concurrency: int = 16,
        attempts: int = 2,
        episode_timeout: float = 1800.0,
        capacity_wait: float = 3600.0,
        ledger: EpisodeLedger | None = None,
    ) -> None:
        """Bind where sandboxes start, the rollout's limits, and a template when the default is not what is needed."""
        if concurrency < 1 or attempts < 1:
            raise ValueError("concurrency and attempts must be at least 1")
        self._client = client or SandboxReach.nearest()
        self._template = template or SandboxTemplate()
        self._concurrency = concurrency
        self._attempts = attempts
        self._episode_timeout = episode_timeout
        self._capacity_wait = capacity_wait
        self._ledger = ledger

    async def run(self, tasks: Mapping[str, TaskT], episode: Episode[TaskT]) -> RolloutReport:
        """Run an episode for every task that has no reward yet and report on all of them, in the order given."""
        records = {} if self._ledger is None else await asyncio.to_thread(self._ledger.completed)
        waiting = [(key, task) for key, task in tasks.items() if key not in records]
        pending = iter(waiting)
        try:
            async with asyncio.TaskGroup() as group:
                for _ in range(min(self._concurrency, len(waiting))):
                    group.create_task(self._worker(pending, episode, records))
        except ExceptionGroup as failures:
            raise failures.exceptions[0] from None
        return RolloutReport(tuple(records[key] for key in tasks))

    async def _worker(
        self, pending: Iterator[tuple[str, TaskT]], episode: Episode[TaskT], records: dict[str, EpisodeRecord]
    ) -> None:
        """Take one task after another until none is left, keeping each record as soon as it exists."""
        for key, task in pending:
            record = await self._attempted(key, task, episode)
            if self._ledger is not None:
                await asyncio.to_thread(self._ledger.append, record)
            records[key] = record

    async def _attempted(self, key: str, task: TaskT, episode: Episode[TaskT]) -> EpisodeRecord:
        """Start the episode again only while its host or sandbox was lost; anything else is its outcome."""
        started = monotonic()
        failure = ""
        for attempt in range(1, self._attempts + 1):
            try:
                reward, detail = await self._episode(task, episode)
            except (SandboxError, TimeoutError) as error:
                failure = self._reason(error)
                if not self._lost(error):
                    return EpisodeRecord(key, None, attempt, monotonic() - started, failure)
            else:
                return EpisodeRecord(key, reward, attempt, monotonic() - started, detail=detail)
        return EpisodeRecord(key, None, self._attempts, monotonic() - started, failure)

    async def _episode(self, task: TaskT, episode: Episode[TaskT]) -> tuple[float, JsonValue]:
        """Run one episode in a sandbox of its own, which is terminated even if starting it was interrupted.

        The host also ends the sandbox shortly after the episode's time is up, should this process be gone.
        """
        sandbox = self._client.from_id(f"episode-{uuid.uuid4().hex}")
        lifetime = min(self._episode_timeout + self.LIFETIME_MARGIN_SECONDS, self.LONGEST_LIFETIME_SECONDS)
        try:
            await self._template.start(self._client, sandbox.id, self._capacity_wait, lifetime)
            return self._scored(await asyncio.wait_for(episode(sandbox, task), self._episode_timeout))
        finally:
            with contextlib.suppress(SandboxError):
                await sandbox.terminate_async()

    @staticmethod
    def _scored(outcome: Outcome) -> tuple[float, JsonValue]:
        """Split an outcome into reward and detail; a reward that is not a finite number is the episode's mistake."""
        reward, detail = outcome if isinstance(outcome, tuple) else (outcome, None)
        if not math.isfinite(reward):
            raise ValueError(f"an episode returned {reward!r} as its reward, which is not a finite number")
        return float(reward), detail

    @staticmethod
    def _lost(error: Exception) -> bool:
        """Tell a host or sandbox that went away from a failure a new sandbox would only repeat."""
        gone = isinstance(error, SandboxNotFoundError) and not isinstance(error, SandboxFileNotFoundError)
        return gone or isinstance(error, SandboxUnavailableError)

    def _reason(self, error: Exception) -> str:
        """Name a failure; a timeout with no words of its own is the episode running past its limit."""
        words = str(error) or f"the episode ran past {self._episode_timeout:g} s"
        return f"{type(error).__name__}: {words}"
