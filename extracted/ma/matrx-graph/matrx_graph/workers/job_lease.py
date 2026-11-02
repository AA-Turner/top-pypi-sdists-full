"""The job lease a running execution holds, as seen from inside the work (lane K1, 2026-10-21).

Live, 2026-10-21 (run 8749d414, job c1d89868): the database dropped every connection for ten minutes, the reaper
read the expired lease as a dead worker and requeued the job, and the SAME process started the run again while the
first execution was still alive (hung on a store call). The first copy logged "finishing the in-flight run anyway"
and kept its organization import slot, so the second copy waited on itself.

The rule now (Arman, 2026-10-21): **a copy that loses its job lease stops itself.** The runner publishes the lease
of the job it executes on this ContextVar; long, many-item work (an import writes item after item) calls
:func:`check` before each item. Once the lease is gone — the renewal answered "not ours", or the job row says
another claim holds it — ``check`` raises :class:`JobLeaseLost`, the copy stops without writing again, and the
host skips its terminal write (the new copy owns the run). The runner also cancels the lost copy's task, so a copy
parked between items stops too.

``JobLeaseLost`` is a ``CancelledError``: to the engine and the host a lost lease is a cancellation of THIS copy,
never a failure of the run (a failure would be written over the new copy's run).
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import time
from collections.abc import Iterator
from contextvars import ContextVar
from dataclasses import dataclass, field
from uuid import UUID

log = logging.getLogger(__name__)

class JobLeaseLost(asyncio.CancelledError):
    """This copy's job lease was reaped or taken by another claim: stop now, write nothing more."""


@dataclass
class JobLease:
    job_id: str
    run_id: str
    claimed_by: str | None
    #: fewest seconds between two reads of the job row by ``check`` (a many-item run checks before every item); the
    #: runner sets it from its lease (a tenth of the renewal beat), and the renewal's own answer is used in between
    look_every: float = 0.0
    #: the task running this copy of the job: whoever notices the loss first (the renewal, or the work's own
    #: ``check``) cancels it, so the WHOLE copy stops at once (lane K1b, B2: run-ahead swallowed a ``JobLeaseLost``
    #: raised inside one node, and the copy kept checkpointing and routing until the next renewal)
    owner: asyncio.Task | None = field(default=None, repr=False)
    #: the copy finished its work and is settling the job (``complete``): a renewal that lands after the settle
    #: commits answers "not ours", and that is not a loss (K1b, M1)
    settling: bool = False
    #: per-copy fencing token for anything this copy holds (an import slot): a newer copy's is always greater. The
    #: runner sets the job's attempt (bumped by every claim); a lease made by hand defaults to its creation time
    generation: float = field(default_factory=time.time)
    visibility_timeout: int = 600
    lost: bool = False
    why: str = ""
    _looked: float = field(default=0.0, repr=False)

    def mark_lost(self, why: str) -> None:
        if self.settling:
            log.info("job %s: settled while a renewal was in flight; not a lost lease", self.job_id[:8])
            return
        if not self.lost:
            log.error("job %s (run %s) lost its lease (%s): this copy stops and writes nothing more",
                      self.job_id[:8], self.run_id[:8], why)
        self.lost, self.why = True, why
        owner = self.owner
        if owner is not None and not owner.done() and owner is not _running_task():
            owner.cancel(f"job {self.job_id[:8]} lease lost: {why}")

    async def still_held(self) -> bool | None:
        """The job row's answer: True while this claim holds it, False once it does not, None when unreadable."""
        from matrx_graph.db._registry import get_model

        try:
            rows = await get_model("WfJob").filter(id=str(UUID(self.job_id))).all(use_cache=False)
        except Exception:  # noqa: BLE001 — unreadable (an outage): the lease is not judged on a store that is down
            log.warning("could not read job %s to check its lease", self.job_id[:8], exc_info=True)
            return None
        if not rows:
            return False
        row = rows[0]
        get = row.get if isinstance(row, dict) else lambda k: getattr(row, k, None)
        if get("claimed_at") is None:
            return False
        # every claim stamps a token: a token that is not this copy's (or one where this copy had none) is another
        # claim (K1b, M4: a token-less copy used to read every later claim as its own)
        return get("claimed_by") == self.claimed_by

    async def not_ours(self, why: str) -> bool:
        """The queue says this copy no longer holds its job. When the reaper only DEAD-LETTERED it (a false "dead" on
        the last attempt), no other copy can ever own the run: take the job back and keep going, so the run is
        finished and its terminal status written (K1b, B1). Otherwise mark the lease lost (which stops the copy).
        Returns True when the copy keeps the job."""
        from matrx_graph.workers.queue import take_back_false_dead_letter

        if self.settling:
            return True
        try:
            kept = await take_back_false_dead_letter(
                self.job_id, claimed_by=self.claimed_by, visibility_timeout_seconds=self.visibility_timeout)
        except Exception:  # noqa: BLE001 — unknown: the copy stops (the safe side for a run another copy may own)
            log.warning("job %s: could not try to take back a dead-lettered job", self.job_id[:8], exc_info=True)
            kept = False
        if not kept:
            self.mark_lost(why)
        return kept

    async def check(self) -> None:
        """Raise :class:`JobLeaseLost` when this copy no longer holds its job; read the row at most every
        ``look_every`` seconds."""
        if not self.lost and time.monotonic() - self._looked >= self.look_every:
            self._looked = time.monotonic()
            if await self.still_held() is False:
                await self.not_ours("the job row is claimed by another copy or was requeued")
        if self.lost:
            raise JobLeaseLost(f"job {self.job_id[:8]} lease lost: {self.why}")


def _running_task() -> asyncio.Task | None:
    try:
        return asyncio.current_task()
    except RuntimeError:
        return None


_current: ContextVar[JobLease | None] = ContextVar("matrx_graph_job_lease", default=None)


def current() -> JobLease | None:
    """The lease of the job this task executes; None outside a queued job (an inline run has no job lease)."""
    return _current.get()


async def check() -> None:
    """Before each item of many-item work: raises :class:`JobLeaseLost` once this copy's job lease is gone."""
    lease = _current.get()
    if lease is not None:
        await lease.check()


def lost() -> bool:
    lease = _current.get()
    return bool(lease is not None and lease.lost)


@contextlib.contextmanager
def holding(lease: JobLease) -> Iterator[JobLease]:
    token = _current.set(lease)
    try:
        yield lease
    finally:
        _current.reset(token)


__all__ = ["JobLease", "JobLeaseLost", "check", "current", "holding", "lost"]
