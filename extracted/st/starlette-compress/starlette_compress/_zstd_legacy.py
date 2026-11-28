from __future__ import annotations

from typing import cast

from zstandard import ZstdCompressor

from starlette_compress._responder import CompressionResponder
from starlette_compress._utils import (
    DEFAULT_CONTENT_TYPES,
    DEFAULT_STREAMING_CONTENT_TYPES,
)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from typing import Protocol

    from starlette.types import ASGIApp

    class _ZstdChunker(Protocol):
        def compress(self, data: bytes) -> Iterator[bytes]: ...
        def flush(self) -> Iterator[bytes]: ...
        def finish(self) -> Iterator[bytes]: ...


class _ZstdLegacyStreamEncoder:
    """Streaming encoder backed by zstandard's chunker (bounded output).

    The size pledge applies only when a known Content-Length was supplied
    (buffered streams); streaming always passes ``-1``.

    Per-message flush uses ``chunker.flush()`` with no argument. Never pass
    module-level ``zstandard.FLUSH_BLOCK`` (it equals COMPRESSOBJ_FLUSH_FINISH
    and ends the frame).
    """

    __slots__ = ('_chunker',)

    def __init__(self, chunker: _ZstdChunker) -> None:
        self._chunker = chunker

    def feed(self, data: bytes, flush: bool) -> Iterable[bytes]:
        yield from self._chunker.compress(data)
        if flush:
            yield from self._chunker.flush()

    def finish(self) -> Iterable[bytes]:
        return self._chunker.finish()


class ZstdResponder(CompressionResponder):
    __slots__ = ()

    def __init__(
        self,
        app: ASGIApp,
        minimum_size: int,
        level: int,
        content_types: frozenset[str] = DEFAULT_CONTENT_TYPES,
        streaming_content_types: frozenset[str] = DEFAULT_STREAMING_CONTENT_TYPES,
    ) -> None:
        def oneshot(body: bytes) -> bytes:
            return ZstdCompressor(level=level).compress(body)

        def create_encoder(content_length: int) -> _ZstdLegacyStreamEncoder:
            chunker = cast(
                '_ZstdChunker', ZstdCompressor(level=level).chunker(content_length)
            )
            return _ZstdLegacyStreamEncoder(chunker)

        super().__init__(
            app,
            minimum_size,
            'zstd',
            oneshot,
            create_encoder,
            content_types,
            streaming_content_types,
        )
