# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Shared GCS utilities for registry operations.

This module provides common GCS helper functions used across registry
operations, including connector stubs and metadata management.
"""

from __future__ import annotations

from typing import Literal

from google.cloud import storage

from airbyte_ops_mcp.gcp_auth import get_gcp_credentials

# GCS bucket names for the metadata service
PROD_METADATA_SERVICE_BUCKET_NAME = "prod-airbyte-cloud-connector-metadata-service"
DEV_METADATA_SERVICE_BUCKET_NAME = "dev-airbyte-cloud-connector-metadata-service-2"

# Type alias for environment ID
EnvId = Literal["dev", "prod"]


def get_gcs_client() -> storage.Client:
    """Get a GCS storage client using centralized credentials.

    Uses the centralized GCP authentication from gcp_auth module,
    which supports both GCP_PROD_DB_ACCESS_CREDENTIALS env var
    and standard ADC discovery.

    Returns:
        A configured GCS storage client.
    """
    credentials = get_gcp_credentials()
    return storage.Client(credentials=credentials)


def get_bucket_name(env: EnvId) -> str:
    """Get the metadata service bucket name.

    Args:
        env: The environment ID ('dev' or 'prod').

    Returns:
        The bucket name to use for GCS operations.
    """
    if env == "prod":
        return PROD_METADATA_SERVICE_BUCKET_NAME
    return DEV_METADATA_SERVICE_BUCKET_NAME


def get_gcs_file_text(
    bucket_name: str,
    path: str,
    client: storage.Client | None = None,
) -> str | None:
    """Read a text file from GCS.

    Args:
        bucket_name: The GCS bucket name.
        path: The path to the file within the bucket.
        client: Optional GCS client. If not provided, creates one using get_gcs_client().

    Returns:
        The file contents as a string, or None if the file doesn't exist.
    """
    if client is None:
        client = get_gcs_client()

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(path)

    if not blob.exists():
        return None

    return blob.download_as_string().decode("utf-8")


def upload_gcs_file_text(
    bucket_name: str,
    path: str,
    content: str,
    content_type: str = "text/plain",
    client: storage.Client | None = None,
) -> None:
    """Upload a text file to GCS.

    Args:
        bucket_name: The GCS bucket name.
        path: The path to the file within the bucket.
        content: The text content to upload.
        content_type: The MIME type of the content. Defaults to "text/plain".
        client: Optional GCS client. If not provided, creates one using get_gcs_client().
    """
    if client is None:
        client = get_gcs_client()

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(path)
    blob.upload_from_string(content, content_type=content_type)
