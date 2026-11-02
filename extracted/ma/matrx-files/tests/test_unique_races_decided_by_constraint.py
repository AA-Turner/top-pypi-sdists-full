"""The unique-race classifiers read SQLSTATE 23505 + the constraint name, never the words.

The old text match needed "23505"/"unique"/"duplicate key" in the rendered message; an ORM
IntegrityError raised `from None` with other words slipped past it and a benign race
became a hard failure. Guard: scripts/check_no_db_error_text_matching.py.
"""

from __future__ import annotations

import asyncpg
from matrx_orm import IntegrityError

from matrx_files.cloud_sync.sync_engine import SyncEngine
from matrx_files.cloud_sync.versioning import _is_version_unique_violation
from matrx_files.dedup import is_dedup_unique_violation

WORDS = "conflicto: la fila ya está"


def _unique(constraint: str) -> IntegrityError:
    driver = asyncpg.exceptions.UniqueViolationError(WORDS)
    err = IntegrityError(constraint="unique", original_error=driver, constraint_name=constraint)
    err.__suppress_context__ = True
    return err


def test_dedup_canonical_race() -> None:
    assert is_dedup_unique_violation(_unique("cld_files_dedup_canonical"))
    assert SyncEngine._is_dedup_unique_violation(_unique("cld_files_dedup_canonical"))
    assert not is_dedup_unique_violation(_unique("cld_files_owner_id_file_path_key"))
    assert not is_dedup_unique_violation(RuntimeError("23505 cld_files_dedup_canonical"))


def test_path_race() -> None:
    assert SyncEngine._is_path_unique_violation(_unique("cld_files_owner_id_file_path_key"))
    assert not SyncEngine._is_path_unique_violation(_unique("cld_files_dedup_canonical"))


def test_version_race() -> None:
    assert _is_version_unique_violation(_unique("cld_file_versions_file_id_version_number_key"))
    assert _is_version_unique_violation(_unique("file_versions_file_id_version_number_key"))
    assert not _is_version_unique_violation(_unique("something_else_key"))
