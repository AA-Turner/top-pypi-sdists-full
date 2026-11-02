"""Authorized, cached audio extraction from a parent video file.

Demuxes (stream-copy) or normalizes the audio track of an owned video
``files.files`` row into a standalone, playable audio derivative
(``derivation_kind='audio_extracted'``). Idempotent per
``(parent, kind, source revision)`` — repeat calls return the existing
child. The processor's existing hooks then probe duration + waveform.

Codec decision (recorded in common-docs/systems/media/media-capture/FEATURE.md):

    source audio codec  →  output
    aac                 →  stream copy into .m4a  (audio/mp4)
    opus / vorbis       →  stream copy into .ogg  (audio/ogg)
    mp3                 →  stream copy into .mp3  (audio/mpeg)
    flac                →  stream copy into .flac (audio/flac)
    anything else       →  transcode to AAC 128k stereo .m4a (audio/mp4)

Memory bound: the SOURCE object is streamed to a temp file
(``router.download_to_path_async``) and read only by ffmpeg — its bytes
never enter Python. Only the (much smaller) extracted audio is loaded
for the managed write.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
import subprocess
import uuid
from pathlib import Path
from tempfile import gettempdir
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .asset_envelope import FileRef
from .derivations import FileDerivationKind, inherit_derived_file_policy
from .system_paths import AUDIO_EXTRACTS

if TYPE_CHECKING:
    from .service import FileService

logger = logging.getLogger(__name__)

AUDIO_EXTRACTED_KIND = FileDerivationKind.AUDIO_EXTRACTED.value

# codec → (copy?, extension, mime). Anything absent transcodes to AAC/M4A.
_COPY_TARGETS: dict[str, tuple[str, str]] = {
    "aac": (".m4a", "audio/mp4"),
    "opus": (".ogg", "audio/ogg"),
    "vorbis": (".ogg", "audio/ogg"),
    "mp3": (".mp3", "audio/mpeg"),
    "flac": (".flac", "audio/flac"),
}
_TRANSCODE_TARGET: tuple[str, str] = (".m4a", "audio/mp4")


class AudioExtractionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AudioExtractionResult(BaseModel):
    """One extracted-audio derivative plus lineage diagnostics."""

    source_file_id: str
    audio_codec: str | None = None
    extraction_mode: Literal["stream_copy", "transcoded"]
    cache_hit: bool
    file: FileRef


class ExtractionPlan(BaseModel):
    """Pure codec → ffmpeg-arg decision, unit-testable without ffmpeg."""

    model_config = ConfigDict(frozen=True)

    copy_stream: bool
    extension: str
    mime_type: str
    mode: Literal["stream_copy", "transcoded"]


def plan_extraction(audio_codec: str | None) -> ExtractionPlan:
    """Decide stream-copy vs transcode for a detected source audio codec."""
    codec = (audio_codec or "").strip().lower()
    target = _COPY_TARGETS.get(codec)
    if target is not None:
        ext, mime = target
        return ExtractionPlan(
            copy_stream=True, extension=ext, mime_type=mime, mode="stream_copy"
        )
    ext, mime = _TRANSCODE_TARGET
    return ExtractionPlan(
        copy_stream=False, extension=ext, mime_type=mime, mode="transcoded"
    )


def extraction_ffmpeg_args(plan: ExtractionPlan) -> list[str]:
    """The output-side ffmpeg arguments for a plan (input args added by caller)."""
    if plan.copy_stream:
        return ["-vn", "-acodec", "copy"]
    return ["-vn", "-ac", "2", "-c:a", "aac", "-b:a", "128k"]


_AUDIO_STREAM_RE = re.compile(r"Stream #\d+:\d+.*?Audio:\s*([A-Za-z0-9_]+)")


def _probe_audio_codec_sync(ffmpeg: str, path: str) -> str | None:
    """Detect the first audio stream's codec by parsing ``ffmpeg -i`` stderr.

    Uses ffmpeg (bundled via imageio-ffmpeg) rather than ffprobe, which the
    bundled build does not ship. Returns None when no audio stream exists.
    """
    proc = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", path],
        capture_output=True,
        text=True,
        errors="replace",
    )
    # ffmpeg -i with no output always exits non-zero; the stream table is
    # still printed. Parse stderr regardless of return code.
    match = _AUDIO_STREAM_RE.search(proc.stderr or "")
    return match.group(1).lower() if match else None


def _extract_audio_sync(
    ffmpeg: str, source_path: str, output_path: str, plan: ExtractionPlan
) -> None:
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-y",
        "-i",
        source_path,
        *extraction_ffmpeg_args(plan),
        output_path,
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        tail = (proc.stderr or b"")[-800:]
        raise RuntimeError(
            f"audio extraction failed (ffmpeg rc={proc.returncode}, "
            f"mode={plan.mode}): {tail!r}"
        )


def extraction_cache_key(source_record: dict[str, Any]) -> str:
    """Stable key per (parent, source revision) — invalidates on re-upload."""
    source_revision = (
        source_record.get("checksum")
        or source_record.get("current_version")
        or source_record.get("updated_at")
        or "unknown"
    )
    payload = json.dumps(
        {
            "source_file_id": str(source_record["id"]),
            "source_revision": str(source_revision),
            "format_version": 1,
        },
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


async def extract_audio(
    service: FileService,
    *,
    file_id: str,
    user_id: str,
    request: AudioExtractionRequest | None = None,
) -> AudioExtractionResult:
    """Authorize, demux/normalize, persist, and return the audio derivative."""
    request = request or AudioExtractionRequest()
    if not isinstance(request, AudioExtractionRequest):
        request = AudioExtractionRequest.model_validate(request)

    source = await service.read_record(file_id, user_id=user_id, level="read")
    source_mime = (source.get("mime_type") or "").split(";", 1)[0].strip().lower()
    if not source_mime.startswith("video/"):
        raise ValueError(
            f"File {file_id!r} is {source_mime or 'unknown'!r}, not a video — "
            "audio extraction requires a video/* parent."
        )

    cache_key = extraction_cache_key(source)
    cached = await service.db.find_derivative_async(
        parent_file_id=str(source["id"]),
        derivation_kind=AUDIO_EXTRACTED_KIND,
        metadata_key="extraction_key",
        metadata_value=cache_key,
    )
    if cached is not None:
        derivation_meta = cached.get("derivation_metadata") or {}
        return AudioExtractionResult(
            source_file_id=str(source["id"]),
            audio_codec=derivation_meta.get("source_audio_codec"),
            extraction_mode=(
                "stream_copy"
                if derivation_meta.get("extraction_mode") == "stream_copy"
                else "transcoded"
            ),
            cache_hit=True,
            file=await service.build_file_ref(cached),
        )

    # Canonical-first, matching every other read path (download streaming,
    # thumbnails): legacy dedup-loser rows point at the winner's object.
    storage_uri = source.get("canonical_storage_uri") or source.get("storage_uri")
    if not storage_uri:
        raise FileNotFoundError(f"File {file_id!r} has no readable storage object.")

    from .specific_handlers.video_compose import _resolve_ffmpeg_binary

    ffmpeg = _resolve_ffmpeg_binary()
    tmp_dir = Path(gettempdir())
    source_path = tmp_dir / f"mtx-audio-src-{uuid.uuid4().hex}"
    output_path: Path | None = None
    try:
        await service.router.download_to_path_async(storage_uri, str(source_path))
        loop = asyncio.get_event_loop()
        codec = await loop.run_in_executor(
            None, _probe_audio_codec_sync, ffmpeg, str(source_path)
        )
        if codec is None:
            raise ValueError(
                f"File {file_id!r} contains no audio stream to extract."
            )
        plan = plan_extraction(codec)
        output_path = tmp_dir / f"mtx-audio-out-{uuid.uuid4().hex}{plan.extension}"
        await loop.run_in_executor(
            None,
            _extract_audio_sync,
            ffmpeg,
            str(source_path),
            str(output_path),
            plan,
        )
        audio_bytes = output_path.read_bytes()
    finally:
        _unlink_quietly(source_path)
        if output_path is not None:
            _unlink_quietly(output_path)

    source_name = source.get("file_name") or str(source["id"])
    stem = source_name.rsplit(".", 1)[0] or str(source["id"])
    derivation_metadata = {
        "extraction_key": cache_key,
        "source_audio_codec": codec,
        "extraction_mode": plan.mode,
        "source_checksum": source.get("checksum"),
        "source_version": source.get("current_version"),
    }
    file_path = AUDIO_EXTRACTS.path(
        str(source["id"]), f"{stem}{plan.extension}"
    )
    # Inherit the parent's whole access context — web lane, list filter, contextual-access
    # policy keys, AND organization_id via the metadata org channel; without it
    # the derivative lands in the writer's PERSONAL org (wrong tenant for any
    # org-owned parent).
    owner_id = str(source.get("created_by") or user_id)
    access, write_metadata = inherit_derived_file_policy(
        source,
        {
            "parent_file_id": str(source["id"]),
            "derivation_kind": AUDIO_EXTRACTED_KIND,
            **derivation_metadata,
        },
    )
    written = await service.sync_engine.managed_write_async(
        file_path,
        audio_bytes,
        mime_type=plan.mime_type,
        published_to_web=access.published_to_web,
        shown_to=access.shown_to,
        change_summary=f"Extracted audio ({plan.mode}) from {source_name}",
        metadata=write_metadata,
        user_id=owner_id,
        parent_file_id=str(source["id"]),
        derivation_kind=AUDIO_EXTRACTED_KIND,
        derivation_metadata=derivation_metadata,
    )
    derivative = await service.db.get_file_async(written.file_id)
    if derivative is None:
        raise RuntimeError(
            f"Audio derivative {written.file_id!r} was written but cannot be loaded."
        )

    return AudioExtractionResult(
        source_file_id=str(source["id"]),
        audio_codec=codec,
        extraction_mode=plan.mode,
        cache_hit=False,
        file=await service.build_file_ref(derivative),
    )


def _unlink_quietly(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


__all__ = [
    "AUDIO_EXTRACTED_KIND",
    "AudioExtractionRequest",
    "AudioExtractionResult",
    "ExtractionPlan",
    "extract_audio",
    "extraction_cache_key",
    "extraction_ffmpeg_args",
    "plan_extraction",
]
