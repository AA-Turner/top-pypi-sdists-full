"""Streaming ZIP assembly — bounded-memory archive responses.

Building an archive in ``io.BytesIO`` and returning it in one response body
double-buffers every entry on top of the source bytes. ``stream_zip`` writes
the archive through a non-seekable chunk sink instead: because the sink can't
seek, ``zipfile`` emits data descriptors after each entry, which is exactly
what allows entry-by-entry streaming — each entry's compressed bytes go out
as soon as it is added, and peak memory is O(one entry), not O(archive).

Usage (FastAPI):

    async def _entries() -> AsyncIterator[tuple[str, bytes]]:
        async for item in producer:
            yield item.filename, item.content

    return StreamingResponse(stream_zip(_entries()), media_type="application/zip")

Pair with a lazy producer (e.g. ``pdf.ops.iter_render_pages_to_image_bytes``)
for end-to-end bounded memory.
"""

from __future__ import annotations

import io
import zipfile
from collections.abc import AsyncIterator


class ZipChunkSink(io.RawIOBase):
    """Non-seekable write sink for ``zipfile`` that collects written chunks.

    ``seekable() == False`` is load-bearing: it switches ``zipfile`` into
    data-descriptor mode so entries can stream without rewinding.
    """

    def __init__(self) -> None:
        self._chunks: list[bytes] = []

    def writable(self) -> bool:  # pragma: no cover - trivial
        return True

    def write(self, b) -> int:  # type: ignore[override]
        data = bytes(b)
        self._chunks.append(data)
        return len(data)

    def drain(self) -> list[bytes]:
        """Return and clear everything written since the last drain."""
        out, self._chunks = self._chunks, []
        return out


async def stream_zip(
    entries: AsyncIterator[tuple[str, bytes]],
    *,
    compression: int = zipfile.ZIP_DEFLATED,
) -> AsyncIterator[bytes]:
    """Consume ``(filename, content)`` pairs and yield ZIP bytes as produced.

    The central directory is emitted after the final entry (on ZipFile
    close), so consumers get a complete, standards-valid archive.
    """
    sink = ZipChunkSink()
    with zipfile.ZipFile(sink, mode="w", compression=compression) as zf:
        async for filename, content in entries:
            zf.writestr(filename, content)
            for chunk in sink.drain():
                yield chunk
    for chunk in sink.drain():
        yield chunk


__all__ = ["ZipChunkSink", "stream_zip"]
