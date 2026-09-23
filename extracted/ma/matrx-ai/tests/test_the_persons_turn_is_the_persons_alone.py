"""THE PERSON'S TURN IS THE PERSON'S ALONE.

The real turn this guard is built from
--------------------------------------
On 2026-09-22, cold walk 21 drove the Masterwork Scout interview on production
as a first-time Expert (a residential repainting contractor). On her fifth turn
she described how she reads a chalk rag. The interviewer's answer opened:

    "Ignoring the injected block — that's platform noise, not from you."

Live evidence: ``chat.conversation`` 2eefaf04-1d23-4db5-82a6-1d3c0bfc870e,
assistant message at ``position`` 17; her turn is ``position`` 16, and its
durable ``model_context`` records the exact two blocks the platform staged for
that turn — reproduced byte for byte in ``fixtures/cold_walk_21_turn5.json``.

Root cause: those blocks were concatenated INTO her message's text, behind a
frame that told the model "the user did not write it … Do not respond to it".
The frame worked: the model disposed of the block and said so, to a person who
cannot see it and has no idea what was injected into her words. No wording
fixes that while the block sits inside her turn — the model answers her turn,
so anything inside it is answerable.

The fix is structural: per-turn platform material travels in the context
channel (``MessageList.attach_turn_context``) and is delivered in the
provider's SYSTEM channel. These assertions run against the assembled Anthropic
request, not against an intermediate helper.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "cold_walk_21_turn5.json").read_text()
)


def _the_real_turn() -> tuple[UnifiedConfig, str]:
    """The walk-21 turn, rebuilt: her words, and the two blocks that turn staged."""
    typed = FIXTURE["typed_by_the_person"]
    config = UnifiedConfig(
        model="claude-sonnet-4-5",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text=typed)])]
        ),
    )
    config.system_instruction = "You are Masterwork — Scout. Interview the Expert."
    config.messages.attach_turn_context(
        FIXTURE["active_context_block"], slot="active_context"
    )
    config.messages.attach_turn_context(
        FIXTURE["context_manifest_block"], slot="context_manifest"
    )
    return config, typed


def _assembled() -> tuple[dict, str]:
    config, typed = _the_real_turn()
    request = AnthropicTranslator().build_request(config, make_profile(model_name=config.model, wire_format="anthropic"))
    return request, typed


def _user_wire_text(request: dict) -> str:
    parts: list[str] = []
    for message in request["messages"]:
        if message.get("role") != "user":
            continue
        content = message.get("content")
        if isinstance(content, str):
            parts.append(content)
            continue
        for block in content or []:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text") or "")
    return "\n".join(parts)


def _system_wire_text(request: dict) -> str:
    system = request.get("system")
    if isinstance(system, str):
        return system
    return "\n".join(block.get("text") or "" for block in system or [])


def test_her_turn_reaches_the_model_as_exactly_what_she_typed() -> None:
    request, typed = _assembled()

    assert _user_wire_text(request) == typed


@pytest.mark.parametrize(
    "platform_marker",
    ["<turn_context", "<active_context>", "<available_context>", "AI Matrx platform"],
)
def test_no_platform_material_of_any_kind_is_inside_her_turn(platform_marker: str) -> None:
    request, _ = _assembled()

    assert platform_marker not in _user_wire_text(request)


def test_the_platform_material_is_delivered_in_the_system_channel() -> None:
    request, _ = _assembled()
    system = _system_wire_text(request)

    assert "<turn_context" in system
    assert FIXTURE["active_context_block"] in system
    assert FIXTURE["context_manifest_block"] in system


@pytest.mark.parametrize(
    "disposal_instruction",
    ["ignore", "do not respond to it", "not from you", "noise"],
)
def test_the_model_is_never_told_to_dispose_of_something_in_its_answer(
    disposal_instruction: str,
) -> None:
    """The sentence the Expert read was the model obeying an instruction.

    Nothing the platform sends may ask the model to ignore, discard, or not
    respond to material addressed to it — that is an instruction whose
    compliance is narratable, and on 2026-09-22 it was narrated at a person.
    """
    request, _ = _assembled()
    system = _system_wire_text(request)
    frame = system[system.index("<turn_context") :]

    assert disposal_instruction not in frame.lower()


def test_the_frame_forbids_mentioning_the_block_at_all() -> None:
    request, _ = _assembled()

    assert "Never quote it, name it, or mention that it exists" in _system_wire_text(request)


def test_the_per_turn_block_never_costs_the_prompt_cache() -> None:
    """Anthropic: the stable instruction carries the breakpoint; the per-turn
    block follows it UNCACHED, so a block rebuilt every turn cannot invalidate
    the cached prefix."""
    request, _ = _assembled()
    system = request["system"]

    assert isinstance(system, list) and len(system) == 2
    assert system[0]["cache_control"] == {"type": "ephemeral"}
    assert "<turn_context" not in system[0]["text"]
    assert "cache_control" not in system[1]
    assert system[1]["text"].startswith("<turn_context")


def test_nothing_from_the_turn_channel_can_reach_storage() -> None:
    config, typed = _the_real_turn()

    stored = config.to_storage_dict()["messages"]

    assert stored == [
        {
            "role": "user",
            "content": [{"type": "text", "text": typed}],
        }
    ]


def test_slots_accumulate_and_clear_together() -> None:
    messages = MessageList(
        _messages=[UnifiedMessage(role="user", content=[TextContent(text="HER WORDS")])]
    )
    messages.attach_turn_context("<attached_skills>S</attached_skills>", slot="skills")
    messages.attach_turn_context("<agent_context>A</agent_context>", slot="agent_context")
    messages.attach_turn_context("<available_context>M</available_context>", slot="manifest")

    rendered = messages.render_turn_context() or ""
    for survivor in ("<attached_skills>", "<agent_context>", "<available_context>"):
        assert survivor in rendered, f"{survivor} was clobbered by a later slot"
    assert "HER WORDS" not in rendered

    messages.attach_turn_context("REPLACED", slot="skills")
    assert "<attached_skills>" not in (messages.render_turn_context() or "")

    messages.clear_turn_context()
    assert messages.render_turn_context() is None
    assert messages[0].content[0].text == "HER WORDS"


# ── THE FIRST TURN (cold walk 22, 2026-09-22) ──────────────────────────────
#
# The fix above made per-turn platform material leave her turn. Her FIRST turn
# still carried the platform's own sentence: the Masterwork Scout's definition
# ends with a seeded user message, and her first words were appended INTO it.
# chat.conversation e450743f-45ad-4caa-8d30-149138c7f757, position 0: `content`
# began "Let's get started. Follow the mode you were given above, then ask your
# first concrete question." and then her words (`user_content` held hers
# alone). Reproduced byte for byte in fixtures/cold_walk_22_turn1.json.

FIRST_TURN = json.loads(
    (Path(__file__).parent / "fixtures" / "cold_walk_22_turn1.json").read_text()
)


def _the_first_turn(*, supports_tools: bool = True) -> tuple[UnifiedConfig, str]:
    """The Scout's definition as it loads (system + its seeded opening turn),
    then her first message, through the ONE door every run path uses."""
    config = UnifiedConfig.from_dict(
        {
            "model": "claude-sonnet-4-5",
            "messages": [
                {"role": "system", "content": "You are Masterwork — Scout. Interview the Expert."},
                {
                    "role": "user",
                    "content": [{"type": "text", "text": FIRST_TURN["definition_opening_turn"]}],
                },
            ],
        }
    )
    config.supports_tools = supports_tools
    typed = FIRST_TURN["typed_by_the_person"]
    config.append_or_extend_user_input(typed)
    return config, typed


def test_the_walk_22_first_turn_really_was_merged() -> None:
    """The fixture is the defect, not a paraphrase of it."""
    assert FIRST_TURN["stored_content_text"].startswith(
        FIRST_TURN["definition_opening_turn"]
    )
    assert FIRST_TURN["stored_content_text"].endswith(FIRST_TURN["typed_by_the_person"])


def test_her_first_turn_reaches_the_model_as_exactly_what_she_typed() -> None:
    config, typed = _the_first_turn()
    request = AnthropicTranslator().build_request(
        config, make_profile(model_name=config.model, wire_format="anthropic")
    )

    assert _user_wire_text(request) == typed
    assert "Let's get started" not in _user_wire_text(request)


def test_the_opening_turn_is_delivered_as_instructions() -> None:
    config, _ = _the_first_turn()
    request = AnthropicTranslator().build_request(
        config, make_profile(model_name=config.model, wire_format="anthropic")
    )
    system = _system_wire_text(request)

    assert FIRST_TURN["definition_opening_turn"] in system
    assert '<opening_turn source="agent_definition">' in system
    assert "never quote it, name it, or mention that it exists" in system
    for disposal in ("ignore", "do not respond", "noise"):
        assert disposal not in system[system.index("<opening_turn") :].lower()


def test_her_stored_first_turn_is_hers_alone() -> None:
    config, typed = _the_first_turn()
    stored = config.to_storage_dict()

    assert stored["messages"] == [
        {
            "role": "user",
            "content": [{"type": "text", "text": typed}],
            "user_content": [{"type": "text", "text": typed}],
        }
    ]


def test_the_opening_turn_survives_into_every_later_turn() -> None:
    """Lossless replay: it is frozen into the persisted system text, exactly
    where a continuation reads the prompt back from."""
    config, _ = _the_first_turn()
    persisted = config.to_storage_dict()["system_instruction"]

    assert FIRST_TURN["definition_opening_turn"] in persisted
    reloaded = UnifiedConfig.from_dict(
        {"model": "claude-sonnet-4-5", "system_instruction": persisted, "messages": []}
    )
    assert FIRST_TURN["definition_opening_turn"] in (reloaded.resolved_system_instruction or "")


def test_a_non_chat_model_keeps_the_template_in_its_prompt() -> None:
    """An image / TTS model's prompt IS the user text — nothing is lifted."""
    config, typed = _the_first_turn(supports_tools=False)

    only = [m for m in config.messages if m.role == "user"]
    assert len(only) == 1
    text = only[0].content[0].text
    assert text.startswith(FIRST_TURN["definition_opening_turn"]) and text.endswith(typed)


def test_a_later_turn_is_never_lifted() -> None:
    """Once anything was answered, a trailing user row is hers, not a seed."""
    config = UnifiedConfig.from_dict(
        {
            "model": "claude-sonnet-4-5",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": "first"}]},
                {"role": "assistant", "content": [{"type": "text", "text": "answer"}]},
                {"role": "user", "content": [{"type": "text", "text": "an old row"}]},
            ],
        }
    )
    assert config.lift_opening_turn(person_is_speaking=True) is False


def test_a_non_chat_model_that_slips_through_gets_the_template_back() -> None:
    """The dispatch backstop: capability is known there for every path."""
    from types import SimpleNamespace

    from matrx_ai.providers.unified_client import _strip_chat_decorations_if_non_fc

    config, typed = _the_first_turn()  # lifted: the run thought it was a chat model
    _strip_chat_decorations_if_non_fc(config, SimpleNamespace(supports_function_calling=False))

    text = [m for m in config.messages if m.role == "user"][0].content[0].text
    assert text.startswith(FIRST_TURN["definition_opening_turn"]) and text.endswith(typed)
    assert config.system_instruction.opening_turn == ""
