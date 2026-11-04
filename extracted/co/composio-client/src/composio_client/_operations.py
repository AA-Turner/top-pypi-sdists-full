# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""The operations this client publishes, as the runtime knows them.

Read by two collaborators that both need to recognize a dispatched request:
``_deprecation.match_operation``, which names the accessor a notice belongs
to, and ``_base_client._credential_source``, which under ``AutoAuth`` asks
``_credentials.select_scheme`` which credential header the request carries
(a fixed ``auth`` mode never reads the table).

``schemes`` is present only where it is *not* the ``ApiKeyAuth`` default, so
the table reads as a list of exceptions. A row without it, and a path that
matches no row at all, both mean the same thing to ``AutoAuth`` — send the
project key — which is what an escape-hatch ``client.get()`` needs.
"""

from __future__ import annotations

from typing import NamedTuple


class Operation(NamedTuple):
    """One operation as the runtime knows it.

    ``path`` is the *un-substituted* template and ``chain`` the public client
    path it is callable at, so a dispatched request can be traced back to the
    accessor the caller actually wrote.
    """

    method: str
    path: str
    chain: tuple[str, ...]
    #: The operation's declared security schemes, verbatim from the spec, and
    #: present only where they are not the ``("ApiKeyAuth",)`` default.
    schemes: tuple[str, ...] | None = None


OPERATIONS: tuple[Operation, ...] = (
    Operation(
        "delete",
        "/api/v3.1/auth_configs/{nanoid}",
        ("auth_configs", "delete"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "delete",
        "/api/v3.1/connected_accounts/{nanoid}",
        ("connected_accounts", "delete"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "delete",
        "/api/v3.1/custom/toolkits/{slug}",
        ("custom", "delete_toolkit"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "delete",
        "/api/v3.1/mcp/servers/{serverId}/instances/{instanceId}",
        ("mcp", "delete_instance"),
    ),
    Operation("delete", "/api/v3.1/mcp/{id}", ("mcp", "delete")),
    Operation(
        "delete",
        "/api/v3.1/org/owner/project/{nano_id}",
        ("org", "owner", "project", "delete"),
        schemes=("OrgApiKeyAuth",),
    ),
    Operation("delete", "/api/v3.1/tool_router/session/{session_id}", ("tool_router", "session", "delete")),
    Operation(
        "delete",
        "/api/v3.1/trigger_instances/manage/{triggerId}",
        ("trigger_instances", "manage", "delete"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("delete", "/api/v3.1/webhook_subscriptions/{id}", ("webhook_subscriptions", "delete")),
    Operation(
        "get",
        "/api/v3.1/auth/session/info",
        ("auth", "session", "retrieve_info"),
        schemes=("UserApiKeyAuth",),
    ),
    Operation(
        "get",
        "/api/v3.1/auth_configs",
        ("auth_configs", "list"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "get",
        "/api/v3.1/auth_configs/{nanoid}",
        ("auth_configs", "retrieve"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("get", "/api/v3.1/cli/get-session", ("_internal", "cli", "get_session"), schemes=("no_auth",)),
    Operation(
        "get",
        "/api/v3.1/cli/realtime/credentials",
        ("_internal", "cli", "realtime", "credentials"),
        schemes=("UserApiKeyAuth",),
    ),
    Operation(
        "get",
        "/api/v3.1/connected_accounts",
        ("connected_accounts", "list"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "get",
        "/api/v3.1/connected_accounts/{nanoid}",
        ("connected_accounts", "retrieve"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("get", "/api/v3.1/files/list", ("files", "list")),
    Operation(
        "get",
        "/api/v3.1/internal/action_execution/fields",
        ("_internal", "logs", "tools", "list_fields"),
    ),
    Operation(
        "get",
        "/api/v3.1/internal/action_execution/log/{id}",
        ("_internal", "logs", "tools", "retrieve"),
    ),
    Operation("get", "/api/v3.1/internal/trigger/log/{id}", ("_internal", "logs", "triggers", "retrieve")),
    Operation("get", "/api/v3.1/keyring/transfer_keys", ("keyring", "list_transfer_keys")),
    Operation("get", "/api/v3.1/logs/tool_execution/{id}", ("logs", "retrieve_tool_execution")),
    Operation("get", "/api/v3.1/mcp/app/{appKey}", ("mcp", "retrieve_app")),
    Operation("get", "/api/v3.1/mcp/servers", ("mcp", "list")),
    Operation("get", "/api/v3.1/mcp/servers/{serverId}/instances", ("mcp", "list_instances")),
    Operation("get", "/api/v3.1/mcp/{id}", ("mcp", "retrieve")),
    Operation(
        "get",
        "/api/v3.1/org/consumer/config",
        ("_internal", "org", "consumer", "retrieve_config"),
        schemes=("UserApiKeyAuth",),
    ),
    Operation(
        "get",
        "/api/v3.1/org/consumer/connected_toolkits",
        ("_internal", "org", "consumer", "list_connected_toolkits"),
        schemes=("UserApiKeyAuth",),
    ),
    Operation("get", "/api/v3.1/org/list", ("org", "list"), schemes=("UserApiKeyAuth",)),
    Operation(
        "get",
        "/api/v3.1/org/owner/project/list",
        ("org", "owner", "project", "list"),
        schemes=("OrgApiKeyAuth",),
    ),
    Operation(
        "get",
        "/api/v3.1/org/owner/project/{nano_id}",
        ("org", "owner", "project", "retrieve"),
        schemes=("OrgApiKeyAuth",),
    ),
    Operation("get", "/api/v3.1/org/project/list", ("org", "project", "list"), schemes=("UserApiKeyAuth",)),
    Operation("get", "/api/v3.1/session_configs", ("session_configs", "list")),
    Operation("get", "/api/v3.1/session_configs/{session_config_id}", ("session_configs", "retrieve")),
    Operation("get", "/api/v3.1/tool_router/session/{session_id}", ("tool_router", "session", "retrieve")),
    Operation(
        "get",
        "/api/v3.1/tool_router/session/{session_id}/config_history",
        ("tool_router", "session", "config_history"),
    ),
    Operation(
        "get",
        "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/items",
        ("tool_router", "session", "files", "list"),
    ),
    Operation(
        "get",
        "/api/v3.1/tool_router/session/{session_id}/toolkits",
        ("tool_router", "session", "toolkits"),
    ),
    Operation("get", "/api/v3.1/tool_router/session/{session_id}/tools", ("tool_router", "session", "tools")),
    Operation("get", "/api/v3.1/toolkits", ("toolkits", "list"), schemes=("ApiKeyAuth", "UserApiKeyAuth")),
    Operation("get", "/api/v3.1/toolkits/categories", ("toolkits", "retrieve_categories")),
    Operation("get", "/api/v3.1/toolkits/changelog", ("toolkits", "retrieve_changelog")),
    Operation(
        "get",
        "/api/v3.1/toolkits/{slug}",
        ("toolkits", "retrieve"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "get",
        "/api/v3.1/toolkits/{toolkit_slug}/scopes/grant_context",
        ("toolkits", "retrieve_scopes_grant_context"),
    ),
    Operation("get", "/api/v3.1/tools", ("tools", "list"), schemes=("ApiKeyAuth", "UserApiKeyAuth")),
    Operation(
        "get",
        "/api/v3.1/tools/enum",
        ("tools", "retrieve_enum"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "get",
        "/api/v3.1/tools/{tool_slug}",
        ("tools", "retrieve"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "get",
        "/api/v3.1/trigger_instances/active",
        ("trigger_instances", "list_active"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "get",
        "/api/v3.1/triggers_types",
        ("triggers_types", "list"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "get",
        "/api/v3.1/triggers_types/list/enum",
        ("triggers_types", "retrieve_enum"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "get",
        "/api/v3.1/triggers_types/{slug}",
        ("triggers_types", "retrieve"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("get", "/api/v3.1/webhook_endpoints", ("webhook_endpoints", "list")),
    Operation("get", "/api/v3.1/webhook_endpoints/{nano_id}", ("webhook_endpoints", "retrieve")),
    Operation("get", "/api/v3.1/webhook_subscriptions", ("webhook_subscriptions", "list")),
    Operation(
        "get",
        "/api/v3.1/webhook_subscriptions/event_types",
        ("webhook_subscriptions", "list_event_types"),
    ),
    Operation("get", "/api/v3.1/webhook_subscriptions/{id}", ("webhook_subscriptions", "retrieve")),
    Operation(
        "patch",
        "/api/v3.1/auth_configs/{nanoid}",
        ("auth_configs", "update"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("patch", "/api/v3.1/auth_configs/{nanoid}/{status}", ("auth_configs", "update_status")),
    Operation(
        "patch",
        "/api/v3.1/connected_accounts/{nanoId}/status",
        ("connected_accounts", "update_status"),
    ),
    Operation("patch", "/api/v3.1/connected_accounts/{nanoid}", ("connected_accounts", "patch")),
    Operation(
        "patch",
        "/api/v3.1/custom/toolkits/{slug}",
        ("custom", "update_toolkits"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("patch", "/api/v3.1/mcp/{id}", ("mcp", "update")),
    Operation("patch", "/api/v3.1/tool_router/session/{session_id}", ("tool_router", "session", "patch")),
    Operation(
        "patch",
        "/api/v3.1/trigger_instances/manage/{triggerId}",
        ("trigger_instances", "manage", "update"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("patch", "/api/v3.1/webhook_endpoints/{nano_id}", ("webhook_endpoints", "update")),
    Operation("patch", "/api/v3.1/webhook_subscriptions/{id}", ("webhook_subscriptions", "update")),
    Operation("post", "/api/v3.1/api_key_revocation", ("api_key_revocation", "create"), schemes=("no_auth",)),
    Operation(
        "post",
        "/api/v3.1/auth_configs",
        ("auth_configs", "create"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "post",
        "/api/v3.1/cli/codact_failures",
        ("_internal", "cli", "create_codact_failure"),
        schemes=("UserApiKeyAuth",),
    ),
    Operation(
        "post",
        "/api/v3.1/cli/create-session",
        ("_internal", "cli", "create_session"),
        schemes=("no_auth",),
    ),
    Operation(
        "post",
        "/api/v3.1/cli/realtime/auth",
        ("_internal", "cli", "realtime", "auth"),
        schemes=("UserApiKeyAuth",),
    ),
    Operation("post", "/api/v3.1/connected_accounts", ("connected_accounts", "create")),
    Operation("post", "/api/v3.1/connected_accounts/complete_auth", ("connected_accounts", "complete_auth")),
    Operation(
        "post",
        "/api/v3.1/connected_accounts/link",
        ("link", "create"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("post", "/api/v3.1/connected_accounts/{nanoid}/refresh", ("connected_accounts", "refresh")),
    Operation("post", "/api/v3.1/connected_accounts/{nanoid}/revoke", ("connected_accounts", "revoke")),
    Operation(
        "post",
        "/api/v3.1/consumer/permissions/resolve",
        ("_internal", "consumer", "permissions", "resolve"),
        schemes=("UserApiKeyAuth", "ApiKeyAuth"),
    ),
    Operation(
        "post",
        "/api/v3.1/custom/toolkits",
        ("custom", "create_toolkit"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "post",
        "/api/v3.1/custom/toolkits/sync",
        ("custom", "sync"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "post",
        "/api/v3.1/custom/toolkits/upsert",
        ("custom", "upsert"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("post", "/api/v3.1/files/upload/request", ("files", "create_presigned_url")),
    Operation("post", "/api/v3.1/internal/action_execution/logs", ("_internal", "logs", "tools", "list")),
    Operation("post", "/api/v3.1/internal/trigger/logs", ("_internal", "logs", "triggers", "list")),
    Operation("post", "/api/v3.1/logs/tool_execution", ("logs", "create_tool_execution")),
    Operation("post", "/api/v3.1/mcp/servers", ("mcp", "create")),
    Operation("post", "/api/v3.1/mcp/servers/custom", ("mcp", "custom", "create")),
    Operation("post", "/api/v3.1/mcp/servers/generate", ("mcp", "generate", "url")),
    Operation("post", "/api/v3.1/mcp/servers/{serverId}/instances", ("mcp", "create_instance")),
    Operation(
        "post",
        "/api/v3.1/org/consumer/project/resolve",
        ("_internal", "org", "consumer", "project", "resolve"),
        schemes=("UserApiKeyAuth",),
    ),
    Operation(
        "post",
        "/api/v3.1/org/owner/project/new",
        ("org", "owner", "project", "create"),
        schemes=("OrgApiKeyAuth",),
    ),
    Operation(
        "post",
        "/api/v3.1/org/owner/project/{nano_id}/regenerate_api_key",
        ("org", "owner", "project", "regenerate_api_key"),
        schemes=("OrgApiKeyAuth",),
    ),
    Operation(
        "post",
        "/api/v3.1/org/usage/summary",
        ("org", "usage", "retrieve_summary"),
        schemes=("OrgApiKeyAuth",),
    ),
    Operation(
        "post",
        "/api/v3.1/org/usage/{entity_type}",
        ("org", "usage", "retrieve"),
        schemes=("OrgApiKeyAuth",),
    ),
    Operation("post", "/api/v3.1/project/usage/summary", ("project", "usage", "retrieve_summary")),
    Operation("post", "/api/v3.1/project/usage/{entity_type}", ("project", "usage", "retrieve")),
    Operation("post", "/api/v3.1/tool_router/session", ("tool_router", "session", "create")),
    Operation(
        "post",
        "/api/v3.1/tool_router/session/{session_id}/attach",
        ("tool_router", "session", "attach"),
    ),
    Operation(
        "post",
        "/api/v3.1/tool_router/session/{session_id}/execute",
        ("tool_router", "session", "execute"),
    ),
    Operation(
        "post",
        "/api/v3.1/tool_router/session/{session_id}/execute_meta",
        ("tool_router", "session", "execute_meta"),
    ),
    Operation("post", "/api/v3.1/tool_router/session/{session_id}/link", ("tool_router", "session", "link")),
    Operation(
        "post",
        "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/delete",
        ("tool_router", "session", "files", "delete"),
    ),
    Operation(
        "post",
        "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/download_url",
        ("tool_router", "session", "files", "create_download_url"),
    ),
    Operation(
        "post",
        "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/upload_url",
        ("tool_router", "session", "files", "create_upload_url"),
    ),
    Operation(
        "post",
        "/api/v3.1/tool_router/session/{session_id}/proxy_execute",
        ("tool_router", "session", "proxy_execute"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation(
        "post",
        "/api/v3.1/tool_router/session/{session_id}/search",
        ("tool_router", "session", "search"),
    ),
    Operation("post", "/api/v3.1/toolkits/multi", ("toolkits", "retrieve_multi")),
    Operation(
        "post",
        "/api/v3.1/toolkits/{toolkit_slug}/scopes/recommended",
        ("toolkits", "recommend_scopes"),
    ),
    Operation("post", "/api/v3.1/tools/execute/proxy", ("tools", "proxy")),
    Operation(
        "post",
        "/api/v3.1/tools/execute/{tool_slug}",
        ("tools", "execute"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("post", "/api/v3.1/tools/execute/{tool_slug}/input", ("tools", "get_input")),
    Operation("post", "/api/v3.1/tools/scopes/required", ("tools", "retrieve_required_scopes")),
    Operation(
        "post",
        "/api/v3.1/trigger_instances/{slug}/upsert",
        ("trigger_instances", "upsert"),
        schemes=("ApiKeyAuth", "UserApiKeyAuth"),
    ),
    Operation("post", "/api/v3.1/webhook_endpoints", ("webhook_endpoints", "create")),
    Operation("post", "/api/v3.1/webhook_endpoints/{nano_id}", ("webhook_endpoints", "replace")),
    Operation("post", "/api/v3.1/webhook_subscriptions", ("webhook_subscriptions", "create")),
    Operation(
        "post",
        "/api/v3.1/webhook_subscriptions/{id}/rotate_secret",
        ("webhook_subscriptions", "rotate_secret"),
    ),
)


OPERATIONS_BY_CHAIN: dict[tuple[str, ...], Operation] = {
    operation.chain: operation for operation in OPERATIONS
}
