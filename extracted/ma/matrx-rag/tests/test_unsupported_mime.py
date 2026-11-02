"""Phase 2c — UnsupportedMimeError surfacing.

Non-text MIMEs whose ingestion pipeline isn't wired must NOT silently
return ``None`` from the resolver — that leaves the user's document
stuck at ``status='pending'`` forever with no feedback. Instead the
resolver raises ``UnsupportedMimeError``, and the ingestion path
converts it into a structured IngestionResult + an
``rag.ingest.error`` stream event.

Both readers (``matrx_rag.sources._resolve_cld_file`` and
``matrx_rag.ingestion._maybe_dispatch_pdf``) go through
``get_db_model("Files")`` now — the tests stub that ORM lookup so they run
without a live DB.
"""

from __future__ import annotations

import asyncio
from typing import Any


class _StubFilesQuery:
    """Stands in for the ``Files.filter(...)`` QueryBuilder chain used by
    ``matrx_rag.sources._resolve_cld_file`` — the only method it needs is
    the terminal ``values()`` used there."""

    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def filter(self, *args, **kwargs):
        return self

    async def values(self, *fields):
        return self._rows


class _StubFilesModel:
    def __init__(self, row: dict[str, Any] | None) -> None:
        # sources.py selects a fixed column set for files.files — shape the
        # row the same way the real Files model / asyncpg row would.
        if row is None:
            self._rows: list[dict[str, Any]] = []
        else:
            self._rows = [
                {
                    "id": row["id"],
                    "created_by": row["owner_id"],
                    "organization_id": row["organization_id"],
                    "file_path": row["file_path"],
                    "file_name": row["file_name"],
                    "mime_type": row["mime_type"],
                    "storage_uri": row["storage_uri"],
                    "metadata": row["metadata"],
                    "published_to_web": False,
                    "parent_folder_id": None,
                }
            ]

    def filter(self, *args, **kwargs):
        return _StubFilesQuery(self._rows)


def _install_stub_pool(monkeypatch, row: dict[str, Any] | None) -> None:
    stub_files_model = _StubFilesModel(row)

    def _fake_get_db_model(name: str, schema: str | None = None):
        if name == "Files":
            return stub_files_model
        raise AssertionError(f"unexpected get_db_model({name!r}) call in this test")

    # ingestion.py's PDF-dispatch MIME lookup (_maybe_dispatch_pdf) now reads
    # via get_db_model("Files") too (same name/shape as sources.py's
    # _resolve_cld_file) — stub the ORM lookup in BOTH modules so
    # ingest_source's pre-check for cld_file sees the same row everywhere.
    import matrx_rag.ingestion as ingestion_mod

    monkeypatch.setattr(ingestion_mod, "get_db_model", _fake_get_db_model)

    # sources.py's _resolve_cld_file reads via get_db_model("Files") too —
    # stub the ORM lookup instead of a raw connection. The caller in every
    # test here is the file's owner (owner_id == user_id passed to
    # resolve()/ingest_source()), so the ACL short-circuits on the
    # created_by == user_id branch and never touches Permissions /
    # OrganizationMember.
    import matrx_rag.sources as sources_mod

    monkeypatch.setattr(sources_mod, "get_db_model", _fake_get_db_model)


def test_resolve_cld_file_raises_unsupported_mime(monkeypatch):
    """A cld_file with a MIME outside TEXT_MIMES (and not a PDF/image
    routed by ingest_source) → UnsupportedMimeError, not silent None."""
    from matrx_rag.sources import UnsupportedMimeError, resolve

    row = {
        "id": "11111111-1111-1111-1111-111111111111",
        "owner_id": "22222222-2222-2222-2222-222222222222",
        "organization_id": None,
        "file_path": "/x/song.mp3",
        "file_name": "song.mp3",
        "mime_type": "audio/mpeg",
        "storage_uri": "s3://b/song.mp3",
        "metadata": {},
    }
    _install_stub_pool(monkeypatch, row)

    try:
        # user_id required since the fail-closed ownership contract (P0-11):
        # resolve() returns None immediately without one.
        asyncio.run(resolve("cld_file", row["id"], None, user_id=row["owner_id"]))
    except UnsupportedMimeError as exc:
        assert exc.mime_type == "audio/mpeg"
        assert exc.file_name == "song.mp3"
        assert exc.source_id == row["id"]
        return
    raise AssertionError("UnsupportedMimeError was not raised")


def test_classify_binary_pipeline_is_the_one_source_of_truth():
    """PDF/image detection lives in ONE function — by MIME or by suffix (a TUS
    upload routinely lands as application/octet-stream)."""
    from matrx_rag.sources import classify_binary_pipeline

    assert classify_binary_pipeline("application/pdf", None) == "pdf"
    assert classify_binary_pipeline("application/pdf; charset=binary", None) == "pdf"
    assert classify_binary_pipeline("application/octet-stream", "scan.PDF") == "pdf"
    assert classify_binary_pipeline("image/png", None) == "image"
    assert classify_binary_pipeline(None, "photo.jpeg") == "image"
    # Genuinely unwired — no pipeline owns these.
    assert classify_binary_pipeline("audio/mpeg", "song.mp3") == ""
    assert classify_binary_pipeline("text/plain", "a.txt") == ""


def test_resolve_cld_file_pdf_raises_quietly_as_binary_pipeline(monkeypatch):
    """A PDF reaching the TEXT resolver is NORMAL — auto_ingest pre-resolves
    here for cost/change detection before ingest_source dispatches it to the
    pdf_pipeline. It must raise with ``binary_pipeline=True`` and must NOT
    print the red 'no extraction pipeline wired' banner: that banner was a LIE
    on every PDF ingest (the pipeline ran fine straight after), and a guard
    that cries wolf is a guard nobody reads."""
    import matrx_rag.sources as sources_mod
    from matrx_rag.sources import UnsupportedMimeError, resolve

    row = {
        "id": "66666666-6666-6666-6666-666666666666",
        "owner_id": "77777777-7777-7777-7777-777777777777",
        "organization_id": None,
        "file_path": "/x/letter.pdf",
        "file_name": "letter.pdf",
        "mime_type": "application/pdf",
        "storage_uri": "s3://b/letter.pdf",
        "metadata": {},
    }
    _install_stub_pool(monkeypatch, row)

    banners: list[dict[str, Any]] = []
    monkeypatch.setattr(
        sources_mod,
        "vcprint",
        lambda *a, **kw: banners.append(kw),
    )

    try:
        asyncio.run(resolve("cld_file", row["id"], None, user_id=row["owner_id"]))
    except UnsupportedMimeError as exc:
        assert exc.binary_pipeline is True
        assert exc.mime_type == "application/pdf"
        assert banners == [], f"PDF must not print an unsupported-mime banner, got {banners}"
        return
    raise AssertionError("UnsupportedMimeError was not raised")


def test_resolve_cld_file_unwired_mime_is_structured_warning(monkeypatch):
    """A genuinely unwired user upload stays typed but does not pollute ERROR logs."""
    import matrx_rag.sources as sources_mod
    from matrx_rag.sources import UnsupportedMimeError, resolve

    row = {
        "id": "88888888-8888-8888-8888-888888888888",
        "owner_id": "99999999-9999-9999-9999-999999999999",
        "organization_id": None,
        "file_path": "/x/song.mp3",
        "file_name": "song.mp3",
        "mime_type": "audio/mpeg",
        "storage_uri": "s3://b/song.mp3",
        "metadata": {},
    }
    _install_stub_pool(monkeypatch, row)

    banners: list[dict[str, Any]] = []
    monkeypatch.setattr(
        sources_mod,
        "vcprint",
        lambda *a, **kw: banners.append(kw),
    )

    try:
        asyncio.run(resolve("cld_file", row["id"], None, user_id=row["owner_id"]))
    except UnsupportedMimeError as exc:
        assert exc.binary_pipeline is False
        assert len(banners) == 1 and "UNSUPPORTED MIME" in banners[0]["title"]
        # A user-uploaded type outside the currently wired extraction set is
        # returned through the typed RagIngestError path below; it is not an
        # operational ERROR for the production repair queue.
        assert banners[0]["color"] == "yellow"
        return
    raise AssertionError("UnsupportedMimeError was not raised")


def test_resolve_cld_file_returns_none_for_missing_row(monkeypatch):
    """A missing row still returns None — the resolver only raises on
    found-but-unwired. Distinguishes 'deleted between enqueue and
    pickup' (benign) from 'binary we can't process' (error)."""
    from matrx_rag.sources import resolve

    _install_stub_pool(monkeypatch, None)
    out = asyncio.run(
        resolve(
            "cld_file",
            "00000000-0000-0000-0000-000000000000",
            None,
            user_id="22222222-2222-2222-2222-222222222222",
        )
    )
    assert out is None


def test_ingest_source_surfaces_unsupported_mime_event(monkeypatch):
    """ingest_source catches UnsupportedMimeError, returns a structured
    IngestionResult with an unsupported_mime error, AND emits an
    ``rag.ingest.error`` stream event so the FE sees it."""
    from matrx_rag.ingestion import ingest_source

    row = {
        "id": "33333333-3333-3333-3333-333333333333",
        "owner_id": "44444444-4444-4444-4444-444444444444",
        "organization_id": None,
        "file_path": "/x/sheet.xlsx",
        "file_name": "sheet.xlsx",
        "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "storage_uri": "s3://b/sheet.xlsx",
        "metadata": {},
    }
    _install_stub_pool(monkeypatch, row)

    events: list[dict[str, Any]] = []

    class _Emitter:
        async def send_data(self, payload):
            # ingestion emits typed models (matrx_rag.rag_events.RagIngestError);
            # record the wire dict the FE would see.
            events.append(payload.model_dump() if hasattr(payload, "model_dump") else payload)

    result = asyncio.run(
        ingest_source(
            "cld_file",
            row["id"],
            None,
            force=False,
            emitter=_Emitter(),
            # user_id required since the fail-closed ownership contract (P0-11).
            user_id=row["owner_id"],
            # organization_id is required since the 2026-06-03 leak-class guard
            # (ingestion.py); the unsupported-mime path is reached only after it.
            organization_id="55555555-5555-5555-5555-555555555555",
        )
    )
    assert result.chunks_written == 0
    assert result.error and result.error.startswith("unsupported_mime:")
    assert result.error and "spreadsheetml" in result.error

    err_events = [e for e in events if e.get("kind") == "rag.ingest.error"]
    assert len(err_events) == 1, f"expected one error event, got {events}"
    ev = err_events[0]
    assert ev["error_type"] == "unsupported_mime"
    assert ev["mime_type"].startswith("application/vnd.openxml")
    assert ev["file_name"] == "sheet.xlsx"
    assert ev["source_id"] == row["id"]


def test_ingest_source_distinct_error_for_missing_source(monkeypatch):
    """A row that doesn't exist still produces a clean 'source_not_found'
    error — distinct error string from unsupported_mime so a caller can
    tell them apart in metrics / FE handling."""
    from matrx_rag.ingestion import ingest_source

    _install_stub_pool(monkeypatch, None)
    result = asyncio.run(
        ingest_source(
            "cld_file",
            "00000000-0000-0000-0000-000000000000",
            None,
            force=False,
            # user_id required since the fail-closed ownership contract (P0-11).
            user_id="44444444-4444-4444-4444-444444444444",
            # organization_id is required since the 2026-06-03 leak-class guard.
            organization_id="55555555-5555-5555-5555-555555555555",
        )
    )
    assert result.error == "source_not_found"
