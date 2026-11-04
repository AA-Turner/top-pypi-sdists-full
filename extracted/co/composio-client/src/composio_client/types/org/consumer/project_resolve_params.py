# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.org.consumer.project_resolve_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class ProjectResolveParams(TypedDict, total=False):
    x_user_api_key: Required[str]
    x_org_id: Required[str]


__all__ = [
    "ProjectResolveParams",
]
