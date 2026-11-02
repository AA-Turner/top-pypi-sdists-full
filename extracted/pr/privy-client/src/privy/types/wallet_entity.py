# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .entity_id import EntityID
from .wallet_entity_type import WalletEntityType

__all__ = ["WalletEntity"]


class WalletEntity(BaseModel):
    """The entity a wallet is attributed to."""

    id: EntityID
    """A Privy entity ID."""

    type: WalletEntityType
    """The type of entity a wallet is attributed to."""
