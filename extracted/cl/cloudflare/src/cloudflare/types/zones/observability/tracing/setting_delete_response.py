# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["SettingDeleteResponse"]


class SettingDeleteResponse(BaseModel):
    destinations: List[str]
    """Up to 100 OpenTelemetry destination identifiers that receive traces."""

    enabled: bool
    """Whether Cloudflare Traces is enabled for the zone."""

    forward_context: bool
    """Whether trace context is sent externally or across a zone boundary."""

    persist: bool
    """Whether traces are persisted in Cloudflare."""

    propagation_policy: Literal["accept", "authenticated", "reject"]
    """When inbound trace context may be continued.

    Authenticated propagation is not supported yet.
    """

    sampling_ratio: float
    """The ratio of requests sampled for tracing, from 0 to 1."""
