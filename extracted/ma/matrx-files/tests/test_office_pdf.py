from __future__ import annotations

import base64
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_files import FileRef
from matrx_files.office_pdf import (
    PDF_CONVERSION_KIND,
    conversion_cache_key,
    convert_office_pdf,
)
from matrx_files.specific_handlers.office import PresentationSpec, SlideSpec, generate_office
from matrx_files.specific_handlers.office.convert import libreoffice_available


def _sample_pptx(slide_count: int = 3) -> bytes:
    spec = PresentationSpec(
        title="Test deck",
        slides=[
            SlideSpec(title=f"Slide {n}", bullets=[f"Point {n}.1", f"Point {n}.2"])
            for n in range(1, slide_count + 1)
        ],
    )
    return base64.b64decode(generate_office(spec).base64_data)


class _FakeDb:
    def __init__(self) -> None:
        self.cached: dict[str, Any] | None = None
        self.find_kwargs: dict[str, Any] = {}
        self.derivative: dict[str, Any] | None = None

    async def find_derivative_async(self, **kwargs: Any) -> dict[str, Any] | None:
        self.find_kwargs = kwargs
        return self.cached

    async def get_file_async(self, file_id: str) -> dict[str, Any] | None:
        return self.derivative or {
            "id": file_id,
            "file_name": "converted.pdf",
            "mime_type": "application/pdf",
            "size_bytes": 123,
            "published_to_web": False,
            "shown_to": "only_me",
            "metadata": {},
        }


class _FakeRouter:
    def __init__(self, source: bytes) -> None:
        self.source = source
        self.calls = 0

    async def read_async(self, _: str) -> bytes:
        self.calls += 1
        return self.source


class _FakeSyncEngine:
    def __init__(self) -> None:
        self.content: bytes | None = None
        self.kwargs: dict[str, Any] = {}

    async def managed_write_async(
        self, _: str, content: bytes, **kwargs: Any
    ) -> SimpleNamespace:
        self.content = content
        self.kwargs = kwargs
        return SimpleNamespace(file_id="converted-file-id")


class _FakeService:
    def __init__(self, source: bytes, *, mime_type: str, file_name: str) -> None:
        self.source_record = {
            "id": "source-file-id",
            "mime_type": mime_type,
            "file_name": file_name,
            "size_bytes": len(source),
            "checksum": "source-sha",
            "current_version": 2,
            "published_to_web": False,
            "shown_to": "only_me",
            "created_by": "owner-id",
            "storage_uri": "s3://bucket/source",
        }
        self.db = _FakeDb()
        self.router = _FakeRouter(source)
        self.sync_engine = _FakeSyncEngine()

    async def read_record(self, _: str, **__: Any) -> dict[str, Any]:
        return self.source_record

    async def build_file_ref(self, record: dict[str, Any], **_: Any) -> FileRef:
        return FileRef(
            file_id=str(record["id"]),
            file_name=record.get("file_name"),
            mime_type=record.get("mime_type"),
            size_bytes=record.get("size_bytes"),
            url="https://example.test/converted.pdf",
        )


PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"


async def test_non_office_source_is_rejected_before_any_byte_read() -> None:
    service = _FakeService(b"%PDF-1.7", mime_type="application/pdf", file_name="a.pdf")
    with pytest.raises(ValueError, match="not an\n?.*Office|not an "):
        await convert_office_pdf(
            service,  # type: ignore[arg-type]
            file_id="source-file-id",
            user_id="owner-id",
        )
    assert service.router.calls == 0


async def test_cached_conversion_fetches_zero_source_bytes() -> None:
    service = _FakeService(b"unused", mime_type=PPTX_MIME, file_name="deck.pptx")
    service.db.cached = {
        "id": "cached-pdf-id",
        "file_name": "deck.pdf",
        "mime_type": "application/pdf",
        "size_bytes": 321,
        "published_to_web": False,
        "shown_to": "only_me",
        "metadata": {},
        "derivation_metadata": {"source_office_kind": "pptx", "page_count": 3},
    }

    result = await convert_office_pdf(
        service,  # type: ignore[arg-type]
        file_id="source-file-id",
        user_id="owner-id",
    )

    assert result.cache_hit is True
    assert result.page_count == 3
    assert result.office_kind == "pptx"
    assert result.file.file_id == "cached-pdf-id"
    assert service.router.calls == 0
    assert service.db.find_kwargs["derivation_kind"] == PDF_CONVERSION_KIND


def test_cache_key_invalidates_on_source_revision_change() -> None:
    base = {"id": "f1", "checksum": "abc", "current_version": 1}
    assert conversion_cache_key(base) == conversion_cache_key(dict(base))
    assert conversion_cache_key(base) != conversion_cache_key({**base, "checksum": "def"})
    assert conversion_cache_key(base) != conversion_cache_key({**base, "id": "f2"})


@pytest.mark.skipif(not libreoffice_available(), reason="LibreOffice not on this host")
async def test_derivative_inherits_parent_org_and_row_access() -> None:
    # An org-owned deck's PDF derivative must land in the PARENT's org and
    # web lane and list filter — never fall back to the writer's personal org (the
    # wrong-tenant defect inherit_derived_file_policy exists to prevent).
    service = _FakeService(_sample_pptx(1), mime_type=PPTX_MIME, file_name="deck.pptx")
    service.source_record["organization_id"] = "org-1234"
    service.source_record["published_to_web"] = True
    service.source_record["shown_to"] = "my_team"

    await convert_office_pdf(
        service,  # type: ignore[arg-type]
        file_id="source-file-id",
        user_id="owner-id",
    )

    assert service.sync_engine.kwargs["published_to_web"] is True
    assert service.sync_engine.kwargs["shown_to"] == "my_team"
    assert service.sync_engine.kwargs["metadata"]["organization_id"] == "org-1234"


@pytest.mark.skipif(not libreoffice_available(), reason="LibreOffice not on this host")
async def test_pptx_converts_to_real_pdf_derivative_with_slide_count() -> None:
    # The PDF page count must equal the deck's ACTUAL slide count — measured
    # from the bytes via the codec, not assumed from the spec (the generator's
    # `title=` adds a title slide on top of the 3 content slides).
    raw = _sample_pptx(3)
    from matrx_files.specific_handlers.office import extract_office

    slide_count = len(extract_office(raw, file_name="deck.pptx").portions)
    service = _FakeService(raw, mime_type=PPTX_MIME, file_name="deck.pptx")

    result = await convert_office_pdf(
        service,  # type: ignore[arg-type]
        file_id="source-file-id",
        user_id="owner-id",
    )

    assert result.cache_hit is False
    assert result.office_kind == "pptx"
    assert result.page_count == slide_count
    assert service.sync_engine.content is not None
    assert service.sync_engine.content.startswith(b"%PDF")
    assert service.sync_engine.kwargs["parent_file_id"] == "source-file-id"
    assert service.sync_engine.kwargs["derivation_kind"] == PDF_CONVERSION_KIND
    meta = service.sync_engine.kwargs["derivation_metadata"]
    assert meta["source_office_kind"] == "pptx"
    assert meta["page_count"] == slide_count
    assert meta["source_checksum"] == "source-sha"
