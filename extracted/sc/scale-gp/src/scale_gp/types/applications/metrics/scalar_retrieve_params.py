# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["ScalarRetrieveParams"]


class ScalarRetrieveParams(TypedDict, total=False):
    application_spec_id: Required[str]

    account_id: str
    """Account ID used for authorization"""

    from_ts: int
    """The starting (oldest) timestamp window in seconds."""

    to_ts: int
    """The ending (most recent) timestamp in seconds."""

    variants: SequenceNotStr[str]
    """Which variants to filter on"""
