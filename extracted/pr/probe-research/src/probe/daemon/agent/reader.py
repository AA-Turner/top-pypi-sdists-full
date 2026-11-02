"""the reader agent: one turn of read/session/feedback, bounded by rounds, wall time and size."""

from __future__ import annotations
from dataclasses import dataclass, field
from probe.foundation.compat.compat import StrEnum
from typing import Any, Callable

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.exceptions import SkipToolExecution
from probe.daemon.agent import toolset, tools
from probe.daemon.agent.state import RunState



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


class TurnLimit(StrEnum):
    """The reader guard that ended a turn. SIZE is the planned end of a turn that
    grew big (the reader never compacts); the others stop a runaway."""

    ROUNDS = "rounds"
    WALL = "wall"
    SIZE = "size"


@dataclass
class ReaderState(RunState):
    """A reader turn's shared state: the ask it answers (None: a turn on its own),
    and the plain-code limits that tell the model to end the turn."""

    ask: str | None = None
    started: float = 0.0
    rounds: int = 0
    limit_why: str | None = None
    #: Which guard set `limit_why`, as of the last tool call it stopped.
    limit_kind: TurnLimit | None = None
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
            self.state.limit_why, self.state.limit_kind = f"{READ_ROUNDS} model rounds", TurnLimit.ROUNDS
        elif self._now() - self.state.started >= wall:
            self.state.limit_why, self.state.limit_kind = f"{wall:.0f} seconds", TurnLimit.WALL
        elif self.state.last_request_tokens >= READ_STOP_TOKENS:
            self.state.limit_why, self.state.limit_kind = f"{READ_STOP_TOKENS:,} tokens", TurnLimit.SIZE
        elif self.state.last_request_wire > COMPACT_MESSAGES:
            self.state.limit_why, self.state.limit_kind = f"{COMPACT_MESSAGES:,} messages", TurnLimit.SIZE
        if self.state.limit_why is not None:
            raise SkipToolExecution(TURN_LIMIT.format(why=self.state.limit_why))
        return args


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
    bash_only = toolset.bash_only()
    capabilities: list = [ReaderLimits(state=state), ExcludeWatchedSession(session_id), state.detector]
    if bash_only:
        capabilities = _order(capabilities)
    else:
        from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER, HIDE_SESSION_WORK_HEADER

        # The watched session, named on every MCP call: the transcript
        # self-exclusion, and the hosted MCP's opt-in that leaves out every
        # project, experiment and run THAT session created -- the work the
        # daemon's writer records as the session goes, never prior work. (The
        # `bash` tool set's `probe mcp call` names it the same way:
        # `local_commands._target`.)
        _native_mcp(capabilities, " to the reader",
                    {AGENT_HEADER: agent, AGENT_SESSION_HEADER: session_id, HIDE_SESSION_WORK_HEADER: "1"})
    capabilities += _harness(state)

    agent = Agent(model, instructions=instructions, deps_type=tools.Deps, output_type=ReadResult,
                  capabilities=capabilities, retries=2)

    @agent.output_validator
    async def _message_fits(context: RunContext[tools.Deps], result: ReadResult) -> ReadResult:
        text = (result.message or "").strip()
        if state.ask is None and len(text) > MESSAGE_MAX_CHARS():
            raise ModelRetry(MESSAGE_TOO_LONG.format(n=len(text)))
        return ReadResult(message=text)

    if bash_only:
        _mcp_guide(agent)

        @agent.tool(name="bash", description=bash_description(READER_BASH_DESCRIPTION, READER_COMMAND_MAP,
                                                              tasks=True))
        async def bash(ctx: RunContext[tools.Deps], command: str, why: str = "") -> str:
            ctx.deps.harness = ctx.deps.harness or harness
            _bash_ready(ctx, state)
            try:
                return await tools.shell(ctx.deps, command, why)
            except Exception as exc:  # noqa: BLE001
                log.warning("reader bash tool failed: %s", exc)
                return f"tool error ({type(exc).__name__}): {exc}"

        return agent

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
        from probe.shared.feedback import feedback as fb
        from probe.shared.mailbox import approvals as appr

        try:
            request = fb.hold(text, session_id=session_id, source=fb.Source.DAEMON_READER, harness=harness)
        except fb.Refused as exc:
            return f"not sent: {exc}"
        except Exception as exc:  # noqa: BLE001
            return f"tool error ({type(exc).__name__}): {exc}"
        if request.state == appr.DENIED:
            return f"not sent: the researcher already said no to this feedback ({request.question.header})."
        return READER_FEEDBACK_HELD.format(header=request.question.header)

    return agent


def MESSAGE_MAX_CHARS() -> int:  # noqa: N802 -- read at call time: tests patch the mailbox's cap
    from probe.shared import mailbox

    return mailbox.MESSAGE_MAX_CHARS
from probe.daemon.agent.agent import _bash_ready, _harness, _order  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.audit import _KNOWLEDGE_SEARCH_TOOLS  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.context import COMPACT_MESSAGES, wire_messages  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.guards import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.prompts import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    READER_BASH_DESCRIPTION,
    READER_COMMAND_MAP,
    _mcp_guide,
    _native_mcp,
    bash_description,
)
