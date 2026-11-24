"""FORCING GUARD — a person turn that joins a running loop never rewrites the prefix the loop cached.

Live (lane C116, 2026-11-09/10): ``prompt_cache_prefix_drift`` on groq gpt-oss-20b (conversations 9eacb6c9,
5f62921c, 985e1ecc, 3c5c695d, 545440be), openai gpt-5-nano (ad0e8d97) and anthropic claude-sonnet-5-5
(85c1d3b6). Every one has the same request snapshots: send N carried the ``<turn_context>`` block before her
FIRST words (``system, CTX, user1``); a queued person message then joined the same loop
(``drain_pending_injections``) and send N+1 carried the block before her NEW words only
(``system, user1, assistant, CTX, user2``). The block the loop had already sent — inside the prefix the
provider cached — vanished from her first turn, so every byte after the system text was re-written to the
cache. The freeze (``MessageList.freeze_turn_context``) re-froze for the new turn and dropped the old block;
``keep_turn_context_for_next_turn`` only ran at the END of the request.

The fix keeps the earlier turn's frozen block on that turn the moment a new person turn re-freezes
(``send_boundary._turn_block``), so ``_replay_kept_turn_context`` places it again where the loop sent it.

Each case runs the real send boundary and the real translator for every chat wire, and compares the two
sends with the real ``cache_guard`` (the alarm that filed the live rows). Assembling the same send twice
must also give the same bytes.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.providers.cache_guard import compare_wire_prefix, wire_prefix
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You are a careful assistant. " * 40
BLOCK = "<active_context><organization id=\"o-1\">Workspace</organization></active_context>"

WIRES = [
    ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
    ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses"),
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat"),
]


def _msg(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


def _send(module: str, cls: str, wire_format: str, config: UnifiedConfig, iteration: int) -> Any:
    profile = make_profile(model_name="m", wire_format=wire_format)
    prep = order_for_wire(config, profile, iteration=iteration)
    translator = getattr(importlib.import_module(module), cls)()
    return translator.build_request(prep.wire_config if prep.wire_config is not None else config, profile)


def _loop_config() -> UnifiedConfig:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=[_msg("user", "FIRST WORDS write 120 lines")]))
    config.system_instruction = SYSTEM
    config.messages.attach_turn_context(BLOCK, slot="active_context")
    return config


@pytest.mark.parametrize(("module", "cls", "wire_format"), WIRES)
def test_a_queued_person_turn_keeps_the_loops_cached_prefix(module: str, cls: str, wire_format: str) -> None:
    config = _loop_config()
    _send(module, cls, wire_format, config, iteration=1)
    # One tool round (the live Sonnet case 85c1d3b6 had several): the send after it caches a prefix
    # holding the block before her first words.
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="c0", name="lookup", arguments={"q": "keeper"})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="c0", name="lookup", content="RESULT " * 50)])
    )
    first = _send(module, cls, wire_format, config, iteration=2)
    # Her queued message drains into the SAME loop (``drain_pending_injections``), after the reply.
    config.messages.append(_msg("assistant", "1. The keeper climbs the stairs."))
    config.messages.append(_msg("user", "SECOND WORDS what was the keeper's name?"))
    second = _send(module, cls, wire_format, config, iteration=3)

    prev, new = wire_prefix(first), wire_prefix(second)
    assert prev is not None and new is not None, "the cache guard cannot read this wire"
    drift = compare_wire_prefix(prev, new)
    assert not drift.changed, f"{wire_format}: the queued turn rewrote the cached prefix: {list(drift.changed)}"


@pytest.mark.parametrize(("module", "cls", "wire_format"), WIRES)
def test_the_same_send_assembled_twice_is_byte_identical(module: str, cls: str, wire_format: str) -> None:
    a = wire_prefix(_send(module, cls, wire_format, _loop_config(), iteration=1))
    b = wire_prefix(_send(module, cls, wire_format, _loop_config(), iteration=1))
    assert a is not None and b is not None
    assert a.sha() == b.sha() and not compare_wire_prefix(a, b).changed


#: Gemini's wire carries no call id on a function response, so a trim there cannot be placed by id
#: (named in C116 as a known limit, not covered here).
ID_WIRES = [w for w in WIRES if w[2] != "google_chat"]


@pytest.mark.parametrize(("module", "cls", "wire_format"), ID_WIRES)
def test_a_declared_tool_output_trim_is_placed_on_every_wire(module: str, cls: str, wire_format: str) -> None:
    """The send boundary's large-output trim is LAWFUL behind the cache line; the guard must find the trimmed
    result on the wire by its call id. On the xAI proto wire (``ROLE_TOOL`` / ``toolCallId``) it could not, so
    every grok trim was filed as ``prompt_cache_prefix_drift`` (C116: conversation 6c62a26b, 3 tool results
    "could not place")."""
    from matrx_ai.providers.cache_guard import TrimDeclaration, place_trim_on_wire

    config = _loop_config()
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="call_7c116", name="web", arguments={"q": "x"})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="call_7c116", name="web", content="BIG " * 50)])
    )
    request = _send(module, cls, wire_format, config, iteration=2)
    positions, unplaced = place_trim_on_wire(request, TrimDeclaration(results=frozenset({"call_7c116"})))
    assert unplaced == 0 and positions, f"{wire_format}: the declared trim of call-7 was not found on the wire"


# REVIEW-C116 I1: the send boundary often orders a list of COPIES (wire swaps deep-copy every message;
# an attached file homed on her first turn copies that message). The kept block must reach the stored
# message too, or every send after the one that kept it loses the block again. Four sends: first words,
# a tool round, her queued words, another tool round; every pair compared.


def _send_on_copies(module: str, cls: str, wire_format: str, config: UnifiedConfig, iteration: int, mode: str) -> Any:
    import copy

    from matrx_ai.config.send_boundary import STAGE_LOOP, SendPrep, _wire_list

    profile = make_profile(model_name="m", wire_format=wire_format)
    prep = SendPrep(stage=STAGE_LOOP)
    if mode == "deep_copy":  # build_wire_config with wire swaps present
        wire = copy.copy(config)
        wire.messages = copy.deepcopy(config.messages)
        prep.wire_config = wire
    elif mode == "first_turn_copy":  # place_attached_files homes a file on her first turn: copy(out[index])
        placed = [copy.copy(m) if i == 0 else m for i, m in enumerate(config.messages)]
        wire = copy.copy(config)
        wire.messages = _wire_list(config.messages, placed)
        prep.wire_config = wire
    prep = order_for_wire(config, profile, prep=prep, iteration=iteration)
    translator = getattr(importlib.import_module(module), cls)()
    return translator.build_request(prep.wire_config if prep.wire_config is not None else config, profile)


def _tool_round(config: UnifiedConfig, call_id: str) -> None:
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id=call_id, name="lookup", arguments={"q": "k"})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id=call_id, name="lookup", content="RESULT " * 50)])
    )


@pytest.mark.parametrize("mode", ["same_objects", "deep_copy", "first_turn_copy"])
@pytest.mark.parametrize(("module", "cls", "wire_format"), WIRES)
def test_every_send_after_the_queued_turn_keeps_the_prefix(module: str, cls: str, wire_format: str, mode: str) -> None:
    config = _loop_config()
    sends = [_send_on_copies(module, cls, wire_format, config, 1, mode)]
    _tool_round(config, "c0")
    sends.append(_send_on_copies(module, cls, wire_format, config, 2, mode))
    config.messages.append(_msg("assistant", "1. The keeper climbs the stairs."))
    config.messages.append(_msg("user", "SECOND WORDS what was the keeper's name?"))
    sends.append(_send_on_copies(module, cls, wire_format, config, 3, mode))
    _tool_round(config, "c1")
    sends.append(_send_on_copies(module, cls, wire_format, config, 4, mode))
    for n in range(1, 4):
        drift = compare_wire_prefix(wire_prefix(sends[n - 1]), wire_prefix(sends[n]))
        assert not drift.changed, f"{wire_format} {mode}: send {n} -> {n + 1} rewrote the prefix: {list(drift.changed)}"
    # The stored message carries the kept block (the copy alone is lost from the next send on).
    from matrx_ai.config.typed_text_last import STORED_TURN_CONTEXT_KEY

    first = list(config.messages)[0]
    assert BLOCK in (first.metadata or {}).get(STORED_TURN_CONTEXT_KEY, ""), f"{mode}: the stored first turn kept nothing"


def test_an_ambiguous_id_less_turn_is_never_matched_to_the_wrong_stored_turn() -> None:
    """C116 round-2 review: the ledger holds two id-less person turns with the same words ("ok") and
    the wire list is shifted against it (the window dropped the first pair). Position + words named
    stored[0] for the wire copy of stored[2], and the kept block + typed layout were stamped and
    persisted on the wrong turn. Ambiguous → no stored match (the wire copy is still stamped)."""
    from matrx_ai.config import send_boundary as sb

    def message(role: str, text: str) -> UnifiedMessage:
        return UnifiedMessage(role=role, content=[TextContent(text=text)])

    stored = [message("user", "ok"), message("assistant", "hi"), message("user", "ok"), message("assistant", "x")]
    wire = [message("user", "ok")]  # a copy of stored[2], at index 0 after the window cut
    got = sb._stored_message(stored, wire[0], 0, sb._turn_key(stored, 0))
    assert got is None or got is stored[2], f"matched stored[{stored.index(got)}]"
    # Unambiguous words still resolve by position.
    stored[2] = message("user", "only once")
    assert sb._stored_message(stored, message("user", "ok"), 0, sb._turn_key(stored, 0)) is stored[0]
