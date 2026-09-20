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


# ── the byte ceiling is the provider's, measured, not a local guess ─────────
#
# 🚨 2026-09-18, live: the catalog carried Groq's dev-tier 100 MB while the
# endpoint enforced 25 MB (24.20 MB FLAC transcribed; 27.0 MB came back
# ``413 Request Entity Too Large``). Two copies of one number, and the
# audiobook lane trusted the wrong one.


class _Profile:
    def __init__(self, stt: dict | None) -> None:
        self.offering_metadata = {} if stt is None else {"stt": stt}


@pytest.mark.asyncio
async def test_the_ceiling_comes_from_the_offering(monkeypatch) -> None:
    import matrx_ai.catalog.resolve as resolve
    from matrx_ai.processing.audio.stt import provider_audio_limit_mb

    async def fake(model_ref, *a, **kw):
        return _Profile({"max_file_size_mb": 25})

    monkeypatch.setattr(resolve, "resolve_call_profile", fake)
    assert await provider_audio_limit_mb("stt-default") == 25.0


@pytest.mark.asyncio
@pytest.mark.parametrize("stt", [None, {}, {"max_file_size_mb": None},
                                 {"max_file_size_mb": 0}, {"max_file_size_mb": "nonsense"}])
async def test_an_undeclared_ceiling_falls_back_to_the_measured_floor(monkeypatch, stt) -> None:
    """Never optimistic: an offering that says nothing gets the number we
    measured against the live endpoint, not the vendor's best-tier headline."""
    import matrx_ai.catalog.resolve as resolve
    from matrx_ai.processing.audio.stt import (
        DEFAULT_PROVIDER_AUDIO_LIMIT_MB,
        provider_audio_limit_mb,
    )

    async def fake(model_ref, *a, **kw):
        return _Profile(stt)

    monkeypatch.setattr(resolve, "resolve_call_profile", fake)
    assert await provider_audio_limit_mb("stt-default") == DEFAULT_PROVIDER_AUDIO_LIMIT_MB
    assert DEFAULT_PROVIDER_AUDIO_LIMIT_MB == 25.0
