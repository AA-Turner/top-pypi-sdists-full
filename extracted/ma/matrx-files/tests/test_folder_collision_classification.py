"""Folder recovery accepts only a recognized path uniqueness collision."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from matrx_files.cloud_sync.sync_engine import FolderOrganizationMismatch, SyncEngine

from _files_db_double import UniqueViolation


@pytest.mark.parametrize("method", ["sync", "async", "labelled"])
@pytest.mark.parametrize(
    "error", [RuntimeError("insert failed"), UniqueViolation("unrelated_unique_key")]
)
@pytest.mark.asyncio
async def test_unrelated_insert_error_propagates_even_if_winner_exists(method, error):
    engine = object.__new__(SyncEngine)
    engine._db = MagicMock()
    winner = {"id": "winner", "organization_id": "org"}
    engine._db.get_folder_by_path = MagicMock(side_effect=[None, winner])
    engine._db.get_folder_by_path_async = AsyncMock(side_effect=[None, winner])
    engine._db.create_folder = MagicMock(side_effect=error)
    engine._db.create_folder_async = AsyncMock(side_effect=error)
    with pytest.raises(type(error)) as caught:
        if method == "sync":
            engine._ensure_folder("docs/file", "user", "org")
        elif method == "async":
            await engine._ensure_folder_async("docs/file", "user", "org")
        else:
            await engine.ensure_labelled_folder_chain_async(
                owner_id="user", organization_id="org", segments=[("docs", "Docs")]
            )
    assert caught.value is error
    if method == "sync":
        assert engine._db.get_folder_by_path.call_count == 1
    else:
        assert engine._db.get_folder_by_path_async.await_count == 1


@pytest.mark.parametrize("method", ["sync", "async", "labelled"])
@pytest.mark.parametrize("org", ["org", "other"])
@pytest.mark.parametrize(
    "constraint", ["folders_owner_org_path_key", "cld_folders_owner_id_folder_path_key"]
)
@pytest.mark.asyncio
async def test_path_collision_reuses_same_org_and_refuses_foreign_org(method, org, constraint):
    engine = object.__new__(SyncEngine)
    engine._db = MagicMock()
    winner = {"id": "winner", "organization_id": org}
    error = UniqueViolation(constraint)
    engine._db.get_folder_by_path = MagicMock(side_effect=[None, winner])
    engine._db.get_folder_by_path_async = AsyncMock(side_effect=[None, winner])
    engine._db.create_folder = MagicMock(side_effect=error)
    engine._db.create_folder_async = AsyncMock(side_effect=error)

    async def invoke():
        if method == "sync":
            return engine._ensure_folder("docs/file", "user", "org")
        if method == "async":
            return await engine._ensure_folder_async("docs/file", "user", "org")
        return (
            await engine.ensure_labelled_folder_chain_async(
                owner_id="user", organization_id="org", segments=[("docs", "Docs")]
            )
        )[1]

    if org == "other":
        with pytest.raises(FolderOrganizationMismatch):
            await invoke()
    else:
        assert await invoke() == "winner"


@pytest.mark.asyncio
async def test_labelled_path_collision_revives_trashed_folder():
    engine = object.__new__(SyncEngine)
    engine._db = MagicMock()
    engine._db.get_folder_by_path_async = AsyncMock(return_value=None)
    engine._db.create_folder_async = AsyncMock(
        side_effect=UniqueViolation("cld_folders_owner_id_folder_path_key")
    )
    engine._db.get_folder_by_path_any_state_async = AsyncMock(
        return_value={"id": "trashed", "organization_id": "org", "deleted_at": "2026-01-01"}
    )
    engine._db.restore_folder_async = AsyncMock(
        return_value={"id": "trashed", "organization_id": "org", "deleted_at": None}
    )
    assert await engine.ensure_labelled_folder_chain_async(
        owner_id="user", organization_id="org", segments=[("docs", "Docs")]
    ) == ("docs", "trashed")
    engine._db.restore_folder_async.assert_awaited_once_with("trashed")
