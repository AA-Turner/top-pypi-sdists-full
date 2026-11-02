from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pymupdf
import pytest

from matrx_files import FileRef
from matrx_files.backends.s3_backend import S3Backend
from matrx_files.pdf_pages import (
    MAX_SELECTED_PDF_PAGES,
    PDF_PAGE_SELECTION_KIND,
    PdfPageSelectionRequest,
    requested_page_numbers,
    select_pdf_pages,
)


def _sample_pdf(page_count: int = 1000) -> bytes:
    doc = pymupdf.open()
    try:
        for page_number in range(1, page_count + 1):
            page = doc.new_page(width=200, height=200)
            page.insert_text((24, 40), f"Legal source page {page_number}")
        return doc.tobytes()
    finally:
        doc.close()


class _FakeDb:
    def __init__(self) -> None:
        self.cached: dict[str, Any] | None = None
        self.derivative: dict[str, Any] | None = None

    async def find_derivative_async(self, **_: Any) -> dict[str, Any] | None:
        return self.cached

    async def update_file_async(
        self, file_id: str, updates: dict[str, Any]
    ) -> dict[str, Any]:
        self.derivative = {
            "id": file_id,
            "file_name": "selected.pdf",
            "mime_type": "application/pdf",
            "size_bytes": 123,
            "visibility": "personal",
            "metadata": {},
            **updates,
        }
        return self.derivative

    async def get_file_async(self, _: str) -> dict[str, Any] | None:
        return self.derivative or {
            "id": "selected-file-id",
            "file_name": "selected.pdf",
            "mime_type": "application/pdf",
            "size_bytes": 123,
            "visibility": "personal",
            "metadata": {},
        }


class _FakeRouter:
    def __init__(self, source: bytes) -> None:
        self.source = source
        self.calls = 0

    async def download_to_path_async(self, _: str, local_path: str) -> int:
        self.calls += 1
        Path(local_path).write_bytes(self.source)
        return len(self.source)


class _FakeSyncEngine:
    def __init__(self) -> None:
        self.content: bytes | None = None
        self.kwargs: dict[str, Any] = {}

    async def managed_write_async(
        self, _: str, content: bytes, **kwargs: Any
    ) -> SimpleNamespace:
        self.content = content
        self.kwargs = kwargs
        return SimpleNamespace(file_id="selected-file-id")


class _FakeService:
    def __init__(self, source: bytes) -> None:
        self.source_record = {
            "id": "source-file-id",
            "mime_type": "application/pdf",
            "size_bytes": len(source),
            "checksum": "source-sha",
            "current_version": 7,
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
            url="https://example.test/selected.pdf",
        )


async def test_sparse_pages_from_thousand_page_pdf_stay_one_ordered_file() -> None:
    service = _FakeService(_sample_pdf())

    result = await select_pdf_pages(
        service,  # type: ignore[arg-type]
        file_id="source-file-id",
        user_id="owner-id",
        request=PdfPageSelectionRequest(pages=[997, 2, 500, 2]),
    )

    assert result.source_pages == [997, 2, 500]
    assert result.source_page_count == 1000
    assert result.source_bytes_fetched == len(service.router.source)
    assert result.source_fetch_strategy == "full_object_stream_to_disk"
    assert result.output_page_map[0].source_page == 997
    assert service.router.calls == 1
    assert service.sync_engine.kwargs["parent_file_id"] == "source-file-id"
    assert service.sync_engine.kwargs["derivation_kind"] == PDF_PAGE_SELECTION_KIND
    assert service.sync_engine.kwargs["derivation_metadata"]["source_pages"] == [997, 2, 500]

    assert service.sync_engine.content is not None
    selected = pymupdf.open(
        stream=service.sync_engine.content,
        filetype="pdf",
    )
    try:
        assert selected.page_count == 3
        assert "Legal source page 997" in selected[0].get_text()
        assert "Legal source page 2" in selected[1].get_text()
        assert "Legal source page 500" in selected[2].get_text()
    finally:
        selected.close()


async def test_cached_selection_fetches_zero_source_bytes() -> None:
    service = _FakeService(_sample_pdf(4))
    service.db.cached = {
        "id": "cached-file-id",
        "file_name": "cached.pdf",
        "mime_type": "application/pdf",
        "size_bytes": 321,
        "visibility": "personal",
        "metadata": {},
        "derivation_metadata": {"source_page_count": 4},
    }

    result = await select_pdf_pages(
        service,  # type: ignore[arg-type]
        file_id="source-file-id",
        user_id="owner-id",
        request=PdfPageSelectionRequest(pages=[4, 1]),
    )

    assert result.cache_hit is True
    assert result.source_bytes_fetched == 0
    assert result.source_fetch_strategy == "cache_hit"
    assert result.file.file_id == "cached-file-id"
    assert service.router.calls == 0


def test_page_selection_validation_is_bounded_before_expansion() -> None:
    assert requested_page_numbers([4, 1, 4], None) == [4, 1]
    with pytest.raises(ValueError, match="at most"):
        PdfPageSelectionRequest(
            page_ranges=[{"start": 1, "end": MAX_SELECTED_PDF_PAGES + 1}]
        )


def test_s3_materialization_uses_native_download_to_disk(tmp_path: Path) -> None:
    payload = b"large-pdf-placeholder"

    class _Client:
        calls: list[tuple[str, str]] = []

        def download_file(self, bucket: str, key: str, local_path: str) -> None:
            self.calls.append((bucket, key))
            Path(local_path).write_bytes(payload)

    client = _Client()
    backend = S3Backend.__new__(S3Backend)
    backend._configured = True
    backend._default_bucket = ""
    backend._client = client
    destination = tmp_path / "source.pdf"

    written = backend.download_to_path("legal-bucket/matter/source.pdf", str(destination))

    assert client.calls == [("legal-bucket", "matter/source.pdf")]
    assert destination.read_bytes() == payload
    assert written == len(payload)
