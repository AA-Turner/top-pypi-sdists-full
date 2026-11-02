"""Cloud-agnostic multipart upload helpers (works on both GCS and S3).

Protocol summary:
  1. _calculate_multipart_ranges(file_size) -> list of (start, end) byte ranges
  2. For each range: read bytes, compute base64-MD5
  3. POST initiate with part_hashes -> {upload_id, part_urls[]}
  4. PUT each part directly to its presigned URL with Content-MD5 header
     (parallel, max 6 concurrent, 3 retries with exponential backoff)
  5. POST complete with {upload_id, parts: [{part_number, etag, checksum}]}
"""

import asyncio
import base64
import concurrent.futures
import hashlib
import logging
import math
import time
from pathlib import Path
from typing import Any
from uuid import UUID

from httpx import (
    AsyncClient,
    Client,
    ConnectError,
    HTTPStatusError,
    ReadError,
    RemoteProtocolError,
    TimeoutException,
    codes,
)
from tqdm import tqdm

from edison_client.clients.exceptions import DataStorageCreationError

logger = logging.getLogger(__name__)

# Multipart upload constants.
# Backend (crow_service.cloud.multipart_manager) supports both AWS S3 and GCS XML
# multipart, so this works on both clouds.
MIN_PART_SIZE_BYTES = 5 * 1024 * 1024  # 5MB - S3/GCS minimum (except last part)
MAX_MULTIPART_PARTS = 10_000  # S3/GCS hard limit on parts per upload
PREFERRED_PART_SIZE_SMALL = 10 * 1024 * 1024  # files < 1 GiB
PREFERRED_PART_SIZE_MEDIUM = 50 * 1024 * 1024  # files 1-10 GiB
PREFERRED_PART_SIZE_LARGE = 100 * 1024 * 1024  # files >= 10 GiB
MAX_CONCURRENT_PART_UPLOADS = 6
PART_UPLOAD_MAX_RETRIES = 3
PART_UPLOAD_RETRY_BASE_DELAY_SECONDS = 1.0  # backoff: 1s, 2s, 4s


def _calculate_multipart_ranges(file_size_bytes: int) -> list[tuple[int, int]]:
    """Compute byte ranges for multipart upload parts.

    Returns a list of (start, end) byte ranges
    with end exclusive. Always returns at least 1 range. For an empty file
    (size 0), returns [(0, 0)] which is a single empty part.

    Tier selection by file size:
      - < 1 GiB  -> 10 MiB preferred parts
      - < 10 GiB -> 50 MiB preferred parts
      - >= 10 GiB -> 100 MiB preferred parts
    """
    if file_size_bytes <= 0:
        return [(0, 0)]

    if file_size_bytes < 1024 * 1024 * 1024:
        preferred_part_size = PREFERRED_PART_SIZE_SMALL
    elif file_size_bytes < 10 * 1024 * 1024 * 1024:
        preferred_part_size = PREFERRED_PART_SIZE_MEDIUM
    else:
        preferred_part_size = PREFERRED_PART_SIZE_LARGE

    num_parts = math.ceil(file_size_bytes / preferred_part_size)

    if num_parts > MAX_MULTIPART_PARTS:
        required_part_size = math.ceil(file_size_bytes / MAX_MULTIPART_PARTS)
        num_parts = math.ceil(file_size_bytes / required_part_size)

    actual_part_size = file_size_bytes / num_parts
    if actual_part_size < MIN_PART_SIZE_BYTES < file_size_bytes:
        num_parts = math.ceil(file_size_bytes / MIN_PART_SIZE_BYTES)

    part_count = max(1, num_parts)
    part_size = math.ceil(file_size_bytes / part_count)

    ranges: list[tuple[int, int]] = []
    for i in range(part_count):
        start = i * part_size
        end = min((i + 1) * part_size, file_size_bytes)
        ranges.append((start, end))
    return ranges


def _b64_md5(data: bytes) -> str:
    """Compute base64-encoded MD5 digest of data.

    Returns the canonical AWS/RFC 1864 form (base64 of the 16-byte raw digest),
    suitable for the S3/GCS Content-MD5 header.
    """
    return base64.b64encode(hashlib.md5(data).digest()).decode("ascii")  # noqa: S324


def _read_file_range(file_path: Path, start: int, end: int) -> bytes:
    """Read bytes [start, end) from file_path. Returns b'' for empty range."""
    if end <= start:
        return b""
    with open(file_path, "rb") as f:
        f.seek(start)
        return f.read(end - start)


# Transport-level errors that justify a retry (TCP/DNS/TLS failures, dropped
# connections, read timeouts). HTTPStatusError is handled separately because we
# only want to retry transient server statuses (429, 5xx).
_PART_RETRYABLE_ERRORS = (
    ConnectError,
    TimeoutException,
    RemoteProtocolError,
    ReadError,
)


def _is_retryable_http_status(status_code: int) -> bool:
    """True for transient server-side statuses worth retrying.

    429 is included because S3/GCS use it for throttling and explicitly
    recommend exponential-backoff retry. Other 4xx propagates immediately
    -- retrying a request with a bad signature, expired URL, or wrong
    Content-MD5 won't fix it.
    """
    return (
        status_code == codes.TOO_MANY_REQUESTS
        or codes.INTERNAL_SERVER_ERROR <= status_code < 600  # noqa: PLR2004
    )


async def _aupload_one_part(
    part_client: AsyncClient,
    part_url: str,
    chunk: bytes,
    content_md5: str,
    part_number: int,
) -> str:
    """PUT a single part to its presigned URL with retry on transient errors.

    Returns the ETag header from the response. Retries up to
    PART_UPLOAD_MAX_RETRIES times on transport errors AND on HTTP 429/5xx.
    Backoff is exponential: 1s, 2s, 4s. Other 4xx responses propagate
    immediately.

    Idempotency: retrying a part PUT to the same presigned URL is safe; the
    cloud overwrites the same part with byte-identical content (same upload_id,
    same part_number, same Content-MD5).
    """
    last_error: Exception | None = None
    for attempt in range(PART_UPLOAD_MAX_RETRIES):
        try:
            resp = await part_client.put(
                part_url, content=chunk, headers={"Content-MD5": content_md5}
            )
            resp.raise_for_status()
            return resp.headers.get("etag", "")
        except HTTPStatusError as e:
            if not _is_retryable_http_status(e.response.status_code):
                raise
            last_error = e
        except _PART_RETRYABLE_ERRORS as e:
            last_error = e

        if attempt < PART_UPLOAD_MAX_RETRIES - 1:
            delay = PART_UPLOAD_RETRY_BASE_DELAY_SECONDS * (2**attempt)
            logger.warning(
                f"Part {part_number} upload failed "
                f"(attempt {attempt + 1}/{PART_UPLOAD_MAX_RETRIES}), "
                f"retrying in {delay}s: {last_error!r}"
            )
            await asyncio.sleep(delay)
    raise DataStorageCreationError(
        f"Failed to upload part {part_number} after {PART_UPLOAD_MAX_RETRIES} attempts: {last_error!r}"
    ) from last_error


def _upload_one_part(
    part_client: Client,
    part_url: str,
    chunk: bytes,
    content_md5: str,
    part_number: int,
) -> str:
    last_error: Exception | None = None
    for attempt in range(PART_UPLOAD_MAX_RETRIES):
        try:
            resp = part_client.put(
                part_url, content=chunk, headers={"Content-MD5": content_md5}
            )
            resp.raise_for_status()
            return resp.headers.get("etag", "")
        except HTTPStatusError as e:
            if not _is_retryable_http_status(e.response.status_code):
                raise
            last_error = e
        except _PART_RETRYABLE_ERRORS as e:
            last_error = e

        if attempt < PART_UPLOAD_MAX_RETRIES - 1:
            delay = PART_UPLOAD_RETRY_BASE_DELAY_SECONDS * (2**attempt)
            logger.warning(
                f"Part {part_number} upload failed "
                f"(attempt {attempt + 1}/{PART_UPLOAD_MAX_RETRIES}), "
                f"retrying in {delay}s: {last_error!r}"
            )
            time.sleep(delay)
    raise DataStorageCreationError(
        f"Failed to upload part {part_number} after {PART_UPLOAD_MAX_RETRIES} attempts: {last_error!r}"
    ) from last_error


async def _aupload_file_multipart(
    client: AsyncClient,
    entry_id: UUID | str,
    file_path: Path,
    file_size: int,
    progress_bar: tqdm,
) -> None:
    """Upload a file via the cloud-agnostic multipart-upload route (async).

    Steps:
      1. Compute byte ranges + base64 MD5 per part.
      2. POST initiate -> {upload_id, part_urls}.
      3. PUT each part to its presigned URL (max 6 concurrent), no auth header.
      4. POST complete with {upload_id, parts}.

    Caller is responsible for the terminal PATCH .../{entry_id} {status: active}.
    """
    logger.debug(f"Starting multipart upload for {file_path} ({file_size:,} bytes)")

    ranges = _calculate_multipart_ranges(file_size)
    part_hashes: list[str] = []
    for start, end in ranges:
        chunk = _read_file_range(file_path, start, end)
        part_hashes.append(_b64_md5(chunk))

    initiate_resp = await client.post(
        f"/v0.1/data-storage/data-entries/{entry_id}/multipart-upload/initiate",
        json={"part_hashes": part_hashes},
    )
    initiate_resp.raise_for_status()
    initiate_body = initiate_resp.json()
    upload_id: str = initiate_body["upload_id"]
    part_urls: list[str] = initiate_body["part_urls"]

    if len(part_urls) != len(ranges):
        raise DataStorageCreationError(
            f"Server returned {len(part_urls)} part URLs but expected {len(ranges)}"
        )

    parts_out: list[dict[str, Any]] = [{} for _ in ranges]
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_PART_UPLOADS)

    async def upload_part_with_index(index: int) -> None:
        async with semaphore:
            start, end = ranges[index]
            chunk = _read_file_range(file_path, start, end)
            etag = await _aupload_one_part(
                part_client=part_client,
                part_url=part_urls[index],
                chunk=chunk,
                content_md5=part_hashes[index],
                part_number=index + 1,
            )
            parts_out[index] = {
                "part_number": index + 1,
                "etag": etag,
                "checksum": part_hashes[index],
            }
            progress_bar.update(len(chunk))

    async with AsyncClient(timeout=None) as part_client:  # noqa: S113
        tasks = [
            asyncio.create_task(upload_part_with_index(i)) for i in range(len(ranges))
        ]
        try:
            await asyncio.gather(*tasks)
        except BaseException:
            for t in tasks:
                if not t.done():
                    t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

    complete_resp = await client.post(
        f"/v0.1/data-storage/data-entries/{entry_id}/multipart-upload/complete",
        json={"upload_id": upload_id, "parts": parts_out},
    )
    complete_resp.raise_for_status()
    logger.debug(
        f"Multipart upload completed for entry {entry_id} ({len(ranges)} parts)"
    )


def _upload_file_multipart(
    client: Client,
    entry_id: UUID | str,
    file_path: Path,
    file_size: int,
    progress_bar: tqdm,
) -> None:
    """Upload a file via the multipart-upload route (sync, native).

    Native sync implementation using ThreadPoolExecutor for parallel part PUTs.
    Do NOT replace this with asyncio.run wrapping the async version - that
    would raise RuntimeError when called from inside a running event loop
    (Jupyter, FastAPI handlers that misuse the sync API, etc.).
    """
    logger.debug(f"Starting multipart upload for {file_path} ({file_size:,} bytes)")

    ranges = _calculate_multipart_ranges(file_size)
    part_hashes: list[str] = []
    for start, end in ranges:
        chunk = _read_file_range(file_path, start, end)
        part_hashes.append(_b64_md5(chunk))

    initiate_resp = client.post(
        f"/v0.1/data-storage/data-entries/{entry_id}/multipart-upload/initiate",
        json={"part_hashes": part_hashes},
    )
    initiate_resp.raise_for_status()
    initiate_body = initiate_resp.json()
    upload_id: str = initiate_body["upload_id"]
    part_urls: list[str] = initiate_body["part_urls"]

    if len(part_urls) != len(ranges):
        raise DataStorageCreationError(
            f"Server returned {len(part_urls)} part URLs but expected {len(ranges)}"
        )

    parts_out: list[dict[str, Any]] = [{} for _ in ranges]

    def upload_part_with_index(index: int, part_client: Client) -> None:
        start, end = ranges[index]
        chunk = _read_file_range(file_path, start, end)
        etag = _upload_one_part(
            part_client=part_client,
            part_url=part_urls[index],
            chunk=chunk,
            content_md5=part_hashes[index],
            part_number=index + 1,
        )
        parts_out[index] = {
            "part_number": index + 1,
            "etag": etag,
            "checksum": part_hashes[index],
        }
        progress_bar.update(len(chunk))

    with (
        Client(timeout=None) as part_client,  # noqa: S113
        concurrent.futures.ThreadPoolExecutor(
            max_workers=MAX_CONCURRENT_PART_UPLOADS
        ) as executor,
    ):
        futures = [
            executor.submit(upload_part_with_index, i, part_client)
            for i in range(len(ranges))
        ]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    complete_resp = client.post(
        f"/v0.1/data-storage/data-entries/{entry_id}/multipart-upload/complete",
        json={"upload_id": upload_id, "parts": parts_out},
    )
    complete_resp.raise_for_status()
    logger.debug(
        f"Multipart upload completed for entry {entry_id} ({len(ranges)} parts)"
    )
