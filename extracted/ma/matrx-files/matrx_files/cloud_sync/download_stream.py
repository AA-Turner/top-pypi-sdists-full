"""Range-aware streaming download primitive.

Lifts the previously-inline /files/{id}/download logic from aidream into
matrx-utils so any host gets the same RFC-7233 Range handling, ETag,
Content-Disposition, and S3 chunked streaming for free.

Public API:

- :class:`StreamingResult` — the typed result a router converts to a FastAPI
  ``StreamingResponse`` (or any other web framework's equivalent).
- :func:`parse_range_header` — RFC-7233 parser. Returns ``(start, end)`` or
  the sentinel ``(-1, -1)`` for unsatisfiable ranges.
- :func:`build_content_disposition` — RFC-5987 + RFC-6266 compliant.
- :func:`sniffed_content_type` — anti-XSS coercion for inline rendering.
- :class:`DownloadStreamer` — orchestrates HEAD + Range parse + S3 streaming.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable

# Content-Type / disposition policy lives in the stdlib-only leaf module so the
# write path + re-stamp backfill share the exact same decision. Re-exported
# below (see __all__) for back-compat with existing importers.
from ..content_headers import build_content_disposition, sniffed_content_type

if TYPE_CHECKING:
    from .sync_engine import SyncEngine

logger = logging.getLogger(__name__)


_RANGE_CHUNK_BYTES = 256 * 1024  # 256 KiB


def parse_range_header(header: str | None, total_size: int) -> tuple[int, int] | None:
    """Parse ``Range: bytes=<start>-<end>`` per RFC-7233.

    Returns ``(start, end)`` inclusive byte offsets, or ``None`` when the
    header is absent / malformed (caller serves the whole object). For
    unsatisfiable ranges (start beyond ``total_size``), returns the
    sentinel ``(-1, -1)`` so the caller can emit 416 Range Not Satisfiable.
    """
    if not header or total_size <= 0:
        return None
    if not header.strip().lower().startswith("bytes="):
        return None
    spec = header.strip()[6:]
    spec = spec.split(",", 1)[0].strip()
    if "-" not in spec:
        return None
    start_s, end_s = spec.split("-", 1)
    start_s, end_s = start_s.strip(), end_s.strip()
    last = total_size - 1
    try:
        if not start_s:
            n = int(end_s)
            if n <= 0:
                return None
            start = max(0, total_size - n)
            end = last
        else:
            start = int(start_s)
            end = int(end_s) if end_s else last
    except ValueError:
        return None
    if start > last:
        return (-1, -1)
    if end > last:
        end = last
    if end < start:
        return None
    return (start, end)


@dataclass
class StreamingResult:
    """Typed download response. Host wraps with the framework's streaming type."""
    iterator: Any                                # sync or async iterator yielding bytes
    media_type: str
    headers: dict[str, str]
    status_code: int                             # 200 | 206
    content_length: int
    storage_etag: str | None = None             # actual object revision, not file checksum


class _BodyChunks:
    """Own the opened body even before iteration begins."""

    def __init__(self, body: Any):
        self._body = body
        self._chunks = iter(body.iter_chunks(chunk_size=_RANGE_CHUNK_BYTES))
        self._closed = False

    def __iter__(self):
        return self

    def __next__(self) -> bytes:
        if self._closed:
            raise StopIteration
        try:
            while True:
                chunk = next(self._chunks)
                if chunk:
                    return chunk
        except BaseException:
            self.close()
            raise

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            try:
                self._body.close()
            except Exception:
                pass


class StorageRevisionChanged(RuntimeError):
    """The verified stored object changed; never retry against its new revision."""


class BoundedStreamingUnavailable(RuntimeError):
    """The selected object cannot be read without whole-file buffering."""


class DownloadStreamer:
    """Reads a cld_files row's bytes with Range support.

    Selects between S3 chunked streaming (current or pinned version) and
    buffered fallback (other backends).
    Public CDN redirection is the caller's responsibility — the streamer
    operates on bytes only.
    """

    def __init__(self, engine: "SyncEngine") -> None:
        self._engine = engine

    async def open_stream(
        self,
        record: dict,
        *,
        range_header: str | None = None,
        version: int | None = None,
        allow_inline: bool = False,
        require_bounded: bool = False,
        expected_storage_etag: str | None = None,
    ) -> StreamingResult:
        """Open a streaming download for the given file record.

        - ``range_header``: RFC-7233 Range header value (None → full content).
        - ``version``: pin storage URI, size and checksum to a saved version.
        - ``allow_inline``: allow inline disposition for image/video/audio/PDF.
        - ``require_bounded``: refuse non-streaming storage before reading bytes.
        """
        if expected_storage_etag is not None and (
            not isinstance(expected_storage_etag, str)
            or re.fullmatch(r'"[\x21\x23-\x7e]{1,254}"', expected_storage_etag) is None
        ):
            raise ValueError("Invalid storage revision tag.")

        if version is not None:
            if type(version) is not int or version <= 0:
                raise ValueError("Version must be a positive integer.")
            saved = await self._engine.versions.get_version_async(record["id"], version)
            if saved is None:
                raise FileNotFoundError(f"Version {version} not found for file {record['id']!r}")
            uri = saved["storage_uri"]
            record = {**record, "canonical_storage_uri": None, "storage_uri": uri,
                      "size_bytes": saved.get("size_bytes"), "checksum": saved.get("checksum"),
                      "file_name": uri.rsplit("/", 1)[-1], "mime_type": None}

        media_type, force_attachment = sniffed_content_type(
            record, allow_inline=allow_inline,
        )
        base_headers: dict[str, str] = {
            "Accept-Ranges": "bytes",
            "Content-Disposition": build_content_disposition(
                record.get("file_name") or "file",
                force_attachment=force_attachment,
            ),
            "ETag": f'"{record.get("checksum") or ""}"',
        }

        storage_uri = (
            record.get("canonical_storage_uri")
            or record.get("storage_uri")
            or ""
        )
        router = self._engine.router
        s3_backend = router.s3 if storage_uri.startswith("s3://") and router.is_configured("s3") else None

        # Refuse before fallback allocates a whole file for bounded consumers.
        if s3_backend is None or not hasattr(s3_backend, "_get_client"):
            if require_bounded or expected_storage_etag is not None:
                raise BoundedStreamingUnavailable("Selected storage does not support bounded streaming.")
            content = await router.read_async(storage_uri)
            total_size = len(content)
            parsed = parse_range_header(range_header, total_size)
            if parsed == (-1, -1):
                return StreamingResult(iterator=_single_chunk_iter(b""), media_type=media_type,
                    headers={**base_headers, "Content-Range": f"bytes */{total_size}"},
                    status_code=416, content_length=0)
            headers = dict(base_headers)
            status_code = 200
            if parsed is not None:
                start, end = parsed
                content = content[start:end + 1]
                headers["Content-Range"] = f"bytes {start}-{end}/{total_size}"
                status_code = 206
            headers["Content-Length"] = str(len(content))
            return StreamingResult(
                iterator=_single_chunk_iter(content),
                media_type=media_type,
                headers=headers,
                status_code=status_code,
                content_length=len(content),
            )

        # S3 path: resolve bucket/key, HEAD for size if the row didn't carry one.
        uri_path = storage_uri.split("://", 1)[1]
        bucket, key = s3_backend._parse_path(uri_path)
        client = s3_backend._get_client()

        total_size = int(record.get("size_bytes") or 0)
        if total_size <= 0:
            head = client.head_object(Bucket=bucket, Key=key)
            total_size = int(head.get("ContentLength") or 0)

        parsed = parse_range_header(range_header, total_size)
        # Unsatisfiable — caller emits 416 with this Content-Range header.
        if parsed == (-1, -1):
            return StreamingResult(
                iterator=_single_chunk_iter(b""),
                media_type=media_type,
                headers={**base_headers, "Content-Range": f"bytes */{total_size}"},
                status_code=416,
                content_length=0,
            )

        get_kw: dict[str, Any] = {"Bucket": bucket, "Key": key}
        is_range = parsed is not None
        if is_range:
            start, end = parsed  # type: ignore[misc]
            get_kw["Range"] = f"bytes={start}-{end}"

        if expected_storage_etag is not None:
            get_kw["IfMatch"] = expected_storage_etag
        try:
            s3_resp = client.get_object(**get_kw)
        except Exception as exc:
            response = getattr(exc, "response", None)
            if expected_storage_etag is not None and isinstance(response, dict) and (
                response.get("Error", {}).get("Code") == "PreconditionFailed"
                or response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 412
            ):
                raise StorageRevisionChanged("Stored object revision changed.") from None
            raise
        body = s3_resp.get("Body")
        if body is None:
            raise RuntimeError("S3 returned no body")

        storage_etag = s3_resp.get("ETag")
        if not isinstance(storage_etag, str) or re.fullmatch(r'"[\x21\x23-\x7e]{1,254}"', storage_etag) is None:
            storage_etag = None
        if expected_storage_etag is not None and storage_etag != expected_storage_etag:
            _BodyChunks(body).close()
            raise StorageRevisionChanged("Stored object revision changed.")

        if is_range:
            start, end = parsed  # type: ignore[misc]
            content_length = end - start + 1
            headers = {
                **base_headers,
                "Content-Range": f"bytes {start}-{end}/{total_size}",
                "Content-Length": str(content_length),
            }
            status_code = 206
        else:
            content_length = total_size
            headers = {**base_headers, "Content-Length": str(total_size)}
            status_code = 200

        return StreamingResult(
            iterator=_BodyChunks(body),
            storage_etag=storage_etag,
            media_type=media_type,
            headers=headers,
            status_code=status_code,
            content_length=content_length,
        )


def _single_chunk_iter(content: bytes):
    """One-shot iterator for buffered fallback paths."""
    def _gen():
        if content:
            yield content
    return _gen()


__all__ = [
    "StreamingResult",
    "DownloadStreamer",
    "parse_range_header",
    "build_content_disposition",
    "sniffed_content_type",
]
