"""A mandate refusal's message matches its code (2026-11-16).

Every ``MandateRefused`` inherited the base class's resolver-missing message, so an ``inputs`` refusal (the
caller left a guaranteed value out) told the reader to "Install a mandate resolver for this process" and
never named what was missing. Triage then chased a deployment fault that did not exist.
"""

from matrx_ai.mandates import MandateRefused


def test_an_inputs_refusal_names_the_missing_inputs_and_not_the_resolver_remedy() -> None:
    exc = MandateRefused(
        "brand.rule_check_own_writing",
        code="inputs",
        sentence="This agent needs Brand, and nothing was given for it.",
        missing=("brand_id",),
        door="chat_start",
    )
    text = str(exc)
    assert "Install a mandate resolver" not in text, text
    assert "brand_id" in text and "[inputs]" in text and "chat_start" in text, text
    assert exc.sentence and exc.missing == ("brand_id",) and exc.code == "inputs"


def test_a_refusal_with_nothing_missing_says_its_sentence_once() -> None:
    exc = MandateRefused("x.y", code="no_holder", sentence="no rung answers this job.", door="resolve")
    text = str(exc)
    assert "Install a mandate resolver" not in text
    assert text.count("no rung answers this job") == 1 and "Missing" not in text
