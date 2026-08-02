from __future__ import annotations

import base64
import logging
import mimetypes
from pathlib import Path
from typing import Any

import pyarrow as pa

_LOG = logging.getLogger(__name__)

HF_DATASET_NAME = "openslr/librispeech_asr"
HF_DATASET_CONFIG = "clean"
HF_DATASET_SPLIT = "test"


def _extract_source(row: dict[str, Any]) -> str | None:
    audio = row.get("audio")
    if audio is not None:
        if isinstance(audio, dict):
            audio_bytes = audio.get("bytes")
            audio_path = audio.get("path") or audio.get("url") or audio.get("source")
            if audio_bytes:
                return _encode_data_url(audio_bytes, audio_path)
            if audio_path:
                path_value = str(audio_path)
                if _is_remote_path(path_value):
                    return path_value
                local_bytes = _read_local_bytes(path_value)
                if local_bytes:
                    return _encode_data_url(local_bytes, path_value)
                return path_value
        if isinstance(audio, str):
            if _is_remote_path(audio):
                return audio
            local_bytes = _read_local_bytes(audio)
            if local_bytes:
                return _encode_data_url(local_bytes, audio)
            return audio
        for attr in ("path", "url", "source"):
            value = getattr(audio, attr, None)
            if value:
                value_str = str(value)
                if _is_remote_path(value_str):
                    return value_str
                local_bytes = _read_local_bytes(value_str)
                if local_bytes:
                    return _encode_data_url(local_bytes, value_str)
                return value_str

    for key in ("file", "file_path", "path", "url"):
        value = row.get(key)
        if value:
            return str(value)

    return None


def _extract_clip_id(row: dict[str, Any], source: str | None, idx: int) -> str:
    for key in ("id", "utterance_id", "file", "file_id", "path"):
        value = row.get(key)
        if value:
            return str(value)

    if source:
        return Path(str(source)).stem or f"row-{idx}"

    return f"row-{idx}"


def _is_remote_path(path: str) -> bool:
    return path.startswith(("http://", "https://", "s3://", "gs://", "hf://"))


def _read_local_bytes(path: str) -> bytes | None:
    try:
        file_path = Path(path)
    except Exception:
        return None

    if not file_path.exists():
        return None

    try:
        return file_path.read_bytes()
    except Exception as exc:
        _LOG.warning("Failed to read audio bytes from %s: %s", path, exc)
        return None


def _encode_data_url(data: bytes, path: str | None) -> str:
    mime = None
    if path:
        suffix = Path(path).suffix.lower()
        if suffix in (".flac", ".wav", ".mp3", ".ogg", ".m4a"):
            mime = {
                ".flac": "audio/flac",
                ".wav": "audio/wav",
                ".mp3": "audio/mpeg",
                ".ogg": "audio/ogg",
                ".m4a": "audio/mp4",
            }.get(suffix)
    if not mime:
        mime, _ = mimetypes.guess_type(path or "")
    if not mime:
        mime = "application/octet-stream"

    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _load_hf_dataset():  # noqa: ANN001
    try:
        from datasets import load_dataset
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "The 'datasets' package is required to load Hugging Face datasets. "
            "Add it to e2e/whisper_transcription/pyproject.toml."
        ) from exc

    dataset = load_dataset(
        HF_DATASET_NAME,
        HF_DATASET_CONFIG,
        split=HF_DATASET_SPLIT,
        streaming=True,
    )
    try:
        from datasets import Audio

        features = getattr(dataset, "features", None)
        if features and "audio" in features:
            dataset = dataset.cast_column("audio", Audio(decode=False))
    except Exception as exc:
        _LOG.warning("Failed to disable audio decoding: %s", exc)

    return dataset


def load_audio_samples(row_limit: int, num_clips: int) -> pa.Table:
    """
    Return a PyArrow table containing LibriSpeech audio sources.

    Args:
        row_limit: Maximum number of rows to include.
        num_clips: Maximum number of clips to process per audio file.

    Returns:
        PyArrow table with columns: clip_id, source, num_clips.
    """
    if row_limit <= 0:
        return pa.table({"clip_id": [], "source": [], "num_clips": []})

    dataset = _load_hf_dataset()
    rows: list[dict[str, str]] = []

    num_clips_value = int(num_clips) if num_clips is not None else None

    for idx, row in enumerate(dataset):
        if len(rows) >= row_limit:
            break

        source = _extract_source(row)
        if not source:
            _LOG.warning("Skipping row %s: missing audio source", idx)
            continue

        clip_id = _extract_clip_id(row, source, idx)
        rows.append(
            {
                "clip_id": clip_id,
                "source": source,
                "num_clips": num_clips_value,
            }
        )

    if not rows:
        _LOG.warning("No audio samples available for transcription tests")
        return pa.table({"clip_id": [], "source": [], "num_clips": []})

    if row_limit > len(rows):
        _LOG.info(
            "Requested %s rows but only %s samples are available",
            row_limit,
            len(rows),
        )

    return pa.Table.from_pylist(rows)
