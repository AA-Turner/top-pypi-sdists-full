"""Shared plumbing for v0.2 object-storage-backed trajectory state."""

import asyncio
import gzip
import json
import logging
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import httpx
import httpx_aiohttp
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)

from edison_client.utils.general import retry_if_connection_error

logger = logging.getLogger(__name__)

# means "this body is still gzipped"
GZIP_MAGIC_HEADER = b"\x1f\x8b"

DOWNLOAD_TIMEOUT_SECONDS = 60.0
MAX_RETRY_ATTEMPTS = 3
RETRY_MULTIPLIER = 1
MAX_RETRY_WAIT = 10

MAX_CONCURRENT_BLOB_DOWNLOADS = 16

FOLLOW_BLOB_REDIRECTS = True

_V0D2_ROUTE_ABSENT_DETAILS = {404: "Not Found", 405: "Method Not Allowed"}


class StateBlobDownloadError(Exception):
    """Raised when an object-store-backed state blob could not be read."""


def means_v0d2_routes_absent(response: httpx.Response) -> bool:
    """True only when ``response`` is FastAPI's "no such route" 404/405."""
    expected_detail = _V0D2_ROUTE_ABSENT_DETAILS.get(response.status_code)
    if expected_detail is None:
        return False
    try:
        body = response.json()
    except ValueError:
        return False
    return isinstance(body, dict) and body.get("detail") == expected_detail


def decode_state_blob(raw: bytes) -> Any:
    if raw.startswith(GZIP_MAGIC_HEADER):
        raw = gzip.decompress(raw)
    return json.loads(raw)


def collect_state_rows(data: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    agent_state = data.get("agent_state")
    if isinstance(agent_state, list):
        rows.extend(row for row in agent_state if isinstance(row, dict))
    environment_frame = data.get("environment_frame")
    if isinstance(environment_frame, dict):
        rows.append(environment_frame)
    return rows


def _rows_needing_download(data: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in collect_state_rows(data)
        if row.get("state") is None and row.get("download_url")
    ]


# Storage fields that only exist on the v0.2 read path.
_V0D2_ONLY_FIELDS = ("download_url", "content_encoding")


def _strip_v0d2_only_fields(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        for field in _V0D2_ONLY_FIELDS:
            row.pop(field, None)


@retry(
    retry=retry_if_connection_error,
    stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def _download_blob(client: httpx.Client, download_url: str) -> Any:
    response = client.get(download_url)
    response.raise_for_status()
    return decode_state_blob(response.content)


@retry(
    retry=retry_if_connection_error,
    stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def _adownload_blob(client: httpx.AsyncClient, download_url: str) -> Any:
    response = await client.get(download_url)
    response.raise_for_status()
    return await asyncio.to_thread(decode_state_blob, response.content)


def _apply_states(
    data: Mapping[str, Any],
    pending: list[dict[str, Any]],
    results: list[Any],
) -> None:
    for row, result in zip(pending, results, strict=True):
        if isinstance(result, BaseException):
            raise StateBlobDownloadError(
                f"Failed to download trajectory state blob for row {row.get('id')}"
            ) from result
        row["state"] = result
    _strip_v0d2_only_fields(collect_state_rows(data))


def materialize_state_blobs(data: Mapping[str, Any]) -> None:
    pending = _rows_needing_download(data)
    if not pending:
        _strip_v0d2_only_fields(collect_state_rows(data))
        return

    with (
        httpx.Client(
            timeout=DOWNLOAD_TIMEOUT_SECONDS,
            follow_redirects=FOLLOW_BLOB_REDIRECTS,
        ) as client,
        ThreadPoolExecutor(
            max_workers=min(MAX_CONCURRENT_BLOB_DOWNLOADS, len(pending))
        ) as pool,
    ):
        futures = [
            pool.submit(_download_blob, client, row["download_url"]) for row in pending
        ]
        results: list[Any] = []
        for future in futures:
            try:
                results.append(future.result())
            except Exception as e:
                results.append(e)

    _apply_states(data, pending, results)


async def amaterialize_state_blobs(data: Mapping[str, Any]) -> None:
    pending = _rows_needing_download(data)
    if not pending:
        _strip_v0d2_only_fields(collect_state_rows(data))
        return

    async with httpx_aiohttp.HttpxAiohttpClient(
        timeout=DOWNLOAD_TIMEOUT_SECONDS,
        follow_redirects=FOLLOW_BLOB_REDIRECTS,
    ) as client:
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_BLOB_DOWNLOADS)

        async def download(row: dict[str, Any]) -> Any:
            async with semaphore:
                return await _adownload_blob(client, row["download_url"])

        results = await asyncio.gather(
            *(download(row) for row in pending), return_exceptions=True
        )

    _apply_states(data, pending, list(results))
