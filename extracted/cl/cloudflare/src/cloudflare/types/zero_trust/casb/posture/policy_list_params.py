# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PolicyListParams"]


class PolicyListParams(TypedDict, total=False):
    account_id: Required[str]

    cursor: str
    """Cursor for pagination.

    Obtained from the `result_info.cursor` field of a previous response.
    """
