# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["CustomListParams"]


class CustomListParams(TypedDict, total=False):
    account_id: Required[str]

    profile_type: Literal["warp", "browser_extension"]
    """Filter profiles by client type. When omitted, only WARP profiles are returned."""
