# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""GCS helper functions for registry operations.

This module provides utilities for interacting with Google Cloud Storage,
including authentication and file operations.
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
from pathlib import Path

from google.cloud import storage
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


def get_gcs_storage_client(gcs_creds: str | None = None) -> storage.Client:
    """Get the GCS storage client.

    Credential resolution order:
    1. Explicit `gcs_creds` argument (JSON string).
    2. `GCS_CREDENTIALS` environment variable (JSON string).
    3. `GCP_GSM_CREDENTIALS` environment variable (JSON string).
    4. Application Default Credentials (ADC) - e.g. `gcloud auth application-default login`.

    Args:
        gcs_creds: Optional GCS credentials JSON string. If not provided,
            will read from GCS_CREDENTIALS environment variable, then fall
            back to Application Default Credentials.

    Returns:
        storage.Client: Authenticated GCS storage client
    """
    gcs_creds = (
        gcs_creds
        if gcs_creds
        else os.environ.get("GCS_CREDENTIALS") or os.environ.get("GCP_GSM_CREDENTIALS")
    )
    if gcs_creds:
        service_account_info = json.loads(gcs_creds)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info
        )
        project = service_account_info.get("project_id")
        return storage.Client(credentials=credentials, project=project)

    # Fall back to Application Default Credentials (ADC)
    logger.debug("GCS_CREDENTIALS not set; using Application Default Credentials.")
    project = (
        os.environ.get("GOOGLE_CLOUD_PROJECT")
        or os.environ.get("CLOUDSDK_CORE_PROJECT")
        or os.environ.get("GCLOUD_PROJECT")
    )
    return storage.Client(project=project)


def get_gcs_credentials_token() -> dict[str, str] | None:
    """Return a credentials token suitable for `gcsfs.GCSFileSystem(token=...)`.

    Credential resolution order:
    1. `GCS_CREDENTIALS` environment variable (JSON service account key) - returns parsed dict.
    2. `GCP_GSM_CREDENTIALS` environment variable (JSON service account key) - returns parsed dict.
    3. Application Default Credentials (ADC) - returns `None` so that
       `gcsfs` falls through to `google.auth.default()`.

    Returns:
        Parsed JSON dict when explicit credentials are available, or `None`
        to signal that `gcsfs` should use ADC.
    """
    gcs_creds = os.environ.get("GCS_CREDENTIALS") or os.environ.get(
        "GCP_GSM_CREDENTIALS"
    )
    if gcs_creds:
        return json.loads(gcs_creds)

    logger.debug(
        "GCS_CREDENTIALS and GCP_GSM_CREDENTIALS not set; gcsfs will use "
        "Application Default Credentials."
    )
    return None


def safe_read_gcs_file(gcs_blob: storage.Blob) -> str | None:
    """Safely read a file from GCS.

    Args:
        gcs_blob: The GCS blob to read

    Returns:
        File contents as string, or None if blob doesn't exist
    """
    if not gcs_blob.exists():
        return None

    return gcs_blob.download_as_string().decode("utf-8")


def compute_gcs_md5(file_path: Path) -> str:
    """Compute MD5 hash in GCS-compatible format.

    GCS uses base64-encoded MD5 hashes for content verification.

    Args:
        file_path: Path to the file

    Returns:
        Base64-encoded MD5 hash
    """
    md5_hash = hashlib.md5()
    md5_hash.update(file_path.read_bytes())
    return base64.b64encode(md5_hash.digest()).decode("utf-8")


def upload_file_if_changed(
    local_file_path: Path,
    bucket: storage.bucket.Bucket,
    blob_path: str,
    disable_cache: bool = False,
) -> tuple[bool, str | None]:
    """Upload a file to GCS if it has changed.

    Compares MD5 hashes to avoid re-uploading unchanged files.

    Args:
        local_file_path: Path to the local file
        bucket: GCS bucket to upload to
        blob_path: Path within the bucket
        disable_cache: If True, set Cache-Control to no-cache

    Returns:
        Tuple of (was_uploaded, blob_id)
    """
    local_file_md5_hash = compute_gcs_md5(local_file_path)
    remote_blob = bucket.blob(blob_path)

    # Reload the blob to get the md5_hash
    blob_exists = remote_blob.exists()
    if blob_exists:
        remote_blob.reload()

    remote_blob_md5_hash = remote_blob.md5_hash if blob_exists else None

    if local_file_md5_hash != remote_blob_md5_hash:
        if disable_cache:
            remote_blob.cache_control = "no-cache"
        remote_blob.upload_from_filename(str(local_file_path))
        return True, remote_blob.id

    return False, remote_blob.id
