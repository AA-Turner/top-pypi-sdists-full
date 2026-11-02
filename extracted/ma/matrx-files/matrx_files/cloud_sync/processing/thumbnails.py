"""Universal post-upload media processing for cld_files — Phase 1d backfill.

Designed for two call sites:

  1. **Fire-and-forget after upload** (TUS finalize, legacy /files/upload,
     anywhere a file lands in cld_files without going through POST /assets):

        asyncio.create_task(generate_thumbnail_for_file(fm, file_id))

  2. **Backfill** — apply the full Phase 1 / 1c / 1d.1 treatment to every
     existing cld_files row that pre-dates these phases. Idempotent, so
     safe to re-run repeatedly:

        await ensure_media_processing(fm, file_id)

Both call sites do the same work:

  - **Phase 1**: render the SOCIAL_BASELINE variants (og_url /
    thumbnail_url / tiny_url) from a universally-rasterised source
    (image passthrough, PDF page 1, video frame, audio waveform,
    mime-icon fallback for everything else).
  - **Phase 1c**: render the kind-specific full-res variants (page1_url
    for PDFs, poster_url for videos) so DocumentBlock / VideoBlock
    carry a browser-renderable primary representation.
  - **Phase 1d.1**: probe width / height / duration_ms / page_count
    from the source bytes and persist to the cld_files columns
    (page_count lands in metadata.page_count since there's no column).

Idempotency comes from VariantsService — variant keys that already
exist for the (master, key) pair are skipped. Probe failures + variant
render failures are non-fatal so a bad file never blocks the upload
pipeline OR the backfill loop.
"""

from __future__ import annotations

import asyncio
import os
import tempfile
import time
from typing import Any

from matrx_utils import vcprint

# Size-aware source strategy (Phase 6b — bounded-memory large-media
# processing). Objects at/above this threshold are NEVER read whole into
# Python memory: they are streamed to a NamedTemporaryFile via the backend's
# streaming download (boto3 ``download_file``) and probed/rendered BY PATH
# (OpenCV / pydub-ffmpeg read from disk). Below it, the in-memory fast path
# is kept — a single read, no disk round-trip.
LARGE_MEDIA_THRESHOLD_BYTES: int = 64 * 1024 * 1024  # 64 MiB

# In-process per-file in-flight guard. Upload trigger, TUS finalize, and the
# backfill can all fire generate_thumbnail_for_file(file_id) concurrently;
# concurrent callers JOIN the canonical task instead of duplicating the
# download + render work. (Same pattern as aidream's
# services/file_analysis/pipeline.py ``_inflight_analyses``.) Cross-process
# dedup remains the VariantsService variant-key idempotency.
_INFLIGHT: dict[str, asyncio.Task[bool]] = {}
_INFLIGHT_LOCK = asyncio.Lock()


async def generate_thumbnail_for_file(
    fm: Any,
    file_id: str,
    *,
    record: dict[str, Any] | None = None,
    allow_lineage: bool = False,
    force_rerender: bool = False,
) -> bool:
    """Render variants + probe metadata for a cld_files row.

    Returns True when any variant landed (new or already present), False
    on early-skip or any non-fatal failure. Never raises — must not
    bring down the upload pipeline.

    Idempotent across both variants (VariantsService key-deduplication)
    and column updates (overwrites with the probed values, which are
    deterministic for a given byte sequence).

    ``allow_lineage=True`` bypasses ONLY the parent_file_id guard — for
    masters that legitimately carry lineage (a scanned PDF's parent is
    its first source photo). The variant-row guard (derived_from /
    variant_key) always applies; the cascade incident cannot recur via
    this flag because variant rows are identified by metadata, not by
    parentage.

    ``force_rerender=True`` re-renders variants whose keys already exist,
    overwriting each existing variant IN PLACE (same file_path → the
    managed write upserts the row and overwrites the S3 object; no
    duplicate rows, no orphaned objects). This is the healing path for
    masters whose variant keys are occupied by stale content — e.g. the
    mime-icon thumbnails written for Office/PDF files before their real
    page-1 render lanes existed (the variant-key dedup trap: plain
    re-runs skip occupied keys forever).

    Concurrency: per-file in-flight dedup. When another invocation for the
    same ``file_id`` is already running in this process, this call awaits
    that task's result instead of starting a second download/render. The
    first invocation's kwargs win (same edge-case rule as file analysis).

    Memory: sources at/above ``LARGE_MEDIA_THRESHOLD_BYTES`` are streamed
    to a temp file and processed by path — the object bytes never enter
    Python memory. See the ``_from_path`` family in
    ``specific_handlers/thumbnail_source.py``.
    """
    async with _INFLIGHT_LOCK:
        existing = _INFLIGHT.get(file_id)
        if existing is not None and not existing.done():
            vcprint(
                f"[thumbnails] dedup: already in flight for file={file_id}; joining",
                color="cyan",
            )
            joined = existing
        else:
            joined = None
            task = asyncio.ensure_future(
                _generate_impl(
                    fm, file_id, record=record,
                    allow_lineage=allow_lineage, force_rerender=force_rerender,
                )
            )
            _INFLIGHT[file_id] = task

    if joined is not None:
        try:
            return await asyncio.shield(joined)
        except Exception:
            # The canonical task's failure is its own diagnostic; a joiner
            # never raises (contract: this function never raises).
            return False

    try:
        return await task
    finally:
        async with _INFLIGHT_LOCK:
            if _INFLIGHT.get(file_id) is task:
                _INFLIGHT.pop(file_id, None)


async def _reconcile_owner_id(
    record: dict[str, Any], file_id: str, db: Any,
) -> dict[str, Any] | None:
    """Guarantee the record carries ``owner_id`` before it reaches a write path.

    A caller-supplied record may be a BARE DB row — read straight off the ORM
    without the read-path shim that exposes the DB's ``created_by`` column as
    Python's ``owner_id`` (``db.py::_owner_from_db``). The variants service
    writes with ``master_record["owner_id"]``, so a bare row raises KeyError
    at WRITE time ONLY — invisible for any file that needed no new variant.
    That is how the universal backfill ran "clean" while accomplishing nothing:
    on 2026-08-08 every Office row died here and the run still printed DONE.

    There is exactly one thing the caller can mean, so reconcile loudly rather
    than killing the row.
    """
    if "owner_id" in record:
        return record
    if record.get("created_by"):
        vcprint(
            f"[thumbnails] COERCED file={file_id}: caller-supplied record has no "
            f"'owner_id' (bare DB row) — deriving it from 'created_by'. Pass "
            f"records through db.get_file_async so the read-path shim applies.",
            color="yellow",
        )
        return {**record, "owner_id": record["created_by"]}
    vcprint(
        f"[thumbnails] file={file_id}: caller-supplied record has neither "
        f"'owner_id' nor 'created_by' — re-reading via get_file_async.",
        color="yellow",
    )
    return await db.get_file_async(file_id)


async def _generate_impl(
    fm: Any,
    file_id: str,
    *,
    record: dict[str, Any] | None = None,
    allow_lineage: bool = False,
    force_rerender: bool = False,
) -> bool:
    """Canonical single-flight body of :func:`generate_thumbnail_for_file`."""
    started = time.monotonic()
    db = fm.sync_engine.db
    try:
        if record is None:
            record = await db.get_file_async(file_id)
        if not record:
            return False

        record = await _reconcile_owner_id(record, file_id, db)
        if not record:
            return False

        mime = record.get("mime_type") or ""
        if not mime:
            return False

        # Phase 1d.3 defense-in-depth — refuse to process a row that is
        # itself a variant. This is the bug-fix for the cascade incident
        # where the backfill iterated every cld_files row matching the
        # mime filter (including variant rows) and re-processed each one
        # as if it were a master, creating "variants of variants" up to
        # 12 levels deep. The query-side filter in the backfill script
        # (filtered_query in cloud_sync/backfill/thumbnails.py) is the
        # primary defense; this is the second layer so no future caller
        # can accidentally re-trigger the cascade.
        meta = record.get("metadata") or {}
        if meta.get("derived_from") or meta.get("variant_key"):
            vcprint(
                f"[thumbnails] file={file_id} is a variant "
                f"(derived_from={meta.get('derived_from')}, "
                f"variant_key={meta.get('variant_key')}) — skipping",
                color="yellow",
            )
            return False
        if record.get("parent_file_id") and not allow_lineage:
            vcprint(
                f"[thumbnails] file={file_id} has parent_file_id={record['parent_file_id']} — skipping",
                color="yellow",
            )
            return False
        if (record.get("file_path") or "").startswith("system-files/"):
            vcprint(
                f"[thumbnails] file={file_id} lives under system-files/ — skipping",
                color="yellow",
            )
            return False

        # Read master bytes — prefer canonical_storage_uri (where present).
        source_uri = record.get("canonical_storage_uri") or record.get("storage_uri")
        if not source_uri:
            return False

        # ----- Size-aware source strategy (Phase 6b) --------------------
        # Small objects: single whole-object read, in-memory fast path.
        # Large objects (>= LARGE_MEDIA_THRESHOLD_BYTES): stream to a temp
        # file via the backend's streaming download and process BY PATH —
        # the object bytes never enter Python memory.
        from matrx_files.specific_handlers import thumbnail_source as ts

        size_bytes = int(record.get("size_bytes") or 0)
        use_streaming = size_bytes >= LARGE_MEDIA_THRESHOLD_BYTES

        content: bytes | None = None
        tmp_path: str | None = None
        try:
            if use_streaming:
                vcprint(
                    f"[thumbnails] file={file_id} size={size_bytes} >= "
                    f"{LARGE_MEDIA_THRESHOLD_BYTES} — streaming to temp file "
                    f"(bounded-memory path)",
                    color="cyan",
                )
                file_name = record.get("file_name") or ""
                suffix = os.path.splitext(file_name)[1] or ".tmp"
                fd, tmp_path = tempfile.mkstemp(suffix=suffix, prefix="mtx-thumb-")
                os.close(fd)
                written = await fm.sync_engine.router.download_to_path_async(
                    source_uri, tmp_path
                )
                if not written:
                    return False
            else:
                content = await fm.sync_engine.router.read_async(source_uri)
                if not content:
                    return False

            return await _process_source(
                fm, file_id, record, mime, ts,
                content=content, tmp_path=tmp_path, started=started,
                force_rerender=force_rerender,
            )
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
    except Exception as e:
        vcprint(f"[thumbnails] file={file_id} failed: {e!r}", color="yellow")
        return False


#: Families whose bytes have a real rasteriser (image passthrough, video frame,
#: PDF/Office page 1, audio waveform). Everything else only ever renders the
#: mime icon.
_VISUAL_FAMILIES = frozenset({"image", "video", "pdf", "document", "audio"})


def _visual_mime(
    *, content: bytes | None, tmp_path: str | None, mime: str, file_name: str | None
) -> str | None:
    """The mime to rasterise as, or None when the bytes have no visual."""
    from matrx_files.media_sniff import sniff_mime_type
    from matrx_files.specific_handlers.thumbnail_source import _mime_family

    if content is not None:
        head = content[:512]
    else:
        try:
            with open(tmp_path or "", "rb") as fh:
                head = fh.read(512)
        except OSError:
            head = b""
    sniffed = sniff_mime_type(claimed=mime, head_bytes=head, filename=file_name)
    family = _mime_family(sniffed)
    if family in ("image", "pdf"):
        # These two have magic numbers: the bytes must prove the claim. A text
        # file named .png is text.
        from matrx_files.media_sniff import _magic_byte_sniff

        magic = _magic_byte_sniff(head)
        if magic is not None:
            return magic if _mime_family(magic) == family else None
        if family == "pdf":
            return None
        # Image formats the cheap sniff has no magic for (BMP, TIFF, ICO, ...):
        # the image decoder reads the header and says whether these are pixels.
        try:
            import io

            from PIL import Image

            with Image.open(io.BytesIO(content) if content is not None else (tmp_path or "")) as img:
                return sniffed if img.format else None
        except Exception:
            return None
    return sniffed if family in _VISUAL_FAMILIES else None


async def _process_source(
    fm: Any,
    file_id: str,
    record: dict[str, Any],
    mime: str,
    ts: Any,
    *,
    content: bytes | None,
    tmp_path: str | None,
    started: float,
    force_rerender: bool = False,
) -> bool:
    """Probe + render from EITHER in-memory bytes or an on-disk temp file.

    Exactly one of ``content`` / ``tmp_path`` is set. The caller owns the
    temp file lifecycle.
    """
    db = fm.sync_engine.db
    file_name = record.get("file_name")

    # ----- Phase 1d.1: probe + persist intrinsic metadata ---------------
    # Probe width / height / duration_ms / page_count from the source.
    # Skip the column update when the row already carries every probed
    # field (avoids a needless write on idempotent re-runs).
    probed: dict = {}
    try:
        if tmp_path is not None:
            probed = await ts.probe_source_metadata_from_path(
                tmp_path, mime, file_name=file_name,
            )
        else:
            probed = await ts.probe_source_metadata(
                content, mime, file_name=file_name,
            )
    except Exception:
        probed = {}

    if probed:
        col_updates: dict = {}
        if probed.get("width") is not None and record.get("width") is None:
            col_updates["width"] = probed["width"]
        if probed.get("height") is not None and record.get("height") is None:
            col_updates["height"] = probed["height"]
        if probed.get("duration_ms") is not None and record.get("duration_ms") is None:
            col_updates["duration_ms"] = probed["duration_ms"]
        if probed.get("page_count") is not None:
            base_meta = record.get("metadata") or {}
            if base_meta.get("page_count") != probed["page_count"]:
                col_updates["metadata"] = {**base_meta, "page_count": probed["page_count"]}
        if col_updates:
            try:
                await db.update_file_async(file_id, col_updates)
                # Reflect the update on the in-memory record so the
                # variants pipeline + caller see consistent data.
                record = {**record, **col_updates}
            except Exception as e:
                vcprint(
                    f"[thumbnails] file={file_id} probe-persist failed: {e!r}",
                    color="yellow",
                )

    # ----- Phase 0: only content with a real visual makes variants -----
    # Decided by the BYTES (magic-byte sniff first, then name, then claim),
    # never by the extension or the stored mime alone. A .txt upload got three
    # stored image variants (og/thumb/tiny) of a gray mime icon -- three extra
    # files.files rows per text file (Lane E, 2026-10-21, file 6ddac242).
    # Text, code, archives and unknown bytes have no visual to render; the UI
    # draws their icon itself.
    visual_mime = _visual_mime(content=content, tmp_path=tmp_path, mime=mime, file_name=file_name)
    if visual_mime is None:
        vcprint(
            f"[thumbnails] file={file_id} mime={mime} name={file_name!r}: no visual "
            f"content (sniffed) — no variants made",
            color="cyan",
        )
        return False
    # Render as what the bytes ARE: a PNG stored as application/octet-stream
    # is rasterised as a PNG, not drawn as a generic icon.
    mime = visual_mime

    # ----- Phase 1: SOCIAL_BASELINE variants ----------------------------
    # Rasterise via the universal dispatcher (image passthrough, PDF page 1,
    # video frame, audio waveform, mime-icon fallback). On the bounded path
    # the raster source is produced BY PATH; the raster output itself
    # (a single image) is small and safe to hold in memory.
    if tmp_path is not None:
        raster_bytes, _raster_mime = await ts.render_thumbnail_source_from_path(
            tmp_path, mime, file_name=file_name,
        )
    else:
        raster_bytes, _raster_mime = await ts.render_thumbnail_source_bytes(
            content, mime, file_name=file_name,
        )
    # A force-rerender OVERWRITES existing variants, so it must never
    # replace real content with a fallback. Every per-family rasteriser
    # degrades to the deterministic mime icon on failure (a corrupt file,
    # a LibreOffice conversion that dies on one document), and that icon
    # would silently clobber a good page-1 thumbnail. The icon renderer is
    # deterministic + memoised, so an exact byte comparison identifies the
    # fallback with no new API surface and works for every family.
    icon_bytes = ts.render_mime_icon_bytes(mime_type=mime)
    if not force_rerender and raster_bytes == icon_bytes:
        # The render failed and fell back to the gray mime icon. A placeholder
        # is never stored as a thumbnail: the file has no preview, and every
        # client draws its type icon plus "Preview unavailable" (main's
        # ruling, 2026-10-21).
        vcprint(
            f"[thumbnails] file={file_id} ({mime}, {file_name!r}): render fell back to "
            f"the mime icon — no thumbnail stored (preview unavailable)",
            color="yellow",
        )
        return False
    if force_rerender:
        if raster_bytes == icon_bytes:
            vcprint(
                f"[thumbnails] REFUSING force_rerender for file={file_id} "
                f"({mime}, {file_name!r}): the rasteriser fell back to the "
                f"mime ICON — overwriting the existing variants would replace "
                f"real content with a placeholder. Existing variants left "
                f"untouched; investigate why this file failed to render.",
                color="red",
            )
            return False

    from matrx_files import SOCIAL_BASELINE

    rendered = await fm.sync_engine.variants.render_async(
        record,
        variants_specs=list(SOCIAL_BASELINE),
        master_bytes=raster_bytes,
        force_rerender=force_rerender,
    )

    # ----- Phase 1c: kind-specific full-res variants --------------------
    # PDF page 1 at 150 DPI → page1_url; video frame at native res → poster_url.
    kind_specific: list[str] = []
    try:
        if tmp_path is not None:
            kind_variants = await ts.render_kind_specific_variants_from_path(
                tmp_path, mime, file_name=file_name,
            )
        else:
            kind_variants = await ts.render_kind_specific_variants(
                content, mime, file_name=file_name,
            )
        for key, kind_content, kmime, family in kind_variants:
            await fm.sync_engine.variants.persist_prerendered_async(
                record,
                variant_key=key,
                content=kind_content,
                mime_type=kmime,
                variant_family=family,
                force_rerender=force_rerender,
            )
            kind_specific.append(key)
    except Exception as e:
        vcprint(
            f"[thumbnails] file={file_id} kind-specific failed: {e!r}",
            color="yellow",
        )

    elapsed = (time.monotonic() - started) * 1000
    vcprint(
        f"[thumbnails] file={file_id} mime={mime} "
        f"baseline={list(rendered.keys())} kind={kind_specific} "
        f"probed={list(probed.keys())} "
        f"source={'temp-file' if tmp_path is not None else 'in-memory'} "
        f"elapsed={elapsed:.0f}ms",
        color="cyan",
    )
    return bool(rendered) or bool(kind_specific) or bool(probed)


# Alias matching the call-site naming used by aidream's backfill script.
# generate_thumbnail_for_file now does much more than thumbnails (it
# probes metadata + renders kind-specific variants too); the alias
# makes that explicit at the import site.
ensure_media_processing = generate_thumbnail_for_file


__all__ = [
    "generate_thumbnail_for_file",
    "ensure_media_processing",
    "LARGE_MEDIA_THRESHOLD_BYTES",
]
