# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["WorkspaceUpdateParams", "DataRetention"]


class WorkspaceUpdateParams(TypedDict, total=False):
    data_retention: DataRetention
    """How long result data is retained before automatic deletion.

    Defaults to 7 days if not specified. Maximum retention is 14 days (336 hours).
    """

    name: Optional[str]


class DataRetention(TypedDict, total=False):
    """How long result data is retained before automatic deletion.

    Defaults to 7 days if not specified. Maximum retention is 14 days (336 hours).
    """

    unit: Required[Literal["hours", "days"]]
    """Time unit for retention duration"""

    value: Required[int]
    """Duration value. Maximum retention is 14 days (or 336 hours)."""
