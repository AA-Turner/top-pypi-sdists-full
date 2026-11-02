"""Durable sink: fire-and-forget write of the full event to S3.

Each event lands as one JSON object under the raw prefix:

    s3://<bucket>/<raw_prefix>dt=YYYY-MM-DD/<call_id>.json

A nightly compaction job rolls each day's raw objects into one Parquet file
under the curated prefix. Writes are best-effort and never block or fail the
tool call. Oversized fields are spilled to an overflow object so a single huge
response (e.g. a big kubectl dump) can't bloat every curated row, without losing
the data.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import boto3

from cube_cloud.config import settings
from cube_cloud.telemetry.events import ToolCallEvent

logger = logging.getLogger(__name__)

_s3_client = None


def _client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3", region_name=settings.aws_region)
    return _s3_client


def _cap_response(event: ToolCallEvent) -> tuple[dict[str, Any], str | None]:
    """Return (event_dict, overflow_body). If the response exceeds the ceiling,
    clip the stored copy, flag it, and return the full body to spill. The row's
    `response_size_bytes` already holds the true full size, so it is left as-is."""
    body = event.to_dict()
    ceiling = settings.telemetry_field_max_bytes
    full = event.response or ""
    encoded = full.encode("utf-8")
    if len(encoded) <= ceiling:
        return body, None

    body["response"] = encoded[:ceiling].decode("utf-8", errors="ignore")
    body["response_truncated"] = True
    return body, full


def emit(event: ToolCallEvent) -> None:
    """Schedule the S3 write without blocking. Swallows all errors."""
    if not settings.telemetry_bucket:
        logger.debug("telemetry: no bucket configured, skipping S3 archive")
        return

    body, overflow = _cap_response(event)
    payload = json.dumps(body, default=str, separators=(",", ":")).encode("utf-8")
    raw_key = f"{settings.telemetry_raw_prefix}dt={event.dt}/{event.call_id}.json"
    overflow_key = (
        f"{settings.telemetry_overflow_prefix}dt={event.dt}/{event.call_id}.txt"
        if overflow is not None
        else None
    )

    def _put() -> None:
        try:
            client = _client()
            if overflow_key is not None:
                client.put_object(
                    Bucket=settings.telemetry_bucket,
                    Key=overflow_key,
                    Body=overflow.encode("utf-8"),
                    ContentType="text/plain",
                )
            client.put_object(
                Bucket=settings.telemetry_bucket,
                Key=raw_key,
                Body=payload,
                ContentType="application/json",
            )
        except Exception:
            logger.exception("telemetry: S3 archive write failed")

    try:
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, _put)  # fire-and-forget
    except RuntimeError:
        # No running loop (batch/tests) — write synchronously.
        _put()
