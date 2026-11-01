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
                        messages, older turns summarized. The model writes
                        the summary's prose; plain code appends the landed
                        writes from the logbook (`with_logbook`), so no id
                        or slug in the history passed through the model
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
from typing import Any, Callable

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from probe.shared.notes import owed as owed_ledger
from probe.daemon.host import lease
from probe.daemon.agent import toolset, tools
#: While a model call runs, the writer's lease is renewed this often (a call may
#: take 30 minutes; the lease lives 240 s).
LEASE_RENEW_IN_CALL_S = 60.0


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
#: (plan 3.5): once per run, and "say why not" ends it. The words are the CLI's
#: owed ledger's (`probe.shared.notes.owed`), which an inline agent is sent back with too.
SUMMARY_OWED = owed_ledger.SUMMARY_OWED + ", then end with final_result."
#: The same, for a run this run tagged invalid with no note on it (notes parity N3).
NOTE_OWED = owed_ledger.NOTE_OWED + ", then end with final_result."
#: The same, for an eligible experiment this run concluded with no tables or
#: charts set (plan 3.8; the checkout said so).
VISUALS_OWED = ("Not ended: these experiments have no tables or charts set: {entities}. Set them (read "
                "overview-visuals, then probe visuals options and probe visuals set), or say why not, then end "
                "with final_result.")
#: How many times the writer's output validator can send a run back: once each
#: for SUMMARY_OWED, NOTE_OWED and VISUALS_OWED.
OWED_SEND_BACKS = 3


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
    # Last: the innermost wrap, so the trace records the answer the model got.
    caps.append(RetriesSpentAreRefusals())
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


def _order(capabilities: list) -> list:
    """`CallOrder` first, while calls run together (`toolset.parallel`): its
    waiting must come before every hook that can skip a call."""
    return [CallOrder(), *capabilities] if toolset.parallel() else capabilities


def _bash_ready(ctx: RunContext[tools.Deps], state: RunState) -> None:
    """What a `bash` call's deps need from its agent: `probe daemon task`'s runner
    (bound to this agent's task model -- `model.task_model`, a cheaper one when the
    server serves it (daemon cost round 7, F4) -- run usage and run state), when
    tasks are on."""
    deps = ctx.deps
    if deps is None or deps.task:
        return
    if not toolset.tasks():
        deps.task_runner = None
        return
    from probe.daemon.agent.model import model as model_mod

    model, usage = model_mod.task_model(ctx.model), ctx.usage
    # Where its trace lines go (F5): under this `bash` call, in this model round.
    call_id, round_now = ctx.tool_call_id, (state.trace.round if state.trace is not None else 0)

    async def runner(text: str):
        return await run_task(text, deps=deps, model=model, usage=usage, parent=state, task_of=call_id,
                              parent_round=round_now)

    deps.task_runner = runner


def build_agent(instructions: str, *, model, state: RunState | None = None):
    state = state or RunState()
    bash_only = toolset.bash_only()
    capabilities: list = [LeaseGate(), state.detector]
    if bash_only:
        capabilities = _order(capabilities)
    if not bash_only:
        _native_mcp(capabilities, "")
    capabilities += _harness(state)

    # The OUTPUT budget also pays for the send-backs below (`summaries_owed`),
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
        notes = tools.notes_owed(ctx.deps)
        if notes and not ctx.deps.notes_owed_asked:
            # A note is not the summary door's: no mode to wait for.
            ctx.deps.notes_owed_asked = True
            tools.tally_save(ctx.deps)
            raise ModelRetry(NOTE_OWED.format(entities=", ".join(notes)))
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

    if bash_only:
        _mcp_guide(agent)

        # Not Pydantic AI's `sequential`: `CallOrder` runs the writes alone, in
        # order, and the reads together (`toolset.parallel`; off: sequential as before).
        @agent.tool(name="bash", sequential=not toolset.parallel(),
                    description=bash_description(SHELL_DESCRIPTION, COMMAND_MAP))
        async def bash(ctx: RunContext[tools.Deps], command: str, why: str = "") -> str:
            lost = ctx.deps.lost_writes
            ctx.deps.record_status = state.status
            _bash_ready(ctx, state)
            try:
                text = await tools.shell(ctx.deps, command, why)
            except Exception as exc:  # noqa: BLE001 -- R5: a failed tool is the model's to work around
                log.warning("bash tool failed: %s", exc)
                text = f"tool error ({type(exc).__name__}): {exc}"
                if _writes(ctx.deps, command):
                    # Nothing says the command it was running did not write. Not for a call
                    # proven to read: it may run beside a write whose count this would move.
                    ctx.deps.lost_writes += 1
            finally:
                _renew_after(ctx.deps)
            lost_write_retry(ctx, lost, text)
            return text

        return agent

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

    @agent.tool(sequential="edit" in writes, description=EDIT_DESCRIPTION)
    async def edit(ctx: RunContext[tools.Deps], path: str, old: str, new: str) -> str:
        try:
            return await tools.edit_file(ctx.deps, path, old, new)
        except Exception as exc:  # noqa: BLE001 -- R5: a failed tool is the model's to work around
            log.warning("edit tool failed: %s", exc)
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
from probe.daemon.agent.answers import lost_write_retry  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.context import counted_compaction  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.guards import CallOrder, LeaseGate, RetriesSpentAreRefusals, _writes, log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.prompts import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    COMMAND_MAP,
    EDIT_DESCRIPTION,
    READ_DESCRIPTION,
    SESSION_DESCRIPTION,
    SHELL_DESCRIPTION,
    _mcp_guide,
    _native_mcp,
    bash_description,
)
from probe.daemon.agent.state import RunState, TraceRecorder, UsageMeter  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tasks import run_task  # noqa: E402 -- pieces need each other; the front door loads this one first
