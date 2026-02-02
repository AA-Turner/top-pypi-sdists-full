"""File download implementation for remote execution client."""

import logging
import os
from pathlib import Path

import httpx

from exponent.core.remote_execution.cli_rpc_types import (
    DownloadFromUrlRequest,
    DownloadFromUrlResponse,
)

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = "Indent-HTTP-Client/1.0"


async def download_file_from_url(
    request: DownloadFromUrlRequest,
) -> DownloadFromUrlResponse:
    """
    Download a file from a URL to the local filesystem.

    Args:
        request: DownloadFromUrlRequest containing URL, file path, and timeout

    Returns:
        DownloadFromUrlResponse with file path, size, and success status
    """
    logger.info(f"Downloading file to {request.file_path}")

    try:
        file_path = Path(request.file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        headers = {"User-Agent": DEFAULT_USER_AGENT}

        async with httpx.AsyncClient(timeout=request.timeout) as client:
            async with client.stream("GET", request.url, headers=headers) as response:
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)

            file_size = os.path.getsize(file_path)

            logger.info(f"Downloaded file to {request.file_path} ({file_size} bytes)")

            return DownloadFromUrlResponse(
                file_path=request.file_path,
                file_size_bytes=file_size,
                success=True,
                error_message=None,
            )

    except httpx.TimeoutException:
        error_msg = (
            f"Download from {request.url} timed out after {request.timeout} seconds"
        )
        logger.error(error_msg)
        return DownloadFromUrlResponse(
            file_path=request.file_path,
            file_size_bytes=0,
            success=False,
            error_message=error_msg,
        )

    except httpx.HTTPStatusError as e:
        error_msg = (
            f"HTTP error downloading from {request.url}: {e.response.status_code}"
        )
        logger.error(error_msg)
        return DownloadFromUrlResponse(
            file_path=request.file_path,
            file_size_bytes=0,
            success=False,
            error_message=error_msg,
        )

    except httpx.RequestError as e:
        error_msg = f"Request error downloading from {request.url}: {e!s}"
        logger.error(error_msg)
        return DownloadFromUrlResponse(
            file_path=request.file_path,
            file_size_bytes=0,
            success=False,
            error_message=error_msg,
        )

    except OSError as e:
        error_msg = f"File system error writing to {request.file_path}: {e!s}"
        logger.error(error_msg)
        return DownloadFromUrlResponse(
            file_path=request.file_path,
            file_size_bytes=0,
            success=False,
            error_message=error_msg,
        )

    except Exception as e:
        error_msg = f"Unexpected error downloading from {request.url}: {e!s}"
        logger.error(error_msg)
        return DownloadFromUrlResponse(
            file_path=request.file_path,
            file_size_bytes=0,
            success=False,
            error_message=error_msg,
        )
