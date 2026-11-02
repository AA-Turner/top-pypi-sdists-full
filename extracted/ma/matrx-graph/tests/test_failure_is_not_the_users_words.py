"""A failure is classified by its CLASS, never by what the person wrote.

THE LIVE FAILURE this file replays: workflow run
``053e8b72-be54-4775-960f-c180c8b0e0d2`` ("Newsroom Desk", definition
9c12787a-d62e-4141-80fb-f92a088ced16) failed 2026-09-12 21:27:39Z. It died on a
matrx-orm ``QueryTimeoutError`` writing its 1.1 MB step-3 ``workflow.checkpoint``
row, and the Expert was shown:

    "This account needs an age check before AI can run."   (cause consent_required)

The technical text persisted in ``workflow.run.error`` is 309,687 characters: the
ORM renders the statement's ``Args:`` — which were the ``n_map`` fan-out's
per-item ``document`` inputs — and one of those documents quoted
*"legislatures are ultimate guardians of the liberties and welfare of the
people"* at offset 86,379. The message ladder's first rung is
``coppa|consent[_ ]required|guardian|age[_ ]undeclared``.

The strings below are VERBATIM slices of that row, read back with the Supabase
MCP on 2026-09-12 (``select error->>'technical' …``), not invented examples.
"""

from __future__ import annotations

from matrx_graph.failure import (
    CLASSIFY_TEXT_LIMIT,
    Cause,
    classification_text,
    failure_from_exception,
    failure_from_text,
)
from matrx_graph.workers.queue import FailureClass, classify_failure

# ---------------------------------------------------------------------------
# The live text (trimmed to what the test needs; every character is real)
# ---------------------------------------------------------------------------

_LIVE_HEAD = (
    "QueryTimeoutError: \n"
    + "-" * 80
    + "\nMatrx ORM  |  QueryTimeoutError\n\n"
    "Query timed out during execute_query\n"
    "  Operation: execute_query\n"
    "  Query:     INSERT INTO workflow.checkpoint (id, run_id, thread_id, "
    "parent_checkpoint_id, step, channel_values, next_invocations, metadata, "
    "created_at, pending_bindings, version) VALUES ($1, $2, $3, $4, $5, $6, $7, "
    "$8, $9, $10, $11) RETURNING *\n"
)

# What follows "Args:" is the RUN'S DATA — the fan-out's document inputs.
_LIVE_ARGS_WITH_USER_DOCUMENTS = (
    "  Args:      ('8db59518-cb32-4260-9eb5-961b12c95a42', "
    "'053e8b72-be54-4775-960f-c180c8b0e0d2', "
    "'053e8b72-be54-4775-960f-c180c8b0e0d2', "
    "'81a13221-1eb3-49e5-9951-27d1942fe426', 3, '{}', "
    '\'[{"node_id": "n_doc_ledger", "inputs": {"form": "Analysis", "document": '
    '"LABEL: DOCUMENT 1 — First Amended Complaint and Jury Demand … the '
    "vindication of constitutional interests such as those embraced by the "
    "Fourth Amendment . To be sure, 'it must be remembered that legislatures "
    "are ultimate guardians of the liberties and welfare of the people in quite "
    "as great a degree as the courts.' Missouri, Kansas & Texas R. Co. of Texas "
    'v. May, 194 U.S. 267 …"}}]\'\n'
)

_LIVE_HINT_TAIL = (
    "\nHint:\n"
    "  - The query held a connection but didn't return inside command_timeout.\n"
    "  - Write query (INSERT).\n"
    "  - NOT safe to retry blindly — a write may have ambiguous completion, and\n"
    "    an unchanged lock convoy will time out again.\n" + "-" * 80 + "\n"
)

LIVE_TECHNICAL = _LIVE_HEAD + _LIVE_ARGS_WITH_USER_DOCUMENTS + _LIVE_HINT_TAIL

#: The sentence the Expert actually saw. It must never come back.
THE_LIE = "This account needs an age check before AI can run."


class _FakeQueryTimeoutError(Exception):
    """Stands in for ``matrx_orm.exceptions.QueryTimeoutError``.

    matrx-graph's tests must pass with matrx-orm absent, so the class is
    synthesized with the real module path and name — which is exactly what the
    classifier keys on.
    """

    __module__ = "matrx_orm.exceptions"
    __qualname__ = "QueryTimeoutError"


_FakeQueryTimeoutError.__name__ = "QueryTimeoutError"


# ---------------------------------------------------------------------------
# The regression: the run that lied
# ---------------------------------------------------------------------------


def test_live_checkpoint_timeout_is_not_reported_as_an_age_check():
    """The exact live text, through the exact path that produced the lie."""
    failure = failure_from_text(LIVE_TECHNICAL)
    assert failure.cause != Cause.CONSENT_REQUIRED
    assert failure.cause == Cause.PERSISTENCE_FAILED
    assert failure.message != THE_LIE
    assert "age check" not in failure.message
    # The technical text keeps the real reason but NOT the statement's bound
    # args: ``technical`` is persisted to ``workflow.run.error`` and rendered by
    # clients, and those args were the run's own documents (309 KB of them).
    # Since 2026-09-17 the full render goes to the log only — see
    # tests/test_client_bound_error_redaction.py.
    assert failure.technical is not None
    assert "Query timed out" in failure.technical
    assert "ultimate guardians" not in failure.technical
    assert "Args:" not in failure.technical


def test_live_checkpoint_timeout_from_the_exception_is_persistence():
    exc = _FakeQueryTimeoutError(LIVE_TECHNICAL)
    failure = failure_from_exception(exc, step_id="n_map", step_label="Document Ledger")
    assert failure.cause == Cause.PERSISTENCE_FAILED
    assert failure.error_type == "QueryTimeoutError"
    assert failure.message != THE_LIE


def test_any_matrx_orm_exception_classifies_by_module_not_prose():
    """An ORM error class nobody listed still lands on persistence."""
    klass = type("SomeBrandNewOrmError", (Exception,), {"__module__": "matrx_orm.exceptions"})
    failure = failure_from_exception(klass("consent_required guardian coppa"))
    assert failure.cause == Cause.PERSISTENCE_FAILED


# ---------------------------------------------------------------------------
# The rule the fix installs
# ---------------------------------------------------------------------------


def test_classification_text_never_returns_the_payload():
    safe = classification_text(LIVE_TECHNICAL)
    assert "guardians" not in safe
    assert "Args:" not in safe
    assert "Query timed out during execute_query" in safe
    assert len(safe) <= CLASSIFY_TEXT_LIMIT


def test_classification_text_is_bounded():
    assert len(classification_text("x" * (CLASSIFY_TEXT_LIMIT * 3))) == CLASSIFY_TEXT_LIMIT


def test_classification_text_keeps_a_first_line_that_starts_with_a_marker():
    """A message that opens WITH a marker must still classify on something."""
    assert classification_text("Args: whatever\nmore").strip() == "Args: whatever"


def test_a_real_consent_refusal_still_classifies_as_consent():
    """The rung is not weakened — it just no longer reads the person's documents."""
    failure = failure_from_text(
        "EducationConsentRequiredError: consent_required — age_undeclared for this learner"
    )
    assert failure.cause == Cause.CONSENT_REQUIRED


# ---------------------------------------------------------------------------
# The same class of mistake in the worker's retry decision
# ---------------------------------------------------------------------------


def test_queue_disposition_ignores_payload_words():
    """A document containing "connection refused" must not decide retryability."""
    exc = Exception(
        "ValueError: the step could not be prepared\n"
        "  Args:      ('the witness stated the connection refused to reset', )"
    )
    assert classify_failure(exc).failure_class is FailureClass.TERMINAL


def test_queue_disposition_still_retries_a_real_transient_message():
    exc = Exception("sending request failed: connection reset by peer")
    assert classify_failure(exc).failure_class is FailureClass.RETRYABLE
