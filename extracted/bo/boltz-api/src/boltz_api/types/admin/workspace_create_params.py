# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WorkspaceCreateParams", "DataRetention", "SpendingLimit", "SpendingLimitLimit"]


class WorkspaceCreateParams(TypedDict, total=False):
    data_retention: DataRetention
    """How long result data is retained before automatic deletion.

    Defaults to 7 days if not specified. Maximum retention is 14 days (336 hours).
    """

    name: str
    """Workspace name"""

    spending_limit: SpendingLimit


class DataRetention(TypedDict, total=False):
    """How long result data is retained before automatic deletion.

    Defaults to 7 days if not specified. Maximum retention is 14 days (336 hours).
    """

    unit: Required[Literal["hours", "days"]]
    """Time unit for retention duration"""

    value: Required[int]
    """Duration value. Maximum retention is 14 days (or 336 hours)."""


class SpendingLimitLimit(TypedDict, total=False):
    amount: Required[int]
    """Workspace spending limit amount in milli-USD.

    Tracking starts when the limit is configured; prior or already-committed
    unreserved work is not counted in this workspace cap ledger. An amount of
    9007199254740991 (2^53 - 1) is the unlimited sentinel: usage is tracked but
    never blocked, and amounts at or above half the sentinel are normalized to it.
    """

    currency: Required[Literal["MILLI_USD"]]
    """Workspace spending limits currently support milli-USD only."""


class SpendingLimit(TypedDict, total=False):
    limit: Required[SpendingLimitLimit]

    type: Required[Literal["lifetime"]]
