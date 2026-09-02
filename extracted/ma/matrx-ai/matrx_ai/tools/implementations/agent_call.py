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

import time
from typing import Any

from matrx_utils import vcprint

from matrx_ai.tools.models import (
    AGENT_DEPTH_METADATA_KEY,
    ToolContext,
    ToolError,
    ToolResult,
    build_agent_media_content,
)

# Hard ceiling on nested agent_call depth. A CAPS constant (not an env var) per
# the repo's config doctrine: changing it is a code push, and a missing value
# can never silently disable the guard. depth 0 = the top-level request's agent;
# each nested agent_call increments it. 3 lets an agent call an agent that calls
# an agent, then stops — enough for real composition, short of a runaway loop.
MAX_AGENT_CALL_DEPTH = 3

# Key under AppContext.metadata carrying the current nesting depth. Canonical
# constant lives in tools/models.py — the SAME key feeds the ToolType.AGENT
# max_recursion_depth guardrail (the orchestrator reads it into every
# ToolContext), so both nesting guards see one truth. The bump lands on the
# parent metadata BEFORE the fork copies it, making the guard real across the
# run_agent boundary.
_AGENT_CALL_DEPTH_KEY = AGENT_DEPTH_METADATA_KEY

# Hard cap on the text a `remember=True` write-back enqueues into the source
# conversation's inbox. The note becomes a future model turn there — an
# unbounded child answer would be re-sent to the provider on every later loop
# iteration of the ORIGINAL conversation (the exact cost class the tool-result
# size gate exists for). CAPS constant per the config doctrine.
REMEMBER_NOTE_MAX_CHARS = 20_000


def _fail(
    ctx: ToolContext,
    started_at: float,
    *,
    error_type: str,
    message: str,
    suggested_action: str | None = None,
    is_retryable: bool = False,
    exc: BaseException | None = None,
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
    return ToolResult(
        success=False,
        error=error,
        started_at=started_at,
        completed_at=time.time(),
        tool_name="agent_call",
        call_id=ctx.call_id,
    )


async def _can_access(row: Any, app_ctx: Any) -> bool:
    """Admin, owner (created_by), or canonical viewer-level access.

    Viewer access IS the run gate (Arman's 2026-08-12 ruling replacing the
    dropped ``is_public`` flag): builtins, org grants, and shares all resolve
    through ``iam.has_access_for`` — never re-implement that ladder here.
    """
    if getattr(app_ctx, "is_admin", False):
        return True
    user_id = getattr(app_ctx, "user_id", None)
    if not user_id:
        return False
    if str(getattr(row, "created_by", "") or "") == str(user_id):
        return True
    from matrx_ai.db.agx_manager import agent_viewer_access

    return await agent_viewer_access(str(row.id), str(user_id))


async def _load_owned_conversation(conversation_id: str, user_id: str) -> Any | None:
    """Owner-only conversation gate, mirroring the /inbox route's check.

    Returns the live row, or None for a miss / not-owned / soft-deleted row —
    404 semantics belong to the caller: all three are the same answer, so
    another user's conversation existence never leaks. Org/shared conversation
    access is the same deliberate v1 gap as agent visibility above.
    """
    from matrx_ai.db import cxm

    rows = await cxm.conversation.filter_items(id=conversation_id, created_by=str(user_id))
    live = [r for r in rows if getattr(r, "deleted_at", None) is None]
    return live[0] if live else None


async def _load_history_messages(
    conversation_id: str, up_to_position: int | None
) -> list[Any]:
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


async def agent_call(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Run a saved agent by id and return its result. See module docstring."""
    started_at = time.time()

    # Validate the declared arg contract (also makes the tool "verified" against
    # the DB row — the drift gate checks the model name appears in this source).
    from matrx_ai.tools._generated_declarations import AgentCallArgs

    parsed = AgentCallArgs(**args)
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
        from matrx_ai.db.agx_manager import AgxDefinition
    except Exception as exc:
        return _fail(
            ctx,
            started_at,
            error_type="feature_unavailable",
            message=f"Agent runtime is not available in this environment: {exc}",
            exc=exc,
        )

    try:
        row = await AgxDefinition.load_by_id_or_none(agent_id)
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
        return _fail(
            ctx,
            started_at,
            error_type="not_found",
            message=f"No agent found with id {agent_id}.",
            suggested_action="Verify the agent_id. Use an agent you own or one that is public.",
        )

    if not await _can_access(row, app_ctx):
        return _fail(
            ctx,
            started_at,
            error_type="not_allowed",
            message=f"You do not have access to agent {agent_id}.",
            suggested_action="Use an agent you own or a public agent.",
        )

    if getattr(row, "is_active", True) is False or getattr(row, "is_archived", False):
        return _fail(
            ctx,
            started_at,
            error_type="agent_unavailable",
            message=f"Agent {agent_id} is inactive or archived and cannot be run.",
        )

    # ── Settings override → LLMParams ───────────────────────────────────
    config_overrides = None
    if parsed.settings:
        from pydantic import ValidationError

        from matrx_ai.config.llm_params import LLMParams

        try:
            config_overrides = LLMParams(**parsed.settings)
        except ValidationError as exc:
            return _fail(
                ctx,
                started_at,
                error_type="invalid_arguments",
                message=f"Invalid settings override: {exc}",
                suggested_action="settings accepts LLM params like model, temperature, "
                "max_output_tokens, reasoning_effort, top_p.",
                exc=exc,
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
        source_conversation_id = (
            parsed.history_conversation_id or ""
        ).strip() or (getattr(app_ctx, "conversation_id", None) or "")
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
            source_row = await _load_owned_conversation(
                source_conversation_id, str(app_ctx.user_id)
            )
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
                message=f"No conversation found with id {source_conversation_id}.",
                suggested_action="Use a conversation you own. Ephemeral (store=false) "
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

    # ── Recursion guard ─────────────────────────────────────────────────
    try:
        depth = int(app_ctx.metadata.get(_AGENT_CALL_DEPTH_KEY, 0))
    except (TypeError, ValueError):
        depth = 0
    if depth >= MAX_AGENT_CALL_DEPTH:
        return _fail(
            ctx,
            started_at,
            error_type="recursion_limit",
            message=f"agent_call nesting limit reached (depth {depth} ≥ "
            f"{MAX_AGENT_CALL_DEPTH}). Refusing to run another nested agent.",
            suggested_action="Flatten the agent composition or do the remaining work directly.",
        )

    # ── Load + run the target agent ─────────────────────────────────────
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import run_agent

    try:
        agent = await Agent.from_agent(
            agent_id,
            variables=parsed.variables or None,
            config_overrides=config_overrides,
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
    run_conversation_id: str | None = None
    history_message_count = 0
    if history_mode != "none" and source_conversation_id:
        if not (parsed.user_input or "").strip() and not list(agent.config.messages):
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
            try:
                fork_info = await forker(
                    source_conversation_id=source_conversation_id,
                    user_id=str(app_ctx.user_id),
                    up_to_position=parsed.history_up_to_position,
                    parent_conversation_id=getattr(app_ctx, "conversation_id", None) or None,
                    conversation_type="subagent",
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
        history_read_id = run_conversation_id or source_conversation_id
        try:
            history = await _load_history_messages(
                history_read_id,
                # Fork already applied the cut; re-slicing the fork would be a
                # second, off-by-N application of the same bound.
                None if history_mode == "fork" else parsed.history_up_to_position,
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
        if history:
            # Prepend: [borrowed past] + [agent's own authored messages] + the
            # user_input turn run_agent appends — mirroring hydrate_persisted_history
            # ordering (persisted first, new turns after).
            own_messages = list(agent.config.messages)
            agent.config.messages.clear()
            agent.config.messages.extend(history)
            agent.config.messages.extend(own_messages)
            history_message_count = len(history)

    label = f"agent_call:{getattr(agent, 'name', None) or agent_id}"[:60]

    # Carry the child depth via a task-local context rebinding, NEVER an
    # in-place bump on the shared metadata dict — concurrent sibling tool calls
    # in one batch share that dict (asyncio.gather), so the old bump/restore
    # raced siblings into false nesting and could leave the parent's depth
    # permanently inflated. Each batch call runs in its own task context, so
    # the rebinding is invisible to siblings; run_agent's fork copies the
    # bumped metadata for the child.
    from matrx_connect.context.app_context import set_app_context

    set_app_context(
        app_ctx.with_overrides(
            metadata={**app_ctx.metadata, _AGENT_CALL_DEPTH_KEY: depth + 1}
        )
    )
    try:
        require_complete_output = parsed.result_mode in ("reference", "inline_once")
        result = await run_agent(
            agent,
            label=label,
            source_feature="agent_call",
            conversation_id=run_conversation_id,
            user_input=parsed.user_input or None,
            # Reference mode: the child's tokens never reach the client — the
            # descriptor + ValueStoredEvent are the caller's signal.
            suppress_stream=parsed.result_mode == "reference",
            allow_client_delegation=parsed.result_mode != "reference",
            require_complete_output=require_complete_output,
        )
    finally:
        # Restore THIS task's binding (no-op for siblings; keeps the bump from
        # leaking if calls ever run sequentially in the loop task).
        set_app_context(app_ctx)

    if not result.success:
        return _fail(
            ctx,
            started_at,
            error_type="agent_execution",
            message=f"Agent '{getattr(agent, 'name', agent_id)}' failed: {result.error}",
            suggested_action="Check the agent's variables and configuration.",
        )

    if require_complete_output:
        child_status = str((result.metadata or {}).get("status") or "")
        incomplete_status = (
            child_status
            if child_status in {"failed", "paused", "truncated"}
            or child_status.startswith("suspended")
            else ""
        )
        empty_output = not (result.output or "").strip()
        if incomplete_status or empty_output:
            status_label = incomplete_status or "empty_response"
            return _fail(
                ctx,
                started_at,
                error_type="agent_incomplete_output",
                message=(
                    f"Agent '{getattr(agent, 'name', agent_id)}' did not produce a "
                    f"complete storable result (status={status_label}); no value was stored."
                ),
                suggested_action="Retry the child agent or use inline mode for partial output.",
                is_retryable=True,
            )

    # Surface structured output natively when the agent declares a schema (and
    # the text parses) — keeps the model from receiving stringified JSON and
    # satisfies the ToolResult.output contract gate. Uses the one JSON funnel.
    from matrx_ai.agents.output import parse_agent_output

    raw_output = result.output or ""
    extraction = parse_agent_output(raw_output, agent)
    if extraction.success and isinstance(extraction.data, dict | list):
        result_value: Any = extraction.data
    else:
        result_value = raw_output

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
                key=(parsed.result_key or "").strip()
                or (getattr(agent, "name", None) or agent_id),
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
                "agent_name": getattr(agent, "name", None) or "",
                "stored": descriptor,
                "model_id": result.model_id,
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
        "agent_name": getattr(agent, "name", None) or "",
        "result": result_value,
        "model_id": result.model_id,
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



__all__ = ["agent_call"]
