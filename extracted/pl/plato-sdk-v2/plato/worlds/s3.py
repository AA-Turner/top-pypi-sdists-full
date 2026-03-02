"""Shared S3 upload/download helpers via Chronos presigned URLs.

All transfers are streamed to avoid loading entire payloads into memory.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Chunk size for streaming reads/writes (256 KB)
_CHUNK_SIZE = 256 * 1024


async def upload_to_s3(
    chronos_url: str,
    session_id: str,
    endpoint: str,
    data: bytes | str | Path,
    content_type: str,
    timeout: int = 30,
) -> bool:
    """Upload data to S3 via a Chronos presigned PUT URL.

    Args:
        chronos_url: Chronos base URL (e.g. ``https://host``).
        session_id: Session ID for the presigned URL request.
        endpoint: URL path component (e.g. ``state``, ``workspace``).
        data: Bytes to upload, or a ``Path`` to stream from disk.
        content_type: Content-Type header value.
        timeout: HTTP timeout in seconds.
    """
    if not chronos_url or not session_id:
        logger.warning(f"Cannot upload {endpoint}: missing chronos_url or session_id")
        return False

    api_key = os.environ.get("PLATO_API_KEY", "")

    try:
        import httpx

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(
                f"{chronos_url}/api/sessions/{session_id}/{endpoint}-upload-url",
                headers={"X-API-Key": api_key},
            )
            if resp.status_code != 200:
                logger.warning(f"Failed to get {endpoint} upload URL: {resp.status_code}")
                return False

            put_url = resp.json()["url"]

            if isinstance(data, Path):
                file_size = data.stat().st_size
                headers = {"Content-Type": content_type, "Content-Length": str(file_size)}

                async def _file_stream():
                    with open(data, "rb") as f:
                        while True:
                            chunk = f.read(_CHUNK_SIZE)
                            if not chunk:
                                break
                            yield chunk

                put_resp = await client.put(
                    put_url,
                    content=_file_stream(),
                    headers=headers,
                    timeout=max(timeout, 300),
                )
            else:
                if isinstance(data, str):
                    data = data.encode()
                put_resp = await client.put(
                    put_url,
                    content=data,
                    headers={"Content-Type": content_type},
                    timeout=max(timeout, 300),
                )

            size = data.stat().st_size if isinstance(data, Path) else len(data)
            if put_resp.status_code in (200, 201, 204):
                logger.info(f"Uploaded {endpoint} ({size} bytes)")
                return True
            else:
                logger.warning(f"{endpoint} upload failed: {put_resp.status_code}")
                return False

    except Exception as e:
        logger.warning(f"Failed to upload {endpoint}: {e}")
        return False


async def download_to_file(
    chronos_url: str,
    session_id: str,
    endpoint: str,
    dest: Path,
    timeout: int = 30,
) -> bool:
    """Download from S3 via presigned URL, streaming directly to a file.

    Args:
        chronos_url: Chronos base URL.
        session_id: Session ID for the presigned URL request.
        endpoint: URL path component (e.g. ``state``, ``workspace``).
        dest: Destination file path.
        timeout: HTTP timeout in seconds.

    Returns:
        True on success, False on failure.
    """
    if not chronos_url:
        logger.warning(f"Cannot download {endpoint}: no chronos_url")
        return False

    api_key = os.environ.get("PLATO_API_KEY", "")

    try:
        import httpx

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(
                f"{chronos_url}/api/sessions/{session_id}/{endpoint}-download-url",
                headers={"X-API-Key": api_key},
            )
            if resp.status_code != 200:
                logger.warning(f"No {endpoint} available for session {session_id}: {resp.status_code}")
                return False

            get_url = resp.json()["url"]

            total = 0
            async with client.stream("GET", get_url, timeout=max(timeout, 300)) as stream:
                if stream.status_code != 200:
                    logger.warning(f"{endpoint} download failed: {stream.status_code}")
                    return False
                dest.parent.mkdir(parents=True, exist_ok=True)
                with open(dest, "wb") as f:
                    async for chunk in stream.aiter_bytes(chunk_size=_CHUNK_SIZE):
                        f.write(chunk)
                        total += len(chunk)

            logger.info(f"Downloaded {endpoint} ({total} bytes) to {dest}")
            return True

    except Exception as e:
        logger.warning(f"Failed to download {endpoint}: {e}")
        return False


async def download_from_s3(
    chronos_url: str,
    session_id: str,
    endpoint: str,
    timeout: int = 30,
) -> bytes | None:
    """Download data from S3 via a Chronos presigned GET URL.

    Note: This loads the entire response into memory. Prefer
    :func:`download_to_file` for large payloads.
    """
    if not chronos_url:
        logger.warning(f"Cannot download {endpoint}: no chronos_url")
        return None

    api_key = os.environ.get("PLATO_API_KEY", "")

    try:
        import httpx

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(
                f"{chronos_url}/api/sessions/{session_id}/{endpoint}-download-url",
                headers={"X-API-Key": api_key},
            )
            if resp.status_code != 200:
                logger.warning(f"No {endpoint} available for session {session_id}: {resp.status_code}")
                return None

            get_url = resp.json()["url"]
            data_resp = await client.get(get_url, timeout=max(timeout, 300))
            if data_resp.status_code != 200:
                logger.warning(f"{endpoint} download failed: {data_resp.status_code}")
                return None

            return data_resp.content

    except Exception as e:
        logger.warning(f"Failed to download {endpoint}: {e}")
        return None
