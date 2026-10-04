"""
Pre-execution resolver and tool injector for structured input content blocks.

Called by the executor immediately before every API call.  Walks the last
user message, finds any unresolved structured input blocks, and calls each
block's own resolve() method.  Each block is fully responsible for its own
fetch logic — this file is a pure dispatcher.

Also handles editable tool injection: if any block has editable=True, the
corresponding tools are added to config.tools before the model is called.
The mutation routes through ``merge_request_tools`` (see
``matrx_ai.tools.merge``) — the single write path that every tool source
shares (request envelope, capability registry, dynamic mid-loop drain).

Design principles:
- Each structured input class owns its resolve() method in structured_input_config.py.
- Each class declares _editable_tools — the tool names it needs when editable=True.
- This module only orchestrates: find blocks, run them concurrently, handle errors.
- Errors on non-optional blocks propagate so the executor can surface them.
- Runs concurrently across all blocks in the message using asyncio.gather().
- After resolution, any blocks with recorded failures notify the emitter so
  the client can display a warning (e.g. "page could not be loaded").
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from matrx_utils import vcprint

from matrx_ai.config.structured_input_config import _StructuredInputBase

if TYPE_CHECKING:
    from matrx_ai.config.message_config import MessageList
    from matrx_ai.config.unified_config import UnifiedConfig


async def _resolve_one(block: _StructuredInputBase) -> None:
    """Call block.resolve(), handling optional_context suppression."""
    try:
        await block.resolve()
    except NotImplementedError:
        vcprint(
            f"[StructuredInputResolver] No resolver for type {block.type!r} — skipping",
            color="yellow",
        )
    except Exception as exc:
        if block.optional_context:
            vcprint(
                f"[StructuredInputResolver] Optional block {block.type!r} failed, dropping: {exc}",
                color="yellow",
            )
        else:
            raise


def _emit_block_warnings(block: _StructuredInputBase) -> None:
    """
    If a resolved block recorded failures in metadata, fire a structured
    warning event to the client via the execution context emitter.

    Two uniform failure surfaces are read:
      - metadata["scrape_failures"]   = [{url, reason}, ...]   (webpage inputs)
      - metadata["resource_failures"] = [{ref, reason}, ...]   (notes, tasks, …)

    Both coerce cleanly into StructuredInputFailure (url / ref / reason).
    """
    failures: list[dict] = [
        *block.metadata.get("scrape_failures", []),
        *block.metadata.get("resource_failures", []),
    ]
    if not failures:
        return

    try:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        if ctx is None:
            return
        emitter = ctx.emitter
    except Exception:
        return

    import asyncio as _asyncio

    async def _send() -> None:
        from matrx_connect.context.data_types import StructuredInputWarningData

        await emitter.send_data(
            StructuredInputWarningData(
                block_type=block.type,
                failures=failures,
            )
        )

    try:
        loop = _asyncio.get_event_loop()
        if loop.is_running():
            from matrx_utils import detached_task

            detached_task(_send(), name=f"structured_input_warning:{block.type}")
    except Exception as exc:
        vcprint(f"[StructuredInputResolver] Warning emit failed: {exc}", color="yellow")


def inject_editable_tools(messages: MessageList, config: UnifiedConfig) -> None:
    """Inject the management tools for structured input blocks that want them.

    The set per block is decided by ``block.editable_tools()``:
      - editable=True (explicit)         -> the full CRUD set for the type;
      - editable=False (explicit)        -> nothing (read-only; enforced
        separately by the read-only id registry — see
        ``collect_read_only_resource_ids``);
      - editable unspecified (None)      -> nothing. The agent's own tools, if
        any, are left untouched — we neither add nor remove.

    An explicit editable=True wins over an agent's exclusions: this path does NOT
    pass the agent's ``excluded`` set to ``merge_request_tools``, so a per-
    attachment user signal re-adds a tool a general agent default removed.

    Walks ALL messages (not just the last) so blocks from prior turns keep their
    tools available throughout the conversation. Idempotent — safe to call on
    every iteration.

    Routes through ``merge_request_tools`` (TOOL_INJECTION_REFACTOR.md phase A2)
    so all mutations to ``config.tools`` go through the single write path that
    enforces dedup + conflict detection.
    """
    from matrx_connect.context.app_context import (
        set_app_context,
        try_get_app_context,
    )

    from matrx_ai.config.enums import Role
    from matrx_ai.tools.merge import active_tool_executors, merge_request_tools
    from matrx_ai.tools.specs import RegisteredToolSpec

    needed: set[str] = set()
    for message in messages:
        if message.role != Role.USER:
            continue
        for item in message.content:
            if isinstance(item, _StructuredInputBase):
                needed.update(item.editable_tools())

    if not needed:
        return

    specs = [RegisteredToolSpec(name=n) for n in sorted(needed)]
    ctx = try_get_app_context()
    if ctx is None:
        # Defensive fallback — production paths always have ctx set by the
        # streaming infrastructure. Keeps this helper usable in raw test code
        # without a contextvar.
        existing = set(config.tools)
        to_add = sorted(needed - existing)
        if to_add:
            vcprint(
                f"[StructuredInputResolver] Injecting editable tools (no ctx): {to_add}",
                color="cyan",
            )
            config.tools = list(config.tools) + to_add
        return

    pre_existing = set(config.tools)
    new_ctx = merge_request_tools(
        config,
        ctx,
        specs,
        active_executors=active_tool_executors(ctx),
    )
    if new_ctx is not ctx:
        set_app_context(new_ctx)
    actually_added = sorted(needed - pre_existing)
    if actually_added:
        vcprint(
            f"[StructuredInputResolver] Injecting editable tools: {actually_added}",
            color="cyan",
        )


def collect_read_only_resource_ids(messages: MessageList) -> None:
    """Record the live ids of all explicitly read-only attachments for this turn.

    Walks EVERY user message (mirrors ``inject_editable_tools``) in chronological
    order. For each live id, the latest explicit decision wins: ``False`` adds
    the lock, ``True`` removes it, and ``None`` leaves the prior decision alone.
    This keeps a prior attachment locked while also allowing the user to reattach
    it as editable later, as the read-only refusal explicitly instructs.

    Writes the set onto the shared ``AppContext.metadata`` under
    ``READ_ONLY_RESOURCE_IDS_KEY``; write-capable tools consult it via
    ``is_resource_read_only`` before mutating. No-op when there is no context.
    """
    from matrx_connect.context.app_context import try_get_app_context

    from matrx_ai.config.enums import Role
    from matrx_ai.config.read_only_resources import set_read_only_resource_ids

    ctx = try_get_app_context()
    if ctx is None:
        return

    locked: set[str] = set()
    for message in messages:
        if message.role != Role.USER:
            continue
        for item in message.content:
            if not isinstance(item, _StructuredInputBase) or item.editable is None:
                continue
            resource_ids = item.resource_ids()
            if item.editable is True:
                locked.difference_update(resource_ids)
            else:
                locked.update(resource_ids)

    set_read_only_resource_ids(ctx.metadata, locked)
    if locked:
        vcprint(
            f"[StructuredInputResolver] Read-only resources locked: {sorted(locked)}",
            color="cyan",
        )


async def _load_agent_names(agent_ids: set[str]) -> dict[str, str]:
    """agent.definition id -> name, in ONE batched read. {} on any failure —
    the wording then falls back to "your …" rather than failing the turn."""
    if not agent_ids:
        return {}
    try:
        from matrx_ai.db._registry import get_model

        rows = await get_model("Definition").filter(id__in=sorted(agent_ids)).all()
    except Exception as exc:  # noqa: BLE001 — naming is wording, never a failed turn
        vcprint(
            f"[StructuredInputResolver] remarks: agent names unavailable ({exc}) — "
            "using 'your …' wording",
            color="yellow",
        )
        return {}
    return {
        str(row.id): str(getattr(row, "name", "") or "")  # orm-getattr-ok: model row
        for row in rows
    }


def _active_conversation_id() -> str | None:
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — no request context (a bare unit test)
        return None
    value = getattr(ctx, "conversation_id", None) if ctx is not None else None
    return str(value) if value else None


async def _prepare_remarks(
    messages: MessageList,
    containing: object,
    blocks_to_resolve: list[_StructuredInputBase],
) -> None:
    """Give each unresolved remarks block its location map, and put remarks last.

    Location wording ("your previous reply", "your reply 3 back") counts
    assistant TURNS back from the user message that CONTAINS the remark, so it
    needs the conversation — which a block's own resolve() never sees. It is
    bound here, once, and the rendered text is frozen in resolved_text: later
    turns skip resolved blocks, so the wording stays true to its own turn.

    When the counted replies come from more than one agent, another agent's
    reply is named ("Archaeologist's previous reply"): its names load in one
    batched read; the answering agent's own replies keep "your …".

    Remarks ride AFTER the person's typed text in the same turn: their typed
    message is what they are saying now; the remarks are what it refers to.
    """
    from matrx_ai.config.remarks import reply_agents, reply_authors, turns_back_by_message_id
    from matrx_ai.config.structured_input_config import RemarksInputContent

    remarks = [b for b in blocks_to_resolve if isinstance(b, RemarksInputContent)]
    if not remarks:
        return
    history = list(messages)

    # THREADS R1: every item gets its stable id and its conversation-wide
    # handle (c1, c2 …) BEFORE the wording is frozen — the handle is part of
    # the marker. R3: comment_reply failures recorded since the last remarks
    # ride in this remarks text (on the first block).
    from matrx_ai.config.remark_handles import assign_remark_handles, drain_reply_failures

    conversation_id = _active_conversation_id()
    await assign_remark_handles(
        history, [item for block in remarks for item in block.items], conversation_id
    )
    reply_failures = await drain_reply_failures(conversation_id)

    turns_back = turns_back_by_message_id(history, containing)
    authors: dict[str, str] = {}
    agent_by_reply = reply_agents(history, turns_back)
    if agent_by_reply:
        from matrx_ai.persistence.queue_helpers import running_agent_id

        answering = running_agent_id()
        names = await _load_agent_names(set(agent_by_reply.values()) - {answering})
        authors = reply_authors(agent_by_reply, names, answering)
    for index, block in enumerate(remarks):
        block.bind_turns_back(turns_back, authors, reply_failures if index == 0 else None)

    content = containing.content  # type: ignore[attr-defined]
    ordered = [c for c in content if not isinstance(c, RemarksInputContent)] + [
        c for c in content if isinstance(c, RemarksInputContent)
    ]
    if any(a is not b for a, b in zip(ordered, content, strict=True)):
        content[:] = ordered


async def resolve_structured_inputs(messages: MessageList) -> None:
    """Resolve all unresolved structured input blocks in the last user message.

    Runs all fetches concurrently.  Non-optional failures propagate as
    exceptions so the executor can surface them to the caller.  Optional
    failures are logged and silently dropped (block produces no output).

    Only the last user message is processed — prior turns are already stored
    and their resolved_text (if any) is already in metadata from when they
    were first sent.

    After resolution, any blocks with scrape_failures in metadata fire a
    client-side warning event via the emitter.
    """
    from matrx_ai.config.enums import Role

    last_user = messages.get_last_by_role(Role.USER)
    if last_user is None:
        return

    blocks_to_resolve = [
        item
        for item in last_user.content
        if isinstance(item, _StructuredInputBase) and "resolved_text" not in item.metadata
    ]

    if not blocks_to_resolve:
        return

    await _prepare_remarks(messages, last_user, blocks_to_resolve)

    vcprint(
        f"[StructuredInputResolver] Resolving {len(blocks_to_resolve)} block(s)",
        color="cyan",
    )

    await asyncio.gather(*[_resolve_one(b) for b in blocks_to_resolve])

    for block in blocks_to_resolve:
        _emit_block_warnings(block)
