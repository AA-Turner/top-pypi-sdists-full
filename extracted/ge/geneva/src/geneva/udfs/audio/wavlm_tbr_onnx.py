# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
WavLM TBR (ONNX) speaker-timbre embedding UDF for Geneva.

This module wraps the Hugging Face ``Orange/Speaker-wavLM-tbr`` model into a
RecordBatch UDF. It expects 16 kHz mono waveforms and returns a normalized
embedding that represents speaker voice timbre for similarity and clustering.

Inputs
------
- audio column: ``list<float32>`` mono PCM samples (default: ``"audio"``)
- sample rate column: optional int (default sample rate: ``16000``)

Output
------
- one speaker embedding vector per input row as ``list<float32>``

Requirements
------------
- onnxruntime (or onnxruntime-gpu for CUDA execution)
- numpy

Model Assets
------------
Model files are expected to already exist in ``model_dir``; this module does
not auto-download assets. ``model_dir`` must contain ``model.onnx``.
Model card: https://huggingface.co/Orange/Speaker-wavLM-tbr
"""

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

DEFAULT_AUDIO_COLUMN = "audio"
DEFAULT_SAMPLE_RATE = 16000
DEFAULT_MAX_SECONDS = 30.0
MODEL_FILENAME = "model.onnx"
DEFAULT_INPUT_NAME = "input_values"
DEFAULT_OUTPUT_NAME = "embeddings"


def _extract_audio_inputs(
    batch: pa.RecordBatch, column: str
) -> tuple[list[np.ndarray], list[int]]:
    """Return valid audio arrays and row indices for ``column``."""

    index = batch.schema.get_field_index(column)
    if index == -1:
        raise ValueError(f"Column '{column}' not found in RecordBatch")

    field = batch.schema.field(index)
    if not pa.types.is_list(field.type) and not pa.types.is_large_list(field.type):
        raise TypeError(f"Column '{column}' must contain list<float32> audio data")

    values = batch.column(index).to_pylist()
    valid_indices: list[int] = []
    valid_audio: list[np.ndarray] = []
    for idx, value in enumerate(values):
        if value is None:
            continue
        if not isinstance(value, (list, tuple, np.ndarray)):
            raise TypeError(
                f"Audio column '{column}' must contain list-like values; "
                f"received {type(value).__name__}."
            )
        audio = np.asarray(value, dtype=np.float32)
        if audio.ndim == 2:
            audio = audio.mean(axis=0)
        if audio.ndim != 1:
            raise TypeError(
                f"Audio samples must be 1D mono arrays; received shape {audio.shape}."
            )
        valid_indices.append(idx)
        valid_audio.append(audio)

    return valid_audio, valid_indices


class _WavLMTBREmbeddingModel:
    """
    Lazy-loading wrapper for WavLM TBR (ONNX) inference.

    This class is designed to be picklable for Geneva workers. The ONNX session
    is loaded lazily on first use.
    """

    def __init__(
        self,
        model_dir: str | Path,
        audio_column: str = DEFAULT_AUDIO_COLUMN,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        sample_rate_column: str | None = None,
        max_seconds: float = DEFAULT_MAX_SECONDS,
        num_gpus: float = 0.0,
        providers: Sequence[str] | None = None,
        input_name: str = DEFAULT_INPUT_NAME,
        output_name: str = DEFAULT_OUTPUT_NAME,
        embedding_dim: int | None = None,
    ) -> None:
        self.model_dir = Path(model_dir).expanduser()
        self.audio_column = audio_column
        self.sample_rate = sample_rate
        self.sample_rate_column = sample_rate_column
        self.max_seconds = max_seconds
        self.num_gpus = num_gpus
        self.providers = list(providers) if providers is not None else None
        self.input_name = input_name
        self.output_name = output_name
        self.embedding_dim = embedding_dim

        self._session = None
        self._resolved_input_name = None
        self._resolved_output_name = None

    def __getstate__(self) -> dict[str, Any]:
        # Pickle only configuration so Geneva workers can reconstruct runtime state.
        return {
            "model_dir": str(self.model_dir),
            "audio_column": self.audio_column,
            "sample_rate": self.sample_rate,
            "sample_rate_column": self.sample_rate_column,
            "max_seconds": self.max_seconds,
            "num_gpus": self.num_gpus,
            "providers": self.providers,
            "input_name": self.input_name,
            "output_name": self.output_name,
            "embedding_dim": self.embedding_dim,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        # Restore configuration from pickle payload and rebuild caches lazily.
        self.model_dir = Path(state["model_dir"]).expanduser()
        self.audio_column = state["audio_column"]
        self.sample_rate = state["sample_rate"]
        self.sample_rate_column = state["sample_rate_column"]
        self.max_seconds = state["max_seconds"]
        self.num_gpus = state["num_gpus"]
        self.providers = state["providers"]
        self.input_name = state["input_name"]
        self.output_name = state["output_name"]
        self.embedding_dim = state["embedding_dim"]

        # Runtime caches are intentionally not serialized.
        self._session = None
        self._resolved_input_name = None
        self._resolved_output_name = None

    @property
    def session(self) -> Any:
        # Worker processes are isolated, so lock-free lazy init is sufficient here.
        if self._session is None:
            self._session = self._build_session()
        return self._session

    def _build_session(self) -> Any:
        try:
            import onnxruntime as ort
        except ImportError as exc:
            raise ImportError(
                "onnxruntime is required. Install via `pip install onnxruntime`."
            ) from exc

        model_path = self.model_dir / MODEL_FILENAME
        if not model_path.exists():
            raise FileNotFoundError(f"ONNX model not found at {model_path}")

        session_options = ort.SessionOptions()
        providers = _resolve_providers(self.num_gpus, self.providers)
        return ort.InferenceSession(
            str(model_path),
            sess_options=session_options,
            providers=providers,
        )

    def _resolve_io_names(self) -> tuple[str, str]:
        if self._resolved_input_name and self._resolved_output_name:
            return self._resolved_input_name, self._resolved_output_name

        inputs = [i.name for i in self.session.get_inputs()]
        outputs = [o.name for o in self.session.get_outputs()]

        input_name = self.input_name if self.input_name in inputs else inputs[0]
        output_name = self.output_name if self.output_name in outputs else outputs[0]

        if input_name != self.input_name:
            _LOG.warning(
                "Expected input name '%s' but using '%s' from ONNX model",
                self.input_name,
                input_name,
            )
        if output_name != self.output_name:
            _LOG.warning(
                "Expected output name '%s' but using '%s' from ONNX model",
                self.output_name,
                output_name,
            )

        self._resolved_input_name = input_name
        self._resolved_output_name = output_name
        return input_name, output_name

    def _embed(self, audio: np.ndarray, sample_rate: int) -> list[float] | None:
        if audio.size == 0:
            return None

        if sample_rate != self.sample_rate:
            raise ValueError(
                f"Expected {self.sample_rate} Hz audio; received {sample_rate} Hz."
            )

        if self.max_seconds and self.max_seconds > 0:
            max_samples = int(self.max_seconds * sample_rate)
            if audio.shape[0] > max_samples:
                audio = audio[:max_samples]

        input_name, output_name = self._resolve_io_names()
        input_tensor = np.expand_dims(audio.astype(np.float32), axis=0)
        outputs = self.session.run([output_name], {input_name: input_tensor})
        embedding = outputs[0]

        if embedding.ndim != 2:
            raise ValueError(
                f"Expected ONNX output shape (batch, dim), got {embedding.shape}."
            )

        return embedding[0].astype(np.float32).tolist()

    def infer_embedding_dim(self, sample_rate: int) -> int:
        """Infer output embedding dimension from model metadata or a probe run."""

        if self.embedding_dim is not None:
            return self.embedding_dim

        inferred_dim: int | None = None
        try:
            output_shape = self.session.get_outputs()[0].shape
            if len(output_shape) >= 2 and isinstance(output_shape[1], int):
                inferred_dim = int(output_shape[1])
        except Exception:
            _LOG.debug(
                "Could not infer embedding dim from ONNX metadata",
                exc_info=True,
            )

        if inferred_dim is None:
            dummy_samples = max(1, int(sample_rate))
            dummy_audio = np.zeros(dummy_samples, dtype=np.float32)
            embedding = self._embed(dummy_audio, sample_rate)
            if embedding is None:
                raise ValueError("Unable to infer embedding dimension for ONNX model.")
            inferred_dim = len(embedding)

        self.embedding_dim = inferred_dim
        return inferred_dim

    def embed_batch(self, batch: pa.RecordBatch) -> pa.Array:
        audio_values, valid_indices = _extract_audio_inputs(batch, self.audio_column)
        sample_rates = _extract_optional_column(
            batch,
            self.sample_rate_column,
            (int,),
            self.sample_rate,
            "Sample rate",
        )

        output: list[list[float] | None] = [None] * batch.num_rows
        for audio, idx in zip(audio_values, valid_indices, strict=True):
            output[idx] = self._embed(audio, sample_rates[idx])

        embedding_dim = self.embedding_dim
        if embedding_dim is None:
            for value in output:
                if value is not None:
                    embedding_dim = len(value)
                    break
        if embedding_dim is None:
            raise ValueError("Unable to infer embedding dimension from empty batch.")

        return pa.array(
            output,
            type=pa.list_(pa.float32(), embedding_dim),
        )


def wavlm_tbr_embedding_udf(
    model_dir: str | Path,
    *,
    audio_column: str = DEFAULT_AUDIO_COLUMN,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    sample_rate_column: str | None = None,
    max_seconds: float = DEFAULT_MAX_SECONDS,
    num_gpus: float = 0.0,
    providers: Sequence[str] | None = None,
    input_name: str = DEFAULT_INPUT_NAME,
    output_name: str = DEFAULT_OUTPUT_NAME,
    embedding_dim: int | None = None,
) -> UDF:
    """
    Build a WavLM TBR ONNX UDF that emits speaker-timbre embeddings per row.

    Parameters
    ----------
    model_dir:
        Path to a directory containing ``model.onnx``.
        Files must already exist locally; this function does not download them.
    audio_column:
        Name of the input audio column in the RecordBatch. Values must be
        mono waveforms encoded as ``list<float32>``.
    sample_rate:
        Expected audio sample rate in Hz.
    sample_rate_column:
        Optional column name providing per-row sample rates. If omitted, all
        rows use ``sample_rate``.
    max_seconds:
        Maximum audio duration to process per row. Audio longer than this is
        truncated. Set to ``0`` or a negative value to disable truncation.
    num_gpus:
        Geneva GPU allocation for this UDF. ``0.0`` uses CPU providers; positive
        values request CUDA providers.
    providers:
        Optional ONNX Runtime provider list. If provided, this overrides auto selection.
    input_name:
        Expected ONNX input tensor name. If missing in the model graph, the
        first model input is used.
    output_name:
        Expected ONNX output tensor name. If missing in the model graph, the
        first model output is used.
    embedding_dim:
        Optional fixed embedding dimension. If omitted, dimension is inferred
        from ONNX metadata or a probe run.

    Returns
    -------
    UDF
        A RecordBatch UDF that returns one speaker-timbre embedding vector per
        row as ``list<float32>``.
    """

    model = _WavLMTBREmbeddingModel(
        model_dir=model_dir,
        audio_column=audio_column,
        sample_rate=sample_rate,
        sample_rate_column=sample_rate_column,
        max_seconds=max_seconds,
        num_gpus=num_gpus,
        providers=providers,
        input_name=input_name,
        output_name=output_name,
        embedding_dim=embedding_dim,
    )

    model_name = urllib.parse.quote_plus(str(model_dir))
    udf_name = f"wavlm-tbr-onnx:{model_name}"

    inferred_dim = (
        embedding_dim
        if embedding_dim is not None
        else model.infer_embedding_dim(sample_rate)
    )

    @udf(
        name=udf_name,
        data_type=pa.list_(pa.float32(), inferred_dim),
        num_gpus=num_gpus,
    )
    class WavLMTBREmbeddingUDF:
        def __init__(self) -> None:
            self._model = model
            self.sample_rate = sample_rate

        def __call__(self, batch: pa.RecordBatch) -> pa.Array:
            return self._model.embed_batch(batch)

    return WavLMTBREmbeddingUDF()  # type: ignore
