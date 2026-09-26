# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ReceiptPDFParams"]


class ReceiptPDFParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    doctype: str
    """The document type to generate."""
