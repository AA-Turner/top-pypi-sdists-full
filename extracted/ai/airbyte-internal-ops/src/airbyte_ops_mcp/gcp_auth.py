# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Purpose-driven GCP credential resolvers.

Each public function resolves credentials for a specific GCP service. Callers
declare *what* they need access to; the resolver handles *how* to get it.

Resolution order (SA/ADC path):
1. BigQuery checks only `GCP_BIGQUERY_CREDENTIALS`; other resolvers check only
   `GCP_PROD_DB_ACCESS_CREDENTIALS`.
2. Standard ADC discovery (workload identity, gcloud auth, GOOGLE_APPLICATION_CREDENTIALS)

Usage:
    from airbyte_ops_mcp.gcp_auth import get_gcp_credentials_for_tier_gcs_ro

    # Backend/CLI/webapp (SA/ADC path)
    credentials = get_gcp_credentials_for_tier_gcs_ro()
"""

from __future__ import annotations

import json
import logging
import os
import sys
import threading

import google.auth
import google.auth.credentials
from google.cloud import logging as gcp_logging
from google.cloud import secretmanager
from google.oauth2 import service_account

from airbyte_ops_mcp.constants import (
    ENV_GCP_BIGQUERY_CREDENTIALS,
    ENV_GCP_PROD_DB_ACCESS_CREDENTIALS,
)

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
_cached_sa_credentials: dict[tuple[str, ...], google.auth.credentials.Credentials] = {}
_sa_credentials_lock = threading.Lock()


def _resolve_sa_credentials(
    env_vars: tuple[str, ...] = (ENV_GCP_PROD_DB_ACCESS_CREDENTIALS,),
) -> google.auth.credentials.Credentials:
    """Resolve SA/ADC credentials (shared implementation for all SA-based resolvers).

    Resolution order:
    1. First non-empty environment variable in `env_vars` (JSON content); invalid
       credentials raise an error.
    2. Standard ADC discovery (workload identity, gcloud auth, GOOGLE_APPLICATION_CREDENTIALS)

    Credentials are cached by environment-variable order after resolution.
    """
    cached_credentials = _cached_sa_credentials.get(env_vars)
    if cached_credentials is not None:
        return cached_credentials

    with _sa_credentials_lock:
        cached_credentials = _cached_sa_credentials.get(env_vars)
        if cached_credentials is not None:
            return cached_credentials

        for env_var in env_vars:
            creds_json = os.getenv(env_var)
            if not creds_json:
                continue
            creds_dict = json.loads(creds_json)
            if not isinstance(creds_dict, dict):
                raise ValueError("Credential JSON must be an object")

            if creds_dict.get("type") == "service_account":
                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=DEFAULT_GCP_SCOPES,
                )
                identity = _get_identity_from_service_account_info(creds_dict)
            else:
                credentials, _ = google.auth.load_credentials_from_dict(
                    creds_dict,
                    scopes=DEFAULT_GCP_SCOPES,
                )
                identity = _get_identity_from_credentials(credentials)

            identity_str = f" (identity: {identity})" if identity else ""
            print(
                f"GCP credentials loaded from {env_var}{identity_str}",
                file=sys.stderr,
            )
            logger.debug(f"Loaded GCP credentials from {env_var} env var")
            _cached_sa_credentials[env_vars] = credentials
            return credentials

        credentials, project = google.auth.default(scopes=DEFAULT_GCP_SCOPES)
        identity = _get_identity_from_credentials(credentials)
        identity_str = f" (identity: {identity})" if identity else ""
        project_str = f" (project: {project})" if project else ""
        print(
            f"GCP credentials loaded via ADC{project_str}{identity_str}",
            file=sys.stderr,
        )
        logger.debug(f"Loaded GCP credentials via ADC discovery (project: {project})")
        _cached_sa_credentials[env_vars] = credentials
        return credentials


# =============================================================================
# Purpose-driven credential resolvers
# =============================================================================


def get_gcp_credentials_for_tier_gcs_ro() -> google.auth.credentials.Credentials:
    """Resolve credentials for the customer-tier GCS export bucket.

    Customer tiers are read from the platform's GCS export of
    `organization_customer_tiers` in `gs://airbyte_warehouse_exports`
    (`prod-ab-cloud-proj`). Resolves via SA/ADC for all callers (backend, CLI,
    and the webapp runtime service account).
    """
    return _resolve_sa_credentials()


def get_gcp_credentials_for_prod_db_replica() -> google.auth.credentials.Credentials:
    """Resolve credentials for Cloud SQL prod replica access."""
    return _resolve_sa_credentials()


def get_gcp_credentials_for_bigquery() -> google.auth.credentials.Credentials:
    """Resolve credentials for BigQuery access."""
    return _resolve_sa_credentials((ENV_GCP_BIGQUERY_CREDENTIALS,))


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
