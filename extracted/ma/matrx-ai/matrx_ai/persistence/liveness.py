"""Run liveness — "is this run still making progress?", answerable from outside it.

THE PROBLEM (live 2026-10-03, conversation 93ea4aed): during a DB outage a
background turn sat in its final synchronous commit for 7+ minutes. The lease
heartbeat beside it kept renewing — it only knew the PROCESS was alive — so the
conversation stayed locked (``run_in_flight``) until the process restarted. A
lease that renews for a wedged run defeats every lease-expiry rule.

THE PRIMITIVE: a run declares each wait it is willing to block on, with its
bound (``bounded_section(name, budget_seconds)``). Every blocking persistence
point in the Coordinator does this. A section still open past its budget means
the run is NOT making progress — whatever the bound's own mechanism promised.
The lease heartbeat asks :meth:`RunLiveness.overrun` before every renewal and
stops renewing (and fails the run loudly) the moment one is overrun.

Only DECLARED waits are judged: a long tool or a slow model call is legitimate
work and never trips this. A run with no ``RunLiveness`` bound (out-of-request
scripts, tests) pays nothing — ``bounded_section`` is then a no-op.
"""

from __future__ import annotations

import itertools
import time
from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass

# Slack past a section's declared budget before it counts as overrun — the
# bound's own timer and the heartbeat's beat are not synchronised. CAPS.
OVERRUN_GRACE_SECONDS: float = 15.0


@dataclass(frozen=True)
class Overrun:
    """One declared wait that outlived its budget."""

    section: str
    budget_seconds: float
    open_for_seconds: float

    def describe(self) -> str:
        return (
            f"'{self.section}' has been blocked {self.open_for_seconds:.0f}s "
            f"(declared bound {self.budget_seconds:.0f}s)"
        )


class RunLiveness:
    """The set of bounded waits one run is currently blocked in."""

    def __init__(self, label: str = "") -> None:
        self.label = label
        self._ids = itertools.count()
        # id → (section name, budget, monotonic start)
        self._open: dict[int, tuple[str, float, float]] = {}
        #: Set by the lease heartbeat when it gave up on this run — the run's own
        #: unwind reads it to fail the turn honestly instead of "cancelled".
        self.stalled: Overrun | None = None
        self.closed = False

    @contextmanager
    def section(self, name: str, budget_seconds: float) -> Iterator[None]:
        sid = next(self._ids)
        self._open[sid] = (name, float(budget_seconds), time.monotonic())
        try:
            yield
        finally:
            self._open.pop(sid, None)

    def overrun(
        self, *, now: float | None = None, grace_seconds: float = OVERRUN_GRACE_SECONDS
    ) -> Overrun | None:
        """The longest-overdue open section, or None when the run is progressing."""
        t = time.monotonic() if now is None else now
        worst: Overrun | None = None
        for name, budget, started in list(self._open.values()):
            open_for = t - started
            if open_for > budget + grace_seconds and (
                worst is None or open_for - budget > worst.open_for_seconds - worst.budget_seconds
            ):
                worst = Overrun(section=name, budget_seconds=budget, open_for_seconds=open_for)
        return worst

    def close(self) -> None:
        """The run this tracker watched has ended; it is pruned from the stack."""
        self.closed = True

    @property
    def open_sections(self) -> list[str]:
        return [name for name, _, _ in self._open.values()]


class RunStalledError(Exception):
    """A run stopped making progress and was stopped — the turn FAILED.

    Duck-typed ``error_info`` (``error_type`` / ``user_message``) so every stream
    handler surfaces it as a fatal error the person can read."""

    def __init__(self, overrun: Overrun) -> None:
        self.overrun = overrun
        super().__init__(f"run stopped making progress: {overrun.describe()}")
        self.error_info = _RunStalledInfo(overrun)


class _RunStalledInfo:
    error_type = "matrx_run_stalled"
    is_retryable = True
    user_message = (
        "This response failed: saving it stalled while the database was not "
        "answering, so it was stopped. Please send your message again."
    )

    def __init__(self, overrun: Overrun) -> None:
        self.details = {
            "section": overrun.section,
            "budget_seconds": overrun.budget_seconds,
            "open_for_seconds": round(overrun.open_for_seconds, 1),
        }


# The STACK of trackers for runs nested in this task (a conversation that runs a
# utility that runs an agent…). A declared wait registers on every live one, so
# each run's heartbeat judges the waits made on its behalf.
_current_liveness: ContextVar[tuple[RunLiveness, ...]] = ContextVar(
    "matrx_ai_run_liveness", default=()
)


def bind_run_liveness(liveness: RunLiveness) -> Token[tuple[RunLiveness, ...]]:
    """Push ``liveness`` for this context (and tasks spawned with a copied
    context). Closed trackers are pruned on every push so the stack never grows."""
    live = tuple(t for t in _current_liveness.get() if not t.closed)
    return _current_liveness.set((*live, liveness))


def unbind_run_liveness(token: Token[tuple[RunLiveness, ...]]) -> None:
    try:
        _current_liveness.reset(token)
    except ValueError:  # reset from a different context — leave it; it dies with the task
        pass


def new_run_liveness(label: str) -> RunLiveness:
    """Create a tracker for a run starting in this task and push it. The lease
    heartbeat closes it when it stops, which prunes it from the stack."""
    liveness = RunLiveness(label)
    bind_run_liveness(liveness)
    return liveness


def current_run_liveness() -> RunLiveness | None:
    live = [t for t in _current_liveness.get() if not t.closed]
    return live[-1] if live else None


def stalled_run() -> Overrun | None:
    """The overrun a heartbeat gave up on, for any run in this task's stack."""
    for tracker in reversed(_current_liveness.get()):
        if tracker.stalled is not None:
            return tracker.stalled
    return None


@contextmanager
def bounded_section(name: str, budget_seconds: float) -> Iterator[None]:
    """Declare a bounded blocking wait on every live run in this context."""
    live = [t for t in _current_liveness.get() if not t.closed]
    if not live:
        yield
        return
    with ExitStack() as stack:
        for tracker in live:
            stack.enter_context(tracker.section(name, budget_seconds))
        yield


__all__ = [
    "OVERRUN_GRACE_SECONDS",
    "Overrun",
    "RunLiveness",
    "RunStalledError",
    "bind_run_liveness",
    "bounded_section",
    "current_run_liveness",
    "new_run_liveness",
    "stalled_run",
    "unbind_run_liveness",
]
