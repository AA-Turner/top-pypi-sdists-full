"""THE REQUEST ENDS WITH WHAT THE PERSON TYPED (Arman, 2026-10-19).

    "there is content added AFTER the user's message!!!! That is NEVER EVER allowed because it
    completely poisons the request. The request must always END with the actual text the user
    typed. The things we add from the harness have to come before the user's message, never
    after."

Rule home: ``common-docs/systems/agents/agent-variable-binding/FEATURE.md``.

What this module owns
---------------------
``place_before_typed_text`` decides the order of the newest person turn on the wire, for every
chat provider. Its only wire caller is the send boundary (``send_boundary.order_for_wire``,
stored on ``SendPrep.wire_messages``); translators render that list and never reorder:

1. the agent's authored text (a template the person's words complete) stays first;
2. this turn's platform block (``MessageList.render_turn_context`` — live date, selection,
   values, attached skills…) comes next, as its OWN user turn (never a part of hers);
3. the person's attachments (and the ``<attachment …/>`` label each one carries) follow;
4. the person's typed text is LAST, byte-identical.

A turn with no typed text (a system job, an attachment-only send) keeps its own instruction last:
the block goes at the start of that message. On a send whose newest message is a tool result (a
live tool loop at any iteration, or a resumed turn: approval card, client-delegated tool, headless
resume) the block is placed where the turn's first send placed it — before the person's typed text
in their turn (``resumed_person_turn_index``), never after the tool result — so every send of the
turn sees its page values and the cached prefix is unchanged.

Never persisted: the placement is built on a shallow copy of the newest message for one send;
the ledger keeps the person's message exactly as stored.

``typed_text_problem`` is the guard: given the message list a send will render, it names what
rides after the person's typed text, or returns ``None``. ``prepare_for_send`` runs it on every
loop send (announced, never fatal), and the release-gate test
``tests/test_request_ends_with_what_the_person_typed.py`` runs the boundary's order through every
translator.
The live twin: ``aidream/scripts/check_request_ends_with_typed_text.py``.
"""

from __future__ import annotations

import copy
import logging
from typing import Any

logger = logging.getLogger(__name__)

#: The opening of the framed per-turn block (``MessageList.render_turn_context``).
TURN_CONTEXT_MARK = '<turn_context source="platform"'
#: Metadata key on the platform's own host turn (``host_turn``).
HOST_TURN_KEY = "platform_host_turn"
#: Metadata key on an EARLIER turn's block replayed where that turn's sends carried it
#: (``place_before_typed_text(..., replayed=True)``). Never ``HOST_TURN_KEY``: translators read
#: that key as "this send's block was placed" (``BaseTranslator._boundary_placed_block``).
REPLAYED_TURN_KEY = "platform_replayed_turn"
#: ``cx_message.metadata`` key on a person turn whose block rode INSIDE a cached prefix (a tool-loop
#: send: the block sits before her words, the rolling cache mark on the newest tool result). The
#: next turn replays it in the same place, so its history is byte-identical to what that send
#: cached (``send_boundary.keep_turn_context_for_next_turn``).
STORED_TURN_CONTEXT_KEY = "turn_context_in_cache"
#: Beside it: the per-slot texts that block was rendered from, so a later turn that places the kept
#: block on her turn again (a woken turn, a resumed run) sends only what changed since, as current.
STORED_TURN_CONTEXT_SLOTS_KEY = "turn_context_slots_in_cache"
#: Beside it: which of her blocks were her typed text when that send split her turn
#: (``typed_layout``: ``[[block index, tail chars]]``, ``-1`` = the whole block). The typed marks
#: live on the in-memory blocks only and do not survive storage, so a replay from storage could
#: not tell an authored template from her words and placed the block before the template
#: (REVIEW-C110 minor 1: first send ``[template] block [words]``, replay ``block [template+words]``,
#: the next turn after a tool loop missed the cache from message 0). The replay re-applies it.
STORED_TYPED_LAYOUT_KEY = "turn_context_typed_layout"
#: ``cx_message.metadata`` key on a person turn whose send placed LATE TOOL definitions before her words and kept
#: no whole block (a one-send turn): ``{late_tools:<wire name>: block}``. Every later send places exactly these
#: blocks there again (``send_boundary._replay_kept_turn_context``), inside the cached prefix, and a later turn
#: sends only the late tools that are new or changed since (``send_boundary._carried_late_tools``).
STORED_LATE_TOOLS_KEY = "late_tools_in_cache"
#: Host-turn metadata: this replayed turn carries ONLY late tool definitions (a carrier). The fit never drops it —
#: the definitions are what the model calls, not a cache convenience (``send_boundary._drop_replayed_turn_context``).
LATE_TOOLS_CARRIER_KEY = "platform_late_tools_carrier"
#: Host-turn metadata on a replayed whole block: the late tool slots inside it, so a fit that drops the block
#: leaves those definitions behind as a carrier.
REPLAYED_LATE_SLOTS_KEY = "platform_replayed_late_tools"

_DATA_TAIL_ATTR = "_variable_data_tail"


def _role(message: Any) -> str:
    role = getattr(message, "role", None)
    return str(getattr(role, "value", role) or "").lower()


def typed_words_of(content: Any) -> str:
    """A message's own words: the string itself, or its text blocks joined — never a Python repr.

    Dict-shaped (``{"type": "text", "text": ...}``) and object-shaped (``TextContent``) blocks both
    count; attachments and tool blocks carry no typed words.
    """
    if isinstance(content, str):
        return content
    texts: list[str] = []
    for block in content or []:
        if isinstance(block, str):
            texts.append(block)
            continue
        kind = block.get("type") if isinstance(block, dict) else getattr(block, "type", None)
        kind = str(getattr(kind, "value", kind) or "text")
        text = block.get("text") if isinstance(block, dict) else getattr(block, "text", None)
        if kind in ("text", "input_text") and isinstance(text, str) and text.strip():
            texts.append(text)
    return "\n\n".join(texts)


def person_turn_index(messages: list[Any]) -> int | None:
    """Index of the newest PERSON turn the reply answers, or ``None`` (mid tool loop, no user turn).

    A trailing authored prefill (the reply continues from it) is skipped: the person's turn is
    the one just before it.
    """
    if not messages:
        return None
    from matrx_ai.config.message_flags import flags_of
    from matrx_ai.config.tools_config import ToolResultContent

    index = len(messages) - 1
    last = messages[index]
    if _role(last) == "assistant" and flags_of(last).get("prefill") and index > 0:
        index -= 1
        last = messages[index]
    if _role(last) != "user":
        return None
    if any(isinstance(c, ToolResultContent) for c in getattr(last, "content", None) or []):
        return None
    return index


def _split(content: list[Any]) -> tuple[list[Any], list[Any], list[Any]]:
    """(authored, person attachments, person typed text) — order kept inside each group."""
    from matrx_ai.config.template_substitution import data_tail, is_data, mark_as_data
    from matrx_ai.config.unified_content import TextContent

    authored: list[Any] = []
    attachments: list[Any] = []
    typed: list[Any] = []
    from matrx_ai.config.attached_files import is_homed_block

    for block in content:
        if is_homed_block(block):
            # A homed block (an attached file or a held copy, ``attached_files``) rides with the
            # person's attachments, never authored lead: no send splits her turn around it.
            attachments.append(block)
            continue
        if is_data(block):
            (typed if type(block) is TextContent else attachments).append(block)
            continue
        tail = data_tail(block) if isinstance(block, TextContent) else ""
        if tail and isinstance(block.text, str) and block.text.endswith(tail):
            head = copy.copy(block)
            head.text = block.text[: len(block.text) - len(tail)]
            head.__dict__.pop(_DATA_TAIL_ATTR, None)
            if head.text.strip():
                authored.append(head)
            typed_block = TextContent(text=tail)
            mark_as_data(typed_block)
            typed.append(typed_block)
            continue
        authored.append(block)
    return authored, attachments, typed


def is_host_authored(message: Any) -> bool:
    """Whether ``message`` is a turn the SERVER wrote (``host_authored_user_turn``: a loop guard,
    ceiling, answer check, injection notice) or the platform's own host turn — never her words."""
    from matrx_ai.config.message_config import HOST_AUTHORED_BY

    metadata = getattr(message, "metadata", None)
    if not isinstance(metadata, dict):
        return False
    return (
        metadata.get("authored_by") == HOST_AUTHORED_BY
        or bool(metadata.get(HOST_TURN_KEY))
        or bool(metadata.get(REPLAYED_TURN_KEY))
    )


def turn_person_index(messages: list[Any]) -> int | None:
    """Index of the person turn the newest messages answer, or ``None``.

    The newest user message that is neither a tool result nor server-written. A server notice
    in the loop (``host_authored_user_turn``) sits right after a tool result, so a block placed
    before it rides after that result — the placement owner ruling PB-05 forbids. With no
    person-written turn at all (a headless run the host started), the newest user message that is
    not a tool result stands in, as before.
    """
    from matrx_ai.config.message_config import TURN_OPENING_REASONS
    from matrx_ai.config.tools_config import ToolResultContent

    # 🚨 A HEADLESS LOOP'S TURN IS ITS OPENING, NEVER A LATER NOTICE (lane DR, 2026-11-15: drift row
    # a059058b, conversation 2ca35cd7). With no person-written turn, the newest host turn used to stand in —
    # so a helper's report drained mid-loop (``host_authored_user_turn(reason="injection:…")``) became "the
    # turn", the block was re-frozen before it and left the opening turn inside the cached prefix. Stand-ins,
    # best first: the newest turn-opening host turn (``TURN_OPENING_REASONS``), else the newest host turn that
    # does not follow a tool result (a notice in the loop sits right after one), else the newest host turn.
    opening: int | None = None
    unlooped: int | None = None
    fallback: int | None = None
    for index in range(len(messages) - 1, -1, -1):
        message = messages[index]
        if _role(message) != "user":
            continue
        if any(isinstance(c, ToolResultContent) for c in getattr(message, "content", None) or []):
            continue
        if not is_host_authored(message):
            return index
        if fallback is None:
            fallback = index
        if opening is None and is_turn_opening(message, TURN_OPENING_REASONS):
            opening = index
        if unlooped is None and (index == 0 or _role(messages[index - 1]) != "tool"):
            unlooped = index
    if opening is not None:
        return opening
    return unlooped if unlooped is not None else fallback


def is_turn_opening(message: Any, reasons: frozenset[str] | None = None) -> bool:
    """Whether ``message`` is a host turn that OPENED a turn (``TURN_OPENING_REASONS``), not a notice in one."""
    if reasons is None:
        from matrx_ai.config.message_config import TURN_OPENING_REASONS as reasons
    metadata = getattr(message, "metadata", None)
    return isinstance(metadata, dict) and metadata.get("authored_reason") in reasons


def resumed_person_turn_index(messages: list[Any]) -> int | None:
    """Index of the person turn a RESUMED run answers, or ``None``.

    A resumed run (approval card, client-delegated tool, headless resume) starts on a list whose
    newest message is a tool result. Its person turn is the newest user message that is neither
    a tool result nor server-written (``turn_person_index``). The send boundary asks for it on
    every send whose newest message is a tool result (``send_boundary.order_for_wire``).
    """
    if not messages or _role(messages[-1]) != "tool":
        return None
    return turn_person_index(messages)


def place_before_typed_text(
    messages: list[Any],
    block: str | None,
    *,
    index: int | None = None,
    replayed: bool = False,
    host_metadata: dict[str, Any] | None = None,
) -> tuple[list[Any], bool]:
    """The send's message list with the newest person turn ordered so it ENDS with typed text.

    The platform block rides its OWN user turn (never a part of the person's message, never
    glued to her words) placed right before the person's own content: ``[authored template]``
    → ``[platform block]`` → ``[her attachments + typed text]``. Providers that merge
    consecutive user turns (Anthropic, Gemini) keep each as its own block/part.

    Returns ``(messages, placed)`` — ``placed`` is True when ``block`` was placed. The input
    list and its messages are never mutated; an unchanged turn returns the very same list.
    ``replayed=True`` places an EARLIER turn's stored block (``STORED_TURN_CONTEXT_KEY``) in the
    same layout, marked ``REPLAYED_TURN_KEY`` instead of ``HOST_TURN_KEY`` (plus ``host_metadata``).
    """
    if index is None:
        index = person_turn_index(messages)
    if index is None:
        return messages, False
    message = messages[index]
    content = list(getattr(message, "content", None) or [])
    host = host_turn(message, block) if block else None
    if host is not None and replayed:
        host.metadata = {REPLAYED_TURN_KEY: True, **(host_metadata or {})}
    # The homed blocks (attached files, held copies: ``attached_files.HOMED_BLOCK_MARK``) placed at
    # the start of this turn stay BEFORE the platform block on every send — the first send of a turn and every later replay of its kept
    # block alike — so the prefix a tool loop cached is the prefix the next turn sends
    # (REVIEW-C103 #2: the first send led with the file, the replay with the block, block 0
    # differed and the whole loop was re-written). With no block to place nothing moves.
    files = _leading_file_blocks(content) if host is not None else []
    rest = content[len(files):] if len(files) < len(content) else content
    if rest is content:
        files = []
    authored, attachments, typed = _split(rest)
    if not typed:
        # Read back from storage, her typed marks are gone: the layout the turn's send kept
        # (``STORED_TYPED_LAYOUT_KEY``) splits her turn exactly as that send did.
        metadata = getattr(message, "metadata", None)
        layout = metadata.get(STORED_TYPED_LAYOUT_KEY) if isinstance(metadata, dict) else None
        marked = with_typed_layout(rest, layout)
        if marked is not rest:
            authored, attachments, typed = _split(marked)
    if typed:
        person = [*attachments, *typed]
        lead = [*files, *authored]
    else:
        # No typed text: the job's own instruction (or the attachment) stays last.
        person, lead = rest, files
    if host is None and not lead and [id(b) for b in person] == [id(b) for b in content]:
        return messages, False
    turn: list[Any] = []
    if lead:
        head = copy.copy(message)
        head.content = lead
        turn.append(head)
    if host is not None:
        turn.append(host)
    own = copy.copy(message)
    own.content = person
    turn.append(own)
    return [*messages[:index], *turn, *messages[index + 1 :]], host is not None


def _own_block_indexes(content: list[Any]) -> list[int]:
    """Positions of HER blocks in ``content``: never a host-written block (a group chat's ``"Name:"``
    speaker block, ``authored_by=host``) nor a homed block (file or held copy) — both are added on
    the wire copy only, so the stored message she wrote never has them. A typed layout counts her blocks
    only: recorded on the stored message, applied on the wire turn, the same index names the same
    block (REVIEW-C110b I1: the speaker block shifted every index by one and the replay sent
    ``[HER WORDS] [BLOCK] [Alice:]``)."""
    from matrx_ai.config.attached_files import is_homed_block
    from matrx_ai.config.message_config import HOST_AUTHORED_BY

    own: list[int] = []
    for index, block in enumerate(content or []):
        metadata = getattr(block, "metadata", None)
        if isinstance(metadata, dict) and metadata.get("authored_by") == HOST_AUTHORED_BY:
            continue
        if is_homed_block(block):
            continue
        own.append(index)
    return own


def typed_layout(content: list[Any]) -> list[list[int]] | None:
    """Where her typed text sits among HER blocks of ``content`` (``_own_block_indexes``):
    ``[[own index, tail chars]]`` (``-1`` = the whole block is typed; else that many trailing chars
    of an authored block), or ``None``."""
    from matrx_ai.config.template_substitution import data_tail, is_data
    from matrx_ai.config.unified_content import TextContent

    blocks = list(content or [])
    out: list[list[int]] = []
    for own, index in enumerate(_own_block_indexes(blocks)):
        block = blocks[index]
        if type(block) is not TextContent:
            continue
        if is_data(block):
            out.append([own, -1])
            continue
        tail = data_tail(block)
        if tail and isinstance(block.text, str) and block.text.endswith(tail):
            out.append([own, len(tail)])
    return out or None


def with_typed_layout(content: list[Any], layout: Any) -> list[Any]:
    """``content`` with the typed marks of ``layout`` re-applied on copies of HER blocks (host-written
    and file blocks are skipped, as when it was recorded); ``content`` itself when the layout no
    longer fits (a block moved or changed: never guess)."""
    from matrx_ai.config.template_substitution import add_data_tail, mark_as_data
    from matrx_ai.config.unified_content import TextContent

    if not isinstance(layout, list) or not layout:
        return content
    out = list(content)
    own = _own_block_indexes(out)
    for entry in layout:
        if not (isinstance(entry, (list, tuple)) and len(entry) == 2):
            return content
        position, chars = entry
        if not (isinstance(position, int) and isinstance(chars, int) and 0 <= position < len(own)):
            return content
        index = own[position]
        block = out[index]
        if type(block) is not TextContent or not isinstance(block.text, str):
            return content
        twin = copy.copy(block)
        if chars < 0:
            mark_as_data(twin)
        elif 0 < chars <= len(block.text):
            add_data_tail(twin, block.text[len(block.text) - chars :])
        else:
            return content
        out[index] = twin
    return out


def _leading_file_blocks(content: list[Any]) -> list[Any]:
    """The homed blocks (files, held copies) at the start of ``content`` (where ``attached_files``
    puts them), keyed on ``HOMED_BLOCK_MARK``."""
    from matrx_ai.config.attached_files import is_homed_block

    out: list[Any] = []
    for block in content:
        if not is_homed_block(block):
            break
        out.append(block)
    return out


def host_turn(person_message: Any, block: str) -> Any:
    """The platform's own user turn carrying ``block`` (marked, never persisted)."""
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.unified_content import TextContent

    turn = UnifiedMessage(role=getattr(person_message, "role", "user"), content=[TextContent(text=block)])
    turn.metadata = {HOST_TURN_KEY: True}
    return turn


def refresh_host_turn(messages: list[Any], block: str | None) -> list[Any]:
    """``messages`` with the platform's host turn re-rendered to carry ``block``.

    For a per-turn slot joined AFTER the send boundary placed the block (a converted prefill's
    instruction, ``providers/unified_client._apply_message_flags``): the turn keeps its place,
    only its text follows the block. No host turn, or no block → the same list.
    """
    if not block:
        return messages
    out = list(messages)
    for index, message in enumerate(out):
        metadata = getattr(message, "metadata", None)
        if isinstance(metadata, dict) and metadata.get(HOST_TURN_KEY):
            turn = host_turn(message, block)
            # A part after the block (late tool definitions the fit left off the wire, re-sent here by
            # ``send_boundary._settle_late_tools_on_wire``) stays.
            turn.content = [*turn.content, *list(getattr(message, "content", None) or [])[1:]]
            out[index] = turn
            return out
    return messages


def _is_person_turn(message: Any) -> bool:
    from matrx_ai.config.tools_config import ToolResultContent

    return (
        _role(message) == "user"
        and not is_host_authored(message)
        and not any(isinstance(c, ToolResultContent) for c in getattr(message, "content", None) or [])
    )


def _is_trailing_note(message: Any) -> bool:
    """A server-written user turn (``host_authored_user_turn``: an inbox report, a decision note) that
    is not the platform's own block turn and did not open a turn."""
    from matrx_ai.config.message_config import HOST_AUTHORED_BY
    from matrx_ai.config.tools_config import ToolResultContent

    metadata = getattr(message, "metadata", None)
    return (
        _role(message) == "user"
        and isinstance(metadata, dict)
        and metadata.get("authored_by") == HOST_AUTHORED_BY
        and not metadata.get(HOST_TURN_KEY)
        and not metadata.get(REPLAYED_TURN_KEY)
        and not is_turn_opening(message)
        and not any(isinstance(c, ToolResultContent) for c in getattr(message, "content", None) or [])
    )


def notes_before_her_words(messages: list[Any]) -> list[Any]:
    """The send's list with every host note that DIRECTLY follows a person turn placed right before
    her own words (live guard, system_error 599b42da, 2026-11-18).

    The Turn-Boundary Inbox drain (``dynamic_drain.drain_pending_injections``) appends a host note
    (a Studio decision note, a helper's report, a wake) after her message when it runs at the first
    boundary of her turn, so the request ended with the server's words. Applied to EVERY person
    turn on every send, so a later send of the loop (and the next turn's history) carries the same
    order and the cached prefix holds. Wire copy only: the ledger keeps its order; an unchanged list
    is returned as the very same list.
    """
    out: list[Any] | None = None
    work = messages
    index = 0
    while index < len(work):
        if not _is_person_turn(work[index]):
            index += 1
            continue
        end = index + 1
        while end < len(work) and _is_trailing_note(work[end]):
            end += 1
        if end == index + 1:
            index += 1
            continue
        if out is None:
            out = list(work)
            work = out
        notes = work[index + 1 : end]
        work[index : end] = [*notes, work[index]]
        index = end
    return out if out is not None else messages


def _trailing_note_problem(messages: list[Any]) -> str | None:
    """A host note riding after the newest person turn with nothing in between, or ``None``."""
    end = len(messages)
    at = end - 1
    while at >= 0 and _is_trailing_note(messages[at]):
        at -= 1
    if at == end - 1 or at < 0 or not _is_person_turn(messages[at]):
        return None
    if not typed_words_of(getattr(messages[at], "content", None)).strip():
        return None
    texts = [typed_words_of(getattr(m, "content", None))[:60] for m in messages[at + 1 :]]
    return "after the typed text: host note " + " | ".join(texts)


def typed_text_problem(messages: list[Any]) -> str | None:
    """What rides after the person's typed text in the newest person turn, or ``None``.

    Reads the list exactly as it will be rendered. Only a turn that carries typed text is judged
    (a system job's instruction-last order is its author's). A server-written note riding after
    her turn (nothing else in between) is named too.
    """
    from matrx_ai.config.template_substitution import data_tail, is_data
    from matrx_ai.config.unified_content import TextContent

    trailing = _trailing_note_problem(messages)
    if trailing:
        return trailing
    index = person_turn_index(messages)
    if index is None:
        return None
    content = list(getattr(messages[index], "content", None) or [])
    has_typed = any(
        (is_data(b) and type(b) is TextContent) or (isinstance(b, TextContent) and data_tail(b))
        for b in content
    )
    if not has_typed:
        return None
    last = content[-1] if content else None
    if last is not None and type(last) is TextContent and is_data(last):
        return None
    if last is not None and isinstance(last, TextContent) and data_tail(last) and last.text.endswith(data_tail(last)):
        return None
    after: list[str] = []
    seen_typed = False
    for b in content:
        if (is_data(b) and type(b) is TextContent) or (isinstance(b, TextContent) and data_tail(b)):
            seen_typed = True
            after = []
            continue
        if seen_typed:
            text = getattr(b, "text", None)
            after.append(text[:60] if isinstance(text, str) else type(b).__name__)
    return "after the typed text: " + " | ".join(after or [type(last).__name__])


def announce_problem(problem: str, *, conversation_id: str | None, stage: str) -> None:
    """Loud, never fatal: a red console banner + an ERROR log line (app_log in the host)."""
    try:
        from matrx_utils import vcprint

        vcprint(
            data={"conversation_id": conversation_id, "stage": stage, "problem": problem},
            title="🚨 THE REQUEST DOES NOT END WITH WHAT THE PERSON TYPED",
            color="red",
        )
    except Exception:  # noqa: BLE001 — the log line below is the record
        pass
    logger.error(
        "request does not end with the person's typed text (conversation %s, %s): %s",
        conversation_id,
        stage,
        problem,
    )
