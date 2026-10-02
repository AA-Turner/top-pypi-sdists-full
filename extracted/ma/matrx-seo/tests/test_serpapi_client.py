"""The ONE SerpAPI engine's contract.

Every SerpAPI engine draws on ONE small monthly allowance, so the properties
that the deleted second client lacked — retry, quota capture, the body-carried
error reason, per-call cost evidence, and an observer that makes a spent search
impossible to lose — are pinned here rather than in a rank-specific test.
"""

from collections.abc import Mapping
from decimal import Decimal
from typing import Any

import pytest

from matrx_seo.providers.serpapi_client import (
    SerpApiCall,
    SerpApiClient,
    SerpApiError,
    SerpApiHttpResponse,
    SerpApiRetryExhausted,
    clear_serpapi_call_observers,
    register_serpapi_call_observer,
)

_OK_PAYLOAD = {
    "search_metadata": {"id": "abc123", "status": "Success"},
    "organic_results": [{"position": 1, "link": "https://example.com"}],
}


class FixtureTransport:
    def __init__(self, responses: list[SerpApiHttpResponse]) -> None:
        self.responses = responses
        self.calls: list[dict[str, Any]] = []

    async def get_json(
        self, _url: str, params: Mapping[str, str | int]
    ) -> SerpApiHttpResponse:
        self.calls.append(dict(params))
        return self.responses.pop(0)


@pytest.fixture(autouse=True)
def _no_leaked_observers():
    yield
    clear_serpapi_call_observers()


async def test_a_retryable_status_is_retried_and_the_attempt_count_is_evidence() -> None:
    transport = FixtureTransport(
        [
            SerpApiHttpResponse(status_code=429, payload={}, headers={"retry-after": "0"}),
            SerpApiHttpResponse(status_code=200, payload=_OK_PAYLOAD),
        ]
    )
    client = SerpApiClient(transport=transport, max_attempts=2, base_backoff_seconds=0)
    call = await client.search({"engine": "google", "q": "x"}, api_key="k")
    assert len(transport.calls) == 2
    assert call.attempts == 2
    assert call.search_id == "abc123"


async def test_retries_are_bounded() -> None:
    transport = FixtureTransport(
        [SerpApiHttpResponse(status_code=503, payload={}) for _ in range(3)]
    )
    client = SerpApiClient(transport=transport, max_attempts=3, base_backoff_seconds=0)
    with pytest.raises(SerpApiRetryExhausted):
        await client.search({"engine": "google", "q": "x"}, api_key="k")
    assert len(transport.calls) == 3


async def test_the_reason_serpapi_put_in_the_body_survives() -> None:
    """A permanently dead target must not become an unexplained 'HTTP 400'."""
    transport = FixtureTransport(
        [
            SerpApiHttpResponse(
                status_code=400, payload={"error": "Unsupported `location` parameter"}
            )
        ]
    )
    client = SerpApiClient(transport=transport)
    with pytest.raises(SerpApiError, match="Unsupported `location` parameter"):
        await client.search({"engine": "google", "q": "x"}, api_key="k")


async def test_a_200_carrying_an_error_body_is_still_an_error() -> None:
    transport = FixtureTransport(
        [SerpApiHttpResponse(status_code=200, payload={"error": "Google hasn't returned results"})]
    )
    client = SerpApiClient(transport=transport)
    with pytest.raises(SerpApiError, match="hasn't returned results"):
        await client.search({"engine": "google", "q": "x"}, api_key="k")


async def test_quota_headers_are_captured() -> None:
    transport = FixtureTransport(
        [
            SerpApiHttpResponse(
                status_code=200,
                payload=_OK_PAYLOAD,
                headers={"X-RateLimit-Remaining": "134", "Content-Type": "application/json"},
            )
        ]
    )
    call = await SerpApiClient(transport=transport).search(
        {"engine": "google", "q": "x"}, api_key="k"
    )
    assert call.quota_headers == {"x-ratelimit-remaining": "134"}


async def test_the_key_is_redacted_in_evidence_never_merely_absent() -> None:
    transport = FixtureTransport([SerpApiHttpResponse(status_code=200, payload=_OK_PAYLOAD)])
    call = await SerpApiClient(transport=transport).search(
        {"engine": "google", "q": "x"}, api_key="live-secret"
    )
    # It reached the wire...
    assert transport.calls[0]["api_key"] == "live-secret"
    # ...and never the evidence.
    assert call.request_parameters["api_key"] == "***"
    assert call.request_evidence["params"]["api_key"] == "***"
    assert "live-secret" not in str(call.request_evidence)


async def test_every_call_reaches_the_observers() -> None:
    """The whole point: a search spent outside an SEO collection can no longer
    disappear the way the deleted `serpi_api` client's did."""
    seen: list[SerpApiCall] = []
    register_serpapi_call_observer(seen.append)
    transport = FixtureTransport([SerpApiHttpResponse(status_code=200, payload=_OK_PAYLOAD)])
    client = SerpApiClient(transport=transport, estimated_cost_per_search="0.01")
    await client.search({"engine": "google_images", "q": "x"}, api_key="k")
    assert len(seen) == 1
    assert seen[0].engine == "google_images"
    assert seen[0].estimated_cost == Decimal("0.01")


async def test_an_observer_that_raises_never_kills_a_paid_search() -> None:
    def explode(_call: SerpApiCall) -> None:
        raise RuntimeError("bookkeeping is broken")

    register_serpapi_call_observer(explode)
    transport = FixtureTransport([SerpApiHttpResponse(status_code=200, payload=_OK_PAYLOAD)])
    call = await SerpApiClient(transport=transport).search(
        {"engine": "google", "q": "x"}, api_key="k"
    )
    assert call.search_id == "abc123"


async def test_a_missing_search_id_is_refused() -> None:
    transport = FixtureTransport(
        [SerpApiHttpResponse(status_code=200, payload={"organic_results": []})]
    )
    with pytest.raises(SerpApiError, match="omitted search_metadata.id"):
        await SerpApiClient(transport=transport).search(
            {"engine": "google", "q": "x"}, api_key="k"
        )


async def test_a_search_without_a_key_never_reaches_the_wire() -> None:
    transport = FixtureTransport([])
    with pytest.raises(ValueError, match="require an api_key"):
        await SerpApiClient(transport=transport).search({"engine": "google"}, api_key="")
    assert transport.calls == []
