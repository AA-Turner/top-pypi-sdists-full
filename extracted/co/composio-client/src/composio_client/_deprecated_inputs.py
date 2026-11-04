# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Deprecated caller-facing inputs, generated from the committed spec.

Read by ``_base_client._prepare``, which warns before dispatch when a
deprecated wire name is present in the merged query or the mapped body —
no response required, unlike ``_deprecation.inspect_deprecation``.

``param`` is the disambiguated keyword the method signature actually
accepts (``query_show_disabled_2`` where two deprecated flat params
collide after snake_casing), read off the same ``flatParams`` the resource
method is rendered from — so this table can never name a keyword the
method does not have.
"""

from __future__ import annotations

from typing import NamedTuple


class DeprecatedInput(NamedTuple):
    wire: str
    location: str
    param: str
    replacement_wire: str | None
    replacement_param: str | None


DEPRECATED_INPUTS: dict[tuple[str, ...], tuple[DeprecatedInput, ...]] = {
    ("auth_configs", "list"): (
        DeprecatedInput("deprecated_app_id", "query", "deprecated_app_id", "toolkit_slug", "toolkit_slug"),
        DeprecatedInput("deprecated_status", "query", "deprecated_status", None, None),
    ),
    ("toolkits", "list"): (DeprecatedInput("managed_by", "query", "managed_by", None, None),),
    ("tools", "list"): (
        DeprecatedInput("auth_config_ids", "query", "auth_config_ids", None, None),
        DeprecatedInput("search", "query", "search", "query", "query"),
    ),
    ("trigger_instances", "list_active"): (
        DeprecatedInput(
            "connectedAccountIds",
            "query",
            "query_connected_account_ids_2",
            "connected_account_ids",
            "query_connected_account_ids_1",
        ),
        DeprecatedInput(
            "authConfigIds",
            "query",
            "query_auth_config_ids_2",
            "auth_config_ids",
            "query_auth_config_ids_1",
        ),
        DeprecatedInput("triggerIds", "query", "query_trigger_ids_2", "trigger_ids", "query_trigger_ids_1"),
        DeprecatedInput(
            "triggerNames",
            "query",
            "query_trigger_names_2",
            "trigger_names",
            "query_trigger_names_1",
        ),
        DeprecatedInput(
            "showDisabled",
            "query",
            "query_show_disabled_2",
            "show_disabled",
            "query_show_disabled_1",
        ),
        DeprecatedInput(
            "deprecatedConnectedAccountUuids",
            "query",
            "deprecated_connected_account_uuids",
            "connected_account_ids",
            "query_connected_account_ids_1",
        ),
        DeprecatedInput(
            "deprecatedAuthConfigUuids",
            "query",
            "deprecated_auth_config_uuids",
            "auth_config_ids",
            "query_auth_config_ids_1",
        ),
    ),
    ("auth_configs", "update"): (
        DeprecatedInput("restrict_to_following_tools", "body", "restrict_to_following_tools", None, None),
        DeprecatedInput("tool_access_config", "body", "tool_access_config", None, None),
        DeprecatedInput("shared_credentials", "body", "shared_credentials", None, None),
    ),
    ("mcp", "generate", "url"): (
        DeprecatedInput("managed_auth_by_composio", "body", "managed_auth_by_composio", None, None),
    ),
    ("tool_router", "session", "proxy_execute"): (
        DeprecatedInput("custom_connection_data", "body", "custom_connection_data", None, None),
    ),
    ("tools", "proxy"): (
        DeprecatedInput("custom_connection_data", "body", "custom_connection_data", None, None),
    ),
    ("tools", "execute"): (
        DeprecatedInput("entity_id", "body", "entity_id", "user_id", "user_id"),
        DeprecatedInput("allow_tracing", "body", "allow_tracing", None, None),
    ),
    ("trigger_instances", "upsert"): (
        DeprecatedInput(
            "connectedAuthId",
            "body",
            "connected_auth_id",
            "connected_account_id",
            "connected_account_id",
        ),
        DeprecatedInput(
            "triggerConfig",
            "body",
            "body_trigger_config_2",
            "trigger_config",
            "body_trigger_config_1",
        ),
        DeprecatedInput("version", "body", "version", "toolkit_versions", "toolkit_versions"),
    ),
}
