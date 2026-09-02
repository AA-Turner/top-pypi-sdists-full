"""The official-video composer reads its sources through the media funnel.

Every episode whose media went durable-public failed composition with
``Cannot determine storage backend from HTTPS URL: 'https://cdn…'`` because
the composer fed public CDN URLs to the raw storage reader
(``FileManager.read_url_async`` → ``parse_storage_url``), which only speaks
S3 URLs and native URIs. The canonical funnel — ``resolve_media_async`` on a
``MediaRef`` — resolves by IDENTITY (file_id → cld_files row → S3) and knows
every URL dialect we mint, CDN included.

Two layers, each sufficient alone:
  1. the composer's reader builds a MediaRef and never touches read_url_async;
  2. a bare ``file_id`` handle is carried as identity, not smuggled as a URL.
"""

from __future__ import annotations

import base64

import pytest

from matrx_ai.agent_runners import podcast_generator as pg

CDN_URL = "https://cdn.matrxserver.com/4cf62e4e-2679-484f-b652-034e697418df/db22f2a2-9548-4eb7-946b-19b267bdee09?v=84f485d6"
FILE_ID = "db22f2a2-9548-4eb7-946b-19b267bdee09"


class _FakeFileManager:
    """Records how it was asked for bytes. ``read_url_async`` is a landmine:
    calling it is the bug this test exists to prevent."""

    def __init__(self, payload: bytes = b"MP4BYTES") -> None:
        self.payload = payload
        self.seen: list[tuple[str | None, str | None]] = []

    async def resolve_media_async(self, ref, *, needs_bytes: bool = False, **_kw):
        assert needs_bytes is True, "composer must ask for bytes"
        self.seen.append((ref.file_id, ref.url))
        ref.base64_data = base64.b64encode(self.payload).decode("ascii")
        ref.is_resolved = True
        return ref

    async def read_url_async(self, url: str) -> bytes:  # pragma: no cover
        raise AssertionError(
            "composer used the raw storage reader — a public CDN URL dies there"
        )


@pytest.mark.asyncio
async def test_cdn_url_handle_resolves_through_the_media_funnel():
    fm = _FakeFileManager()
    data = await pg._read_media_handle_bytes(fm, CDN_URL)
    assert data == b"MP4BYTES"
    assert fm.seen == [(None, CDN_URL)]


@pytest.mark.asyncio
async def test_bare_file_id_handle_is_carried_as_identity():
    fm = _FakeFileManager()
    await pg._read_media_handle_bytes(fm, f"  {FILE_ID}  ")
    assert fm.seen == [(FILE_ID, None)], "a file_id must never be sent as a URL"


@pytest.mark.asyncio
async def test_resolver_failure_is_raised_with_the_handle_named():
    class _Failing(_FakeFileManager):
        async def resolve_media_async(self, ref, *, needs_bytes=False, **_kw):
            ref.resolver_error = "file_not_found"
            return ref

    with pytest.raises(RuntimeError) as exc:
        await pg._read_media_handle_bytes(_Failing(), CDN_URL)
    assert "file_not_found" in str(exc.value)
    assert CDN_URL in str(exc.value)
