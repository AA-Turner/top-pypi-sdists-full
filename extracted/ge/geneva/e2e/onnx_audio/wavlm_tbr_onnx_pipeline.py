# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Pipeline helpers for WavLM TBR ONNX speaker-embedding workflows."""

from __future__ import annotations

import argparse
import contextlib
from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Any

import numpy as np

import geneva
from e2e.onnx_audio._pipeline_utils import _default_local_context, _open_or_create_table
from geneva.udfs.audio.wavlm_tbr_onnx import wavlm_tbr_embedding_udf

if TYPE_CHECKING:
    from geneva.transformer import UDF

DEFAULT_DATASET = "openslr/librispeech_asr"
DEFAULT_CONFIG = "clean"
DEFAULT_SPLIT = "test"
DEFAULT_NUM_SPEAKERS = 4
DEFAULT_SAMPLES_PER_SPEAKER = 100
DEFAULT_SEED = 13
DEFAULT_SAMPLE_RATE = 16000
DEFAULT_TABLE = "librispeech_speaker_embeddings"
DEFAULT_AUDIO_COLUMN = "audio"
DEFAULT_SR_COLUMN = "sampling_rate"
DEFAULT_EMBED_COLUMN = "embedding"
DEFAULT_MANIFEST_NAME = "speaker-wavlm-tbr-onnx-udf"


def ensure_manifest(conn: geneva.Connection, manifest_name: str) -> None:
    """Define a manifest suitable for running the WavLM UDF on remote workers."""
    from geneva.manifest.builder import GenevaManifestBuilder

    manifest = (
        GenevaManifestBuilder.create(manifest_name)
        .pip(
            [
                "numpy>=1.26",
                "onnxruntime>=1.17,<1.24",
            ]
        )
        .build()
    )
    conn.define_manifest(manifest_name, manifest)


def _load_dataset(
    dataset: str,
    config: str,
    split: str,
    cache_dir: str | None,
) -> Any:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise ImportError(
            "The `datasets` library is required. Install via `pip install datasets`."
        ) from exc

    ds = load_dataset(dataset, config, split=split, cache_dir=cache_dir, streaming=True)
    return ds.decode(False)


def _sample_rows_single_pass(
    dataset: Any,
    *,
    samples_per_speaker: int,
    seed: int,
    num_speakers: int,
) -> list[dict[str, Any]]:
    """Single-pass reservoir sampling over a streaming LibriSpeech iterator."""

    sample_rng = np.random.default_rng(seed + 1)
    speaker_counts: dict[int, int] = {}
    reservoirs: dict[int, list[dict[str, Any]]] = {}

    for row in dataset:
        raw_speaker = row.get("speaker_id")
        if raw_speaker is None:
            continue
        speaker_id = int(raw_speaker)
        speaker_counts[speaker_id] = speaker_counts.get(speaker_id, 0) + 1

        reservoir = reservoirs.setdefault(speaker_id, [])
        if len(reservoir) < samples_per_speaker:
            reservoir.append(row)
            continue

        choice = sample_rng.integers(0, speaker_counts[speaker_id])
        if choice < samples_per_speaker:
            reservoir[choice] = row

    eligible = [
        speaker_id
        for speaker_id, count in speaker_counts.items()
        if count >= samples_per_speaker
    ]
    if len(eligible) < num_speakers:
        raise ValueError(
            f"Only {len(eligible)} speakers have >= {samples_per_speaker} samples; "
            f"requested {num_speakers}."
        )

    select_rng = np.random.default_rng(seed)
    selected_speakers = select_rng.choice(eligible, size=num_speakers, replace=False)

    rows: list[dict[str, Any]] = []
    for raw_speaker_id in selected_speakers.tolist():
        speaker_id = int(raw_speaker_id)
        samples = reservoirs.get(speaker_id, [])
        if len(samples) != samples_per_speaker:
            raise ValueError(
                "Not enough samples for selected speaker "
                f"{speaker_id}: {len(samples)}"
            )
        rows.extend(samples)

    sample_rng.shuffle(rows)
    return rows


def _decode_audio(record: dict[str, Any], sample_rate: int) -> tuple[np.ndarray, int]:
    try:
        import soundfile as sf
    except ImportError as exc:
        raise ImportError(
            "soundfile is required for audio decoding; "
            "install via `pip install soundfile`."
        ) from exc

    audio = record.get("audio")
    if audio is None:
        raise ValueError("Missing audio data in record.")

    data = None
    sr = None
    if isinstance(audio, dict):
        audio_bytes = audio.get("bytes")
        audio_path = audio.get("path")
        if audio_bytes:
            import io

            with sf.SoundFile(io.BytesIO(audio_bytes)) as file:
                sr = file.samplerate
                data = file.read(dtype="float32")
        elif audio_path:
            with sf.SoundFile(audio_path) as file:
                sr = file.samplerate
                data = file.read(dtype="float32")
    elif isinstance(audio, str):
        with sf.SoundFile(audio) as file:
            sr = file.samplerate
            data = file.read(dtype="float32")

    if data is None or sr is None:
        raise ValueError("Unable to decode audio; missing path or bytes.")

    if data.ndim == 2:
        data = data.mean(axis=0)

    if sr != sample_rate:
        raise ValueError(
            f"Expected {sample_rate} Hz audio; decoded {sr} Hz. "
            "Resample the dataset to 16 kHz before running."
        )

    return data.astype(np.float32), int(sr)


def _build_rows(
    records: list[dict[str, Any]],
    sample_rate: int,
    audio_column: str,
    sample_rate_column: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for idx, row in enumerate(records):
        audio_array, decoded_sr = _decode_audio(row, sample_rate)
        rows.append(
            {
                "row_id": idx,
                "id": row.get("id"),
                "speaker_id": row.get("speaker_id"),
                "chapter_id": row.get("chapter_id"),
                "file": row.get("file"),
                "text": row.get("text"),
                audio_column: audio_array.tolist(),
                sample_rate_column: decoded_sr,
            }
        )
    return rows


def build_librispeech_rows(
    *,
    dataset: str = DEFAULT_DATASET,
    config: str = DEFAULT_CONFIG,
    split: str = DEFAULT_SPLIT,
    cache_dir: str | None = None,
    seed: int = DEFAULT_SEED,
    num_speakers: int = DEFAULT_NUM_SPEAKERS,
    samples_per_speaker: int = DEFAULT_SAMPLES_PER_SPEAKER,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    audio_column: str = DEFAULT_AUDIO_COLUMN,
    sample_rate_column: str = DEFAULT_SR_COLUMN,
) -> list[dict[str, Any]]:
    """Sample LibriSpeech records and return table rows."""
    dataset_iter = _load_dataset(dataset, config, split, cache_dir)
    sampled_records = _sample_rows_single_pass(
        dataset_iter,
        samples_per_speaker=samples_per_speaker,
        seed=seed,
        num_speakers=num_speakers,
    )
    return _build_rows(
        sampled_records,
        sample_rate,
        audio_column,
        sample_rate_column,
    )


def ensure_table(
    conn: geneva.Connection,
    table_name: str,
    rows: list[dict[str, Any]],
) -> geneva.Table:
    """Create or open a table for speaker-embedding runs."""
    return _open_or_create_table(conn, table_name, rows)


def run_wavlm_tbr_pipeline(
    table: geneva.Table,
    *,
    model_dir: str | None = None,
    embedding_udf: UDF | None = None,
    audio_column: str = DEFAULT_AUDIO_COLUMN,
    sample_rate_column: str = DEFAULT_SR_COLUMN,
    embedding_column: str = DEFAULT_EMBED_COLUMN,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    max_seconds: float = 30.0,
    num_gpus: float = 0.0,
    checkpoint_size: int = 8,
    concurrency: int = 4,
    rebind_udf: bool = True,
    create_index: bool = True,
    index_type: str = "IVF_PQ",
    metric: str = "cosine",
    num_partitions: int | None = None,
    num_sub_vectors: int | None = 128,
    replace_index: bool = True,
    context: AbstractContextManager[None] | None = None,
) -> geneva.Table:
    """
    Add/update a WavLM embedding column, backfill it, and optionally index it.

    Pass either ``model_dir`` (to build the ONNX UDF) or ``embedding_udf`` (for
    testing/custom UDF implementations).
    """
    if embedding_udf is None:
        if model_dir is None:
            raise ValueError("Either model_dir or embedding_udf must be provided")
        embedding_udf = wavlm_tbr_embedding_udf(
            model_dir=model_dir,
            audio_column=audio_column,
            sample_rate=sample_rate,
            sample_rate_column=sample_rate_column,
            max_seconds=max_seconds,
            num_gpus=num_gpus,
        )

    if embedding_column not in table.schema.names:
        table.add_columns({embedding_column: embedding_udf})
    elif rebind_udf:
        table.alter_columns({"path": embedding_column, "udf": embedding_udf})

    active_context = context or contextlib.nullcontext()
    with active_context:
        table.backfill(
            embedding_column,
            checkpoint_size=checkpoint_size,
            concurrency=concurrency,
        )

    if create_index:
        index_kwargs: dict[str, Any] = {
            "metric": metric,
            "vector_column_name": embedding_column,
            "replace": replace_index,
            "index_type": index_type,
        }
        if num_partitions is not None:
            index_kwargs["num_partitions"] = num_partitions
        if num_sub_vectors is not None and "PQ" in index_type:
            index_kwargs["num_sub_vectors"] = num_sub_vectors
        table.create_index(**index_kwargs)

    return table


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-uri", default="./db", help="Geneva database URI")
    parser.add_argument("--table", default=DEFAULT_TABLE, help="Table name")
    parser.add_argument(
        "--model-dir",
        required=True,
        help="Directory containing model.onnx",
    )
    parser.add_argument(
        "--dataset",
        default=DEFAULT_DATASET,
        help="Hugging Face dataset name",
    )
    parser.add_argument(
        "--dataset-cache-dir",
        default=None,
        help="Optional Hugging Face cache directory",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Random seed for speaker sampling",
    )
    parser.add_argument(
        "--num-speakers",
        type=int,
        default=DEFAULT_NUM_SPEAKERS,
        help="Number of speakers to sample",
    )
    parser.add_argument(
        "--samples-per-speaker",
        type=int,
        default=DEFAULT_SAMPLES_PER_SPEAKER,
        help="Number of utterances per speaker",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=DEFAULT_SAMPLE_RATE,
        help="Target sample rate for audio",
    )
    parser.add_argument(
        "--audio-column",
        default=DEFAULT_AUDIO_COLUMN,
        help="Audio column name",
    )
    parser.add_argument(
        "--sample-rate-column",
        default=DEFAULT_SR_COLUMN,
        help="Sample rate column name",
    )
    parser.add_argument(
        "--embedding-column",
        default=DEFAULT_EMBED_COLUMN,
        help="Embedding output column name",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=30.0,
        help="Truncate audio longer than this many seconds",
    )
    parser.add_argument("--num-gpus", type=float, default=0.0, help="GPU fraction")
    parser.add_argument(
        "--checkpoint-size",
        "--batch-size",
        action="store",
        dest="checkpoint_size",
        type=int,
        default=8,
        help="Backfill checkpoint size",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="Backfill concurrency",
    )
    parser.add_argument(
        "--cluster",
        default=None,
        help="Optional cluster name for remote execution",
    )
    parser.add_argument(
        "--manifest-name",
        default=None,
        help="Manifest name to use when running on a cluster",
    )
    parser.add_argument(
        "--define-manifest",
        action="store_true",
        help="Define/update the manifest before running",
    )
    parser.add_argument(
        "--no-create-table",
        action="store_true",
        help="Do not create a dataset-backed table when missing",
    )
    parser.add_argument(
        "--no-rebind-udf",
        action="store_true",
        help="Do not alter an existing embedding column to the latest UDF",
    )
    parser.add_argument(
        "--skip-index",
        action="store_true",
        help="Skip creating a vector index",
    )
    parser.add_argument(
        "--index-type",
        default="IVF_PQ",
        choices=["IVF_FLAT", "IVF_PQ", "IVF_HNSW_SQ", "IVF_HNSW_PQ"],
        help="Vector index type",
    )
    parser.add_argument(
        "--metric",
        default="cosine",
        help="Vector index distance metric",
    )
    parser.add_argument(
        "--num-partitions",
        type=int,
        default=None,
        help="Number of IVF partitions",
    )
    parser.add_argument(
        "--num-sub-vectors",
        type=int,
        default=128,
        help="Number of PQ sub-vectors",
    )
    parser.add_argument(
        "--no-replace-index",
        action="store_true",
        help="Do not replace an existing vector index",
    )
    args = parser.parse_args()

    conn = geneva.connect(args.db_uri)

    if args.no_create_table:
        table = conn.open_table(args.table)
    else:
        rows = build_librispeech_rows(
            dataset=args.dataset,
            config=DEFAULT_CONFIG,
            split=DEFAULT_SPLIT,
            cache_dir=args.dataset_cache_dir,
            seed=args.seed,
            num_speakers=args.num_speakers,
            samples_per_speaker=args.samples_per_speaker,
            sample_rate=args.sample_rate,
            audio_column=args.audio_column,
            sample_rate_column=args.sample_rate_column,
        )
        table = ensure_table(conn, args.table, rows)

    context: AbstractContextManager[None]
    if args.cluster:
        manifest_name = args.manifest_name or DEFAULT_MANIFEST_NAME
        if args.define_manifest or args.manifest_name is None:
            ensure_manifest(conn, manifest_name)
        context = conn.context(cluster=args.cluster, manifest=manifest_name)
    else:
        context = _default_local_context(conn)

    run_wavlm_tbr_pipeline(
        table,
        model_dir=args.model_dir,
        audio_column=args.audio_column,
        sample_rate_column=args.sample_rate_column,
        embedding_column=args.embedding_column,
        sample_rate=args.sample_rate,
        max_seconds=args.max_seconds,
        num_gpus=args.num_gpus,
        checkpoint_size=args.checkpoint_size,
        concurrency=args.concurrency,
        rebind_udf=not args.no_rebind_udf,
        create_index=not args.skip_index,
        index_type=args.index_type,
        metric=args.metric,
        num_partitions=args.num_partitions,
        num_sub_vectors=args.num_sub_vectors,
        replace_index=not args.no_replace_index,
        context=context,
    )


if __name__ == "__main__":
    main()
