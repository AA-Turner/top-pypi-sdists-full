# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.triggers_type_retrieve_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class Toolkit(BaseModel):
    "Information about the toolkit that provides this trigger"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    logo: str
    "Logo of the toolkit"
    name: str
    "Deprecated: Use slug instead"
    slug: str
    "Unique identifier for the parent toolkit"


class TriggersTypeRetrieveResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    config: Dict[str, Optional[object]]
    "Configuration schema required to set up this trigger"
    description: str
    "Detailed description of what the trigger does"
    instructions: str
    "Step-by-step instructions on how to set up and use this trigger"
    name: str
    "Human-readable name of the trigger"
    payload: Dict[str, Optional[object]]
    "Schema of the data payload this trigger will deliver when it fires"
    requires_webhook_endpoint_setup: Optional[bool] = None
    "True when the developer must register a Composio-issued webhook URL with the\nupstream provider (e.g. Slack Event Subscriptions, Notion integration webhooks).\nSee the webhook_endpoint API for the setup."
    slug: str
    "Unique identifier for the trigger type"
    toolkit: Toolkit
    "Information about the toolkit that provides this trigger"
    type: Literal['webhook', 'poll']
    "The trigger mechanism - either webhook (event-based) or poll (scheduled check)"
    version: str
    "Version of the trigger type"
    types: list[Literal["webhook", "poll"]]


__all__ = [
    "TriggersTypeRetrieveResponse",
    "Toolkit",
]
