"""Direct-to-storage upload behind client.files.upload(), installed by client.py.

The generated files.upload() sends the whole file in one multipart request, which
the platform edge rejects above 4.5 MB. The clients here keep the same call and
return value but run the signed URL flow instead: create an upload URL, PUT the
bytes straight to storage, then confirm the upload. Files up to 500 MB upload
this way.

    client.files.upload(
        file=("results.csv", open("results.csv", "rb"), "text/csv"),
        job_execution_id=os.environ["LABRIC_JOB_EXECUTION_ID"],
    )

`file` takes what the generated method takes: bytes, a readable, or a tuple of
(filename, content) or (filename, content, content_type). The platform records
the filename, so one is required unless the readable carries a `.name`. A missing
content type is guessed from the filename and falls back to application/octet-stream.

Pass job_execution_id (or set the LABRIC_JOB_EXECUTION_ID environment variable) to
record the file as an artifact of that job execution, or instrument_id for data
captured by an instrument the Sync app cannot reach.
"""

from __future__ import annotations

import asyncio
import mimetypes
import os
from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING, Any

import httpx

from .files.client import AsyncFilesClient, FilesClient

if TYPE_CHECKING:
    from .core.file import File
    from .core.request_options import RequestOptions
    from .types.file_upload_schema import FileUploadSchema

DEFAULT_CONTENT_TYPE = "application/octet-stream"
STREAM_CHUNK_BYTES = 1 << 20
# Bounds each read or write on the PUT to storage, not the whole transfer.
UPLOAD_TIMEOUT_SECONDS = 300


class SignedUrlFilesClient(FilesClient):
    """The generated files client with upload() routed through a signed URL."""

    def upload(
        self,
        *,
        file: File,
        job_execution_id: str | None = None,
        instrument_id: str | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileUploadSchema:
        """Upload a file of any size up to 500 MB and return its record.

        Runs create_upload_url, a PUT of the bytes to the returned URL, and
        confirm_upload, so the file only becomes visible once its bytes are stored.
        """
        file_name, content, content_type = describe_file(file)
        target = self.create_upload_url(
            file_name=file_name,
            content_type=content_type,
            job_execution_id=job_execution_id or os.getenv("LABRIC_JOB_EXECUTION_ID"),
            instrument_id=instrument_id,
            request_options=request_options,
        )
        put_to_signed_url(target.upload_url, content, target.headers)
        return self.confirm_upload(
            file_id=target.file_id, request_options=request_options
        )


class AsyncSignedUrlFilesClient(AsyncFilesClient):
    """The generated async files client with upload() routed through a signed URL."""

    async def upload(
        self,
        *,
        file: File,
        job_execution_id: str | None = None,
        instrument_id: str | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileUploadSchema:
        """Upload a file of any size up to 500 MB and return its record.

        Runs create_upload_url, a PUT of the bytes to the returned URL, and
        confirm_upload, so the file only becomes visible once its bytes are stored.
        """
        file_name, content, content_type = describe_file(file)
        target = await self.create_upload_url(
            file_name=file_name,
            content_type=content_type,
            job_execution_id=job_execution_id or os.getenv("LABRIC_JOB_EXECUTION_ID"),
            instrument_id=instrument_id,
            request_options=request_options,
        )
        await async_put_to_signed_url(target.upload_url, content, target.headers)
        return await self.confirm_upload(
            file_id=target.file_id, request_options=request_options
        )


class SignedUrlUploads:
    """Mixin that serves SignedUrlFilesClient as client.files."""

    @property
    def files(self) -> SignedUrlFilesClient:
        if self._files is None:
            self._files = SignedUrlFilesClient(client_wrapper=self._client_wrapper)
        return self._files


class AsyncSignedUrlUploads:
    """Mixin that serves AsyncSignedUrlFilesClient as client.files."""

    @property
    def files(self) -> AsyncSignedUrlFilesClient:
        if self._files is None:
            self._files = AsyncSignedUrlFilesClient(client_wrapper=self._client_wrapper)
        return self._files


def describe_file(file: File) -> tuple[str, Any, str]:
    """Split a core.File value into (filename, content, content_type)."""
    if isinstance(file, tuple):
        file_name, content, content_type = (tuple(file) + (None, None))[:3]
    else:
        file_name, content, content_type = None, file, None
    file_name = file_name or os.path.basename(getattr(content, "name", "") or "")
    if not file_name:
        raise ValueError(
            "Pass file as (filename, content) so the upload can be named on the platform"
        )
    content_type = (
        content_type or mimetypes.guess_type(file_name)[0] or DEFAULT_CONTENT_TYPE
    )
    return file_name, content, content_type


def put_to_signed_url(url: str, content: Any, headers: dict[str, str]) -> None:
    """PUT file content to a signed storage URL, streaming readables in chunks."""
    body, content_length = _put_body(content)
    with httpx.Client(timeout=UPLOAD_TIMEOUT_SECONDS) as http:
        http.put(
            url, content=body, headers=_put_headers(headers, content_length)
        ).raise_for_status()


async def async_put_to_signed_url(
    url: str, content: Any, headers: dict[str, str]
) -> None:
    """PUT file content to a signed storage URL from the async client.

    Reads run in a worker thread, so measuring and streaming a large file
    never stalls the event loop.
    """
    body, content_length = await asyncio.to_thread(_put_body, content)
    if not isinstance(body, bytes):
        body = _as_async_chunks(body)
    async with httpx.AsyncClient(timeout=UPLOAD_TIMEOUT_SECONDS) as http:
        response = await http.put(
            url, content=body, headers=_put_headers(headers, content_length)
        )
    response.raise_for_status()


def _put_headers(headers: dict[str, str], content_length: int) -> dict[str, str]:
    # The URL is signed for exactly the given headers; an explicit Content-Length
    # keeps httpx from switching a streamed body to chunked transfer encoding.
    return {**headers, "Content-Length": str(content_length)}


def _put_body(content: Any) -> tuple[bytes | Iterator[bytes], int]:
    """Return the PUT body and its length in bytes.

    Seekable readables stream in chunks, text ones encoded to UTF-8 after a
    first pass that measures them. Anything else is read into memory, since its
    byte length is only known once read.
    """
    if isinstance(content, str):
        content = content.encode("utf-8")
    if isinstance(content, (bytes, bytearray)):
        return bytes(content), len(content)
    # An empty read tells text streams ("") from binary ones (b"") whatever
    # wrapper class they use, and is the sentinel that ends chunked reading.
    end_of_stream = content.read(0)
    to_bytes = str.encode if isinstance(end_of_stream, str) else bytes
    if not _is_seekable(content):
        return _put_body(to_bytes(content.read()))

    def chunks() -> Iterator[bytes]:
        return (
            to_bytes(chunk)
            for chunk in iter(lambda: content.read(STREAM_CHUNK_BYTES), end_of_stream)
        )

    start = content.tell()
    size = sum(len(chunk) for chunk in chunks())
    content.seek(start)
    return chunks(), size


def _is_seekable(readable: Any) -> bool:
    try:
        return readable.seekable()
    except (AttributeError, OSError, ValueError):
        return False


async def _as_async_chunks(chunks: Iterator[bytes]) -> AsyncIterator[bytes]:
    while (chunk := await asyncio.to_thread(next, chunks, None)) is not None:
        yield chunk
