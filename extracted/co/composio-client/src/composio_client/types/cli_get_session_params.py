# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.cli_get_session_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class CliGetSessionParams(TypedDict, total=False):
    id: Required[str]
    "CLI session ID (UUID format) or 6-character code to check.\n\nBoth formats are supported for flexibility in client implementations."


__all__ = [
    "CliGetSessionParams",
]
