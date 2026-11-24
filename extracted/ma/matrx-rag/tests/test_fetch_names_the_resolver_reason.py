"""CGU-10 row 31: a PDF whose bytes the file gate refused failed as "cloud_sync read returned empty" —
the refusal itself was never named, so the access defect hid for weeks. The stage names the resolver's reason."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_rag import stages


class _Rows:
    def filter(self, **_k):
        return self

    async def values(self, *_a):
        return [{"file_name": "a.pdf", "storage_uri": "s3://bucket/a"}]


@pytest.mark.asyncio
async def test_an_unreadable_file_names_why(monkeypatch: pytest.MonkeyPatch) -> None:
    class _Fm:
        async def resolve_media_async(self, ref, *, needs_bytes: bool):
            return SimpleNamespace(base64_data=None, resolver_error="access_denied")

    monkeypatch.setattr(stages, "get_db_model", lambda _name: _Rows())
    monkeypatch.setattr("matrx_rag._ext.get_cloud_file_manager", lambda: _Fm())
    with pytest.raises(RuntimeError, match="access_denied"):
        await stages._fetch_cld_file_to_disk("file-1")
