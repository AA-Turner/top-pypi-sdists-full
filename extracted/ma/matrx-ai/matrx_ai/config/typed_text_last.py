"""THE REQUEST ENDS WITH WHAT THE PERSON TYPED (Arman, 2026-10-19).

    "there is content added AFTER the user's message!!!! That is NEVER EVER allowed because it
    completely poisons the request. The request must always END with the actual text the user
    typed. The things we add from the harness have to come before the user's message, never
    after."

Rule home: ``common-docs/systems/agents/agent-variable-binding/FEATURE.md``.

What this module owns
---------------------
``place_before_typed_text`` decides the order of the newest person turn on the wire, for every
chat provider (``BaseTranslator.messages_for_wire`` is its only wire caller):

1. the agent's authored text (a template the person's words complete) stays first;
2. this turn's platform block (``MessageList.render_turn_context`` — live date, selection,
   values, attached skills…) comes next, as its OWN user turn (never a part of hers);
3. the person's attachments (and the ``<attachment …/>`` label each one carries) follow;
4. the person's typed text is LAST, byte-identical.

A turn with no typed text (a system job, an attachment-only send) keeps its own instruction last:
the block goes at the start of that message. Mid tool loop (the newest message is a tool result)
nothing is placed — the person's turn is history then, and the block is not re-sent.

Never persisted: the placement is built on a shallow copy of the newest message for one send;
the ledger keeps the person's message exactly as stored.

``typed_text_problem`` is the guard: given the message list a send will render, it names what
rides after the person's typed text, or returns ``None``. ``prepare_for_send`` runs it on every
loop send (announced, never fatal), and the release-gate test
``tests/test_request_ends_with_what_the_person_typed.py`` runs it through every translator.
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

_DATA_TAIL_ATTR = "_variable_data_tail"


def _role(message: Any) -> str:
    role = getattr(message, "role", None)
    return str(getattr(role, "value", role) or "").lower()


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
    for block in content:
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


def place_before_typed_text(messages: list[Any], block: str | None) -> tuple[list[Any], bool]:
    """The send's message list with the newest person turn ordered so it ENDS with typed text.

    The platform block rides its OWN user turn (never a part of the person's message, never
    glued to her words) placed right before the person's own content: ``[authored template]``
    → ``[platform block]`` → ``[her attachments + typed text]``. Providers that merge
    consecutive user turns (Anthropic, Gemini) keep each as its own block/part.

    Returns ``(messages, placed)`` — ``placed`` is True when ``block`` was placed. The input
    list and its messages are never mutated; an unchanged turn returns the very same list.
    """
    index = person_turn_index(messages)
    if index is None:
        return messages, False
    message = messages[index]
    content = list(getattr(message, "content", None) or [])
    authored, attachments, typed = _split(content)
    host = host_turn(message, block) if block else None
    if typed:
        person = [*attachments, *typed]
        lead = authored
    else:
        # No typed text: the job's own instruction (or the attachment) stays last.
        person, lead = content, []
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


def host_turn(person_message: Any, block: str) -> Any:
    """The platform's own user turn carrying ``block`` (marked, never persisted)."""
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.unified_content import TextContent

    turn = UnifiedMessage(role=getattr(person_message, "role", "user"), content=[TextContent(text=block)])
    turn.metadata = {HOST_TURN_KEY: True}
    return turn


def typed_text_problem(messages: list[Any]) -> str | None:
    """What rides after the person's typed text in the newest person turn, or ``None``.

    Reads the list exactly as it will be rendered. Only a turn that carries typed text is judged
    (a system job's instruction-last order is its author's).
    """
    from matrx_ai.config.template_substitution import data_tail, is_data
    from matrx_ai.config.unified_content import TextContent

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
