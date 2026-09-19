"""The STT provider takes a file by NAME, and refuses most names.

🚨 2026-09-17: a two-hour ``.m4b`` audiobook — ordinary MP4/AAC bytes — was
refused by Groq with ``400 unsupported_audio_format`` purely for its
extension, after a paid round-trip, and the caller had nothing honest to say.
The boundary now answers that question locally, before the call.
"""

from __future__ import annotations

import pytest

from matrx_ai.processing.audio.stt import (
    PROVIDER_ACCEPTED_AUDIO_SUFFIXES,
    prepare_audio_file,
    provider_accepts_audio_container,
)


@pytest.mark.parametrize("name", sorted(PROVIDER_ACCEPTED_AUDIO_SUFFIXES))
def test_every_declared_suffix_is_accepted(name: str) -> None:
    assert provider_accepts_audio_container(f"/tmp/recording{name}")
    assert provider_accepts_audio_container(f"/tmp/RECORDING{name.upper()}")


@pytest.mark.parametrize(
    "name",
    ["book.m4b", "voice.aac", "memo.wma", "call.amr", "master.aiff",
     "field.caf", "clip.3gp", "notes.txt", "noextension"],
)
def test_containers_the_provider_refuses_are_named_before_the_call(name: str) -> None:
    assert not provider_accepts_audio_container(name)


@pytest.mark.asyncio
async def test_prepare_audio_file_refuses_an_m4b_locally(tmp_path) -> None:
    book = tmp_path / "handbook.m4b"
    book.write_bytes(b"\x00" * 1024)
    with pytest.raises(ValueError, match="not one the transcription provider accepts"):
        await prepare_audio_file(str(book), max_file_size_mb=100.0)


@pytest.mark.asyncio
async def test_prepare_audio_file_still_passes_an_accepted_container(tmp_path) -> None:
    clip = tmp_path / "clip.flac"
    clip.write_bytes(b"\x00" * 2048)
    (name, data), size_mb = await prepare_audio_file(str(clip), max_file_size_mb=100.0)
    assert name == "clip.flac" and len(data) == 2048 and size_mb < 1
