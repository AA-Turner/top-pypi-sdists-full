# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_delete_params."""

from __future__ import annotations

from typing import Optional

from typing_extensions import TypedDict


class ConnectedAccountDeleteParams(TypedDict, total=False):
    revoke_on_delete: Optional[bool]
    "When `true`, the delete also starts a background job that revokes the upstream\ncredentials of every connected account in scope, and the response carries a\n`revoke_job_id`. Defaults to `false`. Revocation is irreversible — recovering a\ndeleted entity does not restore working credentials."


__all__ = [
    "ConnectedAccountDeleteParams",
]
