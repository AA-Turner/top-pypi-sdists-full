"""A row flagged published over PRIVATE bytes (sharing's generic ``makePublic`` set the flag without the move) is
repaired by publishing it again: the bytes move to the public bucket. Before (MAILCHIMP-DUPE K, 2026-11-13, a mail
designer image), the unchanged-flag no-op returned early and the file stayed private forever."""

from __future__ import annotations

import pytest

from matrx_files.cloud_sync import cdn
from matrx_files.cloud_sync import sync_engine as se


class _Db:
    def __init__(self, row: dict) -> None:
        self.row = row

    async def get_file_async(self, file_id: str) -> dict:
        return dict(self.row)

    async def update_file_async(self, file_id: str, cols: dict) -> None:
        self.row.update(cols)


class _Router:
    def __init__(self) -> None:
        self.copies: list[tuple[str, str]] = []

    async def copy_async(self, a: str, b: str) -> None:
        self.copies.append((a, b))

    async def delete_async(self, a: str) -> None:
        pass


def _engine(row: dict):
    cls = next(c for c in vars(se).values() if isinstance(c, type) and hasattr(c, "set_published_to_web_async"))
    e = object.__new__(cls)
    e._db, e._router = _Db(row), _Router()
    e._resolve_user_id = lambda uid: uid
    return e


@pytest.fixture(autouse=True)
def _public_bucket(monkeypatch):
    monkeypatch.setattr(cdn, "public_bucket_or_raise", lambda context: "pub-bucket")


@pytest.mark.asyncio
async def test_republishing_a_published_row_over_private_bytes_moves_them() -> None:
    e = _engine({"id": "f1", "published_to_web": True, "storage_uri": "s3://private-bucket/u/a.png", "metadata": {}})
    await e.set_published_to_web_async("f1", True, user_id="u1")
    assert e._router.copies == [("s3://private-bucket/u/a.png", "s3://pub-bucket/u/a.png")]
    assert e._db.row["storage_uri"] == "s3://pub-bucket/u/a.png"


@pytest.mark.asyncio
async def test_a_published_row_already_public_is_still_a_no_op() -> None:
    e = _engine({"id": "f2", "published_to_web": True, "storage_uri": "s3://pub-bucket/u/b.png", "metadata": {}})
    await e.set_published_to_web_async("f2", True, user_id="u1")
    assert e._router.copies == []
