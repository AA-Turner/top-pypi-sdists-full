# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["SuppressionEditParams"]


class SuppressionEditParams(TypedDict, total=False):
    account_id: Required[str]
    """Cloudflare account ID."""

    expires_at: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """New expiry.

    Send `null` to make the suppression permanent; omit to leave it unchanged.
    """

    note: str
    """Replacement advisory note.

    Send an empty string to clear it; omit to leave it unchanged.
    """

    scope: object
    """Not editable.

    Scope is fixed when the suppression is created; any value returns 400 with code
    `scope_immutable`. Delete and recreate the suppression to change it.
    """
