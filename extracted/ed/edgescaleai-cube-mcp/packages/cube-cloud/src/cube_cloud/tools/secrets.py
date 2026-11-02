"""Secret management tools."""

from __future__ import annotations

import json

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_common import apollo_queries as Q

from cube_cloud.tools.environments import _resolve_environment


async def _find_entity(client: ApolloClient, env_id: str, entity_name: str) -> dict:
    """Find an entity by name in an environment. Raises ApolloError if not found."""
    data = await client.graphql(Q.ENTITY_SECRETS, {"id": env_id})
    entities = (
        data.get("apollo", {})
        .get("environmentById", {})
        .get("entities", {})
        .get("entities", [])
    )

    search = entity_name.lower()
    matched = [
        e for e in entities
        if search in (e.get("displayName") or "").lower()
        or search in ((e.get("entityLocator") or {}).get("entityName") or "").lower()
    ]

    if len(matched) == 1:
        return matched[0]
    elif len(matched) == 0:
        names = [
            e.get("displayName") or (e.get("entityLocator") or {}).get("entityName", "?")
            for e in entities
        ]
        raise ApolloError(
            f"Entity '{entity_name}' not found.\n"
            f"Available entities:\n" + "\n".join(f"  - {n}" for n in names)
        )
    else:
        # Try exact match
        exact = [
            e for e in matched
            if (e.get("displayName") or "").lower() == search
            or ((e.get("entityLocator") or {}).get("entityName") or "").lower() == search
        ]
        if len(exact) == 1:
            return exact[0]
        names = [e.get("displayName") or "?" for e in matched]
        raise ApolloError(
            f"Multiple entities match '{entity_name}':\n"
            + "\n".join(f"  - {n}" for n in names)
            + "\n\nPlease be more specific."
        )


async def create_secret(
    client: ApolloClient,
    environment: str,
    entity_name: str,
    secret_name: str,
    secret_value: str | None = None,
    secret_keys: str | None = None,
    description: str | None = None,
) -> str:
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    entity = await _find_entity(client, env_id, entity_name)
    entity_id = entity["id"]
    entity_display = (
        entity.get("displayName")
        or (entity.get("entityLocator") or {}).get("entityName", "?")
    )

    # Build the target specification — Apollo secrets are always multikey
    if secret_keys:
        try:
            keys_dict = json.loads(secret_keys)
        except json.JSONDecodeError as e:
            # NOT echoed: every value in this payload is raw secret material by
            # definition. Worse, `scrub_secrets` could not save it — the captured
            # value is the whole string while the response held a 200-char PREFIX,
            # so substring replacement never matched, and it reached the agent
            # transcript and the S3 archive intact.
            return f"Error: secret_keys must be valid JSON ({e})."
        raw_values = [{"key": k, "rawValue": v} for k, v in keys_dict.items()]
    elif secret_value:
        raw_values = [{"key": secret_name, "rawValue": secret_value}]
    else:
        return "Error: Either secret_value or secret_keys must be provided."

    target_spec = {"multiValue": {"rawValues": raw_values}}

    secret_input = {
        "name": secret_name,
        "description": description or secret_name,
        "targetSpecification": target_spec,
    }

    data = await client.graphql(
        Q.CREATE_SECRET,
        {"entityId": entity_id, "secrets": [secret_input]},
    )
    rids = data.get("apollo", {}).get("createSecrets", [])

    return (
        f"Secret created on {env_name}\n"
        f"  Entity: {entity_display}\n"
        f"  Name:   {secret_name}\n"
        f"  RID:    {rids[0] if rids else '(unknown)'}"
    )


async def update_secret(
    client: ApolloClient,
    environment: str,
    entity_name: str,
    secret_name: str,
    secret_value: str | None = None,
    secret_key: str | None = None,
    secret_key_value: str | None = None,
    description: str | None = None,
) -> str:
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    entity = await _find_entity(client, env_id, entity_name)
    entity_id = entity["id"]
    entity_display = (
        entity.get("displayName")
        or (entity.get("entityLocator") or {}).get("entityName", "?")
    )

    # Verify the secret exists on this entity
    secrets = entity.get("secrets", [])
    secret = None
    for s in secrets:
        if s.get("name", "").lower() == secret_name.lower():
            secret = s
            break

    if not secret:
        secret_names = [s.get("name", "?") for s in secrets]
        return (
            f"Secret '{secret_name}' not found on {entity_display}.\n"
            f"Available secrets: {', '.join(secret_names) if secret_names else '(none)'}"
        )

    # Build the update request — all secrets are multikey in Apollo
    if secret_key and secret_key_value:
        request = {"multikeySetKey": {"key": secret_key, "value": secret_key_value}}
    elif secret_value:
        # Single-value update: set the key matching the secret name
        request = {"multikeySetKey": {"key": secret_name, "value": secret_value}}
    elif description:
        request = {"updateDescription": {"description": description}}
    else:
        return "Error: Provide secret_value, secret_key+secret_key_value, or description."

    secret_update = {
        "name": secret_name,
        "request": request,
    }

    await client.graphql(
        Q.UPDATE_SECRET,
        {"entityId": entity_id, "secrets": [secret_update]},
    )

    return (
        f"Secret updated on {env_name}\n"
        f"  Entity: {entity_display}\n"
        f"  Name:   {secret_name}"
    )
