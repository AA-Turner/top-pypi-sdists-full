# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SuppressionListParams"]


class SuppressionListParams(TypedDict, total=False):
    account_id: Required[str]
    """Cloudflare account ID."""

    cursor: str
    """Opaque pagination cursor returned as `result_info.next_cursor`.

    It carries the filters that produced it.
    """

    email: str
    """Exact email-address filter."""

    per_page: int
    """Maximum number of suppressions to return per page."""

    reason: Literal["manual", "complaint", "hard_bounce", "soft_bounce", "policy"]
    """Filter to suppressions with this reason."""

    scope_type: Literal["account", "sending_domain"]
    """
    Filter by scope: `account` returns only account-wide suppressions,
    `sending_domain` only sending-domain suppressions. Omit to list both,
    sending-domain suppressions first.
    """

    scope_value: str
    """Exact sending-domain filter. Requires `scope_type=sending_domain`."""

    search: str
    """
    A complete address is an exact match; a value ending in `@` matches that
    username across every domain. Prefix searches may return short intermediate
    pages while the bounded account scan advances.
    """
