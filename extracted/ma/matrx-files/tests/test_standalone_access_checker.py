"""The standalone service injects the authoritative DB policy as the file gate.

Regression cover for a real production bug: the standalone matrx-files service
(files.matrxserver.com) never called `configure_access_checker`, so every file
request fell back to the Python permission SUBSET. That subset cannot resolve the
contextual crawl-artifact → web.site container grant, so org members were denied
their own crawl screenshots with `has 'none'` — even though `files.has_access_for`
grants them. These tests pin the injected checker's routing, that the DB's verdict
(allow AND deny) is returned unaltered, and that installing it makes
`require_async` consult the DB, not the fallback — while the sync gate stays on
the deny-more subset.

No DB: `call_function` (the DB boundary) is mocked. The DB functions themselves
are proven live.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from matrx_files.cloud_sync.permissions import (
    PermissionsManager,
    configure_access_checker,
    get_access_checker,
)
from matrx_files.standalone import access_checker as ac


@pytest.fixture(autouse=True)
def _reset_checker():
    yield
    configure_access_checker(None, sync_checker=None)


class _ExplodingDB:
    """Any Python-side resolution is a bug once the checker is injected."""

    async def get_file_async(self, *a, **k):  # pragma: no cover
        raise AssertionError("Python fallback consulted despite an injected checker")


class _StrangerDB:
    """Sync subset view of a private file owned by someone else, no grant, no judge."""

    def get_file(self, fid):
        return {"id": fid, "owner_id": "owner-1", "visibility": "personal"}

    def get_user_permission(self, rid, rtype, uid):
        return None

    def has_platform_viewer_access(self, uid, rtype, rid):
        return False


@pytest.mark.parametrize("db_verdict", [True, False])
async def test_file_returns_the_files_has_access_for_verdict(monkeypatch, db_verdict) -> None:
    call = AsyncMock(return_value=db_verdict)
    monkeypatch.setattr(ac, "call_function", call)

    assert await ac.db_access_allowed("u1", "file", "f1", "read") is db_verdict
    # files → files.has_access_for(user, file_id, db_level); read → viewer.
    call.assert_awaited_once_with("matrx_files", "files", "has_access_for", "u1", "f1", "viewer")


async def test_non_file_routes_through_iam_has_access_for(monkeypatch) -> None:
    call = AsyncMock(return_value=False)
    monkeypatch.setattr(ac, "call_function", call)

    assert await ac.db_access_allowed("u1", "folder", "d1", "read") is False
    call.assert_awaited_once_with(
        "matrx_files", "iam", "has_access_for", "u1", "folder", "d1", "viewer"
    )


async def test_level_mapping_read_write_admin(monkeypatch) -> None:
    call = AsyncMock(return_value=True)
    monkeypatch.setattr(ac, "call_function", call)

    for level, expected in (("read", "viewer"), ("write", "editor"), ("admin", "admin")):
        call.reset_mock()
        await ac.db_access_allowed("u1", "file", "f1", level)
        assert call.await_args.args[-1] == expected


async def test_unknown_level_raises(monkeypatch) -> None:
    monkeypatch.setattr(ac, "call_function", AsyncMock(return_value=True))
    with pytest.raises(ValueError, match="unknown access level"):
        await ac.db_access_allowed("u1", "file", "f1", "sudo")


async def test_missing_actor_or_resource_denies_without_a_db_call(monkeypatch) -> None:
    call = AsyncMock(return_value=True)
    monkeypatch.setattr(ac, "call_function", call)

    assert await ac.db_access_allowed("", "file", "f1", "read") is False
    assert await ac.db_access_allowed("u1", "file", "", "read") is False
    call.assert_not_awaited()


async def test_install_makes_require_async_use_the_db_policy(monkeypatch) -> None:
    """After install, require_async consults the DB checker — never the fallback."""
    call = AsyncMock(return_value=True)
    monkeypatch.setattr(ac, "call_function", call)

    ac.install_standalone_access_checker()
    assert get_access_checker() is ac.db_access_allowed

    pm = PermissionsManager(_ExplodingDB(), user_id="org-member")
    # A contextual crawl artifact an org member should see: the fallback would
    # explode (_ExplodingDB); the injected DB policy grants it.
    assert await pm.require_async("file", "crawl-file", "read", "org-member") == "read"
    call.assert_awaited_once_with(
        "matrx_files", "files", "has_access_for", "org-member", "crawl-file", "viewer"
    )


def test_install_leaves_the_sync_gate_on_the_deny_more_subset(monkeypatch) -> None:
    """The sync gate cannot borrow the async pool: it must stay on the subset,
    never on a permissive stand-in."""
    monkeypatch.setattr(ac, "call_function", AsyncMock(return_value=True))

    ac.install_standalone_access_checker()

    pm = PermissionsManager(_StrangerDB(), user_id="stranger")
    with pytest.raises(PermissionError, match=r"has 'none'.*python-subset \(sync path\)"):
        pm.require("file", "f1", "read", "stranger")
