"""A DATABASE REFUSAL OF THE MODEL'S OWN VALUES IS NEVER A PLATFORM ERROR (2026-11-11).

Live: ``tool_execution_failed`` rows for ``sql (database): Insert failed. IntegrityError ...
violates check constraint "legal_entity_person_roles_check"`` / ``..._identifier_kind_check`` /
foreign key ``legal_entity_document_document_type_id_fkey``, and ``sql (permission): Schema
'information_schema' is not application data``. The model read each and corrected itself, but
the executor filed every one. SUT: the real ``db_hints`` classifiers, the real executor
predicate and the real ``_agent_db_error`` enrichment. A connection drop is still filed.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_ai.tools import db_hints
from matrx_ai.tools.executor import _is_expected_domain_failure
from matrx_ai.tools.implementations import database as db_tool


class IntegrityError(Exception):
    """Stands in for the ORM wrapper: class name only, no sqlstate."""


CHECK_MSG = 'new row for relation "person_roles" violates check constraint "legal_entity_person_roles_check"'
FK_MSG = 'insert or update on table "d" violates foreign key constraint "legal_entity_document_document_type_id_fkey"'


@pytest.mark.parametrize("exc", [IntegrityError(CHECK_MSG), IntegrityError(FK_MSG), RuntimeError(CHECK_MSG)])
def test_a_constraint_violation_is_a_refusal(exc: Exception) -> None:
    assert db_hints.is_constraint_refusal(exc)
    assert db_tool._db_error_type(exc) == "constraint_violation"
    assert _is_expected_domain_failure(tool_name="sql", error_type=db_tool._db_error_type(exc), message=str(exc))


@pytest.mark.parametrize("exc", [ConnectionResetError("connection was closed"), TimeoutError("query timed out"), RuntimeError("boom")])
def test_an_infrastructure_failure_is_still_filed(exc: Exception) -> None:
    assert not db_hints.is_constraint_refusal(exc)
    assert db_tool._db_error_type(exc) == "database"
    assert not _is_expected_domain_failure(tool_name="sql", error_type="database", message=str(exc))


def test_the_sql_permission_refusal_is_not_filed() -> None:
    assert _is_expected_domain_failure(
        tool_name="sql", error_type="permission", message="Schema 'information_schema' is not application data"
    )


def test_a_check_refusal_names_the_allowed_values(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake(database: str, *, constraint: str) -> list[dict[str, str]]:
        assert constraint == "legal_entity_person_roles_check"
        return [
            {
                "table_schema": "legal",
                "table_name": "person_roles",
                "definition": "CHECK ((role = ANY (ARRAY['officer'::text, 'director'::text])))",
            }
        ]

    import matrx_orm.catalog as catalog

    monkeypatch.setattr(catalog, "describe_check_constraint", fake)
    monkeypatch.setattr(db_tool, "_get_database_name", lambda: "x")
    message, action = asyncio.run(db_tool._agent_db_error(IntegrityError(CHECK_MSG)))
    assert "'officer'" in message and "'director'" in message
    assert "Fix them" in action


@pytest.mark.parametrize(
    "definition",
    [
        "CHECK ((status <> 'deleted'::text))",
        "CHECK ((status !~~ 'x'::text))",
        "CHECK ((code ~ '^[A-Z]{3}$'::text))",
        "CHECK ((kind <> ALL (ARRAY['a'::text, 'b'::text])))",
        "CHECK ((kind <> ALL ('{a,b}'::text[])))",
        "CHECK ((NOT (kind IN ('a', 'b'))))",
    ],
)
def test_only_an_allowed_list_names_allowed_values(definition: str) -> None:
    assert db_hints.allowed_values_from_check(definition) == []


def test_any_array_and_in_forms_name_allowed_values() -> None:
    assert db_hints.allowed_values_from_check(
        "CHECK ((role = ANY (ARRAY['officer'::text, 'director'::text])))"
    ) == ["officer", "director"]
    assert db_hints.allowed_values_from_check("CHECK (kind IN ('a', 'b'))") == ["a", "b"]


class _Pg(Exception):
    def __init__(self, state: str, text: str) -> None:
        super().__init__(text)
        self.sqlstate = state


@pytest.mark.parametrize("state", ["42501", "40001"])
def test_a_permission_or_serialization_failure_still_files(state: str) -> None:
    exc = _Pg(state, "permission denied / could not serialize access")
    assert not db_hints.is_constraint_refusal(exc)
    assert db_tool._db_error_type(exc) == "database"
