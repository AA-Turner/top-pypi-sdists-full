# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.trigger_instance_upsert_params."""

from __future__ import annotations

from typing import Annotated, Dict, Literal, Optional, Union

from typing_extensions import NotRequired, TypedDict
from .._types import PropertyInfo


class TriggerInstanceUpsertParams(TypedDict, total=False):
    connected_auth_id: Annotated[str, PropertyInfo(alias='connectedAuthId')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use connected_account_id instead."
    body_trigger_config_2: Annotated[Dict[str, Optional[object]], PropertyInfo(alias='triggerConfig')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use trigger_config instead."
    connected_account_id: str
    "Connected account nanoid.\n\nOptional when user_id is provided — the first active connection for that user\nand the trigger's toolkit is auto-resolved."
    user_id: str
    "The user id (entity id) that owns the connection.\n\nWhen connected_account_id is omitted, the first active connection for this user\nand the trigger's toolkit is auto-resolved (same as tool execution). When\nconnected_account_id is also provided and the project has 2FA enabled, user_id\nis validated against the owner of that connection."
    egress_url: NotRequired[str | None]
    body_trigger_config_1: Annotated[Dict[str, Optional[object]], PropertyInfo(alias='trigger_config')]
    "Trigger configuration"
    type: NotRequired[Literal["poll", "webhook"]]
    polling_interval: NotRequired[int]
    version: str
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use toolkit_versions instead."
    toolkit_versions: Union[str, Dict[str, str], None]
    "Toolkit version specification.\n\nSupports \"latest\" string or a record mapping toolkit slugs to specific versions."


__all__ = [
    "TriggerInstanceUpsertParams",
]
