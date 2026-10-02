# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["WorkspaceRetrieveSpendingLimitResponse", "AccruedUsage", "Limit"]


class AccruedUsage(BaseModel):
    amount: int
    """Workspace spending limit amount in milli-USD.

    Tracking starts when the limit is configured; prior or already-committed
    unreserved work is not counted in this workspace cap ledger. An amount of
    9007199254740991 (2^53 - 1) is the unlimited sentinel: usage is tracked but
    never blocked, and amounts at or above half the sentinel are normalized to it.
    """

    currency: Literal["MILLI_USD"]
    """Workspace spending limits currently support milli-USD only."""


class Limit(BaseModel):
    amount: int
    """Workspace spending limit amount in milli-USD.

    Tracking starts when the limit is configured; prior or already-committed
    unreserved work is not counted in this workspace cap ledger. An amount of
    9007199254740991 (2^53 - 1) is the unlimited sentinel: usage is tracked but
    never blocked, and amounts at or above half the sentinel are normalized to it.
    """

    currency: Literal["MILLI_USD"]
    """Workspace spending limits currently support milli-USD only."""


class WorkspaceRetrieveSpendingLimitResponse(BaseModel):
    """Configured lifetime workspace spending limit, or null if unset.

    Unset workspaces have no workspace-level cap and continue to use organization-level billing.
    """

    accrued_usage: AccruedUsage

    limit: Limit

    type: Literal["lifetime"]
