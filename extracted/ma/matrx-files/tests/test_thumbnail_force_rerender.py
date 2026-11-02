"""Forcing-function tests for the force_rerender healing path.

``force_rerender`` exists to heal the variant-key dedup trap: a master
whose real variant keys are occupied by STALE content (mime-icon
thumbnails written before the Office/PDF page-1 render lanes existed).
Plain re-runs skip occupied keys forever, so the only way to fix them is
to overwrite in place.

Overwriting is destructive, which makes ONE property load-bearing:

    A force-rerender must NEVER replace a real thumbnail with a
    mime-icon fallback.

Every per-family rasteriser degrades to the deterministic mime icon when
it fails (corrupt file, a LibreOffice conversion that dies on one
document). Without a guard, a single failing file turns a good page-1
thumbnail into a gray placeholder — and because the write succeeds,
nothing would ever flag it.

These tests exercise ``_process_source`` (the real system under test)
against in-memory fakes, so a regression in the guard fails here rather
than in production S3.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_files.cloud_sync.processing import thumbnails as sut
from matrx_files.specific_handlers import thumbnail_source as ts

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

REAL_RENDER = b"\x89PNG\r\n\x1a\n-pretend-this-is-a-real-page-1-render"


class _FakeVariants:
    """Records what the pipeline asked it to write."""

    def __init__(self) -> None:
        self.render_calls: list[dict[str, Any]] = []
        self.prerendered_calls: list[dict[str, Any]] = []

    async def render_async(self, record, *, variants_specs, master_bytes, force_rerender=False):
        self.render_calls.append(
            {
                "master_bytes": master_bytes,
                "force_rerender": force_rerender,
                "keys": [s.get("key") for s in variants_specs],
            }
        )
        return {s["key"]: object() for s in variants_specs if s.get("key")}

    async def persist_prerendered_async(self, record, **kwargs):
        self.prerendered_calls.append(kwargs)
        return object()


class _FakeDb:
    async def update_file_async(self, file_id, updates):  # pragma: no cover - unused here
        return None


class _FakeSyncEngine:
    def __init__(self) -> None:
        self.variants = _FakeVariants()
        self.db = _FakeDb()


class _FakeFm:
    def __init__(self) -> None:
        self.sync_engine = _FakeSyncEngine()


def _record() -> dict[str, Any]:
    return {
        "id": "11111111-1111-1111-1111-111111111111",
        "owner_id": "22222222-2222-2222-2222-222222222222",
        "file_name": "quarterly-report.docx",
        "file_path": "docs/quarterly-report.docx",
        "mime_type": DOCX_MIME,
        "metadata": {},
    }


async def _run(fm, *, raster: bytes, force_rerender: bool) -> bool:
    """Drive _process_source with a rasteriser pinned to ``raster``."""

    class _StubTs:
        # The guard compares against the REAL icon renderer — never stub it,
        # or the test would pass while the production comparison is broken.
        render_mime_icon_bytes = staticmethod(ts.render_mime_icon_bytes)

        @staticmethod
        async def probe_source_metadata(content, mime, *, file_name=None):
            return {}

        @staticmethod
        async def render_thumbnail_source_bytes(content, mime, *, file_name=None):
            return raster, "image/png"

        @staticmethod
        async def render_kind_specific_variants(content, mime, *, file_name=None):
            return []

    return await sut._process_source(
        fm,
        _record()["id"],
        _record(),
        DOCX_MIME,
        _StubTs,
        content=b"fake-docx-bytes",
        tmp_path=None,
        started=0.0,
        force_rerender=force_rerender,
    )


@pytest.mark.asyncio
async def test_force_rerender_refuses_to_overwrite_with_mime_icon():
    """THE load-bearing property: a failed render must not clobber real content.

    The rasteriser returns exactly what the real dispatcher returns when an
    Office conversion fails — the deterministic mime icon. The pipeline must
    write NOTHING.
    """
    fm = _FakeFm()
    icon = ts.render_mime_icon_bytes(mime_type=DOCX_MIME)

    ok = await _run(fm, raster=icon, force_rerender=True)

    assert ok is False, "a refused force-rerender must report failure, not success"
    assert fm.sync_engine.variants.render_calls == [], (
        "REGRESSION: the pipeline overwrote existing variants with a mime icon. "
        "This silently replaces real page-1 thumbnails with gray placeholders."
    )


@pytest.mark.asyncio
async def test_force_rerender_writes_when_the_render_is_real():
    """The guard must not block the healing path it exists to enable."""
    fm = _FakeFm()

    ok = await _run(fm, raster=REAL_RENDER, force_rerender=True)

    assert ok is True
    assert len(fm.sync_engine.variants.render_calls) == 1
    call = fm.sync_engine.variants.render_calls[0]
    assert call["master_bytes"] == REAL_RENDER
    assert call["force_rerender"] is True, (
        "force_rerender must reach VariantsService — without it the existing "
        "keys are reused and the stale icons are never healed."
    )


@pytest.mark.asyncio
async def test_bare_db_row_is_reconciled_not_crashed():
    """A caller-supplied BARE DB row (created_by, no owner_id) must still work.

    The DB column is ``created_by``; Python code expects ``owner_id`` (the
    read-path shim in db.py maps one to the other). The backfill queries the
    ORM directly, so its rows skip that shim — and the variants service only
    touches ``owner_id`` on the WRITE path. The result was a KeyError that
    fired exclusively for files that actually needed a new variant, i.e. every
    file the backfill existed to fix, while files with nothing to do passed
    cleanly. The whole universal backfill was inert and reported success.

    There is exactly one thing the caller can mean here, so the pipeline
    reconciles instead of dying.
    """
    bare = {k: v for k, v in _record().items() if k != "owner_id"}
    bare["created_by"] = "22222222-2222-2222-2222-222222222222"
    assert "owner_id" not in bare, "the fixture must reproduce the bare-row shape"

    out = await sut._reconcile_owner_id(bare, bare["id"], _FakeDb())

    assert out is not None
    assert out["owner_id"] == "22222222-2222-2222-2222-222222222222", (
        "owner_id must be reconciled from created_by before any write path"
    )


@pytest.mark.asyncio
async def test_record_without_owner_or_creator_is_re_read():
    """No usable identity in the record → go back to the DB, don't guess."""

    canonical = {**_record(), "owner_id": "33333333-3333-3333-3333-333333333333"}

    class _ReReadDb(_FakeDb):
        def __init__(self) -> None:
            self.reads: list[str] = []

        async def get_file_async(self, file_id):
            self.reads.append(file_id)
            return canonical

    db = _ReReadDb()
    stripped = {k: v for k, v in _record().items() if k not in ("owner_id", "created_by")}

    out = await sut._reconcile_owner_id(stripped, stripped["id"], db)

    assert db.reads == [stripped["id"]], "must re-read exactly once"
    assert out["owner_id"] == "33333333-3333-3333-3333-333333333333"


@pytest.mark.asyncio
async def test_reconcile_is_a_no_op_when_owner_id_is_present():
    """The happy path must not pay for a DB read."""

    class _ExplodingDb(_FakeDb):
        async def get_file_async(self, file_id):
            raise AssertionError("must not re-read when owner_id is already present")

    rec = _record()
    out = await sut._reconcile_owner_id(rec, rec["id"], _ExplodingDb())
    assert out is rec


@pytest.mark.asyncio
async def test_a_failed_render_stores_no_thumbnail_on_a_first_pass():
    """No gray icon is ever stored as a thumbnail (main's ruling, 2026-10-21).

    A first-pass upload whose render fell back to the mime icon stores
    nothing; the clients draw the type icon plus "Preview unavailable".
    """
    fm = _FakeFm()
    icon = ts.render_mime_icon_bytes(mime_type=DOCX_MIME)

    ok = await _run(fm, raster=icon, force_rerender=False)

    assert ok is False
    assert fm.sync_engine.variants.render_calls == [], (
        "a gray mime-icon placeholder was stored as the file's thumbnail"
    )
