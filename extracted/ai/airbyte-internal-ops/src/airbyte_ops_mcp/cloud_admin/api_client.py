# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Low-level API client for Airbyte Cloud operations.

This module provides direct HTTP access to Airbyte Cloud APIs that are not
yet available in PyAirbyte. This is vendored functionality from PyAirbyte PR #838.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

import requests
from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp import constants as ops_constants
from airbyte_ops_mcp.cloud_admin.registry_lookup import (
    resolve_canonical_name_to_definition_id,
)

# Internal enums for scoped configuration API "magic strings"
# These values caused issues during development and are now centralized here


class _ScopedConfigKey(str, Enum):
    """Configuration keys used in scoped configuration API.

    Valid values from airbyte-platform-internal:
    oss/airbyte-data/src/main/kotlin/io/airbyte/data/services/shared/ScopedConfigurationKey.kt
    """

    CONNECTOR_VERSION = "connector_version"
    NETWORK_SECURITY_TOKEN = "network_security_token"
    PRODUCT_LIMITS = "product_limits"


class _ResourceType(str, Enum):
    """Resource types for scoped configuration.

    Valid values from airbyte-platform-internal:
    oss/airbyte-config/config-models/src/generated/java/io/airbyte/config/ConfigResourceType.java
    """

    ACTOR_DEFINITION = "actor_definition"
    USER = "user"
    WORKSPACE = "workspace"
    ORGANIZATION = "organization"
    CONNECTION = "connection"
    SOURCE = "source"
    DESTINATION = "destination"


class _ScopeType(str, Enum):
    """Scope types for scoped configuration.

    Valid values from airbyte-platform-internal:
    oss/airbyte-config/config-models/src/generated/java/io/airbyte/config/ConfigScopeType.java
    """

    ORGANIZATION = "organization"
    WORKSPACE = "workspace"
    ACTOR = "actor"


class _OriginType(str, Enum):
    """Origin types for scoped configuration.

    Valid values from airbyte-platform-internal:
    oss/airbyte-config/config-models/src/generated/java/io/airbyte/config/ConfigOriginType.java
    """

    USER = "user"
    BREAKING_CHANGE = "breaking_change"
    CONNECTOR_ROLLOUT = "connector_rollout"


def _auth_root_for_config_api_root(config_api_root: str | None) -> str:
    """Return the token exchange root for the configured API target."""
    if not config_api_root:
        return constants.CLOUD_API_ROOT
    if config_api_root.startswith("http://localhost:"):
        return config_api_root
    return constants.CLOUD_API_ROOT


def _get_access_token(
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
    config_api_root: str | None = None,
) -> str:
    """Get an access token for Airbyte Cloud API.

    If a bearer_token is provided, it is returned directly (already an access token).
    Otherwise, exchanges client_id/client_secret for an access token.

    Args:
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        Access token string

    Raises:
        PyAirbyteInputError: If authentication fails or no valid credentials provided
    """
    # If bearer token provided, use it directly
    if bearer_token:
        return bearer_token

    # Otherwise, exchange client credentials for access token
    if not client_id or not client_secret:
        raise PyAirbyteInputError(
            message="Either bearer_token or both client_id and client_secret must be provided",
        )

    auth_root = _auth_root_for_config_api_root(config_api_root)
    auth_url = f"{auth_root}/applications/token"
    response = requests.post(
        auth_url,
        json={
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to authenticate with Airbyte Cloud: {response.status_code} {response.text}",
            context={
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    data = response.json()
    return data["access_token"]


def get_user_id_by_email(
    email: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> str:
    """Get user ID from email address.

    Args:
        email: The user's email address
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        User ID (UUID string)

    Raises:
        PyAirbyteInputError: If user not found or API request fails
    """
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    endpoint = f"{config_api_root}/users/list_instance_admin"
    response = requests.post(
        endpoint,
        json={},
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to list users: {response.status_code} {response.text}",
            context={
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    data = response.json()
    users = data.get("users", [])

    for user in users:
        if user.get("email", "").strip().lower() == email.strip().lower():
            return user["userId"]

    raise PyAirbyteInputError(
        message=f"No user found with email: {email}",
        context={
            "email": email,
            "available_users": len(users),
        },
    )


def list_instance_admin_users(
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> tuple[dict[str, str], ...]:
    """List instance-admin users from the Config API."""
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )
    endpoint = f"{config_api_root}/users/list_instance_admin"
    response = requests.post(
        endpoint,
        json={},
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to list users: {response.status_code} {response.text}",
            context={
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    users = response.json().get("users", [])
    return tuple(
        {
            "userId": str(user.get("userId", "")),
            "email": str(user.get("email", "")),
        }
        for user in users
        if isinstance(user, dict) and user.get("userId") and user.get("email")
    )


def resolve_connector_version_id(
    actor_definition_id: str,
    connector_type: Literal["source", "destination"],
    version: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> str:
    """Resolve a version string to an actor_definition_version_id.

    Args:
        actor_definition_id: The actor definition ID
        connector_type: Either "source" or "destination"
        version: The version string (e.g., "0.1.47-preview.abe7cb4")
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        Version ID (UUID string)

    Raises:
        PyAirbyteInputError: If version cannot be resolved or API request fails
    """
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    endpoint = f"{config_api_root}/actor_definition_versions/resolve"
    payload = {
        "actorDefinitionId": actor_definition_id,
        "actorType": connector_type,
        "dockerImageTag": version,
    }

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to resolve version: {response.status_code} {response.text}",
            context={
                "endpoint": endpoint,
                "payload": payload,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    data = response.json()
    version_id = data.get("versionId")

    if not version_id:
        raise PyAirbyteInputError(
            message=f"Could not resolve version '{version}' for connector",
            context={
                "actor_definition_id": actor_definition_id,
                "connector_type": connector_type,
                "version": version,
                "response": data,
            },
        )

    return version_id


def _resolve_connector_definition_id(
    *,
    connector_name: str,
    connector_type: Literal["source", "destination"],
    config_api_root: str,
    access_token: str,
) -> str:
    """Resolve a connector name to an actor definition ID."""
    if not config_api_root.startswith("http://localhost:"):
        return resolve_canonical_name_to_definition_id(connector_name)

    definitions_endpoint = (
        f"{config_api_root}/source_definitions/list_latest"
        if connector_type == "source"
        else f"{config_api_root}/destination_definitions/list_latest"
    )
    definitions_response = requests.post(
        definitions_endpoint,
        json={},
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    if definitions_response.status_code != 200:
        raise PyAirbyteInputError(
            message=(
                "Failed to resolve local connector definition: "
                f"{definitions_response.status_code} {definitions_response.text}"
            ),
            context={
                "endpoint": definitions_endpoint,
                "connector_name": connector_name,
            },
        )
    definitions_key = (
        "sourceDefinitions" if connector_type == "source" else "destinationDefinitions"
    )
    definition_id_key = (
        "sourceDefinitionId"
        if connector_type == "source"
        else "destinationDefinitionId"
    )
    for definition in definitions_response.json().get(definitions_key, []):
        raw_name = str(definition.get("name", ""))
        docker_repository = str(definition.get("dockerRepository", ""))
        canonical_name = docker_repository.rsplit("/", maxsplit=1)[-1] or raw_name
        if connector_name in (canonical_name, raw_name):
            return definition[definition_id_key]
    raise PyAirbyteInputError(
        message=f"Could not resolve local connector definition for {connector_name}",
        context={
            "endpoint": definitions_endpoint,
            "connector_name": connector_name,
        },
    )


def _get_scoped_configuration_context(
    actor_definition_id: str,
    scope_type: _ScopeType,
    scope_id: str,
    config_api_root: str,
    access_token: str,
) -> dict[str, Any] | None:
    """Get the active scoped configuration for a single scope level.

    This is the canonical way to query /scoped_configuration/get_context.
    Used by both the unset path and the multi-scope checking in the set path.

    Args:
        actor_definition_id: The actor definition ID for the connector
        scope_type: The scope type enum (ACTOR, WORKSPACE, or ORGANIZATION)
        scope_id: The ID for the scope (connector_id, workspace_id, or organization_id)
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        access_token: Pre-authenticated access token

    Returns:
        The active configuration dict if an override exists at this scope, or None.

    Raises:
        PyAirbyteInputError: If the API request fails
    """
    endpoint = f"{config_api_root}/scoped_configuration/get_context"
    context_payload = {
        "config_key": _ScopedConfigKey.CONNECTOR_VERSION.value,
        "resource_type": _ResourceType.ACTOR_DEFINITION.value,
        "resource_id": actor_definition_id,
        "scope_type": scope_type.value,
        "scope_id": scope_id,
    }

    response = requests.post(
        endpoint,
        json=context_payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to get scoped configuration context for {scope_type.value} scope: "
            f"{response.status_code} {response.text}",
            context={
                "endpoint": endpoint,
                "payload": context_payload,
                "scope_type": scope_type.value,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    context_data = response.json()
    return context_data.get("activeConfiguration")


def get_all_scoped_configuration_contexts(
    connector_id: str,
    actor_definition_id: str,
    workspace_id: str,
    organization_id: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> dict[str, dict[str, Any]]:
    """Get version override configurations at all scope levels (actor, workspace, organization).

    This ALWAYS checks all three scope levels to provide a complete picture of any version
    overrides that may affect the connector. All scope IDs are required to ensure comprehensive
    checking - this function will not silently skip any scope.

    Args:
        connector_id: The ID of the deployed connector (source or destination)
        actor_definition_id: The actor definition ID for the connector
        workspace_id: The workspace ID (required - must always check workspace scope)
        organization_id: The organization ID (required - must always check org scope)
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        Dictionary containing only the scopes that have active configurations.
        Empty dict if no overrides exist (falsy). Keys are 'actor', 'workspace',
        'organization' - only present if an override exists at that scope.

    Raises:
        PyAirbyteInputError: If any API request fails
    """
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    # Start with empty dict - only add entries for scopes that have active configs
    # This ensures the result is falsy if nothing is set
    results: dict[str, dict[str, Any]] = {}

    # Always check all three scopes - no optional skipping
    # Using enum values consistently to avoid magic strings
    scopes_to_check: list[tuple[_ScopeType, str]] = [
        (_ScopeType.ACTOR, connector_id),
        (_ScopeType.WORKSPACE, workspace_id),
        (_ScopeType.ORGANIZATION, organization_id),
    ]

    for scope_type_enum, scope_id in scopes_to_check:
        active_config = _get_scoped_configuration_context(
            actor_definition_id=actor_definition_id,
            scope_type=scope_type_enum,
            scope_id=scope_id,
            config_api_root=config_api_root,
            access_token=access_token,
        )
        if active_config:
            results[scope_type_enum.value] = active_config

    return results


def get_connector_version(
    connector_id: str,
    connector_type: Literal["source", "destination"],
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
    workspace_id: str | None = None,
) -> dict[str, Any]:
    """Get version information for a deployed connector.

    This function retrieves the current version and override status. If workspace_id is provided,
    it also fetches detailed scoped configuration context at all scope levels (actor, workspace,
    organization) to provide a complete picture of any version pins.

    Args:
        connector_id: The ID of the deployed connector (source or destination)
        connector_type: Either "source" or "destination"
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)
        workspace_id: Optional workspace ID to enable detailed scope checking

    Returns:
        Dictionary containing:
        - dockerImageTag: The current version string
        - isVersionOverrideApplied: Boolean indicating if override is active
        - scopedConfigs: (if workspace_id provided) Dict with 'actor', 'workspace', 'organization'
          keys containing the active configuration at each scope level, or None

    Raises:
        PyAirbyteInputError: If the API request fails
    """
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    # Determine endpoint based on connector type
    # config_api_root already includes /v1
    if connector_type == "source":
        endpoint = f"{config_api_root}/actor_definition_versions/get_for_source"
        payload = {"sourceId": connector_id}
        definition_id_key = "sourceDefinitionId"
    else:
        endpoint = f"{config_api_root}/actor_definition_versions/get_for_destination"
        payload = {"destinationId": connector_id}
        definition_id_key = "destinationDefinitionId"

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to get connector version: {response.status_code} {response.text}",
            context={
                "connector_id": connector_id,
                "connector_type": connector_type,
                "endpoint": endpoint,
                "payload": payload,
                "config_api_root": config_api_root,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    data = response.json()

    result: dict[str, Any] = {
        "dockerImageTag": data.get("dockerImageTag", "unknown"),
        "isVersionOverrideApplied": data.get(
            "isVersionOverrideApplied", data.get("isOverrideApplied", False)
        ),
    }

    # If workspace_id is provided, also get detailed scoped configuration context
    if workspace_id:
        # Get actor_definition_id from the connector info
        get_endpoint = f"{config_api_root}/{connector_type}s/get"
        get_payload: dict[str, str] = {f"{connector_type}Id": connector_id}

        get_response = requests.post(
            get_endpoint,
            json=get_payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        if get_response.status_code == 200:
            connector_info = get_response.json()
            actor_definition_id = connector_info.get(definition_id_key)

            if actor_definition_id:
                # Get organization_id from workspace
                workspace_endpoint = f"{config_api_root}/workspaces/get"
                workspace_response = requests.post(
                    workspace_endpoint,
                    json={"workspaceId": workspace_id},
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "User-Agent": ops_constants.USER_AGENT,
                        "Content-Type": "application/json",
                    },
                    timeout=30,
                )

                organization_id = None
                if workspace_response.status_code == 200:
                    workspace_data = workspace_response.json()
                    organization_id = workspace_data.get("organizationId")

                if organization_id:
                    result["scopedConfigs"] = get_all_scoped_configuration_contexts(
                        connector_id=connector_id,
                        actor_definition_id=actor_definition_id,
                        workspace_id=workspace_id,
                        organization_id=organization_id,
                        config_api_root=config_api_root,
                        bearer_token=access_token,
                    )

    return result


def set_connector_version_override(
    connector_id: str,
    connector_type: Literal["source", "destination"],
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    workspace_id: str | None = None,
    version: str | None = None,
    unset: bool = False,
    override_reason: str | None = None,
    override_reason_reference_url: str | None = None,
    user_email: str | None = None,
    bearer_token: str | None = None,
) -> bool:
    """Set or clear a version override for a deployed connector.

    This function checks all three scope levels (actor, workspace, organization) before
    creating a new override to prevent duplicate key constraint violations. If an override
    already exists at the actor scope with a different version, it will be deleted first
    before creating the new one.

    Note:
        Race condition caveat: The check-then-delete-then-create sequence is not atomic.
        If two concurrent requests attempt to set version overrides for the same connector,
        both could pass the existence check and one could still fail with a duplicate key
        error. The improved 500 error message provides guidance in this case.

    Args:
        connector_id: The ID of the deployed connector
        connector_type: Either "source" or "destination"
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        workspace_id: The workspace ID
        version: The version to pin to (e.g., "0.1.0"), or None to unset
        unset: If True, removes any existing override
        override_reason: Required when setting. Explanation for the override
        override_reason_reference_url: Optional URL with more context
        user_email: Email of user creating the override
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        True if operation succeeded, False if no override existed (unset only)

    Raises:
        PyAirbyteInputError: If the API request fails or parameters are invalid
    """
    # Input validation
    if (version is None) == (not unset):
        raise PyAirbyteInputError(
            message="Must specify EXACTLY ONE of version (to set) OR unset=True (to clear), but not both",
        )

    if not unset and (not override_reason or len(override_reason.strip()) < 10):
        raise PyAirbyteInputError(
            message="override_reason is required when setting a version and must be at least 10 characters",
        )

    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    # Build the scoped configuration
    scope_type = _ScopeType.ACTOR

    if unset:
        # To unset, we need to delete the scoped configuration
        # First, get the actor_definition_id for the connector
        get_endpoint: str = f"{config_api_root}/{connector_type}s/get"
        get_payload: dict[str, str] = {f"{connector_type}Id": connector_id}
        definition_id_key = f"{connector_type}DefinitionId"

        get_response = requests.post(
            get_endpoint,
            json=get_payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        if get_response.status_code != 200:
            raise PyAirbyteInputError(
                message=f"Failed to get {connector_type} info: {get_response.status_code} {get_response.text}",
            )

        connector_info = get_response.json()
        actor_definition_id = connector_info.get(definition_id_key)

        if not actor_definition_id:
            raise PyAirbyteInputError(
                message=f"Could not find {definition_id_key} in {connector_type} info",
            )

        # Use the shared helper to get the scoped configuration context at actor scope
        active_config = _get_scoped_configuration_context(
            actor_definition_id=actor_definition_id,
            scope_type=_ScopeType.ACTOR,
            scope_id=connector_id,
            config_api_root=config_api_root,
            access_token=access_token,
        )

        if not active_config:
            # No override exists, nothing to do
            return False

        # Delete the active configuration
        delete_endpoint = f"{config_api_root}/scoped_configuration/delete"
        delete_payload = {"scopedConfigurationId": active_config["id"]}

        response = requests.post(
            delete_endpoint,
            json=delete_payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        if response.status_code not in (200, 204):
            raise PyAirbyteInputError(
                message=f"Failed to delete version override: {response.status_code} {response.text}",
                context={
                    "delete_endpoint": delete_endpoint,
                    "config_id": active_config["id"],
                    "status_code": response.status_code,
                    "response": response.text,
                },
            )

        return True

    else:
        # Set a new override
        # First, get the actor_definition_id for the connector
        get_endpoint = f"{config_api_root}/{connector_type}s/get"
        get_payload: dict[str, str] = {f"{connector_type}Id": connector_id}
        definition_id_key = f"{connector_type}DefinitionId"

        get_response = requests.post(
            get_endpoint,
            json=get_payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        if get_response.status_code != 200:
            raise PyAirbyteInputError(
                message=f"Failed to get {connector_type} info: {get_response.status_code} {get_response.text}",
            )

        connector_info = get_response.json()
        actor_definition_id = connector_info.get(definition_id_key)

        if not actor_definition_id:
            raise PyAirbyteInputError(
                message=f"Could not find {definition_id_key} in {connector_type} info",
            )

        # Resolve version string to version ID
        version_id = resolve_connector_version_id(
            actor_definition_id=actor_definition_id,
            connector_type=connector_type,
            version=version,
            config_api_root=config_api_root,
            client_id=client_id,
            client_secret=client_secret,
            bearer_token=bearer_token,
        )

        # Get organization_id from workspace info for comprehensive scope checking
        # This is REQUIRED - we must always check all three scopes
        workspace_endpoint = f"{config_api_root}/workspaces/get"
        workspace_payload = {"workspaceId": workspace_id}
        workspace_response = requests.post(
            workspace_endpoint,
            json=workspace_payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        if workspace_response.status_code != 200:
            raise PyAirbyteInputError(
                message=f"Failed to get workspace info: {workspace_response.status_code} {workspace_response.text}. "
                "Workspace info is required to determine organization_id for comprehensive scope checking.",
                context={
                    "workspace_id": workspace_id,
                    "status_code": workspace_response.status_code,
                    "response": workspace_response.text,
                },
            )
        workspace_info = workspace_response.json()
        organization_id = workspace_info.get("organizationId")
        if not organization_id:
            raise PyAirbyteInputError(
                message="Workspace does not have an organization_id. "
                "Organization ID is required for comprehensive scope checking.",
                context={
                    "workspace_id": workspace_id,
                    "workspace_info": workspace_info,
                },
            )

        # Check for existing scoped configuration at ALL scope levels BEFORE creating
        # This prevents duplicate key constraint violations (500 errors) and provides
        # clear messaging about where existing pins are set
        all_configs = get_all_scoped_configuration_contexts(
            connector_id=connector_id,
            actor_definition_id=actor_definition_id,
            workspace_id=workspace_id,
            organization_id=organization_id,
            config_api_root=config_api_root,
            client_id=client_id,
            client_secret=client_secret,
            bearer_token=bearer_token,
        )

        # Check actor-level config first (most specific)
        actor_config = all_configs.get(_ScopeType.ACTOR.value)
        if actor_config:
            existing_version_id = actor_config.get("value")
            # API returns snake_case field names
            existing_version_name = actor_config.get("value_name", "unknown")

            # If already pinned to the same version at actor level, no action needed
            if existing_version_id == version_id:
                # Build detailed message with full context about the existing pin
                # API returns snake_case field names
                existing_description = actor_config.get(
                    "description", "No description provided"
                )
                existing_reference_url = actor_config.get(
                    "reference_url", "No reference URL"
                )
                existing_origin = actor_config.get("origin", "unknown")
                existing_origin_type = actor_config.get("origin_type", "unknown")
                existing_created_at = actor_config.get("created_at", "unknown")
                existing_updated_at = actor_config.get("updated_at", "unknown")
                existing_scope_name = actor_config.get("scope_name", "unknown")
                existing_resource_name = actor_config.get("resource_name", "unknown")

                detailed_message = (
                    f"Connector is already pinned to version {existing_version_name} "
                    f"(version_id: {existing_version_id}) at actor scope.\n\n"
                    f"EXISTING PIN DETAILS:\n"
                    f"  - Config ID: {actor_config.get('id')}\n"
                    f"  - Pinned Version: {existing_version_name}\n"
                    f"  - Connector Name: {existing_scope_name}\n"
                    f"  - Connector Definition: {existing_resource_name}\n"
                    f"  - Description: {existing_description}\n"
                    f"  - Reference URL: {existing_reference_url}\n"
                    f"  - Origin Type: {existing_origin_type}\n"
                    f"  - Origin: {existing_origin}\n"
                    f"  - Created At: {existing_created_at}\n"
                    f"  - Updated At: {existing_updated_at}\n\n"
                    f"No action needed. Use unset=True first if you want to re-pin to a different version."
                )

                raise PyAirbyteInputError(
                    message=detailed_message,
                    context={
                        "connector_id": connector_id,
                        "connector_type": connector_type,
                        "existing_version": existing_version_name,
                        "existing_version_id": existing_version_id,
                        "requested_version": version,
                        "requested_version_id": version_id,
                        "existing_config_id": actor_config.get("id"),
                        "existing_description": existing_description,
                        "existing_reference_url": existing_reference_url,
                        "existing_origin": existing_origin,
                        "existing_origin_type": existing_origin_type,
                        "existing_created_at": existing_created_at,
                        "existing_updated_at": existing_updated_at,
                        "scope_level": _ScopeType.ACTOR.value,
                        "scope_type_from_api": actor_config.get("scope_type"),
                        "scope_id_from_api": actor_config.get("scope_id"),
                        "full_existing_config": actor_config,
                    },
                )

            # If pinned to a different version at actor level, delete it first
            # SAFETY GUARD: Only delete if the returned config is truly actor-scoped
            # (not an inherited workspace/org config returned by the API)
            api_scope_type = actor_config.get("scope_type", "").lower()
            api_scope_id = actor_config.get("scope_id", "")
            if api_scope_type != _ScopeType.ACTOR.value or api_scope_id != connector_id:
                raise PyAirbyteInputError(
                    message=f"Cannot delete existing config: API returned a config that is not actor-scoped. "
                    f"Expected scope_type='{_ScopeType.ACTOR.value}' and scope_id='{connector_id}', "
                    f"but got scope_type='{api_scope_type}' and scope_id='{api_scope_id}'. "
                    f"This may be an inherited config from workspace/organization level.",
                    context={
                        "connector_id": connector_id,
                        "expected_scope_type": _ScopeType.ACTOR.value,
                        "expected_scope_id": connector_id,
                        "actual_scope_type": api_scope_type,
                        "actual_scope_id": api_scope_id,
                        "full_config": actor_config,
                    },
                )

            delete_endpoint = f"{config_api_root}/scoped_configuration/delete"
            delete_payload = {"scopedConfigurationId": actor_config["id"]}

            delete_response = requests.post(
                delete_endpoint,
                json=delete_payload,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": ops_constants.USER_AGENT,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

            if delete_response.status_code not in (200, 204):
                raise PyAirbyteInputError(
                    message=f"Failed to delete existing actor-level version override before setting new one: "
                    f"{delete_response.status_code} {delete_response.text}. "
                    f"Connector is currently pinned to {existing_version_name} at actor scope.",
                    context={
                        "delete_endpoint": delete_endpoint,
                        "config_id": actor_config["id"],
                        "existing_version": existing_version_name,
                        "requested_version": version,
                        "status_code": delete_response.status_code,
                        "response": delete_response.text,
                        "scope_level": _ScopeType.ACTOR.value,
                    },
                )

        # Report if there are pins at workspace or organization level (informational)
        # These won't cause duplicate key errors but users should be aware of them
        workspace_config = all_configs.get(_ScopeType.WORKSPACE.value)
        org_config = all_configs.get(_ScopeType.ORGANIZATION.value)
        inherited_pins: list[str] = []
        if workspace_config:
            ws_version = workspace_config.get("valueName", "unknown")
            inherited_pins.append(f"workspace (version: {ws_version})")
        if org_config:
            org_version = org_config.get("valueName", "unknown")
            inherited_pins.append(f"organization (version: {org_version})")

        # Get user ID from email - required by API spec
        if not user_email:
            raise PyAirbyteInputError(
                message="user_email is required to set a version override",
                context={
                    "connector_id": connector_id,
                    "connector_type": connector_type,
                },
            )
        origin = get_user_id_by_email(
            email=user_email,
            config_api_root=config_api_root,
            client_id=client_id,
            client_secret=client_secret,
            bearer_token=bearer_token,
        )

        # Create the override with correct schema
        endpoint = f"{config_api_root}/scoped_configuration/create"

        # Build payload with explicit string values for auditability
        # (enum.value ensures we log exactly what we send)
        payload: dict[str, Any] = {
            "config_key": _ScopedConfigKey.CONNECTOR_VERSION.value,
            "resource_type": _ResourceType.ACTOR_DEFINITION.value,
            "resource_id": actor_definition_id,
            "scope_type": scope_type.value,
            "scope_id": connector_id,
            "value": version_id,  # Use version ID, not version string
            "description": override_reason,
            "origin_type": _OriginType.USER.value,
            "origin": origin,
        }

        if override_reason_reference_url:
            payload["reference_url"] = override_reason_reference_url

        response = requests.post(
            endpoint,
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        if response.status_code not in (200, 201):
            # Provide helpful guidance for 500 errors which often indicate duplicates
            error_message = f"Failed to set version override: {response.status_code} {response.text}"
            if response.status_code == 500:
                error_message += (
                    " A 500 error often indicates a duplicate key constraint violation - "
                    "the connector may already be pinned. Try using unset=True first, "
                    "or use the error lookup tool to get more details on the error ID."
                )
                if inherited_pins:
                    error_message += (
                        f" Note: Version pins were found at other scope levels: {', '.join(inherited_pins)}. "
                        "These inherited pins won't cause duplicate key errors but may affect the connector."
                    )
            raise PyAirbyteInputError(
                message=error_message,
                context={
                    "connector_id": connector_id,
                    "connector_type": connector_type,
                    "version": version,
                    "version_id": version_id,
                    "endpoint": endpoint,
                    "payload": payload,
                    "actor_definition_id": actor_definition_id,
                    "status_code": response.status_code,
                    "response": response.text,
                    "inherited_pins": inherited_pins if inherited_pins else None,
                    "all_scope_configs": {
                        k: {"id": v.get("id"), "valueName": v.get("valueName")}
                        for k, v in all_configs.items()
                        if v
                    },
                },
            )

        return True


def set_workspace_connector_version_override(
    workspace_id: str,
    connector_name: str,
    connector_type: Literal["source", "destination"],
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    version: str | None = None,
    unset: bool = False,
    override_reason: str | None = None,
    override_reason_reference_url: str | None = None,
    user_email: str | None = None,
    bearer_token: str | None = None,
) -> bool:
    """Set or clear a workspace-level version override for a connector type.

    This pins ALL instances of a connector type within a workspace to a specific version.
    For example, pinning 'source-github' at workspace level means all GitHub sources
    in that workspace will use the pinned version.

    Args:
        workspace_id: The workspace ID
        connector_name: The connector name (e.g., 'source-github')
        connector_type: Either "source" or "destination"
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        version: The version to pin to (e.g., "0.1.0"), or None to unset
        unset: If True, removes any existing override
        override_reason: Required when setting. Explanation for the override
        override_reason_reference_url: Optional URL with more context
        user_email: Email of user creating the override
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        True if operation succeeded, False if no override existed (unset only)

    Raises:
        PyAirbyteInputError: If the API request fails or parameters are invalid
    """
    # Input validation
    if (version is None) == (not unset):
        raise PyAirbyteInputError(
            message="Must specify EXACTLY ONE of version (to set) OR unset=True (to clear), but not both",
        )

    if not unset and (not override_reason or len(override_reason.strip()) < 10):
        raise PyAirbyteInputError(
            message="override_reason is required when setting a version and must be at least 10 characters",
        )

    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    # Resolve connector name to actor_definition_id using the shared registry lookup
    actor_definition_id = _resolve_connector_definition_id(
        connector_name=connector_name,
        connector_type=connector_type,
        config_api_root=config_api_root,
        access_token=access_token,
    )
    if unset:
        # Get the existing workspace-level configuration
        active_config = _get_scoped_configuration_context(
            actor_definition_id=actor_definition_id,
            scope_type=_ScopeType.WORKSPACE,
            scope_id=workspace_id,
            config_api_root=config_api_root,
            access_token=access_token,
        )

        if not active_config:
            return False

        # Verify this is actually a workspace-scoped config (not inherited from org)
        api_scope_type = active_config.get("scope_type", "").lower()
        api_scope_id = active_config.get("scope_id", "")
        if api_scope_type != _ScopeType.WORKSPACE.value or api_scope_id != workspace_id:
            raise PyAirbyteInputError(
                message=f"Cannot delete: the active config is not workspace-scoped. "
                f"Expected scope_type='{_ScopeType.WORKSPACE.value}' and scope_id='{workspace_id}', "
                f"but got scope_type='{api_scope_type}' and scope_id='{api_scope_id}'. "
                f"This may be an inherited config from organization level.",
                context={
                    "workspace_id": workspace_id,
                    "expected_scope_type": _ScopeType.WORKSPACE.value,
                    "actual_scope_type": api_scope_type,
                    "actual_scope_id": api_scope_id,
                    "full_config": active_config,
                },
            )

        # Delete the configuration
        delete_endpoint = f"{config_api_root}/scoped_configuration/delete"
        delete_payload = {"scopedConfigurationId": active_config["id"]}

        response = requests.post(
            delete_endpoint,
            json=delete_payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        if response.status_code not in (200, 204):
            raise PyAirbyteInputError(
                message=f"Failed to delete workspace version override: {response.status_code} {response.text}",
                context={
                    "delete_endpoint": delete_endpoint,
                    "config_id": active_config["id"],
                    "status_code": response.status_code,
                    "response": response.text,
                },
            )

        return True

    # Set a new workspace-level override
    # Resolve version string to version ID
    version_id = resolve_connector_version_id(
        actor_definition_id=actor_definition_id,
        connector_type=connector_type,
        version=version,
        config_api_root=config_api_root,
        bearer_token=access_token,
    )

    # Check for existing workspace-level configuration
    existing_config = _get_scoped_configuration_context(
        actor_definition_id=actor_definition_id,
        scope_type=_ScopeType.WORKSPACE,
        scope_id=workspace_id,
        config_api_root=config_api_root,
        access_token=access_token,
    )

    if existing_config:
        existing_version_id = existing_config.get("value")
        existing_version_name = existing_config.get("value_name", "unknown")

        # If already pinned to the same version, no action needed
        if existing_version_id == version_id:
            raise PyAirbyteInputError(
                message=f"Workspace is already pinned to version {existing_version_name} for {connector_name}. "
                f"Use unset=True first if you want to re-pin to a different version.",
                context={
                    "workspace_id": workspace_id,
                    "connector_name": connector_name,
                    "existing_version": existing_version_name,
                    "requested_version": version,
                },
            )

        # Verify this is a workspace-scoped config before deleting
        api_scope_type = existing_config.get("scope_type", "").lower()
        api_scope_id = existing_config.get("scope_id", "")
        if (
            api_scope_type == _ScopeType.WORKSPACE.value
            and api_scope_id == workspace_id
        ):
            # Delete existing workspace-level config before creating new one
            delete_endpoint = f"{config_api_root}/scoped_configuration/delete"
            delete_payload = {"scopedConfigurationId": existing_config["id"]}

            delete_response = requests.post(
                delete_endpoint,
                json=delete_payload,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": ops_constants.USER_AGENT,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

            if delete_response.status_code not in (200, 204):
                raise PyAirbyteInputError(
                    message=f"Failed to delete existing workspace version override: "
                    f"{delete_response.status_code} {delete_response.text}",
                )

    # Get user ID from email
    if not user_email:
        raise PyAirbyteInputError(
            message="user_email is required to set a version override",
        )
    origin = get_user_id_by_email(
        email=user_email,
        config_api_root=config_api_root,
        bearer_token=access_token,
    )

    # Create the override
    endpoint = f"{config_api_root}/scoped_configuration/create"
    payload: dict[str, Any] = {
        "config_key": _ScopedConfigKey.CONNECTOR_VERSION.value,
        "resource_type": _ResourceType.ACTOR_DEFINITION.value,
        "resource_id": actor_definition_id,
        "scope_type": _ScopeType.WORKSPACE.value,
        "scope_id": workspace_id,
        "value": version_id,
        "description": override_reason,
        "origin_type": _OriginType.USER.value,
        "origin": origin,
    }

    if override_reason_reference_url:
        payload["reference_url"] = override_reason_reference_url

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code not in (200, 201):
        raise PyAirbyteInputError(
            message=f"Failed to set workspace version override: {response.status_code} {response.text}",
            context={
                "workspace_id": workspace_id,
                "connector_name": connector_name,
                "version": version,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    return True


def set_organization_connector_version_override(
    organization_id: str,
    connector_name: str,
    connector_type: Literal["source", "destination"],
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    version: str | None = None,
    unset: bool = False,
    override_reason: str | None = None,
    override_reason_reference_url: str | None = None,
    user_email: str | None = None,
    bearer_token: str | None = None,
) -> bool:
    """Set or clear an organization-level version override for a connector type.

    This pins ALL instances of a connector type across an entire organization to a
    specific version. For example, pinning 'source-github' at organization level means
    all GitHub sources in all workspaces within that organization will use the pinned version.

    Args:
        organization_id: The organization ID
        connector_name: The connector name (e.g., 'source-github')
        connector_type: Either "source" or "destination"
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        version: The version to pin to (e.g., "0.1.0"), or None to unset
        unset: If True, removes any existing override
        override_reason: Required when setting. Explanation for the override
        override_reason_reference_url: Optional URL with more context
        user_email: Email of user creating the override
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        True if operation succeeded, False if no override existed (unset only)

    Raises:
        PyAirbyteInputError: If the API request fails or parameters are invalid
    """
    # Input validation
    if (version is None) == (not unset):
        raise PyAirbyteInputError(
            message="Must specify EXACTLY ONE of version (to set) OR unset=True (to clear), but not both",
        )

    if not unset and (not override_reason or len(override_reason.strip()) < 10):
        raise PyAirbyteInputError(
            message="override_reason is required when setting a version and must be at least 10 characters",
        )

    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    # Resolve connector name to actor_definition_id using the shared registry lookup
    actor_definition_id = _resolve_connector_definition_id(
        connector_name=connector_name,
        connector_type=connector_type,
        config_api_root=config_api_root,
        access_token=access_token,
    )

    if unset:
        # Get the existing organization-level configuration
        active_config = _get_scoped_configuration_context(
            actor_definition_id=actor_definition_id,
            scope_type=_ScopeType.ORGANIZATION,
            scope_id=organization_id,
            config_api_root=config_api_root,
            access_token=access_token,
        )

        if not active_config:
            return False

        # Verify this is actually an organization-scoped config
        api_scope_type = active_config.get("scope_type", "").lower()
        api_scope_id = active_config.get("scope_id", "")
        if (
            api_scope_type != _ScopeType.ORGANIZATION.value
            or api_scope_id != organization_id
        ):
            raise PyAirbyteInputError(
                message=f"Cannot delete: the active config is not organization-scoped. "
                f"Expected scope_type='{_ScopeType.ORGANIZATION.value}' and scope_id='{organization_id}', "
                f"but got scope_type='{api_scope_type}' and scope_id='{api_scope_id}'.",
                context={
                    "organization_id": organization_id,
                    "expected_scope_type": _ScopeType.ORGANIZATION.value,
                    "actual_scope_type": api_scope_type,
                    "actual_scope_id": api_scope_id,
                    "full_config": active_config,
                },
            )

        # Delete the configuration
        delete_endpoint = f"{config_api_root}/scoped_configuration/delete"
        delete_payload = {"scopedConfigurationId": active_config["id"]}

        response = requests.post(
            delete_endpoint,
            json=delete_payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": ops_constants.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )

        if response.status_code not in (200, 204):
            raise PyAirbyteInputError(
                message=f"Failed to delete organization version override: {response.status_code} {response.text}",
                context={
                    "delete_endpoint": delete_endpoint,
                    "config_id": active_config["id"],
                    "status_code": response.status_code,
                    "response": response.text,
                },
            )

        return True

    # Set a new organization-level override
    # Resolve version string to version ID
    version_id = resolve_connector_version_id(
        actor_definition_id=actor_definition_id,
        connector_type=connector_type,
        version=version,
        config_api_root=config_api_root,
        bearer_token=access_token,
    )

    # Check for existing organization-level configuration
    existing_config = _get_scoped_configuration_context(
        actor_definition_id=actor_definition_id,
        scope_type=_ScopeType.ORGANIZATION,
        scope_id=organization_id,
        config_api_root=config_api_root,
        access_token=access_token,
    )

    if existing_config:
        existing_version_id = existing_config.get("value")
        existing_version_name = existing_config.get("value_name", "unknown")

        # If already pinned to the same version, no action needed
        if existing_version_id == version_id:
            raise PyAirbyteInputError(
                message=f"Organization is already pinned to version {existing_version_name} for {connector_name}. "
                f"Use unset=True first if you want to re-pin to a different version.",
                context={
                    "organization_id": organization_id,
                    "connector_name": connector_name,
                    "existing_version": existing_version_name,
                    "requested_version": version,
                },
            )

        # Verify this is an organization-scoped config before deleting
        api_scope_type = existing_config.get("scope_type", "").lower()
        api_scope_id = existing_config.get("scope_id", "")
        if (
            api_scope_type == _ScopeType.ORGANIZATION.value
            and api_scope_id == organization_id
        ):
            # Delete existing organization-level config before creating new one
            delete_endpoint = f"{config_api_root}/scoped_configuration/delete"
            delete_payload = {"scopedConfigurationId": existing_config["id"]}

            delete_response = requests.post(
                delete_endpoint,
                json=delete_payload,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": ops_constants.USER_AGENT,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

            if delete_response.status_code not in (200, 204):
                raise PyAirbyteInputError(
                    message=f"Failed to delete existing organization version override: "
                    f"{delete_response.status_code} {delete_response.text}",
                )

    # Get user ID from email
    if not user_email:
        raise PyAirbyteInputError(
            message="user_email is required to set a version override",
        )
    origin = get_user_id_by_email(
        email=user_email,
        config_api_root=config_api_root,
        bearer_token=access_token,
    )

    # Create the override
    endpoint = f"{config_api_root}/scoped_configuration/create"
    payload: dict[str, Any] = {
        "config_key": _ScopedConfigKey.CONNECTOR_VERSION.value,
        "resource_type": _ResourceType.ACTOR_DEFINITION.value,
        "resource_id": actor_definition_id,
        "scope_type": _ScopeType.ORGANIZATION.value,
        "scope_id": organization_id,
        "value": version_id,
        "description": override_reason,
        "origin_type": _OriginType.USER.value,
        "origin": origin,
    }

    if override_reason_reference_url:
        payload["reference_url"] = override_reason_reference_url

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code not in (200, 201):
        raise PyAirbyteInputError(
            message=f"Failed to set organization version override: {response.status_code} {response.text}",
            context={
                "organization_id": organization_id,
                "connector_name": connector_name,
                "version": version,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    return True


def start_connector_rollout(
    docker_repository: str,
    docker_image_tag: str,
    actor_definition_id: str,
    updated_by: str,
    rollout_strategy: Literal["manual", "automated", "overridden"],
    config_api_root: str,
    initial_rollout_pct: int | None = None,
    final_target_rollout_pct: int | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
    customer_tier: Literal["TIER_0", "TIER_1", "TIER_2", "ALL"] | None = None,
) -> dict[str, Any]:
    """Start a connector rollout workflow.

    This function calls the platform API to start a connector rollout workflow,
    transitioning the rollout from INITIALIZED to WORKFLOW_STARTED state.

    Args:
        docker_repository: The docker repository (e.g., "airbyte/source-github")
        docker_image_tag: The docker image tag (e.g., "1.2.0-rc.2")
        actor_definition_id: The actor definition ID (UUID)
        updated_by: The user ID performing the operation (UUID)
        rollout_strategy: The rollout strategy - "manual", "automated", or "overridden"
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        initial_rollout_pct: Initial/step percentage for rollout progression (0-100).
            For automated rollouts, this is the percentage increment per step.
            Default is 25% if not specified.
        final_target_rollout_pct: Maximum percentage of actors to pin (0-100).
            The rollout will not exceed this percentage. Default is 50% if not specified.
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)
        customer_tier: The customer tier to target for this rollout. One of
            "TIER_0", "TIER_1", "TIER_2", or "ALL". When not specified, the platform
            API defaults to TIER_2. Use "ALL" to target all customer tiers.

    Returns:
        Dictionary containing the API response with the updated rollout data

    Raises:
        PyAirbyteInputError: If the API request fails
    """
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    endpoint = f"{config_api_root}/connector_rollout/manual_start"
    payload: dict[str, Any] = {
        "docker_repository": docker_repository,
        "docker_image_tag": docker_image_tag,
        "actor_definition_id": actor_definition_id,
        "updated_by": updated_by,
        "rollout_strategy": rollout_strategy,
    }

    if initial_rollout_pct is not None:
        payload["initial_rollout_pct"] = initial_rollout_pct
    if final_target_rollout_pct is not None:
        payload["final_target_rollout_pct"] = final_target_rollout_pct
    if customer_tier is not None:
        payload["filters"] = {
            "tierFilter": {
                "tier": customer_tier,
            },
        }

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=60,
    )

    if response.status_code == 404:
        raise PyAirbyteInputError(
            message=f"Rollout not found for {docker_repository}:{docker_image_tag}",
            context={
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "actor_definition_id": actor_definition_id,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    if response.status_code == 422:
        raise PyAirbyteInputError(
            message=f"Invalid input for starting rollout: {response.text}",
            context={
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "actor_definition_id": actor_definition_id,
                "rollout_strategy": rollout_strategy,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to start connector rollout: {response.status_code} {response.text}",
            context={
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "actor_definition_id": actor_definition_id,
                "rollout_strategy": rollout_strategy,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    return response.json()


def progress_connector_rollout(
    docker_repository: str,
    docker_image_tag: str,
    actor_definition_id: str,
    rollout_id: str,
    updated_by: str,
    config_api_root: str,
    target_percentage: int | None = None,
    actor_ids: list[str] | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> dict[str, Any]:
    """Progress a connector rollout by pinning actors to the RC version.

    This function calls the platform API to progress a connector rollout,
    either by specifying a target percentage or specific actor IDs to pin.

    Args:
        docker_repository: The docker repository (e.g., "airbyte/source-github")
        docker_image_tag: The docker image tag (e.g., "1.2.0-rc.2")
        actor_definition_id: The actor definition ID (UUID)
        rollout_id: The rollout ID (UUID)
        updated_by: The user ID performing the operation (UUID)
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        target_percentage: Target percentage of actors to pin (1-100)
        actor_ids: Specific actor IDs to pin (alternative to target_percentage)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        Dictionary containing the API response with the updated rollout data

    Raises:
        PyAirbyteInputError: If the API request fails
    """
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    endpoint = f"{config_api_root}/connector_rollout/manual_rollout"
    payload: dict[str, Any] = {
        "docker_repository": docker_repository,
        "docker_image_tag": docker_image_tag,
        "actor_definition_id": actor_definition_id,
        "id": rollout_id,
        "updated_by": updated_by,
    }

    if target_percentage is not None:
        payload["target_percentage"] = target_percentage
    if actor_ids is not None:
        payload["actor_ids"] = actor_ids

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=60,
    )

    if response.status_code == 404:
        raise PyAirbyteInputError(
            message=f"Rollout not found: {rollout_id}",
            context={
                "rollout_id": rollout_id,
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    if response.status_code == 422:
        raise PyAirbyteInputError(
            message=f"Invalid input for rollout progression: {response.text}",
            context={
                "rollout_id": rollout_id,
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "target_percentage": target_percentage,
                "actor_ids": actor_ids,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to progress connector rollout: {response.status_code} {response.text}",
            context={
                "rollout_id": rollout_id,
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "target_percentage": target_percentage,
                "actor_ids": actor_ids,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    return response.json()


def finalize_connector_rollout(
    docker_repository: str,
    docker_image_tag: str,
    actor_definition_id: str,
    rollout_id: str,
    updated_by: str,
    state: Literal["succeeded", "failed_rolled_back", "canceled"],
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
    error_msg: str | None = None,
    failed_reason: str | None = None,
    retain_pins_on_cancellation: bool | None = None,
) -> dict[str, Any]:
    """Finalize a connector rollout by promoting, rolling back, or canceling.

    This function calls the platform API to finalize a connector rollout.

    Args:
        docker_repository: The docker repository (e.g., "airbyte/source-github")
        docker_image_tag: The docker image tag (e.g., "1.2.0-rc.2")
        actor_definition_id: The actor definition ID (UUID)
        rollout_id: The rollout ID (UUID)
        updated_by: The user ID performing the operation (UUID)
        state: The final state - "succeeded" (promote), "failed_rolled_back" (rollback),
            or "canceled" (cancel)
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)
        error_msg: Optional error message (for failed/canceled states)
        failed_reason: Optional failure reason (for failed/canceled states)
        retain_pins_on_cancellation: If True, retain version pins when canceling

    Returns:
        Dictionary containing the API response with status field

    Raises:
        PyAirbyteInputError: If the API request fails
    """
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    endpoint = f"{config_api_root}/connector_rollout/manual_finalize"
    payload: dict[str, Any] = {
        "docker_repository": docker_repository,
        "docker_image_tag": docker_image_tag,
        "actor_definition_id": actor_definition_id,
        "id": rollout_id,
        "updated_by": updated_by,
        "state": state,
    }

    if error_msg:
        payload["error_msg"] = error_msg
    if failed_reason:
        payload["failed_reason"] = failed_reason
    if retain_pins_on_cancellation is not None:
        payload["retain_pins_on_cancellation"] = retain_pins_on_cancellation

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=60,
    )

    if response.status_code == 404:
        raise PyAirbyteInputError(
            message=f"Rollout not found: {rollout_id}",
            context={
                "rollout_id": rollout_id,
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    if response.status_code == 422:
        raise PyAirbyteInputError(
            message=f"Invalid input for rollout finalization: {response.text}",
            context={
                "rollout_id": rollout_id,
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "state": state,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to finalize connector rollout: {response.status_code} {response.text}",
            context={
                "rollout_id": rollout_id,
                "docker_repository": docker_repository,
                "docker_image_tag": docker_image_tag,
                "state": state,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    return response.json()


def get_actor_sync_info(
    rollout_id: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> dict[str, Any]:
    """Get actor sync info for a connector rollout.

    This function calls the platform API to get sync statistics for actors
    participating in a rollout. Unlike the SQL-based approach, this endpoint
    filters sync stats to only include syncs that actually used the RC version
    associated with the rollout.

    Args:
        rollout_id: The rollout ID (UUID)
        config_api_root: The Config API root URL (e.g., CLOUD_CONFIG_API_ROOT)
        client_id: The Airbyte Cloud client ID (required if no bearer_token)
        client_secret: The Airbyte Cloud client secret (required if no bearer_token)
        bearer_token: Pre-existing bearer token (takes precedence over client credentials)

    Returns:
        Dictionary containing:
        - data.actorSelectionInfo: Info about actor selection (numActors, numPinnedToConnectorRollout, etc.)
        - data.syncs: Dict mapping actor_id to sync stats (numConnections, numSucceeded, numFailed)

    Raises:
        PyAirbyteInputError: If the API request fails or rollout not found
    """
    access_token = _get_access_token(
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
        config_api_root=config_api_root,
    )

    endpoint = f"{config_api_root}/connector_rollout/get_actor_sync_info"
    payload = {"id": rollout_id}

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": ops_constants.USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=60,
    )

    if response.status_code == 404:
        raise PyAirbyteInputError(
            message=f"Rollout not found: {rollout_id}",
            context={
                "rollout_id": rollout_id,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    if response.status_code != 200:
        raise PyAirbyteInputError(
            message=f"Failed to get actor sync info: {response.status_code} {response.text}",
            context={
                "rollout_id": rollout_id,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.text,
            },
        )

    return response.json()
