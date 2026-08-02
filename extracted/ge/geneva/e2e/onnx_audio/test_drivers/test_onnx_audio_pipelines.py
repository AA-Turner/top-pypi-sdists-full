# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""E2E tests for ONNX audio pipeline helpers with synthetic local data."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import pyarrow as pa

import geneva
from e2e.onnx_audio.kokoro_base_onnx_pipeline import run_kokoro_base_tts_pipeline
from e2e.onnx_audio.wavlm_tbr_onnx_pipeline import run_wavlm_tbr_pipeline

if TYPE_CHECKING:
    from geneva.transformer import UDF


def _connect_tmp_db(tmp_path) -> geneva.Connection:  # noqa: ANN001
    db_uri = tmp_path / f"geneva_db_{uuid.uuid4().hex}"
    return geneva.connect(str(db_uri))


def _fake_kokoro_tts_udf() -> UDF:
    @geneva.udf(
        data_type=pa.list_(pa.float32()),
        version=f"test-kokoro-{uuid.uuid4().hex}",
    )
    def _udf(text: str, speaker: str) -> list[float]:
        speaker_bonus = float(len(speaker))
        base = float(len(text))
        return [base, base + speaker_bonus]

    return _udf


def _fake_speaker_embedding_udf() -> UDF:
    @geneva.udf(
        data_type=pa.list_(pa.float32(), 4),
        version=f"test-wavlm-{uuid.uuid4().hex}",
    )
    def _udf(audio: list[float], sampling_rate: int) -> list[float]:
        values = [float(v) for v in audio]
        mean_value = sum(values) / len(values)
        variance = sum((v - mean_value) ** 2 for v in values) / len(values)
        std_value = variance**0.5
        return [mean_value, std_value, float(len(values)), float(sampling_rate)]

    return _udf


def test_kokoro_pipeline_backfills_audio(
    tmp_path,  # noqa: ANN001
) -> None:
    conn = _connect_tmp_db(tmp_path)
    table = conn.create_table(
        f"kokoro_pipeline_{uuid.uuid4().hex}",
        data=[
            {"text": "hello world", "speaker": "af", "speed": 1.0},
            {"text": "goodbye", "speaker": "bf", "speed": 0.8},
        ],
        mode="overwrite",
    )

    with conn.local_ray_context():
        run_kokoro_base_tts_pipeline(
            table,
            tts_udf=_fake_kokoro_tts_udf(),
            output_column="speech",
            checkpoint_size=2,
            concurrency=1,
        )

    frame = table.to_pandas()
    assert "speech" in frame.columns

    non_null_audio = frame["speech"].dropna()
    assert len(non_null_audio) == 2

    first_audio = non_null_audio.iloc[0]
    assert len(first_audio) == 2
    assert first_audio[0] > 0.0


def test_wavlm_pipeline_backfills_and_indexes_embeddings(
    tmp_path,  # noqa: ANN001
) -> None:
    conn = _connect_tmp_db(tmp_path)
    rows: list[dict[str, object]] = []
    for idx in range(32):
        base = float(idx + 1)
        audio = [base * 0.01 + (j * 0.001) for j in range(200)]
        rows.append({"audio": audio, "sampling_rate": 16000})
    table = conn.create_table(
        f"speaker_pipeline_{uuid.uuid4().hex}",
        data=rows,
        mode="overwrite",
    )

    with conn.local_ray_context():
        run_wavlm_tbr_pipeline(
            table,
            embedding_udf=_fake_speaker_embedding_udf(),
            embedding_column="embedding",
            checkpoint_size=4,
            concurrency=1,
            create_index=True,
            index_type="IVF_FLAT",
            num_partitions=1,
            num_sub_vectors=None,
        )

    frame = table.to_pandas()
    assert "embedding" in frame.columns

    non_null_embeddings = frame["embedding"].dropna()
    assert len(non_null_embeddings) == len(frame)

    first_embedding = non_null_embeddings.iloc[0]
    assert len(first_embedding) == 4

    indices = table.list_indices()
    assert len(indices) > 0

    query_vector = [float(value) for value in first_embedding]
    results = (
        table.search(query_vector, vector_column_name="embedding")
        .limit(5)
        .to_list()
    )
    assert len(results) > 0
