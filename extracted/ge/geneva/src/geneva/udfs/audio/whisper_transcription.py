# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
UDFs for the Whisper transcription + Qwen embedding pipeline.

Steps:
1) Download audio bytes from sources (URL or local path)
2) Decode + resample to 16kHz and chunk into 30s windows
3) Transcribe each chunk with Whisper v3 Turbo
4) Embed transcript chunks with Qwen3 Embedding
"""

from __future__ import annotations

import base64
import logging
from pathlib import Path
from typing import Any, cast

import pyarrow as pa
import requests

import geneva
from geneva import retry_all
from geneva.udfs.audio._chunking import (
    CHUNK_SECONDS,
    MAX_AUDIO_SECONDS,
    TARGET_SAMPLE_RATE,
    _chunk_samples,
    _decode_audio,
    _resample,
)

_LOG = logging.getLogger(__name__)

# todo replace with openai/whisper-large-v3-turbo, using this for faster iteration
WHISPER_MODEL_ID = "openai/whisper-tiny"

QWEN_EMBED_MODEL_ID = "Qwen/Qwen3-Embedding-0.6B"

# UDF batch size (rows per task)
ASR_BATCH_SIZE = 32
# Inference batch size (clips per forward pass)
ASR_INFER_BATCH_SIZE = 1
EMBED_BATCH_SIZE = 4_096
EMBED_INFER_BATCH_SIZE = 32
EMBEDDING_DIM = 1024

_CHUNK_STRUCT = pa.struct(
    [
        pa.field("chunk_id", pa.int32()),
        pa.field("start_sec", pa.float32()),
        pa.field("end_sec", pa.float32()),
        pa.field("samples", pa.list_(pa.float32())),
    ]
)

_EMBEDDING_TYPE = pa.list_(pa.float32(), EMBEDDING_DIM)


def _resolve_audio_source(source: str) -> str:
    if source.startswith("s3://"):
        without_scheme = source[5:]
        bucket, _, key = without_scheme.partition("/")
        return f"https://{bucket}.s3.amazonaws.com/{key}"
    if source.startswith("gs://"):
        without_scheme = source[5:]
        bucket, _, key = without_scheme.partition("/")
        return f"https://storage.googleapis.com/{bucket}/{key}"
    if source.startswith("file://"):
        return source[7:]
    return source


def _decode_data_url(source: str) -> bytes | None:
    if not source.startswith("data:"):
        return None

    try:
        header, payload = source.split(",", 1)
    except ValueError:
        return None

    if ";base64" not in header:
        return None

    try:
        return base64.b64decode(payload)
    except (ValueError, TypeError) as exc:
        _LOG.warning("Failed to decode data URL: %s", exc)
        return None


@geneva.udf(
    version="0.1",
    data_type=pa.large_binary(),
    num_cpus=2,
    num_gpus=0,
    on_error=retry_all(),
)
def download_audio(source: str) -> bytes | None:
    """Fetch audio bytes from a public URL or local path (http/s3/gs/file)."""
    if not source:
        raise ValueError("source is required for download_audio")

    data_bytes = _decode_data_url(source)
    if data_bytes is not None:
        return data_bytes

    resolved = _resolve_audio_source(source)

    try:
        path = Path(resolved)
    except Exception:
        path = None

    if path and path.exists():
        try:
            return path.read_bytes()
        except Exception as exc:  # pragma: no cover
            _LOG.warning("Failed to read %s: %s", path, exc)
            return None

    try:
        resp = requests.get(resolved, timeout=60)
        resp.raise_for_status()
        return resp.content
    except Exception as exc:  # pragma: no cover
        _LOG.warning("Failed to download %s: %s", resolved, exc)
        return None


@geneva.udf(
    version="0.1",
    data_type=pa.list_(_CHUNK_STRUCT),
    num_cpus=1,
    num_gpus=0,
    on_error=retry_all(),
)
def chunk_audio(
    audio_bytes: bytes,
    num_clips: int | None = None,
) -> list[dict[str, Any]] | None:
    """Decode audio bytes, resample to 16kHz, and chunk into 30s windows."""
    if audio_bytes is None:
        raise ValueError("audio_bytes is required for chunk_audio")

    try:
        samples, sample_rate = _decode_audio(audio_bytes)
        duration = len(samples) / float(sample_rate) if sample_rate else 0.0
        if duration > MAX_AUDIO_SECONDS:
            _LOG.info(
                "Skipping audio longer than %ss (%.2fs)", MAX_AUDIO_SECONDS, duration
            )
            return None

        samples = _resample(samples, sample_rate, TARGET_SAMPLE_RATE)
        max_clips = int(num_clips) if num_clips is not None else None
        return _chunk_samples(samples, TARGET_SAMPLE_RATE, max_clips=max_clips) or None
    except Exception as exc:  # pragma: no cover
        _LOG.warning("Failed to decode audio: %s", exc)
        return None


@geneva.udf(
    version="0.1",
    data_type=pa.large_string(),
    checkpoint_size=ASR_BATCH_SIZE,
    num_cpus=4,
    num_gpus=0,
    on_error=retry_all(),
)
class WhisperChunkTranscriber:
    """Transcribe a single audio chunk with Whisper v3 Turbo."""

    def __init__(self, model_id: str = WHISPER_MODEL_ID) -> None:
        self.model_id = model_id
        self._pipe = None

    def setup(self) -> None:
        import torch
        from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

        device = 0 if torch.cuda.is_available() else -1
        dtype = torch.float16 if device == 0 else torch.float32

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id,
            dtype=dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True,
        )
        processor = AutoProcessor.from_pretrained(self.model_id)

        self._pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            dtype=dtype,
            device=device,
        )
        self._patch_missing_num_frames()

    def _patch_missing_num_frames(self) -> None:
        if self._pipe is None:
            return

        feature_extractor = self._pipe.feature_extractor

        class _FeatureExtractorWrapper:
            def __init__(self, extractor: Any) -> None:
                self._extractor = extractor

            def __call__(self, *args: Any, **kwargs: Any) -> Any:
                processed = self._extractor(*args, **kwargs)
                if "num_frames" in processed:
                    return processed

                if "attention_mask" in processed:
                    mask = processed["attention_mask"]
                    try:
                        processed["num_frames"] = mask.sum(-1)
                        return processed
                    except Exception as exc:
                        _LOG.debug(
                            "Failed to derive num_frames from attention_mask: %s",
                            exc,
                            exc_info=True,
                        )

                try:
                    import numpy as np

                    raw = args[0]
                    if isinstance(raw, (list, tuple)):
                        lengths = [len(np.asarray(item)) for item in raw]
                        processed["num_frames"] = [
                            int(length // self._extractor.hop_length)
                            for length in lengths
                        ]
                    else:
                        processed["num_frames"] = int(
                            len(np.asarray(raw)) // self._extractor.hop_length
                        )
                except Exception:
                    _LOG.warning(
                        "Failed to derive num_frames for Whisper input; "
                        "token timestamps may be inaccurate."
                    )

                return processed

            def __getattr__(self, name: str) -> Any:
                return getattr(self._extractor, name)

        self._pipe.feature_extractor = _FeatureExtractorWrapper(feature_extractor)

    def __call__(self, samples: pa.Array) -> pa.Array:  # batched UDF
        num_rows = len(samples)
        if num_rows == 0:
            return pa.array([], type=pa.large_string())

        pipe = self._pipe
        if pipe is None:
            self.setup()
            pipe = self._pipe
        if pipe is None:  # pragma: no cover
            raise RuntimeError("Whisper pipeline failed to initialize")

        import numpy as np

        inputs: list[dict[str, Any]] = []
        row_indices: list[int] = []
        outputs: list[str | None] = [None] * num_rows

        for row_idx, sample_scalar in enumerate(samples):
            if sample_scalar is None:
                continue
            sample_list = sample_scalar.as_py()
            if not sample_list:
                continue
            inputs.append(
                {
                    "array": np.asarray(sample_list, dtype=np.float32),
                    "sampling_rate": TARGET_SAMPLE_RATE,
                }
            )
            row_indices.append(row_idx)

        if inputs:
            results: list[Any] = []
            for start in range(0, len(inputs), ASR_INFER_BATCH_SIZE):
                batch_inputs = inputs[start : start + ASR_INFER_BATCH_SIZE]
                batch_results = cast("Any", pipe)(
                    batch_inputs,
                    batch_size=ASR_INFER_BATCH_SIZE,
                    generate_kwargs={"task": "transcribe"},
                )
                if isinstance(batch_results, dict):
                    batch_results = [batch_results]
                results.extend(batch_results)

            for row_idx, result in zip(row_indices, results, strict=False):
                text = ""
                if isinstance(result, dict):
                    text = (result.get("text") or "").strip()
                outputs[row_idx] = text

        return pa.array(outputs, type=pa.large_string())


@geneva.udf(
    version="0.1",
    data_type=_EMBEDDING_TYPE,
    checkpoint_size=EMBED_BATCH_SIZE,
    num_cpus=4,
    num_gpus=0,
    on_error=retry_all(),
)
class TranscriptEmbedder:
    """Embed transcript text using Qwen3 Embedding."""

    def __init__(self, model_id: str = QWEN_EMBED_MODEL_ID) -> None:
        self.model_id = model_id
        self._model = None

    def setup(self) -> None:
        import torch
        from sentence_transformers import SentenceTransformer

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = SentenceTransformer(
            self.model_id,
            device=device,
            processor_kwargs={"padding_side": "left"},
        )

    def __call__(self, text: pa.Array) -> pa.Array:  # batched UDF
        num_rows = len(text)
        if num_rows == 0:
            return pa.array([], type=_EMBEDDING_TYPE)

        model = self._model
        if model is None:
            self.setup()
            model = self._model
        if model is None:  # pragma: no cover
            raise RuntimeError("Transcript embedding model failed to initialize")

        output: list[list[float] | None] = [None] * num_rows
        flat_texts: list[str] = []
        row_indices: list[int] = []

        for row_idx, text_scalar in enumerate(text):
            if text_scalar is None:
                continue
            text_value = text_scalar.as_py()
            if not isinstance(text_value, str) or not text_value:
                output[row_idx] = None
                continue
            flat_texts.append(text_value)
            row_indices.append(row_idx)

        if flat_texts:
            embeddings = model.encode(
                flat_texts,
                batch_size=EMBED_INFER_BATCH_SIZE,
                normalize_embeddings=True,
            )
            raw = (
                embeddings.tolist()
                if hasattr(embeddings, "tolist")
                else [list(e) for e in embeddings]
            )
            embeddings_list: list[list[float]] = raw  # type: ignore[assignment]
            for row_idx, embedding in zip(row_indices, embeddings_list, strict=False):
                output[row_idx] = embedding

        return pa.array(output, type=_EMBEDDING_TYPE)


__all__ = [
    "download_audio",
    "chunk_audio",
    "WhisperChunkTranscriber",
    "TranscriptEmbedder",
    "WHISPER_MODEL_ID",
    "QWEN_EMBED_MODEL_ID",
    "TARGET_SAMPLE_RATE",
    "CHUNK_SECONDS",
    "MAX_AUDIO_SECONDS",
    "ASR_BATCH_SIZE",
    "ASR_INFER_BATCH_SIZE",
    "EMBED_BATCH_SIZE",
    "EMBEDDING_DIM",
]
