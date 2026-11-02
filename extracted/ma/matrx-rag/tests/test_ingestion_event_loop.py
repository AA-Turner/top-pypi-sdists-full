from __future__ import annotations

import asyncio
import time

import pytest

from matrx_rag import image_pipeline, ingestion, pdf_pipeline
from matrx_rag.sources import ResolvedSource


@pytest.mark.asyncio
async def test_source_chunking_does_not_block_event_loop(monkeypatch) -> None:
    def slow_chunk_text(
        text: str,
        *,
        language: str | None = None,
    ) -> list[ingestion.Chunk]:
        del text, language
        time.sleep(0.2)
        return []

    monkeypatch.setattr(ingestion, "chunk_text", slow_chunk_text)
    source = ResolvedSource(
        source_kind="note",
        source_id="source-1",
        field_id=None,
        owner_id="owner-1",
        organization_id="org-1",
        text="content",
        mime_type="text/plain",
        language="en",
        source_hash="source-hash",
        metadata={},
    )
    started_at = asyncio.get_running_loop().time()
    heartbeat_at: float | None = None

    async def heartbeat() -> None:
        nonlocal heartbeat_at
        await asyncio.sleep(0.01)
        heartbeat_at = asyncio.get_running_loop().time()

    await asyncio.gather(ingestion._chunk_source("note", source), heartbeat())

    assert heartbeat_at is not None
    assert heartbeat_at - started_at < 0.1


@pytest.mark.asyncio
async def test_embedding_payload_formatting_does_not_block_event_loop(monkeypatch) -> None:
    original_format_vector = ingestion._format_vector

    def slow_format_vector(values: list[float]) -> str:
        time.sleep(0.2)
        return original_format_vector(values)

    monkeypatch.setattr(ingestion, "_format_vector", slow_format_vector)
    started_at = asyncio.get_running_loop().time()
    heartbeat_at: float | None = None

    async def heartbeat() -> None:
        nonlocal heartbeat_at
        await asyncio.sleep(0.01)
        heartbeat_at = asyncio.get_running_loop().time()

    payloads, _ = await asyncio.gather(
        ingestion._format_embedding_payloads(
            ["chunk-1"],
            [[1, 2.5]],
            organization_id="org-1",
            owner_id="owner-1",
        ),
        heartbeat(),
    )

    assert payloads == [("chunk-1", "org-1", "owner-1", "[1.0,2.5]")]
    assert heartbeat_at is not None
    assert heartbeat_at - started_at < 0.1


@pytest.mark.asyncio
async def test_pdf_table_chunking_does_not_block_event_loop(monkeypatch) -> None:
    def slow_append(
        chunks: list[pdf_pipeline.Chunk],
        tables: list[dict[str, object]],
    ) -> None:
        del chunks, tables
        time.sleep(0.2)

    monkeypatch.setattr(pdf_pipeline, "_append_pdf_table_chunks", slow_append)
    started_at = asyncio.get_running_loop().time()
    heartbeat_at: float | None = None

    async def heartbeat() -> None:
        nonlocal heartbeat_at
        await asyncio.sleep(0.01)
        heartbeat_at = asyncio.get_running_loop().time()

    await asyncio.gather(pdf_pipeline._add_pdf_table_chunks([], []), heartbeat())

    assert heartbeat_at is not None
    assert heartbeat_at - started_at < 0.1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "operation",
    [
        lambda: pdf_pipeline._local_path_exists("/tmp/rag-test.pdf"),
        lambda: image_pipeline._read_local_bytes("/tmp/rag-test.png"),
    ],
)
async def test_local_file_probes_do_not_block_event_loop(monkeypatch, operation) -> None:
    def slow_exists(self) -> bool:
        del self
        time.sleep(0.2)
        return False

    monkeypatch.setattr(pdf_pipeline.Path, "exists", slow_exists)
    started_at = asyncio.get_running_loop().time()
    heartbeat_at: float | None = None

    async def heartbeat() -> None:
        nonlocal heartbeat_at
        await asyncio.sleep(0.01)
        heartbeat_at = asyncio.get_running_loop().time()

    await asyncio.gather(operation(), heartbeat())

    assert heartbeat_at is not None
    assert heartbeat_at - started_at < 0.1


@pytest.mark.asyncio
async def test_image_file_read_does_not_block_event_loop(monkeypatch) -> None:
    monkeypatch.setattr(image_pipeline.Path, "exists", lambda self: True)

    def slow_read_bytes(self) -> bytes:
        del self
        time.sleep(0.2)
        return b"image"

    monkeypatch.setattr(image_pipeline.Path, "read_bytes", slow_read_bytes)
    started_at = asyncio.get_running_loop().time()
    heartbeat_at: float | None = None

    async def heartbeat() -> None:
        nonlocal heartbeat_at
        await asyncio.sleep(0.01)
        heartbeat_at = asyncio.get_running_loop().time()

    raw_bytes, _ = await asyncio.gather(
        image_pipeline._read_local_bytes("/tmp/rag-test.png"),
        heartbeat(),
    )

    assert raw_bytes == b"image"
    assert heartbeat_at is not None
    assert heartbeat_at - started_at < 0.1
