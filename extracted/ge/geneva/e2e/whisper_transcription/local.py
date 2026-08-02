# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Run the Whisper transcription pipeline entirely locally.

Example:
    cd e2e/whisper_transcription
    uv run python local.py --row-limit 10 --num-clips 2 --checkpoint-size 8
"""

from __future__ import annotations

import argparse
import importlib.util
import logging
import os
import uuid
from pathlib import Path

from dataset import load_audio_samples
from pipeline import run_pipeline

import geneva
from geneva.cluster import GenevaCluster

_LOG = logging.getLogger(__name__)


def _ensure_local_dependencies() -> None:
    required = [
        "datasets",
        "soundfile",
        "scipy",
        "torch",
        "transformers",
        "sentence_transformers",
    ]
    missing = [name for name in required if importlib.util.find_spec(name) is None]
    if not missing:
        return

    missing_list = ", ".join(missing)
    raise RuntimeError(
        "Missing local dependencies for the Whisper pipeline: "
        f"{missing_list}. LOCAL_RAY does not use manifests, so these must be "
        "installed in the current environment."
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Whisper pipeline locally")
    parser.add_argument(
        "--db-path",
        default=str(Path(".local/whisper_transcription").resolve()),
        help="Local directory for the Geneva database",
    )
    parser.add_argument(
        "--row-limit",
        type=int,
        default=5,
        help="Number of dataset rows to process",
    )
    parser.add_argument(
        "--num-clips",
        type=int,
        default=5,
        help="Number of clips (30s chunks) to process per audio file",
    )
    parser.add_argument(
        "--checkpoint-size",
        type=int,
        default=2,
        help="Backfill checkpoint size",
    )
    parser.add_argument(
        "--cluster-name",
        default="local-whisper-transcription",
        help="Cluster name for the local Ray runtime",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    args = _parse_args()

    _ensure_local_dependencies()
    from geneva.udfs.audio.whisper_transcription import download_audio  # noqa: PLC0415

    db_path = Path(args.db_path).expanduser().absolute()
    db_path.mkdir(parents=True, exist_ok=True)

    conn = geneva.connect(db_path)
    cluster = GenevaCluster.create_local(args.cluster_name).build()
    conn.define_cluster(args.cluster_name, cluster)

    metadata = load_audio_samples(args.row_limit, args.num_clips)
    if len(metadata) == 0:
        raise RuntimeError("No audio metadata available to build a test table")

    table_name = f"whisper_transcription_{uuid.uuid4().hex}"
    tbl = conn.create_table(table_name, metadata, mode="overwrite")
    _LOG.info(
        "Created table '%s' with %s rows and columns %s",
        table_name,
        len(tbl),
        tbl.schema.names,
    )

    os.environ["GENEVA_TABLE_NAME"] = table_name

    _LOG.info("Adding audio_bytes UDF column")
    tbl.add_columns({"audio_bytes": download_audio})

    chunk_tbl, chunk_table_name = run_pipeline(
        tbl, conn, args.cluster_name, None, args.checkpoint_size
    )

    _LOG.info("Final chunk table: %s (rows=%s)", chunk_table_name, len(chunk_tbl))
    _LOG.info("Schema: %s", chunk_tbl.schema.names)


if __name__ == "__main__":
    main()
