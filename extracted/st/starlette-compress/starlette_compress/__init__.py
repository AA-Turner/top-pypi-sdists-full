from __future__ import annotations

import sys
from operator import index

from starlette.datastructures import MutableHeaders

from starlette_compress._identity import IdentityResponder
from starlette_compress._utils import (
    DEFAULT_CONTENT_TYPES,
    DEFAULT_STREAMING_CONTENT_TYPES,
    parse_accept_encoding,
)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Iterable

    from starlette.types import ASGIApp, Receive, Scope, Send

_ZSTD_MIN_LEVEL = -131072
_ZSTD_MAX_LEVEL = 22


def _validate_nonnegative_int(name: str, value: int) -> int:
    try:
        parsed = index(value)
    except TypeError as error:
        raise TypeError(
            f'{name} must be an integer, got {type(value).__name__}'
        ) from error
    if parsed < 0:
        raise ValueError(f'{name} must be nonnegative, got {parsed}')
    return parsed


def _validate_level(name: str, value: int, minimum: int, maximum: int) -> int:
    try:
        level = index(value)
    except TypeError as error:
        raise TypeError(
            f'{name} must be an integer, got {type(value).__name__}'
        ) from error
    if not minimum <= level <= maximum:
        raise ValueError(f'{name} must be between {minimum} and {maximum}, got {level}')
    return level


def _normalize_content_types(name: str, values: Iterable[str]) -> frozenset[str]:
    if isinstance(values, (str, bytes, bytearray)):
        raise TypeError(
            f'{name} must be an iterable of media-type strings, got {type(values).__name__}'
        )
    normalized: set[str] = set()
    for item in values:
        if not isinstance(item, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f'{name} entries must be strings, got {type(item).__name__}'
            )
        media_type = item.strip().lower()
        if not media_type:
            raise ValueError(f'{name} entries must not be empty')
        normalized.add(media_type)
    return frozenset(normalized)


__version__ = '3.0.0'


class CompressMiddleware:
    __slots__ = (
        '_brotli',
        '_content_types',
        '_gzip',
        '_identity',
        '_minimum_size',
        '_remove_accept_encoding',
        '_streaming_content_types',
        '_zstd',
        'app',
    )

    def __init__(
        self,
        app: ASGIApp,
        *,
        minimum_size: int = 500,
        zstd: bool = True,
        zstd_level: int = 4,
        brotli: bool = True,
        brotli_quality: int = 4,
        gzip: bool = True,
        gzip_level: int = 4,
        remove_accept_encoding: bool = False,
        content_types: Iterable[str] | None = None,
        streaming_content_types: Iterable[str] | None = None,
    ) -> None:
        """Compression middleware supporting multiple algorithms.

        Positive Accept-Encoding qualities make methods eligible, then server
        priority selects Zstandard, Brotli, Gzip, or no compression (identity).
        Relative quality values do not reorder that priority. Missing/unsupported
        encodings fall back to identity, without a 406 response.

        Args:
            app: ASGI application to wrap.
            minimum_size: Nonnegative minimum ordinary one-shot body size in
                bytes. Multi-message responses begin compression without
                buffering to this threshold. Streaming content types (e.g.
                ``text/event-stream``) also bypass it for one-shot bodies and
                flush each non-empty continuing body message.
            zstd: Enable Zstandard compression.
            zstd_level: Zstandard compression level (-131072 through 22).
                Checked when enabled.
            brotli: Enable Brotli compression.
            brotli_quality: Brotli quality level (0-11). Checked when enabled.
            gzip: Enable Gzip compression.
            gzip_level: Gzip compression level (0-9). Checked when enabled.
            remove_accept_encoding: Remove request ``Accept-Encoding`` after reading it.
            content_types: Iterable of compressible media-type strings
                (case-insensitive). Defaults to :data:`DEFAULT_CONTENT_TYPES`.
            streaming_content_types: Iterable of media-type strings that commit
                early, bypass ``minimum_size``, and flush each continuing body
                message. Any type explicitly passed here is also included in
                ``content_types``. When omitted, defaults to
                ``DEFAULT_STREAMING_CONTENT_TYPES & content_types``.

        Raises:
            TypeError: ``minimum_size``, an enabled compression level, or a
                content-type collection/entry has an incompatible type.
            ValueError: ``minimum_size`` is negative, an enabled compression
                level is outside its valid range, or a content-type entry is
                empty.
        """
        minimum_size = _validate_nonnegative_int('minimum_size', minimum_size)
        if zstd:
            zstd_level = _validate_level(
                'zstd_level', zstd_level, _ZSTD_MIN_LEVEL, _ZSTD_MAX_LEVEL
            )
        if brotli:
            brotli_quality = _validate_level('brotli_quality', brotli_quality, 0, 11)
        if gzip:
            gzip_level = _validate_level('gzip_level', gzip_level, 0, 9)

        resolved_content_types = (
            DEFAULT_CONTENT_TYPES
            if content_types is None
            else _normalize_content_types('content_types', content_types)
        )
        if streaming_content_types is None:
            resolved_streaming_types = (
                DEFAULT_STREAMING_CONTENT_TYPES & resolved_content_types
            )
        else:
            resolved_streaming_types = _normalize_content_types(
                'streaming_content_types', streaming_content_types
            )
            resolved_content_types |= resolved_streaming_types

        self.app = app
        self._minimum_size = minimum_size
        self._content_types = resolved_content_types
        self._streaming_content_types = resolved_streaming_types
        self._identity = IdentityResponder(
            app,
            minimum_size,
            resolved_content_types,
            resolved_streaming_types,
        )
        self._remove_accept_encoding = remove_accept_encoding

        if zstd:
            if sys.version_info >= (3, 14):
                from starlette_compress._zstd import ZstdResponder
            else:
                from starlette_compress._zstd_legacy import ZstdResponder

            self._zstd = ZstdResponder(
                app,
                minimum_size,
                zstd_level,
                resolved_content_types,
                resolved_streaming_types,
            )
        else:
            self._zstd = None

        if brotli:
            from starlette_compress._brotli import BrotliResponder

            self._brotli = BrotliResponder(
                app,
                minimum_size,
                brotli_quality,
                resolved_content_types,
                resolved_streaming_types,
            )
        else:
            self._brotli = None

        if gzip:
            from starlette_compress._gzip import GZipResponder

            self._gzip = GZipResponder(
                app,
                minimum_size,
                gzip_level,
                resolved_content_types,
                resolved_streaming_types,
            )
        else:
            self._gzip = None

    @property
    def minimum_size(self) -> int:
        """Minimum one-shot body size in bytes before compressing."""
        return self._minimum_size

    @property
    def content_types(self) -> frozenset[str]:
        """Normalized lowercase media types eligible for compression."""
        return self._content_types

    @property
    def streaming_content_types(self) -> frozenset[str]:
        """Normalized lowercase media types using early-commit streaming flushes."""
        return self._streaming_content_types

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Run the ASGI application, negotiating response compression on HTTP scopes.

        Raises:
            RuntimeError: If the wrapped application sends ``http.response.start``
                more than once on an HTTP scope.
        """
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        raw_headers: Iterable[tuple[bytes, bytes]] = scope['headers']
        if not isinstance(raw_headers, list):
            raw_headers = scope['headers'] = list(raw_headers)

        accept_encoding = [
            value.decode('latin-1')
            for name, value in raw_headers
            if name == b'accept-encoding'
        ]

        if accept_encoding:
            if self._remove_accept_encoding:
                headers = MutableHeaders(scope=scope)
                del headers['Accept-Encoding']

            accept_encodings = parse_accept_encoding(
                ','.join(accept_encoding)
                if len(accept_encoding) > 1
                else accept_encoding[0]
            )
            if self._zstd is not None and 'zstd' in accept_encodings:
                return await self._zstd(scope, receive, send)
            if self._brotli is not None and 'br' in accept_encodings:
                return await self._brotli(scope, receive, send)
            if self._gzip is not None and 'gzip' in accept_encodings:
                return await self._gzip(scope, receive, send)

        return await self._identity(scope, receive, send)


__all__ = (
    'DEFAULT_CONTENT_TYPES',
    'DEFAULT_STREAMING_CONTENT_TYPES',
    'CompressMiddleware',
)
