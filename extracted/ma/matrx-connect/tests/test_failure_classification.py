"""The streaming crash path must not blame the user or invent an error type.

Live incident (2026-08-17): ``agent.slot_definition`` was renamed to
``agent.mandate`` in the shared database while the deployed build still queried
the old name. A user's vision interview died and the browser received:

    error_type:   "visioninterview:72175649_error"   (a NEW type per session)
    user_message: "…failed unexpectedly. Please try again or adjust your settings."
    message:      "\\u001b[91m\\n---- Matrx ORM | SchemaMismatchError (table) …"

Three defects in one payload: an ungroupable type, a message telling a
non-technical user to fix settings they did not break, and raw ANSI-colored
operator output. These tests pin all three.
"""

from __future__ import annotations

from matrx_connect.streaming.failure_classification import (
    classify_infrastructure_failure,
    stable_error_type,
    strip_ansi,
)


# ── error_type must identify the FAILURE CLASS, never the run ───────────────


def test_session_id_is_stripped_from_the_error_type() -> None:
    """The exact label from the incident."""
    assert stable_error_type("VisionInterview:72175649") == "visioninterview_error"


def test_full_uuid_is_stripped() -> None:
    assert (
        stable_error_type("Research:3fc5420f-1e92-4bef-8a05-311d0f853e79")
        == "research_error"
    )


def test_two_sessions_of_the_same_feature_share_one_error_type() -> None:
    """This is the whole point — one class, one type, countable."""
    assert stable_error_type("VisionInterview:72175649") == stable_error_type(
        "VisionInterview:aabbccdd"
    )


def test_label_without_an_id_is_unchanged_in_meaning() -> None:
    assert stable_error_type("ResearchSearch") == "researchsearch_error"


def test_label_that_is_only_an_id_still_produces_a_name() -> None:
    """Never degrade to a bare '_error' — that is worse than the id."""
    assert stable_error_type("72175649") == "72175649_error"


# ── infrastructure failures are named, and never blamed on the user ─────────


class SchemaMismatchError(Exception):
    """Stand-in for matrx-orm's error — matrx-connect classifies by NAME
    because it must not depend on matrx-orm (package boundary)."""


class UndefinedTableError(Exception):
    pass


def test_schema_mismatch_is_classified() -> None:
    failure = classify_infrastructure_failure(SchemaMismatchError("relation missing"))
    assert failure is not None
    assert failure.error_type == "database_schema_mismatch"


def test_infrastructure_message_never_tells_the_user_to_change_settings() -> None:
    """The regression that actually reached a human."""
    failure = classify_infrastructure_failure(UndefinedTableError("42P01"))
    assert failure is not None
    lowered = failure.user_message.lower()
    assert "settings" not in lowered
    assert "nothing you did" in lowered


def test_a_wrapped_cause_still_classifies() -> None:
    """A service that wraps the DB error in its own type must not
    reintroduce the anonymous failure."""
    try:
        try:
            raise UndefinedTableError("relation 'agent.slot_definition' does not exist")
        except UndefinedTableError as inner:
            raise RuntimeError("slot resolution failed") from inner
    except RuntimeError as outer:
        failure = classify_infrastructure_failure(outer)

    assert failure is not None
    assert failure.error_type == "database_schema_mismatch"


def test_an_ordinary_bug_is_left_unclassified() -> None:
    """Only infrastructure gets the 'not your fault' message. A genuine
    application bug must NOT be laundered into 'try again in a moment'."""
    assert classify_infrastructure_failure(ValueError("bad input")) is None


def test_cyclic_cause_chain_terminates() -> None:
    a = RuntimeError("a")
    b = RuntimeError("b")
    a.__cause__ = b
    b.__cause__ = a
    assert classify_infrastructure_failure(a) is None


# ── nothing client-bound carries terminal escapes ──────────────────────────


def test_ansi_escapes_are_stripped() -> None:
    raw = "\x1b[91m\nMatrx ORM  |  SchemaMismatchError (table)\n\x1b[0m"
    cleaned = strip_ansi(raw)
    assert "\x1b" not in cleaned
    assert "SchemaMismatchError" in cleaned  # diagnostics preserved


def test_strip_ansi_is_idempotent() -> None:
    raw = "\x1b[91mred\x1b[0m"
    assert strip_ansi(strip_ansi(raw)) == strip_ansi(raw)


# ── the mandate contract family (2026-08-27 incident) ───────────────────────
#
# Every ``pdf.content_cleaner`` run refused on a broken Provision promise and
# reached the browser as ``pdfclean_error`` with "Please try again or adjust
# your settings." — one error type per ROUTE for one failure class, and advice
# no user could act on. Same three defects as the 2026-08-17 incident above,
# one family over.


class BrokenOfferPromise(ValueError):
    """Stand-in for matrx_ai.mandates — classified by NAME, never imported."""


class ProvisionInputError(ValueError):
    """Stand-in for aidream.services.mandates.provisions."""


class MandateResolutionUnavailable(RuntimeError):
    """Stand-in for matrx_ai.mandates."""


def test_broken_offer_promise_is_a_named_failure_class() -> None:
    failure = classify_infrastructure_failure(
        BrokenOfferPromise("guaranteed offered value(s) ['content'] were not supplied")
    )
    assert failure is not None
    assert failure.error_type == "mandate_contract_broken"


def test_provision_input_error_shares_that_class() -> None:
    """One failure class, one type — countable across every route."""
    a = classify_infrastructure_failure(BrokenOfferPromise("x"))
    b = classify_infrastructure_failure(ProvisionInputError("x"))
    assert a is not None and b is not None
    assert a.error_type == b.error_type


def test_unresolvable_mandate_is_its_own_named_class() -> None:
    failure = classify_infrastructure_failure(MandateResolutionUnavailable("x"))
    assert failure is not None
    assert failure.error_type == "mandate_unresolved"


def test_mandate_failures_never_tell_the_user_to_adjust_settings() -> None:
    """The cause is a code-side contract disagreement. No setting fixes it."""
    for exc in (
        BrokenOfferPromise("x"),
        ProvisionInputError("x"),
        MandateResolutionUnavailable("x"),
    ):
        failure = classify_infrastructure_failure(exc)
        assert failure is not None
        assert "adjust your settings" not in failure.user_message
        assert "Nothing you did caused it" in failure.user_message


def test_a_wrapped_mandate_failure_still_classifies() -> None:
    """A service that re-raises its own type must not re-anonymize the cause."""

    class ServiceError(RuntimeError):
        pass

    try:
        try:
            raise BrokenOfferPromise("x")
        except BrokenOfferPromise as cause:
            raise ServiceError("pdf cleanup failed") from cause
    except ServiceError as exc:
        failure = classify_infrastructure_failure(exc)

    assert failure is not None
    assert failure.error_type == "mandate_contract_broken"


def test_a_missing_database_function_is_a_schema_mismatch() -> None:
    """Live 2026-10-22: a call shape no overload matched reached a person as
    "DataFetch failed unexpectedly (UndefinedFunctionError)"."""

    class UndefinedFunctionError(Exception):
        pass

    failure = classify_infrastructure_failure(UndefinedFunctionError("function x(jsonb) does not exist"))
    assert failure is not None
    assert failure.error_type == "database_schema_mismatch"


def test_the_unclassified_crash_sentence_names_no_class_or_label() -> None:
    from matrx_connect.streaming.failure_classification import GENERIC_CRASH_MESSAGE

    assert "Error" not in GENERIC_CRASH_MESSAGE
    assert "settings" not in GENERIC_CRASH_MESSAGE
    assert "unexpectedly" not in GENERIC_CRASH_MESSAGE
