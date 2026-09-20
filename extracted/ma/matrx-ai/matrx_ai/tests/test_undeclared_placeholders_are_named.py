"""AGT-N-7 — an undeclared `{{placeholder}}` is named, never silently delivered.

THE MEASURED DEFECT (DYNAMIC-VALUES §D, 2026-09-16): `{{name}}` is substituted by a
naive `str.replace` over the declared variables, so `{{foo}}` — which nobody declared —
*"survives verbatim into the prompt with no warning anywhere in the substitution chain"*.
The model reads two braces and a word and either repeats them at a person or invents the
value they stood for.

The GREEN is the contract: the turn knows the name, and the system prompt carries one
sentence telling the model it was not delivered and must not be guessed.

The RED TWIN is the old behaviour, asserted directly: with the recorder removed from the
substitution path, the same prompt goes to the model with the brace still in it and
NOTHING anywhere names it. That is the failure this guard exists to make impossible, and
it is demonstrated, not described.
"""

from __future__ import annotations

from matrx_ai.config.undeclared import (
    begin_turn,
    note_unresolved,
    omission_sentence,
    undelivered,
)


def _prompt() -> str:
    return (
        "You are writing to {{customer_name}} about their {{plan_tier}} plan. "
        "Their renewal date is {{renewal_date}}."
    )


def _substitute(text: str, variables: dict[str, str]) -> str:
    """Exactly what the live substitution does: naive replace, declared names only."""
    for name, value in variables.items():
        text = text.replace(f"{{{{{name}}}}}", value)
    return text


def test_green_the_undelivered_placeholders_are_recorded_and_named() -> None:
    begin_turn()
    declared = {"customer_name": "All Green Recycling"}
    rendered = _substitute(_prompt(), declared)

    note_unresolved(rendered)

    # Both undeclared names are known to the turn, in the order they appear.
    assert undelivered() == ("plan_tier", "renewal_date")

    sentence = omission_sentence()
    assert sentence is not None
    # It names them the way they appear in the prompt, so the model can match them.
    assert "{{plan_tier}}" in sentence
    assert "{{renewal_date}}" in sentence
    # And it forbids the two failure modes the defect produced.
    assert "Do not guess" in sentence
    assert "say plainly which one was not delivered" in sentence

    # The delivered one is NOT named — a notice that cried about everything would be
    # ignored, and the substitution actually worked for this one.
    assert "customer_name" not in sentence


def test_red_the_same_prompt_with_no_recorder_names_nothing() -> None:
    """RED TWIN — the pre-guard behaviour, run on purpose.

    Substitution happens, the undeclared braces survive into the text the model would
    read, and because nothing recorded them the turn can answer no question about what
    it failed to deliver. Both halves of the old defect, asserted.
    """
    begin_turn()
    rendered = _substitute(_prompt(), {"customer_name": "All Green Recycling"})

    # The brace really does reach the model.
    assert "{{plan_tier}}" in rendered
    # And with no recorder in the path, the turn knows nothing and says nothing.
    assert undelivered() == ()
    assert omission_sentence() is None


def test_a_fully_delivered_prompt_says_nothing_at_all() -> None:
    begin_turn()
    rendered = _substitute(
        _prompt(),
        {"customer_name": "All Green", "plan_tier": "Pro", "renewal_date": "2026-11-02"},
    )
    note_unresolved(rendered)
    assert undelivered() == ()
    assert omission_sentence() is None


def test_the_pattern_does_not_mistake_structure_for_a_placeholder() -> None:
    """A prompt carrying JSON, a Jinja block or a Handlebars helper is not an omission."""
    begin_turn()
    note_unresolved(
        'Return {{"ok": true}} shaped JSON. {{# each rows }} {{! a comment }} '
        "{{ if x > 1 }}"
    )
    assert undelivered() == ()


def test_the_notice_is_appended_to_a_system_prompt_exactly_once() -> None:
    """The live path: a config substituted twice carries ONE notice, not two."""
    from matrx_ai.config.unified_config import UnifiedConfig

    config = UnifiedConfig(
        model="claude-sonnet-4-5",
        messages=[],
        system_instruction="Write to {{customer_name}} about {{plan_tier}}.",
    )
    begin_turn()
    config.replace_variables({"customer_name": "All Green"})
    first = config.system_instruction.base_instruction
    assert "{{plan_tier}}" in first, "the brace is recorded, never erased"
    assert first.count("[matrx:not-delivered]") == 1
    assert "{{plan_tier}}" in first.split("[matrx:not-delivered]")[1]

    config.replace_variables({"customer_name": "All Green"})
    assert config.system_instruction.base_instruction.count("[matrx:not-delivered]") == 1
