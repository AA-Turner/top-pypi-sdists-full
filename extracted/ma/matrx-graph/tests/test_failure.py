"""The structured-failure derivation — matrx_graph.failure.

These tests are written against the REAL failure text measured in the live
``workflow.run.error`` column on 2026-08-20 (144 failed/errored rows), not
against invented examples. Each case below is a verbatim message from that
census, so a regression here is a regression against production.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, Field, ValidationError

from matrx_graph.errors import NodeInputValidationError
from matrx_graph.failure import (
    Cause,
    build_failure,
    failure_from_exception,
    failure_from_text,
    strip_ansi,
)


# ---------------------------------------------------------------------------
# ANSI never reaches the database
# ---------------------------------------------------------------------------


def test_strip_ansi_removes_escaped_and_orphaned_color_codes():
    """Three live rows carry the ORPHANED form (`[91m`, ESC byte already lost
    on the way through str()) — stripping only the escaped form would have
    left them exactly as they are."""
    assert strip_ansi("\x1b[91mred\x1b[0m") == "red"
    assert strip_ansi("[91m Matrx ORM | IntegrityError[0m") == " Matrx ORM | IntegrityError"
    assert strip_ansi("[1;31mred[0m") == "red"


def test_strip_ansi_never_eats_ordinary_bracketed_english():
    """The orphan pattern has no ESC byte to anchor on, so it MUST stay narrow.
    Eating a person's text to tidy a color code is the worse failure."""
    text = "kept [3 items] and [1m ago] and [5m left] and value[10m"
    assert strip_ansi(text) == text


def test_built_failure_is_ansi_free_on_every_string():
    failure = build_failure(
        cause=Cause.PERSISTENCE_FAILED,
        technical="IntegrityError: [91mduplicate key[0m",
        message="[91mSaving failed.[0m",
    )
    assert "[91m" not in (failure.technical or "")
    assert "[91m" not in failure.message


# ---------------------------------------------------------------------------
# The whole point: pydantic already parsed this for us
# ---------------------------------------------------------------------------


class _IngestInput(BaseModel):
    sources: list[str] = Field(min_length=1)


def test_pydantic_validation_error_yields_field_expected_and_got():
    """`ValidationError` literally names ``sources`` and says it wanted at
    least one item. Before this module that was stringified and then guessed
    at with a regex on the other side of the wire."""
    with pytest.raises(ValidationError) as caught:
        _IngestInput(sources=[])

    failure = failure_from_exception(caught.value, step_id="ingest", step_label="Study Pack")

    assert failure.cause == Cause.MISSING_INPUT
    assert failure.field == "sources"
    assert failure.expected == "at least one entry"
    assert failure.step_id == "ingest"
    assert failure.step_label == "Study Pack"
    # The sentence is GENERATED from step_label + field — no pattern was
    # written for Study Pack anywhere.
    assert "Study Pack" in failure.message
    assert "sources" in failure.message
    # The raw text is kept, never dropped.
    assert "ValidationError" in (failure.technical or "")


def test_wrong_type_is_invalid_input_not_missing_input():
    """The two must not collapse: "you left it empty" and "that isn't a list"
    are different sentences and different next steps."""
    with pytest.raises(ValidationError) as caught:
        _IngestInput(sources="not-a-list")

    failure = failure_from_exception(caught.value)
    assert failure.cause == Cause.INVALID_INPUT
    assert failure.field == "sources"


def test_multi_field_validation_keeps_every_problem():
    class _Multi(BaseModel):
        query: str
        count: int

    with pytest.raises(ValidationError) as caught:
        _Multi()  # type: ignore[call-arg]

    failure = failure_from_exception(caught.value)
    assert {p.field for p in failure.fields} == {"query", "count"}
    # `field` is the primary; `fields` is the whole truth.
    assert failure.field in {"query", "count"}


def test_validation_error_wrapped_by_an_engine_error_is_still_unwrapped():
    """Live rows read "ExecutionError: ValidationError: 1 validation error for
    WordCountInput …" — the structure is one hop down __cause__."""
    try:
        try:
            _IngestInput(sources=[])
        except ValidationError as inner:
            raise RuntimeError("Node 'ingest' failed at step 0") from inner
    except RuntimeError as outer:
        failure = failure_from_exception(outer)

    assert failure.cause == Cause.MISSING_INPUT
    assert failure.field == "sources"


# ---------------------------------------------------------------------------
# The engine's own input gate
# ---------------------------------------------------------------------------


def test_node_input_validation_error_field_errors_become_structure():
    """Verbatim from the live census:
    "NodeInputValidationError: The values for 'w6_in' don't match what this
    step asks for: - (value): 'cast_json' is a required property"."""
    exc = NodeInputValidationError(
        "The values for 'w6_in' don't match what this step asks for:",
        node_id="w6_in",
        field_errors=["(value): 'cast_json' is a required property"],
    )
    failure = failure_from_exception(exc, step_label="Cast the voices")

    assert failure.cause == Cause.MISSING_INPUT
    assert failure.field == "cast_json"
    assert failure.got == "nothing"
    # step_id comes off the exception itself when the caller didn't supply one.
    assert failure.step_id == "w6_in"
    assert "Cast the voices" in failure.message


def test_node_id_is_never_used_as_a_step_label():
    """ "n-l4fuKvk13v needs a topic" names nothing the reader recognizes."""
    exc = NodeInputValidationError(
        "bad", node_id="n-l4fuKvk13v", field_errors=["(value): 'topic' is a required property"]
    )
    failure = failure_from_exception(exc)
    assert failure.step_label is None
    assert "n-l4fuKvk13v" not in failure.message


# ---------------------------------------------------------------------------
# Stringified ValidationErrors (old rows, and any layer that flattened early)
# ---------------------------------------------------------------------------


def test_stringified_validation_error_still_yields_fields():
    """Verbatim live message. 26 of 133 rows in the census were dumps like
    this one."""
    text = (
        "Node 'ingest' failed at step 0: 1 validation error for "
        "IngestFromMediaRefsInput\nsources\n  Field required "
        "[type=missing, input_value={}, input_type=dict]\n"
        "    For further information visit https://errors.pydantic.dev/2.11/v/missing"
    )
    failure = failure_from_text(text)
    assert failure.cause == Cause.MISSING_INPUT
    assert failure.field == "sources"
    assert failure.technical == text


def test_too_short_dump_reads_as_missing_not_invalid():
    text = (
        "ValidationError: 1 validation error for IngestFromMediaRefsInput\nsources\n"
        "  List should have at least 1 item after validation, not 0 "
        "[type=too_short, input_value=[], input_type=list]"
    )
    assert failure_from_text(text).cause == Cause.MISSING_INPUT


# ---------------------------------------------------------------------------
# The prose ladder — every entry below is a real live message family
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("message", "expected_cause"),
    [
        (
            "ValueError: this step runs an agent, and an agent run belongs to an organization",
            Cause.NO_ORGANIZATION,
        ),
        (
            "ExecutionError: EducationConsentRequiredError: Education AI generation "
            "refused: COPPA consent required (age_band=None)",
            Cause.CONSENT_REQUIRED,
        ),
        (
            "EdgeRoutingError: edge 'e_plan_kwlines' mapping 'items' could not "
            "resolve against the output of node 'plan'",
            Cause.WIRING_BROKEN,
        ),
        (
            "ExecutionError: Disallowed call target. Only the safe helpers "
            "(abs, all, any, bool, float, int, len, max, min",
            Cause.EXPRESSION_REJECTED,
        ),
        (
            "LessonGenerationError: Outline pass failed: Model claude-sonnet-4-6 "
            "hit token cap (finish_reason='max_tokens')",
            Cause.OUTPUT_TRUNCATED,
        ),
        (
            "Node 'structure' failed at step 1: content.structure failed: Model "
            "failed to produce valid StructuredKnowledge",
            Cause.AI_OUTPUT_UNUSABLE,
        ),
        (
            "NodeFailureError: Node 'call_w1' failed: child_run_errored: "
            "subgraph.call: child run 884d6ee7 ended errored",
            Cause.CHILD_RUN_FAILED,
        ),
        (
            # Live 2026-10-27 (run 6033f4dc): a child's database permission refusal
            # read "out of AI credits" because "Insufficient" in the driver's
            # class name matched the credits rung.
            "Node 'save' failed: child_run_errored: PermissionDeniedError: Permission "
            "denied by the database: permission denied for table kg_chunks  DB error:  "
            "asyncpg.exceptions.InsufficientPrivilegeError: permission denied for table "
            "kg_chunks [SQLSTATE 42501]",
            Cause.NOT_AUTHORIZED,
        ),
        (
            "Error code: 429 - insufficient_quota: You exceeded your current quota",
            Cause.RATE_LIMITED,
        ),
        ("BadRequestError: insufficient credits on this account", Cause.OUT_OF_CREDITS),
    ],
)
def test_prose_ladder_recovers_real_live_message_families(message, expected_cause):
    assert failure_from_text(message).cause == expected_cause


def test_unrecognised_message_is_honestly_generic_and_keeps_the_raw_text():
    """The fallback must never invent a cause — and must never lose the line
    the Expert would hand back to us."""
    failure = failure_from_text("ZeroDivisionError: integer division or modulo by zero")
    assert failure.cause == Cause.ENGINE_ERROR
    assert failure.technical == "ZeroDivisionError: integer division or modulo by zero"
    assert failure.message


# ---------------------------------------------------------------------------
# Stranded runs are OUR failure
# ---------------------------------------------------------------------------


def test_stranded_run_has_its_own_cause_and_never_blames_the_reader():
    from matrx_graph.failure import stranded_failure

    failure = stranded_failure(
        technical=(
            "Force-failed by user — run was stranded in 'running' state. This "
            "usually means the task died without writing its terminal status."
        )
    )
    assert failure.cause == Cause.RUN_STRANDED
    assert "nothing you did" in failure.message
    # The operational detail is kept for us, but it is NOT the headline.
    assert "Force-failed" in (failure.technical or "")
    assert "Force-failed" not in failure.message


# ---------------------------------------------------------------------------
# The persisted shape
# ---------------------------------------------------------------------------


def test_to_column_always_carries_message_for_pre_structure_readers():
    """Every reader that predates the structure looks for ``message`` first
    (the client's errorMessage(), agent_plans, replay). The payload must be a
    strict SUPERSET of what they used to get, never a replacement."""
    payload = failure_from_text("ValueError: boom").to_column()
    assert isinstance(payload["message"], str) and payload["message"]
    assert payload["cause"]
    assert payload["technical"] == "ValueError: boom"
    # Absent facts stay absent rather than persisting a wall of nulls.
    assert "field" not in payload
    assert "fields" not in payload


def test_engine_failure_in_a_step_tells_the_person_what_to_do_never_the_step_label():
    """Live 2026-10-22 (agent_build "Read the request"): the person read "Read the request stopped
    partway through." - engine plumbing, no next move. The fallback line names neither the step nor
    the exception, says what to do, and the technical detail stays on the record."""
    failure = failure_from_text(
        "KeyError: 'cost_parent_request_id'",
        step_id="start",
        step_label="Read the request",
    )
    assert failure.cause == Cause.ENGINE_ERROR
    assert "stopped partway through" not in failure.message
    assert "Read the request" not in failure.message
    assert "KeyError" not in failure.message
    assert "Try again" in failure.message
    assert failure.technical == "KeyError: 'cost_parent_request_id'"


# ---------------------------------------------------------------------------
# The usage gate's refusal is the person's usage limit, never "our side"
# ---------------------------------------------------------------------------

# Verbatim, live 2026-10-24 (Discover run ac8858af, step `detective`): the run
# row said "Something went wrong on our side" (cause engine_error) while every
# node said the account's usage limit was reached.
_LIVE_USAGE_RUN_TEXT = (
    "ExecutionError: FanOutAllItemsFailedError: All 1 item of step 'What the company says about "
    "itself' (detective) failed, so nothing reached the steps after it: UsageLimitReachedError: "
    "You've reached your AI usage limit for now. Upgrade your plan to keep going. ×1 [2 of 3 "
    "invocations in this step completed and are preserved; retry re-runs only the failed one(s)]"
)


def test_a_run_stopped_by_the_usage_limit_says_so():
    failure = failure_from_text(
        _LIVE_USAGE_RUN_TEXT,
        step_id="detective",
        step_label="What the company says about itself",
        error_type="ExecutionError",
    )
    assert failure.cause == Cause.USAGE_LIMIT_REACHED
    assert "usage limit" in failure.message
    assert "our side" not in failure.message
    assert "$" not in failure.message


def test_the_usage_refusal_class_and_code_settle_the_cause_without_prose():
    class UsageLimitReachedError(Exception):
        pass

    assert failure_from_exception(UsageLimitReachedError("x")).cause == Cause.USAGE_LIMIT_REACHED
    for code in ("usage_limit_reached", "guest_ai_allowance_used"):
        assert failure_from_text("refused", error_type=code).cause == Cause.USAGE_LIMIT_REACHED


# ---------------------------------------------------------------------------
# A database permission refusal is access, never money (live 2026-10-27,
# runs efa6d55d + db21bda7: data.record.find on seo.collection_run)
# ---------------------------------------------------------------------------

_LIVE_COLLECTION_RUN_TECHNICAL = (
    "ExecutionError: PermissionDeniedError:\nPermission denied by the database: "
    "permission denied for table collection_run\n  Database:  supabase_automation_matrix\n"
    "  SQLSTATE:  42501\n  DB error:  asyncpg.exceptions.InsufficientPrivilegeError: "
    "permission denied for table collection_run [SQLSTATE 42501] hint=Grant the required "
    "privileges to the current role with: GRANT SELECT ON seo.collection_run TO authenticated;"
)


def test_live_collection_run_permission_text_names_the_table_not_credits():
    failure = failure_from_text(_LIVE_COLLECTION_RUN_TECHNICAL, step_id="model")
    assert failure.cause == Cause.NOT_AUTHORIZED
    assert failure.message == "This step can't read seo.collection_run with your access."
    assert "credit" not in failure.message.lower()


def test_real_asyncpg_insufficient_privilege_exception_is_not_authorized():
    import asyncpg

    exc = asyncpg.exceptions.InsufficientPrivilegeError("permission denied for table credit_balance")
    failure = failure_from_exception(exc)
    assert failure.cause == Cause.NOT_AUTHORIZED
    assert "credit_balance" in failure.message


def test_permission_refusal_on_a_credit_named_table_is_still_access():
    failure = failure_from_text("permission denied for table credit_balances [SQLSTATE 42501]")
    assert failure.cause == Cause.NOT_AUTHORIZED
    assert failure.message == "This step can't reach credit_balances with your access."


def test_a_genuine_credits_error_still_maps_to_credits():
    failure = failure_from_text("BadRequestError: Your credit balance is too low to access the API")
    assert failure.cause == Cause.OUT_OF_CREDITS
    assert failure.message == "This workspace is out of AI credits."


def test_a_raised_spend_refusal_keeps_its_approval_link():
    """A step that RAISES the gate's refusal (an action under tool.call) carries the refusal's own
    ``approval_url`` onto the run's failure, so the person gets the Approve link (2026-10-27 review)."""
    from matrx_graph.failure import failure_from_exception

    class RunApprovalRequiredError(Exception):
        is_caller_refusal = True

        def __init__(self) -> None:
            super().__init__("This agent waits for an administrator to approve it.")
            self.approval_url = "https://manage.aimatrx.com/admin/approvals/a-1"

    try:
        try:
            raise RunApprovalRequiredError()
        except RunApprovalRequiredError as inner:
            raise RuntimeError("tool.call → research: the action failed") from inner
    except RuntimeError as wrapped:
        outer = wrapped
    for exc in (RunApprovalRequiredError(), outer):
        got = failure_from_exception(exc, step_id="research")
        assert got.cause == "spend_approval_required", got.to_column()
        assert got.approval_url == "https://manage.aimatrx.com/admin/approvals/a-1", got.to_column()


def test_an_exception_raised_while_handling_a_refusal_is_not_that_refusal():
    """Only explicit wrapping (``raise ... from``) carries the refusal's approval link, never ``__context__``."""
    from matrx_graph.failure import failure_from_exception

    class RunApprovalRequiredError(Exception):
        is_caller_refusal = True
        approval_url = "https://manage.aimatrx.com/admin/approvals/a-2"

    try:
        try:
            raise RunApprovalRequiredError("held")
        except RunApprovalRequiredError:
            raise KeyError("an unrelated bug in the handler")  # noqa: B904 — the point of the test
    except KeyError as unrelated:
        got = failure_from_exception(unrelated, step_id="s")
    assert got.approval_url is None and got.cause != "spend_approval_required", got.to_column()
