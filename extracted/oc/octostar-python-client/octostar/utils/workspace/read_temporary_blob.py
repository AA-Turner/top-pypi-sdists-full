import logging
import codecs
import os
import httpx
from typing import Dict, Optional, Tuple
from urllib import parse as urllib_parse

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


DEFAULT_TIMEOUT = 120


def _is_dev_mode() -> bool:
    return f"{os.getenv('OS_DEV_MODE')}".lower() == "true"


def _blob_api_url(client: Client, filename: str) -> str:
    """Build the blob download API endpoint URL."""
    base = client.get_base_url_v1()
    return f"{base}/api/v1/files/download-blob/{filename}"


def _resolve_url(client: Client, path: str, use_external: bool) -> str:
    """Resolve a presigned URL, joining with base URL in external/dev mode."""
    if use_external:
        return urllib_parse.urljoin(client.get_base_url_v1(), path)
    return path


def _head_sync(url: str, headers: dict, client: Client) -> Dict[str, str]:
    """Send a HEAD request to the blob API proxy and return the response headers."""
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = http_client.head(url, headers=headers)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("read_temporary_blob", response, client)
    return dict(response.headers)


async def _head_async(url: str, headers: dict, client: Client) -> Dict[str, str]:
    """Send a HEAD request to the blob API proxy and return the response headers (async)."""
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = await http_client.head(url, headers=headers)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("read_temporary_blob", response, client)
    return dict(response.headers)


def _get_download_url_sync(
    api_url: str, headers: dict, filename: str, client: Client
) -> str:
    """Fetch the presigned download URL from the API."""
    use_external = _is_dev_mode()
    params = {"external_url": use_external}
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = http_client.get(api_url, headers=headers, params=params)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("read_temporary_blob", response, client)
    result = response.json()
    url = result.get("url")
    if not url:
        raise ValueError(
            f"read_temporary_blob: no download url returned for {filename}"
        )
    return _resolve_url(client, url, use_external)


async def _get_download_url_async(
    api_url: str, headers: dict, filename: str, client: Client
) -> str:
    """Fetch the presigned download URL from the API (async)."""
    use_external = _is_dev_mode()
    params = {"external_url": use_external}
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = await http_client.get(
                        api_url, headers=headers, params=params
                    )
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("read_temporary_blob", response, client)
    result = response.json()
    url = result.get("url")
    if not url:
        raise ValueError(
            f"read_temporary_blob: no download url returned for {filename}"
        )
    return _resolve_url(client, url, use_external)


def _decode_iter(chunks, encoding="utf-8", errors="strict"):
    decoder = codecs.getincrementaldecoder(encoding)(errors=errors)
    for chunk in chunks:
        text = decoder.decode(chunk)
        if text or not chunk:
            yield text
    tail = decoder.decode(b"", final=True)
    if tail:
        yield tail


async def _decode_iter_async(chunks, encoding="utf-8", errors="strict"):
    decoder = codecs.getincrementaldecoder(encoding)(errors=errors)
    async for chunk in chunks:
        text = decoder.decode(chunk)
        if text or not chunk:
            yield text
    tail = decoder.decode(b"", final=True)
    if tail:
        yield tail


def _iter_lines(chunks_iter):
    pending = b""
    for chunk in chunks_iter:
        data = pending + chunk
        pending = b""
        lines = data.splitlines(keepends=True)
        if not lines:
            continue
        if not lines[-1].endswith(b"\n"):
            pending = lines.pop()
        for line in lines:
            yield line.rstrip(b"\r\n")
    if pending:
        yield pending.rstrip(b"\r\n")


async def _iter_lines_async(chunks_iter):
    pending = b""
    async for chunk in chunks_iter:
        data = pending + chunk
        pending = b""
        lines = data.splitlines(keepends=True)
        if not lines:
            continue
        if not lines[-1].endswith(b"\n"):
            pending = lines.pop()
        for line in lines:
            yield line.rstrip(b"\r\n")
    if pending:
        yield pending.rstrip(b"\r\n")


def sync(
    filename: str,
    decode: bool = True,
    stream: bool = False,
    stream_lines: bool = False,
    stream_chunk_size: int = 65_536,
    byte_range: Optional[Tuple[int, Optional[int]]] = None,
    headers_only: bool = False,
    client: Client = None,
):
    """
    # Read a temporary blob from the user's temp bucket

    Downloads a file from the authenticated user's temporary S3 bucket.
    This is useful for retrieving temporary files that were uploaded for
    processing or export operations.

    ## Arguments
    - `filename`: The name of the file in the temp bucket
    - `decode`: Whether to decode the contents to UTF-8 (default: True). If False, returns raw bytes
    - `stream`: Whether to return the contents in chunks
    - `stream_lines`: Whether to chunk the contents per line
    - `stream_chunk_size`: How many bytes each chunk should be
    - `byte_range`: Optional (start, end) tuple for Range requests. end can be None for open-ended ranges.
        Example: (0, 1023) fetches the first 1024 bytes; (1024, None) fetches from byte 1024 onwards.
    - `headers_only`: If True, send a HEAD request and return the response headers as a dict
        instead of downloading the body. Useful for inspecting content-type, content-length,
        etag, or last-modified without fetching the full blob.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    - When `headers_only=True`: a ``dict[str, str]`` of response headers.
    - Otherwise: a string (if decode=True) or bytes (if decode=False) of the file contents,
      or a generator when streaming.

    ## Raises
    - `ApiConnectionError`: If requesting the presigned download URL or HEAD request failed
    - `ConnectionError`: If the download from S3 failed
    """
    if not client:
        client = get_default_client()

    api_url = _blob_api_url(client, filename)
    auth_headers = dict(client.get_headers())

    if headers_only:
        return _head_sync(api_url, auth_headers, client)

    download_url = _get_download_url_sync(api_url, auth_headers, filename, client)

    s3_headers = {}
    if byte_range is not None:
        start, end = byte_range
        if end is not None:
            s3_headers["Range"] = f"bytes={start}-{end}"
        else:
            s3_headers["Range"] = f"bytes={start}-"

    if not stream:
        response = None
        try:
            for attempt in network_retry_strategy():
                with attempt:
                    with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
                        response = http_client.get(download_url, headers=s3_headers)
                        response.raise_for_status()
        except Exception:
            raise ConnectionError(
                f"read_temporary_blob: download failed for {filename}"
                + (f" — {response.status_code}: {response.text}" if response else "")
            )
        content = response.content
        if decode:
            content = content.decode()
        return content

    def _read_chunk(url, start, increment, http_client):
        headers = {"Range": f"bytes={start}-{start + increment - 1}"}
        response = http_client.get(url, headers=headers)
        if response.status_code == 206:
            return response.content, start + increment, False
        elif response.status_code == 416:
            return None, start, False
        elif response.status_code == 403:
            return None, start, True
        else:
            raise ConnectionError(
                f"read_temporary_blob: download failed for {filename} — {response.status_code}: {response.text}"
            )

    def _chunk_generator():
        start = byte_range[0] if byte_range is not None else 0
        end = byte_range[1] if byte_range is not None else None
        url = download_url
        http_client = httpx.Client(timeout=DEFAULT_TIMEOUT)
        try:
            while True:
                if end is not None:
                    remaining = end - start + 1
                    if remaining <= 0:
                        break
                    increment = min(stream_chunk_size, remaining)
                else:
                    increment = stream_chunk_size
                chunk, start, url_expired = _read_chunk(
                    url, start, increment, http_client
                )
                if url_expired:
                    _logger.info(
                        f"Presigned URL expired at byte {start}, refreshing..."
                    )
                    url = _get_download_url_sync(
                        api_url, auth_headers, filename, client
                    )
                    continue
                if chunk is None:
                    break
                yield chunk
        finally:
            http_client.close()

    if stream_lines:
        result = _iter_lines(_chunk_generator())
    else:
        result = _chunk_generator()

    if decode:
        result = _decode_iter(result)
    return result


async def asyncio(
    filename: str,
    decode: bool = True,
    stream: bool = False,
    stream_lines: bool = False,
    stream_chunk_size: int = 65_536,
    byte_range: Optional[Tuple[int, Optional[int]]] = None,
    headers_only: bool = False,
    client: Client = None,
):
    """
    # Read a temporary blob from the user's temp bucket (async)

    Downloads a file from the authenticated user's temporary S3 bucket.
    This is useful for retrieving temporary files that were uploaded for
    processing or export operations.

    ## Arguments
    - `filename`: The name of the file in the temp bucket
    - `decode`: Whether to decode the contents to UTF-8 (default: True). If False, returns raw bytes
    - `stream`: Whether to return the contents in chunks
    - `stream_lines`: Whether to chunk the contents per line
    - `stream_chunk_size`: How many bytes each chunk should be
    - `byte_range`: Optional (start, end) tuple for Range requests. end can be None for open-ended ranges.
        Example: (0, 1023) fetches the first 1024 bytes; (1024, None) fetches from byte 1024 onwards.
    - `headers_only`: If True, send a HEAD request and return the response headers as a dict
        instead of downloading the body.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    - When `headers_only=True`: a ``dict[str, str]`` of response headers.
    - Otherwise: a string (if decode=True) or bytes (if decode=False) of the file contents,
      or an async generator when streaming.

    ## Raises
    - `ApiConnectionError`: If requesting the presigned download URL or HEAD request failed
    - `ConnectionError`: If the download from S3 failed
    """
    if not client:
        client = get_default_client()

    api_url = _blob_api_url(client, filename)
    auth_headers = dict(client.get_headers())

    if headers_only:
        return await _head_async(api_url, auth_headers, client)

    download_url = await _get_download_url_async(
        api_url, auth_headers, filename, client
    )

    s3_headers = {}
    if byte_range is not None:
        start, end = byte_range
        if end is not None:
            s3_headers["Range"] = f"bytes={start}-{end}"
        else:
            s3_headers["Range"] = f"bytes={start}-"

    if not stream:
        response = None
        try:
            for attempt in network_retry_strategy():
                with attempt:
                    async with httpx.AsyncClient(
                        timeout=DEFAULT_TIMEOUT
                    ) as http_client:
                        response = await http_client.get(
                            download_url, headers=s3_headers
                        )
                        response.raise_for_status()
        except Exception:
            raise ConnectionError(
                f"read_temporary_blob: download failed for {filename}"
                + (f" — {response.status_code}: {response.text}" if response else "")
            )
        content = response.content
        if decode:
            content = content.decode()
        return content

    async def _read_chunk_async(url, start, increment, http_client):
        headers = {"Range": f"bytes={start}-{start + increment - 1}"}
        response = await http_client.get(url, headers=headers)
        if response.status_code == 206:
            return response.content, start + increment, False
        elif response.status_code == 416:
            return None, start, False
        elif response.status_code == 403:
            return None, start, True
        else:
            raise ConnectionError(
                f"read_temporary_blob: download failed for {filename} — {response.status_code}: {response.text}"
            )

    async def _chunk_generator():
        start = byte_range[0] if byte_range is not None else 0
        end = byte_range[1] if byte_range is not None else None
        url = download_url
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http_client:
            while True:
                if end is not None:
                    remaining = end - start + 1
                    if remaining <= 0:
                        break
                    increment = min(stream_chunk_size, remaining)
                else:
                    increment = stream_chunk_size
                chunk, start, url_expired = await _read_chunk_async(
                    url, start, increment, http_client
                )
                if url_expired:
                    _logger.info(
                        f"Presigned URL expired at byte {start}, refreshing..."
                    )
                    url = await _get_download_url_async(
                        api_url, auth_headers, filename, client
                    )
                    continue
                if chunk is None:
                    break
                yield chunk

    if stream_lines:
        result = _iter_lines_async(_chunk_generator())
    else:
        result = _chunk_generator()

    if decode:
        result = _decode_iter_async(result)
    return result
