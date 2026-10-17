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

    compaction          conversation mode only: past CONTEXT_TOKENS, old tool
                        results cleared first, then older turns summarized,
                        down to COMPACT_TO of it; past COMPACT_MESSAGES
                        messages, older turns summarized
    warn_on_cache_busts a collapsed prompt cache is logged
    repair_tool_arguments  malformed JSON arguments repaired before validation

and three of its own: `LoopDetector` (the same failing call 3 times, a refusal
that reads alike in 3 model rounds, or the same successful call 5 times, in one
run: the run stops), `UsageMeter` (every
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
from dataclasses import dataclass, field, replace
from probe._compat import StrEnum
from typing import Any, Callable

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.exceptions import SkipToolExecution, UnexpectedModelBehavior

from probe.daemon import lease, tools
from probe.daemon import trace as trace_mod
# The Probe MCP's address, shared with the CLI's `probe mcp tools|call` (`/probe inline`).
from probe.sdk.config import STOCK_MCP_URL, mcp_url  # noqa: F401 -- STOCK_MCP_URL re-exported

log = logging.getLogger("probe.daemon")
#: Conversation mode compacts once the context passes this many tokens (estimated).
#: The writer: 250K (Richard, 2026-10-07: "lets cap the writer to 250k tokens";
#: it was 950K, his "1m" of 09-28). Every round re-reads the whole context, and in
#: the 7 days to 10-07, 78% of writer spend ($763 of $972) was calls over 200K
#: tokens; under 272K OpenAI also bills gpt-6.1-sol at its short-context rate.
#: The reader: only the immediate reading matters (Richard, 2026-09-28: "compact
#: to 120k"). It never compacts: a turn that would pass its size starts the
#: conversation fresh instead (rule A, `reader_lane`; 2026-10-14).
#: Both are the client's own; the server can lower them (`writer_context_tokens`,
#: `read_context_tokens`; Richard 2026-10-07, T10: "server-pushed cap").
CONTEXT_TOKENS = int(os.environ.get("PROBE_DAEMON_CONTEXT_TOKENS") or 250_000)
READ_CONTEXT_TOKENS = int(os.environ.get("PROBE_READER_CONTEXT_TOKENS") or 120_000)


def _lowered_by_server(own: int, lane: str) -> int:
    from probe.daemon import model as model_mod

    server = model_mod.server_context_tokens(lane)
    return min(own, server) if server is not None and own > 0 else own


def writer_context_tokens() -> int:
    """The writer's size: CONTEXT_TOKENS, or the server's if that is lower."""
    from probe.daemon import model as model_mod

    return _lowered_by_server(CONTEXT_TOKENS, model_mod.LANE_WRITE)


def read_context_tokens() -> int:
    """The reader's size: READ_CONTEXT_TOKENS, or the server's if that is lower."""
    from probe.daemon import model as model_mod

    return _lowered_by_server(READ_CONTEXT_TOKENS, model_mod.LANE_READ)
#: While a model call runs, the writer's lease is renewed this often (a call may
#: take 30 minutes; the lease lives 240 s).
LEASE_RENEW_IN_CALL_S = 60.0
#: Compaction's first tier keeps this many recent tool call / result pairs whole...
KEEP_TOOL_PAIRS = 6
#: ...and clears nothing unless that reclaims at least this many tokens (a clear
#: rewrites history, so the provider re-caches from there: not for a few tokens).
MIN_CLEAR_TOKENS = 20_000
#: Once the context passes its size, compaction brings it down to this share of
#: it. Every compaction rewrites the history, and the provider then re-caches all
#: of it at the write price; stopping just under the size made the next bite
#: cross it again, so a long session compacted (and re-cached ~1M tokens) on
#: nearly every bite (2026-10-05, "22 messages -> 22" once a minute).
COMPACT_TO = 0.5
#: The summarizing tier keeps the newest messages, whole, up to this share of the
#: size: a token budget, since one message can be a whole bite of the session.
#: The newest message stays even when it alone is bigger.
KEEP_SHARE = 0.25
#: Compaction also runs once the history is more than this many chat messages
#: on the wire (`wire_messages`), whatever its size: the server's model route
#: refuses a request of more than 2,000 (`MAX_CHAT_MESSAGES`,
#: `app/companion/chat_router.py`). A session of small bites reached 2,003 at
#: 245K tokens, under the writer's 250K size, and its next call was refused with
#: a 400 (strand-ai, 2026-10-11). The gap to 2,000 covers what the count leaves
#: out: the instructions' own messages and EARLIER_TURNS.
COMPACT_MESSAGES = 1_800
#: ...and the summarizing tier then keeps at most this many wire messages of the
#: newest (still within KEEP_SHARE), so the next count compaction is ~1,300
#: messages away, not one round.
KEEP_MESSAGES = 500
#: The user turn put between the summary and a kept tail that opens with the
#: model's own message (`user_turn_first`).
EARLIER_TURNS = "[earlier turns are summarized above]"
#: The loop detector: the same refusal or failure in this many model rounds of
#: one run...
LOOP_FAILURES = 3
#: ...or the same successful call (tool and arguments) this many times.
LOOP_REPEATS = 5
#: Pydantic AI's own words (`_agent_graph`, pinned 2.51.0) for a response the token
#: limit cut off before any of it was an answer, or in the middle of a tool call
#: (`IncompleteToolCall`). gpt-6.1-sol spent the provider's 16,384-token default
#: thinking (strand-ai, 2026-10-09..12: 126 such calls, one request sent 14 times).
_NO_ANSWER = re.compile(r"Model token limit \(.*?\) exceeded (before any response was generated|while "
                        r"generating a tool call)")
#: What the daemon says when that happened.
ANSWERED_NOTHING = "the model thought until its token limit and answered nothing"


def answered_nothing(exc: BaseException) -> bool:
    """Did the model spend its whole token limit before answering anything? The
    same request does the same again, so it is never retried as it was. Only the
    library's own message counts: never a body a model's words could fill."""
    return isinstance(exc, UnexpectedModelBehavior) and bool(_NO_ANSWER.match(exc.message or ""))


def answered(response: Any) -> bool:
    """Did a model response come back with an answer? Only one the token limit cut
    off (`finish_reason` "length") can be none: when it holds no words and no
    complete tool call -- a call cut off mid arguments is no answer, the way
    Pydantic AI's own `IncompleteToolCall` check reads it. Any other response is
    one, a turn that only thought included (its retry is the model's next round)."""
    from pydantic_ai.messages import TextPart, ToolCallPart

    if response.finish_reason != "length":
        return True
    for part in response.parts:
        if isinstance(part, TextPart) and part.content.strip():
            return True
        if isinstance(part, ToolCallPart):
            try:
                part.args_as_dict(raise_if_invalid=True)
            except Exception:  # noqa: BLE001 -- arguments cut off mid way
                continue
            return True
    return False

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
    reply: str = Field(default="", description="Your answer to the main agent's request: what you did, or why not. "
                                               "Empty if there was none.")


#: The output tool that ends a run (pydantic-ai's name for `BiteResult`'s tool).
FINAL_RESULT = "final_result"

#: The retry a writer reads when it ended a run in the same response as a write
#: that did not land (B2): the run goes on, with what the command answered.
WRITE_LOST = ("Not ended: a write in this response did not land, so the run goes on. It answered:\n{output}\n"
              "Fix it, or say why not, then end with final_result.")


#: The retry a writer reads when it ends a run that created a project or
#: experiment, or set an experiment's conclusion, without pushing that summary
#: (plan 3.5): once per run, and "say why not" ends it.
SUMMARY_OWED = ("Not ended: these summaries were not updated in this run: {entities}. Update each "
                "(probe summary checkout, edit the file, probe summary push), or say why not, then end with "
                "final_result.")
#: The same, for an eligible experiment this run concluded with no tables or
#: charts set (plan 3.8; the checkout said so).
VISUALS_OWED = ("Not ended: these experiments have no tables or charts set: {entities}. Set them (read "
                "overview-visuals, then probe visuals options and probe visuals set), or say why not, then end "
                "with final_result.")
#: How many times the writer's output validator can send a run back: once for
#: SUMMARY_OWED, once for VISUALS_OWED.
OWED_SEND_BACKS = 2


def ends_run(ctx: RunContext) -> bool:
    """Whether the response this tool call came in also calls `final_result`:
    under pydantic-ai's default 'graceful' end strategy the run ends once the
    tools before it ran, and the model never reads their answers."""
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    last = ctx.messages[-1] if ctx.messages else None
    return isinstance(last, ModelResponse) and any(
        isinstance(p, ToolCallPart) and p.tool_name == FINAL_RESULT for p in last.parts)


def lost_write_retry(ctx: RunContext[tools.Deps], lost_before: int, output: str) -> None:
    """Raise `ModelRetry` (which suppresses the run's end) when this call lost a
    write (`Deps.lost_writes` grew) in a response that also ends the run. Not on
    the tool's last attempt: past it pydantic-ai fails the whole run, and the
    worker's open-failures list still shows the write to the next one."""
    from pydantic_ai import ModelRetry

    if ctx.deps.lost_writes > lost_before and not ctx.last_attempt and ends_run(ctx):
        raise ModelRetry(WRITE_LOST.format(output=output))


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
    EARLIER_TURNS in front of it; any other history is returned as it is.

    A tail can also open with tool results whose calls were summarized away:
    the harness's cut pairs a call with its ToolReturnPart but not with a
    RetryPromptPart, so it can land right after a round whose calls all failed
    validation. Nothing can answer to those, so a request of only such results
    is dropped there (Pydantic AI would drop it on the way out and send the
    model's tool call straight after the system messages)."""
    from pydantic_ai.messages import (
        ModelRequest,
        ModelResponse,
        RetryPromptPart,
        SystemPromptPart,
        ToolReturnPart,
        UserPromptPart,
    )

    def orphaned(message: Any) -> bool:
        return bool(message.parts) and all(
            isinstance(p, ToolReturnPart) or (isinstance(p, RetryPromptPart) and p.tool_name is not None)
            for p in message.parts)

    out: list = []
    for i, message in enumerate(messages):
        if isinstance(message, ModelRequest) and all(isinstance(p, SystemPromptPart) for p in message.parts):
            out.append(message)
            continue
        if isinstance(message, ModelRequest) and orphaned(message):
            continue
        if isinstance(message, ModelResponse):
            return [*out, ModelRequest(parts=[UserPromptPart(EARLIER_TURNS)]), *messages[i:]]
        return messages if len(out) == i else [*out, *messages[i:]]
    if len(out) == len(messages):
        return messages
    # Nothing left but the system messages: the user turn the request needs.
    return [*out, ModelRequest(parts=[UserPromptPart(EARLIER_TURNS)])]


def wire_messages(messages: list) -> int:
    """How many chat messages `messages` are on the model route, which counts
    those, not Pydantic AI's: one per model response, one per part of a request
    (each tool result, prompt and system part is its own message,
    `OpenAIChatModel._map_user_message`). One round of three parallel reads is 2
    messages here and 4 on the wire."""
    from pydantic_ai.messages import ModelRequest

    return sum(len(m.parts) if isinstance(m, ModelRequest) else 1 for m in messages)


def newest_within(messages: list, wire: int) -> int:
    """How many of the newest `messages` fit in `wire` chat messages (at least
    one)."""
    total = 0
    for n, message in enumerate(reversed(messages)):
        total += wire_messages([message])
        if total > wire:
            return max(n, 1)
    return len(messages)


def counted_compaction(state: RunState):
    """TieredCompaction that tells `state` each time it rewrote the history, and
    keeps a user turn first after it (`user_turn_first`). The size is the
    state's (the writer's by default); the reader never compacts.

    It runs once the context passes the size and compacts down to COMPACT_TO of
    it (the harness's own target is that lower mark; the size is our gate), the
    summary keeping the newest KEEP_SHARE of the size whole, and at most
    KEEP_MESSAGES wire messages. A history of more than COMPACT_MESSAGES wire
    messages is summarized whatever its size, since the model route refuses one
    past 2,000."""
    from pydantic_ai_harness.compaction import (
        ClearToolResults,
        SummarizingCompaction,
        TieredCompaction,
        estimate_context_tokens,
        estimate_token_count,
    )

    size = state.context_tokens or writer_context_tokens()
    if size <= 0:
        # Would compact before every request: refused, so the worker falls back to
        # bites (`worker._compaction_available`), as the harness's own
        # `target_tokens=0` refusal did before the floors below were added.
        raise ValueError(f"a context of {size} tokens cannot be compacted to")

    class KeptByCount(SummarizingCompaction):
        """Keeps the newest `keep_tokens`, but never more than KEEP_MESSAGES wire
        messages: when the newest KEEP_MESSAGES alone fit the token budget, the
        token cut would keep more of them, so the cut is by count."""

        async def compact(self, messages: list, ctx: Any) -> list:
            n = newest_within(messages, KEEP_MESSAGES)
            if (self.keep_tokens is not None and n < len(messages)
                    and estimate_token_count(messages[-n:], self.tokenizer) <= self.keep_tokens):
                return await replace(self, keep_tokens=None, keep_messages=n).compact(messages, ctx)
            return await super().compact(messages, ctx)

    summarizer = KeptByCount(max_messages=1, keep_tokens=max(1, int(size * KEEP_SHARE)),
                             preserve_first_user_message=False,
                             summary_prompt=SUMMARY_PROMPT,
                             tool_return_max_chars=1_500,
                             summarization_capabilities=[UsageMeter(on_round=state.on_round)])

    @dataclass
    class CountedCompaction(TieredCompaction):
        async def before_model_request(self, ctx: Any, request_context: Any) -> Any:
            before = request_context.messages
            over_size = estimate_context_tokens(list(before), self.tokenizer,
                                                model_request_parameters=request_context.model_request_parameters) > size
            if not over_size and wire_messages(before) <= COMPACT_MESSAGES:
                request_context.messages = user_turn_first(before)
                return request_context
            n, wire = len(before), wire_messages(before)
            out = await super().before_model_request(ctx, request_context) if over_size else request_context
            if wire_messages(out.messages) > COMPACT_MESSAGES:
                # Too many messages for the model route, whatever their size (or the
                # cheap tier was enough for the size): the summarizing tier, by count.
                # It calls the model this request goes to, as the tiers above do.
                tier_ctx = ctx if request_context.model is ctx.model else replace(ctx, model=request_context.model)
                out.messages = await summarizer.compact(list(out.messages), tier_ctx)
            after = out.messages
            if after is not before and (len(after) != n or any(a is not b for a, b in zip(after, before))):
                log.info("compacted the conversation (%s): %s messages (%s on the wire) -> %s (%s)",
                         "size" if over_size else "count", n, wire, len(after), wire_messages(after))
                state.compacted()
            out.messages = user_turn_first(out.messages)
            return out

    return CountedCompaction(
        tiers=[ClearToolResults(max_tokens=1, keep_pairs=KEEP_TOOL_PAIRS, min_clear_tokens=MIN_CLEAR_TOKENS),
               summarizer],
        target_tokens=max(1, int(size * COMPACT_TO)))


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
    if state.conversation and state.compacts:
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
    holds while the writer records the session (`_renew_after`)."""
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

    # The OUTPUT budget also pays for the two send-backs below (`summaries_owed`),
    # and a run never refills it: past it pydantic-ai fails the whole run.
    agent = Agent(model, instructions=instructions, deps_type=tools.Deps, output_type=BiteResult,
                  capabilities=capabilities, retries={"tools": 2, "output": 2 + OWED_SEND_BACKS})
    writes = write_tools()

    @agent.output_validator
    async def summaries_owed(ctx: RunContext[tools.Deps], output: BiteResult) -> BiteResult:
        """Send the run back once when it owes a summary (`tools.summaries_owed`).
        Not after a stop, and not twice: the second end stands, reasons and all."""
        from pydantic_ai import ModelRetry

        if ctx.deps is None or ctx.deps.stopped is not None:
            return output
        owed = tools.summaries_owed(ctx.deps)
        tables = tools.visuals_owed(ctx.deps)
        due = (owed and not ctx.deps.summaries_owed_asked) or (tables and not ctx.deps.visuals_owed_asked)
        if due and await tools.summaries_mode(ctx.deps, (owed or tables)[0]) != "recorder":
            # Lane mode refuses the push, and an unknown mode is no reason to
            # spend the rounds: the end stands.
            tools.tally_settled(ctx.deps)
            return output
        if owed and not ctx.deps.summaries_owed_asked:
            ctx.deps.summaries_owed_asked = True
            tools.tally_save(ctx.deps)
            raise ModelRetry(SUMMARY_OWED.format(entities=", ".join(owed)))
        if tables and not ctx.deps.visuals_owed_asked:
            ctx.deps.visuals_owed_asked = True
            tools.tally_save(ctx.deps)
            raise ModelRetry(VISUALS_OWED.format(entities=", ".join(tables)))
        tools.tally_settled(ctx.deps)
        return output

    @agent.tool(sequential="shell" in writes, description=SHELL_DESCRIPTION)
    async def shell(ctx: RunContext[tools.Deps], command: str, why: str = "") -> str:
        lost = ctx.deps.lost_writes
        try:
            text = await tools.shell(ctx.deps, command, why)
        except Exception as exc:  # noqa: BLE001 -- R5: a failed tool is the model's to work around
            log.warning("shell tool failed: %s", exc)
            text = f"tool error ({type(exc).__name__}): {exc}"
            ctx.deps.lost_writes += 1  # nothing says the command it was running did not write
        finally:
            _renew_after(ctx.deps)
        # Outside the `except` above, which would turn the retry into text.
        lost_write_retry(ctx, lost, text)
        return text

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


def _renew_after(deps: tools.Deps) -> None:
    """A finished tool call is progress: extend the lease (R11) -- but only one this
    process still holds while the writer still records the session (`lease.records`:
    the switch reads `daemon`). Never BEFORE the tool: its
    own lease check must see a lease that lapsed, was released with a reason or
    went to another daemon, not one renewed a moment earlier."""
    if deps.replay is None and lease.held(deps.session_id) and lease.records(deps.session_id):
        lease.renew(deps.session_id)



# ---------------------------------------------------------------------------
# The reader (daemon reads): a second agent in the same worker. It only reads -
# `read`, `session` (open / outline / search) and the Probe MCP - and ends every
# turn with `final_result(message)`. Its text is the researcher's approved text
# (`~/daemon-prompts/reads/`; copies in tests/fixtures/daemon_prompts/reads/).
# ---------------------------------------------------------------------------

#: A reader turn: at most this many model rounds...
#: Runaway guards only, never a working budget (Richard 2026-10-08: "something that
#: wouldnt reasonably be hit"). Was 8 rounds / 60 s / 80 s; on the devbox's 532
#: finished turns the most rounds was 6 bar one capped turn, and the longest took
#: 143 s (one model round on a 741K-token prompt).
READ_ROUNDS = 40
#: ...and this many seconds (READ_WALL_ASK_S when it answers an ask).
READ_WALL_S = 300.0
READ_WALL_ASK_S = 360.0
#: ...and, once a round's request is this many tokens (or more wire messages
#: than COMPACT_MESSAGES), it ends: the reader never compacts, so a turn would
#: otherwise grow round by round until the model route refuses it as over its
#: ceiling (260K) and the turn's whole work is lost. One more round of tool
#: results (a `read` page is at most ~6K tokens) still fits under the ceiling.
READ_STOP_TOKENS = 180_000

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
    "- `logbook` - words across the writer's past writes and lookups (`query`).\n"
    "\n"
    "Each `op` takes only its own options."
)

READER_FEEDBACK_DESCRIPTION = (
    "Send the Probe team feedback about Probe: what happened and what would have helped (at most 1,000 "
    "characters). The researcher sees all of it and decides - nothing is sent without their yes."
)
#: What the reader's `feedback` tool answers once the question is held.
READER_FEEDBACK_HELD = ("held as {header}: the main agent asks the researcher at their next prompt. Nothing is sent "
                        "unless they say yes.")

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
    #: The reader never compacts: the lane starts its conversation fresh instead.
    compacts: bool = False
    #: The last round's request: its provider-counted tokens and wire messages.
    last_request_tokens: int = 0
    last_request_wire: int = 0


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
        response = await handler(request_context)
        try:
            usage = getattr(response, "usage", None)
            self.state.last_request_tokens = int(getattr(usage, "input_tokens", 0) or 0)
            self.state.last_request_wire = wire_messages(list(request_context.messages)) + 1
        except Exception as exc:  # noqa: BLE001 -- a size it cannot read stops nothing
            log.warning("reader: could not size the round's request: %s", exc)
        return response

    async def before_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any) -> Any:
        wall = READ_WALL_ASK_S if self.state.ask else READ_WALL_S
        if self.state.rounds >= READ_ROUNDS - 1:
            self.state.limit_why = f"{READ_ROUNDS} model rounds"
        elif self._now() - self.state.started >= wall:
            self.state.limit_why = f"{wall:.0f} seconds"
        elif self.state.last_request_tokens >= READ_STOP_TOKENS:
            self.state.limit_why = f"{READ_STOP_TOKENS:,} tokens"
        elif self.state.last_request_wire > COMPACT_MESSAGES:
            self.state.limit_why = f"{COMPACT_MESSAGES:,} messages"
        if self.state.limit_why is not None:
            raise SkipToolExecution(TURN_LIMIT.format(why=self.state.limit_why))
        return args


#: The hosted MCP's knowledge search, under its name and the one before it.
_KNOWLEDGE_SEARCH_TOOLS = frozenset({"search", "search_knowledge"})


@dataclass
class ExcludeWatchedSession(AbstractCapability[tools.Deps]):
    """Every knowledge search leaves out the session the reader watches: it must
    never find the main agent's own session and hand it back as the team's prior
    work. Belt and braces -- the reader's MCP connection also names the session
    on `X-Probe-Agent-Session`, which the server excludes on its own.

    Matched on the tool's own name (the last `__` segment of a prefixed MCP
    name), exactly: `search` since 2026-10-08, `search_knowledge` from a hosted
    MCP that has not rolled yet. An `endswith("search")` would also catch tools
    that merely end in those letters."""

    session_id: str

    async def before_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any) -> Any:
        name = str(getattr(call, "tool_name", "")).rsplit("__", 1)[-1]
        if name in _KNOWLEDGE_SEARCH_TOOLS and isinstance(args, dict):
            args = {**args, "exclude_session": self.session_id}
        return args


def build_reader_agent(instructions: str, *, model, state: ReaderState, session_id: str,
                       agent: str):
    """The reader: `read`, `session` (its three ops), `feedback` (for the Probe
    team, asked of the researcher first), the Probe MCP and `final_result(message)`.
    No shell, no lease."""
    from pydantic_ai import ModelRetry

    harness = agent  # the watched session's harness; `agent` is the reader itself below
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

    @agent.tool(description=READER_FEEDBACK_DESCRIPTION)
    async def feedback(ctx: RunContext[tools.Deps], text: str) -> str:
        from probe import feedback as fb
        from probe.daemon import approvals as appr

        try:
            req = fb.hold(text, session_id=session_id, source=fb.Source.DAEMON_READER, harness=harness)
        except fb.Refused as exc:
            return f"not sent: {exc}"
        except Exception as exc:  # noqa: BLE001
            return f"tool error ({type(exc).__name__}): {exc}"
        if req.state == appr.DENIED:
            return f"not sent: the researcher already said no to this feedback ({req.question.header})."
        return READER_FEEDBACK_HELD.format(header=req.question.header)

    return agent


def MESSAGE_MAX_CHARS() -> int:  # noqa: N802 -- read at call time: tests patch the mailbox's cap
    from probe.daemon import mailbox

    return mailbox.MESSAGE_MAX_CHARS


# ---------------------------------------------------------------------------
# The team-note audit (daemon-team-note-audit, 2026-10-11): a third agent in the
# same worker, run once when the note is due. `shell`, `read` and the Probe MCP,
# asking nothing (`tools.Deps.audit`), editing its own copy of the note and ending
# with `final_result(report)`. Its judgment is the researcher's `audit-team-note`
# and `edit-notes` skills; its own text (`audit_note.md`) says how it runs.
# ---------------------------------------------------------------------------

#: An audit run: at most this many model rounds, and this many seconds. Runaway
#: guards only, never a working budget.
AUDIT_ROUNDS = 80
AUDIT_WALL_S = 30 * 60.0
#: Past AUDIT_WALL_S a run gets this long to end with final_result before it is cut.
AUDIT_GRACE_S = 120.0
#: A write to its copy before the run has opened any evidence (D9: Haiku 5.5 ended
#: 3 of 7 writer bites without a look). Mechanics only: what does not run, and why.
NO_EVIDENCE_YET = ("not run: the team note changes only after this audit has opened some of what it claims "
                   "(a file, a command's output, Probe) - nothing has been opened yet.")
#: The report reaches the main agent as one `[Probe]` message, opened by this label;
#: together they stay inside the mailbox's unasked cap. A longer report is cut.
AUDIT_REPORT_PREFIX = "Team-note audit: "
AUDIT_REPORT_CHARS = 1150
#: The hosted MCP's open-web tools (`probe.mcp.server._WEB_TOOLS`): text anyone can
#: author, which an audit publishing unasked into every teammate's instructions
#: must not take in.
AUDIT_REFUSED_TOOLS = frozenset({"find_papers"})
AUDIT_WEB_REFUSED = "not run: the team-note audit reads the team's records and the session's folders, not the open web."
#: The team note's folder and file (`team_note_file.paths`: `<state>/probe/team-note/
#: probe-team-note.md`) and the audit's own copy (`audit.draft_dir`, `<state>/probe/
#: audit/`): a command that names them is about the note, not evidence for it. The
#: path, not a bare "team-note" -- a repo folder may carry those words.
TEAM_NOTE_MARKERS = ("probe/team-note", "probe-team-note.md", "probe/audit/")
#: Commands that read nothing about the world: running one is not a look.
_NOT_A_LOOK = frozenset({"date", "echo", "printf", "pwd", "true", "false", "whoami", "sleep", "env", "cd"})
#: Filters that are a look only when they open a file of their own (`head -50 x.py`),
#: not as the end of a pipe (`... | head`).
_FILTERS = frozenset({"head", "tail", "wc", "sort", "uniq", "tee", "test", "["})
_SEGMENTS = re.compile(r"&&|\|\||[;|\n]")
_NUMBER = re.compile(r"^[+-]?\d+[kKmMbB]?$")
#: `probe notes sync` / `probe notes team`: the note itself, not evidence for it.
_NOTE_ITSELF = re.compile(r"^\s*probe\s+notes\s+(sync|team)\b")


class AuditResult(BaseModel):
    """Ends the audit."""

    report: str = Field(description="the report the audit-team-note skill asks for. At most 1,150 characters.")


@dataclass
class AuditState(RunState):
    """An audit run's shared state: its copy of the note (`draft`), how many looks
    it has taken (`EvidenceGate`) and the plain-code limits that tell the model to
    end it."""

    draft: str = ""
    evidence: int = 0
    started: float = 0.0
    rounds: int = 0
    limit_why: str | None = None


def _names_team_note(text: str, draft: str = "") -> bool:
    return any(marker in text for marker in TEAM_NOTE_MARKERS) or bool(draft and draft in text)


def writes_draft(command: str, draft: str) -> bool:
    """Does this shell command write the audit's copy? The shell allows a note
    write only as `cat > FILE <<'TAG'` (`shell._note_write`): the copy as the
    target of a `>` (not a `2>` or `&>`)."""
    if not draft:
        return False
    home = os.path.expanduser("~")
    spellings = {draft}
    if draft.startswith(home + os.sep):
        rest = draft[len(home):]
        spellings |= {"~" + rest, "$HOME" + rest, "${HOME}" + rest}
    targets = "|".join(re.escape(s) for s in sorted(spellings, key=len, reverse=True))
    return re.search(r"(?<![0-9&])>>?\s*['\"]?(?:" + targets + ")", command) is not None


def _opens_a_file(words: list[str]) -> bool:
    return any(not w.startswith("-") and not _NUMBER.match(w) for w in words[1:])


def is_a_look(tool_name: str, args: Any, draft: str = "") -> bool:
    """Did this (successful) tool call open some of what the note claims? A read or
    command about the team note itself, and a command that reads nothing, is not."""
    if tool_name == "read":
        return not _names_team_note(str((args or {}).get("path", "")), draft)
    if tool_name != "shell":
        return True  # the Probe MCP: the team's record
    command = str((args or {}).get("command", ""))
    if _names_team_note(command, draft):
        return False
    for part in _SEGMENTS.split(command):
        words = part.strip().split()
        if not words or words[0] in _NOT_A_LOOK or _NOTE_ITSELF.match(part):
            continue
        if words[0] in _FILTERS and not _opens_a_file(words):
            continue
        return True
    return False


@dataclass
class EvidenceGate(AbstractCapability[tools.Deps]):
    """D9 (Haiku 5.5's known failure is ending without a look): a write to the
    audit's copy is skipped until the run has opened some evidence, and every
    successful look is counted (`AuditState.evidence`), so the lane can tell a run
    that never looked from one that did. The open web is refused outright."""

    state: AuditState

    async def before_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any) -> Any:
        name = str(getattr(call, "tool_name", "")).rsplit("__", 1)[-1]
        if name in AUDIT_REFUSED_TOOLS:
            raise SkipToolExecution(AUDIT_WEB_REFUSED)
        if (call.tool_name == "shell" and self.state.evidence == 0
                and writes_draft(str((args or {}).get("command", "")), self.state.draft)):
            raise SkipToolExecution(NO_EVIDENCE_YET)
        return args

    async def after_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any, result: Any) -> Any:
        if _ran(result) and is_a_look(call.tool_name, args, self.state.draft):
            self.state.evidence += 1
        return result


_STEP_RAN = re.compile(r"^\[exit 0\b", re.M)


def _ran(result: Any) -> bool:
    """Did the call run? A compound command's output (`$ part` lines, each with its
    own `[exit N]`) ran when one of its parts exited 0: its first line alone says
    nothing (`outcome` reads only that)."""
    if isinstance(result, str) and result.lstrip().startswith("$ "):
        return bool(_STEP_RAN.search(result))
    return outcome(result) == Verdict.OK


@dataclass
class AuditLimits(AbstractCapability[tools.Deps]):
    """Counts the run's model rounds; once it is out of rounds or time, every
    further tool call answers TURN_LIMIT so the model ends it with final_result."""

    state: AuditState

    async def wrap_model_request(self, ctx: Any, *, request_context: Any, handler: Any) -> Any:
        self.state.rounds += 1
        return await handler(request_context)

    async def before_tool_execute(self, ctx: Any, *, call: Any, tool_def: Any, args: Any) -> Any:
        import time

        if self.state.rounds >= AUDIT_ROUNDS - 1:
            self.state.limit_why = f"{AUDIT_ROUNDS} model rounds"
        elif time.monotonic() - self.state.started >= AUDIT_WALL_S:
            self.state.limit_why = f"{AUDIT_WALL_S:.0f} seconds"
        if self.state.limit_why is not None:
            raise SkipToolExecution(TURN_LIMIT.format(why=self.state.limit_why))
        return args


def build_audit_agent(instructions: str, *, model, state: AuditState):
    """The team-note audit: `shell`, `read`, the Probe MCP (the writer's
    connection, its open-web tools refused) and `final_result(report)`. Its tools
    ask nothing (`tools.Deps.audit`)."""
    capabilities: list = [LeaseGate(), AuditLimits(state=state), EvidenceGate(state=state), state.detector]
    try:
        from pydantic_ai.capabilities.mcp import MCP

        from probe.daemon.worker import probe_env

        env = probe_env("")
        key = env.get("PROBE_TOKEN", "")
        url = mcp_url(env.get("PROBE_BASE_URL", ""))
        if key and url and os.environ.get("PROBE_DAEMON_MCP", "1") != "0":
            capabilities.append(MCP(url=url, authorization_token=f"Bearer {key}", id="probe", defer_loading=False))
    except Exception as exc:  # noqa: BLE001
        log.warning("Probe MCP unavailable to the audit: %s", exc)
    capabilities += _harness(state)

    agent = Agent(model, instructions=instructions, deps_type=tools.Deps, output_type=AuditResult,
                  capabilities=capabilities, retries=2)

    @agent.tool(sequential=True, description=SHELL_DESCRIPTION)
    async def shell(ctx: RunContext[tools.Deps], command: str, why: str = "") -> str:
        try:
            return await tools.shell(ctx.deps, command, why)
        except Exception as exc:  # noqa: BLE001
            log.warning("audit shell tool failed: %s", exc)
            return f"tool error ({type(exc).__name__}): {exc}"
        finally:
            _renew_after(ctx.deps)

    @agent.tool(description=READ_DESCRIPTION)
    async def read(ctx: RunContext[tools.Deps], path: str, offset: int | None = None,
                   limit: int | None = None) -> str:
        try:
            return await tools.read_file(ctx.deps, path, offset, limit)
        except Exception as exc:  # noqa: BLE001
            log.warning("audit read tool failed: %s", exc)
            return f"tool error ({type(exc).__name__}): {exc}"
        finally:
            _renew_after(ctx.deps)

    return agent
