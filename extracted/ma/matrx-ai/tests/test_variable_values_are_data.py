"""A variable's value is DATA: braces it brings are never slots (verify-RC-B5 r3 F5).

Live: Clean up ran on a chat answer holding ``{{pilot_region}}``. The agent's
template put the answer in ``{{transcript}}``; a second substitution pass took
the first pass's output as its template, counted ``{{pilot_region}}`` as an
authored placeholder, and told the model it was "NOT DELIVERED" — the agent
replied only "{{pilot_region}} was not delivered." (conversation 119f9545).
"""

from __future__ import annotations

from matrx_ai.config.undeclared import begin_turn, undelivered
from matrx_ai.config.unified_content import TextContent

ANSWER = "Phase one covers the 12 pilot stores in {{pilot_region}} on {{launch_date}}."


def _fresh() -> None:
    begin_turn()


def test_braces_inside_a_value_are_never_announced_as_undelivered_across_passes() -> None:
    _fresh()
    block = TextContent(text="Clean up this transcript:\n{{transcript}}")
    block.replace_variables({"transcript": ANSWER})  # pass 1 (agent definition)
    block.replace_variables({"transcript": ANSWER, "tone": "plain"})  # pass 2 (the run)
    assert block.text == f"Clean up this transcript:\n{ANSWER}"
    assert undelivered() == ()


def test_a_value_holding_another_variables_placeholder_is_not_filled() -> None:
    _fresh()
    block = TextContent(text="{{transcript}}\n\nRegion hint: {{pilot_region}}")
    block.replace_variables({"transcript": ANSWER, "pilot_region": "Arizona"})
    # The author's slot is filled; the braces inside the answer stay the answer's.
    assert block.text == f"{ANSWER}\n\nRegion hint: Arizona"


def test_an_authored_slot_left_for_a_later_pass_is_still_filled_then() -> None:
    _fresh()
    block = TextContent(text="{{transcript}} — for {{audience}}")
    block.replace_variables({"transcript": ANSWER})
    block.replace_variables({"audience": "store managers"})
    assert block.text == f"{ANSWER} — for store managers"


def test_an_authored_slot_nobody_filled_is_still_announced() -> None:
    _fresh()
    block = TextContent(text="Write for {{audience}}: {{transcript}}")
    block.replace_variables({"transcript": ANSWER})
    assert undelivered() == ("audience",)
