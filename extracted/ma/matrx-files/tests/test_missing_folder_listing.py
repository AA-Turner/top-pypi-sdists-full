"""Folder-scoped listings: an absent folder is an empty collection; a present one
scopes the listing to exactly that path's folders (one per organization — a read never narrows
to one organization), for exactly the resolved user."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from matrx_files.cloud_sync.sync_engine import SyncEngine


def _engine(db: object) -> SyncEngine:
    engine = SyncEngine.__new__(SyncEngine)
    engine._config = SimpleNamespace(user_id="user-1")
    engine._db = db
    return engine


class _FolderScopedDB:
    """Listing rows keyed by (owner, folder id). Only the resolved folder's uuid,
    queried for the resolved owner, finds the folder's rows — the root listing
    (folder id None) holds different rows, so an unscoped query diverges."""

    _FOLDER = {"id": "folder-uuid", "folder_path": "docs/reports"}
    _ROWS = {
        ("user-1", ("folder-uuid",)): [{"id": "inside-docs-reports"}],
        ("user-1", None): [{"id": "at-root"}, {"id": "inside-docs-reports"}],
    }

    def get_folders_by_path(self, owner_id, folder_path):
        return [self._FOLDER] if (owner_id, folder_path) == ("user-1", "docs/reports") else []

    def list_files(self, owner_id, folder_id=None):
        key = tuple(folder_id) if isinstance(folder_id, list) else folder_id
        return self._ROWS.get((owner_id, key), [])

    list_folders = list_files

    async def get_folders_by_path_async(self, owner_id, folder_path):
        return self.get_folders_by_path(owner_id, folder_path)

    async def list_files_async(self, owner_id, folder_id=None):
        return self.list_files(owner_id, folder_id)

    list_folders_async = list_files_async


@pytest.mark.parametrize(
    ("method_name", "lookup_name", "list_name"),
    [
        ("list_files", "get_folders_by_path", "list_files"),
        ("list_folders", "get_folders_by_path", "list_folders"),
    ],
)
def test_missing_folder_returns_empty_without_querying_uuid_column(
    method_name: str,
    lookup_name: str,
    list_name: str,
) -> None:
    db = Mock()
    getattr(db, lookup_name).return_value = []
    engine = _engine(db)

    result = getattr(engine, method_name)("missing/folder")

    assert result == []
    getattr(db, list_name).assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method_name", "lookup_name", "list_name"),
    [
        ("list_files_async", "get_folders_by_path_async", "list_files_async"),
        ("list_folders_async", "get_folders_by_path_async", "list_folders_async"),
    ],
)
async def test_missing_folder_async_returns_empty_without_querying_uuid_column(
    method_name: str,
    lookup_name: str,
    list_name: str,
) -> None:
    db = Mock()
    setattr(db, lookup_name, AsyncMock(return_value=[]))
    setattr(db, list_name, AsyncMock())
    engine = _engine(db)

    result = await getattr(engine, method_name)("missing/folder")

    assert result == []
    getattr(db, list_name).assert_not_awaited()


@pytest.mark.parametrize("method_name", ["list_files", "list_folders"])
def test_existing_folder_lists_only_that_folders_rows(method_name: str) -> None:
    engine = _engine(_FolderScopedDB())

    assert getattr(engine, method_name)("docs/reports") == [{"id": "inside-docs-reports"}]


@pytest.mark.asyncio
@pytest.mark.parametrize("method_name", ["list_files_async", "list_folders_async"])
async def test_existing_folder_async_lists_only_that_folders_rows(method_name: str) -> None:
    engine = _engine(_FolderScopedDB())

    assert await getattr(engine, method_name)("docs/reports") == [{"id": "inside-docs-reports"}]
