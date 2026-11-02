"""A job that refuses its VALUES names them — it never says "no AI assigned" (2026-10-27).

Live: run d92b06b3 (Who buys) refused because the value ``charter`` was not given, and the person
read "Who buys (mandate) has no AI assigned to do the job." — the prose ladder matched the bare
word "mandate", so every refusal that merely mentioned a mandate (a missing value, a wrong shape,
a template path, a wiring mistake) sent the reader to the agent binding. The texts below are the
live refusal texts, verbatim in their load-bearing part.
"""

from __future__ import annotations

import pytest

from matrx_graph.failure import Cause, failure_from_exception, failure_from_text

_GUARANTEED_MISSING = (
    "ExecutionError: MandateResolutionError: Mandate 'seo.ai_visibility_evidence_icp': Provision "
    "'seo.ai_visibility_evidence_icp': this run cannot start on the values it was given — charter: "
    "guaranteed offered value was not supplied by the call site — a guaranteed value is a promise; "
    "the run refuses rather than let the agent answer about something it was never given "
    "[3 of 4 invocations in this step completed and are preserved; retry re-runs only the failed one(s)]"
)
_HOLDER_INPUTS_MISSING = (
    "ExecutionError: MandateResolutionError: Mandate 'seo.ai_visibility_evidence_icp': the agent that "
    "runs this job did not get every value it requires: url: this job guarantees this value on every "
    "call, so the run refuses without it; description: this job guarantees this value on every call, "
    "so the run refuses without it. The binding that fulfils this job feeds nothing into the agent."
)
_WRONG_SHAPE = (
    "MandateResolutionError: Mandate 'agent_factory.instructions': Provision "
    "'agent_factory.instructions_step': this run cannot start on the values it was given — "
    "sample_inputs: expected a string (text)"
)


def test_a_missing_guaranteed_value_is_a_missing_input_that_names_it() -> None:
    failure = failure_from_text(_GUARANTEED_MISSING, step_label="Who buys")
    assert failure.cause == Cause.MISSING_INPUT
    assert failure.field == "charter"
    assert "charter" in failure.message
    assert "no AI assigned" not in failure.message


def test_every_missing_value_is_named_in_the_one_sentence() -> None:
    failure = failure_from_text(_HOLDER_INPUTS_MISSING, step_label="Who buys")
    assert failure.cause == Cause.MISSING_INPUT
    assert [p.field for p in failure.fields] == ["url", "description"]
    assert "“url”" in failure.message and "“description”" in failure.message


def test_a_wrong_shaped_value_is_an_invalid_input_that_names_it() -> None:
    failure = failure_from_text(_WRONG_SHAPE, step_label="Write")
    assert failure.cause == Cause.INVALID_INPUT
    assert failure.field == "sample_inputs"
    assert "a string (text)" in (failure.expected or "")


def test_a_raised_refusal_reads_the_same_as_its_text() -> None:
    class ExecutionError(RuntimeError):
        pass

    failure = failure_from_exception(
        ExecutionError(_GUARANTEED_MISSING.removeprefix("ExecutionError: ")), step_label="Who buys"
    )
    assert failure.cause == Cause.MISSING_INPUT
    assert failure.field == "charter"


@pytest.mark.parametrize(
    ("text", "cause"),
    [
        (
            "TemplatePathMissing: template path '$item.once_key' does not resolve for item 0: segment "
            "'once_key' is missing. Item 0 is an object with keys ['index', 'item_key', 'mandate_key']",
            Cause.WIRING_BROKEN,
        ),
        (
            "ValueError: ai.mandate.start:write (mandate 'x.y') was fed ['column'] outside "
            "provision_values. A Run Mandate step hands the mandate its state",
            Cause.WIRING_BROKEN,
        ),
        (
            "UnresolvedInputError: Node 'take' references workflow input 'mandate_key' but no value "
            "landed for this run and it has no default.",
            Cause.MISSING_INPUT,
        ),
    ],
)
def test_the_word_mandate_alone_is_not_evidence_of_no_ai(text: str, cause: str) -> None:
    assert failure_from_text(text, step_label="Step").cause == cause


@pytest.mark.parametrize(
    "text",
    [
        "MandateRefused: Mandate 'a.b' (workflow_step) could not be resolved: Mandate 'a.b': not "
        "found in mandate.* — declare it",
        "ExecutionError: MandateResolutionError: Mandate 'a.b': names provision 'a.c' which no code "
        "in this process declares — its input contract cannot be applied",
    ],
)
def test_a_real_resolution_refusal_still_says_no_ai(text: str) -> None:
    assert failure_from_text(text, step_label="Step").cause == Cause.MANDATE_UNRESOLVED


@pytest.mark.parametrize(
    ("text", "cause"),
    [
        (
            "MandateError: Mandate 'meet.wrap_up': Meet Wrap-Up Composer could not finish this job: "
            "This agent made many paid calls in the last hour, so its runs are paused until that "
            "hour's volume drops. An administrator can also approve it.",
            Cause.SPEND_APPROVAL_REQUIRED,
        ),
        (
            "MandateError: Mandate 'x.y': Writer could not finish this job: This agent is waiting for "
            "an administrator to approve its spending, so it was not run.",
            Cause.SPEND_APPROVAL_REQUIRED,
        ),
        (
            "MandateError: Mandate 'x.y': Writer could not finish this job: This model is limited to "
            "approved accounts (Claude Opus). Not run; no other model was used.",
            Cause.MODEL_NOT_APPROVED,
        ),
        (
            "TopTierModelRefusedError: This model is limited to approved accounts (Claude Opus).",
            Cause.MODEL_NOT_APPROVED,
        ),
    ],
)
def test_a_model_or_volume_refusal_inside_a_mandate_error_keeps_its_honest_cause(
    text: str, cause: str
) -> None:
    failure = failure_from_text(text, step_label="Wrap up")
    assert failure.cause == cause
    assert "no AI assigned" not in failure.message


@pytest.mark.parametrize(
    "text",
    [
        "AI turn ended with status 'failed' (automation_guardrail): Refused: paused by its guardrail — "
        "Refused: retry storm — this automation was refused 5 times in 10 minutes on the same input "
        "(limit 5). It is paused; fix why it repeats, then resume it.",
        "Refused: retry storm — this automation failed 6 times in 24 hours on the same input "
        "(limit 5). It is paused; fix why it fails, then resume it.",
    ],
)
def test_a_paused_automation_says_so_not_an_engine_error(text: str) -> None:
    failure = failure_from_text(text, step_label="Wrap up")
    assert failure.cause == "automation_paused"
    assert "paused" in failure.message
