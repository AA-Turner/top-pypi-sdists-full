from __future__ import annotations

import pytest

from matrx_files.audio_extract import (
    AUDIO_EXTRACTED_KIND,
    _AUDIO_STREAM_RE,
    extraction_cache_key,
    extraction_ffmpeg_args,
    plan_extraction,
)
from matrx_files.derivations import FILE_DERIVATION_KINDS


def test_audio_extracted_kind_is_registered() -> None:
    assert AUDIO_EXTRACTED_KIND == "audio_extracted"
    assert AUDIO_EXTRACTED_KIND in FILE_DERIVATION_KINDS


@pytest.mark.parametrize(
    ("codec", "copy_stream", "ext", "mime"),
    [
        ("aac", True, ".m4a", "audio/mp4"),
        ("AAC", True, ".m4a", "audio/mp4"),
        ("opus", True, ".ogg", "audio/ogg"),
        ("vorbis", True, ".ogg", "audio/ogg"),
        ("mp3", True, ".mp3", "audio/mpeg"),
        ("flac", True, ".flac", "audio/flac"),
        ("pcm_s16le", False, ".m4a", "audio/mp4"),
        ("ac3", False, ".m4a", "audio/mp4"),
        (None, False, ".m4a", "audio/mp4"),
        ("", False, ".m4a", "audio/mp4"),
    ],
)
def test_plan_extraction_codec_table(
    codec: str | None, copy_stream: bool, ext: str, mime: str
) -> None:
    plan = plan_extraction(codec)
    assert plan.copy_stream is copy_stream
    assert plan.extension == ext
    assert plan.mime_type == mime
    assert plan.mode == ("stream_copy" if copy_stream else "transcoded")


def test_ffmpeg_args_copy_vs_transcode() -> None:
    copy_args = extraction_ffmpeg_args(plan_extraction("aac"))
    assert copy_args == ["-vn", "-acodec", "copy"]
    transcode_args = extraction_ffmpeg_args(plan_extraction("ac3"))
    assert "-c:a" in transcode_args and "aac" in transcode_args
    assert "copy" not in transcode_args


def test_stream_regex_parses_ffmpeg_stderr() -> None:
    stderr = (
        "  Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p\n"
        "  Stream #0:1(und): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo\n"
    )
    match = _AUDIO_STREAM_RE.search(stderr)
    assert match is not None
    assert match.group(1).lower() == "aac"


def test_cache_key_changes_with_source_revision() -> None:
    base = {"id": "f-1", "checksum": "abc"}
    changed = {"id": "f-1", "checksum": "def"}
    other_file = {"id": "f-2", "checksum": "abc"}
    k = extraction_cache_key(base)
    assert k == extraction_cache_key(dict(base))  # stable
    assert k != extraction_cache_key(changed)
    assert k != extraction_cache_key(other_file)
