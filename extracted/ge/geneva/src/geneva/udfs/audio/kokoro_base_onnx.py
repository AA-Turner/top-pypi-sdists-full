# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Kokoro Base (ONNX) batch text-to-speech UDF for Geneva.

This module wraps the Hugging Face ``NeuML/kokoro-base-onnx`` model into a
RecordBatch UDF for text-to-speech generation.

Inputs
------
- text column: string or large string (default: ``"text"``)
- speaker column: optional string; if omitted, ``speaker`` is used for all rows
- speed column: optional positive float; if omitted, ``speed`` is used for all rows

Output
------
- one waveform per input row as ``list<float32>`` at 24 kHz
- each waveform contains many audio samples; there is not more than one
  waveform output per input row

Requirements
------------
- onnxruntime (or onnxruntime-gpu for CUDA execution)
- numpy
- ttstokenizer
- soundfile (optional, for writing WAVs outside the UDF)

Model Assets
------------
Model files are expected to already exist in ``model_dir``; this module does
not auto-download assets. ``model_dir`` must contain ``model.onnx`` and
``voices.json``.
Model card and speaker list: https://huggingface.co/NeuML/kokoro-base-onnx
"""

import json
import logging
import urllib.parse
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa

from geneva.transformer import UDF, udf
from geneva.udfs.audio._onnx_utils import _extract_optional_column, _resolve_providers

_LOG = logging.getLogger(__name__)

DEFAULT_SAMPLE_RATE = 24000
DEFAULT_TEXT_COLUMN = "text"
DEFAULT_SPEAKER = "af"
DEFAULT_SPEED = 1.0
MODEL_FILENAME = "model.onnx"
VOICES_FILENAME = "voices.json"


def _extract_string_inputs(
    batch: pa.RecordBatch, column: str
) -> tuple[list[str], list[int], list[Any]]:
    """Return valid string values and row indices for ``column``."""

    index = batch.schema.get_field_index(column)
    if index == -1:
        raise ValueError(f"Column '{column}' not found in RecordBatch")

    field = batch.schema.field(index)
    if not pa.types.is_string(field.type) and not pa.types.is_large_string(field.type):
        raise TypeError(f"Column '{column}' must contain string data")

    values = batch.column(index).to_pylist()
    valid_indices: list[int] = []
    valid_texts: list[str] = []
    for idx, value in enumerate(values):
        if value is None:
            continue
        if not isinstance(value, str):
            raise TypeError(
                "Kokoro TTS UDF expects string inputs, received "
                f"{type(value).__name__}."
            )
        valid_indices.append(idx)
        valid_texts.append(value)

    return valid_texts, valid_indices, values


class _KokoroBaseTTSModel:
    """
    Lazy-loading wrapper for Kokoro Base (ONNX) inference.

    This class is designed to be picklable for Geneva workers. Heavy
    objects like the ONNX session and tokenizer are loaded lazily.
    """

    def __init__(
        self,
        model_dir: str | Path,
        text_column: str = DEFAULT_TEXT_COLUMN,
        speaker: str = DEFAULT_SPEAKER,
        speaker_column: str | None = None,
        speed: float = DEFAULT_SPEED,
        speed_column: str | None = None,
        num_gpus: float = 0.0,
        providers: Sequence[str] | None = None,
    ) -> None:
        self.model_dir = Path(model_dir).expanduser()
        self.text_column = text_column
        self.speaker = speaker
        self.speaker_column = speaker_column
        self.speed = speed
        self.speed_column = speed_column
        self.num_gpus = num_gpus
        self.providers = list(providers) if providers is not None else None

        self._session = None
        self._tokenizer = None
        self._voices = None

    def __getstate__(self) -> dict[str, Any]:
        # Pickle only configuration so Geneva workers can reconstruct runtime state.
        return {
            "model_dir": str(self.model_dir),
            "text_column": self.text_column,
            "speaker": self.speaker,
            "speaker_column": self.speaker_column,
            "speed": self.speed,
            "speed_column": self.speed_column,
            "num_gpus": self.num_gpus,
            "providers": self.providers,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        # Restore configuration from pickle payload and rebuild caches lazily.
        self.model_dir = Path(state["model_dir"]).expanduser()
        self.text_column = state["text_column"]
        self.speaker = state["speaker"]
        self.speaker_column = state["speaker_column"]
        self.speed = state["speed"]
        self.speed_column = state["speed_column"]
        self.num_gpus = state["num_gpus"]
        self.providers = state["providers"]

        # These runtime caches are process-local and rebuilt lazily after unpickle.
        self._session = None
        self._tokenizer = None
        self._voices = None

    @property
    def session(self) -> Any:
        # Worker processes are isolated, so lock-free lazy init is sufficient here.
        if self._session is None:
            self._session = self._build_session()
        return self._session

    @property
    def tokenizer(self) -> Any:
        # Worker processes are isolated, so lock-free lazy init is sufficient here.
        if self._tokenizer is None:
            self._tokenizer = self._build_tokenizer()
        return self._tokenizer

    @property
    def voices(self) -> dict[str, np.ndarray]:
        # Worker processes are isolated, so lock-free lazy init is sufficient here.
        if self._voices is None:
            self._voices = self._load_voices()
        return self._voices

    def _build_session(self) -> Any:
        try:
            import onnxruntime as ort
        except ImportError as exc:
            raise ImportError(
                "onnxruntime is required; install via `pip install onnxruntime` "
                "or `pip install onnxruntime-gpu` for CUDA."
            ) from exc

        model_path = self.model_dir / MODEL_FILENAME
        if not model_path.exists():
            raise FileNotFoundError(
                f"ONNX model not found at {model_path}. "
                "Download model.onnx from the Hugging Face repository."
            )

        providers = _resolve_providers(self.num_gpus, self.providers)
        return ort.InferenceSession(str(model_path), providers=providers)

    def _build_tokenizer(self) -> Any:
        try:
            from ttstokenizer import IPATokenizer
        except ImportError as exc:
            raise ImportError(
                "ttstokenizer is required; install via `pip install ttstokenizer`."
            ) from exc

        return IPATokenizer()

    def _load_voices(self) -> dict[str, np.ndarray]:
        voices_path = self.model_dir / VOICES_FILENAME
        if not voices_path.exists():
            raise FileNotFoundError(
                f"Voices file not found at {voices_path}. "
                "Download voices.json from the Hugging Face repository."
            )

        with voices_path.open("r", encoding="utf-8") as handle:
            voices = json.load(handle)

        converted: dict[str, np.ndarray] = {}
        for speaker_id, table in voices.items():
            converted[speaker_id] = np.asarray(table, dtype=np.float32)
        return converted

    def _select_style(self, speaker_id: str, token_length: int) -> np.ndarray:
        if speaker_id not in self.voices:
            raise ValueError(
                f"Unknown speaker '{speaker_id}'. "
                f"Available speakers: {sorted(self.voices.keys())}"
            )

        table = self.voices[speaker_id]
        if table.ndim == 3 and 1 in table.shape:
            table = np.squeeze(table)
        if table.ndim != 2:
            raise ValueError(
                "Expected speaker table to be 2D (or 3D with a singleton dim), "
                f"got shape {table.shape}"
            )

        index = min(token_length, table.shape[0] - 1)
        style = table[index]
        if style.ndim == 1:
            style = np.expand_dims(style, axis=0)
        return style

    def _synthesize_one(self, text: str, speaker_id: str, speed: float) -> list[float]:
        if speed <= 0:
            raise ValueError("speed must be a positive float")

        tokens = self.tokenizer(text)
        if len(tokens) == 0:
            return []

        tokens_array = np.array([[0, *tokens, 0]], dtype=np.int64)
        style = self._select_style(speaker_id, len(tokens))
        speed_array = np.ones(1, dtype=np.float32) * float(speed)

        outputs = self.session.run(
            None,
            {
                "tokens": tokens_array,
                "style": style,
                "speed": speed_array,
            },
        )

        audio = np.asarray(outputs[0], dtype=np.float32).squeeze()
        return audio.tolist()

    def synthesize(self, batch: pa.RecordBatch) -> pa.Array:
        texts, valid_indices, values = _extract_string_inputs(batch, self.text_column)

        speaker_values = _extract_optional_column(
            batch,
            self.speaker_column,
            str,
            self.speaker,
            "speaker",
        )
        speed_values = _extract_optional_column(
            batch,
            self.speed_column,
            (int, float),
            self.speed,
            "speed",
        )

        outputs: list[list[float] | None] = [None] * len(values)
        if texts:
            for idx, text in zip(valid_indices, texts, strict=True):
                speaker_id = speaker_values[idx]
                speed = float(speed_values[idx])
                outputs[idx] = self._synthesize_one(text, speaker_id, speed)

        return pa.array(outputs, type=pa.list_(pa.float32()))


def kokoro_base_tts_udf(
    model_dir: str | Path,
    *,
    text_column: str = DEFAULT_TEXT_COLUMN,
    speaker: str = DEFAULT_SPEAKER,
    speaker_column: str | None = None,
    speed: float = DEFAULT_SPEED,
    speed_column: str | None = None,
    num_gpus: float = 0.0,
    providers: Sequence[str] | None = None,
) -> UDF:
    """
    Build a Kokoro Base ONNX text-to-speech UDF.

    Parameters
    ----------
    model_dir:
        Path to a directory containing ``model.onnx`` and ``voices.json``.
        Files must already exist locally; this function does not download them.
    text_column:
        Name of the input text column in the RecordBatch.
    speaker:
        Default speaker id used when ``speaker_column`` is not provided.
        Supported speaker IDs come from ``voices.json`` in ``model_dir`` and are
        documented on the model card:
        https://huggingface.co/NeuML/kokoro-base-onnx
    speaker_column:
        Optional column name providing per-row speaker ids. If omitted, all rows
        use ``speaker``.
    speed:
        Default positive speed multiplier applied when ``speed_column`` is not
        provided. ``1.0`` is nominal speed, values greater than ``1.0`` are
        faster, and values between ``0`` and ``1.0`` are slower.
    speed_column:
        Optional column name providing per-row speed multipliers. If omitted,
        all rows use ``speed``.
    num_gpus:
        Geneva GPU allocation for this UDF. ``0.0`` uses CPU providers; positive
        values request CUDA providers.
    providers:
        Optional ONNX Runtime provider list. If provided, this overrides auto selection.

    Returns
    -------
    UDF
        A RecordBatch UDF that returns one waveform per row as
        ``list<float32>``.
    """

    model = _KokoroBaseTTSModel(
        model_dir=model_dir,
        text_column=text_column,
        speaker=speaker,
        speaker_column=speaker_column,
        speed=speed,
        speed_column=speed_column,
        num_gpus=num_gpus,
        providers=providers,
    )

    model_name = urllib.parse.quote_plus(str(model_dir))
    udf_name = f"kokoro-base-onnx:{model_name}"

    @udf(
        name=udf_name,
        data_type=pa.list_(pa.float32()),
        num_gpus=num_gpus,
    )
    class KokoroBaseTTSUDF:
        def __init__(self) -> None:
            self._model = model
            self.sample_rate = DEFAULT_SAMPLE_RATE

        def __call__(self, batch: pa.RecordBatch) -> pa.Array:
            return self._model.synthesize(batch)

    return KokoroBaseTTSUDF()  # type: ignore
