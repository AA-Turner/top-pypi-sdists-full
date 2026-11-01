"""capabilities that gate tool calls: the lease gate, read/write call ordering, loop detection, spent retries."""

from __future__ import annotations
import json
import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from probe.foundation.compat.compat import StrEnum
from typing import Any
from pydantic_ai import RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.exceptions import SkipToolExecution, UnexpectedModelBehavior
from probe.daemon.agent import tools

log = logging.getLogger("probe.daemon")
#: The loop detector: the same refusal or failure in this many model rounds of
#: one run...
LOOP_FAILURES = 3
#: ...or the same successful call (tool and arguments) this many times.
LOOP_REPEATS = 5


@dataclass
class LeaseGate(AbstractCapability[tools.Deps]):
    """Before ANY tool runs -- the daemon's own, the Probe MCP's --
    `tools.write_refusal`: once the switch moved or the lease is gone, the call
    is skipped and answers the stop message (and `Deps.stopped` is set, so the
    worker ends the bite without covering it). The model's final answer is an
    output tool, which no tool hook sees: it can always end the bite."""

    async def before_tool_execute(self, ctx: RunContext[tools.Deps], *, call: Any, tool_def: Any, args: Any) -> Any:
        stop = tools.write_refusal(ctx.deps)
        if stop is not None:
            raise SkipToolExecution(stop)
        return args


#: The `bash` calls of one model response that only read run together, at most
#: this many at once (`CallOrder`).
PARALLEL_READS = 4
#: A call still waiting this long for an earlier call of its response to reach
#: the gate is logged -- and goes on waiting: no call ever runs ahead of an
#: earlier one the order puts first. Every call reaches the gate at once (Pydantic
#: AI starts a response's calls as tasks together, and the gate is the first hook);
#: one whose arguments fail validation never does, and is known from the start
#: (`_bash_command`), so nobody waits for it.
ARRIVAL_S = 5.0
#: ...and once it has waited this long for one that never started, it does not
#: run at all: it answers EARLIER_NEVER_STARTED (NEW wording,
#: fixtures/daemon_prompts/tools/parallel-replies.NEW.md).
NEVER_STARTED_S = 120.0
EARLIER_NEVER_STARTED = "not run: an earlier call never started; send this one again."


@dataclass
class _Slot:
    """One `bash` call of a response, as `CallOrder` orders it."""

    index: int
    writes: bool
    #: Its arguments: an identical call later in the response waits for this one.
    key: str
    arrived: Any = None
    done: Any = None
    #: It holds one of the PARALLEL_READS slots while it runs.
    holds: bool = False
    #: Past the gate, not over yet.
    running: bool = False
    #: Its arguments fail validation, so it was taken for one that never comes.
    dropped: bool = False


@dataclass
class CallOrder(AbstractCapability[tools.Deps]):
    """The `bash` calls of one model response run together when they only read,
    and one at a time, in the model's order, when they write (`toolset.parallel`).

    Each call is classified from the response itself, before any runs: a write
    is any call `tools.reads_only` cannot prove reads (a probe write, a note
    write, anything off the safe list: it may be asked, held or run in bypass).
    Then, at the FIRST tool hook of each call:

        a write   waits for every earlier call of the response to finish, and
                  every later call waits for it: it runs alone, in order
        a read    waits only for the earlier writes (and an earlier identical
                  call: the loop detector then sees each repeat's answer before
                  the next runs), then takes one of PARALLEL_READS slots

    That is Pydantic AI's own barrier (`sequential=True`) for writes, kept inside
    the one tool, and parallel reads beside it. Because the waiting is the first
    hook, every later hook -- the lease gate, the loop detector, the limits, the
    audit's evidence gate -- sees a write only once the calls before it are over,
    as it did when the whole tool was sequential. A call is over when its task
    ends (each call of a response runs as its own task), whatever ended it: a
    later hook's skip, an error, a cancel; a refusal or failure in one call is its
    own answer and cancels nothing. `ran`, `together` and `peak` count, over the
    run, the calls gated, the ones that started while another of their response
    ran, and the most at once."""

    tool: str = "bash"
    limit: int = PARALLEL_READS
    ran: int = 0
    together: int = 0
    peak: int = 0
    _response: Any = None
    _slots: dict = field(default_factory=dict)
    _by_task: dict = field(default_factory=dict)
    _sem: Any = None
    _running: int = 0

    async def before_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any) -> Any:
        import asyncio

        if call.tool_name != self.tool:
            return args
        slot = self._slot(ctx, call)
        task = asyncio.current_task()
        if slot is None or task is None:
            return args
        if slot.dropped:
            # Taken for one that never comes, it came after all (its arguments
            # repaired): it is ordered as a write from here.
            slot.dropped, slot.done = False, asyncio.Event()
        slot.arrived.set()
        earlier = self._by_task.get(task)
        if earlier is not None:
            # The same task runs its calls one after another: that one is over.
            self._release(earlier)
        self._by_task[task] = slot
        try:
            for other in sorted(self._slots.values(), key=lambda s: s.index):
                if other.index >= slot.index:
                    break
                if slot.writes or other.writes or other.key == slot.key:
                    await self._finished(other)
            if not slot.writes:
                await self._sem.acquire()
                slot.holds = True
        except BaseException:
            self._release(slot)
            raise
        self.ran += 1
        self.together += self._running > 0
        self._running += 1
        slot.running = True
        self.peak = max(self.peak, self._running)
        task.add_done_callback(lambda _t, s=slot: self._release(s))
        return args

    def _slot(self, ctx: Any, call: Any) -> _Slot | None:
        """This call's slot; the response's slots are made when its first call
        arrives. None: no response to order by (the call runs as it comes)."""
        import asyncio

        from pydantic_ai.messages import ModelResponse, ToolCallPart

        messages = getattr(ctx, "messages", None) or []
        response = messages[-1] if messages else None
        if not isinstance(response, ModelResponse):
            return None
        if response is not self._response:
            if self._sem is None:
                self._sem = asyncio.Semaphore(max(1, self.limit))
            self._response, self._slots, self._by_task = response, {}, {}
            parts = [p for p in response.parts if isinstance(p, ToolCallPart) and p.tool_name == self.tool]
            for i, part in enumerate(parts):
                command = _bash_command(part)
                slot = _Slot(i, writes=command is None or _writes(getattr(ctx, "deps", None), command),
                             key=command if command is not None else part.tool_call_id,
                             arrived=asyncio.Event(), done=asyncio.Event())
                if command is None:  # it fails validation: it never reaches the hooks
                    slot.dropped = True
                    slot.arrived.set()
                    slot.done.set()
                self._slots[part.tool_call_id] = slot
        return self._slots.get(call.tool_call_id)

    async def _finished(self, other: _Slot) -> None:
        import asyncio

        if not other.arrived.is_set():
            try:
                await asyncio.wait_for(other.arrived.wait(), ARRIVAL_S)
            except asyncio.TimeoutError:
                log.warning("bash call %s of the response has not reached the gate after %.0f s; the calls after "
                            "it wait for it", other.index, ARRIVAL_S)
                try:
                    await asyncio.wait_for(other.arrived.wait(), max(0.0, NEVER_STARTED_S - ARRIVAL_S))
                except asyncio.TimeoutError:
                    log.warning("bash call %s of the response never started: the calls after it are not run",
                                other.index)
                    raise SkipToolExecution(EARLIER_NEVER_STARTED) from None
        await other.done.wait()

    def _release(self, slot: _Slot) -> None:
        if slot.done.is_set():
            return
        if slot.holds:
            slot.holds = False
            self._sem.release()
        if slot.running:
            slot.running = False
            self._running -= 1
        slot.done.set()


def _bash_command(part: Any) -> str | None:
    """A `bash` call's command, or None when its arguments would fail validation
    (not a JSON object, no string `command`, a `why` that is not a string, any
    other argument: the tool forbids extra ones)."""
    try:
        args = part.args_as_dict()
    except Exception:  # noqa: BLE001 -- malformed: Pydantic AI answers it a retry
        return None
    command, why = args.get("command"), args.get("why", "")
    valid = isinstance(command, str) and isinstance(why, str) and set(args) <= {"command", "why"}
    return command if valid else None


def _writes(deps: Any, command: str) -> bool:
    """Whether a `bash` call counts as a write for `CallOrder`. The reader's and a
    task's never do: each runs only reads (`tools._checked_shell_command`,
    `build_task_agent`), anything else is refused at once."""
    if deps is None:
        return True
    if deps.reader or deps.task:
        return False
    try:
        return tools.reads_only(deps, command) is not None
    except Exception as exc:  # noqa: BLE001 -- what it cannot read is a write
        log.warning("bash call not classified (%s: %s): it runs alone", type(exc).__name__, exc)
        return True


_FIRST_BRACKET = re.compile(r"^\[([^\]\n]*)\]")
_NONZERO_EXIT = re.compile(r"\bexit (?!0\b)\S+")
_IDS = re.compile(r"\b[0-9a-f]{6,}\b|\d+")


class Verdict(StrEnum):
    """How a tool call went, as the loop detector counts it (`outcome`)."""

    OK = "ok"
    REFUSED = "refused"
    FAILED = "failed"


def outcome(result: Any) -> Verdict:
    """REFUSED, FAILED or OK, from how the daemon's tools word a result:
    `not run...` / `not read...` / `tool error (...)` refuse; `[exit N]` with
    N != 0, a timeout or a stop fail. Anything else (the MCP's) is ok."""
    if not isinstance(result, str):
        return Verdict.OK
    first = result.lstrip().split("\n", 1)[0]
    if first.startswith(("not run", "not read", "tool error")):
        return Verdict.REFUSED
    m = _FIRST_BRACKET.match(first)
    if m and (_NONZERO_EXIT.search(m.group(1)) or "timed out" in m.group(1) or m.group(1).startswith("stopped")):
        return Verdict.FAILED
    return Verdict.OK


@dataclass
class LoopDetector(AbstractCapability[Any]):
    """Stops a run going round in circles (A1): the same refusal or failure in
    LOOP_FAILURES model rounds (the same call, or the same refusal whatever the
    call), or the same successful call -- tool and arguments -- LOOP_REPEATS
    times. Tripped, every later tool call of the run is skipped with a stop
    message and `tripped` says why; the worker ends the run at the next model
    round.

    A refusal that reads alike whatever the call counts once per round: calls the
    model made together had not seen each other's answer, so three different
    reads refused alike in one round are one attempt, not a loop. (The reader
    asked for three run folders' files at once, all outside its folders; with
    ids masked the three refusals read alike and stopped its turn, strand-ai
    2026-10-11.) The same call -- tool and arguments -- counts every time, in a
    round or not: a failing command the model repeats in one response still
    stops the run before it runs a fourth time."""

    failures_to_trip: int = LOOP_FAILURES
    repeats_to_trip: int = LOOP_REPEATS
    tripped: str | None = None
    _failures: Counter = field(default_factory=Counter)
    _calls: Counter = field(default_factory=Counter)
    #: The round each alike-refusal key last counted in.
    _counted_in: dict = field(default_factory=dict)

    async def before_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any) -> Any:
        if self.tripped is not None:
            raise SkipToolExecution(f"not run: the daemon stopped this run - {self.tripped}.")
        return args

    async def after_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any, result: Any) -> Any:
        if self.tripped is not None:
            return result
        try:
            key = (call.tool_name, json.dumps(args, sort_keys=True, default=str))
        except (TypeError, ValueError):
            key = (call.tool_name, repr(args))
        verdict = outcome(result)
        first = str(result).lstrip().split("\n", 1)[0][:160] if isinstance(result, str) else ""
        if verdict == Verdict.OK:
            self._calls[key] += 1
            if self._calls[key] >= self.repeats_to_trip:
                self.tripped = f"the same `{call.tool_name}` call ran {self._calls[key]} times in one run"
            return result
        keys = [("call", *key)]
        if verdict == Verdict.REFUSED:
            keys.append(("said", call.tool_name, _IDS.sub("#", first)))
        # No round known (no run context): every call is its own round.
        round_ = getattr(ctx, "run_step", None)
        for k in keys:
            if k[0] == "said" and round_ is not None:
                if self._counted_in.get(k) == round_:
                    continue
                self._counted_in[k] = round_
            self._failures[k] += 1
            if self._failures[k] >= self.failures_to_trip:
                self.tripped = (f"the same {'refusal' if verdict == Verdict.REFUSED else 'failure'} "
                                f"{self._failures[k]} times in one run: {first}")
                break
        return result


#: What a tool call answers once its tool has used up its retries in the run.
#: Its first line is the same whatever the error, so the loop detector counts
#: a tool that keeps failing in different words as one refusal.
RETRIES_SPENT = "tool error ({tool}): failed {n} times in a row; not retried.\n{error}"
#: Model rounds with a spent retry (any tool) in one run: the last fails the run.
SPENT_RETRIES_TO_FAIL = 2


@dataclass
class RetriesSpentAreRefusals(AbstractCapability[Any]):
    """A tool call that asks for one retry more than its tool's budget answers
    the model with that error instead of failing the run -- once. pydantic-ai
    fails the WHOLE run ("Tool 'entity' exceeded max retries count of 2") on
    the third retry; the retries come from the Probe MCP, whose errors reach the
    model as `ModelRetry` (strand-ai 2026-10-17: the writer mis-copied an
    `entity` cursor three times and the bite was lost). The run's
    SPENT_RETRIES_TO_FAIL-th model round with a spent retry fails the run as
    before: its events stay queued and the next try backs off, which an MCP
    that keeps failing (overloaded, over a quota) needs. Never through the loop
    detector: a loop stop skips its range after two tries, and an answered call
    refills the tool's retries, so counting answers would not bound a run.
    Counted per round: calls the model made together had not seen each other's
    answer."""

    spent_in: set = field(default_factory=set)

    async def wrap_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any, handler: Any) -> Any:
        from pydantic_ai import ModelRetry

        try:
            return await handler(args)
        except UnexpectedModelBehavior as exc:
            # The library checks the budget inside the call: out of retries, the
            # tool's `ModelRetry` comes back as this, caused by it.
            if not isinstance(exc.__cause__, ModelRetry):
                raise
            step = getattr(ctx, "run_step", None)
            self.spent_in.add(step if step is not None else object())
            # Even beside `final_result`: pydantic-ai drops a final result when
            # another call in its response asks for a retry, so the run may go on
            # and the model would read this answer (Codex, review 2026-10-17).
            if len(self.spent_in) >= SPENT_RETRIES_TO_FAIL:
                raise
            log.warning("tool %s ran out of retries; answered: %s", call.tool_name, exc.__cause__.message)
            return RETRIES_SPENT.format(tool=call.tool_name, error=exc.__cause__.message,
                                        n=int(getattr(ctx, "retry", 0) or 0) + 1)
