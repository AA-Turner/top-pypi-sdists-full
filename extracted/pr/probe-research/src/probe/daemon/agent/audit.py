"""the team-note audit agent: edits a draft only after it looked at evidence, within rounds and time."""

from __future__ import annotations
import json
import os
import re
import shlex
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.exceptions import SkipToolExecution
from probe.daemon.agent import toolset, tools
from probe.daemon.agent.state import RunState


#: The hosted MCP's knowledge search, under its name and the one before it.
_KNOWLEDGE_SEARCH_TOOLS = frozenset({"search", "search_knowledge"})


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


def audit_tool_refusal(tool_name: str, args: Any) -> str | None:
    """Why the team-note audit does not run this MCP call, or None: an open-web
    tool, or a search that names Probe's docs (outside text too; mixed, it rides
    beside the team's hits). Named as `ExcludeWatchedSession` names it."""
    name = str(tool_name).rsplit("__", 1)[-1]
    if name in AUDIT_REFUSED_TOOLS:
        return AUDIT_WEB_REFUSED
    search_in = args.get("search_in") if isinstance(args, dict) else None
    if name in _KNOWLEDGE_SEARCH_TOOLS and isinstance(search_in, list):
        from probe.shared.reads.search_contract import ToolCorpus  # as in `_searches_only_probe_docs`

        if ToolCorpus.DOCS in search_in:
            return AUDIT_WEB_REFUSED
    return None
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


def _searches_only_probe_docs(tool_name: str, args: Any) -> bool:
    """A knowledge search whose `search_in` is Probe's own docs alone: a product
    reference, not the team's record. Named as `ExcludeWatchedSession` names it
    (the last `__` segment); a mixed search still reads the team's record."""
    if str(tool_name).rsplit("__", 1)[-1] not in _KNOWLEDGE_SEARCH_TOOLS or not isinstance(args, dict):
        return False
    # Here, not at the top: `probe.mcp` loads the SDK client, which the daemon's
    # import does not otherwise pay for.
    from probe.shared.reads.search_contract import is_docs_only

    return is_docs_only(args.get("search_in"))


def _shell_reads_only_probe_docs(part: str) -> bool:
    """`probe docs ...`, or `probe mcp call search '<json>'` (the `bash` tool set's
    door to the MCP) with docs-only `search_in`, root options (`--base-url x`)
    allowed before the command. JSON this cannot read is a look, as any other
    command is."""
    from probe.sdk.session_marker import command_words

    try:
        words = shlex.split(part)
    except ValueError:
        return False
    if words[:1] != ["probe"]:
        return False
    args = words[1:]
    command = command_words(args)
    if command[:1] == ["docs"]:
        return True
    if command[:2] != ["mcp", "call"] or len(command) < 3:
        return False
    tool = args.index(command[2], args.index("call") + 1)
    try:
        payload = json.loads(" ".join(args[tool + 1 :]))
    except ValueError:
        return False
    return isinstance(payload, dict) and _searches_only_probe_docs(command[2], payload)


def is_a_look(tool_name: str, args: Any, draft: str = "") -> bool:
    """Did this (successful) tool call open some of what the note claims? A read or
    command about the team note itself, a command that reads nothing, and a read
    of Probe's own docs (not the team's record), is not."""
    if tool_name == "read":
        return not _names_team_note(str((args or {}).get("path", "")), draft)
    if tool_name not in ("shell", "bash"):
        # the Probe MCP: the team's record, unless it searched only Probe's docs
        return not _searches_only_probe_docs(tool_name, args)
    command = str((args or {}).get("command", ""))
    if _names_team_note(command, draft):
        return False
    for part in _SEGMENTS.split(command):
        words = part.strip().split()
        if (not words or words[0] in _NOT_A_LOOK or _NOTE_ITSELF.match(part)
                or _shell_reads_only_probe_docs(part)):
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
        refusal = audit_tool_refusal(str(getattr(call, "tool_name", "")), args)
        if refusal is not None:
            raise SkipToolExecution(refusal)
        if (call.tool_name in ("shell", "bash") and self.state.evidence == 0
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
    bash_only = toolset.bash_only()
    capabilities: list = [LeaseGate(), AuditLimits(state=state), EvidenceGate(state=state), state.detector]
    if bash_only:
        capabilities = _order(capabilities)
    else:
        _native_mcp(capabilities, " to the audit")
    capabilities += _harness(state)

    agent = Agent(model, instructions=instructions, deps_type=tools.Deps, output_type=AuditResult,
                  capabilities=capabilities, retries=2)

    if bash_only:
        _mcp_guide(agent)

        @agent.tool(name="bash", sequential=not toolset.parallel(),
                    description=bash_description(SHELL_DESCRIPTION, AUDIT_COMMAND_MAP))
        async def bash(ctx: RunContext[tools.Deps], command: str, why: str = "") -> str:
            _bash_ready(ctx, state)
            try:
                return await tools.shell(ctx.deps, command, why)
            except Exception as exc:  # noqa: BLE001
                log.warning("audit bash tool failed: %s", exc)
                return f"tool error ({type(exc).__name__}): {exc}"
            finally:
                _renew_after(ctx.deps)

        return agent

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
from probe.daemon.agent.agent import _bash_ready, _harness, _order, _renew_after  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.guards import LeaseGate, Verdict, log, outcome  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.prompts import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    AUDIT_COMMAND_MAP,
    READ_DESCRIPTION,
    SHELL_DESCRIPTION,
    _mcp_guide,
    _native_mcp,
    bash_description,
)
from probe.daemon.agent.reader import TURN_LIMIT  # noqa: E402 -- pieces need each other; the front door loads this one first
