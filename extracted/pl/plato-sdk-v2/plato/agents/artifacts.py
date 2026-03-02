"""Artifact upload utilities for Plato agents and worlds.

These functions upload artifacts directly to S3 using presigned URLs.
"""

from __future__ import annotations

import io
import logging
import zipfile
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)


def zip_directory(dir_path: str) -> bytes:
    """Zip an entire directory.

    Args:
        dir_path: Path to the directory

    Returns:
        Zip file contents as bytes.
    """
    path = Path(dir_path)
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(path)
                zf.write(file_path, arcname)

    buffer.seek(0)
    return buffer.read()


async def upload_to_s3(upload_url: str, data: bytes, content_type: str = "application/octet-stream") -> bool:
    """Upload data directly to S3 using a presigned URL.

    Args:
        upload_url: Presigned S3 PUT URL
        data: Raw bytes to upload
        content_type: MIME type of the content

    Returns:
        True if successful, False otherwise
    """
    if not upload_url:
        logger.warning("No upload URL provided")
        return False

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.put(
                upload_url,
                content=data,
                headers={"Content-Type": content_type},
            )
            if response.status_code in (200, 201, 204):
                logger.info(f"Uploaded {len(data)} bytes to S3")
                return True
            else:
                logger.warning(f"S3 upload failed: {response.status_code} {response.text}")
                return False
    except Exception as e:
        logger.warning(f"Failed to upload to S3: {e}")
        return False


async def upload_artifacts(upload_url: str, dir_path: str) -> bool:
    """Upload a directory as a zip directly to S3.

    Args:
        upload_url: Presigned S3 PUT URL
        dir_path: Path to the directory to upload

    Returns:
        True if successful, False otherwise
    """
    try:
        zip_data = zip_directory(dir_path)
        logger.info(f"Zipped directory: {len(zip_data)} bytes")
    except Exception as e:
        logger.warning(f"Failed to zip directory: {e}")
        return False

    return await upload_to_s3(upload_url, zip_data, "application/zip")


async def upload_artifact(
    upload_url: str,
    data: bytes,
    content_type: str = "application/octet-stream",
) -> bool:
    """Upload an artifact directly to S3.

    Args:
        upload_url: Presigned S3 PUT URL
        data: Raw bytes of the artifact
        content_type: MIME type of the content

    Returns:
        True if successful, False otherwise
    """
    return await upload_to_s3(upload_url, data, content_type)
