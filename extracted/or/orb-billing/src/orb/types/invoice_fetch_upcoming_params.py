# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["InvoiceFetchUpcomingParams"]


class InvoiceFetchUpcomingParams(TypedDict, total=False):
    subscription_id: Required[str]

    include_zero_quantity_line_items: Optional[bool]
    """Whether to return line items with a quantity of zero.

    When omitted, Orb returns every line item. A line item that is grouped as part
    of a line item minimum is always returned; an invoice-level minimum does not
    exempt it.
    """
