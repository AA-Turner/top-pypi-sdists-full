"""Re-stamp Content-Type / Content-Disposition on already-written files.files objects.

Objects written before the write path stamped HTTP headers landed in S3 as
``binary/octet-stream`` with no disposition, so bare public CDN URLs download
instead of render. This backfill walks files.files, computes the definitive
headers from the SAME SSOT the write path uses
(:func:`matrx_files.content_headers.resolve_object_headers`), and
rewrites the object's headers via a server-side ``CopyObject`` REPLACE — no
bytes transferred.

Idempotent + resumable:
  * ``head_object`` compares the live headers to the desired ones; an object
    that already matches is skipped (no write).
  * Stable offset pagination over ``(created_at, id)`` — re-stamping doesn't
    mutate the ordering or any filter column, so paging is complete.
  * Bounded concurrency so we don't saturate S3.

Portable: pass a configured ``FileManager`` in. Hosts ship a tiny CLI that
bootstraps their wiring then calls ``run_restamp_headers_backfill(fm, ...)``.
DB access goes through the package's own matrx-orm models (see
``cloud_sync/db.py``).

NOTE: the interim ``_legacy_storage_uri`` column (kept for one bake cycle
after migration 007's rename of ``canonical_storage_uri`` -> ``storage_uri``)
has been dropped from the live schema, so only the authoritative
``storage_uri`` object is re-stamped now. Old frozen URLs that still point
at a path-keyed legacy object are outside this backfill's reach.
"""

from __future__ import annotations

import asyncio
import time
from os.path import basename
from typing import Any

from matrx_utils import vcprint

from ...content_headers import resolve_object_headers
from ..db import _models, _vals

# Tunables.
_BATCH_SIZE = 200
_PARALLELISM = 8

_RESTAMP_COLUMNS = (
    "id",
    "created_by",
    "storage_uri",
    "mime_type",
    "file_name",
    "file_path",
    "published_to_web",
)


async def _next_batch(
    *,
    public_only: bool,
    owner_filter: str | None,
    offset: int,
    batch_size: int,
) -> list[dict]:
    """Fetch the next page of rows by stable offset pagination.

    Re-stamping doesn't flip any column out of a predicate (unlike the rekey
    backfill), so we page by a stable ``(created_at, id)`` ordering.
    """
    mf, _ = _models()
    q = mf.Files.filter(deleted_at__isnull=True)
    if public_only:
        q = q.filter(published_to_web=True)
    if owner_filter:
        q = q.filter(created_by=owner_filter)
    rows = await (
        q.order_by("created_at", "id").offset(offset).limit(batch_size).values(*_RESTAMP_COLUMNS)
    )
    return _vals(rows)


def _split_uri(uri: str) -> tuple[str, str, str] | None:
    """Split <backend>://<bucket>/<key> into (backend, bucket, key)."""
    if "://" not in uri:
        return None
    backend, rest = uri.split("://", 1)
    if "/" not in rest:
        return None
    bucket, key = rest.split("/", 1)
    return backend, bucket, key


def _desired_file_name(row: dict[str, Any]) -> str:
    """Best filename for extension-based mime guessing when mime_type is NULL."""
    return row.get("file_name") or basename(row.get("file_path") or "") or ""


async def _restamp_one_key(
    s3_client: Any,
    bucket: str,
    key: str,
    headers: Any,
    *,
    file_id: str,
    stats: dict[str, int],
) -> None:
    """Head + compare + (if needed) REPLACE the headers on a single object."""
    try:
        head = await asyncio.to_thread(s3_client.head_object, Bucket=bucket, Key=key)
    except Exception as e:
        vcprint(
            f"[restamp] head failed file_id={file_id} key={key} err={e!r}",
            color="yellow",
        )
        stats["object_missing"] += 1
        return

    cur_type = head.get("ContentType", "") or ""
    cur_disp = head.get("ContentDisposition", "") or ""
    if cur_type == headers.content_type and cur_disp == headers.content_disposition:
        stats["already_correct"] += 1
        return

    try:
        await asyncio.to_thread(
            s3_client.copy_object,
            Bucket=bucket,
            Key=key,
            CopySource={"Bucket": bucket, "Key": key},
            MetadataDirective="REPLACE",
            ContentType=headers.content_type,
            ContentDisposition=headers.content_disposition,
        )
    except Exception as e:
        vcprint(
            f"[restamp] copy failed file_id={file_id} key={key} err={e!r}",
            color="yellow",
        )
        stats["restamp_failed"] += 1
        return

    stats["restamped"] += 1


async def _process_row(
    fm: Any,
    s3_client: Any,
    row: dict[str, Any],
    *,
    sem: asyncio.Semaphore,
    stats: dict[str, int],
) -> None:
    async with sem:
        file_id = row["id"]
        headers = resolve_object_headers(
            mime_type=row.get("mime_type"),
            file_name=_desired_file_name(row),
        )

        uri = row.get("storage_uri")
        if not uri or not uri.startswith("s3://"):
            stats["skipped_non_s3"] += 1
            return
        split = _split_uri(uri)
        if split is None:
            stats["skipped_non_s3"] += 1
            return
        _backend, bucket, key = split
        await _restamp_one_key(s3_client, bucket, key, headers, file_id=file_id, stats=stats)


async def run_restamp_headers_backfill(
    fm: Any,
    *,
    public_only: bool = False,
    owner_filter: str | None = None,
    limit: int | None = None,
) -> dict[str, int]:
    """Walk files.files and re-stamp each object's Content-Type / Disposition.

    Pass a configured FileManager (cloud_sync set up). ``public_only=True``
    restricts to rows published to the web (the ones served via bare CDN
    URLs — heal these first).
    """
    if fm is None or fm.sync_engine is None:
        raise RuntimeError("cloud sync not configured — pass a FileManager with sync_engine set")
    if not fm.sync_engine._router.is_configured("s3"):
        raise RuntimeError("S3 backend not configured — cannot re-stamp object headers")

    s3_client = fm.sync_engine._router.s3._get_client()

    sem = asyncio.Semaphore(_PARALLELISM)
    stats: dict[str, int] = {
        "restamped": 0,
        "already_correct": 0,
        "skipped_non_s3": 0,
        "object_missing": 0,
        "restamp_failed": 0,
    }
    seen = 0
    offset = 0
    started = time.monotonic()

    while True:
        batch_target = min(_BATCH_SIZE, (limit - seen)) if limit else _BATCH_SIZE
        if batch_target <= 0:
            break
        rows = await _next_batch(
            public_only=public_only,
            owner_filter=owner_filter,
            offset=offset,
            batch_size=batch_target,
        )
        if not rows:
            break
        await asyncio.gather(
            *(_process_row(fm, s3_client, row, sem=sem, stats=stats) for row in rows),
            return_exceptions=True,
        )
        seen += len(rows)
        offset += len(rows)
        elapsed = time.monotonic() - started
        rate = seen / elapsed if elapsed > 0 else 0
        vcprint(
            f"[restamp] processed={seen:,} restamped={stats['restamped']:,} "
            f"already={stats['already_correct']:,} missing={stats['object_missing']:,} "
            f"failed={stats['restamp_failed']:,} ({rate:.1f}/s)",
            color="cyan",
        )
        if limit and seen >= limit:
            break

    return stats


__all__ = ["run_restamp_headers_backfill"]
