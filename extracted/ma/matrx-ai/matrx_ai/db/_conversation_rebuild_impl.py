"""Conversation Rebuild — Reconstruct message lists from the database.

When loading a conversation from the DB, tool-role messages may have empty
content (when saved by the new tool system). This module joins cx_tool_call
rows to rebuild the full ToolResultContent objects.

Usage:
    from matrx_ai.db import rebuild_conversation_messages

    messages = await rebuild_conversation_messages(conversation_id)
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.unified_config import UnifiedMessage
from matrx_ai.db._registry import get_model

CxMessage = get_model("Message")
CxToolCall = get_model("ToolCall")
CxMedia = get_model("Media")

logger = logging.getLogger(__name__)


def _relocate_separated_tool_results(messages: list[UnifiedMessage]) -> list[UnifiedMessage]:
    """Repair persisted results that landed after a later assistant message.

    A client-delegated result can be finalized after another assistant row has
    already taken the next position.  The row remains authoritative, but its
    model-facing projection must be moved back beside the tool_use it answers;
    otherwise MessageList.sanitize necessarily erases both blocks.
    """
    i = 0
    while i < len(messages):
        msg = messages[i]
        role = getattr(msg.role, "value", msg.role)
        if role != "assistant":
            i += 1
            continue
        calls = [
            c.id
            for c in msg.content
            if getattr(c, "type", None) == "tool_call" and getattr(c, "id", None)
        ]
        if not calls:
            i += 1
            continue

        window_end = i + 1
        adjacent: set[str] = set()
        while window_end < len(messages):
            next_role = getattr(messages[window_end].role, "value", messages[window_end].role)
            if next_role == "assistant":
                break
            for block in messages[window_end].content:
                rid = getattr(block, "tool_use_id", None) or getattr(block, "call_id", None)
                if getattr(block, "type", None) == "tool_result" and rid:
                    adjacent.add(rid)
            window_end += 1

        relocated: list[Any] = []
        for call_id in calls:
            if call_id in adjacent:
                continue
            for j in range(window_end, len(messages)):
                later = messages[j]
                # A repeated provider call id belongs to the nearer assistant
                # occurrence; never steal its result for an earlier turn.
                if any(
                    getattr(c, "type", None) == "tool_call"
                    and getattr(c, "id", None) == call_id
                    for c in later.content
                ):
                    break
                match = next(
                    (
                        c
                        for c in later.content
                        if getattr(c, "type", None) == "tool_result"
                        and (getattr(c, "tool_use_id", None) or getattr(c, "call_id", None))
                        == call_id
                    ),
                    None,
                )
                if match is not None:
                    later.content = [c for c in later.content if c is not match]
                    relocated.append(match)
                    break
        if relocated:
            messages.insert(i + 1, UnifiedMessage(role="tool", content=relocated))
            messages[:] = [m for m in messages if m.content]
            i += 1
        i += 1
    return messages



def _rebuild_tool_result_content(
    tool_calls: list[CxToolCall],
) -> list[dict[str, Any]]:
    """Convert cx_tool_call rows into ToolResultContent-compatible dicts.

    ``cx_tool_call`` is the single source of truth for ``output_chars`` and
    ``output_preview`` — the cx_message pointer block can be stale (e.g.
    client-delegated tools persist the parent message BEFORE the client
    posts the final output back, so its pointer block stays at the
    initial defaults). Always copy these fields through from the
    authoritative DB row so every downstream consumer sees current data.

    Error tool_results need special handling: when a tool errors before
    producing output, ``cx_tool_call.output`` is persisted as ``""`` (the
    formatted error string lives only in-memory via
    ``ToolResult.to_tool_result_content`` during the live run, not on the
    row). Anthropic rejects ``is_error=true`` with empty ``content`` —
    ``messages.N.content.0.tool_result: content cannot be empty if
    `is_error` is true``. We synthesise a non-empty fallback from
    ``error_type`` / ``error_message`` (and a stock string as last
    resort) so rebuilt conversations replay cleanly.
    """
    content_blocks: list[dict[str, Any]] = []

    for tc in tool_calls:
        content = tc.output
        # Groomed rows (Pattern 2): model_stub_at set ⇒ the MODEL sees a compact
        # self-describing stub instead of the full output. The row itself is
        # untouched (the user-facing view reads full cx_tool_call.output) and
        # pairing stays intact — a stub tool_result is still a tool_result, so
        # sanitize never drops the tool_use pair. Reversible by clearing the
        # stamp. Always non-empty (the Anthropic is_error guard).
        if getattr(tc, "model_stub_at", None) is not None:
            content = _stub_tool_result_text(tc)
        elif tc.is_error and not content:
            content = _synthesise_error_content(tc)

        content_blocks.append(
            {
                "type": "tool_result",
                "tool_use_id": tc.call_id,
                "call_id": tc.call_id,
                "name": tc.tool_name,
                "content": content,
                "is_error": tc.is_error,
                "output_chars": tc.output_chars,
                "output_preview": tc.output_preview,
            }
        )

    return content_blocks


def _stub_tool_result_text(tc: CxToolCall) -> str:
    """The compact model-facing replacement for a groomed tool result. Names the
    value key + true size and the retrieval paths, so the model can always get
    the content back deliberately. Never empty."""
    key = (getattr(tc, "value_ref_key", None) or "").strip()
    chars = int(getattr(tc, "output_chars", 0) or 0)
    ref = f" value_ref='{key}'" if key else ""
    fetch = (
        f"value_store get(key='{key}', max_chars=...)"
        if key
        else f"fetch_tool_result(call_id='{tc.call_id}', max_chars=...)"
    )
    return (
        f"[content stubbed]{ref} — {chars} chars retrieved earlier and no longer "
        f"held inline. The full result is unchanged and retrievable via {fetch}."
    )


def _synthesise_error_content(tc: CxToolCall) -> str:
    """Build a fallback content string for an error tool_result row with no output.

    Preference order: ``error_type: error_message`` → ``error_message`` →
    ``error_type`` → stock fallback. Always returns a non-empty string.
    """
    error_type = (getattr(tc, "error_type", None) or "").strip()
    error_message = (getattr(tc, "error_message", None) or "").strip()
    tool_name = getattr(tc, "tool_name", "") or "tool"

    if error_type and error_message:
        return f"{error_type}: {error_message}"
    if error_message:
        return error_message
    if error_type:
        return error_type
    return f"[Tool '{tool_name}' errored with no output]"


async def _map_tool_calls_to_messages(
    messages: list[CxMessage],
    tool_calls: list[CxToolCall],
) -> dict[str, list[CxToolCall]]:
    # Normalize ids to str on BOTH sides. The ORM materializes UUID columns
    # as str today, but a uuid.UUID slipping through either side would make
    # every membership test silently fail — and the model would then replay
    # EMPTY tool results (the persisted role='tool' stubs) on /resume.
    message_ids = {str(msg.id) for msg in messages}

    grouped: dict[str, list[CxToolCall]] = {}
    for tc in tool_calls:
        mid = tc.message_id
        if mid and str(mid) in message_ids and not tc.deleted_at:
            grouped.setdefault(str(mid), []).append(tc)

    return grouped


def _assistant_tool_use_call_ids(msg: CxMessage) -> list[str]:
    """Return the list of tool_use call_ids carried in an assistant message's
    ``content`` JSONB.

    Used by the synthetic-tool-message rebuild path so we know whether the
    cx_tool_call rows attributed to this assistant message are paired by a
    subsequent ``role='tool'`` message in the rebuilt list. When none are,
    we MUST synthesise one — otherwise the orphan tool_use is dropped by
    ``MessageList.sanitize`` at the next provider call and the entire
    delegated-tool round-trip vanishes.
    """
    content = getattr(msg, "content", None) or []
    ids: list[str] = []
    if not isinstance(content, list):
        return ids
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_call":
            continue
        cid = block.get("call_id") or block.get("id") or ""
        if cid:
            ids.append(str(cid))
    return ids


def _tool_result_call_ids(msg: CxMessage) -> list[str]:
    """Return the call_ids carried by ``tool_result`` blocks in a role='tool'
    message's ``content`` JSONB.

    The persisted role='tool' message is the proof that a result already exists
    for these ids — independent of whether any ``cx_tool_call`` row still links
    back via ``message_id``. The pairing guard uses this so a row whose
    ``message_id`` was never back-filled (NULL) can't trick the synthetic path
    into emitting a SECOND tool_result for a call the message already answers.
    """
    content = getattr(msg, "content", None) or []
    ids: list[str] = []
    if not isinstance(content, list):
        return ids
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_result":
            continue
        cid = block.get("call_id") or block.get("tool_use_id") or ""
        if cid:
            ids.append(str(cid))
    return ids


async def rebuild_conversation_messages(
    raw_messages: list[CxMessage],
    tool_calls: list[CxToolCall],
    media: list[CxMedia],
) -> list[CxMessage]:
    ordered_messages = sorted(raw_messages, key=lambda x: x.position)

    tool_call_map: dict[str, list[CxToolCall]] = await _map_tool_calls_to_messages(
        ordered_messages,
        tool_calls,
    )

    # The synthesis pairing accounting (which tool_uses still need a result
    # synthesised) is built AFTER content_rebuild_map below, because it must
    # count the results that the NULL-message_id recovery path also provides.
    # The delegate / suspend / resume path is the primary reason synthesis
    # exists: the assistant message is persisted at iteration commit with the
    # tool_use, but the loop suspends BEFORE any role='tool' message is written.
    # The result lives only in cx_tool_call (resolved by POST /tool_results), so
    # a naive rebuild feeds an orphan tool_use to the model on /resume — which
    # MessageList.sanitize then drops, taking the whole round-trip with it.

    # tool_calls grouped by the call_id they belong to — for fast synthesis
    # lookups below. Only includes rows that aren't deleted; status is NOT
    # filtered here so a 'delegated' (still-outstanding) row can be replayed
    # too (the sanitize pass at the next provider call will still drop the
    # tool_use because the synthesised result will have is_error=False but no
    # output — but at least we tried; the path that opens /resume already
    # 409s on outstanding delegated calls).
    tc_by_call_id: dict[str, list[CxToolCall]] = {}
    for tc in tool_calls:
        if getattr(tc, "deleted_at", None) is not None:
            continue
        if not tc.call_id:
            continue
        tc_by_call_id.setdefault(tc.call_id, []).append(tc)

    # Recovery map: persisted role='tool' messages whose cx_tool_call rows lost
    # the message_id link (NULL). We match the message's content tool_result
    # call_ids to the UNLINKED rows so the pointer stub still rebuilds from the
    # authoritative cx_tool_call row (the single source of truth for
    # output / is_error) instead of replaying an empty stub. Rows already
    # claimed by message_id are never double-claimed here. This is the data-
    # quality half of the 2026-06-22 duplicate-tool_result fix: a NULL
    # message_id should degrade to "rebuild from the row anyway", never to a
    # silent duplicate.
    linked_call_ids: set[str] = {
        tc.call_id for tcs in tool_call_map.values() for tc in tcs if tc.call_id
    }
    content_rebuild_map: dict[str, list[CxToolCall]] = {}
    for m in ordered_messages:
        if m.role != "tool":
            continue
        mid = str(m.id)
        if mid in tool_call_map:
            continue  # already linked by message_id
        recovered: list[CxToolCall] = []
        for cid in _tool_result_call_ids(m):
            if cid in linked_call_ids:
                continue
            recovered.extend(
                tc
                for tc in tc_by_call_id.get(cid, [])
                if not getattr(tc, "message_id", None)
            )
        if recovered:
            content_rebuild_map[mid] = recovered
            recovered_ids = [tc.call_id for tc in recovered]
            msg_text = (
                f"[rebuild_conversation_messages] Recovered {len(recovered)} "
                f"cx_tool_call row(s) for role='tool' message {mid} by call_id — "
                f"their message_id link is NULL. This is the unfinalized-tool-row "
                f"footgun behind duplicate tool_result 400s; the tool's persistence "
                f"path should back-fill cx_tool_call.message_id when it finalizes. "
                f"call_ids={recovered_ids}"
            )
            vcprint(msg_text, color="yellow")
            logger.warning(
                "rebuild recovered %d unlinked cx_tool_call row(s) by call_id for "
                "role='tool' message %s (NULL message_id): %s",
                len(recovered),
                mid,
                recovered_ids,
                extra={
                    "event": "rebuild_recovered_unlinked_tool_call",
                    "message_id": mid,
                    "call_ids": recovered_ids,
                },
            )

    # Pairing accounting — REUSE-SAFE. Anthropic mints globally-unique ids, but
    # Gemini REUSES deterministic call_ids across turns (e.g. gemini_-1 recurs
    # every turn, each a legitimate separate call). A conversation-global "is
    # this id paired anywhere" set therefore wrongly suppresses synthesis for a
    # LATER turn that reuses an id an EARLIER turn already answered — dropping
    # the later round-trip. Instead we (a) COUNT, per call_id, how many results
    # the persisted / recovered role='tool' messages already provide, and (b)
    # CONSUME cx_tool_call ROWS by id. Each turn's call has its own row even when
    # the id repeats, so synthesising only the EXCESS tool_uses from UNCONSUMED
    # rows pairs every turn correctly. (Only VISIBLE role='tool' messages count —
    # the main loop below emits only those.)
    persisted_result_count: dict[str, int] = {}
    consumed_row_ids: set[str] = set()
    for m in ordered_messages:
        if m.role != "tool":
            continue
        if not bool(getattr(m, "is_visible_to_model", True)):
            continue
        if getattr(m, "deleted_at", None) is not None:
            continue
        mid = str(m.id)
        rows = tool_call_map.get(mid) or content_rebuild_map.get(mid)
        if rows:
            for tc in rows:
                if tc.call_id:
                    persisted_result_count[tc.call_id] = (
                        persisted_result_count.get(tc.call_id, 0) + 1
                    )
                rid = getattr(tc, "id", None)
                if rid:
                    consumed_row_ids.add(str(rid))
        else:
            # Content-only role='tool' message (legacy full-content message with
            # no cx_tool_call row to rebuild from) — it still answers its ids.
            for cid in _tool_result_call_ids(m):
                persisted_result_count[cid] = persisted_result_count.get(cid, 0) + 1

    # Running per-call_id counters consulted by the synthesis loop, in document
    # order, so the Nth reuse of an id pairs with the Nth result.
    seen_tool_uses: dict[str, int] = {}
    synth_done: dict[str, int] = {}

    result: list[dict[str, Any]] = []
    for msg in ordered_messages:
        # Agent-context boundary (the designed primitive): the model sees ONLY
        # messages flagged is_visible_to_model and not soft-deleted. A failed
        # turn and any system-compacted message carry is_visible_to_model=False —
        # they remain in the user's history (is_visible_to_user) at their
        # original positions, but are NEVER replayed to the model. This is the
        # "visible to user, hidden from agent" boundary; it also honors the
        # compaction feature. (See STATUS_AND_ERROR_FIELDS.md.)
        if not bool(getattr(msg, "is_visible_to_model", True)):
            continue
        if getattr(msg, "deleted_at", None) is not None:
            continue
        role = msg.role
        msg_id = str(msg.id)

        if role == "tool" and msg_id in tool_call_map:
            rebuilt_content = _rebuild_tool_result_content(tool_call_map[msg_id])
            msg.content = rebuilt_content
        elif role == "tool" and msg_id in content_rebuild_map:
            # message_id link was NULL — rebuild from the rows recovered by
            # call_id so the model sees the authoritative output / error, not an
            # empty pointer stub (and never a duplicate of the synthetic path).
            rebuilt_content = _rebuild_tool_result_content(content_rebuild_map[msg_id])
            msg.content = rebuilt_content

        unified_message = UnifiedMessage.from_cx_message(msg)
        result.append(unified_message)

        # SYNTHESISE the matching tool_result(s) for any tool_use in THIS
        # assistant message that wasn't paired by a persisted role='tool'
        # message later in the conversation. This is the round-trip-vanishing
        # fix — without it, /resume hands the model an orphan tool_use which
        # MessageList.sanitize drops, taking the entire delegated round-trip
        # with it.
        if role == "assistant":
            tool_use_ids = _assistant_tool_use_call_ids(msg)
            synth_tcs: list[CxToolCall] = []
            for cid in tool_use_ids:
                seen_tool_uses[cid] = seen_tool_uses.get(cid, 0) + 1
                # Already answered? Count the persisted results + synths emitted
                # for this id so far. Only the EXCESS tool_uses (beyond available
                # results) need synthesis — this is what keeps a reused Gemini id
                # from suppressing a later turn that legitimately needs its own
                # result.
                already = persisted_result_count.get(cid, 0) + synth_done.get(cid, 0)
                if seen_tool_uses[cid] <= already:
                    continue
                rows = tc_by_call_id.get(cid)
                if not rows:
                    continue
                # Draw the next UNCONSUMED terminal row for this id. Skip rows
                # still 'delegated' or 'running' (no output yet — an empty
                # tool_result would be dropped by sanitize anyway) and rows
                # already emitted by a persisted/recovered message or an earlier
                # synth (consumed) so a reused id never double-emits.
                pick = next(
                    (
                        r
                        for r in rows
                        if str(getattr(r, "id", "")) not in consumed_row_ids
                        and (r.status or "").lower() in ("completed", "error")
                    ),
                    None,
                )
                if pick is None:
                    continue
                synth_tcs.append(pick)
                rid = getattr(pick, "id", None)
                if rid:
                    consumed_row_ids.add(str(rid))
                synth_done[cid] = synth_done.get(cid, 0) + 1
            if synth_tcs:
                synth_content = _rebuild_tool_result_content(synth_tcs)
                # The synthesised tool message has no DB row of its own; we
                # do NOT persist it. It exists only in the rebuilt
                # UnifiedConfig so the provider sees a coherent tool_use /
                # tool_result pair. Anthropic's pairing rule needs role=tool;
                # other providers tolerate this shape via UnifiedMessage's
                # normalisation.
                from matrx_ai.config.unified_config import (
                    UnifiedMessage as _UM,
                )
                synth_msg = _UM.from_dict({
                    "role": "tool",
                    "content": synth_content,
                })
                result.append(synth_msg)

    return _relocate_separated_tool_results(result)
