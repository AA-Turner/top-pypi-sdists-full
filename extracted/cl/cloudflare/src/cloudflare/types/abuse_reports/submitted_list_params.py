# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["SubmittedListParams"]


class SubmittedListParams(TypedDict, total=False):
    account_id: Required[str]

    id: str
    """Filter by report code."""

    created_after: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """Return reports submitted after this time."""

    created_before: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """Return reports submitted before this time."""

    domain: SequenceNotStr[str]
    """Filter by reported domain. This parameter can be specified multiple times."""

    page: int
    """Page of submitted reports to return."""

    per_page: int
    """Number of submitted reports per page."""

    sort: str
    """A property and direction to sort by (id, cdate, domain, type, status)."""

    status: List[Literal["submitted", "accepted", "denied"]]
    """Filter by submitter-facing status.

    This parameter can be specified multiple times.
    """

    type: List[Literal["PHISH", "GEN", "THREAT", "DMCA", "EMER", "TM", "REG_WHO", "NCSEI", "NETWORK"]]
    """Filter by report type. This parameter can be specified multiple times."""
