"""A mandate-held conversation's belt is never frozen onto its row.

THE DEFECT, measured on the live staff thread 2026-09-21. `ask_person` was
added to the Chief of Staff's belt. Five minutes later a headless turn on the
person's real staff thread — the SMS/voice/recovery shape, which does not open
the in-app door — assembled the OLD eighteen tools and answered with the OLD
refusal ("I never collect passwords through chat"). The cause was not the
resolver and not the agent: `chat.conversation.config` held a frozen 25-name
list, and `persist_completed_request` rewrote that blob at the END OF EVERY
TURN. `personal_staff/thread_row.py` already dropped those keys — in
`open_staff_thread`, so the repair was correct for one surface and undone by the
next turn on any of the other four.

WHAT EACH TEST WOULD CATCH. Delete the mandate-held branch in
``structural_conversation_update`` and the first three go red: the belt comes
back, the prompt gets frozen, and the marker is lost so the NEXT turn cannot
even tell the row is mandate-held. The last two pin the ordinary conversation,
which must keep its write-once prefix — a "fix" that unfreezes every chat on
the platform is a worse bug than the one it replaces.
"""

from __future__ import annotations

from matrx_ai.agents.live_structure import (
    HOLDER_OWNED_CONFIG_KEYS,
    LIVE_STRUCTURE_KEY,
    RESPONDER_MANDATE_KEY,
)
from matrx_ai.db.persistence import structural_conversation_update

#: What the live staff row carried before the fix, trimmed to the shape that
#: matters: the old belt plus the automatics, and the freeze flag.
FROZEN_STAFF_ROW = {
    "model": "claude-sonnet-5",
    LIVE_STRUCTURE_KEY: True,
    RESPONDER_MANDATE_KEY: "personal_staff.front_line",
}

#: What the turn assembled and would write back.
ASSEMBLED = {
    "model": "claude-sonnet-5",
    "tools": ["staff_roster", "staff_escalate", "mandate_call", "send_text"],
    "authored_tools": ["staff_roster", "staff_escalate"],
    "dynamic_tools": ["data", "records"],
    "tool_authority_filtered": True,
    "tool_authority_exclusions": ["fs_read", "shell_execute"],
    "temperature": 0.5,
}


def _mandate_held():
    return structural_conversation_update(
        assembled_config=dict(ASSEMBLED),
        existing_config=dict(FROZEN_STAFF_ROW),
        existing_system_instruction=None,
        incoming_system_instruction="You are the Chief of Staff…",
        request_already_frozen=False,
    )


def test_the_holders_belt_never_lands_on_a_mandate_held_row() -> None:
    result = _mandate_held()
    assert result.is_mandate_held is True
    leftovers = [k for k in HOLDER_OWNED_CONFIG_KEYS if k in result.config]
    assert leftovers == [], (
        f"a mandate-held row was written with {leftovers} — the next turn on "
        f"any surface that does not open the in-app door will run that belt "
        f"instead of the Holder's live one"
    )


def test_a_mandate_held_row_keeps_what_is_really_the_conversations() -> None:
    """Dropping the Holder's keys must not drop the row's own settings."""
    result = _mandate_held()
    assert result.config["model"] == "claude-sonnet-5"
    assert result.config["temperature"] == 0.5


def test_the_marker_survives_the_write_that_would_have_clobbered_it() -> None:
    """The preserving code and the clobbering code are the same code.

    The marker rides in the config blob precisely because this write replaces
    that blob wholesale. If it is not re-stamped here it lasts exactly one turn,
    and the turn after that cannot tell a mandate-held row from any other.
    """
    result = _mandate_held()
    assert result.config[LIVE_STRUCTURE_KEY] is True
    assert result.config[RESPONDER_MANDATE_KEY] == "personal_staff.front_line"


def test_a_mandate_held_row_never_freezes_a_system_prompt() -> None:
    result = _mandate_held()
    assert result.system_instruction is None, (
        "freezing the prompt pins the Holder's instructions as a write-once "
        "prefix, so re-instructing the Chief of Staff would never reach the "
        "thread again"
    )
    assert result.mark_request_frozen is False
    assert "system_prompt_frozen" not in result.config


def test_an_ordinary_conversation_still_freezes_on_its_first_turn() -> None:
    """The positive control. Unfreezing every chat would be the worse bug."""
    result = structural_conversation_update(
        assembled_config=dict(ASSEMBLED),
        existing_config={},
        existing_system_instruction=None,
        incoming_system_instruction="You are a helpful assistant.",
        request_already_frozen=False,
    )
    assert result.is_mandate_held is False
    assert result.system_instruction == "You are a helpful assistant."
    assert result.mark_request_frozen is True
    assert result.config["system_prompt_frozen"] is True
    assert result.config["tools"] == ASSEMBLED["tools"]


def test_an_ordinary_conversation_keeps_its_prefix_write_once() -> None:
    result = structural_conversation_update(
        assembled_config=dict(ASSEMBLED),
        existing_config={"system_prompt_frozen": True},
        existing_system_instruction="the prefix turn 1 wrote",
        incoming_system_instruction="something else entirely",
        request_already_frozen=False,
    )
    assert result.system_instruction is None
    assert result.config["system_prompt_frozen"] is True
