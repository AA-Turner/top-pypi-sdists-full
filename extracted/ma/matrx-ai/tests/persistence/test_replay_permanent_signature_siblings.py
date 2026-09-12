"""Sibling deterministic refusals are quarantined like the P0001 case.

SUT: :func:`matrx_ai.persistence.replay.is_permanent_failure_text`.

Review evidence (2026-09-12): the migrations that RAISE P0001 also RAISE with
explicit ERRCODEs P0002 / 28000 / 42501, and 0178 RAISEs with the
foreign_key_violation code for a business-rule refusal. asyncpg maps each to a
class whose name never contains "RaiseError", so the original signature list
let every one of them burn five attempts and file five rows.

Breaks these tests name: a sibling errcode dropped from the list (the row is
retried again), or the fake-FK guard classified recoverable because it wears
the FK class.
"""

from __future__ import annotations

import pytest
from matrx_orm.session.fallback import DISK_SPILL_RECOVERED_MARKER

from matrx_ai.persistence import replay


@pytest.mark.parametrize(
    "text",
    [
        f"{DISK_SPILL_RECOVERED_MARKER}: asyncpg.exceptions.NoDataFoundError: message_not_found [SQLSTATE P0002]",
        "asyncpg.exceptions.InvalidAuthorizationSpecificationError: no_session [SQLSTATE 28000]",
        "asyncpg.exceptions.InsufficientPrivilegeError: not the owner [SQLSTATE 42501]",
        "asyncpg.exceptions.ForeignKeyViolationError: agent definition references missing tool ids: {a} [SQLSTATE 23503]",
        "asyncpg.exceptions.ForeignKeyViolationError: tool 1 is referenced by an agent definition [SQLSTATE 23503]",
    ],
)
def test_sibling_refusals_are_permanent(text: str) -> None:
    assert replay.is_permanent_failure_text(text)


def test_a_real_parent_ordering_fk_race_stays_recoverable() -> None:
    text = (
        'asyncpg.exceptions.ForeignKeyViolationError: insert or update on table "cx_message" '
        'violates foreign key constraint "cx_message_conversation_id_fkey" [SQLSTATE 23503]'
    )
    assert not replay.is_permanent_failure_text(text)
