"""Trajectory sanitization for tool-call/tool-result integrity (ENG-7343, ENG-6214).

Strict providers (Anthropic, OpenAI, and OpenAI-compatible gateways) reject
requests whose tool-call structure is malformed. Mid-tool cancellation,
compaction, session resume, and weak-model output can all produce shapes that
400 the entire request and leave a session unrecoverable. This module is the
single pre-provider chokepoint that repairs them.

Two failure families, both surfacing as request-fatal 400s, are handled here:

1. **Orphan pairs.** An assistant ``tool_call`` with no matching ``tool_result``
   (or the inverse). Anthropic 400s with "unexpected tool_use_id ... must have a
   corresponding tool_use block". Cause: cancel mid-tool, or compaction splitting
   a pair across the summarization boundary.

2. **Malformed tool_calls that the adapter silently drops.** A ``tool_call`` with
   a blank ``function.name`` is dropped by Responses-API adapters while its
   ``function_call_output`` survives, producing OpenAI's
   "No tool call found for function call output with call_id ..." 400 — the same
   symptom as (1) but a different root cause the orphan pass cannot see (the id
   is present on both sides, so the pair *looks* complete). An empty
   ``tool_calls`` array is likewise rejected by some gateways (DeepSeek). These
   are normalized *before* the orphan analysis. Reference: hermes-agent
   ``agent/agent_runtime_helpers.py`` pre-call sanitizer.

None of these passes mutate the input messages or the persisted trajectory —
repaired messages are shallow copies, so stored history and prompt caching stay
byte-stable.
"""

from collections import Counter

from loguru import logger

from dreadnode.generators.message import Message

_INTERRUPTED_TOOL_RESULT = "[Tool execution was interrupted]"
# A blank tool-call name is invalid anyway; a non-empty sentinel keeps the call
# paired with its result through Responses-API adapters that would otherwise drop
# the nameless call and orphan its output.
_EMPTY_NAME_SENTINEL = "invalid_tool_call"


def _repair_tool_calls(messages: list[Message]) -> tuple[list[Message], int, int]:
    """Normalize assistant ``tool_calls`` that strict providers reject.

    - Empty ``tool_calls`` list → ``None`` (some gateways 400 on empty arrays).
    - Blank ``function.name`` → ``_EMPTY_NAME_SENTINEL`` so the call is not
      silently dropped by the adapter and orphaned from its output (ENG-7343).

    Returns ``(messages, emptied, renamed)``. Never mutates the input.
    """
    result: list[Message] = []
    emptied = 0
    renamed = 0

    for m in messages:
        if m.role != "assistant" or not m.tool_calls:
            # Collapse an empty (but non-None) tool_calls array to None.
            if m.role == "assistant" and m.tool_calls is not None and not m.tool_calls:
                result.append(m.model_copy(update={"tool_calls": None}))
                emptied += 1
            else:
                result.append(m)
            continue

        new_calls = []
        changed = False
        for tc in m.tool_calls:
            if (tc.function.name or "").strip():
                new_calls.append(tc)
                continue
            new_calls.append(
                tc.model_copy(
                    update={
                        "function": tc.function.model_copy(update={"name": _EMPTY_NAME_SENTINEL})
                    }
                )
            )
            renamed += 1
            changed = True

        result.append(m.model_copy(update={"tool_calls": new_calls}) if changed else m)

    return result, emptied, renamed


def sanitize_orphan_tool_messages(messages: list[Message]) -> list[Message]:
    """Return ``messages`` with tool-call/result integrity restored.

    Runs the malformed-tool_call repair, then resolves orphan pairs. Does not
    mutate the input list. Idempotent: ``f(f(x)) == f(x)``.
    """
    messages, emptied, renamed = _repair_tool_calls(messages)

    tool_use_ids: set[str] = {
        tc.id for m in messages if m.role == "assistant" and m.tool_calls for tc in m.tool_calls
    }
    # A *count* of available results per id, not a set: duplicate or blank ids
    # (weak models behind OpenAI-compatible gateways emit both) would collapse
    # in a set, so a second same-id call whose result is missing would never be
    # synthesized and reach the provider unmatched. Each call consumes one
    # available result; a call with none left gets a synthesized result.
    available_results: Counter[str] = Counter(
        m.tool_call_id for m in messages if m.role == "tool" and m.tool_call_id is not None
    )

    result: list[Message] = []
    synthesized = 0
    stripped = 0

    for m in messages:
        if m.role == "tool" and m.tool_call_id is not None and m.tool_call_id not in tool_use_ids:
            stripped += 1
            continue

        result.append(m)

        if m.role == "assistant" and m.tool_calls:
            for tc in m.tool_calls:
                if available_results[tc.id] > 0:
                    # Reserve one real result for this call; the rest of the loop
                    # keeps it in place when it is reached.
                    available_results[tc.id] -= 1
                    continue
                result.append(
                    Message(
                        role="tool",
                        tool_call_id=tc.id,
                        content=_INTERRUPTED_TOOL_RESULT,
                    )
                )
                synthesized += 1

    if synthesized or stripped or emptied or renamed:
        # INFO, not DEBUG: any repair here means a malformed/orphan tool shape
        # reached the provider boundary — a signal the compaction boundary
        # detector, a cancel path, or a weak model let something through. We
        # want to see this firing in the wild, not silently paper over it.
        # See ENG-7343 / ENG-6551 Phase 2.
        logger.info(
            "sanitize_orphan_tool_messages: synthesized={}, stripped={}, "
            "emptied_tool_calls={}, renamed_blank_tool_calls={}",
            synthesized,
            stripped,
            emptied,
            renamed,
        )

    return result
