"""An explicit ``system_instruction`` never drops the authored system messages in the list.

Before: ``UnifiedConfig.from_dict`` let an explicit instruction WIN and silently discarded every
authored system message it had lifted. Now the authored ones join AFTER the explicit
instruction, in order (filled with it under the rule); a later one stays in place as history.
"""

from __future__ import annotations

from matrx_ai.config import UnifiedConfig


def _msg(role: str, text: str) -> dict:
    return {"role": role, "content": text}


def test_authored_system_messages_join_after_the_explicit_instruction() -> None:
    config = UnifiedConfig.from_dict(
        {
            "model": "m",
            "system_instruction": "Explicit {{topic}}.",
            "messages": [
                _msg("system", "Authored one {{topic}}."),
                _msg("system", "Authored two."),
                _msg("user", "hi"),
                _msg("assistant", "hello"),
                _msg("system", "History {{topic}}."),
                _msg("user", "next"),
            ],
        },
        authored_message_count=3,
    )
    assert config.system_instruction.base_instruction == (
        "Explicit {{topic}}.\n\nAuthored one {{topic}}.\n\nAuthored two."
    )
    assert [m.role for m in config.messages] == ["user", "assistant", "system", "user"]

    config.replace_variables({"topic": "cats"}, template_messages=[])
    assert config.system_instruction.base_instruction == (
        "Explicit cats.\n\nAuthored one cats.\n\nAuthored two."
    )
    history = config.messages[2].content[0].text
    assert history == "History {{topic}}.", "history system text is data: never filled"


def test_explicit_dict_instruction_keeps_its_fields_and_gains_the_authored_text() -> None:
    config = UnifiedConfig.from_dict(
        {
            "model": "m",
            "system_instruction": {"base_instruction": "Base.", "intro": "Intro."},
            "messages": [_msg("system", "Authored."), _msg("user", "hi")],
        }
    )
    si = config.system_instruction
    assert si.base_instruction == "Base.\n\nAuthored."
    assert si.intro == "Intro."


def test_explicit_instruction_alone_is_unchanged() -> None:
    config = UnifiedConfig.from_dict(
        {"model": "m", "system_instruction": "Only.", "messages": [_msg("user", "hi")]}
    )
    assert config.system_instruction.base_instruction == "Only."
