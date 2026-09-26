# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["BillingAddressValidationResponse", "ValidatedAddress"]


class ValidatedAddress(BaseModel):
    address: Optional[str] = None
    """Validated address line 1."""

    address2: Optional[str] = None
    """Validated address line 2."""

    city: Optional[str] = None
    """Validated city."""

    country: Optional[str] = None
    """Validated country code."""

    state: Optional[str] = None
    """Validated state or province."""

    validation_code: Optional[str] = None
    """The validation result code."""

    zipcode: Optional[str] = None
    """Validated postal or zip code."""


class BillingAddressValidationResponse(BaseModel):
    validated_addresses: Optional[List[ValidatedAddress]] = None
    """List of validated address suggestions."""
