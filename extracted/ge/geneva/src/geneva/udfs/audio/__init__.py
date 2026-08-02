# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Audio-focused pre-built UDFs."""

from geneva.udfs.audio.kokoro_base_onnx import (
    DEFAULT_SPEAKER as KOKORO_DEFAULT_SPEAKER,
)
from geneva.udfs.audio.kokoro_base_onnx import (
    DEFAULT_SPEED as KOKORO_DEFAULT_SPEED,
)
from geneva.udfs.audio.kokoro_base_onnx import (
    DEFAULT_TEXT_COLUMN as KOKORO_DEFAULT_TEXT_COLUMN,
)
from geneva.udfs.audio.kokoro_base_onnx import (
    kokoro_base_tts_udf,
)
from geneva.udfs.audio.wavlm_tbr_onnx import (
    DEFAULT_AUDIO_COLUMN as WAVLM_DEFAULT_AUDIO_COLUMN,
)
from geneva.udfs.audio.wavlm_tbr_onnx import (
    DEFAULT_MAX_SECONDS as WAVLM_DEFAULT_MAX_SECONDS,
)
from geneva.udfs.audio.wavlm_tbr_onnx import (
    DEFAULT_SAMPLE_RATE as WAVLM_DEFAULT_SAMPLE_RATE,
)
from geneva.udfs.audio.wavlm_tbr_onnx import (
    wavlm_tbr_embedding_udf,
)
from geneva.udfs.audio.whisper_transcription import (
    ASR_BATCH_SIZE,
    ASR_INFER_BATCH_SIZE,
    CHUNK_SECONDS,
    EMBED_BATCH_SIZE,
    EMBEDDING_DIM,
    MAX_AUDIO_SECONDS,
    QWEN_EMBED_MODEL_ID,
    TARGET_SAMPLE_RATE,
    WHISPER_MODEL_ID,
    TranscriptEmbedder,
    WhisperChunkTranscriber,
    chunk_audio,
    download_audio,
)

__all__ = [
    "ASR_BATCH_SIZE",
    "ASR_INFER_BATCH_SIZE",
    "CHUNK_SECONDS",
    "EMBED_BATCH_SIZE",
    "EMBEDDING_DIM",
    "MAX_AUDIO_SECONDS",
    "QWEN_EMBED_MODEL_ID",
    "TARGET_SAMPLE_RATE",
    "WHISPER_MODEL_ID",
    "KOKORO_DEFAULT_SPEAKER",
    "KOKORO_DEFAULT_SPEED",
    "KOKORO_DEFAULT_TEXT_COLUMN",
    "WAVLM_DEFAULT_AUDIO_COLUMN",
    "WAVLM_DEFAULT_MAX_SECONDS",
    "WAVLM_DEFAULT_SAMPLE_RATE",
    "TranscriptEmbedder",
    "WhisperChunkTranscriber",
    "chunk_audio",
    "download_audio",
    "kokoro_base_tts_udf",
    "wavlm_tbr_embedding_udf",
]
