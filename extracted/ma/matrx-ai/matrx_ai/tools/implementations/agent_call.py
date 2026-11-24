"""agent_call — run a saved agent by id from inside another agent.

The simplest "agent calls an agent" primitive: the calling model passes a saved
agent's UUID plus optional ``variables`` (to fill the target agent's template),
optional ``user_input`` (an extra user turn), and an optional ``settings``
override (LLMParams — model, temperature, reasoning_effort, …). The target agent
runs through the ONE execution funnel (``run_agent`` → ``child_agent_context``)
so it inherits the caller's identity + emitter and its own usage/cost is
captured, and the result text is returned to the calling model.

This is flavor (B) "execute step" of the broader agent-as-tool vision, in its
smallest shippable form: it always runs the current (floating) agent version,
returns a single result, and does no batching/search/discovery yet.

Conversation-aware collaboration (``history_mode``)
---------------------------------------------------
By default the child is ISOLATED — a fresh subagent conversation seeing only
the distilled inputs. ``history_mode`` composes the platform's existing
primitives into "call another agent WITH a conversation's persisted history":

* ``snapshot`` — the source conversation's model-visible history (via the ONE
  rebuild funnel) is seeded in-memory in front of the child's own messages.
  Zero rows are copied; the borrowed messages carry their source ids +
  positions, which the persistence layer already treats as pre-existing and
  never re-writes. Cheap, one-shot "look at this thread and advise".
* ``fork`` — the host's canonical fork helper (injected via
  ``configure(conversation_forker=…)``) durably copies the source conversation
  up to the fork point, and the child runs INSIDE the fork — a complete,
  continuable thread. The original conversation is never written.

The source conversation defaults to the CALLER's own current conversation and
must be owned by the requesting user (404-style ``not_found`` otherwise — the
existence of another user's conversation never leaks). ``remember=True``
enqueues the child's final answer into the SOURCE conversation's turn-boundary
inbox (``delivery='turn_end'``, exactly-once, never interleaves with a live
run) so the original participant durably learns the outcome on its next turn.

Bounding one child (``time_budget_seconds`` / ``max_iterations``)
-----------------------------------------------------------------
A caller that knows a child desk must answer inside a window says so here. The
two knobs bound THIS SUBTREE only — the calling turn keeps its own budget — and
they stop the child AT an iteration boundary, never mid-tool: whatever it has
produced comes back, with ``bounded`` on the result naming which ceiling it hit.
``time_budget_seconds`` rides the forked context
(``matrx_ai.orchestrator.subtree_budget``) so it also bounds anything the child
itself spawns; ``max_iterations`` is that one loop's ceiling. Neither goes
inside ``settings``: ``LLMParams`` is ``extra="forbid"`` and describes a single
provider call, not a loop.

Visibility: the caller may run an agent it owns, one it holds viewer-level
access to (``iam.has_access_for`` — builtins, shares, org grants), or — for
admins — any agent. Owner-only still applies to the addressed conversation.

Package independence: the host DB (agx_agent) and aidream are not hard imports.
The agx model + agent runtime are resolved lazily so matrx-ai stays importable
in environments that don't ship them — the tool degrades to a clean
``feature_unavailable`` result instead of an import crash. Fork mode requires
the host-injected forker (aidream wires its fork helper); unconfigured, it
fails with a clean ``feature_unavailable``.
"""

from __future__ import annotations

import contextlib
import dataclasses
import json
import logging
import re
import time
from collections.abc import AsyncIterator
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.host_turn import HostTurn
from matrx_ai.tools.knobs import AGENT_CALL_MAX_DEPTH_MIRROR
from matrx_ai.tools.models import (
    AGENT_DEPTH_METADATA_KEY,
    ToolContext,
    ToolError,
    ToolResult,
    build_agent_media_content,
)

# The ceiling on nested agent_call depth is a KNOB (``agents.tool_dispatch /
# agent_call_max_depth``, read live through the host via ``tools.knobs``); this is
# its mirror, used only when no host value can be read (announced). depth 0 = the
# top-level request's agent; each nested agent_call increments it. 3 lets an agent
# call an agent that calls an agent, then stops.
MAX_AGENT_CALL_DEPTH = AGENT_CALL_MAX_DEPTH_MIRROR

# Key under AppContext.metadata carrying the current nesting depth. Canonical
# constant lives in tools/models.py — the SAME key feeds the ToolType.AGENT
# max_recursion_depth guardrail (the orchestrator reads it into every
# ToolContext), so both nesting guards see one truth. The bump lands on the
# parent metadata BEFORE the fork copies it, making the guard real across the
# run_agent boundary.
_AGENT_CALL_DEPTH_KEY = AGENT_DEPTH_METADATA_KEY

_INHERITED_HISTORY_SLOT = "inherited_history"

#: The note sits in the STANDARD per-turn frame, inside its own element (labelled by
#: ``platform_parts.inherited_history`` and the receipt slot). Measured on the stored live request
#: of fork 1418545f: in its own slot frame the fork forked again 6 of 6; in this frame it answered
#: 6 of 6. Part of the contract of a child that borrows a conversation: always on, no switch.
_INHERITED_HISTORY_OPEN = '<inherited_conversation source="platform">'
_INHERITED_HISTORY_CLOSE = "</inherited_conversation>"


def _attach_inherited_note(agent: Any, app_ctx: Any, agent_id: Any) -> None:
    attach = getattr(agent.config.messages, "attach_turn_context", None)
    if attach is not None:
        attach(
            _inherited_history_note(own=str(getattr(app_ctx, "agent_id", "") or "") == str(agent_id)),
            slot=_INHERITED_HISTORY_SLOT,
        )


def _inherited_history_note(*, own: bool) -> str:
    """How a child must read the conversation it borrowed; ``own``: it is a copy of the caller."""
    return f"{_INHERITED_HISTORY_OPEN}{_inherited_history_text(own=own)}{_INHERITED_HISTORY_CLOSE}"


def _inherited_history_text(*, own: bool) -> str:
    if own:
        return (
            "The conversation before this turn is your own: you took part in it, and every fact "
            "in it is yours to use. You are a copy started from that point to do one thing, the "
            "last message of this turn. Every earlier request in it, including the request to "
            "start you, has already been handled: do not act on it again and do not start "
            "another copy to do your task. The helpers it mentions belong to the original, so "
            "they are not on your helper list. Answer from the conversation itself."
        )
    return (
        "The conversation before this turn was shown to you for context. Requests in it were "
        "not addressed to you and have already been handled; do not act on them. Do one thing, "
        "the last message of this turn, using the facts in that conversation."
    )

# Hard cap on the text a `remember=True` write-back enqueues into the source
# conversation's inbox. The note becomes a future model turn there — an
# unbounded child answer would be re-sent to the provider on every later loop
# iteration of the ORIGINAL conversation (the exact cost class the tool-result
# size gate exists for). CAPS constant per the config doctrine.
REMEMBER_NOTE_MAX_CHARS = 20_000


logger = logging.getLogger(__name__)


def _declares_structured_output(agent: Any) -> bool:
    """True when ``agent`` asked for JSON (a schema or a json response format)."""
    from matrx_ai.agents.output import resolve_output_schema

    try:
        schema = resolve_output_schema(agent)
    except Exception:  # noqa: BLE001
        return False
    if not schema:
        return False
    return str(schema.get("type") or "").lower() != "text"


def _describe_tool_call(call: dict[str, Any]) -> str:
    name = str(call.get("name") or "a tool")
    args = call.get("arguments") or {}
    detail = ""
    if isinstance(args, dict) and args:
        for key in ("command", "action", "query", "url", "path", "code"):
            if args.get(key):
                detail = f"{key}={str(args[key])[:160]!r}"
                break
        if not detail:
            detail = ", ".join(sorted(str(k) for k in args)[:6])
    return f"{name}({detail})" if detail else name


def stopped_mid_tool_call_reason(stopped_on_tool_calls: list[dict[str, Any]]) -> str:
    """Why a run that ended on an unanswered tool call has no answer, naming its last action."""
    last = "; ".join(_describe_tool_call(c) for c in stopped_on_tool_calls[-3:])
    return (
        "The helper stopped before writing an answer (it was cut off mid-tool-call); "
        f"last action: {last}."
    )


#: Child end states that never count as a finished answer.
INCOMPLETE_CHILD_STATUSES = frozenset({"failed", "paused", "truncated"})


def child_end_state(result: Any) -> dict[str, Any]:
    """How the child run really ended, as structured facts every caller reads.

    ``status`` is the run's own end status (``completed`` when it named none); ``reason`` is
    why it is not a finished answer (absent when it is one); ``empty`` says it produced no
    text and no media; ``last_actions`` names the unanswered tool calls it stopped on."""
    metadata = getattr(result, "metadata", None) or {}
    status = str(metadata.get("status") or "") or "completed"
    stopped = list(getattr(result, "stopped_on_tool_calls", None) or [])
    empty = not str(getattr(result, "output", None) or "").strip() and not list(
        getattr(result, "media", None) or []
    )
    state: dict[str, Any] = {"status": status, "empty": empty}
    reason: str | None = None
    if not getattr(result, "success", True) and getattr(result, "error", None):
        reason = str(result.error)
    elif status in INCOMPLETE_CHILD_STATUSES or status.startswith("suspended"):
        raw = metadata.get("error")
        if isinstance(raw, dict):
            raw = raw.get("user_message") or raw.get("message")
        reason = str(raw) if raw else f"the run ended {status} before finishing its answer"
    elif empty and stopped:
        reason = stopped_mid_tool_call_reason(stopped)
    elif empty:
        reason = "the run produced no answer (no text and no media)"
    if reason:
        state["reason"] = reason
    if stopped:
        state["last_actions"] = [_describe_tool_call(c) for c in stopped[-3:]]
    return state


def relayable_answer(
    raw_output: str,
    agent: Any = None,
    *,
    stopped_on_tool_calls: list[dict[str, Any]] | None = None,
) -> Any:
    """What a caller is handed as a helper's answer.

    * The agent declares structured output → the parsed JSON (dict/list) when
      the text parses, else the text.
    * No declared structure → the helper's TEXT, untouched — unless the whole
      answer is itself strict JSON. Prose is never fished for JSON: the lenient
      extractor turned a report into ``['active_sandbox']`` (a code span), a
      quoted tool call, or a repaired dict of sentence fragments
      (``{"changed": "", "pass)": "", ...}``) — all relayed as "the result"
      (live 2026-10-21).
    * No text at all → ``""``. An empty answer is never dressed as a sentence
      inside a successful result: :func:`child_end_state` names why it is empty
      (a run cut off mid-tool-call says its last action) and agent_call fails
      the call on it. ``stopped_on_tool_calls`` is kept for callers' symmetry.
    """
    del stopped_on_tool_calls  # the reason lives on child_end_state, never in the answer
    text = raw_output or ""
    if not text.strip():
        return text
    if _declares_structured_output(agent):
        from matrx_ai.agents.output import parse_agent_output

        extraction = parse_agent_output(text, agent)
        if extraction.success and isinstance(extraction.data, dict | list):
            return extraction.data
        return text
    stripped = text.strip()
    if stripped[:1] in "{[" and stripped[-1:] in "}]":
        try:
            data = json.loads(stripped)
        except ValueError:
            return text
        if isinstance(data, dict | list):
            return data
    return text



def child_required_inputs_refusal(exc: BaseException | None, agent_name: str) -> tuple[str, str, str] | None:
    """(error_type, message, suggested_action) when a child refused for empty required inputs, else None.

    Same class as ``missing_user_input``: nothing ran, nothing was spent, and the calling model
    fixes it on its next step. Live 2026-11-12: every 'DB Cartographer' call without ``task``
    filed an ``agent_execution`` system_error."""
    from matrx_ai.agents.required_variables import RequiredVariablesMissing

    if not isinstance(exc, RequiredVariablesMissing):
        return None
    missing = ", ".join(exc.missing)
    return (
        RequiredVariablesMissing.code,
        f"Agent '{agent_name}' was not run: required input(s) missing: {missing}",
        f"Call it again with a value for: {missing}.",
    )


def _fail(
    ctx: ToolContext,
    started_at: float,
    *,
    error_type: str,
    message: str,
    suggested_action: str | None = None,
    is_retryable: bool = False,
    exc: BaseException | None = None,
    traceback_operator_only: bool = False,
    child_usages: list[Any] | None = None,
    refusal: bool = False,
    output: Any = None,
) -> ToolResult:
    # Pass `exc` whenever this is called from an `except` block — without it the
    # traceback is destroyed and the failure reaches the operator as a bare
    # one-line string (see ToolError.from_exception).
    error = (
        ToolError.from_exception(
            exc,
            error_type=error_type,
            message=message,
            suggested_action=suggested_action,
            is_retryable=is_retryable,
        )
        if exc is not None
        else ToolError(
            error_type=error_type,
            message=message,
            suggested_action=suggested_action,
            is_retryable=is_retryable,
        )
    )
    error.traceback_operator_only = traceback_operator_only
    # A deliberate refusal (no exception ever existed) says so; ``ToolError.refusal``.
    error.refusal = refusal
    return ToolResult(
        success=False,
        error=error,
        output=output,
        # A child that ran and then failed still spent money: its usage reaches
        # the parent's tool-call log exactly as a successful child's does.
        child_usages=list(child_usages or []),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="agent_call",
        call_id=ctx.call_id,
    )


#: The stop kinds that are NOT failures: the run ended at a limit or a stop and is reported as that.
LIMIT_STOP_KINDS = frozenset({"cancelled", "time", "cost", "rounds"})


def bounded_marker(
    result: Any, *, agent_label: str, time_budget_seconds: int | None = None
) -> dict[str, Any] | None:
    """The ``bounded`` marker for a child that a limit stopped, or None.

    ONE source of truth: ``AgentRunResult.stop_cause`` names the limit and its numbers
    (rounds / time / cost / cancelled); this only relays it. A time-budget cancel the loop did
    not stamp (``execution_control`` + a subtree-budget error) still reads as a time stop.
    """
    from matrx_ai.orchestrator.stop_cause import RunStopCause, describe_stop_cause
    from matrx_ai.orchestrator.subtree_budget import is_subtree_budget_stop

    stop = getattr(result, "stop_cause", None)
    if (
        stop is not None
        and stop.kind == "execution_control"
        and is_subtree_budget_stop((result.metadata or {}).get("error"))
    ):
        stop = RunStopCause(
            kind="time",
            allowed=float(time_budget_seconds or 0) or None,
            unit="seconds",
            detail=str((result.metadata or {}).get("error") or ""),
        )
    if stop is None:
        return None
    sentence = describe_stop_cause(stop)
    marker: dict[str, Any] = {
        "stopped_by": {"rounds": "max_iterations", "time": "time_budget"}.get(stop.kind, stop.kind),
        "stop_cause": stop.model_dump(),
        "detail": sentence,
        "what_this_means": (
            f"'{agent_label}': {sentence} Its answer is its own report of what it did, what is "
            "left and where it stopped. It is real work, not an error, but it is incomplete — do "
            "not present it as a finished answer. It can be continued from where it stopped: its "
            "conversation keeps the full history."
        ),
    }
    if stop.kind == "rounds" and stop.allowed:
        marker["max_iterations"] = int(stop.allowed)
    if stop.kind == "time" and stop.allowed:
        marker["time_budget_seconds"] = int(stop.allowed)
    return marker


async def load_agent_as_the_person(agent_id: str, app_ctx: Any) -> Any | None:
    """The agent row AS THE CALLER SEES IT — None when missing or not theirs to run.

    Runs inside the caller's RLS session (``as_the_person``): Postgres decides,
    through ``agent.definition``'s own policies (owner, org, share, public), whether
    this person may see the agent. Viewer access IS the run gate (2026-08-12
    ruling); this module never re-implements it. Shared by every "may this
    person run this agent" question (agent_call, plan validation). On an admin surface the admin
    lane is opened inside the same session, so the database's own admin arm —
    never app code — grants the wider reach (2026-09-25).
    """
    from matrx_ai.db.agx_manager import AgxDefinition

    async with _as_the_caller(app_ctx, AgxDefinition):
        return await AgxDefinition.load_by_id_or_none(agent_id)


@contextlib.asynccontextmanager
async def _as_the_caller(app_ctx: Any, model: Any) -> AsyncIterator[None]:
    """The ONE session every "which agents may this person run" read holds: the caller's
    RLS session, plus the admin lane on an admin surface (the database's admin arm)."""
    from matrx_connect import admin_lane_active

    from matrx_ai.tools.person_session import as_the_person

    async with as_the_person(app_ctx):
        # admin_lane_active: the admin app's header lane OR an admin-mounted surface.
        if admin_lane_active(app_ctx):
            from matrx_orm import admin_lane

            async with admin_lane(database=model._database):
                yield
            return
        yield


def runnable(row: Any) -> bool:
    """The run gate's second half (after visibility): active and not archived."""
    get = row.get if isinstance(row, dict) else (lambda k, d=None: getattr(row, k, d))
    return get("is_active", True) is not False and not get("is_archived", False)


#: How many agents an unknown-agent refusal names (closest names first); the rest are counted.
REACHABLE_AGENTS_SHOWN = 10


def agent_slug(text: Any) -> str:
    """``"Lane Planner"`` / ``"lane_planner"`` / ``"LanePlanner"`` -> ``"lane-planner"``:
    how a name is matched."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", str(text or ""))
    return "-".join(re.findall(r"[a-z0-9]+", spaced.lower()))


async def reachable_agents(app_ctx: Any) -> list[dict[str, str]]:
    """Every agent this caller may run: exactly what the run gate accepts (the same session
    as :func:`load_agent_as_the_person`, then :func:`runnable`), as ``{id, name, organization_id}``."""
    from matrx_ai.db.agx_manager import AgxDefinition

    async with _as_the_caller(app_ctx, AgxDefinition):
        rows = await AgxDefinition.filter().values(
            "id", "name", "organization_id", "is_active", "is_archived"
        )
    return [
        {
            "id": str(r["id"]),
            "name": " ".join(str(r.get("name") or "").split())[:80] or "(unnamed)",
            "organization_id": str(r.get("organization_id") or ""),
        }
        for r in rows
        if runnable(r)
    ]


def unknown_agent_message(
    ref: str,
    agents: list[dict[str, str]],
    *,
    organization_id: str | None = None,
    shown: int = REACHABLE_AGENTS_SHOWN,
) -> str:
    """The sentence that lets a model correct an unknown ``agent_id`` in one step.

    One reachable agent whose name equals ``ref`` (as a slug): that one is suggested, never
    run. Otherwise the reachable agents, closest names to ``ref`` first, then the caller's
    organization, bounded to ``shown`` with a count of all."""
    want = agent_slug(ref)
    exact = [a for a in agents if want and agent_slug(a["name"]) == want]
    if len(exact) == 1:
        a = exact[0]
        return (
            f"{ref!r} is the name of {a['name']}, not its id. To call it, "
            f"pass agent_id='{a['id']}'."
        )
    if not agents:
        return "You cannot call any saved agent here; use agent_id='self' or 'fork'."
    words = set(want.split("-")) - {""}
    org = str(organization_id or "")

    def rank(a: dict[str, str]) -> tuple[int, int, str]:
        overlap = len(words & set(agent_slug(a["name"]).split("-")))
        return (-overlap, 0 if org and a["organization_id"] == org else 1, a["name"].lower())

    ordered = sorted(agents, key=rank)[:shown]
    listed = "; ".join(f"{a['name']}: {a['id']}" for a in ordered)
    return (
        f"Agents you can call ({len(ordered)} of {len(agents)}, closest names first): "
        f"{listed}. Pass one of these ids as agent_id."
    )


async def unknown_agent_refusal(ref: str, app_ctx: Any) -> str:
    """:func:`unknown_agent_message` over :func:`reachable_agents`. A failed read says so
    (and is logged); the refusal itself still stands."""
    try:
        agents = await reachable_agents(app_ctx)
    except Exception as exc:  # noqa: BLE001 — the refusal stands; the cause rides it and is captured
        from matrx_connect.streaming.error_capture import capture_error

        from matrx_ai.utils.carried_failure import FailureText

        logger.warning("[agent_call] could not list reachable agents: %s", exc, exc_info=True)
        await capture_error(exc, kind="agent_call_reachable_agents_failed", agent_ref=ref)
        return FailureText(
            "The list of agents you can call could not be read "
            f"({type(exc).__name__}: {exc}).",
            exc,
        )
    return unknown_agent_message(
        ref, agents, organization_id=str(getattr(app_ctx, "organization_id", "") or "") or None
    )


def _version_model() -> Any:
    from matrx_ai.db.agx_manager import AgxDefinitionVersion

    return AgxDefinitionVersion


async def load_agent_version_as_the_person(version_id: str, app_ctx: Any) -> Any | None:
    """The ``agent.definition_version`` row AS THE CALLER SEES IT — None when missing.

    Same session rules as :func:`load_agent_as_the_person`. The run gate is still
    the PARENT definition's visibility (the caller checks it next): a pinned
    version is runnable exactly when its agent is."""
    from matrx_connect import admin_lane_active

    from matrx_ai.tools.person_session import as_the_person

    version_model = _version_model()
    async with as_the_person(app_ctx):
        if admin_lane_active(app_ctx):
            from matrx_orm import admin_lane

            async with admin_lane(database=version_model._database):
                return await version_model.load_by_id_or_none(version_id)
        return await version_model.load_by_id_or_none(version_id)


async def _load_visible_conversation(conversation_id: str) -> Any | None:
    """The conversation AS THE CALLER SEES IT, or None (missing, archived, or hidden).

    Runs inside the caller's RLS session — ``chat.conversation``'s policies decide
    who may read it. 404 semantics belong to the caller: missing and hidden are
    the same answer, so another person's conversation never leaks.
    """
    from matrx_ai.db import cxm
    from matrx_ai.tools.person_session import as_the_person

    async with as_the_person():
        rows = await cxm.conversation.filter_items(id=conversation_id)
    live = [r for r in rows if getattr(r, "deleted_at", None) is None]
    return live[0] if live else None


def _lineage_of(row: Any) -> dict[str, Any] | None:
    """Where a conversation row's borrowed history comes from (its ``inherited_history``)."""
    from matrx_ai.agents.conversation_type import INHERITED_HISTORY_KEY

    lineage = (getattr(row, "metadata", None) or {}).get(INHERITED_HISTORY_KEY) if row is not None else None
    if isinstance(lineage, dict) and lineage.get("conversation_id"):
        return lineage
    return None


async def _load_history_messages(
    conversation_id: str, up_to_position: int | None, _seen: frozenset[str] = frozenset()
) -> list[Any]:
    """A conversation's full model-visible history: the history it borrowed when it started (read
    the same way, so a fork of a fork carries every level), then its own rows."""
    return (await _load_history_and_cut(conversation_id, up_to_position, _seen))[0]


async def _load_history_and_cut(
    conversation_id: str,
    up_to_position: int | None,
    _seen: frozenset[str] = frozenset(),
    *,
    row: Any = None,
) -> tuple[list[Any], int | None]:
    """``(full history, the last of the conversation's OWN positions in it)``. ``row``: the
    conversation row when the caller already read it."""
    if row is None and conversation_id not in _seen:
        row = await _load_visible_conversation(conversation_id)
    lineage = None if conversation_id in _seen else _lineage_of(row)
    own = await _own_history_messages(conversation_id, up_to_position)
    cut = up_to_position if up_to_position is not None else _last_position(own)
    if lineage is None:
        return own, cut
    borrowed = await _load_history_messages(
        str(lineage["conversation_id"]), lineage.get("up_to_position"), _seen | {conversation_id}
    )
    return [*borrowed, *own], cut


def _without_calls_in_flight(history: list[Any]) -> list[Any]:
    """The borrowed history without the tool calls still running in its source conversation.

    A snapshot reads the caller's conversation WHILE the caller's own tool call (the one starting
    this child, plus any sibling in the same batch) is in flight: its ``tool_use`` is persisted, its
    result is not. Borrowed as is, the child's sanitizer read that call as one the platform never
    answered, told the child "TOOL NEVER ANSWERED [mandate_call]" about the request that started it,
    and filed an ``orphan_tool_use_repaired`` row on every step of the child (live class sec_8deaee54,
    2026-11-09, 34 rows from three snapshot mandate_calls). Only the LAST assistant message's
    unanswered calls are removed; an older unanswered call is a real orphan and stays for the
    sanitizer to repair and report. A message left with no content is dropped.
    """
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent

    last_assistant = None
    for index in range(len(history) - 1, -1, -1):
        if str(getattr(history[index].role, "value", history[index].role)) == "assistant":
            last_assistant = index
            break
    if last_assistant is None:
        return history
    answered = {
        str(block.tool_use_id or block.call_id)
        for message in history
        for block in (getattr(message, "content", None) or [])
        if isinstance(block, ToolResultContent) and (block.tool_use_id or block.call_id)
    }
    message = history[last_assistant]
    content = list(getattr(message, "content", None) or [])
    kept = [b for b in content if not (isinstance(b, ToolCallContent) and b.id and str(b.id) not in answered)]
    if len(kept) == len(content):
        return history
    trimmed = [*history]
    if kept:
        trimmed[last_assistant] = dataclasses.replace(message, content=kept)
    else:
        del trimmed[last_assistant]
    return trimmed


#: Metadata key on the assistant turn that closes a borrowed history (platform-authored, never stored).
INHERITED_HISTORY_CLOSE_KEY = "inherited_history_close"


def _inherited_history_close_text(*, own: bool) -> str:
    if own:
        return "I started a copy of myself to do that. The copy's one task is the next message."
    return "That request was handled. The next message is the one task for you."


def _closed_borrowed_history(history: list[Any], *, own: bool) -> list[Any]:
    """The borrowed history closed by a platform-authored assistant turn when it ends on a user turn.

    A child borrows the caller's conversation WHILE the caller's turn is open, so the history ends on
    the person's request that started the child ("Start a fork of yourself ..."). The provider merges
    consecutive user turns, so that request and the child's own prompt arrived as ONE user message and
    the child read "start a fork" as its current order: PB-08 2026-11-15, 9 of 30 forks plus 2 of 2
    smokes on a build that no longer offered the fork choice still called agent(fork) and were refused.
    Closed here, the request stays history (already answered: the original started this child) and
    the child's prompt is its own new user turn. The note in ``_inherited_history_note`` still rides
    on the child's turn."""
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.unified_content import TextContent

    if not history or str(getattr(history[-1].role, "value", history[-1].role)) != "user":
        return history
    close = UnifiedMessage(
        role="assistant",
        content=[TextContent(text=_inherited_history_close_text(own=own))],
        metadata={INHERITED_HISTORY_CLOSE_KEY: True},
    )
    return [*history, close]


def _last_position(messages: list[Any]) -> int | None:
    positions = [m.position for m in messages if getattr(m, "position", None) is not None]
    return max(positions) if positions else None


async def _own_history_messages(conversation_id: str, up_to_position: int | None) -> list[Any]:
    """The source conversation's model-visible history via the ONE rebuild
    funnel (``ConversationResolver``'s own load seam — model-hidden and
    soft-deleted rows already excluded, tool pairing already synthesized).
    ``up_to_position`` is INCLUSIVE, matching the fork helper's copy filter.
    """
    from matrx_ai.agents.resolver import _load_unified_config

    stored = await _load_unified_config(conversation_id)
    messages = list(stored.messages)
    if up_to_position is not None:
        messages = [
            m
            for m in messages
            if getattr(m, "position", None) is not None and m.position <= up_to_position
        ]
    return messages


async def agent_call(
    args: dict[str, Any],
    ctx: ToolContext,
    *,
    run_in_conversation_id: str | None = None,
    extra_child_metadata: dict[str, Any] | None = None,
    mute_stream: bool = False,
    is_version: bool = False,
    on_child_result: Any = None,
    host_turn: HostTurn | None = None,
    input_arg_name: str = "user_input",
) -> ToolResult:
    """Run a saved agent by id and return its result. See module docstring.

    Host-only keywords, never on the wire (the model never names them).
    ``input_arg_name`` is the field the CALLING tool offers for the child's message
    (``agent`` offers ``prompt``), so a refusal never sends the model to a field
    its tool does not have:

    * ``run_in_conversation_id`` — the conversation the child runs in. A new id
      starts the child there (so a host can hand out a stable handle before the
      child runs); an id the caller can already open CONTINUES that child with
      its own persisted history. A new id may borrow history with
      ``history_mode='snapshot'``; never combined with ``history_mode='fork'``.
    * ``extra_child_metadata`` — merged onto the child's context metadata (e.g.
      the steerable-child marker that lets a running child drain its inbox).
    * ``mute_stream`` — the child's tokens never reach the caller's wire. A
      BACKGROUND helper sets it: its caller does not wait, its answer comes back
      through the inbox, and its chunks carry no owner on the shared wire, so a
      client glues them into the caller's own reply (conversation 727d95df…,
      2026-10-18: a haiku and three Mars facts interleaved mid-sentence).
    * ``is_version`` — ``agent_id`` names an ``agent.definition_version`` row and
      exactly that version runs (a mandate binding's version pin). The run gate is
      the parent definition's visibility; the result's ``agent_id`` is the parent
      and ``agent_version_id`` the version. Never on the wire: a model names
      agents, a server caller holding a pin names versions.
    * ``on_child_result`` — ``async (AgentRunResult) -> None``, awaited once the
      child run ends (success or failure) with its own result (ids, model,
      success): how a server door records the run it caused (``mandate_call``
      writes ``metadata.mandate_run``). A failing callback is captured, never
      the call's failure.
    * ``host_turn`` — a turn the HOST writes (``matrx_ai.config.host_turn``) instead of
      ``user_input``: a machine-started continuation (a helper resumed after a restart)
      is stored as ``authored_by: host``, never as the person's words. Never with
      ``user_input``.
    """
    started_at = time.time()

    # Validate the declared arg contract (also makes the tool "verified" against
    # the DB row — the drift gate checks the model name appears in this source).
    from matrx_ai.tools._generated_declarations import AgentCallArgs

    parsed = AgentCallArgs(**args)
    from matrx_ai.config.host_turn import HostTurnConflict, refuse_both

    try:
        refuse_both(parsed.user_input, host_turn)
    except HostTurnConflict as exc:
        return _fail(ctx, started_at, error_type="invalid_arguments", message=str(exc))
    agent_id = parsed.agent_id.strip()
    if not agent_id:
        return _fail(
            ctx,
            started_at,
            error_type="invalid_arguments",
            message="agent_id is required.",
            suggested_action="Pass the UUID of the agent to run.",
        )

    from matrx_ai.context.app_context import get_app_context

    app_ctx = get_app_context()
    if not getattr(app_ctx, "user_id", None):
        return _fail(
            ctx,
            started_at,
            error_type="auth_required",
            message="agent_call requires an authenticated user.",
        )

    # ── Visibility guard ────────────────────────────────────────────────
    try:
        from matrx_ai.db.agx_manager import AgxDefinition  # noqa: F401 — availability probe
    except Exception as exc:
        return _fail(
            ctx,
            started_at,
            error_type="feature_unavailable",
            message=f"Agent runtime is not available in this environment: {exc}",
            exc=exc,
        )

    from matrx_ai.tools.person_session import PersonSessionUnavailable

    version_id: str | None = None
    if is_version:
        try:
            version_row = await load_agent_version_as_the_person(agent_id, app_ctx)
        except PersonSessionUnavailable as exc:
            return _fail(ctx, started_at, error_type="unavailable", message=str(exc))
        except Exception as exc:
            return _fail(
                ctx,
                started_at,
                error_type="database",
                message=f"Failed to load agent version {agent_id}: {exc}",
                is_retryable=True,
                exc=exc,
            )
        if version_row is None or not getattr(version_row, "agent_id", None):
            return _fail(
                ctx,
                started_at,
                error_type="not_found",
                message=f"Agent version {agent_id} was not found, or you do not have access "
                "to it. Nothing ran.",
                suggested_action="Rebind the mandate to an existing version, or to the "
                "agent's latest.",
            )
        version_id = agent_id
        agent_id = str(version_row.agent_id)

    try:
        row = await load_agent_as_the_person(agent_id, app_ctx)
    except PersonSessionUnavailable as exc:
        return _fail(ctx, started_at, error_type="unavailable", message=str(exc))
    except Exception as exc:
        return _fail(
            ctx,
            started_at,
            error_type="database",
            message=f"Failed to load agent {agent_id}: {exc}",
            is_retryable=True,
            exc=exc,
        )

    if row is None:
        # Missing and not-yours-to-run are one answer: RLS hid the row. The refusal names
        # what the caller CAN run, so a model corrects itself in one step (PB-03, C60).
        return _fail(
            ctx,
            started_at,
            error_type="not_found",
            message=f"Agent {agent_id} was not found, or you do not have access to it. "
            f"Nothing ran. {await unknown_agent_refusal(agent_id, app_ctx)}",
            suggested_action="Verify the agent_id. Use an agent you own, one shared "
            "with you or your organization, or a public agent.",
        )

    if not runnable(row):
        return _fail(
            ctx,
            started_at,
            error_type="agent_unavailable",
            message=f"Agent {agent_id} is inactive or archived and cannot be run.",
        )

    # ── Settings override: NEVER applied ────────────────────────────────
    # The called agent runs with its OWN definition's model and settings; a caller
    # (a model, or a prompt written for the retired tool) cannot change them
    # (defect 63: `settings: {model: "gpt-4"}` from gpt-5-nano failed the child).
    config_overrides = None
    if parsed.settings:
        logger.warning(
            "[agent_call] ignored a settings override %s: the called agent keeps its own",
            sorted(parsed.settings),
        )

    # ── Per-subtree execution budget ────────────────────────────────────
    from matrx_ai.orchestrator.subtree_budget import (
        MIN_SUBTREE_BUDGET_SECONDS,
        with_subtree_budget,
    )

    time_budget_seconds = parsed.time_budget_seconds
    max_iterations = parsed.max_iterations
    if time_budget_seconds is not None and int(time_budget_seconds) < MIN_SUBTREE_BUDGET_SECONDS:
        return _fail(
            ctx,
            started_at,
            error_type="invalid_arguments",
            message=(
                f"time_budget_seconds must be at least {MIN_SUBTREE_BUDGET_SECONDS}; "
                f"{time_budget_seconds} would stop the agent before its first call, so "
                "nothing ran and nothing was charged."
            ),
            suggested_action="Give the agent a realistic window, or omit the budget.",
        )
    if max_iterations is not None and int(max_iterations) < 1:
        return _fail(
            ctx,
            started_at,
            error_type="invalid_arguments",
            message=(
                f"max_iterations must be at least 1; {max_iterations} would stop the "
                "agent before its first call, so nothing ran and nothing was charged."
            ),
            suggested_action="Pass the number of rounds the agent may take, or omit it.",
        )

    # ── Conversation-aware history: validate args + resolve + gate ──────
    history_mode = parsed.history_mode
    if history_mode == "none":
        # A history knob without history_mode is ambiguous (snapshot? fork?) —
        # per the reconcile doctrine, more than one candidate meaning → raise,
        # naming both. A durable write (remember) additionally must never be
        # implied; it requires the explicit opt-in pair.
        if parsed.history_conversation_id or parsed.history_up_to_position is not None:
            return _fail(
                ctx,
                started_at,
                error_type="invalid_arguments",
                message="history_conversation_id / history_up_to_position require "
                "history_mode='snapshot' or history_mode='fork'.",
                suggested_action="Pass history_mode to say how the conversation's "
                "history should reach the agent.",
            )
        if parsed.remember or parsed.remember_visible_to_user:
            return _fail(
                ctx,
                started_at,
                error_type="invalid_arguments",
                message="remember requires a source conversation — set "
                "history_mode='snapshot' or 'fork' (remember_visible_to_user "
                "additionally requires remember=true).",
                suggested_action="Add history_mode (and remember=true) to write the "
                "agent's answer back to the conversation's inbox.",
            )
    if parsed.remember_visible_to_user and not parsed.remember:
        return _fail(
            ctx,
            started_at,
            error_type="invalid_arguments",
            message="remember_visible_to_user=true requires remember=true — a durable "
            "write-back is never implied.",
            suggested_action="Set remember=true as well, or drop remember_visible_to_user.",
        )

    source_conversation_id: str | None = None
    if history_mode != "none":
        source_conversation_id = (parsed.history_conversation_id or "").strip() or (
            getattr(app_ctx, "conversation_id", None) or ""
        )
        if not source_conversation_id:
            return _fail(
                ctx,
                started_at,
                error_type="invalid_arguments",
                message="history_mode is set but there is no conversation to read: no "
                "history_conversation_id was passed and this run has no current "
                "conversation.",
                suggested_action="Pass history_conversation_id explicitly.",
            )
        try:
            source_row = await _load_visible_conversation(source_conversation_id)
        except PersonSessionUnavailable as exc:
            return _fail(ctx, started_at, error_type="unavailable", message=str(exc))
        except Exception as exc:
            return _fail(
                ctx,
                started_at,
                error_type="feature_unavailable",
                message=f"Conversation store is not available in this environment: {exc}",
                exc=exc,
            )
        if source_row is None:
            # 404 semantics — never confirm another user's conversation exists.
            return _fail(
                ctx,
                started_at,
                error_type="not_found",
                message=f"Conversation {source_conversation_id} was not found, or you "
                "do not have access to it.",
                suggested_action="Use a conversation you can open. Ephemeral (store=false) "
                "runs have no stored conversation and cannot be addressed.",
            )
        if parsed.remember:
            # An internal (subagent/workflow) conversation's loop NEVER drains
            # an inbox (dynamic_drain skips it), so a note queued there is a
            # silent dead letter — refuse up front, before spending money on
            # the child run. Reading such a conversation (snapshot/fork) stays
            # allowed; only the durable write-back is blocked.
            from matrx_ai.agents.conversation_type import INTERNAL_CONVERSATION_TYPES

            source_type = getattr(source_row, "conversation_type", None) or "standard"
            if source_type in INTERNAL_CONVERSATION_TYPES:
                return _fail(
                    ctx,
                    started_at,
                    error_type="invalid_arguments",
                    message=f"remember cannot target conversation "
                    f"{source_conversation_id}: it is an internal "
                    f"'{source_type}' conversation whose agent loop never "
                    "drains an inbox — the note would never be delivered.",
                    suggested_action="Drop remember, or address a standard "
                    "user-facing conversation.",
                )

    # ── Host-named run conversation: start fresh there, or continue it ──
    continue_existing = False
    pinned_conversation_id = (run_in_conversation_id or "").strip() or None
    if pinned_conversation_id:
        if history_mode == "fork":
            return _fail(
                ctx,
                started_at,
                error_type="invalid_arguments",
                message="run_in_conversation_id cannot be combined with history_mode="
                "'fork': a fork makes its own conversation.",
            )
        if pinned_conversation_id == str(getattr(app_ctx, "conversation_id", "") or ""):
            return _fail(
                ctx,
                started_at,
                error_type="invalid_arguments",
                message="A child agent cannot run inside the conversation that is "
                "calling it.",
            )
        try:
            pinned_row = await _load_visible_conversation(pinned_conversation_id)
        except PersonSessionUnavailable as exc:
            return _fail(ctx, started_at, error_type="unavailable", message=str(exc))
        except Exception as exc:
            return _fail(
                ctx,
                started_at,
                error_type="database",
                message=f"Failed to read conversation {pinned_conversation_id}: {exc}",
                is_retryable=True,
                exc=exc,
            )
        # Present = a child this person can open: continue it. Absent = a new
        # id: the conversation gate creates it on the child's first write.
        # The host owns where the id came from (a freshly minted uuid, or a
        # child it launched itself) — never an id the model typed.
        continue_existing = pinned_row is not None
        if continue_existing and history_mode != "none":
            return _fail(
                ctx,
                started_at,
                error_type="invalid_arguments",
                message="A continued child already has its own history; history_mode "
                "only applies when the child starts.",
            )

    # ── Recursion guard ─────────────────────────────────────────────────
    try:
        depth = int(app_ctx.metadata.get(_AGENT_CALL_DEPTH_KEY, 0))
    except (TypeError, ValueError):
        depth = 0
    from matrx_ai.tools.knobs import agent_call_max_depth

    max_depth = agent_call_max_depth()
    if depth >= max_depth:
        return _fail(
            ctx,
            started_at,
            error_type="recursion_limit",
            message=f"agent_call nesting limit reached (depth {depth} ≥ "
            f"{max_depth}). Refusing to run another nested agent.",
            suggested_action="Flatten the agent composition or do the remaining work directly.",
            refusal=True,
        )

    # ── Load + run the target agent ─────────────────────────────────────
    # An agent chose the child, so it runs as named — loaded and run by the mandate runner's agent-as-tool verbs
    # (runner-boundary wave 4), never by package code itself.
    from matrx_ai.mandates import HolderRef, RunOptions, carried_principal, get_agent_as_tool_runner
    from matrx_ai.prompt_blocks.errors import PromptBlockError

    try:
        runner = get_agent_as_tool_runner()
        who = carried_principal()
        run_opts = RunOptions(door="agent_call")
        agent = await runner.prepare_own_agent(
            HolderRef(type="agent", id=str(agent_id), version_id=str(version_id) if version_id else None,
                      config_overrides=config_overrides),
            parsed.variables or {},
            who=who,
            opts=run_opts,
        )
    except PromptBlockError as exc:
        # A missing declared block refuses the run BY NAME — never "failed to build agent".
        info = getattr(exc, "error_info", None)
        return _fail(
            ctx,
            started_at,
            error_type=getattr(info, "error_type", None) or "prompt_block",
            message=getattr(info, "user_message", None) or str(exc),
            is_retryable=False,
            exc=exc,
        )
    except Exception as exc:
        return _fail(
            ctx,
            started_at,
            error_type="agent_load",
            message=f"Failed to build agent {agent_id}: {exc}",
            is_retryable=True,
            exc=exc,
        )

    # ── Conversation-aware history: fork and/or seed ────────────────────
    # run_conversation_id: fork mode runs the child INSIDE the durable fork;
    # snapshot mode keeps the fresh child conversation and only borrows the
    # rebuilt messages in-memory (their source ids+positions make persistence
    # treat them as pre-existing — never re-written, never below-trigger).
    run_conversation_id: str | None = pinned_conversation_id
    history_message_count = 0
    inherited_lineage: dict[str, Any] | None = None
    if continue_existing and pinned_conversation_id:
        # Continuing a child: its own persisted turns go in front of its
        # authored messages, exactly as fork mode seeds a fork (same funnel).
        try:
            history, _ = await _load_history_and_cut(pinned_conversation_id, None, row=pinned_row)
        except Exception as exc:
            return _fail(
                ctx,
                started_at,
                error_type="database",
                message=f"Failed to load history from conversation {pinned_conversation_id}: {exc}",
                is_retryable=True,
                exc=exc,
            )
        if history:
            await agent.run_first_turn_pass()
            # Only the instructions ride along: the authored opening turn was
            # already asked the first time and is part of the history now.
            own_messages = [
                m
                for m in agent.config.messages
                if str(getattr(getattr(m, "role", None), "value", getattr(m, "role", "")))
                in ("system", "developer")
            ]
            agent.config.messages.clear()
            agent.config.messages.extend(history)
            agent.config.messages.extend(own_messages)
            history_message_count = len(history)
            if _lineage_of(pinned_row) is not None:
                # A continued child that borrowed a history reads it again, with the same note.
                _attach_inherited_note(agent, app_ctx, agent_id)
    if history_mode != "none" and source_conversation_id:
        if not (parsed.user_input or "").strip() and host_turn is None and not list(agent.config.messages):
            # No new turn at all: the run's trigger would be the LAST BORROWED
            # history message — if that is a rebuilt (id-less, synthesized)
            # tool-pairing row it gets mis-persisted as a stray child row. A
            # collaboration call must say what the agent should DO anyway.
            return _fail(
                ctx,
                started_at,
                error_type="invalid_arguments",
                message="history_mode requires a new turn: this agent has no "
                "authored messages and no user_input was passed.",
                suggested_action="Pass user_input telling the agent what to do "
                "with the conversation's history.",
            )
        if history_mode == "fork":
            from matrx_ai._ext import get_conversation_forker

            forker = get_conversation_forker()
            if forker is None:
                return _fail(
                    ctx,
                    started_at,
                    error_type="feature_unavailable",
                    message="history_mode='fork' requires the host's conversation fork "
                    "helper, which is not configured in this environment.",
                    suggested_action="Use history_mode='snapshot' instead.",
                )
            # The fork row is written HERE, before the child runs, so the
            # conversation gate (which puts every candidate conversation in the
            # hidden lane) never stamps it: inside a mandate candidate the fork
            # itself asks for that lane, never "subagent".
            from matrx_graph.candidate import candidate_marker

            fork_type = (
                "mandate_candidate"
                if candidate_marker(app_ctx.metadata) is not None
                else ("subagent" if app_ctx.conversation_id_for_lineage else "auto")
            )
            try:
                fork_info = await forker(
                    source_conversation_id=source_conversation_id,
                    user_id=str(app_ctx.user_id),
                    organization_id=(
                        str(app_ctx.organization_id) if app_ctx.organization_id else None
                    ),
                    up_to_position=parsed.history_up_to_position,
                    parent_conversation_id=app_ctx.conversation_id_for_lineage,
                    conversation_type=fork_type,
                    title=None,
                )
                run_conversation_id = str(fork_info["conversation_id"])
            except Exception as exc:
                return _fail(
                    ctx,
                    started_at,
                    error_type="fork_failed",
                    message=f"Failed to fork conversation {source_conversation_id}: {exc}",
                    is_retryable=True,
                    exc=exc,
                )
        # Fork reads the fork it just made; a snapshot always reads its SOURCE
        # (a host-pinned child conversation is empty and is not the source).
        history_read_id = (
            run_conversation_id if history_mode == "fork" else None
        ) or source_conversation_id
        try:
            history, own_cut = await _load_history_and_cut(
                history_read_id,
                # Fork already applied the cut; re-slicing the fork would be a
                # second, off-by-N application of the same bound.
                None if history_mode == "fork" else parsed.history_up_to_position,
                row=source_row,
            )
        except Exception as exc:
            return _fail(
                ctx,
                started_at,
                error_type="database",
                message=f"Failed to load history from conversation {history_read_id}: {exc}",
                is_retryable=True,
                exc=exc,
            )
        if history_mode == "snapshot":
            history = _without_calls_in_flight(history)
        if history:
            # Prepend: [borrowed past] + [agent's own authored messages] + the
            # user_input turn run_agent appends — mirroring hydrate_persisted_history
            # ordering (persisted first, new turns after).
            # The child's first-turn pass runs BEFORE the borrowed history joins:
            # that history is data and is never filled (execute would otherwise
            # run the pass over it).
            await agent.run_first_turn_pass()
            own_messages = list(agent.config.messages)
            agent.config.messages.clear()
            agent.config.messages.extend(
                _closed_borrowed_history(
                    history, own=str(getattr(app_ctx, "agent_id", "") or "") == str(agent_id)
                )
            )
            agent.config.messages.extend(own_messages)
            history_message_count = len(history)
            # Without this the borrowed past ends on the request that started this child, right
            # beside the child's own prompt, and it reads as a fresh order (PB-08 B7: a fork forked
            # again). Staged per turn in the context channel, so no stored message changes.
            _attach_inherited_note(agent, app_ctx, agent_id)
            if history_mode == "snapshot":
                # Recorded on the child's conversation (conversation gate), so a continued child
                # and a child of this child read the same borrowed history first.
                inherited_lineage = {"conversation_id": str(history_read_id), "up_to_position": own_cut}

    # ── The child's pre-run checks run BEFORE its id goes out ───────────
    # The run below opens the child context, which announces the child's
    # conversation id on the wire (sub_agent INIT) — a conversation that is only
    # written on the child's first write. A child refused by its first-turn pass
    # (required inputs, a declared prompt block) never writes, so announcing it
    # first sent the client a phantom id it then failed to load (live
    # 2026-11-12, system_error dbda7ad6: 'DB Cartographer' without ``task``
    # announced conversation b5d123e3 that never existed). Idempotent: the
    # child's execute finds the pass already applied.
    try:
        await agent.run_first_turn_pass()
    except PromptBlockError as exc:
        info = getattr(exc, "error_info", None)
        return _fail(
            ctx,
            started_at,
            error_type=getattr(info, "error_type", None) or "prompt_block",
            message=getattr(info, "user_message", None) or str(exc),
            is_retryable=False,
            exc=exc,
        )
    except Exception as exc:
        agent_name = str(getattr(agent, "name", None) or agent_id)
        refusal = child_required_inputs_refusal(exc, agent_name)
        if refusal is not None:
            refusal_type, refusal_message, refusal_action = refusal
            return _fail(
                ctx,
                started_at,
                error_type=refusal_type,
                message=refusal_message,
                suggested_action=refusal_action,
                refusal=True,
            )
        return _fail(
            ctx,
            started_at,
            error_type="agent_execution",
            message=f"Agent '{agent_name}' failed before it started: {exc}",
            exc=exc,
        )

    # ── A child must arrive with something to answer ────────────────────
    # An agent with instructions only and no user_input would reach the send
    # boundary EMPTY (live 2026-10-16: a variables-only call to Lane Planner).
    # Refuse here, naming the argument to send — never a run with nothing in it.
    from matrx_ai.agents.child_turn import (
        EMPTY_CONVERSATION_ERROR_TYPE,
        MISSING_CHILD_INPUT_ERROR_TYPE,
        empty_child_turn_guidance,
        refuse_empty_child_turn,
        undeclared_variable_names,
    )

    refusal = (
        None
        if host_turn is not None
        else refuse_empty_child_turn(
            agent,
            user_input=parsed.user_input,
            variables=parsed.variables,
            input_arg=input_arg_name,
        )
    )
    if refusal is not None:
        refusal_message, refusal_action = refusal
        return _fail(
            ctx,
            started_at,
            error_type=MISSING_CHILD_INPUT_ERROR_TYPE,
            message=refusal_message,
            suggested_action=refusal_action,
            refusal=True,
        )

    label = f"agent_call:{getattr(agent, 'name', None) or agent_id}"[:60]

    # Carry the child depth via a task-local context rebinding, NEVER an
    # in-place bump on the shared metadata dict — concurrent sibling tool calls
    # in one batch share that dict (asyncio.gather), so the old bump/restore
    # raced siblings into false nesting and could leave the parent's depth
    # permanently inflated. Each batch call runs in its own task context, so
    # the rebinding is invisible to siblings; run_agent's fork copies the
    # bumped metadata for the child.
    from matrx_connect.context.app_context import set_app_context

    child_metadata = {**app_ctx.metadata, _AGENT_CALL_DEPTH_KEY: depth + 1}
    # Steerability belongs to ONE child, the one its host launched as such —
    # never inherited by that child's own children.
    from matrx_ai.agents.conversation_type import INHERITED_HISTORY_KEY, STEERABLE_CHILD_KEY

    child_metadata.pop(STEERABLE_CHILD_KEY, None)
    # Where THIS child's borrowed history comes from (never its parent's).
    child_metadata.pop(INHERITED_HISTORY_KEY, None)
    if inherited_lineage is not None:
        child_metadata[INHERITED_HISTORY_KEY] = inherited_lineage
    if extra_child_metadata:
        child_metadata.update(extra_child_metadata)
    # Lineage: every chat.tool_call row the child (and its own children) writes
    # names THIS call's row as its parent_call_id, so a reloaded transcript
    # nests the sub-agent's work under this card exactly as the live stream
    # did. Bound on the child's task-local context like the depth — the child's
    # own agent_call rebinds it for its child, which keeps every level honest.
    from matrx_ai.tools.logger import (
        PARENT_TOOL_CALL_ID_KEY,
        PARENT_TOOL_CALL_ROW_KEY,
        ToolExecutionLogger,
    )

    # The call that started this child, by its provider id — rides onto the
    # child's execution record so a crash recovery can find this helper again.
    if ctx.call_id:
        child_metadata[PARENT_TOOL_CALL_ID_KEY] = str(ctx.call_id)
    else:
        child_metadata.pop(PARENT_TOOL_CALL_ID_KEY, None)
    parent_row_id = ToolExecutionLogger().row_id_for_call(ctx)
    if parent_row_id:
        child_metadata[PARENT_TOOL_CALL_ROW_KEY] = parent_row_id
    else:
        vcprint(
            f"[agent_call] no chat.tool_call row is registered for call {ctx.call_id!r} "
            "— the child's tool calls will be written with NO parent_call_id and a "
            "reloaded transcript cannot nest them under this card.",
            color="yellow",
        )
    if time_budget_seconds:
        # A NEW dict every time (never an in-place append): sibling calls in one
        # batch share app_ctx.metadata, and this budget belongs to exactly one
        # of them. run_agent's fork copies it down, so the child, its tools and
        # its own children all poll the same clock.
        child_metadata = with_subtree_budget(
            child_metadata,
            seconds=int(time_budget_seconds),
            label=f"'{getattr(agent, 'name', None) or agent_id}' run",
        )
    set_app_context(app_ctx.with_overrides(metadata=child_metadata))
    try:
        require_complete_output = parsed.result_mode in ("reference", "inline_once")
        muted = parsed.result_mode == "reference" or mute_stream
        result = await runner.run_agent_as_tool(
            agent,
            who=who,
            opts=run_opts,
            label=label,
            source_feature="agent_call",
            conversation_id=run_conversation_id,
            # ONE author per turn: the host's turn, or what was typed (never both on the call).
            **(
                {"host_turn": host_turn}
                if host_turn is not None
                else {"user_input": parsed.user_input or None}
            ),
            # Reference mode: the child's tokens never reach the client — the
            # descriptor + ValueStoredEvent are the caller's signal.
            # `inline_once` is deliberately NOT muted — it is an inline mode
            # whose full output IS delivered this turn (see agent_tool.py
            # § NESTED-AGENT STREAM LEAK and
            # scripts/nested_agent_streams_baseline.json).
            # A background helper (`mute_stream`) is muted the same way: nobody
            # is reading its stream, and its answer arrives through the inbox.
            suppress_stream=muted,
            allow_client_delegation=not muted,
            require_complete_output=require_complete_output,
            max_iterations=int(max_iterations) if max_iterations else None,
        )
    finally:
        # Restore THIS task's binding (no-op for siblings; keeps the bump from
        # leaking if calls ever run sequentially in the loop task).
        set_app_context(app_ctx)

    if on_child_result is not None:
        try:
            await on_child_result(result)
        except Exception as exc:  # noqa: BLE001 — the record is not the answer
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(exc, kind="agent_call_child_result_hook", agent_id=agent_id)

    # A run a LIMIT or a stop ended (cancelled / time / cost / rounds) is reported as that, whatever
    # ``success`` says: a cancelled child is not "failed" — the caller must read the stop cause and
    # what the child had done, not a failure sentence (failure register entry 8).
    _early_bounded = bounded_marker(
        result,
        agent_label=str(getattr(agent, "name", None) or agent_id),
        time_budget_seconds=time_budget_seconds,
    )
    _stopped_by_limit = (
        _early_bounded is not None
        and (_early_bounded.get("stop_cause") or {}).get("kind") in LIMIT_STOP_KINDS
    )

    if not result.success and not _stopped_by_limit:
        # The child's own exception rides the result: hand it to ToolError so
        # the operator gets its real type, message and stack — never only this
        # sentence (2026-10-01: an OpenAI out-of-credit refusal reached the
        # tool executor as "the tool swallowed its exception").
        child_error_type = (result.metadata or {}).get("error_type")
        refusal = child_required_inputs_refusal(result.exception, str(getattr(agent, "name", None) or agent_id))
        if refusal is not None:
            # The child refused BEFORE any model call: the CALLING model left a declared
            # input empty — its to fix on the next step, never a platform failure.
            refusal_type, refusal_message, refusal_action = refusal
            return _fail(
                ctx,
                started_at,
                error_type=refusal_type,
                message=refusal_message,
                suggested_action=refusal_action,
                refusal=True,
                child_usages=list(result.usage_history or []),
            )
        from matrx_ai.providers.caller_refusal import EXPECTED_HOLD_CODES

        if child_error_type in EXPECTED_HOLD_CODES:
            # The child was HELD by a limit or approval someone set (spend approval waiting, an
            # automation guardrail, a plan's usage limit): nothing was spent, the hold has its own
            # human path, and the calling model tells the person. Its code rides as the error type so
            # the executor never files it as a tool failure (live 2026-11-14: a mandate_call held by
            # run_approval_required filed tool_execution_failed).
            return _fail(
                ctx,
                started_at,
                error_type=str(child_error_type),
                message=f"Agent '{getattr(agent, 'name', agent_id)}' is on hold ({child_error_type}): {result.error}",
                suggested_action="Tell the person the run is waiting on that hold; do not call it again until it clears.",
                refusal=True,
                child_usages=list(result.usage_history or []),
            )
        suggested_action = "Check the agent's variables and configuration."
        if child_error_type == EMPTY_CONVERSATION_ERROR_TYPE:
            # The send boundary refused an EMPTY child (nothing sent, nothing
            # spent) — e.g. its authored turn was filled with nothing. Say what
            # to send, never "check the configuration".
            _, suggested_action = empty_child_turn_guidance(
                str(getattr(agent, "name", None) or agent_id),
                input_arg=input_arg_name,
                undeclared=undeclared_variable_names(agent, parsed.variables),
            )
        return _fail(
            ctx,
            started_at,
            error_type="agent_execution",
            message=(
                f"Agent '{getattr(agent, 'name', agent_id)}' failed"
                f"{f' ({child_error_type})' if child_error_type else ''}: {result.error}"
            ),
            suggested_action=suggested_action,
            exc=result.exception,
            # The child's stack is for the operator; the calling model gets the
            # child's own plain sentence above, never a provider billing URL.
            traceback_operator_only=True,
            child_usages=list(result.usage_history or []),
        )

    # ── The child's real end state rides every answer; an unfinished one is never success. ──
    # A child that produced nothing, or ended failed/paused/truncated/suspended, is a FAILED call
    # whatever require_complete_output says (agent-tools VISION, "Research tool results": never
    # report success on work that produced nothing). Its partial answer still rides ``output``
    # beside ``child_end`` so the caller can use what it did. A child a LIMIT stopped keeps its
    # own path below: ``bounded`` names the stop and the answer is what it got to.
    child_end = child_end_state(result)
    if child_end.get("reason") and not _stopped_by_limit:
        agent_label = str(getattr(agent, "name", None) or agent_id)
        status_label = child_end["status"] if child_end["status"] != "completed" else "empty_response"
        partial = relayable_answer(result.output or "", agent)
        return _fail(
            ctx,
            started_at,
            error_type="agent_incomplete_output",
            message=(
                f"Agent '{agent_label}' did not finish its answer (status={status_label}): "
                f"{child_end['reason']}"
                + ("; no value was stored." if require_complete_output else "")
            ),
            suggested_action=(
                "Ask the agent again, or use the partial answer on the result if it is enough."
                if not child_end.get("empty")
                else "Ask the agent again; it returned nothing."
            ),
            is_retryable=True,
            child_usages=list(result.usage_history or []),
            output={
                "agent_id": agent_id,
                **({"agent_version_id": version_id} if version_id else {}),
                "agent_name": getattr(agent, "name", None) or "",
                "result": partial,
                "child_end": child_end,
                **_child_conversation_extra(result, {}),
                "model_id": result.model_id,
            },
        )

    # ── Did a budget stop it? Say so, on the result. ────────────────────
    # A bounded answer that presents itself as complete is the failure this
    # whole mechanism exists to avoid: the caller would relay a partial answer
    # as the final word. The marker is the machine-side twin of the model-side
    # instruction to end with what it did not get to — neither replaces the
    # other, because a desk can forget and a marker cannot say what is missing.
    bounded_extras: dict[str, Any] = {}
    _bounded = _early_bounded
    if _bounded is not None:
        bounded_extras["bounded"] = _bounded

    # The helper's answer, as the caller will see it — see relayable_answer.
    raw_output = result.output or ""
    result_value: Any = relayable_answer(
        raw_output,
        agent,
        stopped_on_tool_calls=list(getattr(result, "stopped_on_tool_calls", None) or []),
    )

    # ── Conversation-aware extras + remember write-back ─────────────────
    # Merged into BOTH result shapes (inline and reference) below.
    collab_extras: dict[str, Any] = {}
    if history_mode != "none" and source_conversation_id:
        agent_name = getattr(agent, "name", None) or agent_id
        child_conversation_id = str(
            (result.metadata or {}).get("conversation_id") or run_conversation_id or ""
        )
        collab_extras["history"] = {
            "mode": history_mode,
            "source_conversation_id": source_conversation_id,
            "messages_included": history_message_count,
        }
        if child_conversation_id:
            collab_extras["child_conversation_id"] = child_conversation_id
        if parsed.remember:
            # Durable write-back: the SOURCE conversation's turn-boundary inbox
            # (delivery='turn_end' — exactly-once, FIFO, drained at the original
            # agent's next final boundary, never interleaving a live run).
            note = raw_output.strip()
            if len(note) > REMEMBER_NOTE_MAX_CHARS:
                note = note[:REMEMBER_NOTE_MAX_CHARS] + "\n… [truncated]"
            note_text = (
                f"[Collaboration note] Agent '{agent_name}' reviewed this "
                f"conversation via agent_call and left this durable note:\n{note}"
            )
            try:
                from uuid import uuid4

                from matrx_ai.db import cxm

                injection_id = str(uuid4())
                await cxm.pending_injection.enqueue(
                    injection_id=injection_id,
                    conversation_id=source_conversation_id,
                    created_by=str(app_ctx.user_id),
                    kind="system_message",
                    content={"text": note_text},
                    source="agent_collab",
                    delivery="turn_end",
                    is_visible_to_user=parsed.remember_visible_to_user,
                    is_visible_to_model=True,
                    metadata={
                        # enqueued_by_request_id: claim_next_turn_end skips
                        # items the CURRENT run enqueued itself — without it a
                        # remember to the caller's own conversation would drain
                        # at this same run's final boundary (an extra paid turn
                        # re-answering output the model already holds).
                        "enqueued_by_request_id": getattr(app_ctx, "request_id", None),
                        "agent_collab": {
                            "caller_conversation_id": getattr(app_ctx, "conversation_id", None)
                            or None,
                            "child_conversation_id": child_conversation_id or None,
                            "agent_id": agent_id,
                            "call_id": ctx.call_id or None,
                        },
                    },
                )
                collab_extras["remember"] = {"status": "queued", "injection_id": injection_id}
            except Exception as exc:
                # The child already ran (paid) — don't fail the whole call, but
                # never swallow: scream + surface on the output so the model
                # knows the write-back did NOT land.
                vcprint(
                    f"[agent_call] remember write-back FAILED for conversation "
                    f"{source_conversation_id}: {exc}",
                    color="red",
                )
                collab_extras["remember"] = {"status": "failed", "error": str(exc)}

    # Reference mode: store the result via the host's value store and return
    # only the bounded descriptor (Pattern 2 — the caller routes it without
    # holding it). inline_once returns BOTH (full now, stubbed later).
    if parsed.result_mode in ("reference", "inline_once"):
        from matrx_ai._ext import get_conversation_value_writer

        writer = get_conversation_value_writer()
        if writer is not None:
            description = (parsed.result_description or "").strip()
            if not description and isinstance(result_value, dict):
                description = str(
                    result_value.get("description") or result_value.get("summary") or ""
                ).strip()[:500]
            if not description:
                description = f"Result of {getattr(agent, 'name', None) or agent_id}"
            descriptor = await writer(
                key=(parsed.result_key or "").strip() or (getattr(agent, "name", None) or agent_id),
                description=description,
                value=result_value,
                json_schema=getattr(agent, "output_schema", None)
                if isinstance(getattr(agent, "output_schema", None), dict)
                else None,
                source_agent_id=agent_id,
                source_call_id=ctx.call_id or None,
            )
            output: dict[str, Any] = {
                "agent_id": agent_id,
                **({"agent_version_id": version_id} if version_id else {}),
                "agent_name": getattr(agent, "name", None) or "",
                "stored": descriptor,
                **_child_conversation_extra(result, collab_extras),
                "model_id": result.model_id,
                "child_end": child_end,
                **bounded_extras,
                **collab_extras,
            }
            if parsed.result_mode == "inline_once":
                output["result"] = result_value
            # Media identity rides reference mode too. Storing the child's TEXT
            # and dropping its picture would leave the caller with a value-store
            # key and no way to ever see or address the image.
            ref_media = list(getattr(result, "media", None) or [])
            if ref_media:
                output["media"] = ref_media
            ref_result = ToolResult(
                success=True,
                output=output,
                provider_content=build_agent_media_content(output, ref_media),
                usage=result.usage or None,
                child_usages=list(result.usage_history or []),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="agent_call",
                call_id=ctx.call_id,
            )
            stored_key = descriptor.get("key") if isinstance(descriptor, dict) else None
            if isinstance(stored_key, str) and stored_key:
                ref_result.value_ref_key = stored_key
            if parsed.result_mode == "reference":
                ref_result.output_self_capped = True
            else:
                # inline_once: the full inline copy is consumed THIS turn; the
                # next rebuild stubs it (the stored value remains fetchable).
                ref_result.auto_stub = True
            return ref_result
        vcprint(
            "[agent_call] result_mode requested but no conversation_value_writer "
            "configured — returning the full output inline",
            color="yellow",
        )

    # A child that PRODUCED media hands back its durable identity, and the tool
    # output takes the canonical `image_ref` shape so `ToolResultContent` builds a
    # real ImageContent block (tools/models.py::_build_image_ref_blocks) which the
    # provider path resolves to bytes before the call. That is the difference
    # between the calling agent SEEING the picture and receiving a link it can
    # only parrot — the latter is what produced expiring S3 URLs in chat history.
    media_refs = list(getattr(result, "media", None) or [])
    output: dict[str, Any] = {
        "agent_id": agent_id,
        **({"agent_version_id": version_id} if version_id else {}),
        "agent_name": getattr(agent, "name", None) or "",
        "result": result_value,
        **_child_conversation_extra(result, collab_extras),
        "model_id": result.model_id,
        "child_end": child_end,
        **bounded_extras,
        **collab_extras,
    }
    if media_refs:
        output["media"] = media_refs

    # Build the model's view OURSELVES rather than borrowing the `image_ref`
    # envelope. That envelope is the screenshot shape: `_build_image_ref_blocks`
    # keeps only width/height/bytes/session/format and labels the block
    # "Screenshot captured." Routing an agent_call through it told the model a
    # false thing about an image it commissioned AND silently dropped the agent's
    # own answer, its name, the collaboration `history`, and the `remember`
    # write-back status that exists precisely so the model learns the write-back
    # FAILED. Here the images become real vision blocks (which the provider path
    # resolves to bytes before the call) and everything else stays as text.
    provider_content = build_agent_media_content(output, media_refs)

    return ToolResult(
        success=True,
        output=output,
        provider_content=provider_content,
        usage=result.usage or None,
        child_usages=list(result.usage_history or []),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="agent_call",
        call_id=ctx.call_id,
    )


def _child_conversation_extra(result: Any, collab_extras: dict[str, Any]) -> dict[str, Any]:
    """``{"child_conversation_id": …}`` — the conversation the child ran in.

    Every agent_call names it (not only collaboration calls), so the card that
    ran the child can open that conversation and a reloaded transcript can load
    the child's own thinking and tool calls beneath it. Collaboration calls
    already carry it in ``collab_extras``; never stated twice."""
    if "child_conversation_id" in collab_extras:
        return {}
    from matrx_ai.context.app_context import try_get_app_context

    app_ctx = try_get_app_context()
    if app_ctx is not None and not bool(getattr(app_ctx, "store", True)):
        # An ephemeral run stores no conversation — naming one would be a door
        # to nothing.
        return {}
    child = str((getattr(result, "metadata", None) or {}).get("conversation_id") or "")
    return {"child_conversation_id": child} if child else {}


__all__ = [
    "REACHABLE_AGENTS_SHOWN",
    "child_end_state",
    "agent_call",
    "agent_slug",
    "reachable_agents",
    "runnable",
    "unknown_agent_message",
    "unknown_agent_refusal",
]
