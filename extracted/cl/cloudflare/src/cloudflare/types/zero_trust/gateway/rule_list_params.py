# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["RuleListParams"]


class RuleListParams(TypedDict, total=False):
    account_id: Required[str]
    """Specify the Cloudflare account identifier."""

    direction: Literal["asc", "desc"]
    """Sort direction.

    When `order_by` is omitted, this controls the direction of the existing
    precedence ordering. Shared rules remain first in either direction. Accepted
    values are `asc` and `desc`.
    """

    filter: SequenceNotStr[str]
    """Filter the returned rules by one or more `field:value` pairs.

    Repeat the parameter to combine filters with logical AND.

    Supported fields are `name`, `id`, `action`, `enabled`, `source_account`,
    `is_shared`, `filters`, and `expression` (max 1024 bytes). The `source_account`
    value is matched as a normalized UUID substring. The `filters` value must be one
    of the rule filter names and matches a member of the rule's `filters` array. The
    `expression` filter performs a case-insensitive literal substring match across
    traffic, identity, and device posture expressions.
    """

    order_by: Literal["name", "created_at", "updated_at", "precedence"]
    """Field to sort the returned rules by.

    Supported values are `name`, `created_at`, `updated_at`, and `precedence`.
    """

    search: str
    """Case-insensitive substring search across rule name and description."""
