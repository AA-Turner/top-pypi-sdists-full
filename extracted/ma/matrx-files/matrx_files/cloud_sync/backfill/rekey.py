"""Rekey files.files rows onto the canonical <owner>/<file_id> S3 key.

Walks files.files rows whose S3 key is still the legacy
``<owner>/<file_path>`` shape, performs a server-side S3 copy to the
canonical ``<owner>/<file_id>`` key, then points ``storage_uri`` at it.

HISTORY — this backfill originally populated a separate
``canonical_storage_uri`` column. Migration 007 (applied after the fleet
backfill completed) renamed that column INTO ``storage_uri``, making
``storage_uri`` the single authoritative URI; the interim
``canonical_storage_uri`` / ``_legacy_storage_uri`` columns no longer
exist. Post-007 a row "needs rekeying" exactly when its ``storage_uri``
key is not ``<owner>/<file_id>`` — checked in Python per row (the shape
test is not a column predicate), with cursor pagination on ``id`` so the
walk always moves forward.

The script is **idempotent + resumable**:
  * Skips rows whose key is already canonical.
  * Skips rows whose legacy storage object is missing (logs + flagged
    in metadata so the operator can investigate).
  * Copying onto an already-existing canonical key is a no-op copy; the
    UPDATE then wires the URI.
  * Bounded concurrency so we don't saturate S3 or the Postgres pool.

Portable: pass a configured ``FileManager`` in. Hosts write a tiny CLI
that bootstraps their wiring then calls ``run_rekey_backfill(fm, ...)``.
DB access goes through the package's own matrx-orm models (see
``cloud_sync/db.py`` — the PostgREST client is gone from this layer).

The script does NOT delete the legacy S3 objects. That happens in a
later cleanup once we are confident the canonical keys are correct
across the fleet (think: bake time of at least 7 days). Until then
both keys exist; old frozen URLs keep resolving against the legacy key.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from matrx_utils import vcprint

from ..db import _models, _vals

# Tunables.
_BATCH_SIZE = 200
_PARALLELISM = 8

# Narrow column set — everything _process_row needs, nothing more.
_REKEY_COLUMNS = ("id", "created_by", "storage_uri", "file_path")


async def _next_batch(
    *,
    owner_filter: str | None,
    batch_size: int,
    cursor_id: str | None,
) -> list[dict]:
    """Fetch the next batch of candidate rows, cursor-paginated on ``id``.

    Post-007 there is no "needs rekey" column predicate (the canonical
    test is a key-shape check done in Python), so we walk every live row
    with ``id > cursor`` — already-canonical rows are counted and skipped
    cheaply in ``_process_row``.
    """
    mf, _ = _models()
    q = mf.Files.filter(deleted_at__isnull=True)
    if cursor_id:
        q = q.filter(id__gt=cursor_id)
    if owner_filter:
        q = q.filter(created_by=owner_filter)
    rows = await q.order_by("id").limit(batch_size).values(*_REKEY_COLUMNS)
    return _vals(rows)


def _canonical_key(owner_id: str, file_id: str) -> str:
    """The canonical S3 key inside the bucket. <owner>/<file_id>."""
    return f"{owner_id}/{file_id}"


def _split_uri(uri: str) -> tuple[str, str, str] | None:
    """Split <backend>://<bucket>/<key> into (backend, bucket, key)."""
    if "://" not in uri:
        return None
    backend, rest = uri.split("://", 1)
    if "/" not in rest:
        return None
    bucket, key = rest.split("/", 1)
    return backend, bucket, key


async def _process_row(
    fm: Any,
    row: dict[str, Any],
    *,
    sem: asyncio.Semaphore,
    stats: dict[str, int],
) -> None:
    async with sem:
        file_id = row["id"]
        owner_id = row.get("owner_id") or row["created_by"]
        legacy_uri = row.get("storage_uri") or ""
        split = _split_uri(legacy_uri)
        if split is None or not legacy_uri.startswith("s3://"):
            # Not an S3-backed row (typical: leftover /tmp test paths).
            # Post-007 storage_uri is the ONLY URI column (NOT NULL), so we
            # never overwrite it with a sentinel — just flag metadata for
            # the operator. Cursor pagination means no churn either way.
            await _flag_missing(file_id, f"non-s3 storage_uri: {legacy_uri[:100]!r}")
            stats["skipped_bad_uri"] += 1
            return
        backend, bucket, legacy_key = split
        canonical_key = _canonical_key(owner_id, file_id)
        canonical_uri = f"{backend}://{bucket}/{canonical_key}"

        # Common case post-007: the key already IS the canonical key.
        if legacy_key == canonical_key:
            stats["already_canonical"] += 1
            return

        if not fm.sync_engine._router.is_configured("s3"):
            stats["skipped_no_backend"] += 1
            return
        s3 = fm.sync_engine._router.s3
        s3_client = s3._get_client()

        # Verify the legacy object exists.
        try:
            await asyncio.to_thread(s3_client.head_object, Bucket=bucket, Key=legacy_key)
        except Exception as e:
            vcprint(
                f"[rekey] legacy missing file_id={file_id} key={legacy_key} err={e!r}",
                color="yellow",
            )
            await _flag_missing(file_id, str(e))
            stats["legacy_missing"] += 1
            return

        # Server-side copy. Idempotent — copying onto an existing object
        # in the same bucket is allowed.
        try:
            await asyncio.to_thread(
                s3_client.copy_object,
                Bucket=bucket,
                Key=canonical_key,
                CopySource={"Bucket": bucket, "Key": legacy_key},
                MetadataDirective="COPY",
            )
        except Exception as e:
            vcprint(f"[rekey] copy failed file_id={file_id} err={e!r}", color="yellow")
            stats["copy_failed"] += 1
            return

        await _update_row(file_id, canonical_uri)
        stats["copied"] += 1


async def _update_row(file_id: str, canonical_uri: str) -> None:
    mf, _ = _models()
    await mf.Files.update_where({"id": file_id}, storage_uri=canonical_uri)


async def _flag_missing(file_id: str, error: str) -> None:
    """Stamp metadata so the operator can find rows whose legacy key 404s."""
    try:
        mf, _ = _models()
        rows = await mf.Files.filter(id=file_id).values("metadata")
        meta = (rows[0].get("metadata") if rows else None) or {}
        meta["_rekey_legacy_missing"] = {"error": error[:500]}
        await mf.Files.update_where({"id": file_id}, metadata=meta)
    except Exception:
        pass


async def rekey_one_file(fm: Any, file_id: str) -> bool:
    """Rekey a single files.files row right after upload.

    Designed for fire-and-forget from the upload handlers:

        asyncio.create_task(rekey_one_file(fm, result.file_id))

    Returns True when the row was rekeyed (or already canonical),
    False on any non-fatal failure. Never raises.
    """
    try:
        if fm is None or fm.sync_engine is None:
            return False
        mf, _ = _models()
        rows = await mf.Files.filter(id=file_id).values(*_REKEY_COLUMNS)
        vals = _vals(rows)
        if not vals:
            return True
        row = vals[0]
        sem = asyncio.Semaphore(1)
        stats = {
            "copied": 0,
            "already_canonical": 0,
            "legacy_missing": 0,
            "copy_failed": 0,
            "skipped_bad_uri": 0,
            "skipped_no_backend": 0,
        }
        await _process_row(fm, row, sem=sem, stats=stats)
        return stats["copied"] > 0 or stats["already_canonical"] > 0
    except Exception:
        return False


async def run_rekey_backfill(
    fm: Any,
    *,
    owner_filter: str | None = None,
    limit: int | None = None,
) -> dict[str, int]:
    """Walk every row needing rekey, copy bytes, update URIs.

    Pass a configured FileManager (with cloud_sync set up). The CLI
    wrapper a host ships should bootstrap settings + context then
    call this function.
    """
    if fm is None or fm.sync_engine is None:
        raise RuntimeError("cloud sync not configured — pass a FileManager with sync_engine set")

    sem = asyncio.Semaphore(_PARALLELISM)
    stats: dict[str, int] = {
        "copied": 0,
        "already_canonical": 0,
        "legacy_missing": 0,
        "copy_failed": 0,
        "skipped_bad_uri": 0,
        "skipped_no_backend": 0,
    }
    seen = 0
    cursor_id: str | None = None
    started = time.monotonic()

    while True:
        batch_target = min(_BATCH_SIZE, (limit - seen)) if limit else _BATCH_SIZE
        if batch_target <= 0:
            break
        rows = await _next_batch(
            owner_filter=owner_filter, batch_size=batch_target, cursor_id=cursor_id
        )
        if not rows:
            break
        cursor_id = rows[-1]["id"]
        await asyncio.gather(
            *(_process_row(fm, row, sem=sem, stats=stats) for row in rows),
            return_exceptions=True,
        )
        seen += len(rows)
        elapsed = time.monotonic() - started
        rate = seen / elapsed if elapsed > 0 else 0
        vcprint(
            f"[rekey] processed={seen:,} copied={stats['copied']:,} "
            f"already={stats['already_canonical']:,} missing={stats['legacy_missing']:,} "
            f"failed={stats['copy_failed']:,} ({rate:.1f}/s)",
            color="cyan",
        )
        if limit and seen >= limit:
            break

    return stats


__all__ = ["rekey_one_file", "run_rekey_backfill"]
