"""A NOT NULL on a DB-inherited column is a race, not a verdict on the row.

SUT: :func:`matrx_ai.persistence.replay.is_permanent_failure_text`.

Live evidence (2026-09-17, ``seo.page_mapper``). ``chat.request`` payloads never
carry an ``organization_id`` — ``platform.inherit_org_from_parent`` reads it off
the row's ``chat.conversation`` parent on INSERT — and
``cx_request_conversation_id_fkey`` is DEFERRABLE INITIALLY DEFERRED. So when
the parent conversation is itself still sitting unrecovered in
``system_write_failure``, the BEFORE-INSERT trigger finds no parent, leaves the
column NULL, and the NOT NULL fires FIRST. The deferred FK — the constraint that
would have named the real problem and been classified a recoverable race — never
gets to speak.

Three ``chat.request`` rows were refused exactly this way at 16:59, 17:00 and
17:01. Every one of their parent conversations was written at 17:02, 60–180
seconds later and far inside ``FK_RACE_MAX_AGE_SECONDS``. All three would have
inserted cleanly on the next sweep. Because ``NotNullViolationError`` is in
``PERMANENT_FAILURE_SIGNATURES``, all three were quarantined on sight and
$0.134860 of already-billed model work was lost from the cost ledger for good.

Breaks this test name: the inherited-column carve-out removed (paid work is
discarded again on a transient parent gap), or the carve-out widened into a
blanket NOT NULL pardon (a genuinely malformed row would then retry instead of
being quarantined on sight).
"""

from __future__ import annotations

import pytest
from matrx_orm.session.fallback import DISK_SPILL_RECOVERED_MARKER

from matrx_ai.persistence import replay

# The refusal exactly as describe_db_exception renders it for the live rows.
_INHERITED_ORG_NOTNULL = (
    "asyncpg.exceptions.NotNullViolationError: null value in column "
    '"organization_id" of relation "request" violates not-null constraint '
    "[SQLSTATE 23502]"
)


def test_the_inherited_org_notnull_is_recoverable() -> None:
    """The exact live refusal must NOT be quarantined on sight."""
    assert not replay.is_permanent_failure_text(_INHERITED_ORG_NOTNULL)


def test_it_is_recoverable_through_the_spill_marker_too() -> None:
    """The same verdict when the text arrives wrapped by the disk-spill lane."""
    wrapped = f"{DISK_SPILL_RECOVERED_MARKER}: {_INHERITED_ORG_NOTNULL}"
    assert not replay.is_permanent_failure_text(wrapped)


def test_the_dedicated_predicate_recognises_it() -> None:
    assert replay.is_inherited_column_notnull_text(_INHERITED_ORG_NOTNULL)


@pytest.mark.parametrize(
    "text",
    [
        # A genuinely malformed row: a NOT NULL on a column NOBODY inherits.
        # No parent's arrival will ever fill it, so it stays permanent.
        'asyncpg.exceptions.NotNullViolationError: null value in column "content" '
        'of relation "cx_message" violates not-null constraint [SQLSTATE 23502]',
        'asyncpg.exceptions.NotNullViolationError: null value in column "status" '
        'of relation "cx_user_request" violates not-null constraint [SQLSTATE 23502]',
    ],
)
def test_other_notnull_refusals_stay_permanent(text: str) -> None:
    """The carve-out is for inherited columns only — not a blanket NOT NULL pardon."""
    assert replay.is_permanent_failure_text(text)


def test_the_carve_out_does_not_leak_into_other_classes() -> None:
    """A non-NOT-NULL error that merely mentions the column stays permanent."""
    check_violation = (
        "asyncpg.exceptions.CheckViolationError: new row for relation "
        '"request" violates check constraint "organization_id_present" '
        "[SQLSTATE 23514]"
    )
    assert replay.is_permanent_failure_text(check_violation)
    assert not replay.is_inherited_column_notnull_text(check_violation)
