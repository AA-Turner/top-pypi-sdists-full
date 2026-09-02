"""Drain queued tool mutations between agent loop iterations.

Phase D-loop of TOOL_INJECTION_REFACTOR.md. A registered tool that wants
to add or remove tools from the active set calls
``ctx.queue_tool_changes(...)`` during its execution. Those mutations land
on ``AppContext.metadata['pending_tool_mutations']`` as a list. Between
iterations of the agent loop, the orchestrator calls ``drain_tool_mutations``
to:

  1. Pop the pending list off the AppContext.
  2. Apply each mutation through the same ``merge_request_tools`` primitive
     every other source uses (capabilities, request.tools, editable blocks).
  3. Emit a ``RESOURCE_CHANGED`` event so the FE knows the tool set shifted.

Registered-tool additions are recorded on ``UnifiedConfig.dynamic_tools`` so
conversation cache/DB reconstruction can restore them on later turns. Inline
definitions and agent-projection state remain request-scoped because they need
their complete typed definitions, not name-only reconstruction.

The drain is intentionally inside the ``matrx_ai.tools`` package so the
orchestrator can call it without crossing to aidream and so test paths
that don't go through the orchestrator can still exercise the primitive.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from matrx_utils import vcprint

from matrx_ai.tools.merge import (
    ToolMergeError,
    active_tool_executors,
    enforce_hard_tool_exclusions,
    merge_request_tools,
)
from matrx_ai.tools.models import _PENDING_TOOL_MUTATIONS_KEY
from matrx_ai.tools.specs import (
    AgentToolSpec,
    InlineToolSpec,
    RegisteredToolSpec,
    ToolSpec,
)

logger = logging.getLogger(__name__)


def _active_tool_names(config) -> list[str]:
    """Return the model-visible tool names in stable request order."""
    from matrx_ai.tools.merge import canonical_tool_names

    names = canonical_tool_names(config.tools)
    for custom_tool in config.custom_tools:
        if custom_tool.name not in names:
            names.append(custom_tool.name)
    return names


def _coerce_spec(raw: Any) -> ToolSpec:
    """Rehydrate a ToolSpec dict from queue_tool_changes back into a typed
    spec. The mutation API serialises specs via model_dump so they survive
    being stashed on the metadata dict; here we reverse that."""
    if hasattr(raw, "model_dump"):
        return raw  # already typed
    if not isinstance(raw, dict):
        raise ToolMergeError(f"Pending mutation contained a non-dict spec: {type(raw).__name__}")
    kind = raw.get("kind")
    if kind == "registered":
        return RegisteredToolSpec.model_validate(raw)
    if kind == "inline":
        return InlineToolSpec.model_validate(raw)
    if kind == "agent":
        # AgentToolSpec needs resolution via apply_unified_tools' resolver
        # before reaching the merge primitive. The drain doesn't have DB
        # access; let merge_request_tools surface the conflict-style error
        # so the operator sees that the tool's queue_tool_changes() call is
        # using the wrong shape for the dynamic-injection path.
        return AgentToolSpec.model_validate(raw)
    raise ToolMergeError(f"Pending mutation: unknown ToolSpec kind {kind!r}")


async def drain_tool_mutations(config, ctx):
    """Apply every queued mutation from ``ctx.metadata`` and clear the queue.

    Returns the (possibly-updated) ``AppContext`` so the caller can rebind
    and ``set_app_context()`` it. Emits a ``RESOURCE_CHANGED`` event when
    any mutation was actually applied so the FE can re-render the active
    tool set.

    Idempotent — calling it on a request with no pending mutations is a
    no-op (returns the same ctx).

    Phase D-loop note: ``AgentToolSpec`` mutations are not yet supported
    through this path (they need DB access for projection). If a tool
    queues an agent spec, ``merge_request_tools`` raises a clean
    ``ToolMergeError`` directing the developer to ``apply_unified_tools``.
    """
    if ctx is None:
        return ctx

    pending = (ctx.metadata or {}).get(_PENDING_TOOL_MUTATIONS_KEY)
    if not pending:
        return ctx

    # Establish host policy before applying removals. On a freshly rehydrated
    # request this is the transition that filters the durable authored set;
    # doing it after a self-removing discovery mutation would restore that
    # just-removed loader from authored state.
    ctx = enforce_hard_tool_exclusions(config, ctx)

    vcprint(
        f"[drain_tool_mutations] entering — {len(pending)} queued mutation(s); "
        f"config.tools={len(config.tools)}, config.custom_tools={len(config.custom_tools)} "
        f"before drain",
        color="cyan",
    )
    before_active = _active_tool_names(config)

    add_specs: list[ToolSpec] = []
    remove_names: list[str] = []
    sources: list[str] = []

    for entry in pending:
        if not isinstance(entry, dict):
            continue
        action = entry.get("action")
        by = entry.get("by") or "?"
        if action == "add":
            for raw in entry.get("specs") or []:
                add_specs.append(_coerce_spec(raw))
            sources.append(f"+by:{by}")
        elif action == "remove":
            remove_names.extend(str(n) for n in entry.get("names") or [])
            sources.append(f"-by:{by}")

    # Removal first — clear the names from config.tools / config.custom_tools
    # / ctx.client_tools so subsequent adds with the same name don't trigger
    # the merge primitive's conflict detector.
    if remove_names:
        before_tools = list(config.tools)
        before_custom = list(config.custom_tools)
        config.tools = [n for n in config.tools if n not in remove_names]
        config.custom_tools = [ct for ct in config.custom_tools if ct.name not in remove_names]
        if ctx.client_tools:
            new_client = [n for n in ctx.client_tools if n not in remove_names]
            if new_client != list(ctx.client_tools):
                ctx = ctx.with_overrides(client_tools=new_client)
        vcprint(
            f"[drain_tool_mutations] Removed {sorted(set(remove_names))} "
            f"(tools: {len(before_tools)}→{len(config.tools)}, "
            f"custom: {len(before_custom)}→{len(config.custom_tools)})",
            color="cyan",
        )

    if add_specs:
        ctx = merge_request_tools(
            config,
            ctx,
            add_specs,
            active_executors=active_tool_executors(ctx),
        )
        vcprint(
            f"[drain_tool_mutations] Added {len(add_specs)} spec(s)",
            color="cyan",
        )

    # Clear the queue regardless — pending entries are consumed.
    new_metadata = dict(ctx.metadata)
    new_metadata.pop(_PENDING_TOOL_MUTATIONS_KEY, None)
    ctx = ctx.with_overrides(metadata=new_metadata)

    # Emit RESOURCE_CHANGED so the FE can re-render the active tool set.
    # Compare final state rather than echoing queued intent: merge can dedup a
    # surface default or reject it through policy, and reporting that name as
    # "added" would make downstream stores diverge from the model's toolset.
    # Payload carries the actual tool names (not just
    # counts) so consumers like the matrx-extend extension's
    # useActiveToolsStore can reconcile their local view without a separate
    # roundtrip — see /Users/armanisadeghi/code/common-docs/systems/clients/extension/CHANNELS.md.
    after_active = _active_tool_names(config)
    before_set = set(before_active)
    after_set = set(after_active)
    added_tools = [name for name in after_active if name not in before_set]
    removed_tools = [name for name in before_active if name not in after_set]

    # Registered discovery additions are conversation state, not a one-request
    # capability side effect. Persist the delta on UnifiedConfig so
    # ConversationResolver cache hits and DB reconstruction both restore it on
    # the next turn; apply_unified_tools will still re-run hard authority and
    # executor viability against the current client before exposing anything.
    # Inline specs intentionally remain request-scoped because a name alone is
    # insufficient to reconstruct their caller-authored schema safely.
    from matrx_ai.tools.merge import canonical_tool_names

    dynamic_tools = canonical_tool_names(getattr(config, "dynamic_tools", None) or [])
    removed_set = set(canonical_tool_names(remove_names))
    if removed_set:
        dynamic_tools = [name for name in dynamic_tools if name not in removed_set]
    authored = set(canonical_tool_names(getattr(config, "authored_tools", None) or []))
    for spec in add_specs:
        if not isinstance(spec, RegisteredToolSpec):
            continue
        name = canonical_tool_names([spec.resolved_tool_id() or spec.name])[0]
        if name in after_set and name not in authored and name not in dynamic_tools:
            dynamic_tools.append(name)
    config.dynamic_tools = dynamic_tools

    if (added_tools or removed_tools) and ctx.emitter is not None:
        active_count = len(after_active)
        try:
            await ctx.emitter.send_resource_changed(
                kind="active_tools",
                action="invalidated",
                resource_id=ctx.conversation_id or ctx.request_id,
                metadata={
                    "added_tools": added_tools,
                    "removed_tools": removed_tools,
                    "active_count": active_count,
                    # Backward-compat: prior consumers read these scalar
                    # fields. Keep them so existing extension versions
                    # don't regress on upgrade.
                    "added": len(added_tools),
                    "removed": len(removed_tools),
                    "sources": sources,
                },
            )
            logger.info(
                "[stream] RESOURCE_CHANGED kind=active_tools added=%d removed=%d active_count=%d",
                len(added_tools),
                len(removed_tools),
                active_count,
            )
        except Exception as exc:
            vcprint(
                f"[drain_tool_mutations] tools_changed event failed: {exc}",
                color="yellow",
            )

    return ctx


def _row_field(row: Any, name: str, default: Any = None) -> Any:
    """Read a field off a claimed inbox row, which may be a model instance or a
    raw dict depending on the manager's update_where return shape."""
    if isinstance(row, dict):
        return row.get(name, default)
    return getattr(row, name, default)


def _content_dict(raw: Any) -> dict[str, Any]:
    """Coerce a JSONB ``content`` value to a dict. ``claim_pending`` returns raw
    asyncpg rows where jsonb comes back as a STRING (the model-read path parses
    it, RETURNING * does not), so we must handle both — otherwise ``.get`` blows
    up on the string in production."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


async def drain_pending_injections(config, ctx, *, include_turn_end: bool = False):
    """Drain the per-conversation Turn-Boundary Inbox (cx_pending_injection).

    Two delivery classes (the three-send-modes ruling — see
    docs/cx_chat/TURN_BOUNDARY_INBOX.md):

      * STEER (``delivery='next_boundary'``) — claimed at EVERY drain point
        (all of them at once, FIFO): delivered mid-run at the next pause.
      * QUEUE (``delivery='turn_end'``) — only when ``include_turn_end=True``
        (the run's FINAL boundary, when the turn is completely done), and only
        ONE per drain: each queued message gets its own answer, in order.

    Claims are atomic (pending → consumed in UPDATE … RETURNING, so concurrent
    drains can't double-deliver), each claimed row is appended as a
    ``role="user"`` message to the LIVE request so the model sees it on its
    next API call, and one ``INJECTION_CONSUMED`` event acks delivery.
    Idempotent: an empty inbox is a single indexed no-op UPDATE that
    returns nothing and mutates nothing.

    Persistence is free: the injected messages live inside ``config.messages``,
    hence inside the ``[result_start_position, result_end_position]`` window the
    existing end-of-run persistence writes — so there is NO separate write here
    and no double-write.

    DB access is via the host-injected ``cxm`` bundle, imported lazily to keep
    the matrx-ai → matrx-orm boundary clean (same pattern as the rest of the
    orchestrator's persistence calls).
    """
    if ctx is None or not getattr(ctx, "conversation_id", None):
        return ctx

    # CLIENT HOST: the Turn-Boundary Inbox lives in cx_pending_injection —
    # a server-DB table read through cxm. A host with a conversation_store
    # configured has no Postgres and no inbox producer; the read would raise
    # DBNotConfiguredError at every tool-loop turn boundary. Skip entirely —
    # drain_tool_mutations (in-memory) still runs via drain_pending.
    from matrx_ai.client_host import get_conversation_store

    if get_conversation_store() is not None:
        return ctx

    # Internal / sub-agent forks have no Turn-Boundary Inbox: no user can queue
    # a message into a child agent's scratch conversation (the producer is the
    # user-facing chat surface, never an internal fan-out). The per-turn
    # ``claim_pending`` UPDATE is therefore pure overhead — and under a
    # concurrent internal fan-out (e.g. NER entity canonicalization spawning
    # dozens of sub-agents) those repeated UPDATEs pile onto the pool and blow
    # past command_timeout (``QueryTimeoutError model='CxPendingInjection'``).
    # Skip entirely for internal agents; the inbox is a user-facing primitive.
    # conversation_type is the durable source of truth (any non-standard type is
    # internal); is_internal_agent is still honored so nothing regresses.
    from matrx_ai.agents.conversation_type import is_internal_conversation

    if is_internal_conversation(ctx):
        return ctx

    from matrx_ai.db.cx_managers import cxm

    claimed = await cxm.pending_injection.claim_pending(
        ctx.conversation_id, request_id=getattr(ctx, "request_id", None)
    )
    if include_turn_end:
        # The turn is completely done — deliver THE NEXT queued message (one
        # per turn; steers drained above ride along with it).
        claimed = claimed + await cxm.pending_injection.claim_next_turn_end(
            ctx.conversation_id, request_id=getattr(ctx, "request_id", None)
        )
    if not claimed:
        return ctx

    from matrx_connect.context.events import (
        ConsumedInjection,
        InjectionConsumedPayload,
    )

    from matrx_ai.config import TextContent, UnifiedMessage

    consumed: list[ConsumedInjection] = []
    for row in claimed:
        injection_id = str(_row_field(row, "id", ""))
        kind = _row_field(row, "kind", "user_message")
        content = _content_dict(_row_field(row, "content", {}))
        text = content.get("text", "")
        is_visible_to_user = bool(_row_field(row, "is_visible_to_user", True))

        if not text:
            # A message kind with no text carries nothing for the model; record
            # the consumption (it's already claimed) and move on. Non-message
            # kinds (tool_mutation/hint/context) are a Phase-2 producer concern
            # and are not routed here yet.
            consumed.append(
                ConsumedInjection(
                    injection_id=injection_id,
                    kind=kind,
                    is_visible_to_user=is_visible_to_user,
                )
            )
            continue

        # role="user" — a queued user turn OR a system steer delivered as a user
        # message (the way tool results are delivered as a tool turn). The
        # Anthropic translator merges this with a preceding tool-result turn so
        # role alternation stays valid.
        # A hidden injection (is_visible_to_user=false — steering notes,
        # agent_collab write-backs) must stay hidden on the DURABLE row too:
        # persistence lifts metadata["is_visible_to_user"] into the typed
        # column (PROMOTED_MESSAGE_COLUMNS); without the stamp the delivered
        # message persisted as a visible user-authored bubble.
        _msg_metadata = {"is_visible_to_user": False} if not is_visible_to_user else None
        config.messages.append(
            UnifiedMessage(
                role="user",
                content=[TextContent(text=text)],
                metadata=_msg_metadata or {},
            )
        )
        # Echo the text + visibility on the event so a client that didn't
        # originate the queue (reopened panel, other device) can render the
        # delivered bubble without its own local record.
        consumed.append(
            ConsumedInjection(
                injection_id=injection_id,
                kind=kind,
                text=text,
                is_visible_to_user=is_visible_to_user,
                position=len(config.messages) - 1,
            )
        )

    vcprint(
        f"[drain_pending_injections] conv={ctx.conversation_id} drained {len(consumed)} item(s)",
        color="cyan",
    )

    if ctx.emitter is not None:
        try:
            await ctx.emitter.send_injection_consumed(
                InjectionConsumedPayload(
                    conversation_id=str(ctx.conversation_id),
                    items=consumed,
                    count=len(consumed),
                )
            )
        except Exception as exc:
            vcprint(
                f"[drain_pending_injections] injection_consumed event failed: {exc}",
                color="yellow",
            )

    return ctx


async def host_iteration_refresh(config, ctx):
    """Invoke the host-injected per-iteration tool refresh (``_ext``
    ``iteration_tool_refresh``), best-effort.

    First consumer: mid-run Orchestra roster injection (ruling D-37) — the
    host re-reads a supervisor Orchestra's membership and reconciles the
    active member tools so a member added to a RUNNING Orchestra is callable
    on this very iteration (and a removed member's tool is filtered at this
    same safe pre-API-call point). The HOST gates itself so plain agent runs
    pay zero extra reads; here we only guarantee placement and that a refresh
    failure logs loudly and never kills the run."""
    if ctx is None:
        return ctx
    from matrx_ai._ext import get_iteration_tool_refresh

    refresh = get_iteration_tool_refresh()
    if refresh is None:
        return ctx
    try:
        new_ctx = await refresh(config, ctx)
    except Exception as exc:  # noqa: BLE001 — best-effort seam, never fatal
        vcprint(
            f"[host_iteration_refresh] host tool refresh FAILED (run continues "
            f"with the previous toolset): {type(exc).__name__}: {exc}",
            color="red",
        )
        logger.warning("host iteration tool refresh failed", exc_info=True)
        return ctx
    return new_ctx if new_ctx is not None else ctx


async def drain_pending(config, ctx):
    """Umbrella turn-boundary drain: in-memory tool mutations first, then the
    DB-backed inbox, then the host's iteration tool refresh. Three producers
    with different sources and idempotency models, unified at one call site so
    the orchestrator has a single drain point per iteration."""
    ctx = await drain_tool_mutations(config, ctx)
    ctx = await drain_pending_injections(config, ctx)
    ctx = await host_iteration_refresh(config, ctx)
    return ctx
