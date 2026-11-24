"""A child-agent call refused for having no message names the field the calling tool actually offers.

PB-03 r2/r3 copy O: gpt-5-nano called ``agent`` with variables and no prompt, and the refusal told it to send
``user_input``, a field the ``agent`` tool does not offer (its field is ``prompt``).

SUT: the real ``empty_child_turn_guidance``.
"""

from __future__ import annotations

from matrx_ai.agents.child_turn import empty_child_turn_guidance


def test_the_sentence_names_the_field_it_is_given() -> None:
    message, action = empty_child_turn_guidance("Lane Planner", input_arg="prompt")
    assert "prompt" in message and "prompt" in action and "user_input" not in message + action
