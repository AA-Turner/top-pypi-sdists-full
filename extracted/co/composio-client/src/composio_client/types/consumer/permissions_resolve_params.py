# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.consumer.permissions_resolve_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, TypedDict
from ..._types import SequenceNotStr


class PermissionsResolveParams(TypedDict, total=False):
    connected_account_ids: NotRequired[SequenceNotStr[str]]
    connected_accounts: NotRequired[dict[str, SequenceNotStr[str]]]
    default: NotRequired[Literal["allow_all", "ask_every_call", "ask_once_per_session"]]


__all__ = [
    "PermissionsResolveParams",
]
