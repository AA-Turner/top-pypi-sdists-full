from __future__ import annotations

from datetime import UTC, datetime

from .adapters import ProviderExecutionContext, SeoProviderAdapter
from .contracts import (
    CollectionRequest,
    NormalizationContext,
    ProviderResponse,
    RankObservation,
    ResolvedCredential,
    SeoCapability,
    SeoObservation,
)
from .repository import SeoRepository


class FakeRankProvider(SeoProviderAdapter):
    capabilities = (SeoCapability.SERP_RANK,)

    def __init__(
        self,
        repository: SeoRepository,
        *,
        provider: str,
        observed_at: datetime | None = None,
        organic_rank: int = 3,
    ) -> None:
        self.provider = provider
        self.observed_at = observed_at or datetime(2026, 7, 21, tzinfo=UTC)
        self.organic_rank = organic_rank
        self.fetch_count = 0
        self.authenticated = False

    async def authenticate(self, credential: ResolvedCredential) -> None:
        if not credential.values:
            raise ValueError("fake credential values must be non-empty")
        self.authenticated = True

    async def collect_response(
        self, request: CollectionRequest, execution: ProviderExecutionContext
    ) -> ProviderResponse:
        if not self.authenticated:
            raise RuntimeError("provider was not authenticated")
        self.fetch_count += 1
        return ProviderResponse(
            raw={
                "keyword_id": request.settings["keyword_id"],
                "rank_target_id": request.settings["rank_target_id"],
                "engine": request.settings.get("engine", self.provider),
                "locale": request.settings.get("locale", "US"),
                "matched_domain": request.settings.get("target_domain", "example.com"),
                "matched_url": request.settings.get("matched_url", "https://example.com/page"),
                "organic_rank": self.organic_rank,
                "observed_at": self.observed_at.isoformat(),
            },
            fetched_at=self.observed_at,
            provider_schema_version="fake-v1",
        )

    async def normalize(
        self, response: ProviderResponse, context: NormalizationContext
    ) -> list[SeoObservation]:
        raw = response.raw
        if not isinstance(raw, dict):
            raise TypeError("fake rank response must be an object")
        return [
            RankObservation(
                keyword_id=str(raw["keyword_id"]),
                rank_target_id=str(raw["rank_target_id"]),
                engine=str(raw["engine"]),
                locale=str(raw["locale"]),
                matched_domain=str(raw["matched_domain"]),
                matched_url=str(raw["matched_url"]),
                organic_rank=int(raw["organic_rank"]),
                absolute_rank=int(raw["organic_rank"]),
                observed_at=datetime.fromisoformat(str(raw["observed_at"])),
            )
        ]


async def fake_credential_resolver(request: CollectionRequest, provider: str) -> ResolvedCredential:
    return ResolvedCredential(
        reference_id=request.credential_reference_id,
        values={"organization": request.organization_id, "provider": provider, "token": "fake"},
    )


async def fake_collection_authorizer(request: CollectionRequest) -> CollectionRequest:
    return request
