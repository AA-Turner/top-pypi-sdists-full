# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Fetch connector test secrets using the PyAirbyte secrets API.

This module uses the PyAirbyte GoogleGSMSecretManager to retrieve
integration test secrets from Google Secret Manager for connectors.

Usage:
    from airbyte_ops_mcp.regression_tests.cdk_secrets import get_first_config_from_secrets

    # Fetch the first config for a connector
    config = get_first_config_from_secrets("source-github")
    if config:
        # Use the config dict
        ...

Note: Requires GCP credentials with access to the integration testing project.
The credentials can be provided via:
- GOOGLE_APPLICATION_CREDENTIALS environment variable
- GCP_GSM_CREDENTIALS environment variable (JSON string)
- Application Default Credentials
"""

from __future__ import annotations

import logging
import os

from airbyte.secrets import GoogleGSMSecretManager

logger = logging.getLogger(__name__)

# Default GCP project for integration test secrets
DEFAULT_GSM_PROJECT = "dataline-integration-testing"


def get_first_config_from_secrets(
    connector_name: str,
    project: str = DEFAULT_GSM_PROJECT,
) -> dict | None:
    """Fetch the first integration test config for a connector from GSM.

    This function uses the PyAirbyte GoogleGSMSecretManager to fetch secrets
    labeled with the connector name and returns the first one as a parsed dict.

    Args:
        connector_name: The connector name (e.g., 'source-github').
        project: The GCP project ID containing the secrets.

    Returns:
        The parsed config dict, or None if no secrets are found or fetching fails.
    """
    # Get credentials from environment
    credentials_json: str | None = None
    credentials_path: str | None = None

    if "GCP_GSM_CREDENTIALS" in os.environ:
        credentials_json = os.environ["GCP_GSM_CREDENTIALS"]
    elif "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    # If no explicit credentials, GoogleGSMSecretManager will try ADC
    try:
        gsm = GoogleGSMSecretManager(
            project=project,
            credentials_json=credentials_json,
            credentials_path=credentials_path,
        )
    except Exception as e:
        logger.warning(f"Failed to initialize GSM client: {e}")
        return None

    logger.info(f"Fetching integration test config for {connector_name} from GSM")

    try:
        # fetch_connector_secret returns the first secret matching the connector label
        secret_handle = gsm.fetch_connector_secret(connector_name)
        # parse_json() calls get_value() internally and parses the result
        config = secret_handle.parse_json()
        logger.info(f"Successfully fetched config for {connector_name}")
        return dict(config) if config else None

    except StopIteration:
        logger.warning(f"No secrets found for connector {connector_name}")
        return None
    except Exception as e:
        # Log the exception type but not the message (may contain sensitive info)
        logger.warning(
            f"Failed to fetch config for {connector_name}: {type(e).__name__}"
        )
        return None
