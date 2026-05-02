# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["MessageRetrieveParams"]


class MessageRetrieveParams(TypedDict, total=False):
    fetch_by_account: bool
    """Fetch the thread by account instead of user"""

    fetch_spans: bool
    """Fetch spans for each message"""
