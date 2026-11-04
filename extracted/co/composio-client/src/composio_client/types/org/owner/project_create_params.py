# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.org.owner.project_create_params."""

from __future__ import annotations

from typing import Iterable, Literal

from typing_extensions import NotRequired, Required, TypedDict
from ...._types import SequenceNotStr


class ApiKeyPermission(TypedDict, total=False):
    preset: Required[Literal["tools", "tool_execution", "proxy_execute", "session_management", "session_tool_execution", "legacy_mcp", "connected_accounts", "auth_configs", "toolkits", "triggers", "webhooks", "observability", "sessions"]]
    access: Required[Literal["none", "read", "write", "read_write"]]


class Config(TypedDict, total=False):
    "Configuration for the project. Use zdr_enabled for Zero Data Retention; log_visibility_setting remains supported for existing clients. Do not send both fields."

    is_2FA_enabled: NotRequired[bool]
    logo_url: NotRequired[str]
    display_name: NotRequired[str]
    mask_secret_keys_in_connected_account: NotRequired[bool]
    log_visibility_setting: NotRequired[Literal["show_all", "dont_store_data"]]
    is_composio_link_enabled_for_managed_auth: NotRequired[bool]
    "Whether to enable composio link for managed authentication. This key will be deprecated in the future. Please don't use this key."
    signed_url_file_expiry_in_seconds: NotRequired[float]
    oauth_callback_verifier_url: NotRequired[str | None]
    "Developer-hosted OAuth callback verifier URL. Setting it enables per-user callback identity verification; null disables it. Must be https and pass SSRF checks."
    theme: NotRequired[dict[str, object | None]]
    "Link-auth theme for the hosted connect page. Opaque to the API; the dashboard owns the token vocabulary and all value validation."
    enable_instant: NotRequired[bool]
    "Enable Instant Toolkits for this project."
    zdr_enabled: NotRequired[bool]
    "Enable Zero Data Retention for the new project. Hobby cannot enable it. Enterprise defaults to enabled; other paid plans default to disabled. An explicit value overrides the default."


class ProjectCreateParams(TypedDict, total=False):
    name: Required[str]
    should_create_api_key: NotRequired[bool]
    api_key_allowed_ips: NotRequired[SequenceNotStr[str]]
    api_key_permissions: NotRequired[Iterable[ApiKeyPermission]]
    config: NotRequired[Config]


__all__ = [
    "ProjectCreateParams",
    "ApiKeyPermission",
    "Config",
]
