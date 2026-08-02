# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Pipeline helpers for Kokoro Base ONNX text-to-speech workflows."""

from __future__ import annotations

import argparse
import contextlib
import logging
from contextlib import AbstractContextManager
from pathlib import Path
from typing import TYPE_CHECKING, Any

import geneva
from e2e.onnx_audio._pipeline_utils import _default_local_context, _open_or_create_table
from geneva.udfs.audio.kokoro_base_onnx import kokoro_base_tts_udf

if TYPE_CHECKING:
    from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)

DEFAULT_SAMPLE_RATE = 24000
DEFAULT_TABLE = "kokoro_tts_demo"
DEFAULT_OUTPUT_COLUMN = "speech"
DEFAULT_MANIFEST_NAME = "kokoro-base-onnx-udf"


def create_kokoro_demo_rows() -> list[dict[str, Any]]:
    """Return demo rows used by the CLI entrypoint."""
    return [
        {
            "id": 1,
            "text": "Hello from Geneva. This is Kokoro Base speaking.",
            "speaker": "af",
            "speed": 1.0,
        },
        {
            "id": 2,
            "text": "Batch inference lets you scale text to speech across a dataset.",
            "speaker": "af",
            "speed": 0.9,
        },
        {
            "id": 3,
            "text": "You can override the speaker and speed per row.",
            "speaker": "af",
            "speed": 1.1,
        },
        {
            "id": 4,
            "text": "I'm sorry Dave, I'm afraid I can't do that.",
            "speaker": "bm_lewis",
            "speed": 0.8,
        },
    ]


def ensure_kokoro_demo_table(
    conn: geneva.Connection,
    table_name: str,
) -> geneva.Table:
    """Create or open the Kokoro demo table."""
    return _open_or_create_table(conn, table_name, create_kokoro_demo_rows())


def ensure_nltk_resources() -> None:
    """Best-effort download of tokenizer resources required by ``ttstokenizer``."""
    try:
        import nltk
    except ImportError:
        return

    try:
        nltk.data.find("corpora/cmudict")
    except LookupError:
        nltk.download("cmudict", quiet=True)

    try:
        nltk.data.find("taggers/averaged_perceptron_tagger_eng")
    except LookupError:
        nltk.download("averaged_perceptron_tagger_eng", quiet=True)


def ensure_manifest(conn: geneva.Connection, manifest_name: str) -> None:
    """Define a manifest suitable for running the Kokoro UDF on remote workers."""
    from geneva.manifest.builder import GenevaManifestBuilder

    manifest = (
        GenevaManifestBuilder.create(manifest_name)
        .pip(
            [
                "nltk>=3.8",
                "numpy>=1.26",
                "onnxruntime>=1.17,<1.24",
                "soundfile>=0.12",
                "ttstokenizer>=1.1,<2",
            ]
        )
        .build()
    )
    conn.define_manifest(manifest_name, manifest)


def _write_wavs(
    table: geneva.Table,
    column: str,
    out_dir: Path,
    max_rows: int,
) -> None:
    try:
        import soundfile as sf
    except ImportError as exc:
        raise ImportError(
            "soundfile is required for WAV output. Install via `pip install soundfile`."
        ) from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    result = table.search().select([column]).to_arrow()
    audio_values = result[column].to_pylist()

    for idx, audio in enumerate(audio_values[:max_rows]):
        if audio is None:
            continue
        output_path = out_dir / f"row_{idx}.wav"
        sf.write(output_path, audio, DEFAULT_SAMPLE_RATE)


def run_kokoro_base_tts_pipeline(
    table: geneva.Table,
    *,
    model_dir: str | Path | None = None,
    tts_udf: UDF | None = None,
    text_column: str = "text",
    speaker: str = "af",
    speaker_column: str | None = None,
    speed: float = 1.0,
    speed_column: str | None = None,
    output_column: str = DEFAULT_OUTPUT_COLUMN,
    checkpoint_size: int = 4,
    concurrency: int = 2,
    rebind_udf: bool = True,
    context: AbstractContextManager[None] | None = None,
) -> geneva.Table:
    """
    Add/update a Kokoro output column and backfill it.

    Pass either ``model_dir`` (to build a Kokoro ONNX UDF) or ``tts_udf`` (for
    testing/custom UDF implementations).
    """
    if tts_udf is None:
        if model_dir is None:
            raise ValueError("Either model_dir or tts_udf must be provided")
        tts_udf = kokoro_base_tts_udf(
            model_dir=model_dir,
            text_column=text_column,
            speaker=speaker,
            speaker_column=speaker_column,
            speed=speed,
            speed_column=speed_column,
        )

    if output_column not in table.schema.names:
        table.add_columns({output_column: tts_udf})
    elif rebind_udf:
        table.alter_columns({"path": output_column, "udf": tts_udf})

    active_context = context or contextlib.nullcontext()
    with active_context:
        table.backfill(
            output_column,
            checkpoint_size=checkpoint_size,
            concurrency=concurrency,
        )

    return table


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-uri", default="./db", help="Geneva database URI")
    parser.add_argument("--table", default=DEFAULT_TABLE, help="Table name")
    parser.add_argument(
        "--model-dir",
        required=True,
        help="Directory containing model.onnx and voices.json",
    )
    parser.add_argument("--text-column", default="text", help="Text column name")
    parser.add_argument(
        "--speaker-column",
        default=None,
        help="Optional speaker column name",
    )
    parser.add_argument(
        "--speed-column",
        default=None,
        help="Optional speed column name",
    )
    parser.add_argument(
        "--speaker",
        default="af",
        help="Default speaker id when speaker-column is not set",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Default speed when speed-column is not set",
    )
    parser.add_argument(
        "--output-column",
        default=DEFAULT_OUTPUT_COLUMN,
        help="Output column name",
    )
    parser.add_argument(
        "--checkpoint-size",
        "--batch-size",
        action="store",
        dest="checkpoint_size",
        type=int,
        default=4,
        help="Backfill checkpoint size",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=2,
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
        "--no-create-demo-table",
        action="store_true",
        help="Do not create a demo table when missing",
    )
    parser.add_argument(
        "--no-rebind-udf",
        action="store_true",
        help="Do not alter an existing output column to the latest UDF",
    )
    parser.add_argument(
        "--write-wav-dir",
        default=None,
        help="Optional output directory for WAV files",
    )
    parser.add_argument(
        "--max-wav",
        type=int,
        default=100,
        help="Maximum WAV files to write",
    )
    args = parser.parse_args()

    ensure_nltk_resources()

    conn = geneva.connect(args.db_uri)
    if args.no_create_demo_table:
        table = conn.open_table(args.table)
    else:
        table = ensure_kokoro_demo_table(conn, args.table)

    if args.speaker_column is None and "speaker" in table.schema.names:
        args.speaker_column = "speaker"
    if args.speed_column is None and "speed" in table.schema.names:
        args.speed_column = "speed"

    context: AbstractContextManager[None]
    if args.cluster:
        manifest_name = args.manifest_name or DEFAULT_MANIFEST_NAME
        if args.define_manifest or args.manifest_name is None:
            ensure_manifest(conn, manifest_name)
        context = conn.context(cluster=args.cluster, manifest=manifest_name)
    else:
        context = _default_local_context(conn)

    run_kokoro_base_tts_pipeline(
        table,
        model_dir=args.model_dir,
        text_column=args.text_column,
        speaker=args.speaker,
        speaker_column=args.speaker_column,
        speed=args.speed,
        speed_column=args.speed_column,
        output_column=args.output_column,
        checkpoint_size=args.checkpoint_size,
        concurrency=args.concurrency,
        rebind_udf=not args.no_rebind_udf,
        context=context,
    )

    if args.write_wav_dir:
        _write_wavs(table, args.output_column, Path(args.write_wav_dir), args.max_wav)


if __name__ == "__main__":
    main()
