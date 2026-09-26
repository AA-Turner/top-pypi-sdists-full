# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["ProxyEndpointListParams"]


class ProxyEndpointListParams(TypedDict, total=False):
    account_id: Required[str]
    """Specify the Cloudflare account identifier."""

    direction: Literal["asc", "desc"]
    """Sort direction.

    Only takes effect when `order_by` is also provided; it is ignored otherwise.
    When `direction` is omitted the effective direction is field-specific:
    `created_at` and `updated_at` default to descending (newest first); `name`
    defaults to ascending.

    - `asc` — ascending.
    - `desc` — descending.
    """

    filter: SequenceNotStr[str]
    """
    Filter the returned proxy endpoints by one or more `field:value` pairs. Repeat
    the parameter to apply multiple filters; they are combined with logical AND (an
    endpoint must satisfy every filter to be returned).

    Supported fields and their matching behaviour:

    - `name` — case-insensitive substring match on the endpoint name.
    - `id` — substring match on the endpoint ID (UUID), with or without dashes.
    - `kind` — exact match on the endpoint kind. The value must be `ip` or
      `identity`; any other value returns `400`.

    Each entry must match one of the per-field patterns below: the field must be one
    of `name`, `id`, or `kind`; `name`/`id` accept any value, while `kind` only
    accepts `ip` or `identity`.
    """

    order_by: Literal["name", "created_at", "updated_at"]
    """Field to sort the returned endpoints by.

    When omitted, the order of results is unspecified. Supported values:

    - `name` — sort alphabetically by endpoint name.
    - `created_at` — sort by creation time; defaults to descending unless
      `direction` is set.
    - `updated_at` — sort by last-modified time; defaults to descending unless
      `direction` is set.
    """

    search: str
    """Case-insensitive substring match on the endpoint name.

    When combined with `filter`, both must match (logical AND).
    """
