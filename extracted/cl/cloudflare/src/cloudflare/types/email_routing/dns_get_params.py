# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DNSGetParams"]


class DNSGetParams(TypedDict, total=False):
    zone_id: Required[str]
    """Identifier."""

    subdomain: str
    """Deprecated.

    When supplied, the response shape differs from the documented default and is not
    modeled in generated SDKs. Do not rely on this parameter.
    """
