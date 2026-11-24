"""A 42501 raised by a database GUARD (a trigger RAISE naming the rule and the right door) reaches the
model in the database's own words, and is a correctable refusal — never "your access level doesn't
permit ... requires super_admin", and never filed as a platform fault.

Live: system_error a6e69644 (2026-11-13) — ``UPDATE files.files SET parent_folder_id`` refused by
``files.guard_rename_path_columns`` ("written ONLY by public.move_file"); the sql tool told the model
it lacked access and the call was filed as tool_execution_failed.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools import db_hints
from matrx_ai.tools.implementations import database

GUARD = ("parent_folder_id on files.files is written ONLY by public.move_file (row). The ONE exception "
         "this trigger allows is back-filling a NULL pointer.")


class InsufficientPrivilegeError(Exception):  # the asyncpg class, by name
    sqlstate = "42501"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class PermissionDeniedError(Exception):  # the matrx-orm wrapper, raised ``from None``
    def __init__(self, original_error: BaseException) -> None:
        super().__init__("\x1b[31mMatrx ORM | PermissionDeniedError\x1b[0m")
        self.original_error = original_error


def _orm_wrapped(message: str) -> BaseException:
    try:
        try:
            raise InsufficientPrivilegeError(message)
        except InsufficientPrivilegeError as e:
            raise PermissionDeniedError(e) from None
    except PermissionDeniedError as wrapped:
        return wrapped


@pytest.mark.asyncio
async def test_a_guard_refusal_reaches_the_model_in_the_databases_words() -> None:
    exc = _orm_wrapped(GUARD)
    assert db_hints.guard_refusal_text(exc) == GUARD
    message, suggested = await database._agent_db_error(exc)
    assert "public.move_file" in message
    assert "super_admin" not in message
    assert database._db_error_type(exc) == db_hints.CONSTRAINT_REFUSAL_ERROR_TYPE


@pytest.mark.asyncio
async def test_a_real_privilege_or_rls_denial_keeps_the_access_message() -> None:
    for text in ("permission denied for table files", 'new row violates row-level security policy for table "files"'):
        exc = _orm_wrapped(text)
        assert db_hints.guard_refusal_text(exc) is None
        message, _ = await database._agent_db_error(exc)
        assert "access level" in message
        assert database._db_error_type(exc) == "database"
