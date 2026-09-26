# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BillingAddressValidationParams"]


class BillingAddressValidationParams(TypedDict, total=False):
    address: str
    """Address line 1."""

    address2: str
    """Address line 2."""

    city: str
    """City."""

    country: str
    """Country code."""

    state: str
    """State or province."""

    zipcode: str
    """Postal or zip code."""
