# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["StudioProjectCreateParams"]


class StudioProjectCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    description: Required[str]
    """The description of the Studio Project"""

    name: Required[str]
    """The name of the Studio Project"""

    studio_api_key: Required[str]
    """Your API key for Studio, can be updated with the PATCH endpoint"""
