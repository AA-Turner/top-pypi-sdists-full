"""Cloud text files resolve their uploaded bytes through the canonical file seam."""

from __future__ import annotations

import asyncio
import base64
from types import SimpleNamespace
from typing import Any


class _Query:
    def __init__(self, row: dict[str, Any]) -> None:
        self._row = row

    async def values(self, *fields: str) -> list[dict[str, Any]]:
        return [{field: self._row[field] for field in fields}]


class _Files:
    def __init__(self, row: dict[str, Any]) -> None:
        self._row = row

    def filter(self, *args: Any, **kwargs: Any) -> _Query:
        return _Query(self._row)


class _FileManager:
    def __init__(self, body: bytes) -> None:
        self._body = body
        self.calls: list[tuple[str | None, bool]] = []

    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool) -> Any:
        self.calls.append((ref.file_id, needs_bytes))
        return SimpleNamespace(
            resolver_error=None,
            base64_data=base64.b64encode(self._body).decode("ascii"),
        )


def _row(*, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "id": "11111111-1111-1111-1111-111111111111",
        "created_by": "22222222-2222-2222-2222-222222222222",
        "organization_id": None,
        "file_path": "Expert Systems/book.txt",
        "file_name": "book.txt",
        "mime_type": "text/plain; charset=utf-8",
        "storage_uri": "s3://private/book.txt",
        "metadata": metadata or {},
        "published_to_web": False,
        "parent_folder_id": None,
    }


def test_uploaded_text_file_reads_canonical_bytes(monkeypatch) -> None:
    import matrx_rag.sources as sources

    row = _row()
    body = b"Scientific advertising is salesmanship in print.\n"
    fm = _FileManager(body)
    monkeypatch.setattr(
        sources,
        "get_db_model",
        lambda name: _Files(row) if name == "Files" else None,
    )
    monkeypatch.setattr(sources, "get_cloud_file_manager", lambda: fm)

    resolved = asyncio.run(
        sources.resolve("cld_file", row["id"], user_id=row["created_by"])
    )

    assert resolved is not None
    assert resolved.text == body.decode()
    assert resolved.metadata["text_source"] == "file_bytes"
    assert fm.calls == [(row["id"], True)]


def test_pre_extracted_text_keeps_zero_io_fast_path(monkeypatch) -> None:
    import matrx_rag.sources as sources

    row = _row(metadata={"text": "already extracted"})
    monkeypatch.setattr(
        sources,
        "get_db_model",
        lambda name: _Files(row) if name == "Files" else None,
    )
    monkeypatch.setattr(
        sources,
        "get_cloud_file_manager",
        lambda: (_ for _ in ()).throw(AssertionError("file manager must not be called")),
    )

    resolved = asyncio.run(
        sources.resolve("cld_file", row["id"], user_id=row["created_by"])
    )

    assert resolved is not None
    assert resolved.text == "already extracted"
    assert resolved.metadata["text_source"] == "metadata"
