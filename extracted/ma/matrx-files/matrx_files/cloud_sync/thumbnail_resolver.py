"""Thumbnail-URL resolver — single source of truth for "give me a thumbnail
URL for this cld_files row".

Phase 1b — replaces the legacy ``cld_files.thumbnail_storage_uri`` /
``cld_files.thumbnail_url`` columns. Thumbnails now live as variant
cld_files rows linked back to the master via ``metadata.derived_from``.
The Phase 1 variants pipeline writes them; this module reads them.

Public API:

    # Single-record: when you have one cld_files row and want a thumbnail URL
    url = await resolve_thumbnail_url_async(fm, record)

    # List-record: when you have N records and want N thumbnail URLs
    # (issues N concurrent queries via asyncio.gather; the
    # idx_cld_files_derived_from B-tree index keeps each lookup O(log n))
    url_by_id = await resolve_thumbnail_urls_async(fm, records)

Both helpers return None when no thumbnail variant exists yet — caller
falls back to a client-side icon or triggers a thumbnail render.
"""

from __future__ import annotations

import asyncio
import itertools
import time
from typing import Any

# Variant key the SOCIAL_BASELINE pipeline writes for the 400×400 thumbnail.
# Centralized here so any future rename is a one-line change.
THUMBNAIL_VARIANT_KEY = "thumbnail_url"


async def resolve_thumbnail_url_async(
    fm: Any,
    record: dict,
    *,
    variant_key: str = THUMBNAIL_VARIANT_KEY,
) -> str | None:
    """Return a usable URL for the row's thumbnail variant, or None.

    Looks up ``metadata.derived_from = record["id"]`` AND
    ``metadata.variant_key = variant_key`` in cld_files (one DB hit via
    the migration-009 expression index), then builds the durable URL via
    SyncEngine.build_urls_for_record_async — private files get the
    authenticated /files/{id}/download?inline=1 route, public the CDN URL.

    No fallback to the legacy ``record["thumbnail_url"]`` /
    ``record["thumbnail_storage_uri"]`` columns — those are dropped in
    migration 011 and reading them would raise once the schema
    catches up. Callers that need a transition fallback should compute
    it explicitly.

    Returns None when the variant hasn't been rendered yet (file
    uploaded before Phase 1, or thumbnail render failed).
    """
    if not record or not record.get("id"):
        return None
    se = fm.sync_engine
    catalog, older = await se.variants.list_with_older_async(record)
    variant = catalog.get(variant_key)
    if not variant:
        # A master replaced in place keeps its older thumbnail until the new bytes are rendered: serve the
        # older one and queue the render (CGU-10 AND-V IMG18 F3) — a list never just loses a thumbnail. Crash-safe
        # by construction: the queued work is derived from the rows themselves, so the next read re-queues it.
        variant = older.get(variant_key)
        if not variant:
            # A LIVE FILE WITH NO LIVE THUMBNAIL HEALS ITSELF (2026-11-20, Matrx Scan): 377 live files had every
            # variant soft-deleted (a test run's archive took variants its run had re-rendered for an unstamped
            # master) and nothing ever rendered them again — the library showed gray tiles forever. The read
            # still answers None now (it never waits on a render); the render is queued so the next read finds it.
            _queue_missing_render(fm, record)
            return None
        _queue_current_render(fm, record, reason="older_version_thumbnail_served")
    urls = await se.build_urls_for_record_async(variant)
    return urls.get("url")


#: Per process: when this file's render was last queued from a READ. A read that keeps finding no thumbnail (an
#: unrenderable file, a render that keeps failing, a list polled every few seconds) queues at most one render per
#: file per window — never a download + render per page view. Cross-process the render is idempotent
#: (VariantsService key dedup); in-process concurrent renders already join one task (processing/thumbnails.py).
READ_RENDER_RETRY_SECONDS: float = 15 * 60
#: Bound on the memo above (insertion-ordered: a re-claim moves to the end). Past it the oldest tenth is dropped in
#: one batch — never a sort per claim on the event loop. A dropped file may queue once more.
READ_RENDER_MEMO_MAX: int = 20_000
_read_render_queued_at: dict[str, float] = {}
#: At most this many read-queued renders run at once per process (each is a DB read, a download of up to 64 MiB
#: held in memory, and a render). A page of 200 thumbnail-less files queues 200; the rest WAIT, none is dropped.
READ_RENDER_CONCURRENCY: int = 4
_render_gate: tuple[Any, asyncio.Semaphore] | None = None

#: Families with a real rasteriser (processing/thumbnails.py ``_VISUAL_FAMILIES``). Only these ever get a
#: thumbnail, so a read of any other file (text, archives, data) never queues a render that downloads its bytes
#: only to decide it has no picture.
_HEALABLE_FAMILIES = frozenset({"image", "video", "pdf", "document", "audio"})


def _queue_missing_render(fm: Any, record: dict) -> None:
    """Queue the render for a LIVE master that has no live variant at all, when it is one that gets a thumbnail.

    A record without ``metadata`` / ``derivation_kind`` (the search RPC's rows) is judged by its mime alone; the
    render re-reads the full row and refuses a variant itself, so the worst case is one cheap read per window."""
    try:
        if record.get("deleted_at") is not None:
            return  # a trashed file's read changes nothing
        meta = record.get("metadata") or {}
        if meta.get("derived_from") or meta.get("variant_key") or record.get("derivation_kind") == "variant":
            return  # a variant never gets variants of its own (the cascade incident)
        from matrx_files.specific_handlers.thumbnail_source import _mime_family

        if _mime_family(record.get("mime_type")) not in _HEALABLE_FAMILIES:
            return
    except Exception:  # noqa: BLE001 — a read never fails on its heal
        return
    _queue_current_render(fm, record, reason="no_live_thumbnail")


def _claim_read_render(file_id: str) -> bool:
    """True when this process has not queued a read render for ``file_id`` within the retry window (and claims it)."""
    now = time.monotonic()
    last = _read_render_queued_at.get(file_id)
    if last is not None and now - last < READ_RENDER_RETRY_SECONDS:
        return False
    _read_render_queued_at.pop(file_id, None)
    _read_render_queued_at[file_id] = now
    if len(_read_render_queued_at) > READ_RENDER_MEMO_MAX:
        drop = max(1, READ_RENDER_MEMO_MAX // 10)
        for stale in list(itertools.islice(_read_render_queued_at, drop)):
            _read_render_queued_at.pop(stale, None)
    return True


def _release_read_render(file_id: str) -> None:
    """Undo a claim whose render never started, so the next read retries at once."""
    _read_render_queued_at.pop(file_id, None)


def _read_render_gate() -> asyncio.Semaphore:
    """The per-process (per running loop) bound on read-queued renders."""
    global _render_gate
    loop = asyncio.get_running_loop()
    if _render_gate is None or _render_gate[0] is not loop:
        _render_gate = (loop, asyncio.Semaphore(READ_RENDER_CONCURRENCY))
    return _render_gate[1]


async def _bounded_render(fm: Any, file_id: str, gate: asyncio.Semaphore) -> bool:
    from .processing import generate_thumbnail_for_file

    async with gate:
        return await generate_thumbnail_for_file(fm, file_id)


def _queue_current_render(fm: Any, record: dict, *, reason: str) -> None:
    """Render the current version's variants (the same idempotent path an upload uses). Never raises.

    Queued in a supervised hop that does NOT carry a test run (``supervised_task`` default): a read never stamps,
    so a test session viewing a person's file never makes test-stamped variants of it. Bounded: at most
    ``READ_RENDER_CONCURRENCY`` run at once; the others wait their turn."""
    try:
        file_id = str(record["id"])
    except Exception:  # noqa: BLE001
        return
    if not _claim_read_render(file_id):
        return
    try:
        from matrx_utils import supervised_task

        supervised_task(
            _bounded_render(fm, file_id, _read_render_gate()),
            kind="file_thumbnail_generation_failed",
            name=f"thumbnail-rerender:{file_id}",
            context={"file_id": file_id, "reason": reason},
        )
    except Exception:  # noqa: BLE001 — a list read never fails on its render queue; the older thumbnail still shows
        _release_read_render(file_id)  # nothing started: the next read tries again, not in 15 minutes
        return


async def resolve_thumbnail_urls_async(
    fm: Any,
    records: list[dict],
    *,
    variant_key: str = THUMBNAIL_VARIANT_KEY,
) -> dict[str, str | None]:
    """Bulk variant of ``resolve_thumbnail_url_async`` for list endpoints.

    Returns ``{file_id: thumbnail_url_or_none}`` for every input record.
    Issues N parallel queries via asyncio.gather — the migration-009
    expression index ``idx_cld_files_derived_from`` keeps each lookup
    O(log n), and Supabase's HTTP connection pool absorbs the parallel
    load comfortably for typical page sizes (≤200).

    A genuine bulk-SQL implementation (single query with WHERE IN) is
    a future optimization; the parallel-gather pattern keeps this
    helper dependency-free + portable across the sync_engine's DB
    backends.
    """
    if not records:
        return {}
    file_ids = [r["id"] for r in records if r and r.get("id")]
    if not file_ids:
        return {}
    coros = [
        resolve_thumbnail_url_async(
            fm, r, variant_key=variant_key,
        )
        for r in records
    ]
    results = await asyncio.gather(*coros, return_exceptions=True)
    out: dict[str, str | None] = {}
    for r, url in zip(records, results, strict=False):
        if not r or not r.get("id"):
            continue
        if isinstance(url, Exception):
            # Per-record failure is non-fatal — leave None and let the
            # FE fall back to its client-side icon.
            out[r["id"]] = None
        else:
            out[r["id"]] = url
    return out


_MASTER_COLUMNS = ("deleted_at", "current_version", "metadata", "mime_type", "derivation_kind")


async def read_thumbnail_async(
    fm: Any,
    file_id: str,
    *,
    user_id: str,
    variant_key: str = THUMBNAIL_VARIANT_KEY,
) -> tuple[bytes, str | None] | None:
    """The thumbnail picture of a file ``user_id`` may read — LIVE OR IN THE TRASH — as ``(bytes, mime_type)``.

    The one read a Trash view needs: a trashed file's every normal door (its record, its download, its asset) keeps
    answering 404, but the picture on its tile is still the person's to see, or Recover is picked blind. The gate is
    the master's: ``user_id`` must READ the master (the host's access checker, ``iam.has_access_for`` — trashed rows
    included, the same judge the restore door asks), and the bytes are read through ``read_stored_bytes``, which asks
    it again of the variant row itself. Only the thumbnail variant is ever served, never the master's own bytes.

    Raises ``FileNotFoundError`` when the file is missing or the caller may not read it (never a hint which); returns
    None when the file has no rendered thumbnail (the caller shows its blank card). A LIVE file with no live thumbnail
    queues its render (the resolver's heal, same guard); a read of a trashed file changes nothing.
    """
    from matrx_files.gated_reads import read_file_row, read_stored_bytes

    master = await read_file_row(file_id, _MASTER_COLUMNS, user_id=user_id)
    if master is None:
        raise FileNotFoundError(f"File {file_id!r} not found")
    trashed = master.get("deleted_at") is not None
    current, older = await fm.sync_engine.variants.list_with_older_async(master, include_deleted=trashed)
    variant = current.get(variant_key) or older.get(variant_key)
    if not trashed and not current.get(variant_key):
        if variant:
            _queue_current_render(fm, {"id": file_id, **master}, reason="older_version_thumbnail_served")
        else:
            _queue_missing_render(fm, {"id": file_id, **master})
    if not variant or not variant.get("storage_uri"):
        return None
    data = await read_stored_bytes(fm, str(variant["id"]), str(variant["storage_uri"]), user_id=user_id)
    return data, variant.get("mime_type")


__all__ = [
    "THUMBNAIL_VARIANT_KEY",
    "read_thumbnail_async",
    "resolve_thumbnail_url_async",
    "resolve_thumbnail_urls_async",
]
