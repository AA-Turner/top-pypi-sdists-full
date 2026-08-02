"""Multipart upload helpers for large files on AWS instances.

This module implements the client side of PipeBio's S3 multipart upload flow:
splitting a file into parts, requesting presigned URLs, uploading each part with
retries, and finalising (or aborting) the upload. :func:`upload_multipart_aws`
is the public entry point and is used automatically by
:meth:`pipebio.pipebio_client.PipebioClient.upload_file` for files at or above
:data:`MULTIPART_THRESHOLD`.
"""

import math
import os
import sys
import time
from typing import Callable, Dict, List, Optional

import requests
from requests import HTTPError
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.models.entity_types import EntityTypes
from pipebio.models.upload_detail import UploadDetail
from pipebio.util import Util

CHUNK_SIZE = 50 * 1024 * 1024
MULTIPART_THRESHOLD = 100 * 1024 * 1024
MAX_RETRIES = 5
CHUNK_UPLOAD_TIMEOUT = 10 * 60


def _format_bytes(size: int) -> str:
    """Format a byte count into a human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def _print_progress(
    bytes_uploaded: int, file_size: int, part_number: int, total_parts: int
) -> None:
    """Print a single-line progress bar that overwrites itself."""
    pct = bytes_uploaded / file_size if file_size > 0 else 1.0
    bar_width = 30
    filled = int(bar_width * pct)
    bar = "\u2588" * filled + "\u2591" * (bar_width - filled)
    line = (
        f"\rUploading: [{bar}] {pct:>6.1%}"
        f"  {_format_bytes(bytes_uploaded)} / {_format_bytes(file_size)}"
        f"  (part {part_number}/{total_parts})\033[K"
    )
    sys.stdout.write(line)
    sys.stdout.flush()
    if bytes_uploaded >= file_size:
        sys.stdout.write("\n")


def _is_retryable(e: Exception) -> bool:
    """Return True if the exception represents a transient failure worth retrying."""
    if isinstance(
        e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
    ):
        return True
    if isinstance(e, HTTPError) and e.response is not None:
        code = e.response.status_code
        return code >= 500 or code == 429
    return False


def _post_with_retries(
    session: BaseUrlSession,
    url: str,
    json: dict,
    retries: int = MAX_RETRIES,
) -> requests.Response:
    """POST to a session endpoint with retries and exponential backoff."""
    for attempt in range(1, retries + 1):
        try:
            response = session.post(url, json=json)
            Util.raise_detailed_error(response)
            return response
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            HTTPError,
        ) as e:
            if not _is_retryable(e) or attempt == retries:
                raise
            wait = min(2**attempt, 60)
            print(f"{url} attempt {attempt} failed, retrying in {wait}s...")
            time.sleep(wait)
    raise Exception(f"POST {url} failed after {retries} attempts")


def upload_multipart_aws(
    session: BaseUrlSession,
    absolute_file_location: str,
    file_name: str,
    parent_id: str,
    project_id: str,
    organization_id: str,
    details: Optional[List[UploadDetail]] = None,
    file_name_id: Optional[str] = None,
    on_progress: Optional[Callable[[int, int], None]] = None,
) -> dict:
    """Upload a large file to an AWS instance using S3 multipart upload.

    Coordinates with the server's multipart-upload endpoints to split the file
    into parts, upload each with retries, and finalise the upload. Attempts to
    abort on failure to free orphaned parts.

    Args:
        session: An authenticated base-url session from the client.
        absolute_file_location: Path to the local file to upload.
        file_name: Friendly name shown in the PipeBio UI.
        parent_id: Id of the target parent folder.
        project_id: Id of the project (shareable) to upload into.
        organization_id: Organization id that will own the upload.
        details: Optional per-file upload details/metadata.
        file_name_id: Optional client-supplied id used to correlate the file.
        on_progress: Optional callback receiving ``(bytes_uploaded, file_size)``
            after each part.

    Returns:
        The created upload job object.

    Raises:
        ValueError: If the file is empty.
    """
    file_size = os.path.getsize(absolute_file_location)
    if file_size == 0:
        raise ValueError("Cannot multipart-upload a zero-byte file.")
    print(f"Starting multipart upload of {file_name} ({_format_bytes(file_size)})")

    create_body: Dict = {
        "name": file_name,
        "type": EntityTypes.SEQUENCE_DOCUMENT.value,
        "shareableId": project_id,
        "targetFolderId": parent_id,
        "ownerId": organization_id,
        "details": [],
    }

    if details:
        for detail in details:
            create_body["details"].append(
                detail.to_json() if hasattr(detail, "to_json") else detail
            )

    if file_name_id:
        create_body["details"].append(
            {
                "name": "fileNameId",
                "type": "fileNameId",
                "value": file_name_id,
            }
        )

    response = _post_with_retries(session, "multipart-upload/_create", create_body)
    data = response.json()
    job = data["job"]
    job_id = job["id"]
    upload_id = data["multipartUploadId"]

    print(f"Multipart upload initiated (jobId={job_id})")

    try:
        parts = _upload_all_parts(
            session,
            absolute_file_location,
            file_size,
            upload_id,
            job_id,
            on_progress,
        )
    except Exception:
        _abort_multipart_upload(session, upload_id, job_id)
        raise

    complete_body = {
        "uploadId": upload_id,
        "fileName": job_id,
        "parts": parts,
    }
    _post_with_retries(session, "multipart-upload/_complete", complete_body)

    print(f"Multipart upload complete ({len(parts)} parts)\n")
    return job


def _upload_all_parts(
    session: BaseUrlSession,
    absolute_file_location: str,
    file_size: int,
    upload_id: str,
    job_id: str,
    on_progress: Optional[Callable[[int, int], None]],
) -> List[Dict]:
    """Read the file in chunks and upload each part. Returns the parts list."""
    total_parts = math.ceil(file_size / CHUNK_SIZE)
    parts: List[Dict] = []
    part_number = 1
    bytes_uploaded = 0

    with open(absolute_file_location, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            etag = _upload_part_aws(session, upload_id, job_id, part_number, chunk)
            parts.append({"PartNumber": part_number, "ETag": etag})
            bytes_uploaded += len(chunk)

            _print_progress(bytes_uploaded, file_size, part_number, total_parts)

            if on_progress:
                on_progress(bytes_uploaded, file_size)

            part_number += 1

    return parts


def _upload_part_aws(
    session: BaseUrlSession,
    upload_id: str,
    job_id: str,
    part_number: int,
    chunk: bytes,
) -> str:
    """Upload a single part with retries. Returns the ETag."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            presigned_body = {
                "uploadId": upload_id,
                "fileName": job_id,
                "partNumber": part_number,
            }
            response = session.post(
                "multipart-upload/_get_presigned_url", json=presigned_body
            )
            Util.raise_detailed_error(response)
            presigned_data = response.json()

            upload_response = requests.put(
                presigned_data["url"],
                data=chunk,
                headers=presigned_data.get("headers", {}),
                timeout=CHUNK_UPLOAD_TIMEOUT,
            )
            upload_response.raise_for_status()

            etag = upload_response.headers.get("ETag")
            if not etag:
                raise Exception(
                    f"Server response for part {part_number} missing ETag header"
                )
            return etag.strip('"')

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as e:
            if not _is_retryable(e) or attempt == MAX_RETRIES:
                raise Exception(
                    f"Failed to upload part {part_number} after {MAX_RETRIES} attempts: {e}"
                ) from e
            wait = min(2**attempt, 60)
            print(
                f"  Part {part_number} attempt {attempt} failed, retrying in {wait}s..."
            )
            time.sleep(wait)

    raise Exception(f"Failed to upload part {part_number}")


def _abort_multipart_upload(
    session: BaseUrlSession,
    upload_id: str,
    job_id: str,
) -> None:
    """Attempt to abort the multipart upload via the server's DELETE endpoint."""
    try:
        session.delete(
            f"multipart-upload/{job_id}",
            json={
                "uploadId": upload_id,
            },
        )
        print(f"Multipart upload aborted (uploadId={upload_id}, jobId={job_id}).")
    except Exception:
        print(
            f"Multipart upload abandoned (uploadId={upload_id}, jobId={job_id}). "
            f"Orphaned parts will be cleaned up automatically."
        )
