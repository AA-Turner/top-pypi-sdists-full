# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.custom_update_toolkits_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, Required, TypedDict


class LogoFile(TypedDict, total=False):
    "Square PNG or JPEG logo, 256-1024px, max 3MB. Omit to keep the current logo."

    content: Required[str]
    "Base64-encoded image, max 3MB decoded"
    mime_type: Required[Literal["image/png", "image/jpeg"]]
    "Image MIME type"


class ApiKeyField(TypedDict, total=False):
    "Label and help text for the API key input on the connect page. API_KEY toolkits only."

    display_name: NotRequired[str]
    "Label for the API key input"
    description: NotRequired[str]
    "Help text below the API key input"


class CustomUpdateToolkitsParams(TypedDict, total=False):
    name: NotRequired[str]
    logo_file: NotRequired[LogoFile]
    api_key_field: NotRequired[ApiKeyField]
    user_id: NotRequired[str]


__all__ = [
    "CustomUpdateToolkitsParams",
    "LogoFile",
    "ApiKeyField",
]
