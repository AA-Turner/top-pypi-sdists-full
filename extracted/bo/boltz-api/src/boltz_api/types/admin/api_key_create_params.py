# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["APIKeyCreateParams"]


class APIKeyCreateParams(TypedDict, total=False):
    name: Required[str]
    """API key name"""

    allowed_ips: SequenceNotStr[str]
    """IP addresses allowed to use this key (IPv4 or IPv6).

    An empty array (the default) means all IPs are allowed.
    """

    expires_in_days: int
    """Days until the key expires. Omit for a key that does not expire."""

    mode: Literal["live", "test"]
    """Key mode. Test keys create test-mode resources with synthetic data."""

    workspace_id: str
    """Workspace ID to scope this key to. Omit for default workspace."""
