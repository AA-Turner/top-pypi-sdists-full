# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ProfileUpdateBillingEmailParams"]


class ProfileUpdateBillingEmailParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    billing_email: str

    preferred_locale: str

    secondary_billing_email: str
