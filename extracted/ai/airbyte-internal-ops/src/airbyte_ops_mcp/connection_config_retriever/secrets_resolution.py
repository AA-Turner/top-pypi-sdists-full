# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Secret resolution for connection config retrieval.

Refactored from: live_tests/_connection_retriever/secrets_resolution.py
Original source: airbyte-platform-internal/tools/connection-retriever/src/connection_retriever/secrets_resolution.py
"""

from __future__ import annotations

from typing import Any

import dpath
from google.cloud import secretmanager

from airbyte_ops_mcp.constants import GCP_PROJECT_NAME


def get_secret_value(
    secret_manager_client: secretmanager.SecretManagerServiceClient, secret_id: str
) -> str:
    """Get the value of the enabled version of a secret."""
    response = secret_manager_client.list_secret_versions(
        request={"parent": secret_id, "filter": "state:ENABLED"}
    )
    if len(response.versions) == 0:
        raise ValueError(f"No enabled version of secret {secret_id} found")
    enabled_version = response.versions[0]
    response = secret_manager_client.access_secret_version(name=enabled_version.name)
    return response.payload.data.decode("UTF-8")


def is_secret(value: Any) -> bool:
    """Determine if a value is a secret."""
    return isinstance(value, dict) and value.get("_secret") is not None


def resolve_secrets_in_config(
    secret_manager_client: secretmanager.SecretManagerServiceClient,
    connector_config: dict,
) -> dict:
    """Recursively resolve secrets in the connector_config."""
    for key in connector_config:
        if is_secret(connector_config[key]):
            secret_id = f"projects/{GCP_PROJECT_NAME}/secrets/{connector_config[key]['_secret']}"
            connector_config[key] = get_secret_value(secret_manager_client, secret_id)
        elif isinstance(connector_config[key], dict):
            connector_config[key] = resolve_secrets_in_config(
                secret_manager_client, connector_config[key]
            )
    return connector_config


def merge_dicts_non_destructive(a: dict, b: dict) -> dict:
    """Merge two dicts, with b taking precedence for conflicts."""
    merged = a.copy()
    for key, value in b.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_dicts_non_destructive(merged[key], value)
        else:
            merged[key] = value
    return merged


def get_resolved_config(
    secret_manager_client: secretmanager.SecretManagerServiceClient,
    actor_configuration: dict,
    actor_oauth_parameter: dict,
    spec: dict,
) -> dict:
    """Get the resolved configuration, resolving secrets and merging OAuth params."""
    resolved_configuration = resolve_secrets_in_config(
        secret_manager_client, actor_configuration
    )

    # Merge the resolved oauth parameter if the actor definition has OAuth
    if "advanced_auth" in spec:
        try:
            is_using_oauth = (
                dpath.get(
                    actor_configuration,
                    "/".join(spec["advanced_auth"]["predicate_key"]),
                )
                == spec["advanced_auth"]["predicate_value"]
            )
        except KeyError:
            # When no predicate_key is defined but we have advanced_auth in spec
            # we can assume that the connector is only using OAuth.
            is_using_oauth = True
        if is_using_oauth:
            resolved_oauth_parameter = resolve_secrets_in_config(
                secret_manager_client, actor_oauth_parameter
            )
            resolved_configuration = merge_dicts_non_destructive(
                resolved_configuration, resolved_oauth_parameter
            )
    return resolved_configuration
