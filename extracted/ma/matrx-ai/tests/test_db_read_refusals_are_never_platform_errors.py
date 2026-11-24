"""A ``db_read`` refusal the model corrects is never a ``tool_execution_failed`` system_error.

Red before (2026-11-17): db_read's up-front refusals (pg_catalog / information_schema / auth,
credential tables) carried ``permission`` but only ``("sql", "permission")`` was expected; a
42501 privilege / RLS denial and a ``relation ... does not exist`` miss were typed ``database``.
All three reached operations as platform faults. A real database fault still files."""

from __future__ import annotations

from matrx_orm.operations.catalog_select import RelationNotReadableError, UnregisteredRelationError

from matrx_ai.tools.executor import _is_expected_domain_failure
from matrx_ai.tools.implementations.database import _db_error_type


class _Denied(Exception):
    sqlstate = "42501"


def test_a_privilege_or_rls_denial_is_a_permission_refusal() -> None:
    assert _db_error_type(_Denied('permission denied for table "x"'), under_rls=True) == "permission"
    assert _db_error_type(RelationNotReadableError("runtime", "_ai_usage_calls"), under_rls=True) == "permission"
    # On the privileged path a 42501 is a missing grant: still a fault.
    assert _db_error_type(_Denied('permission denied for table "x"')) == "database"


def test_a_relation_miss_is_the_callers_to_correct() -> None:
    assert _db_error_type(UnregisteredRelationError('relation "runtime.nope" does not exist')) == "validation"


def test_a_real_database_fault_is_still_a_fault() -> None:
    assert _db_error_type(ConnectionError("pool closed")) == "database"
    assert not _is_expected_domain_failure(tool_name="db_read", error_type="database")


def test_db_read_refusals_are_never_filed() -> None:
    for error_type in ("permission", "validation"):
        assert _is_expected_domain_failure(tool_name="db_read", error_type=error_type), error_type
