import logging
import codecs
import httpx
from typing import Dict, Optional, Tuple
from urllib.parse import quote

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


DEFAULT_TIMEOUT = 120


def _attachment_url(client: Client, os_workspace: str, os_entity_uid: str) -> str:
    """Build the attachment endpoint URL."""
    base = client.get_base_url_v1()
    return f"{base}/api/v2/entities/{quote(os_workspace, safe='')}/{quote(os_entity_uid, safe='')}/attachment"


def _build_headers(
    client: Client,
    byte_range: Optional[Tuple[int, Optional[int]]] = None,
) -> dict:
    """Build request headers including auth and optional Range."""
    headers = dict(client.get_headers())
    if byte_range is not None:
        start, end = byte_range
        if end is not None:
            headers["Range"] = f"bytes={start}-{end}"
        else:
            headers["Range"] = f"bytes={start}-"
    return headers


def _head_sync(url: str, headers: dict, client: Client) -> Dict[str, str]:
    """Send a HEAD request and return the response headers as a dict."""
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = http_client.head(url, headers=headers)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("read_attachment", response, client)
    return dict(response.headers)


async def _head_async(url: str, headers: dict, client: Client) -> Dict[str, str]:
    """Send a HEAD request and return the response headers as a dict (async)."""
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = await http_client.head(url, headers=headers)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("read_attachment", response, client)
    return dict(response.headers)


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
    os_workspace: str,
    os_entity_uid: str,
    decode: bool = True,
    stream: bool = False,
    stream_lines: bool = False,
    stream_chunk_size: int = 65_536,
    byte_range: Optional[Tuple[int, Optional[int]]] = None,
    headers_only: bool = False,
    client: Client = None,
):
    """
    # Read the content of an attachment from its workspace ID and object ID

    Note that querying the ontology for the same entry will only provide metadata
    information about the entity, not the attachment contents themselves.

    ## Arguments
    - `os_workspace`: The workspace ID the object belongs to
    - `os_entity_uid`: The object ID
    - `decode`: Whether to decode the contents to UTF-8
    - `stream`: Whether to return the contents in chunks. Overrides stream_lines and stream_chunk_size if False
    - `stream_lines`: Whether to chunk the contents per line. Overrides stream_chunk_size if set
    - `stream_chunk_size`: How many bytes each chunk should be
    - `byte_range`: Optional (start, end) tuple for Range requests. end can be None for open-ended ranges.
        Example: (0, 1023) fetches the first 1024 bytes; (1024, None) fetches from byte 1024 onwards.
    - `headers_only`: If True, send a HEAD request and return the response headers as a dict
        instead of downloading the body.  Useful for inspecting content-type, content-length,
        etag, or last-modified without fetching the full attachment.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    - When `headers_only=True`: a ``dict[str, str]`` of response headers.
    - Otherwise: a string or bytes representation of the object file contents.

    ## Raises
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    - `ValueError`: If the object has no associated file
    """
    if not client:
        client = get_default_client()

    url = _attachment_url(client, os_workspace, os_entity_uid)
    headers = _build_headers(client, byte_range)

    if headers_only:
        return _head_sync(url, headers, client)

    if not stream:
        response = None
        try:
            for attempt in network_retry_strategy():
                with attempt:
                    with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
                        response = http_client.get(url, headers=headers)
                        response.raise_for_status()
        except Exception:
            raise ApiConnectionError("read_attachment", response, client)
        attachment = response.content
        if decode:
            attachment = attachment.decode()
        return attachment

    # Streaming mode — return a generator that keeps the connection alive
    def _stream_chunks():
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
            with http_client.stream("GET", url, headers=headers) as response:
                if response.status_code >= 400:
                    raise ApiConnectionError("read_attachment", response, client)
                for chunk in response.iter_bytes(chunk_size=stream_chunk_size):
                    yield chunk

    if stream_lines:
        result = _iter_lines(_stream_chunks())
    else:
        result = _stream_chunks()

    if decode:
        result = _decode_iter(result)
    return result


async def asyncio(
    os_workspace: str,
    os_entity_uid: str,
    decode: bool = True,
    stream: bool = False,
    stream_lines: bool = False,
    stream_chunk_size: int = 65_536,
    byte_range: Optional[Tuple[int, Optional[int]]] = None,
    headers_only: bool = False,
    client: Client = None,
):
    """
    # Read the content of an attachment from its workspace ID and object ID (async)

    Note that querying the ontology for the same entry will only provide metadata
    information about the entity, not the attachment contents themselves.

    ## Arguments
    - `os_workspace`: The workspace ID the object belongs to
    - `os_entity_uid`: The object ID
    - `decode`: Whether to decode the contents to UTF-8
    - `stream`: Whether to return the contents in chunks. Overrides stream_lines and stream_chunk_size if False
    - `stream_lines`: Whether to chunk the contents per line. Overrides stream_chunk_size if set
    - `stream_chunk_size`: How many bytes each chunk should be
    - `byte_range`: Optional (start, end) tuple for Range requests. end can be None for open-ended ranges.
        Example: (0, 1023) fetches the first 1024 bytes; (1024, None) fetches from byte 1024 onwards.
    - `headers_only`: If True, send a HEAD request and return the response headers as a dict
        instead of downloading the body.  Useful for inspecting content-type, content-length,
        etag, or last-modified without fetching the full attachment.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    - When `headers_only=True`: a ``dict[str, str]`` of response headers.
    - Otherwise: a string or bytes representation of the object file contents,
      or an async generator when streaming.

    ## Raises
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    - `ValueError`: If the object has no associated file
    """
    if not client:
        client = get_default_client()

    url = _attachment_url(client, os_workspace, os_entity_uid)
    headers = _build_headers(client, byte_range)

    if headers_only:
        return await _head_async(url, headers, client)

    if not stream:
        response = None
        try:
            for attempt in network_retry_strategy():
                with attempt:
                    async with httpx.AsyncClient(
                        timeout=DEFAULT_TIMEOUT
                    ) as http_client:
                        response = await http_client.get(url, headers=headers)
                        response.raise_for_status()
        except Exception:
            raise ApiConnectionError("read_attachment", response, client)
        attachment = response.content
        if decode:
            attachment = attachment.decode()
        return attachment

    # Streaming mode — return an async generator
    async def _stream_chunks():
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http_client:
            async with http_client.stream("GET", url, headers=headers) as response:
                if response.status_code >= 400:
                    raise ApiConnectionError("read_attachment", response, client)
                async for chunk in response.aiter_bytes(chunk_size=stream_chunk_size):
                    yield chunk

    if stream_lines:
        result = _iter_lines_async(_stream_chunks())
    else:
        result = _stream_chunks()

    if decode:
        result = _decode_iter_async(result)
    return result
