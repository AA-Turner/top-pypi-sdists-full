# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WorkspaceSetSpendingLimitParams", "Limit"]


class WorkspaceSetSpendingLimitParams(TypedDict, total=False):
    limit: Required[Limit]

    type: Required[Literal["lifetime"]]


class Limit(TypedDict, total=False):
    amount: Required[int]
    """Workspace spending limit amount in milli-USD.

    Tracking starts when the limit is configured; prior or already-committed
    unreserved work is not counted in this workspace cap ledger. An amount of
    9007199254740991 (2^53 - 1) is the unlimited sentinel: usage is tracked but
    never blocked, and amounts at or above half the sentinel are normalized to it.
    """

    currency: Required[Literal["MILLI_USD"]]
    """Workspace spending limits currently support milli-USD only."""
