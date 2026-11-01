"""what one run shares with the worker (verdicts, rounds, usage) and the capabilities that report into it."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from pydantic_ai.capabilities import AbstractCapability
from probe.daemon.trace import trace as trace_mod
from probe.daemon.agent.guards import LoopDetector, log


@dataclass
class UsageMeter(AbstractCapability[Any]):
    """Hands every model response to `on_round` the moment it arrives (inside the
    model request: a response a later hook rejects is still counted). A failure
    to record is logged, never the run's."""

    on_round: Callable[[Any], None] | None = None

    async def wrap_model_request(self, ctx: Any, *, request_context: Any, handler: Any) -> Any:
        response = await handler(request_context)
        if self.on_round is not None:
            try:
                self.on_round(response)
            except Exception as exc:  # noqa: BLE001
                log.warning("a model round was not recorded: %s: %s", type(exc).__name__, exc)
        return response


@dataclass
class TraceRecorder(trace_mod.Recording, AbstractCapability[Any]):
    """Writes each model call (its delta, the answer, usage, latency) and each
    tool run (duration, outcome, result) to the session's trace file, as they
    happen (`trace.py`). Last in the hook order, so it sees the request as sent,
    after compaction. It observes only: nothing it does changes a request, and
    a failure to write is logged, never the run's."""


@dataclass
class RunState:
    """What one run shares with the worker: the loop detector's verdict, the
    compactions it made, and the worker's hooks (each model round, the state of
    the record)."""

    #: One long conversation per session (T15): no per-bite caps, and compaction
    #: on unless `compacts` is False.
    conversation: bool = False
    #: False: the conversation is never compacted (the reader: its lane starts it
    #: fresh instead, before a turn that would pass the size, rule A).
    compacts: bool = True
    #: The size the conversation compacts at (the reader: starts fresh at).
    context_tokens: int = 0
    #: It compacts this many tokens before that size (the writer's: COMPACT_ROOM_TOKENS).
    compact_room: int = 0
    #: How compaction counts tokens (`server_tokenizer`); None: 4 characters per token.
    tokenizer: Callable[[str], int] | None = None
    on_round: Callable[[Any], None] | None = None
    #: Plain code's state of the record (`session(op=status)`), read on demand.
    status: Callable[[], str] | None = None
    #: Plain code's list of the landed writes (`bite.landed_block`), appended after
    #: each compaction summary so no id or slug in it passes through the model.
    logbook: Callable[[], str] | None = None
    detector: LoopDetector = field(default_factory=LoopDetector)
    compactions: int = 0
    #: The session's trace file for this agent (`trace.py`); None: no trace.
    trace: trace_mod.TraceFile | None = None
    #: What this run's tasks (`probe daemon task`, `run_task`) have spent so far,
    #: counted round by round as they go: dollars (of the rounds a price is known
    #: for), tokens (input and output, priced or not), and how many ran.
    task_usd: float = 0.0
    task_tokens: int = 0
    tasks: int = 0
    #: How many of this run's tasks have started: the next one's number in the trace.
    tasks_started: int = 0
    #: The tasks running now (`TaskState`): each holds back TASK_CAP_USD and
    #: TASK_TOKENS_CUT of the run's budget, less what it has spent, until it ends.
    tasks_running: list = field(default_factory=list)
    _task_slots: Any = None

    def compacted(self) -> None:
        self.compactions += 1

    def task_slots(self) -> Any:
        """At most TASKS_AT_ONCE of this run's tasks run at once: a semaphore of
        their own, never `CallOrder`'s (a task holding a read slot while its own
        reads wait for one would starve them)."""
        import asyncio

        if self._task_slots is None:
            self._task_slots = asyncio.Semaphore(TASKS_AT_ONCE)
        return self._task_slots

    def tasks_spent(self) -> str | None:
        """Why this run's running tasks get no more rounds (its budget is spent), or None."""
        if self.task_usd >= TASK_RUN_USD:
            return f"${self.task_usd:.2f} of ${TASK_RUN_USD:.2f}"
        if self.task_tokens >= TASK_RUN_TOKENS:
            return f"{self.task_tokens:,} of {TASK_RUN_TOKENS:,} tokens"
        return None

    def tasks_full(self, *, running: bool = True) -> str | None:
        """Why this run may start no more tasks, or None: what its tasks spent,
        what each running task still holds back (unless `running` is False: the
        check before a task waits for a slot, when they may end cheaply first),
        and the new task's own hold must fit its budget -- so tasks started
        together cannot overshoot it."""
        running_tasks = self.tasks_running if running else []
        usd = self.task_usd + TASK_CAP_USD + sum(max(0.0, TASK_CAP_USD - t.usd) for t in running_tasks)
        tokens = (self.task_tokens + TASK_TOKENS_CUT
                  + sum(max(0, TASK_TOKENS_CUT - t.tokens) for t in running_tasks))
        if usd > TASK_RUN_USD:
            return f"${usd:.2f} of ${TASK_RUN_USD:.2f}"
        if tokens > TASK_RUN_TOKENS:
            return f"{tokens:,} of {TASK_RUN_TOKENS:,} tokens"
        return None
TASK_TOKENS_CUT = 700_000
#: All the tasks of one run (a writer's bite, a reader's turn, an audit) may
#: spend this much; then `probe daemon task` is refused until the next run.
TASK_RUN_USD = 0.50
#: ...or this many tokens, for a model whose price is unknown.
TASK_RUN_TOKENS = 2_000_000
#: At most this many of one run's tasks run at once (`RunState.task_slots`).
TASKS_AT_ONCE = 2
#: One task's own share of that budget: the most it may spend (priced round by
#: round), and what it holds back of the run's budget until it ends, less what it
#: spent -- a task starts only when its share fits beside the others'
#: (`RunState.tasks_full`). At TASK_CAP_SOFT of it its tool calls tell it to
#: answer; at all of it no further model round is sent (`TaskStopped`). An
#: unpriced model's share is TASK_TOKENS_CUT of TASK_RUN_TOKENS.
TASK_CAP_USD = TASK_RUN_USD / TASKS_AT_ONCE
