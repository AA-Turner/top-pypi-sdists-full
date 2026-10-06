"""Query-shaped web searches through the one collection path.

A plain "what does Google / Brave show for these words" search (brand search,
competitor-name lookup) is a paid provider call like any other: it is checked
against ``seo.reuse_hours.web_search`` before buying (``matrx_seo.reuse``), its
raw answer is stored as the run's payload and read back here, and the answer
carries the receipt's reuse verdict. No observations are normalized from it —
the caller parses the payload it asked for.

Operations: ``google_search`` on the SerpAPI adapter, ``brave.web.search`` on
the Brave adapter. Both are ``RAW_PROVIDER`` capability.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .adapters import SeoProviderAdapter, SeoProviderOperation
from .contracts import CollectionReceipt, CollectionRequest, SeoCapability
from .identity import stable_hash

SERPAPI_GOOGLE_SEARCH_OPERATION = SeoProviderOperation(
    name="google_search",
    capability=SeoCapability.RAW_PROVIDER,
    credential_keys=("SERPAPI_API_KEY",),
    reuse_family="web_search",
)
BRAVE_WEB_SEARCH_OPERATION = SeoProviderOperation(
    name="brave.web.search",
    capability=SeoCapability.RAW_PROVIDER,
    credential_keys=("BRAVE_SEARCH_API_KEY",),
    reuse_family="web_search",
)

Engine = Literal["google", "brave"]
_ENGINES: dict[str, tuple[str, SeoProviderOperation]] = {
    "google": ("serpapi", SERPAPI_GOOGLE_SEARCH_OPERATION),
    "brave": ("brave", BRAVE_WEB_SEARCH_OPERATION),
}


class WebSearchSettings(BaseModel):
    """One search. Hashed as the reuse identity, so equal searches reuse."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=400)
    count: int = Field(default=10, ge=1, le=20)
    country: str = "us"
    language: str = "en"

    def serpapi_parameters(self) -> dict[str, str | int]:
        return {
            "engine": "google",
            "q": self.query,
            "google_domain": "google.com",
            "gl": self.country.lower(),
            "hl": self.language.lower(),
            "num": self.count,
            "output": "json",
        }


def engine_provider(engine: Engine) -> str:
    return _ENGINES[engine][0]


def web_search_request(
    engine: Engine,
    *,
    organization_id: str,
    created_by: str,
    settings: WebSearchSettings,
    force_refresh: bool = False,
    require_fresh_within_seconds: int | None = None,
) -> CollectionRequest:
    """The collection request for one search. Not bound to a site: the same
    words in the same market are one answer for the whole organization."""
    _provider, operation = _ENGINES[engine]
    payload = settings.model_dump(mode="json")
    return CollectionRequest(
        organization_id=organization_id,
        created_by=created_by,
        capability=SeoCapability.RAW_PROVIDER,
        operation=operation.name,
        target_ref=f"web-search:{stable_hash(payload)}",
        observation_period=datetime.now(UTC).date().isoformat(),
        settings=payload,
        force_refresh=force_refresh,
        require_fresh_within_seconds=require_fresh_within_seconds,
    )


@dataclass(frozen=True)
class WebSearchAnswer:
    payload: dict[str, Any] | None
    receipt: CollectionReceipt

    @property
    def run_id(self) -> str:
        return self.receipt.run_id

    @property
    def reuse_reason(self) -> str | None:
        return self.receipt.reuse.reason if self.receipt.reuse is not None else None


async def collect_web_search(
    service: Any, adapter: SeoProviderAdapter, request: CollectionRequest
) -> WebSearchAnswer:
    """Collect (or reuse) one search and read its stored answer back.

    A completed run without a readable payload raises: an answer that cannot be
    read is never reported as an empty result."""
    receipt: CollectionReceipt = await service.collect(adapter, request)
    if not receipt.raw_payload_id:
        raise RuntimeError(f"web search run {receipt.run_id} completed with no stored payload")
    payload = await service.repository.load_raw_payload(receipt.raw_payload_id)
    if payload is None:
        raise RuntimeError(
            f"web search run {receipt.run_id}: "
            f"stored payload {receipt.raw_payload_id} is unreadable"
        )
    if not isinstance(payload, dict):
        raise TypeError(f"web search run {receipt.run_id}: payload is not an object")
    return WebSearchAnswer(payload=payload, receipt=receipt)


__all__ = [
    "BRAVE_WEB_SEARCH_OPERATION",
    "SERPAPI_GOOGLE_SEARCH_OPERATION",
    "WebSearchAnswer",
    "WebSearchSettings",
    "collect_web_search",
    "engine_provider",
    "web_search_request",
]
