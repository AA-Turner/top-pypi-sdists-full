from __future__ import annotations

from typing import cast

import brotli  # pyright: ignore[reportMissingTypeStubs]

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

    class _BrotliCompressor(Protocol):
        def process(self, data: bytes) -> bytes: ...
        def flush(self) -> bytes: ...
        def finish(self) -> bytes: ...


class _BrotliStreamEncoder:
    __slots__ = ('_compressor',)

    def __init__(self, quality: int) -> None:
        self._compressor: _BrotliCompressor = cast(
            '_BrotliCompressor',
            brotli.Compressor(quality=quality),  # pyright: ignore[reportUnknownMemberType]
        )

    def feed(self, data: bytes, flush: bool) -> Iterable[bytes]:
        out = self._compressor.process(data)
        if flush:
            out += self._compressor.flush()
        return (out,) if out else ()

    def finish(self) -> Iterable[bytes]:
        out = self._compressor.finish()
        return (out,) if out else ()


class BrotliResponder(CompressionResponder):
    __slots__ = ()

    def __init__(
        self,
        app: ASGIApp,
        minimum_size: int,
        quality: int,
        content_types: frozenset[str] = DEFAULT_CONTENT_TYPES,
        streaming_content_types: frozenset[str] = DEFAULT_STREAMING_CONTENT_TYPES,
    ) -> None:
        def oneshot(body: bytes) -> bytes:
            return cast(
                'bytes',
                brotli.compress(body, quality=quality),  # pyright: ignore[reportUnknownMemberType]
            )

        def create_encoder(content_length: int) -> _BrotliStreamEncoder:
            return _BrotliStreamEncoder(quality)

        super().__init__(
            app,
            minimum_size,
            'br',
            oneshot,
            create_encoder,
            content_types,
            streaming_content_types,
        )
