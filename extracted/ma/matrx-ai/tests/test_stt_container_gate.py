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


# ── a data URI names its container by its declared type (2026-09-28) ────────
#
# A file_id-only audio part resolves to bare base64. Handed on raw it was read
# as a FILE NAME ("File name too long") and the texted voice memo was skipped;
# as a data URI every container was named "audio.wav" whatever it held.


@pytest.mark.asyncio
async def test_a_flac_data_uri_is_sent_as_flac() -> None:
    import base64

    uri = "data:audio/flac;base64," + base64.b64encode(b"fLaC" + b"\x00" * 64).decode()
    (name, data), _ = await prepare_audio_file(uri, max_file_size_mb=10.0)
    assert name == "audio.flac" and data.startswith(b"fLaC")


@pytest.mark.asyncio
async def test_an_amr_data_uri_is_refused_by_name_not_mislabelled_wav() -> None:
    import base64

    uri = "data:audio/amr;base64," + base64.b64encode(b"#!AMR\n").decode()
    with pytest.raises(ValueError, match="'.amr'"):
        await prepare_audio_file(uri, max_file_size_mb=10.0)


@pytest.mark.asyncio
async def test_bare_base64_audio_is_transcribed_as_a_data_uri(monkeypatch) -> None:
    import base64

    from matrx_ai.config.media_config import AudioContent
    from matrx_ai.processing.audio import stt

    seen: dict[str, str] = {}

    class _Result:
        text = "call me back at five"
        usage = None

    async def fake_execute_stt(request):
        seen["source"] = request.audio_source
        return _Result()

    monkeypatch.setattr(stt, "execute_stt", fake_execute_stt)
    audio = AudioContent(
        base64_data=base64.b64encode(b"fLaC").decode(), mime_type="audio/flac"
    )
    try:
        await audio.get_transcription_async(force_refresh=True)
    except Exception:
        pass  # usage bookkeeping on the fake result is not what this proves
    assert seen["source"].startswith("data:audio/flac;base64,")


@pytest.mark.asyncio
async def test_audio_that_cannot_be_transcribed_is_said_never_silently_removed(monkeypatch) -> None:
    from matrx_ai.config import MessageList, TextContent, UnifiedMessage
    from matrx_ai.config.media_config import AudioContent
    from matrx_ai.processing.audio.audio_preprocessing import preprocess_audio_in_messages

    async def broken(self, force_refresh: bool = False):
        raise ValueError("Audio container '.amr' is not one the transcription provider accepts")

    monkeypatch.setattr(AudioContent, "get_transcription_async", broken)
    messages = MessageList(
        [UnifiedMessage(role="user", content=[AudioContent(base64_data="AAAA", mime_type="audio/amr")])]
    )
    processed, _usage = await preprocess_audio_in_messages(messages, supports_audio_input=False)
    content = list(processed)[0].content
    assert len(content) == 1 and isinstance(content[0], TextContent)
    assert "could not be transcribed" in content[0].text
