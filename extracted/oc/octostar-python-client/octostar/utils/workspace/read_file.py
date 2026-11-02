import logging
from typing import Optional, Tuple

_logger = logging.getLogger(__name__)

from ...client import Client
from . import read_attachment


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
    # Read the content of a file from its workspace ID and object ID

    Downloads the attachment content via the v2 entities API endpoint,
    which handles S3 proxying, Range requests, and conditional headers.

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
      or a generator/async generator when streaming.

    ## Raises
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    - `ValueError`: If the object has no associated file
    """
    return read_attachment.sync(
        os_workspace=os_workspace,
        os_entity_uid=os_entity_uid,
        decode=decode,
        stream=stream,
        stream_lines=stream_lines,
        stream_chunk_size=stream_chunk_size,
        byte_range=byte_range,
        headers_only=headers_only,
        client=client,
    )


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
    # Read the content of a file from its workspace ID and object ID (async)

    Downloads the attachment content via the v2 entities API endpoint,
    which handles S3 proxying, Range requests, and conditional headers.

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
    return await read_attachment.asyncio(
        os_workspace=os_workspace,
        os_entity_uid=os_entity_uid,
        decode=decode,
        stream=stream,
        stream_lines=stream_lines,
        stream_chunk_size=stream_chunk_size,
        byte_range=byte_range,
        headers_only=headers_only,
        client=client,
    )
