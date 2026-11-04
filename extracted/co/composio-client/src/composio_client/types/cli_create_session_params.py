# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.cli_create_session_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import TypedDict


class CliCreateSessionParams(TypedDict, total=False):
    scope: Literal['project', 'user']
    "Key scope.\n\n'project' (default) returns a project-level API key; 'user' returns a user-level\nAPI key valid across projects."
    source: str
    "Free-form string describing the source, e.g. 'Johns MacBook (darwin, v1.2.3)'"


__all__ = [
    "CliCreateSessionParams",
]
