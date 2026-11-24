"""The type-default marker is a writer-side placeholder for NULL, never an enum label.

Live failure (render-check screenshot upload): a dedup/race winner was reconciled with the unstated-default marker
and ``UPDATE files.files SET shown_to = 'type_default'`` hit ``invalid input value for enum platform.shown_to``.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from matrx_utils.row_access import SHOWN_TO_TYPE_DEFAULT

from matrx_files.cloud_sync.sync_engine import SyncEngine


class _Db:
    def __init__(self) -> None:
        self.updates: list[dict] = []

    async def update_file_async(self, file_id, cols):
        self.updates.append(cols)

    async def get_file_async(self, file_id):
        return {"id": file_id, "shown_to": None}

    def update_file(self, file_id, cols):
        self.updates.append(cols)

    def get_file(self, file_id):
        return {"id": file_id, "shown_to": None}


class _Perms:
    async def require_async(self, *a, **k):
        return None

    def require(self, *a, **k):
        return None


def _engine() -> tuple[SimpleNamespace, _Db]:
    db = _Db()
    eng = SimpleNamespace(_db=db, permissions=_Perms())

    async def _res(**k):
        return "ok"

    eng._sync_result_for_existing_async = _res
    eng._sync_result_for_existing = lambda **k: "ok"
    return eng, db


@pytest.mark.asyncio
@pytest.mark.parametrize("marker", [SHOWN_TO_TYPE_DEFAULT, None])
async def test_async_reconcile_never_writes_the_marker(marker) -> None:
    eng, db = _engine()
    row = {"id": "f1", "shown_to": "only_me"}
    out = await SyncEngine._reconcile_existing_result_async(
        eng, existing_row=row, content_bytes=b"", checksum=None, share_with=None, share_level="viewer", uid="u",
        published_to_web=None, shown_to=marker, wants_anyone_link=False,
    )
    assert out == "ok"
    assert db.updates == []


@pytest.mark.parametrize("marker", [SHOWN_TO_TYPE_DEFAULT, None])
def test_sync_reconcile_never_writes_the_marker(marker) -> None:
    eng, db = _engine()
    SyncEngine._reconcile_existing_result_sync(
        eng, existing_row={"id": "f1", "shown_to": "only_me"}, content_bytes=b"", checksum=None, share_with=None,
        share_level="viewer", uid="u", published_to_web=None, shown_to=marker, wants_anyone_link=False,
    )
    assert db.updates == []


@pytest.mark.asyncio
async def test_a_named_label_still_updates() -> None:
    eng, db = _engine()
    await SyncEngine._reconcile_existing_result_async(
        eng, existing_row={"id": "f1", "shown_to": None}, content_bytes=b"", checksum=None, share_with=None,
        share_level="viewer", uid="u", published_to_web=None, shown_to="my_team", wants_anyone_link=False,
    )
    assert db.updates == [{"shown_to": "my_team"}]
