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
from matrx_ai.db.edited_answers import (
    edited_answer_visible_to_model,
    original_model_content,
)
from matrx_ai.db.tool_result_text import _model_notices, tool_result_text_as_received
from matrx_ai.tools.models import _append_model_notices, media_ref_output_blocks

CxMessage = get_model("Message")
CxToolCall = get_model("ToolCall")
CxMedia = get_model("Media")

logger = logging.getLogger(__name__)


def _block_result_id(block: Any) -> str | None:
    if getattr(block, "type", None) != "tool_result":
        return None
    return getattr(block, "tool_use_id", None) or getattr(block, "call_id", None)


def _has_call(msg: UnifiedMessage, call_id: str) -> bool:
    return any(
        getattr(c, "type", None) == "tool_call" and getattr(c, "id", None) == call_id
        for c in msg.content
    )


def _take_earlier_result(messages: list[UnifiedMessage], i: int, call_id: str) -> Any | None:
    """Take the result for the call at ``i`` that was stored BEFORE it.

    ``result_before_call`` (system_error class sec_08238d): an old pair whose
    tool row took a lower position than its assistant row. The stored rows stay
    exactly as they are; only the model-facing projection moves. Conservative:
    the result is taken only when no other call with this provider id appears
    anywhere before it (provider ids are not globally unique, so a result that
    an earlier same-id call could own is never stolen) or between it and ``i``.
    """
    for j in range(i - 1, -1, -1):
        earlier = messages[j]
        if _has_call(earlier, call_id):
            return None
        match = next((c for c in earlier.content if _block_result_id(c) == call_id), None)
        if match is None:
            continue
        if any(_has_call(messages[k], call_id) for k in range(j)):
            return None
        earlier.content = [c for c in earlier.content if c is not match]
        return match
    return None


def _relocate_separated_tool_results(messages: list[UnifiedMessage]) -> list[UnifiedMessage]:
    """Repair persisted results that landed after a later assistant message.

    A client-delegated result can be finalized after another assistant row has
    already taken the next position.  The row remains authoritative, but its
    model-facing projection must be moved back beside the tool_use it answers;
    otherwise MessageList.sanitize necessarily erases both blocks.

    The mirror is healed the same way: a result stored BEFORE its call
    (``result_before_call``) is moved to just after the call. Without it the
    guard erased the pair and filed a new error on every turn of the
    conversation, forever.
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
            found_later = False
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
                    found_later = True
                    break
            if not found_later:
                earlier_match = _take_earlier_result(messages, i, call_id)
                if earlier_match is not None:
                    relocated.append(earlier_match)
                    vcprint(
                        f"[conversation_rebuild] Healed result_before_call: moved the stored "
                        f"result for {call_id!r} beside its call (stored rows untouched).",
                        color="yellow",
                    )
        if relocated:
            healed = UnifiedMessage(role="tool", content=relocated)
            messages.insert(i + 1, healed)
            messages[:] = [m for m in messages if m.content]
            # An earlier message emptied by the move shifts every index; re-find our spot.
            i = next(k for k, m in enumerate(messages) if m is healed)
        i += 1
    return messages



def _answers_name(tc: CxToolCall) -> str:
    """The tool name the result answers: the model's own call name.

    A server write the executor sent to the person as ``apply_surface_write``
    (``metadata.on_screen_redirect``) is stored under the door's name, but the
    model called the writer — Gemini pairs functionResponse to functionCall by name.
    """
    meta = getattr(tc, "metadata", None)
    redirect = meta.get("on_screen_redirect") if isinstance(meta, dict) else None
    answers = redirect.get("answers_name") if isinstance(redirect, dict) else None
    return str(answers) if answers else (getattr(tc, "tool_name", "") or "")


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
            notices = _model_notices(tc)
            if notices:
                content = f"{content}\n\n" + "\n".join(notices)
        elif not tc.is_error and (media_blocks := media_ref_output_blocks(content)) is not None:
            # A stored media-ref envelope (screenshot, document, audio, video)
            # replays as the SAME typed blocks the live turn sent — the image
            # itself, resolved from its file_id at the send boundary — never
            # as the envelope's JSON text (2026-11-01: a resumed extension chat
            # told the model "the screenshot gave me no readable content").
            notices = _model_notices(tc)
            content = (
                _append_model_notices(media_blocks, notices, tc.tool_name)
                if notices
                else media_blocks
            )
        else:
            content = tool_result_text_as_received(tc)

        content_blocks.append(
            {
                "type": "tool_result",
                "tool_use_id": tc.call_id,
                "call_id": tc.call_id,
                "name": _answers_name(tc),
                "content": content,
                "is_error": tc.is_error,
                "output_chars": tc.output_chars,
                "output_preview": tc.output_preview,
            }
        )

    return content_blocks


WAITING_ON_PERSON_TEXT = (
    "WAITING ON THE PERSON [{name}]: this change was proposed to the person and "
    "they have not decided on it yet (their approval card is still open, or they "
    "moved on without answering). It is NOT a failure and nothing was lost: "
    "nothing was written or changed yet. Do not call it again and do not tell "
    "the person it failed or 'dropped out'. If they ask, say it is waiting for "
    "their Apply or Keep as is; if the edit still matters, propose it once."
)


#: A call PARKED ON A PERSON (``chat.tool_call.metadata.parked_on``: an ``ask_person`` question, a spend ask, a
#: one-time-code or credential-capture card): only the person's answer resolves it, whatever tool made it.
PARKED_ON_PERSON_TEXT = (
    "WAITING ON THE PERSON [{name}]: this call is waiting for the person's answer on a card that is still open "
    "(they moved on without answering it yet). It is NOT a failure and nothing was lost. Do not call it again "
    "and do not tell the person it failed. Answer their newest message now; if the call still matters, say "
    "once that its card is waiting for them, and never assume an answer they did not give."
)


def _parked_on_person(tc: CxToolCall) -> bool:
    from matrx_ai.tools.logger import PARKED_ON_KEY

    metadata = getattr(tc, "metadata", None)
    return isinstance(metadata, dict) and bool(metadata.get(PARKED_ON_KEY))


#: A client-run call whose held stream the person's new message released (``_superseded_by_person``). Its app
#: may still answer; the result then lands on the row and reads normally on the following turn.
SUPERSEDED_BY_PERSON_TEXT = (
    "STILL WAITING FOR THE APP [{name}]: this call was handed to the person's app and no result has come back "
    "yet; the person sent a new message instead of waiting. It is NOT known to have failed, and it may still "
    "finish. Do not call it again now and do not tell the person it failed. Answer their newest message; if "
    "the call still matters, check its effect later or ask them to finish it in the app."
)


def _superseded_by_person(tc: CxToolCall) -> bool:
    from matrx_ai.tools.logger import SUPERSEDED_BY_PERSON_KEY

    metadata = getattr(tc, "metadata", None)
    return isinstance(metadata, dict) and bool(metadata.get(SUPERSEDED_BY_PERSON_KEY))


def _waiting_on_person_block(tc: CxToolCall) -> dict[str, Any]:
    name = getattr(tc, "tool_name", "") or "tool"
    if _parked_on_person(tc):
        template = PARKED_ON_PERSON_TEXT
    elif _superseded_by_person(tc):
        template = SUPERSEDED_BY_PERSON_TEXT
    else:
        template = WAITING_ON_PERSON_TEXT
    text = template.format(name=name)
    return {
        "type": "tool_result",
        "tool_use_id": tc.call_id,
        "call_id": tc.call_id,
        "name": _answers_name(tc) or name,
        "content": text,
        "is_error": False,
        "output_chars": len(text),
        "output_preview": None,
    }


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
    # One knob read per organization per rebuild (a conversation has one).
    edited_visible_by_org: dict[str | None, bool] = {}
    # A turn that ENDS on its client-delegated calls is still waiting on the
    # client; one with a later model-visible message means the person moved on
    # without deciding. Only the second gets the "waiting on the person" result.
    last_visible_idx = max(
        (
            i
            for i, m in enumerate(ordered_messages)
            if bool(getattr(m, "is_visible_to_model", True))
            and getattr(m, "deleted_at", None) is None
        ),
        default=-1,
    )
    for msg_idx, msg in enumerate(ordered_messages):
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
        # An assistant answer a person edited in place replays as EDITED unless
        # the organization's knob says the model sees its own original output
        # (agents.messages / edited_answer_visible_to_model, default true —
        # rich-content PLAN decision 13). Only the model-facing projection
        # changes; the row itself is never touched.
        original = original_model_content(msg)
        if original is not None:
            org_id = getattr(msg, "organization_id", None)
            org_key = str(org_id) if org_id is not None else None
            if org_key not in edited_visible_by_org:
                edited_visible_by_org[org_key] = await edited_answer_visible_to_model(org_key)
            if not edited_visible_by_org[org_key]:
                unified_message.content = UnifiedMessage._reconstruct_stored_content(original)
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
            # (row, waiting) in tool_use order - parallel calls keep their order
            synth_plan: list[tuple[CxToolCall, bool]] = []
            has_later_message = msg_idx < last_visible_idx
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
                waiting = False
                if pick is None:
                    # A parallel client-resolved call still `delegated` while the
                    # conversation moved on: the person has not decided. It gets
                    # its OWN honest result (never the generic "never answered"
                    # error that made the model say its tries "kept dropping").
                    pick = next(
                        (
                            r
                            for r in rows
                            if str(getattr(r, "id", "")) not in consumed_row_ids
                            and (r.status or "").lower() == "delegated"
                        ),
                        None,
                    )
                    # A turn that ENDS on its delegated calls is still waiting on the client — unless the
                    # call is PARKED ON A PERSON: its turn already ended (a client answer may not resolve it,
                    # only the person's), so a rebuild that sees it unanswered is a NEW turn the person
                    # started instead of answering, whose own message is appended after this rebuild.
                    # Left bare, the sanitizer paid it "TOOL NEVER ANSWERED" and filed an orphan row on
                    # every step of that turn (conversation 672f953e, 2026-11-19: credential_login parked
                    # on a credential-capture card, 6 rows).
                    # The same holds for a client-run call whose held stream the person's new message released
                    # (``_superseded_by_person``, section 1b rule P9): marked, it is waiting, never an orphan.
                    if pick is None or not (
                        has_later_message or _parked_on_person(pick) or _superseded_by_person(pick)
                    ):
                        continue
                    waiting = True
                synth_tcs.append(pick)
                synth_plan.append((pick, waiting))
                rid = getattr(pick, "id", None)
                if rid:
                    consumed_row_ids.add(str(rid))
                synth_done[cid] = synth_done.get(cid, 0) + 1
            if synth_tcs:
                synth_content = []
                for plan_tc, plan_waiting in synth_plan:
                    synth_content.extend(
                        [_waiting_on_person_block(plan_tc)]
                        if plan_waiting
                        else _rebuild_tool_result_content([plan_tc])
                    )
                # The synthesised tool message has no DB row of its own; we
                # do NOT persist it. It exists only in the rebuilt
                # UnifiedConfig so the provider sees a coherent tool_use /
                # tool_result pair. Anthropic's pairing rule needs role=tool;
                # other providers tolerate this shape via UnifiedMessage's
                # normalization.
                from matrx_ai.config.unified_config import (
                    UnifiedMessage as _UM,
                )
                synth_msg = _UM.from_dict({
                    "role": "tool",
                    "content": synth_content,
                })
                result.append(synth_msg)

    return _relocate_separated_tool_results(result)
