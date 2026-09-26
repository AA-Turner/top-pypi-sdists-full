# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["CancelReasonCreateParams"]


class CancelReasonCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    other: str
    """Additional cancellation details."""

    reason_code: SequenceNotStr[str]
    """The cancellation reason codes."""
