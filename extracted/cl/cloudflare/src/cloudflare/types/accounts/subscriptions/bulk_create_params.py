# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from ...shared_params.subscription import Subscription

__all__ = ["BulkCreateParams"]


class BulkCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    idemp_key: str

    coupon_code: str

    payment_hold_id: int

    subscriptions: Iterable[Subscription]

    user_is_on_session: bool
