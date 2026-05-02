# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["StudioProjectUpdateParams"]


class StudioProjectUpdateParams(TypedDict, total=False):
    description: str
    """The description of the Studio Project"""

    name: str
    """The name of the Studio Project"""

    studio_api_key: str
    """Your API key for Studio, can be updated with the PATCH endpoint"""
