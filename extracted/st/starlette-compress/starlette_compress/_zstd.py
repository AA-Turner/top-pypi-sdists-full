from __future__ import annotations

from typing import cast

# This backend is imported only on Python 3.14+, beyond the checker's 3.11 target.
from compression.zstd import (  # pyright: ignore[reportMissingImports, reportMissingTypeStubs]
    ZstdCompressor,  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType]
)
from compression.zstd import (  # pyright: ignore[reportMissingImports, reportMissingTypeStubs]
    compress as zstd_compress,  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType]
)

from starlette_compress._responder import CompressionResponder
from starlette_compress._utils import (
    DEFAULT_CONTENT_TYPES,
    DEFAULT_STREAMING_CONTENT_TYPES,
)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Protocol

    from starlette.types import ASGIApp

    class _ZstdCompressor(Protocol):
        def compress(self, data: bytes, mode: int) -> bytes: ...
        def flush(self, mode: int) -> bytes: ...


class _ZstdStreamEncoder:
    __slots__ = ('_compressor',)

    def __init__(self, level: int) -> None:
        self._compressor: _ZstdCompressor = cast(
            '_ZstdCompressor',
            ZstdCompressor(level),  # pyright: ignore[reportUnknownMemberType]
        )

    def feed(self, data: bytes, flush: bool) -> Iterable[bytes]:
        mode = cast(
            'int',
            ZstdCompressor.FLUSH_BLOCK if flush else ZstdCompressor.CONTINUE,  # pyright: ignore[reportUnknownMemberType]
        )
        out = self._compressor.compress(data, mode)
        return (out,) if out else ()

    def finish(self) -> Iterable[bytes]:
        mode = cast('int', ZstdCompressor.FLUSH_FRAME)  # pyright: ignore[reportUnknownMemberType]
        out = self._compressor.flush(mode)
        return (out,) if out else ()


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
            return cast('bytes', zstd_compress(body, level=level))

        def create_encoder(content_length: int) -> _ZstdStreamEncoder:
            return _ZstdStreamEncoder(level)

        super().__init__(
            app,
            minimum_size,
            'zstd',
            oneshot,
            create_encoder,
            content_types,
            streaming_content_types,
        )
