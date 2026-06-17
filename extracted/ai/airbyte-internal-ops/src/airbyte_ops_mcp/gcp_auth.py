# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Purpose-driven GCP credential resolvers.

Each public function resolves credentials for a specific GCP service. Callers
declare *what* they need access to; the resolver handles *how* to get it.

Resolution order (SA/ADC path):
1. `GCP_PROD_DB_ACCESS_CREDENTIALS` env var (JSON service account key)
2. Standard ADC discovery (workload identity, gcloud auth, GOOGLE_APPLICATION_CREDENTIALS)

Usage:
    from airbyte_ops_mcp.gcp_auth import get_gcp_credentials_for_bigquery_ro

    # Webapp/MCP with user token override
    credentials = get_gcp_credentials_for_bigquery_ro(access_token_override=user_token)

    # Backend/CLI (SA path)
    credentials = get_gcp_credentials_for_bigquery_ro()
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
from google.oauth2.credentials import Credentials as GoogleOAuthCredentials

from airbyte_ops_mcp.constants import ENV_GCP_PROD_DB_ACCESS_CREDENTIALS

logger = logging.getLogger(__name__)


# =============================================================================
# Internal helpers
# =============================================================================


def _get_identity_from_service_account_info(info: dict) -> str | None:
    """Extract service account identity from parsed JSON info.

    Only accesses the `client_email` key to avoid any risk of leaking
    other credential material.
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
    """
    identity = getattr(credentials, "service_account_email", None)
    if isinstance(identity, str):
        return identity

    identity = getattr(credentials, "signer_email", None)
    if isinstance(identity, str):
        return identity

    return None


# Default scopes for GCP services used by this module
DEFAULT_GCP_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# Module-level cache for SA/ADC credentials (thread-safe)
_cached_sa_credentials: google.auth.credentials.Credentials | None = None
_sa_credentials_lock = threading.Lock()


def _resolve_sa_credentials() -> google.auth.credentials.Credentials:
    """Resolve SA/ADC credentials (shared implementation for all SA-based resolvers).

    Resolution order:
    1. `GCP_PROD_DB_ACCESS_CREDENTIALS` env var (JSON content) — parsed directly
    2. Standard ADC discovery (workload identity, gcloud auth, GOOGLE_APPLICATION_CREDENTIALS)

    Credentials are cached after first resolution for efficiency.
    """
    global _cached_sa_credentials

    if _cached_sa_credentials is not None:
        return _cached_sa_credentials

    with _sa_credentials_lock:
        if _cached_sa_credentials is not None:
            return _cached_sa_credentials

        creds_json = os.getenv(ENV_GCP_PROD_DB_ACCESS_CREDENTIALS)
        if creds_json:
            try:
                creds_dict = json.loads(creds_json)
                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=DEFAULT_GCP_SCOPES,
                )
                identity = _get_identity_from_service_account_info(creds_dict)
                identity_str = f" (identity: {identity})" if identity else ""
                print(
                    f"GCP credentials loaded from {ENV_GCP_PROD_DB_ACCESS_CREDENTIALS}{identity_str}",
                    file=sys.stderr,
                )
                logger.debug(
                    f"Loaded GCP credentials from {ENV_GCP_PROD_DB_ACCESS_CREDENTIALS} env var"
                )
                _cached_sa_credentials = credentials
                return credentials
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(
                    f"Failed to parse {ENV_GCP_PROD_DB_ACCESS_CREDENTIALS}: "
                    f"{type(e).__name__}. Falling back to ADC discovery."
                )

        credentials, project = google.auth.default(scopes=DEFAULT_GCP_SCOPES)
        identity = _get_identity_from_credentials(credentials)
        identity_str = f" (identity: {identity})" if identity else ""
        project_str = f" (project: {project})" if project else ""
        print(
            f"GCP credentials loaded via ADC{project_str}{identity_str}",
            file=sys.stderr,
        )
        logger.debug(f"Loaded GCP credentials via ADC discovery (project: {project})")
        _cached_sa_credentials = credentials
        return credentials


# =============================================================================
# Purpose-driven credential resolvers
# =============================================================================


def get_gcp_credentials_for_bigquery_ro(
    *,
    access_token_override: str | None = None,
) -> google.auth.credentials.Credentials:
    """Resolve credentials for BigQuery on `airbyte-data-prod`.

    If `access_token_override` is provided (webapp user context), builds
    credentials from the user's Google OAuth token. Otherwise resolves via
    SA/ADC for backend and CLI callers.
    """
    if access_token_override:
        return GoogleOAuthCredentials(token=access_token_override)
    return _resolve_sa_credentials()


def get_gcp_credentials_for_prod_db_replica() -> google.auth.credentials.Credentials:
    """Resolve credentials for Cloud SQL prod replica access."""
    return _resolve_sa_credentials()


def get_gcp_credentials_for_registry_gcs_ro() -> google.auth.credentials.Credentials:
    """Resolve credentials for read-only GCS connector registry bucket access."""
    return _resolve_sa_credentials()


def get_gcp_credentials_for_sa_secrets() -> google.auth.credentials.Credentials:
    """Resolve credentials for Secret Manager access (service-owned secrets)."""
    return _resolve_sa_credentials()


def get_gcp_credentials_for_logging() -> google.auth.credentials.Credentials:
    """Resolve credentials for Cloud Logging access."""
    return _resolve_sa_credentials()


# =============================================================================
# Convenience client constructors
# =============================================================================


def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    """Get a Secret Manager client with proper credential handling."""
    credentials = get_gcp_credentials_for_sa_secrets()
    return secretmanager.SecretManagerServiceClient(credentials=credentials)


def get_logging_client(project: str) -> gcp_logging.Client:
    """Get a Cloud Logging client with proper credential handling."""
    credentials = get_gcp_credentials_for_logging()
    return gcp_logging.Client(project=project, credentials=credentials)
