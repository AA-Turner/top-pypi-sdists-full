# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Centralized GCP authentication utilities.

This module provides a single code path for GCP credential handling across
the airbyte-ops-mcp codebase. It supports both standard Application Default
Credentials (ADC) and the GCP_PROD_DB_ACCESS_CREDENTIALS environment variable
used internally at Airbyte.

The preferred approach is to pass credentials directly to GCP client constructors
rather than relying on file-based ADC discovery. This module provides helpers
that construct credentials from JSON content in environment variables.

Usage:
    from airbyte_ops_mcp.gcp_auth import get_gcp_credentials, get_secret_manager_client

    # Get credentials object to pass to any GCP client
    credentials = get_gcp_credentials()
    client = logging.Client(project="my-project", credentials=credentials)

    # Or use the convenience helper for Secret Manager
    client = get_secret_manager_client()
"""

from __future__ import annotations

import json
import logging
import os
import sys
import threading

import google.auth
from google.cloud import logging as gcp_logging
from google.cloud import secretmanager
from google.oauth2 import service_account

from airbyte_ops_mcp.constants import ENV_GCP_PROD_DB_ACCESS_CREDENTIALS

logger = logging.getLogger(__name__)


def _get_identity_from_service_account_info(info: dict) -> str | None:
    """Extract service account identity from parsed JSON info.

    Only accesses the 'client_email' key to avoid any risk of leaking
    other credential material.

    Args:
        info: Parsed service account JSON as a dict.

    Returns:
        The client_email if present and a string, otherwise None.
    """
    client_email = info.get("client_email")
    if isinstance(client_email, str):
        return client_email
    return None


def _get_identity_from_credentials(
    credentials: google.auth.credentials.Credentials,
) -> str | None:
    """Extract identity from a credentials object using safe attribute access.

    Only accesses known-safe attributes that don't trigger network calls
    or token refresh.

    Args:
        credentials: A GCP credentials object.

    Returns:
        The service account email if available, otherwise None.
    """
    # Try service_account_email first (most common for service accounts)
    identity = getattr(credentials, "service_account_email", None)
    if isinstance(identity, str):
        return identity

    # Try signer_email as fallback (sometimes present on impersonated creds)
    identity = getattr(credentials, "signer_email", None)
    if isinstance(identity, str):
        return identity

    return None


# Default scopes for GCP services used by this module
DEFAULT_GCP_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# Module-level cache for credentials (thread-safe)
_cached_credentials: google.auth.credentials.Credentials | None = None
_credentials_lock = threading.Lock()


def get_gcp_credentials() -> google.auth.credentials.Credentials:
    """Get GCP credentials, preferring direct JSON parsing over file-based ADC.

    This function resolves credentials in the following order:
    1. GCP_PROD_DB_ACCESS_CREDENTIALS env var (JSON content) - parsed directly
    2. Standard ADC discovery (workload identity, gcloud auth, GOOGLE_APPLICATION_CREDENTIALS)

    The credentials are cached after first resolution for efficiency.
    Uses the cloud-platform scope which provides access to all GCP services.

    Returns:
        A Credentials object that can be passed to any GCP client constructor.

    Raises:
        google.auth.exceptions.DefaultCredentialsError: If no credentials can be found.
    """
    global _cached_credentials

    # Return cached credentials if available (fast path without lock)
    if _cached_credentials is not None:
        return _cached_credentials

    # Acquire lock for thread-safe credential initialization
    with _credentials_lock:
        # Double-check after acquiring lock (another thread may have initialized)
        if _cached_credentials is not None:
            return _cached_credentials

        # Try GCP_PROD_DB_ACCESS_CREDENTIALS first (JSON content in env var)
        creds_json = os.getenv(ENV_GCP_PROD_DB_ACCESS_CREDENTIALS)
        if creds_json:
            try:
                creds_dict = json.loads(creds_json)
                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=DEFAULT_GCP_SCOPES,
                )
                # Extract identity safely (only after successful credential creation)
                identity = _get_identity_from_service_account_info(creds_dict)
                identity_str = f" (identity: {identity})" if identity else ""
                print(
                    f"GCP credentials loaded from {ENV_GCP_PROD_DB_ACCESS_CREDENTIALS}{identity_str}",
                    file=sys.stderr,
                )
                logger.debug(
                    f"Loaded GCP credentials from {ENV_GCP_PROD_DB_ACCESS_CREDENTIALS} env var"
                )
                _cached_credentials = credentials
                return credentials
            except (json.JSONDecodeError, ValueError) as e:
                # Log only exception type to avoid any risk of leaking credential content
                logger.warning(
                    f"Failed to parse {ENV_GCP_PROD_DB_ACCESS_CREDENTIALS}: "
                    f"{type(e).__name__}. Falling back to ADC discovery."
                )

        # Fall back to standard ADC discovery
        credentials, project = google.auth.default(scopes=DEFAULT_GCP_SCOPES)
        # Extract identity safely from ADC credentials
        identity = _get_identity_from_credentials(credentials)
        identity_str = f" (identity: {identity})" if identity else ""
        project_str = f" (project: {project})" if project else ""
        print(
            f"GCP credentials loaded via ADC{project_str}{identity_str}",
            file=sys.stderr,
        )
        logger.debug(f"Loaded GCP credentials via ADC discovery (project: {project})")
        _cached_credentials = credentials
        return credentials


def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    """Get a Secret Manager client with proper credential handling.

    This function uses get_gcp_credentials() to resolve credentials and passes
    them directly to the client constructor.

    Returns:
        A configured SecretManagerServiceClient instance.
    """
    credentials = get_gcp_credentials()
    return secretmanager.SecretManagerServiceClient(credentials=credentials)


def get_logging_client(project: str) -> gcp_logging.Client:
    """Get a Cloud Logging client with proper credential handling.

    This function uses get_gcp_credentials() to resolve credentials and passes
    them directly to the client constructor.

    Args:
        project: The GCP project ID to use for logging operations.

    Returns:
        A configured Cloud Logging Client instance.
    """
    credentials = get_gcp_credentials()
    return gcp_logging.Client(project=project, credentials=credentials)
