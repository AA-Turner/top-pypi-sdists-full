"""The daemon's Pydantic AI agent: its instructions, tools and capabilities (D13).

Imported only by the AI process (the `daemon` extra). The daemon's own tools
are three -- `shell`, `read` and `session` (`tools.py`) -- plus the output tool
that ends a run, and the Probe MCP toolset from the start, only where it is the
same deployment as the API the daemon's key belongs to. The daemon keeps no
memory of its own. Each tool caps its own output. Tool calls run in parallel,
as Pydantic AI runs them, except the tools that WRITE (`tools.WRITE_TOOLS`):
each of those is a barrier that runs alone, in the order the model called it
(A5).

Every tool call, whichever toolset it comes from (the MCP's reads included),
first passes `LeaseGate`: once this process may no longer act for the session
(`tools.write_refusal`), the call does not run and the model is told to stop.

The pydantic-ai-harness capabilities it runs with (T3):

    compaction          conversation mode only: near CONTEXT_TOKENS, old tool
                        results cleared first, then older turns summarized
    warn_on_cache_busts a collapsed prompt cache is logged
    repair_tool_arguments  malformed JSON arguments repaired before validation

and three of its own: `LoopDetector` (the same refusal or failure 3 times, or the
same successful call 5 times, in one run: the run stops), `UsageMeter` (every
model response recorded as it arrives, T10) and `TraceRecorder` (the session's
trace file, `trace.py`).
"""

from __future__ import annotations

from contextlib import asynccontextmanager

import json
import logging
import os
import re
from collections import Counter
from dataclasses import dataclass, field
from probe._compat import StrEnum
from typing import Any, Callable
from urllib.parse import urlparse

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.exceptions import SkipToolExecution

from probe.daemon import lease, tools
from probe.daemon import trace as trace_mod

log = logging.getLogger("probe.daemon")
STOCK_MCP_URL = "https://mcp.research.prbe.ai/mcp"
#: Conversation mode compacts once the context passes this many tokens (estimated).
#: The writer: near its 1M window, leaving room for the 16K output and the tool
#: schemas (Richard, 2026-09-28: "1m"). The reader: only the immediate reading
#: matters (Richard, 2026-09-28: "compact to 120k").
CONTEXT_TOKENS = int(os.environ.get("PROBE_DAEMON_CONTEXT_TOKENS") or 950_000)
READ_CONTEXT_TOKENS = int(os.environ.get("PROBE_READER_CONTEXT_TOKENS") or 120_000)
#: While a model call runs, the writer's lease is renewed this often (a call may
#: take 30 minutes; the lease lives 240 s).
LEASE_RENEW_IN_CALL_S = 60.0
#: Compaction's first tier keeps this many recent tool call / result pairs whole...
KEEP_TOOL_PAIRS = 6
#: ...and clears nothing unless that reclaims at least this many tokens (a clear
#: rewrites history, so the provider re-caches from there: not for a few tokens).
MIN_CLEAR_TOKENS = 20_000
#: The summarizing tier keeps this many recent messages as they are.
KEEP_MESSAGES = 20
#: The user turn put between the summary and a kept tail that opens with the
#: model's own message (`user_turn_first`).
EARLIER_TURNS = "[earlier turns are summarized above]"
#: The loop detector: the same refusal or failure this many times in one run...
LOOP_FAILURES = 3
#: ...or the same successful call (tool and arguments) this many times.
LOOP_REPEATS = 5

#: The `shell` tool's description, as the researcher wrote it.
SHELL_DESCRIPTION = (
    "Run a generic bash command in the session's working folders. \n"
    "\n"
    " - Commands are checked against a safe list: a safe command runs at once, anything else waits for the "
    "researcher's yes (in bypass mode, it runs)\n"
    " - Commands are chainable (`cd x && probe ...`, `probe ... | jq ...`)\n"
    " - `why`: one line on why you run it."
)

SUMMARY_PROMPT = """\
Summarize this conversation of the Probe daemon - your summary REPLACES it, so it must let the daemon carry \
on without redoing work. Use these headings, and skip one only if it is empty:

## What the session is about
## What was recorded
Every Probe write that landed, with exact ids and slugs.
## What failed or waits for the researcher
Failed or refused writes, and questions waiting (with request ids).
## Where it left off
The last turn and event ids covered, and what was in progress.

Quote ids, numbers, metric names and paths VERBATIM. Reply with the summary only.

<messages>
{messages}
</messages>\
"""

#: The `read` tool's description.
READ_DESCRIPTION = (
    "Read a file - nothing runs. Any file in the session's working folders or the skills folder (e.g. "
    "`track-work/reference.md`).\n"
    "\n"
    "`offset` / `limit`: a range of lines (at most 2000). Neither: a preview of a CSV/TSV, JSON, Parquet or "
    "NumPy file. Never a pickle or an image."
)

#: The `session` tool's description.
SESSION_DESCRIPTION = (
    "Look at the session, or your own record of it. `op` picks what:\n"
    "\n"
    "- `open` - one event in full (`event_id`), or a whole turn (`turn`); long text comes in pages (`page`).\n"
    "- `outline` - one line per turn (`page`).\n"
    "- `search` - words across the WHOLE session (`query`; narrow with `kind`, `turn_from`, `turn_to`).\n"
    "- `logbook` - words across your own past writes and lookups (`query`).\n"
    "- `status` - what is recorded, what failed or waits for the researcher, and how much of the session you "
    "have not been shown.\n"
    "\n"
    "Each `op` takes only its own options."
)


class BiteResult(BaseModel):
    """Ends the bite."""

    summary: str = Field(description='ONE line - what you recorded, or "nothing new".')


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
    """Stops a run going round in circles (A1): the same refusal or failure
    LOOP_FAILURES times (the same call, or the same refusal whatever the call),
    or the same successful call -- tool and arguments -- LOOP_REPEATS times.
    Tripped, every later tool call of the run is skipped with a stop message and
    `tripped` says why; the worker ends the run at the next model round."""

    failures_to_trip: int = LOOP_FAILURES
    repeats_to_trip: int = LOOP_REPEATS
    tripped: str | None = None
    _failures: Counter = field(default_factory=Counter)
    _calls: Counter = field(default_factory=Counter)

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
        for k in keys:
            self._failures[k] += 1
            if self._failures[k] >= self.failures_to_trip:
                self.tripped = (f"the same {'refusal' if verdict == Verdict.REFUSED else 'failure'} "
                                f"{self._failures[k]} times in one run: {first}")
                break
        return result


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

    #: One long conversation per session (T15): compaction on, no per-bite caps.
    conversation: bool = False
    #: The compaction prompt and the size it compacts at (the reader has its own).
    summary_prompt: str = ""
    context_tokens: int = 0
    on_round: Callable[[Any], None] | None = None
    #: Plain code's state of the record (`session(op=status)`), read on demand.
    status: Callable[[], str] | None = None
    detector: LoopDetector = field(default_factory=LoopDetector)
    compactions: int = 0
    #: The session's trace file for this agent (`trace.py`); None: no trace.
    trace: trace_mod.TraceFile | None = None

    def compacted(self) -> None:
        self.compactions += 1


def user_turn_first(messages: list) -> list:
    """The history with a user turn before the model's first message. Compaction
    keeps the summary (system parts) and a tail that can open with the model's
    own tool call; after the system messages, Gemini refuses a tool call that
    follows neither a user turn nor a tool result. Such a tail gets
    EARLIER_TURNS in front of it; any other history is returned as it is."""
    from pydantic_ai.messages import ModelRequest, ModelResponse, SystemPromptPart, UserPromptPart

    for i, message in enumerate(messages):
        if isinstance(message, ModelRequest) and all(isinstance(p, SystemPromptPart) for p in message.parts):
            continue
        if isinstance(message, ModelResponse):
            return [*messages[:i], ModelRequest(parts=[UserPromptPart(EARLIER_TURNS)]), *messages[i:]]
        return messages
    return messages


def counted_compaction(state: RunState):
    """TieredCompaction that tells `state` each time it rewrote the history, and
    keeps a user turn first after it (`user_turn_first`). The summary prompt and
    the size are the state's (the writer's by default, the reader's own)."""
    from pydantic_ai_harness.compaction import ClearToolResults, SummarizingCompaction, TieredCompaction

    @dataclass
    class CountedCompaction(TieredCompaction):
        async def before_model_request(self, ctx: Any, request_context: Any) -> Any:
            before = request_context.messages
            n = len(before)
            out = await super().before_model_request(ctx, request_context)
            after = out.messages
            if after is not before and (len(after) != n or any(a is not b for a, b in zip(after, before))):
                log.info("compacted the conversation: %s messages -> %s", n, len(after))
                state.compacted()
            out.messages = user_turn_first(out.messages)
            return out

    return CountedCompaction(
        tiers=[ClearToolResults(max_tokens=1, keep_pairs=KEEP_TOOL_PAIRS, min_clear_tokens=MIN_CLEAR_TOKENS),
               SummarizingCompaction(max_messages=1, keep_messages=KEEP_MESSAGES, preserve_first_user_message=False,
                                     summary_prompt=state.summary_prompt or SUMMARY_PROMPT,
                                     tool_return_max_chars=1_500,
                                     summarization_capabilities=[UsageMeter(on_round=state.on_round)])],
        target_tokens=state.context_tokens or CONTEXT_TOKENS)


def _harness(state: RunState) -> list:
    """The pydantic-ai-harness capabilities (T3), in hook order. A missing piece
    is logged and left out: the daemon works without any one of them."""
    caps: list = []

    def add(name: str, make: Callable[[], Any]) -> None:
        try:
            caps.append(make())
        except Exception as exc:  # noqa: BLE001
            log.warning("%s unavailable: %s: %s", name, type(exc).__name__, exc)

    from pydantic_ai_harness.repair_tool_arguments import RepairToolArguments

    add("repair_tool_arguments", RepairToolArguments)
    if state.conversation:
        add("compaction", lambda: counted_compaction(state))
    from pydantic_ai_harness.warn_on_cache_busts import WarnOnCacheBusts

    add("warn_on_cache_busts", WarnOnCacheBusts)
    # What each round costs is counted here and nowhere else (T10); there is no
    # spend limit (F2).
    caps.append(UsageMeter(on_round=state.on_round))
    if state.trace is not None:
        caps.append(TraceRecorder(trace=state.trace))
    return caps


@asynccontextmanager
async def keep_lease(deps: tools.Deps, every_s: float | None = None):
    """While a writer run is in progress, renew its lease every
    LEASE_RENEW_IN_CALL_S: one model call may take 30 minutes, and so may the
    compaction's summary call (which pydantic-ai makes before any model-request
    hook), while the lease lives 240 s. Renews only a lease this process still
    holds for a switch at `daemon` (`_renew_after`)."""
    import asyncio

    every = LEASE_RENEW_IN_CALL_S if every_s is None else every_s

    async def keep() -> None:
        while True:
            await asyncio.sleep(every)
            try:
                _renew_after(deps)
            except Exception as exc:  # noqa: BLE001 -- never the run's failure
                log.warning("renewing the lease during a run failed: %s", exc)

    keeper = asyncio.ensure_future(keep())
    try:
        yield
    finally:
        keeper.cancel()


def build_agent(instructions: str, *, model, state: RunState | None = None):
    state = state or RunState()
    capabilities: list = [LeaseGate(), state.detector]
    try:
        from pydantic_ai.capabilities.mcp import MCP

        from probe.daemon.worker import probe_env

        env = probe_env("")
        key = env.get("PROBE_TOKEN", "")
        url = mcp_url(env.get("PROBE_BASE_URL", ""))
        if key and url and os.environ.get("PROBE_DAEMON_MCP", "1") != "0":
            # Loaded from the start: no round to load it before the first read.
            capabilities.append(MCP(url=url, authorization_token=f"Bearer {key}", id="probe", defer_loading=False))
    except Exception as exc:  # noqa: BLE001
        log.warning("Probe MCP unavailable: %s", exc)
    capabilities += _harness(state)

    agent = Agent(model, instructions=instructions, deps_type=tools.Deps, output_type=BiteResult,
                  capabilities=capabilities, retries=2)
    writes = write_tools()

    @agent.tool(sequential="shell" in writes, description=SHELL_DESCRIPTION)
    async def shell(ctx: RunContext[tools.Deps], command: str, why: str = "") -> str:
        try:
            return await tools.shell(ctx.deps, command, why)
        except Exception as exc:  # noqa: BLE001 -- R5: a failed tool is the model's to work around
            log.warning("shell tool failed: %s", exc)
            return f"tool error ({type(exc).__name__}): {exc}"
        finally:
            _renew_after(ctx.deps)

    @agent.tool(sequential="read" in writes, description=READ_DESCRIPTION)
    async def read(ctx: RunContext[tools.Deps], path: str, offset: int | None = None,
                   limit: int | None = None) -> str:
        try:
            return await tools.read_file(ctx.deps, path, offset, limit)
        except Exception as exc:  # noqa: BLE001
            log.warning("read tool failed: %s", exc)
            return f"tool error ({type(exc).__name__}): {exc}"
        finally:
            _renew_after(ctx.deps)

    # `async` on purpose, like every tool here: Pydantic AI runs a plain `def` tool in a
    # worker thread, and the session's store (one SQLite connection) refuses any thread
    # but its own -- on 0.186.1 every session_search / session_open answered
    # "tool error (ProgrammingError)". These are short local reads.
    @agent.tool(sequential="session" in writes, description=SESSION_DESCRIPTION)
    async def session(ctx: RunContext[tools.Deps], op: tools.SessionOpName, event_id: str | None = None,
                      turn: int | None = None, page: int | None = None, query: str | None = None,
                      kind: tools.KindName | None = None, turn_from: int | None = None,
                      turn_to: int | None = None) -> str:
        try:
            return tools.session(ctx.deps, op, status=state.status, event_id=event_id, turn=turn, page=page,
                                 query=query, kind=kind, turn_from=turn_from, turn_to=turn_to)
        except Exception as exc:  # noqa: BLE001
            return f"tool error ({type(exc).__name__}): {exc}"

    return agent


def write_tools() -> frozenset[str]:
    """The daemon's tools that write (`tools.WRITE_TOOLS`): each runs alone, in the
    order the model called it; every other tool runs in parallel."""
    return tools.WRITE_TOOLS


def mcp_url(base_url: str) -> str | None:
    """The Probe MCP for a daemon whose key belongs to `base_url`: `PROBE_MCP_URL`
    when set, the stock MCP beside the stock API, else none -- the daemon's key must
    never be sent to a deployment it was not minted by."""
    explicit = os.environ.get("PROBE_MCP_URL")
    if explicit:
        return explicit
    from probe.sdk.config import DEFAULT_BASE_URL

    return STOCK_MCP_URL if urlparse(base_url).netloc == urlparse(DEFAULT_BASE_URL).netloc else None


def _renew_after(deps: tools.Deps) -> None:
    """A finished tool call is progress: extend the lease (R11) -- but only one this
    process still holds for a switch still at `daemon`. Never BEFORE the tool: its
    own lease check must see a lease that lapsed, was released with a reason or
    went to another daemon, not one renewed a moment earlier."""
    if deps.replay is None and lease.held(deps.session_id) and lease.session_state(deps.session_id) == "daemon":
        lease.renew(deps.session_id)



# ---------------------------------------------------------------------------
# The reader (daemon reads): a second agent in the same worker. It only reads -
# `read`, `session` (open / outline / search) and the Probe MCP - and ends every
# turn with `final_result(message)`. Its text is the researcher's approved text
# (`~/daemon-prompts/reads/`; copies in tests/fixtures/daemon_prompts/reads/).
# ---------------------------------------------------------------------------

#: A reader turn: at most this many model rounds...
READ_ROUNDS = 8
#: ...and this many seconds (READ_WALL_ASK_S when it answers an ask).
READ_WALL_S = 60.0
READ_WALL_ASK_S = 80.0

READER_READ_DESCRIPTION = (
    "Read a file - nothing runs. Any file in the session's working folders, or the main agent's memory and "
    "instruction files.\n"
    "\n"
    "`offset` / `limit`: a range of lines (at most 2000). Neither: a preview of a CSV/TSV, JSON, Parquet or "
    "NumPy file. Never a pickle or an image."
)

READER_SESSION_DESCRIPTION = (
    "Look at the main agent's session. `op` picks what:\n"
    "\n"
    "- `open` - one event in full (`event_id`), or a whole turn (`turn`); long text comes in pages (`page`).\n"
    "- `outline` - one line per turn (`page`).\n"
    "- `search` - words across the WHOLE session (`query`; narrow with `kind`, `turn_from`, `turn_to`).\n"
    "\n"
    "Each `op` takes only its own options."
)

READER_SUMMARY_PROMPT = """\
Summarize this conversation of the Probe reader - your summary REPLACES it, so it must let the reader carry on \
without redoing work. Use these headings, and skip one only if it is empty:

## What the session is about
## What the main agent was sent
Every message and answer (with the question it answered), and the Probe ids and URLs it gave.
## Open asks
The main agent's questions not answered yet.
## Searches that found nothing
What was looked up with no result, so it is not searched again.
## Where it left off
The last turn and event ids covered.

Quote ids, numbers, metric names, URLs and paths VERBATIM. Reply with the summary only.

<messages>
{messages}
</messages>\
"""

MESSAGE_TOO_LONG = "not sent: the message is {n} characters - at most 1,200. Shorten it."
TURN_LIMIT = "not run: this turn was stopped - {why}. End it with final_result."


class ReadResult(BaseModel):
    """Ends your turn."""

    message: str = Field(
        default="",
        description="what the main agent gets, or empty for nothing. At most 1,200 characters, unless it answers an ask.")


@dataclass
class ReaderState(RunState):
    """A reader turn's shared state: the ask it answers (None: a turn on its own),
    and the plain-code limits that tell the model to end the turn."""

    ask: str | None = None
    started: float = 0.0
    rounds: int = 0
    limit_why: str | None = None


@dataclass
class ReaderLimits(AbstractCapability[tools.Deps]):
    """Counts the turn's model rounds; once the turn is out of rounds or time,
    every further tool call answers TURN_LIMIT so the model ends it with
    `final_result`. (The loop detector keys on exact arguments: a reader that
    keeps changing its query would slip past it.)"""

    state: ReaderState
    clock: Callable[[], float] = field(default=None)  # type: ignore[assignment]

    def _now(self) -> float:
        import time

        return (self.clock or time.monotonic)()

    async def wrap_model_request(self, ctx: Any, *, request_context: Any, handler: Any) -> Any:
        self.state.rounds += 1
        return await handler(request_context)

    async def before_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any) -> Any:
        wall = READ_WALL_ASK_S if self.state.ask else READ_WALL_S
        if self.state.rounds >= READ_ROUNDS - 1:
            self.state.limit_why = f"{READ_ROUNDS} model rounds"
        elif self._now() - self.state.started >= wall:
            self.state.limit_why = f"{wall:.0f} seconds"
        if self.state.limit_why is not None:
            raise SkipToolExecution(TURN_LIMIT.format(why=self.state.limit_why))
        return args


@dataclass
class ExcludeWatchedSession(AbstractCapability[tools.Deps]):
    """Every `search_knowledge` call leaves out the session the reader watches:
    it must never find the main agent's own session and hand it back as the
    team's prior work."""

    session_id: str

    async def before_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any) -> Any:
        if str(getattr(call, "tool_name", "")).endswith("search_knowledge") and isinstance(args, dict):
            args = {**args, "exclude_session": self.session_id}
        return args


def build_reader_agent(instructions: str, *, model, state: ReaderState, session_id: str,
                       agent: str):
    """The reader: `read`, `session` (its three ops), the Probe MCP and
    `final_result(message)`. No shell, no lease."""
    from pydantic_ai import ModelRetry

    capabilities: list = [ReaderLimits(state=state), ExcludeWatchedSession(session_id), state.detector]
    try:
        from pydantic_ai.capabilities.mcp import MCP

        from probe.daemon.worker import probe_env

        env = probe_env("")
        key = env.get("PROBE_TOKEN", "")
        url = mcp_url(env.get("PROBE_BASE_URL", ""))
        if key and url and os.environ.get("PROBE_DAEMON_MCP", "1") != "0":
            from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER, HIDE_SESSION_WORK_HEADER

            # The watched session, named on every MCP call: the transcript
            # self-exclusion, and the hosted MCP's opt-in that leaves out every
            # project, experiment and run THAT session created -- the work the
            # daemon's writer records as the session goes, never prior work.
            headers = {AGENT_HEADER: agent, AGENT_SESSION_HEADER: session_id, HIDE_SESSION_WORK_HEADER: "1"}
            capabilities.append(MCP(url=url, authorization_token=f"Bearer {key}", headers=headers, id="probe",
                                    defer_loading=False))
    except Exception as exc:  # noqa: BLE001
        log.warning("Probe MCP unavailable to the reader: %s", exc)
    capabilities += _harness(state)

    agent = Agent(model, instructions=instructions, deps_type=tools.Deps, output_type=ReadResult,
                  capabilities=capabilities, retries=2)

    @agent.output_validator
    async def _message_fits(ctx: RunContext[tools.Deps], result: ReadResult) -> ReadResult:
        text = (result.message or "").strip()
        if state.ask is None and len(text) > MESSAGE_MAX_CHARS():
            raise ModelRetry(MESSAGE_TOO_LONG.format(n=len(text)))
        return ReadResult(message=text)

    @agent.tool(description=READER_READ_DESCRIPTION)
    async def read(ctx: RunContext[tools.Deps], path: str, offset: int | None = None,
                   limit: int | None = None) -> str:
        try:
            return await tools.read_file(ctx.deps, path, offset, limit)
        except Exception as exc:  # noqa: BLE001
            log.warning("reader read tool failed: %s", exc)
            return f"tool error ({type(exc).__name__}): {exc}"

    @agent.tool(description=READER_SESSION_DESCRIPTION)
    async def session(ctx: RunContext[tools.Deps], op: tools.ReaderSessionOpName, event_id: str | None = None,
                      turn: int | None = None, page: int | None = None, query: str | None = None,
                      kind: tools.KindName | None = None, turn_from: int | None = None,
                      turn_to: int | None = None) -> str:
        try:
            return tools.session(ctx.deps, op, event_id=event_id, turn=turn, page=page, query=query, kind=kind,
                                 turn_from=turn_from, turn_to=turn_to)
        except Exception as exc:  # noqa: BLE001
            return f"tool error ({type(exc).__name__}): {exc}"

    return agent


def MESSAGE_MAX_CHARS() -> int:  # noqa: N802 -- read at call time: tests patch the mailbox's cap
    from probe.daemon import mailbox

    return mailbox.MESSAGE_MAX_CHARS
