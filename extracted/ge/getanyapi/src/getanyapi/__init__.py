"""getanyapi - official typed Python SDK for AnyAPI.

    from getanyapi import AnyAPI, AsyncAnyAPI, agent_signup, unwrap
    from getanyapi import AnyAPIError, NotFoundError, RateLimitedError  # etc.

Sync and async clients share generated per-platform namespaces (attached lazily)
through a single transport seam. Output models are pydantic v2; open provider
records round-trip unknown fields via ``.model_extra``. See ../../../SPEC.md
section 3 for the frozen public surface.
"""

from __future__ import annotations

from ._async_client import AsyncAnyAPI
from ._client import AnyAPI, agent_signup
from ._errors import (
    AnyAPIError,
    AuthenticationError,
    BadRequestError,
    ConnectionError,
    InsufficientBalanceError,
    NotFoundError,
    RateLimitedError,
    RequestPendingError,
    ResultNotFoundError,
    TimeoutError,
    UpstreamError,
)
from ._pagination import AsyncPaginator, Paginator
from .types import (
    AccountProfile,
    AgentSignupResult,
    Balance,
    BareRunResult,
    CatalogEntry,
    CatalogSearchResult,
    CatalogSearchResults,
    DiscoveryExecution,
    DiscoveryLane,
    DiscoveryLatency,
    DiscoveryPricing,
    DiscoverySource,
    FlatPricingOffer,
    HighlightField,
    LaneHealth,
    LinearPricingOffer,
    NotFoundReason,
    Output,
    OutputFound,
    OutputNotFound,
    PricingOffer,
    RequestOptions,
    RequestSnapshot,
    RunResult,
    unwrap,
)

__version__ = "0.149.3"

__all__ = [
    # clients + top-level functions
    "AnyAPI",
    "AsyncAnyAPI",
    "agent_signup",
    "unwrap",
    # result + data models
    "RunResult",
    "BareRunResult",
    "Output",
    "OutputFound",
    "OutputNotFound",
    "NotFoundReason",
    "Balance",
    "AccountProfile",
    "CatalogEntry",
    "FlatPricingOffer",
    "LinearPricingOffer",
    "PricingOffer",
    "DiscoveryPricing",
    "DiscoveryExecution",
    "DiscoverySource",
    "LaneHealth",
    "DiscoveryLane",
    "DiscoveryLatency",
    "HighlightField",
    "CatalogSearchResult",
    "CatalogSearchResults",
    "RequestOptions",
    "RequestSnapshot",
    "AgentSignupResult",
    # pagination
    "Paginator",
    "AsyncPaginator",
    # errors
    "AnyAPIError",
    "BadRequestError",
    "AuthenticationError",
    "InsufficientBalanceError",
    "NotFoundError",
    "ResultNotFoundError",
    "RateLimitedError",
    "UpstreamError",
    "ConnectionError",
    "TimeoutError",
    "RequestPendingError",
]
