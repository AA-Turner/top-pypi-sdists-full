"""Tests for the D32 bounded-memory streaming primitives.

- ``matrx_files.zip_stream.stream_zip`` — entry-by-entry ZIP
  assembly through a non-seekable sink (data-descriptor mode).
- ``pdf.ops.iter_render_pages_to_image_bytes`` — lazy per-page renderer with
  back-pressure, matching the materializing ``render_all_pages_*`` output.
"""

from __future__ import annotations

import io
import zipfile
from collections.abc import AsyncIterator

import pymupdf
import pytest

from matrx_files.specific_handlers.pdf import (
    iter_render_pages_to_image_bytes,
    render_all_pages_to_image_bytes,
)
from matrx_files.zip_stream import ZipChunkSink, stream_zip



def _sample_pdf(page_count: int = 4) -> bytes:
    doc = pymupdf.open()
    try:
        for page_num in range(1, page_count + 1):
            page = doc.new_page(width=300, height=400)
            page.insert_text((72, 72), f"Stream sample page {page_num}")
        return doc.tobytes()
    finally:
        doc.close()


async def _entries_from(pairs: list[tuple[str, bytes]]) -> AsyncIterator[tuple[str, bytes]]:
    for pair in pairs:
        yield pair


# ---------------------------------------------------------------------------
# stream_zip
# ---------------------------------------------------------------------------


async def test_stream_zip_round_trips_a_valid_archive() -> None:
    pairs = [
        ("a.txt", b"alpha" * 100),
        ("dir/b.bin", bytes(range(256)) * 10),
        ("empty.txt", b""),
    ]
    chunks = [chunk async for chunk in stream_zip(_entries_from(pairs))]
    assert len(chunks) > 1  # streamed in pieces, not one blob

    archive = b"".join(chunks)
    with zipfile.ZipFile(io.BytesIO(archive)) as zf:
        assert zf.namelist() == [name for name, _ in pairs]
        for name, content in pairs:
            assert zf.read(name) == content
        # A valid archive passes the stdlib integrity check.
        assert zf.testzip() is None


async def test_stream_zip_yields_entry_bytes_incrementally() -> None:
    """Bytes for entry N must be emitted before entry N+1 is consumed —
    that is the whole point (bounded memory, no full-archive buffer)."""
    seen_before_second_entry: list[int] = []

    async def _entries() -> AsyncIterator[tuple[str, bytes]]:
        yield "first.bin", b"x" * 10_000
        # By the time the producer is asked for the second entry, the
        # consumer must already have received the first entry's bytes.
        seen_before_second_entry.append(total_out[0])
        yield "second.bin", b"y" * 10_000

    total_out = [0]
    async for chunk in stream_zip(_entries()):
        total_out[0] += len(chunk)

    assert seen_before_second_entry, "producer never reached the second entry"
    assert seen_before_second_entry[0] > 0, (
        "no bytes were flushed before the second entry — stream_zip is buffering"
    )


def test_zip_chunk_sink_is_non_seekable_and_drains() -> None:
    sink = ZipChunkSink()
    assert sink.writable()
    assert not sink.seekable()
    sink.write(b"abc")
    sink.write(b"def")
    assert sink.drain() == [b"abc", b"def"]
    assert sink.drain() == []


# ---------------------------------------------------------------------------
# iter_render_pages_to_image_bytes
# ---------------------------------------------------------------------------


async def test_iter_render_matches_materializing_render_all() -> None:
    pdf_bytes = _sample_pdf(4)
    expected = render_all_pages_to_image_bytes(pdf_bytes, dpi=72)

    streamed = [
        page async for page in iter_render_pages_to_image_bytes(pdf_bytes, dpi=72)
    ]

    assert [p.page_number for p in streamed] == [p.page_number for p in expected]
    assert [p.content for p in streamed] == [p.content for p in expected]
    assert all(p.format == "png" for p in streamed)


async def test_iter_render_subset_and_order() -> None:
    pdf_bytes = _sample_pdf(4)
    streamed = [
        page
        async for page in iter_render_pages_to_image_bytes(
            pdf_bytes, dpi=72, pages=[3, 1]
        )
    ]
    assert [p.page_number for p in streamed] == [3, 1]


async def test_iter_render_out_of_range_page_raises_before_first_item() -> None:
    pdf_bytes = _sample_pdf(2)
    agen = iter_render_pages_to_image_bytes(pdf_bytes, dpi=72, pages=[1, 99])
    with pytest.raises(ValueError, match="outside document range"):
        await anext(agen)


async def test_iter_render_early_close_does_not_hang() -> None:
    """Closing the generator mid-stream (client disconnect) must release the
    render thread promptly instead of deadlocking on the bounded queue."""
    pdf_bytes = _sample_pdf(4)
    agen = iter_render_pages_to_image_bytes(pdf_bytes, dpi=72, max_buffered=1)
    first = await anext(agen)
    assert first.page_number == 1
    await agen.aclose()  # must not hang
