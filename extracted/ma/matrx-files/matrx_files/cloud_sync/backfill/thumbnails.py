"""Backfill universal media processing for existing files.files rows.

Applies the full Phase 1 / 1c / 1d.1 treatment to every existing
files.files row that pre-dates these phases:

  - SOCIAL_BASELINE variants (og_url / thumbnail_url / tiny_url)
  - Kind-specific variants (page1_url for PDFs, poster_url for videos)
  - Probed metadata (width / height / duration_ms / page_count)

Idempotent + resumable: cursor pagination on ``id`` so each batch
moves forward, and ``generate_thumbnail_for_file`` is internally
idempotent (VariantsService keys + only-write-if-null on columns).

Usage from Python::

    from matrx_files.cloud_sync.backfill.thumbnails import (
        run_thumbnail_backfill,
    )
    stats = await run_thumbnail_backfill(fm, limit=500)

Hosts wrap this with their own CLI. AIDream's CLI is at
``aidream/scripts/backfill_media.py``. DB access goes through the
package's own matrx-orm models (see ``cloud_sync/db.py``).
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from matrx_utils import vcprint

from ..db import _models, _vals
from ..processing.thumbnails import generate_thumbnail_for_file

_BATCH_SIZE = 100
_PARALLELISM = 4  # Pillow + pypdfium2 are CPU-heavy; cap to 4 workers.


def _mime_filter():
    """Phase 1d: target visual + temporal mime families.

    Office documents joined the set when the LibreOffice page-1 lane
    landed (they render a real preview now, not just an icon).
    Unsupported mimes still get a mime-family icon via the universal
    dispatcher, but those are cheap to render on first read so we don't
    backfill them.
    """
    from matrx_orm import Q

    from ...specific_handlers.office import OFFICE_MIMES

    return (
        Q(mime_type__startswith="image/")
        | Q(mime_type__startswith="video/")
        | Q(mime_type__startswith="audio/")
        | Q(mime_type="application/pdf")
        | Q(mime_type__in=sorted(OFFICE_MIMES))
    )


# Columns we read so the row-level skip check (does this row already
# have everything?) can run without a second query. Phase 1d.3 added
# file_path + parent_file_id so the variant-row filter can run without
# a second roundtrip. (The interim ``canonical_storage_uri`` column was
# consolidated into ``storage_uri`` by migration 007 and no longer exists.)
#
# 🚨 This tuple is the generator's ENTIRE view of the row — the backfill
# hands it straight to ``generate_thumbnail_for_file(record=...)``, which
# never re-reads. A column the generator reads but this tuple omits does
# not raise: ``record.get(...)`` returns None and the generator silently
# takes the wrong branch. ``size_bytes`` was missing exactly that way, so
# every backfilled row computed ``size_bytes=0`` and the Phase 6b
# bounded-memory path (stream to a temp file at/above
# LARGE_MEDIA_THRESHOLD_BYTES) could never trigger — the backfill read
# every multi-GB video whole into RAM while the upload path did not.
# Guard: tests/test_backfill_columns.py diffs this tuple against every
# ``record.get("…")`` in the generator. Add a read there → add it here.
_BACKFILL_COLUMNS = (
    "id",
    "created_by",
    "storage_uri",
    "mime_type",
    "file_name",
    "published_to_web",
    "shown_to",
    "width",
    "height",
    "duration_ms",
    "metadata",
    "deleted_at",
    "created_at",
    "file_path",
    "parent_file_id",
    "size_bytes",
)


async def _next_batch(
    *,
    owner_filter: str | None,
    batch_size: int,
    cursor_id: str | None,
    mimes: list[str] | None = None,
) -> list[dict]:
    """Cursor-paginated batch fetch — MASTERS ONLY (no variant rows).

    Uses ``id > cursor_id`` so successive batches move forward without
    needing offsets.

    PHASE 1d.3 BUG FIX (primary defense): excludes variant rows from
    the iteration so the backfill cannot re-process its own output.
    The original query selected every files row matching the mime
    filter — INCLUDING the variant rows it had just written (which are
    files.files rows with mime image/jpeg under file_path
    ``system-files/variants/<master>/<key>.jpg``). Each variant got
    handed back to ``generate_thumbnail_for_file`` as if it were a
    master, generating new variants OF the variant, up to 12 levels
    deep.

    Triple filter:
      - file_path NOT LIKE 'system-files/%'  (positive path filter)
      - parent_file_id IS NULL               (no lineage parent)
      - metadata->>'derived_from' IS NULL    (no derivation hint —
        applied in Python after the round-trip as belt-and-braces)
    """
    mf, _ = _models()
    q = (
        mf.Files.filter(deleted_at__isnull=True, parent_file_id__isnull=True)
        .exclude(file_path__startswith="system-files/")
    )
    if mimes:
        q = q.filter(mime_type__in=mimes)
    else:
        q = q.filter(_mime_filter())
    if cursor_id:
        q = q.filter(id__gt=cursor_id)
    if owner_filter:
        q = q.filter(created_by=owner_filter)
    rows = _vals(await q.order_by("id").limit(batch_size).values(*_BACKFILL_COLUMNS))
    # In-process belt-and-braces — drop any row whose metadata.derived_from
    # slipped through (impossible given the path + parent_file_id filters
    # above, but cheap insurance against future schema drift).
    return [r for r in rows if not ((r.get("metadata") or {}).get("derived_from"))]


async def _has_baseline_variants(fm: Any, master_record: dict) -> bool:
    """Check whether SOCIAL_BASELINE keys already exist for this master.

    When all baseline keys are present AND the dimension columns are
    populated AND any applicable kind-specific variant exists, the row
    is fully processed — we can skip it cheaply.
    """
    try:
        catalog = await fm.sync_engine.variants.list_existing_async(master_record)
    except Exception:
        return False
    return all(k in catalog for k in ("og_url", "thumbnail_url", "tiny_url"))


def _is_fully_processed(record: dict, baseline_present: bool) -> bool:
    """True when this row needs no further backfill work.

    Checks dimension columns (probed at Phase 1d.1) AND baseline variant
    presence. For PDFs we also require page_count in metadata; for
    videos we require duration_ms.
    """
    if not baseline_present:
        return False
    mime = record.get("mime_type") or ""
    has_dims = record.get("width") is not None and record.get("height") is not None
    has_duration = record.get("duration_ms") is not None
    has_page_count = (record.get("metadata") or {}).get("page_count") is not None
    if mime.startswith("image/"):
        return has_dims
    if mime == "application/pdf":
        return has_dims and has_page_count
    if mime.startswith("video/"):
        return has_dims and has_duration
    if mime.startswith("audio/"):
        return has_duration
    return baseline_present


async def _process_one(
    fm: Any,
    row: dict[str, Any],
    *,
    sem: asyncio.Semaphore,
    stats: dict[str, int],
    force: bool,
    force_rerender: bool,
) -> None:
    async with sem:
        try:
            # Pre-flight skip check — avoids the master-bytes read for
            # already-complete rows. ``--force`` bypasses (useful for
            # re-rendering with a tweaked dispatcher).
            if not (force or force_rerender):
                baseline_present = await _has_baseline_variants(fm, row)
                if _is_fully_processed(row, baseline_present):
                    stats["skipped_complete"] += 1
                    return
            ok = await generate_thumbnail_for_file(
                fm, row["id"], record=row, force_rerender=force_rerender,
            )
            stats["processed" if ok else "noop"] += 1
        except Exception as e:
            vcprint(f"[thumb_backfill] file={row['id']} err={e!r}", color="yellow")
            stats["failed"] += 1


async def run_thumbnail_backfill(
    fm: Any,
    *,
    owner_filter: str | None = None,
    limit: int | None = None,
    force: bool = False,
    force_rerender: bool = False,
    mimes: list[str] | None = None,
) -> dict[str, int]:
    """Walk every visual files.files row and backfill variants + metadata.

    Idempotent + resumable + cursor-paginated.

    Args:
        fm: configured FileManager with sync_engine set
        owner_filter: optional user_id to scope the backfill
        limit: optional cap on rows processed (None = process everything)
        force: when True, skip the "already complete" pre-flight check
               so rows re-enter the pipeline — but existing variant keys
               are still REUSED (VariantsService key-dedup). Renders only
               keys that are missing.
        force_rerender: when True, additionally re-render EXISTING variant
               keys, overwriting each in place. This is the healing knob
               for the variant-key dedup trap — masters whose keys are
               occupied by stale content (mime-icon thumbnails written
               before the Office/PDF page-1 render lanes existed). Use
               with ``mimes`` to scope the re-render blast radius.
        mimes: optional explicit mime_type list; replaces the default
               visual-family filter (e.g. Office mimes only).

    Returns stats dict: processed, skipped_complete, noop, failed.
    """
    if fm is None or fm.sync_engine is None:
        raise RuntimeError("cloud sync not configured — pass a FileManager with sync_engine set")

    sem = asyncio.Semaphore(_PARALLELISM)
    stats: dict[str, int] = {
        "processed": 0,
        "skipped_complete": 0,
        "noop": 0,
        "failed": 0,
    }
    seen = 0
    cursor_id: str | None = None
    started = time.monotonic()

    while True:
        target = min(_BATCH_SIZE, (limit - seen)) if limit else _BATCH_SIZE
        if target <= 0:
            break
        rows = await _next_batch(
            owner_filter=owner_filter,
            batch_size=target,
            cursor_id=cursor_id,
            mimes=mimes,
        )
        if not rows:
            break
        cursor_id = rows[-1]["id"]
        await asyncio.gather(
            *(
                _process_one(
                    fm, row, sem=sem, stats=stats,
                    force=force, force_rerender=force_rerender,
                )
                for row in rows
            ),
            return_exceptions=True,
        )
        seen += len(rows)
        elapsed = time.monotonic() - started
        rate = seen / elapsed if elapsed > 0 else 0
        vcprint(
            f"[thumb_backfill] seen={seen:,} "
            f"processed={stats['processed']:,} skipped={stats['skipped_complete']:,} "
            f"noop={stats['noop']:,} failed={stats['failed']:,} ({rate:.1f}/s)",
            color="cyan",
        )
        if limit and seen >= limit:
            break

    elapsed = time.monotonic() - started
    accomplished = stats["processed"] + stats["skipped_complete"]
    vcprint(
        f"[thumb_backfill] DONE seen={seen:,} in {elapsed:.0f}s — "
        f"processed={stats['processed']:,} skipped={stats['skipped_complete']:,} "
        f"noop={stats['noop']:,} failed={stats['failed']:,}",
        color="green" if stats["noop"] == 0 else "yellow",
    )
    # ``noop`` means generate_thumbnail_for_file returned False. It NEVER
    # raises (by contract), so an internal error — a bad record shape, an
    # unreadable master, a refused overwrite — is indistinguishable from
    # "nothing to do" in the counters. A run where nothing was accomplished
    # but rows were seen is a FAILED run wearing a green DONE line; that is
    # exactly how the 2026-08-08 owner_id KeyError hid in plain sight.
    if seen and accomplished == 0:
        vcprint(
            f"[thumb_backfill] ALARM: saw {seen:,} row(s) and accomplished "
            f"NOTHING (processed=0, skipped_complete=0, noop={stats['noop']:,}). "
            f"This is a FAILED run, not a clean one — every row's generator "
            f"returned False. Scroll up for the per-file [thumbnails] warnings; "
            f"they carry the real cause.",
            color="red",
        )
    elif stats["noop"]:
        vcprint(
            f"[thumb_backfill] NOTE: {stats['noop']:,} row(s) returned noop — "
            f"the generator declined them (see per-file [thumbnails] warnings).",
            color="yellow",
        )
    return stats


__all__ = ["run_thumbnail_backfill"]
