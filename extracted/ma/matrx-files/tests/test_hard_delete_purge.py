"""Regression — hard-delete purges every S3 object (no C10 orphan leak).

The Postgres ``hard_delete_file`` RPC cascades the DB row + versions and returns
``{main, versions}`` — the storage URIs the backend must purge from S3. Before
2026-07-10, ``FileService.hard_delete`` and the matrx-ai ``cloud_file`` tool
called the raw DB fn and never purged, orphaning the main object + every version.

These tests pin the ONE primitive
``SyncEngine.hard_delete_and_purge[_async]`` (and the ``managed_delete`` paths
that route through it): the DB fn runs for THIS file, EVERY reported object is
deleted from storage, the byte cache stops serving the deleted bytes, and the
managed path refuses callers the injected access policy does not grant admin.

Doubles: the DB client and the storage router are the external dependencies.
The DB double answers ONLY for ``FILE_ID`` (a cascade issued for any other id
reports nothing), so a wrong-id cascade diverges observably. The access
decision runs through the REAL ``PermissionsManager`` with an injected checker
(the host's DB policy stand-in) — the gate itself is never stubbed.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from matrx_files.cloud_sync.byte_cache import get_byte_cache
from matrx_files.cloud_sync.permissions import PermissionsManager, configure_access_checker
from matrx_files.cloud_sync.sync_engine import (
    HardDeleteDatabaseError,
    HardDeleteStorageError,
    SyncEngine,
)

USER_ID = "user-1"
FILE_ID = "file-abc"
MAIN_URI = "s3://bucket/user-1/file-abc"
VERSION_URIS = ["s3://bucket/user-1/file-abc/v1", "s3://bucket/user-1/file-abc/v2"]
ALL_LEVELS = ("read", "write", "admin")


@pytest.fixture(autouse=True)
def _reset_access_checker_and_cache():
    yield
    configure_access_checker(None, sync_checker=None)
    get_byte_cache().invalidate(FILE_ID)


def _for_this_file(report):
    """A DB fn double that only knows FILE_ID — any other id cascades nothing."""
    return lambda file_id: report if file_id == FILE_ID else None


def _make_engine(*, purge_return, file_record=None, granted=ALL_LEVELS):
    engine = object.__new__(SyncEngine)

    router = MagicMock()
    router.delete = MagicMock(return_value=None)
    router.delete_async = AsyncMock(return_value=None)
    engine._router = router

    fallback_report = _report(MAIN_URI, VERSION_URIS)
    db = MagicMock()
    db.hard_delete_file = MagicMock(side_effect=_for_this_file(purge_return))
    db.hard_delete_file_async = AsyncMock(side_effect=_for_this_file(purge_return))
    db.hard_delete_file_fallback = MagicMock(side_effect=_for_this_file(fallback_report))
    db.hard_delete_file_fallback_async = AsyncMock(side_effect=_for_this_file(fallback_report))
    db.soft_delete_file_async = AsyncMock(return_value=True)
    db.get_file_by_path_async = AsyncMock(return_value=file_record)
    engine._db = db

    async def policy(user_id, resource_type, resource_id, level):
        return (user_id, resource_type, resource_id) == (USER_ID, "file", FILE_ID) and (
            level in granted
        )

    configure_access_checker(policy)
    engine.permissions = PermissionsManager(db, user_id="")

    engine._resolve_user_id = MagicMock(return_value=USER_ID)  # type: ignore[method-assign]
    return engine


def _report(main, versions, retained=()) -> dict:
    """A service-role purge report — every real producer (the SQL function, the ORM
    fallback, the files double) emits all four keys."""
    return {
        "main": main,
        "versions": list(versions),
        "main_retained": False,
        "retained": list(retained),
    }


def _record(**overrides) -> dict:
    record = {"id": FILE_ID, "owner_id": USER_ID, "file_path": "d/x.pdf", "storage_uri": MAIN_URI}
    record.update(overrides)
    return record


@pytest.mark.asyncio
async def test_hard_delete_and_purge_deletes_main_and_versions():
    engine = _make_engine(purge_return=_report(MAIN_URI, VERSION_URIS))

    await engine.hard_delete_and_purge_async(FILE_ID, MAIN_URI)

    engine._db.hard_delete_file_async.assert_awaited_once_with(FILE_ID)
    deleted = {c.args[0] for c in engine._router.delete_async.await_args_list}
    assert deleted == {MAIN_URI, *VERSION_URIS}, "main + every version must be purged"


#: What ``files.hard_delete_file`` returns to a JWT caller (``auth.uid()`` set) —
#: counts only, no ``main`` / ``versions`` / ``retained`` (sql 024/042, final RETURN).
JWT_CALLER_REPORT = {"deleted": True, "versions_deleted": 2, "objects_retained": 1}

#: Reports that carry no ``retained`` list: the database never said which objects a
#: surviving row still references, so none of them can be proven safe to purge.
REPORTS_WITHOUT_RETAINED = {
    "no-report": None,
    "jwt-caller-counts-only": JWT_CALLER_REPORT,
    "uris-but-no-retained-list": {"main": MAIN_URI, "versions": VERSION_URIS},
}


# AD239. Break: a report with no ``retained`` list is read as "nothing retained", so a
# main object a surviving alias still references is purged (or the row's own
# storage_uri is purged on no report at all).
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "report", REPORTS_WITHOUT_RETAINED.values(), ids=REPORTS_WITHOUT_RETAINED.keys()
)
async def test_a_purge_report_without_a_retained_list_purges_nothing_and_says_so(report, caplog):
    engine = _make_engine(purge_return=report)

    with caplog.at_level("ERROR", logger="matrx_files.cloud_sync.sync_engine"):
        await engine.hard_delete_and_purge_async(FILE_ID, MAIN_URI)

    assert engine._router.delete_async.await_args_list == [], "purged objects no retained list cleared"
    refusals = [r for r in caplog.records if r.levelname == "ERROR" and FILE_ID in r.getMessage()]
    assert refusals and "retained" in refusals[0].getMessage(), (
        "the skipped purge was silent — nothing names the file or why storage was left in place"
    )


def test_sync_purge_report_without_a_retained_list_purges_nothing():
    engine = _make_engine(purge_return=JWT_CALLER_REPORT)

    engine.hard_delete_and_purge(FILE_ID, MAIN_URI)

    engine._router.delete.assert_not_called()


# Break: the caller's storage_uri is purged although the report neither cleared it
# (``main`` / ``versions``) nor retained it — a stale record or a row the function
# never found would delete an object nobody proved unreferenced.
@pytest.mark.asyncio
async def test_a_storage_uri_the_report_did_not_clear_is_never_purged(caplog):
    engine = _make_engine(purge_return=_report(None, VERSION_URIS[:1]))

    with caplog.at_level("ERROR", logger="matrx_files.cloud_sync.sync_engine"):
        await engine.hard_delete_and_purge_async(FILE_ID, MAIN_URI)

    assert [c.args[0] for c in engine._router.delete_async.await_args_list] == VERSION_URIS[:1]
    assert any(MAIN_URI in r.getMessage() for r in caplog.records if r.levelname == "ERROR")


@pytest.mark.asyncio
async def test_hard_delete_leaves_storage_untouched_if_both_db_paths_fail():
    engine = _make_engine(purge_return=None)
    engine._db.hard_delete_file_async = AsyncMock(side_effect=RuntimeError("boom"))
    engine._db.hard_delete_file_fallback_async = AsyncMock(
        side_effect=RuntimeError("fallback boom")
    )

    with pytest.raises(HardDeleteDatabaseError):
        await engine.hard_delete_and_purge_async(FILE_ID, MAIN_URI)

    engine._router.delete_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_hard_delete_uses_orm_fallback_when_rpc_fails():
    engine = _make_engine(purge_return=None)
    engine._db.hard_delete_file_async = AsyncMock(side_effect=RuntimeError("dedup conflict"))

    await engine.hard_delete_and_purge_async(FILE_ID, MAIN_URI)

    engine._db.hard_delete_file_fallback_async.assert_awaited_once_with(FILE_ID)
    deleted = {c.args[0] for c in engine._router.delete_async.await_args_list}
    assert deleted == {MAIN_URI, *VERSION_URIS}


@pytest.mark.asyncio
async def test_hard_delete_attempts_every_uri_then_raises_aggregate_storage_error():
    engine = _make_engine(purge_return=_report(MAIN_URI, VERSION_URIS))

    async def _delete(uri: str) -> None:
        if uri in {MAIN_URI, VERSION_URIS[1]}:
            raise RuntimeError("storage unavailable")

    engine._router.delete_async = AsyncMock(side_effect=_delete)

    with pytest.raises(HardDeleteStorageError) as exc_info:
        await engine.hard_delete_and_purge_async(FILE_ID, MAIN_URI)

    assert set(exc_info.value.failed_uris) == {MAIN_URI, VERSION_URIS[1]}
    assert [call.args[0] for call in engine._router.delete_async.await_args_list] == [
        MAIN_URI,
        *VERSION_URIS,
    ]


@pytest.mark.asyncio
async def test_hard_delete_treats_false_storage_result_as_failure():
    engine = _make_engine(purge_return=_report(MAIN_URI, []))
    engine._router.delete_async = AsyncMock(return_value=False)

    with pytest.raises(HardDeleteStorageError) as exc_info:
        await engine.hard_delete_and_purge_async(FILE_ID, MAIN_URI)

    assert exc_info.value.failed_uris == (MAIN_URI,)


@pytest.mark.asyncio
async def test_hard_delete_async_stops_the_byte_cache_serving_deleted_bytes():
    engine = _make_engine(purge_return=_report(MAIN_URI, VERSION_URIS))
    get_byte_cache().put(FILE_ID, bytes_=b"deleted content")

    await engine.hard_delete_and_purge_async(FILE_ID, MAIN_URI)

    assert get_byte_cache().get(FILE_ID) is None


def test_sync_hard_delete_stops_the_byte_cache_serving_deleted_bytes():
    engine = _make_engine(purge_return=_report(MAIN_URI, VERSION_URIS))
    get_byte_cache().put(FILE_ID, bytes_=b"deleted content")

    engine.hard_delete_and_purge(FILE_ID, MAIN_URI)

    assert get_byte_cache().get(FILE_ID) is None


@pytest.mark.asyncio
async def test_managed_delete_async_hard_routes_through_purge():
    engine = _make_engine(
        purge_return=_report(MAIN_URI, VERSION_URIS), file_record=_record()
    )

    ok = await engine.managed_delete_async("d/x.pdf", user_id=USER_ID, hard_delete=True)

    assert ok is True
    deleted = {c.args[0] for c in engine._router.delete_async.await_args_list}
    assert deleted == {MAIN_URI, *VERSION_URIS}


@pytest.mark.asyncio
@pytest.mark.parametrize("hard_delete", [True, False])
async def test_managed_delete_async_refuses_a_caller_without_admin_and_deletes_nothing(
    hard_delete: bool,
):
    engine = _make_engine(
        purge_return=_report(MAIN_URI, VERSION_URIS),
        file_record=_record(),
        granted=("read", "write"),
    )

    with pytest.raises(PermissionError, match="lacks 'admin' access on file 'file-abc'"):
        await engine.managed_delete_async("d/x.pdf", user_id=USER_ID, hard_delete=hard_delete)

    engine._db.hard_delete_file_async.assert_not_awaited()
    engine._db.soft_delete_file_async.assert_not_awaited()
    engine._router.delete_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_managed_delete_async_refuses_system_immutable_file_even_for_admin():
    engine = _make_engine(
        purge_return=_report(MAIN_URI, VERSION_URIS),
        file_record=_record(metadata={"system_immutable": True}),
    )

    with pytest.raises(PermissionError, match="system-managed immutable file cannot be deleted"):
        await engine.managed_delete_async("d/x.pdf", user_id=USER_ID, hard_delete=True)

    engine._db.hard_delete_file_async.assert_not_awaited()
    engine._router.delete_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_managed_delete_async_purges_system_immutable_file_when_explicitly_allowed():
    engine = _make_engine(
        purge_return=_report(MAIN_URI, VERSION_URIS),
        file_record=_record(metadata={"system_immutable": True}),
    )

    ok = await engine.managed_delete_async(
        "d/x.pdf", user_id=USER_ID, hard_delete=True, allow_system_purge=True
    )

    assert ok is True
    deleted = {c.args[0] for c in engine._router.delete_async.await_args_list}
    assert deleted == {MAIN_URI, *VERSION_URIS}


@pytest.mark.asyncio
async def test_managed_delete_async_soft_does_not_purge():
    engine = _make_engine(purge_return=None, file_record=_record())

    await engine.managed_delete_async("d/x.pdf", user_id=USER_ID, hard_delete=False)

    engine._db.soft_delete_file_async.assert_awaited_once_with(FILE_ID)
    engine._router.delete_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_missing_object_reconciliation_soft_deletes_and_invalidates_cache():
    engine = _make_engine(purge_return=None, file_record=_record())
    get_byte_cache().put(FILE_ID, bytes_=b"bytes of a missing object")

    reconciled = await engine.reconcile_missing_object_async("d/x.pdf", user_id=USER_ID)

    assert reconciled is True
    engine._db.soft_delete_file_async.assert_awaited_once_with(FILE_ID)
    assert get_byte_cache().get(FILE_ID) is None
    engine._router.delete_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_missing_object_reconciliation_refuses_a_caller_without_read():
    engine = _make_engine(purge_return=None, file_record=_record(), granted=())

    with pytest.raises(PermissionError, match="lacks 'read' access on file 'file-abc'"):
        await engine.reconcile_missing_object_async("d/x.pdf", user_id=USER_ID)

    engine._db.soft_delete_file_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_missing_object_reconciliation_is_idempotent_after_row_is_hidden():
    engine = _make_engine(purge_return=None, file_record=None)
    engine._invalidate_byte_cache = MagicMock()  # type: ignore[method-assign]

    reconciled = await engine.reconcile_missing_object_async("d/x.pdf", user_id=USER_ID)

    assert reconciled is False
    engine._db.soft_delete_file_async.assert_not_awaited()
    engine._invalidate_byte_cache.assert_not_called()


def test_sync_hard_delete_and_purge_deletes_main_and_versions():
    engine = _make_engine(purge_return=_report(MAIN_URI, VERSION_URIS))

    engine.hard_delete_and_purge(FILE_ID, MAIN_URI)

    deleted = {c.args[0] for c in engine._router.delete.call_args_list}
    assert deleted == {MAIN_URI, *VERSION_URIS}


def test_sync_hard_delete_leaves_storage_untouched_if_database_fails():
    engine = _make_engine(purge_return=None)
    engine._db.hard_delete_file = MagicMock(side_effect=RuntimeError("boom"))
    engine._db.hard_delete_file_fallback = MagicMock(side_effect=RuntimeError("fallback boom"))

    with pytest.raises(HardDeleteDatabaseError):
        engine.hard_delete_and_purge(FILE_ID, MAIN_URI)

    engine._router.delete.assert_not_called()


def test_sync_hard_delete_attempts_all_storage_objects_before_raising():
    engine = _make_engine(purge_return=_report(MAIN_URI, VERSION_URIS))
    engine._router.delete = MagicMock(side_effect=[False, RuntimeError("unavailable"), True])

    with pytest.raises(HardDeleteStorageError) as exc_info:
        engine.hard_delete_and_purge(FILE_ID, MAIN_URI)

    assert set(exc_info.value.failed_uris) == {MAIN_URI, VERSION_URIS[0]}
    assert engine._router.delete.call_count == 3


def test_purge_uris_dedupes_and_skips_none():
    got = SyncEngine._purge_uris_from(
        MAIN_URI,
        {"main": MAIN_URI, "versions": [VERSION_URIS[0], None, VERSION_URIS[0]], "retained": []},
    )
    assert got == [MAIN_URI, VERSION_URIS[0]]


def test_merge_hard_delete_purge_keeps_parent_main_and_collects_descendants():
    from matrx_files.cloud_sync.db import DatabaseClient

    child_uri = "s3://bucket/user-1/child-thumb"
    merged = DatabaseClient._merge_hard_delete_purge(
        {"main": MAIN_URI, "versions": VERSION_URIS[:1]},
        {"main": child_uri, "versions": VERSION_URIS[1:]},
    )
    assert merged["main"] == MAIN_URI
    assert merged["versions"] == [VERSION_URIS[0], child_uri, VERSION_URIS[1]]
