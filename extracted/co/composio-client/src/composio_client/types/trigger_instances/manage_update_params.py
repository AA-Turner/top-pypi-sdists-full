# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.trigger_instances.manage_update_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, TypedDict


class ManageUpdateParams(TypedDict, total=False):
    status: NotRequired[Literal['enable', 'disable']]
    user_id: NotRequired[str]
    egress_url: NotRequired[str | None]


__all__ = [
    "ManageUpdateParams",
]
