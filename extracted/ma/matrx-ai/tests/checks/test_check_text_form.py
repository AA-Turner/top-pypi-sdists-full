"""The one-line text form round-trips to the same Check JSON (CONTRACT v2 §2.2)."""

from __future__ import annotations

import pytest

from matrx_ai.checks.text_form import CheckTextError, format_check, parse_check_text

CONTRACT_EXAMPLES = [
    'expect reply.field("SHELF") contains pick_list(glaze_family).hidden_text.match("shelf (\\S+)")',
    "expect request.system contains input.variables.student_name",
    'expect request.system not contains "SF-88"',
    "expect reply[2].final(1) == input.variables.order_name",
    "expect request[2].system == observed(request[1].system)",
    "expect stored[each].messages not contains input.turn(2).variable_edits.student_name",
    "expect reply[2] not contains pick_list(glaze_family).hidden_text@seeded",
    "expect same_across_doors(request.system, ignore: context)",
    "expect usage.cost_cents <= 2",
    'expect outcome.status == "refused_by_validation"',
    'expect rows("chat.message", conversation_id = run.conversation_id, role = "assistant") count == 0',
    "expect output.items count >= 3",
    'expect tool_calls("search").args.query contains marker("Q")',
    'expect reply.field("TOKENS").split("|", 2).trim == default(oven)@edited',
    'expect door in ["agents", "manual"]',
    'expect output conforms ["title", "items"]',
    "expect reply[1] exists",
]


@pytest.mark.parametrize("text", CONTRACT_EXAMPLES)
def test_round_trip(text):
    check = parse_check_text(text, id="x")
    again = parse_check_text(format_check(check), id="x")
    assert again == check, (text, format_check(check))


def test_seeded_is_the_default_at():
    a = parse_check_text("expect reply[2] not contains pick_list(g).hidden_text@seeded", id="a")
    b = parse_check_text("expect reply[2] not contains pick_list(g).hidden_text", id="a")
    assert a == b


@pytest.mark.parametrize(
    "bad",
    ["expect nowhere contains 1", "expect reply teleports 1", 'expect reply contains "open', "reply contains 1",
     "expect reply contains input", "expect reply == 1 trailing"],
)
def test_errors_name_a_position(bad):
    with pytest.raises(CheckTextError) as err:
        parse_check_text(bad)
    assert err.value.position >= 0
