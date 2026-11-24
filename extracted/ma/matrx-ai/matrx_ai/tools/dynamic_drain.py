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
    # Which tool queued each addition — a bundle's members inherit their lister's
    # source class (a compute target's bundle stays tied to that target).
    added_by: dict[int, str] = {}
    remove_names: list[str] = []
    sources: list[str] = []

    for entry in pending:
        if not isinstance(entry, dict):
            continue
        action = entry.get("action")
        by = entry.get("by") or "?"
        if action == "add":
            for raw in entry.get("specs") or []:
                spec = _coerce_spec(raw)
                added_by[id(spec)] = str(by)
                add_specs.append(spec)
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
        # The provider still sees these declarations (the tools array never
        # shrinks mid-conversation, declaration_ledger.py); record why, so a call
        # to one is refused with a reason instead of a generic one.
        from matrx_ai.tools.declaration_ledger import note_unavailable

        removers = sorted({str(e.get("by") or "?") for e in pending
                           if isinstance(e, dict) and e.get("action") == "remove"})
        note_unavailable(
            remove_names,
            f"it was unloaded mid-conversation by {', '.join(removers)}",
            conversation_id=getattr(ctx, "conversation_id", None),
        )
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
        # Catalog Tools injected mid-run are resolved and pinned to this request
        # before the sync merge reads the registry (CONTRACT §4).
        from matrx_ai.tools.catalog_seam import resolve_lazy_tools
        from matrx_ai.tools.specs import RegisteredToolSpec

        await resolve_lazy_tools(
            [
                key
                for spec in add_specs
                if isinstance(spec, RegisteredToolSpec)
                for key in (spec.tool_id, spec.name)
                if key
            ],
            ctx=ctx,
        )
        ctx = merge_request_tools(
            config,
            ctx,
            add_specs,
            # In-loop additions requested by a tool the run already holds (TOOL-SOURCES
            # injectors table: dynamic_drain); bundle members are also tagged sticky below.
            source="in_loop",
            # The agent's forbidden list holds mid-run too (TOOL-SOURCES.md rule U): a bundle,
            # find_tools or load_tools never brings back a tool the agent forbids. A tool the
            # person picked (user.add beats the list) is already on config.tools, so this only
            # stops NEW additions.
            excluded=list(getattr(config, "agent_excluded_tools", None) or ()),
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
    # capability side effect: they join the conversation's STICKY toolset
    # (TOOL-SOURCES.md) so ConversationResolver cache hits and DB reconstruction
    # both restore them on every later turn; apply_unified_tools still re-runs
    # hard authority and executor viability against the current client before
    # exposing anything. A queued removal is an explicit removal and forgets.
    # Inline specs intentionally remain request-scoped because a name alone is
    # insufficient to reconstruct their caller-authored schema safely.
    from matrx_ai.tools.merge import (
        STICKY_SOURCE_AGENT_BUNDLE,
        STICKY_SOURCE_BUNDLE,
        STICKY_SOURCE_COMPUTE_TARGET,
        agent_owned_listers,
        canonical_tool_names,
        forget_conversation_tools,
        record_conversation_tools,
        sticky_tool_source,
    )

    if remove_names:
        forget_conversation_tools(config, remove_names)
    for spec in add_specs:
        if not isinstance(spec, RegisteredToolSpec):
            continue
        name = canonical_tool_names([spec.resolved_tool_id() or spec.name])[0]
        if name not in after_set:
            continue
        by = added_by.get(id(spec), "")
        # A member inherits its lister's standing: a compute target's bundle stays tied to
        # the target, an agent-owned bundle to the agent; any other opened bundle is the
        # conversation's own (``bundle``).
        lister_source = sticky_tool_source(config, by) if by else STICKY_SOURCE_BUNDLE
        if by and by in agent_owned_listers(config):
            source = f"{STICKY_SOURCE_AGENT_BUNDLE}{by}"
        elif lister_source.startswith(STICKY_SOURCE_COMPUTE_TARGET):
            source = lister_source
        else:
            source = STICKY_SOURCE_BUNDLE
        record_conversation_tools(config, [name], source)

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
    from matrx_ai.agents.conversation_type import (
        STEERABLE_CHILD_KEY,
        is_internal_conversation,
    )

    # The one exception: a child its host launched as steerable (a background
    # helper a parent may message while it works) drains its own inbox.
    steerable = bool((getattr(ctx, "metadata", None) or {}).get(STEERABLE_CHILD_KEY))
    if is_internal_conversation(ctx) and not steerable:
        return ctx

    # ONLY THE RUN THAT PERSISTS MAY TAKE FROM THE INBOX. Delivery is "free"
    # only because the claimed row rides config.messages into this run's
    # end-of-run persistence (see the docstring). A store=False run — a held
    # code call (the conversation labeler via run_held_call), a strict-JSON
    # funnel call — nests inside the chat request's AppContext and inherits its
    # conversation_id, so without this it claims the person's queued message
    # into a throwaway config that is never written: consumed, no row, no
    # answer (PB-05 W-40, conversation 9004fe9b…, 2026-10-01). The row stays
    # pending for the persisting run's own boundary.
    if not getattr(ctx, "store", True):
        return ctx

    from matrx_ai.db.cx_managers import cxm

    claimed = await cxm.pending_injection.claim_pending(
        ctx.conversation_id, request_id=getattr(ctx, "request_id", None)
    )
    # REPORTS DO NOT WAIT FOR THE RUN TO END (Arman, 2026-10-28). A helper's report, agent mail,
    # a background run's end or a due wake-up reaches the running agent at its next boundary —
    # mid-loop, and at the start of a person's new turn — never only at the final boundary.
    claimed = claimed + await cxm.pending_injection.claim_reports_now(
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

    from matrx_ai.config import (
        TextContent,
        UnifiedMessage,
        host_authored_user_turn,
    )

    consumed: list[ConsumedInjection] = []
    host_batch: list[tuple[str, str, str, str, Any, bool]] = []

    def _flush_host_batch() -> None:
        if not host_batch:
            return
        _delivered = host_authored_user_turn(
            "\n\n".join(item[2] for item in host_batch), reason=f"injection:{host_batch[0][1]}"
        )
        _sources = [item[3] for item in host_batch if item[3]]
        if _sources:
            _delivered.metadata["injection_source"] = _sources[0]
        # neutral queue-item keys (never mark a person's words as the host's); the stamps are the
        # ones the woken turn writes (inbox_driver.host_turn_stamps), so a chat draws both alike.
        _delivered.metadata["injection_id"] = host_batch[0][0]
        _delivered.metadata["inbox_injection_ids"] = [item[0] for item in host_batch]
        _queued = [str(item[4]) for item in host_batch if item[4]]
        if _queued:
            _delivered.metadata["enqueued_by_request_id"] = _queued[0]
        config.messages.append(_delivered)
        for _id, _kind, _text, _src, _by, _vis in host_batch:
            consumed.append(
                ConsumedInjection(
                    injection_id=_id,
                    kind=_kind,
                    text=_text,
                    is_visible_to_user=False,
                    position=len(config.messages) - 1,
                )
            )
        host_batch.clear()

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
        # A host note (scheduled wake, deferred-tool result, background-run result, steer,
        # agent_collab write-back, session-offer note) persists flagged as the host's —
        # ``metadata.authored_by = "host"`` with ``authored_reason`` and ``injection_source`` —
        # so the chat labels it instead of quoting it as the person. It carries
        # ``is_visible_to_user=False`` (host_authored_user_turn: a server message is never
        # listed as a message, Arman 2026-11-01); the model still reads it.
        source = str(_row_field(row, "source", "") or "")
        # 🚨 AUTHORSHIP IS STAMPED BY THE WRITER — no reader can infer it. Both
        # halves of this branch land as role="user"; only this code knows which
        # one a person actually typed. A queued user_message IS her words, so
        # `user_content` carries them; a steer or a write-back is host-authored,
        # so `user_content` is stamped EMPTY rather than left NULL (NULL means
        # "a row predating this contract", which makes every correct reader fall
        # back to `content` and quote the machine at her — matrx-frontend D327).
        persons = kind == "user_message" and is_visible_to_user
        _row_metadata = _row_field(row, "metadata", None)
        _queued_by = (
            _row_metadata.get("enqueued_by_request_id") if isinstance(_row_metadata, dict) else None
        )
        if not persons:
            # ONE SHAPE FOR HOST NOTES (C135, PB-08 k=30): every host note a drain takes lands as ONE
            # stored host message — the shape the woken turn (inbox_driver) already writes — never one
            # message per row. Which path delivered a report (this boundary, or a woken turn) used to
            # decide whether two helper reports were one message or two.
            host_batch.append((injection_id, kind, text, source, _queued_by, is_visible_to_user))
            continue
        _flush_host_batch()
        _delivered = UnifiedMessage(
            role="user",
            content=[TextContent(text=text)],
            user_content=[TextContent(text=text)],
            metadata={},
        )
        # THE STORED ROW NAMES ITS QUEUE ITEM (2026-11-05, conversation 6c9efe35...): a queued second send
        # read as the server writing one message twice, because the row said nothing of where it came
        # from. Neutral keys only — they never mark a person's words as the host's.
        _delivered.metadata["injection_id"] = injection_id
        if _queued_by:
            _delivered.metadata["enqueued_by_request_id"] = str(_queued_by)
        config.messages.append(_delivered)
        # Echo the text + is_visible_to_user on the event so a client that didn't
        # originate the queue (reopened panel, other device) can render the
        # delivered bubble without its own local record.
        consumed.append(
            ConsumedInjection(
                injection_id=injection_id,
                kind=kind,
                text=text,
                is_visible_to_user=True,
                position=len(config.messages) - 1,
            )
        )
    _flush_host_batch()

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


#: How often the hold re-checks THIS process's registry (resume / Stop landed here). Not a limit:
#: the cross-task timings (max hold, durable poll) are knobs, ``matrx_ai.db.turn_control``.
_PAUSE_POLL_S = 0.25


async def _spine_stop_while_held() -> str | None:
    """The durable cross-task Stop (and tree budget / deadline) — the same host check the loop polls at
    every iteration (``_ext.get_spine_control_check``). A Stop that reached ANOTHER server task lives
    only there. None to keep holding; never raises."""
    try:
        from matrx_ai._ext import get_spine_control_check

        check = get_spine_control_check()
        return None if check is None else await check()
    except Exception as exc:  # noqa: BLE001 - announced; a blip never ends a hold as a fake stop
        from matrx_utils import vcprint

        vcprint(f"[turn-control] the durable stop check failed while held (still held): {exc}", color="yellow")
        return None


async def apply_turn_controls(ctx) -> None:
    """Apply the durable pause / resume items addressed to this run (Turn-Boundary Inbox, kind
    ``turn_control``) to the in-process request tree. Delivery rides the DB, so it reaches the turn
    whichever server task runs it. Never raises: a control that cannot be read is announced in the
    log and the turn simply continues unpaused (a pause is never faked)."""
    request_id = getattr(ctx, "request_id", None)
    conversation_id = getattr(ctx, "conversation_id", None)
    if not request_id or not conversation_id or not getattr(ctx, "store", True):
        return
    try:
        from matrx_connect.request_controls import RequestControlRegistry

        from matrx_ai.agents.conversation_type import STEERABLE_CHILD_KEY, is_internal_conversation
        from matrx_ai.client_host import get_conversation_store

        if get_conversation_store() is not None:
            return
        if is_internal_conversation(ctx) and not (getattr(ctx, "metadata", None) or {}).get(STEERABLE_CHILD_KEY):
            return
        from matrx_ai.db.cx_managers import cxm

        registry = RequestControlRegistry.get_instance()
        mine = {str(request_id), str(registry.root_of(request_id))}
        for row in await cxm.pending_injection.claim_turn_controls(
            str(conversation_id), request_ids=mine, request_id=str(request_id)
        ):
            op = str(_content_dict(_row_field(row, "content", {})).get("op") or "")
            if op == "pause":
                registry.pause(request_id)
            elif op == "resume":
                registry.resume(request_id)
    except Exception as exc:  # noqa: BLE001 - announced, never silent; the turn must not die on a control read
        from matrx_utils import vcprint

        vcprint(f"[turn-control] could not read the durable pause/resume items: {exc}", color="yellow")


async def hold_while_paused(ctx) -> None:
    """Hold the running turn while its request tree is paused (``RequestControlRegistry.pause``).

    A pause or resume sent to ANOTHER server task arrives as a durable inbox control item
    (``apply_turn_controls``), read here at the boundary and while held. A Stop sent to another task
    is the durable spine stamp, polled here on the same beat: it marks this process's registry
    cancelled, so the loop's own cancel checks stop the turn at once. Ends on resume, on a stop, or
    after ``agents.turn_control.pause_max_hold_seconds`` (announced). Emits ``info`` ``turn_paused``
    / ``turn_resumed`` so the person sees the hold is real. Never raises.
    """
    import asyncio
    import time

    from matrx_connect.request_controls import RequestControlRegistry

    from matrx_ai.db.turn_control import control_poll_seconds, pause_max_hold_seconds

    request_id = getattr(ctx, "request_id", None)
    if not request_id:
        return
    registry = RequestControlRegistry.get_instance()
    await apply_turn_controls(ctx)
    if not registry.is_paused(request_id):
        return
    emitter = getattr(ctx, "emitter", None)
    from matrx_connect.context.events import InfoPayload

    async def _say(code: str, message: str) -> None:
        if emitter is None:
            return
        try:
            await emitter.send_info(InfoPayload(code=code, system_message=message, user_message=message, metadata={"request_id": request_id}))
        except Exception:  # noqa: BLE001 - the hold is real whether or not the note lands
            return

    await _say("turn_paused", "Paused at the next step. Resume to continue.")
    max_hold = pause_max_hold_seconds()
    poll_every = control_poll_seconds()
    started = time.monotonic()
    reason = "resumed"
    last_poll = started
    while registry.is_paused(request_id):
        if time.monotonic() - last_poll >= poll_every:
            last_poll = time.monotonic()
            if await _spine_stop_while_held():
                await registry.cancel(request_id)
            else:
                await apply_turn_controls(ctx)
                if not registry.is_paused(request_id):
                    break
        if registry.is_cancelled(request_id):
            reason = "stopped"
            break
        if time.monotonic() - started > max_hold:
            registry.resume(request_id)
            reason = "timed_out"
            break
        await asyncio.sleep(_PAUSE_POLL_S)
    if reason == "stopped":
        registry.resume(request_id)
    elif reason == "resumed":
        await _say("turn_resumed", "Resumed.")
    elif reason == "timed_out":
        await _say("turn_resumed", "Paused too long, so it continued on its own.")


async def drain_pending(config, ctx):
    """Umbrella turn-boundary drain: in-memory tool mutations first, then the
    DB-backed inbox, then the host's iteration tool refresh. Three producers
    with different sources and idempotency models, unified at one call site so
    the orchestrator has a single drain point per iteration."""
    # A paused turn holds HERE — the turn boundary — before anything is drained, so a
    # steer or a person's edits sent while it waited reach this very next call.
    await hold_while_paused(ctx)
    ctx = await drain_tool_mutations(config, ctx)
    ctx = await drain_pending_injections(config, ctx)
    ctx = await host_iteration_refresh(config, ctx)
    return ctx
