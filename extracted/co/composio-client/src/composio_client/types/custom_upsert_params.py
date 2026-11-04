# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.custom_upsert_params."""

from __future__ import annotations

from typing import Iterable, Literal

from typing_extensions import NotRequired, Required, TypedDict


class ToolkitConfigLogoFile(TypedDict, total=False):
    "Square PNG or JPEG logo, 256-1024px, max 3MB. Defaults to the Model Context Protocol logo."

    content: Required[str]
    "Base64-encoded image, max 3MB decoded"
    mime_type: Required[Literal["image/png", "image/jpeg"]]
    "Image MIME type"


class ToolkitConfigAuthSchemeVariant0(TypedDict, total=False):
    mode: Required[Literal["NO_AUTH"]]


class ToolkitConfigAuthSchemeVariant1ApiKeyField(TypedDict, total=False):
    "Label and help text for the API key input on the connect page"

    display_name: NotRequired[str]
    "Label for the API key input"
    description: NotRequired[str]
    "Help text below the API key input"


class ToolkitConfigAuthSchemeVariant1AdditionalFieldsGenericId(TypedDict, total=False):
    display_name: Required[str]
    "Label shown to the user connecting their account"
    description: NotRequired[str]
    "Help text below the input"


class ToolkitConfigAuthSchemeVariant1AdditionalFields(TypedDict, total=False):
    "Additional values each user enters when connecting. Reference each field in a header, for example X-Org-Id: {{generic_id}}. Use display_name for the user-facing label. Every user must supply each declared field. Values are not secret."

    generic_id: Required[ToolkitConfigAuthSchemeVariant1AdditionalFieldsGenericId]


class ToolkitConfigAuthSchemeVariant1(TypedDict, total=False):
    mode: Required[Literal["API_KEY"]]
    headers: Required[dict[str, str]]
    "Headers sent to the MCP server. Use {{generic_api_key}} where the API key goes."
    api_key_field: NotRequired[ToolkitConfigAuthSchemeVariant1ApiKeyField]
    "Label and help text for the API key input on the connect page"
    additional_fields: NotRequired[ToolkitConfigAuthSchemeVariant1AdditionalFields]
    "Additional values each user enters when connecting. Reference each field in a header, for example X-Org-Id: {{generic_id}}. Use display_name for the user-facing label. Every user must supply each declared field. Values are not secret."


class ToolkitConfigAuthSchemeVariant2(TypedDict, total=False):
    mode: Required[Literal["DCR_OAUTH"]]
    discovery_url: Required[str]
    "OAuth authorization server metadata URL, for example https://<auth server host>/.well-known/oauth-authorization-server. Use the URL your authorization server publishes; it can be on a different host from the MCP server or include a path."


class ToolkitConfig(TypedDict, total=False):
    name: Required[str]
    "Display name of the toolkit"
    app_url: Required[str]
    "MCP server URL. Must use https."
    logo_file: NotRequired[ToolkitConfigLogoFile]
    "Square PNG or JPEG logo, 256-1024px, max 3MB. Defaults to the Model Context Protocol logo."
    auth_schemes: Required[Iterable[ToolkitConfigAuthSchemeVariant0 | ToolkitConfigAuthSchemeVariant1 | ToolkitConfigAuthSchemeVariant2]]
    "How users authenticate to the MCP server"


class CustomUpsertParams(TypedDict, total=False):
    slug: Required[str]
    toolkit_config: Required[ToolkitConfig]


__all__ = [
    "CustomUpsertParams",
    "ToolkitConfigLogoFile",
    "ToolkitConfigAuthSchemeVariant0",
    "ToolkitConfigAuthSchemeVariant1ApiKeyField",
    "ToolkitConfigAuthSchemeVariant1AdditionalFieldsGenericId",
    "ToolkitConfigAuthSchemeVariant1AdditionalFields",
    "ToolkitConfigAuthSchemeVariant1",
    "ToolkitConfigAuthSchemeVariant2",
    "ToolkitConfig",
]
