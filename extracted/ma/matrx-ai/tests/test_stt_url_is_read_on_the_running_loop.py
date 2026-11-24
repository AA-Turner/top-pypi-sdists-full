"""A URL handed to STT is resolved on the running loop, never through the sync resolver in a thread.

Live 2026-11-14: POST /audio/transcribe-url with our own CDN read-aloud file was a 500
("resolve_media could not produce bytes ... cdn_url_not_in_files") although the files row existed:
`asyncio.to_thread(fetch_media)` ran the SYNC ORM lookup off the loop, which swallowed its failure.
"""

import threading

import pytest

import matrx_ai.media as media
from matrx_ai.processing.audio.stt import prepare_audio_file


@pytest.mark.asyncio
async def test_url_audio_resolves_through_the_async_door_on_the_loop_thread(monkeypatch) -> None:
    main = threading.get_ident()
    seen: dict[str, int] = {}

    async def fake_async(url: str, target_format: str = "bytes") -> bytes:
        seen["thread"] = threading.get_ident()
        return b"RIFF"

    def sync_must_not_run(*_a, **_k):
        raise AssertionError("the sync fetch_media must not be used from the STT path")

    monkeypatch.setattr(media, "fetch_media_async", fake_async)
    monkeypatch.setattr(media, "fetch_media", sync_must_not_run)
    (name, data), _size = await prepare_audio_file(
        "https://cdn.matrxserver.com/a/b?v=1", max_file_size_mb=25.0
    )
    assert data == b"RIFF" and name == "audio.wav"
    assert seen["thread"] == main
