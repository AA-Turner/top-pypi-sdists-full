# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PayBadDebtCreateParams"]


class PayBadDebtCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    payment_method_id: str
    """The payment method to use. If omitted, the default payment method is used."""
