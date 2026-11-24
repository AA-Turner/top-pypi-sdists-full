"""P8 "Add a care note": a button authored with `ask` (an option the kit did not read) was saved and did nothing.
The write gate now refuses any KindActionButton option the kit does not read, naming it and the one meant."""

from __future__ import annotations

import pytest

from matrx_ai.tools.implementations.kind_shared import component_button_props_lint

DEAD = """
import { KindActionButton } from "@/components/kind-kit/KindActionButton";
export default function Care({ data, runAction }) {
  return <KindActionButton label="Add a care note" runAction={runAction} action="run"
    ask="What should the note say?" promptBeforeRun
    input={{ mandate: "care.add_note", variables: { dog: data.dog_name }, into: { state: "note_run" } }} />;
}
"""

GOOD_ONE = """
<KindActionButton label="Add a care note" runAction={runAction} action="run"
  asks={{ name: "note", question: "What should the note say?", placeholder: "Likes the blue towel" }}
  input={{ mandate: "care.add_note", variables: { dog: data.dog_name }, into: { state: "note_run" } }} />
"""

GOOD_MANY = """
<KindActionButton label="Add" runAction={runAction} action="run" confirm="Save it?" variant="primary"
  asks={[{ name: "note", question: "Note" }, { name: "who", question: "For?", required: false }]}
  input={() => ({ mandate: "care.add_note", into: { state: "n" } })} />
"""


def test_the_dead_care_note_button_is_refused_with_the_option_named():
    refusal = component_button_props_lint(DEAD)
    assert refusal is not None
    assert "not text" in refusal
    assert "has no option `promptBeforeRun` — did you mean `asks`?" in refusal


def test_the_old_spelling_ask_as_an_unknown_prop_names_the_right_one():
    refusal = component_button_props_lint('<KindActionButton label="x" runAction={r} action="a" input={{}} askFirst />')
    assert refusal and "no option `askFirst` — did you mean `asks`?" in refusal


@pytest.mark.parametrize("source", [GOOD_ONE, GOOD_MANY])
def test_a_well_formed_button_passes(source):
    assert component_button_props_lint(source) is None


def test_an_unknown_ask_field_key_and_a_run_input_ask_are_named():
    bad_field = '<KindActionButton label="x" runAction={r} action="run" asks={{ name: "n", label: "Note" }} input={{}} />'
    assert "`asks` has no option `label`" in (component_button_props_lint(bad_field) or "")
    bad_run = '<KindActionButton label="x" runAction={r} action="run" input={{ mandate: "a.b", ask: { name: "n" }, into: { state: "s" } }} />'
    assert "the run input has no option `ask` — asking first is the button's `asks` option" in (component_button_props_lint(bad_run) or "")
