from __future__ import annotations

import logging

_LOG = logging.getLogger(__name__)

CHUNK_COLUMNS = ["text", "embedding"]


def _log_counts(tbl, label: str, checks: list[tuple[str, str]]) -> None:
    try:
        total = tbl.count_rows()
    except Exception as exc:  # pragma: no cover
        _LOG.warning("Failed to count rows for %s: %s", label, exc)
        return

    parts = [f"total={total}"]
    for name, where in checks:
        try:
            count = tbl.count_rows(filter=where)
        except Exception as exc:  # pragma: no cover
            _LOG.warning("Failed to count %s for %s: %s", name, label, exc)
            continue
        parts.append(f"{name}={count}")

    _LOG.info("%s counts: %s", label, ", ".join(parts))


def run_pipeline(
    tbl, conn, cluster_name: str, manifest_name: str | None, checkpoint_size: int
) -> tuple[object, str]:
    """Run the Whisper pipeline and return the chunk-level table.

    Stage 1: Backfill ``audio_bytes`` on the source table.
    Stage 2: Create a scalar-UDTF materialized view that expands each source
             row into per-chunk rows via ``chunk_audio_udtf``, then refresh it.
    Stage 3: Add ``text`` and ``embedding`` columns on the chunk view and
             backfill them.
    """
    from geneva.chunkers import chunk_audio_udtf

    # Use 5-second chunks so LibriSpeech clips (5-15s) produce multiple
    # chunks per source row, exercising the 1:N UDTF expansion.
    chunker = chunk_audio_udtf(chunk_seconds=5)

    _LOG.info(
        "Connecting to cluster %s and beginning to backfill audio_bytes...",
        cluster_name,
    )

    # Use a single cluster context for all stages so that the manifest zips
    # remain available throughout the entire pipeline run.
    with conn.context(cluster=cluster_name, manifest=manifest_name):
        # Stage 1: backfill audio_bytes on the source table
        _LOG.info("Backfilling column audio_bytes")
        tbl.backfill("audio_bytes", concurrency=4, checkpoint_size=checkpoint_size)

        _log_counts(
            tbl,
            "Source table (post-audio)",
            [("audio_bytes", "audio_bytes IS NOT NULL")],
        )

        # Stage 2: create chunker view for chunking and refresh
        chunk_table_name = f"{tbl.name}_chunks"
        source_query = tbl.search(None).select(
            ["clip_id", "source", "audio_bytes", "num_clips"]
        )
        chunk_tbl = conn.create_udtf_view(chunk_table_name, source_query, chunker)
        _LOG.info("Created chunker view: %s", chunk_table_name)

        chunk_tbl.refresh()
        chunk_tbl = conn.open_table(chunk_table_name)

        _LOG.info("Chunk-level view refreshed: %s", chunk_table_name)
        _log_counts(
            chunk_tbl,
            "Chunk table (post-refresh)",
            [("samples", "samples IS NOT NULL")],
        )

        # Stage 3: add transcription + embedding columns and backfill
        from geneva.udfs.audio.whisper_transcription import (
            TranscriptEmbedder,
            WhisperChunkTranscriber,
        )

        if "text" not in chunk_tbl.schema.names:
            chunk_tbl.add_columns({"text": WhisperChunkTranscriber()})
            chunk_tbl = conn.open_table(chunk_table_name)

        if "embedding" not in chunk_tbl.schema.names:
            chunk_tbl.add_columns({"embedding": TranscriptEmbedder()})
            chunk_tbl = conn.open_table(chunk_table_name)

        for col in CHUNK_COLUMNS:
            _LOG.info("Backfilling column %s", col)
            where = None
            if col == "text":
                where = "text IS NULL AND samples IS NOT NULL"
            elif col == "embedding":
                where = "embedding IS NULL AND text IS NOT NULL AND text != ''"
            chunk_tbl.backfill(
                col, concurrency=4, checkpoint_size=checkpoint_size, where=where
            )
            if col == "text":
                _log_counts(
                    chunk_tbl,
                    "Chunk table (post-text)",
                    [
                        ("text", "text IS NOT NULL"),
                        ("samples", "samples IS NOT NULL"),
                    ],
                )
            elif col == "embedding":
                _log_counts(
                    chunk_tbl,
                    "Chunk table (post-embedding)",
                    [
                        ("embedding", "embedding IS NOT NULL"),
                        ("text", "text IS NOT NULL"),
                    ],
                )

    return chunk_tbl, chunk_table_name
