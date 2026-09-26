# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["SubscriptionCancelDowngradeParams"]


class SubscriptionCancelDowngradeParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    subscription_ids: SequenceNotStr[str]
    """List of subscription identifiers to cancel downgrades for."""
