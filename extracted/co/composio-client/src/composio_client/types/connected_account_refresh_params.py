# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_refresh_params."""

from __future__ import annotations

from typing import Annotated

from typing_extensions import TypedDict
from .._types import PropertyInfo


class ConnectedAccountRefreshParams(TypedDict, total=False):
    query_redirect_url: Annotated[str, PropertyInfo(alias='redirect_url')]
    body_redirect_url: Annotated[str, PropertyInfo(alias='redirect_url')]
    validate_credentials: bool
    "[EXPERIMENTAL] Whether to validate the provided credentials, validates only for\nAPI Key Auth scheme"


__all__ = [
    "ConnectedAccountRefreshParams",
]
