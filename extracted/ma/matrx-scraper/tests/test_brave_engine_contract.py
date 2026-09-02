"""The ONE Brave engine's contract.

These pin the properties that used to live in only ONE of the two Brave clients
(and so were absent from whichever one you happened to call): a 429 is a typed
error and never an empty result set, pacing re-tunes from Brave's own header,
`Retry-After` is honoured, and the locale/section parameters exist at all.
"""

from typing import Any

import httpx
import pytest

from matrx_scraper.search import (
    BraveRateLimitError,
    BraveSearchClient,
    BraveSearchParams,
    NullRateLimiter,
    RateLimiter,
)


class QueueClient:
    def __init__(self, responses: list[httpx.Response]) -> None:
        self.responses = responses
        self.calls: list[dict[str, Any]] = []

    async def __aenter__(self) -> "QueueClient":
        return self

    async def __aexit__(self, *_args: Any) -> None:
        return None

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        self.calls.append({"url": url, **kwargs})
        return self.responses.pop(0)


def _response(status: int, payload: dict[str, Any], **headers: str) -> httpx.Response:
    return httpx.Response(
        status,
        json=payload,
        headers=headers,
        request=httpx.Request("GET", "https://api.search.brave.com/res/v1/web/search"),
    )


def _client(
    responses: list[httpx.Response], **kwargs: Any
) -> tuple[BraveSearchClient, QueueClient]:
    queue = QueueClient(responses)
    return (
        BraveSearchClient(api_key="k", client_factory=lambda: queue, **kwargs),
        queue,
    )


async def test_exhausted_429_raises_instead_of_returning_no_results() -> None:
    """The incident this engine exists to prevent: a throttled key returning
    `None`/`{}` and every caller reading it as 'nothing found'."""
    slept: list[float] = []

    async def sleep(delay: float) -> None:
        slept.append(delay)

    client, queue = _client(
        [_response(429, {}, **{"retry-after": "2"}), _response(429, {})],
        sleep=sleep,
    )
    with pytest.raises(BraveRateLimitError):
        await client.search_response(
            BraveSearchParams(query="q"),
            rate_limiter=NullRateLimiter(),
            max_attempts=2,
        )
    assert len(queue.calls) == 2
    # Retry-After won over the exponential fallback.
    assert slept == [2.0]


async def test_retry_delay_is_capped() -> None:
    slept: list[float] = []

    async def sleep(delay: float) -> None:
        slept.append(delay)

    client, _ = _client(
        [_response(503, {}, **{"retry-after": "9999"}), _response(200, {"web": {"results": []}})],
        sleep=sleep,
    )
    result = await client.search_response(
        BraveSearchParams(query="q"),
        rate_limiter=NullRateLimiter(),
        max_attempts=2,
        max_retry_delay_seconds=5.0,
    )
    assert slept == [5.0]
    assert result.attempts == 2


async def test_pacing_retunes_from_the_advertised_ceiling() -> None:
    limiter = RateLimiter(min_interval=1.2)
    client, _ = _client([_response(200, {"web": {}}, **{"x-ratelimit-limit": "50, 20000"})])
    await client.search_response(BraveSearchParams(query="q"), rate_limiter=limiter)
    # 50 req/sec advertised -> MARGIN (1.2) / 50 = 0.024s, i.e. 41.7 req/sec.
    # The FLOOR (0.02s) deliberately does NOT bind here: it is a cap for an
    # over-reported header, not the working rate. Measured clean against the
    # live PRO key at this rate, 100/100 requests, zero 429s (2026-08-20).
    assert limiter.min_interval == pytest.approx(0.024)


async def test_a_429_still_retunes_pacing() -> None:
    """The header is present on 429s too; a throttled key must not keep pacing
    as if it were unthrottled."""
    limiter = RateLimiter(min_interval=0.6)
    client, _ = _client([_response(429, {}, **{"x-ratelimit-limit": "1, 2000"})])
    with pytest.raises(BraveRateLimitError):
        await client.search_response(
            BraveSearchParams(query="q"), rate_limiter=limiter, max_attempts=1
        )
    assert limiter.min_interval == pytest.approx(1.2)


async def test_locale_and_section_parameters_reach_the_wire() -> None:
    client, queue = _client([_response(200, {"web": {}})])
    await client.search_response(
        BraveSearchParams(
            query="q",
            search_lang="de",
            ui_lang="de-DE",
            spellcheck=False,
            result_filter="web",
        ),
        rate_limiter=NullRateLimiter(),
    )
    params = queue.calls[0]["params"]
    assert params["search_lang"] == "de"
    assert params["ui_lang"] == "de-DE"
    assert params["spellcheck"] is False
    assert params["result_filter"] == "web"


async def test_unset_optional_parameters_are_omitted_entirely() -> None:
    """A caller that passes nothing sends exactly what it sent before these
    parameters existed — Brave rejects some keys outright when blank."""
    client, queue = _client([_response(200, {"web": {}})])
    await client.search_response(BraveSearchParams(query="q"), rate_limiter=NullRateLimiter())
    params = queue.calls[0]["params"]
    for absent in ("search_lang", "ui_lang", "spellcheck", "result_filter", "goggles", "summary"):
        assert absent not in params


async def test_a_per_call_key_overrides_selection_and_gets_its_own_limiter() -> None:
    """How matrx-seo rides this engine with an ORGANIZATION's key while still
    sharing its pacing and throttle handling."""
    client, queue = _client([_response(200, {"web": {}}, **{"x-ratelimit-limit": "1, 2000"})])
    await client.search_response(BraveSearchParams(query="q"), api_key="org-key")
    assert queue.calls[0]["headers"]["X-Subscription-Token"] == "org-key"
    assert client._limiter_for("org-key").min_interval == pytest.approx(1.2)


async def test_a_keyless_client_fails_at_call_time_not_construction(monkeypatch) -> None:
    for var in (
        "BRAVE_SEARCH_API_KEY",
        "BRAVE_API_KEY",
        "BRAVE_SEARCH_API_KEY_AI",
        "BRAVE_SEARCH_API_KEY_PRO_AI",
    ):
        monkeypatch.delenv(var, raising=False)
    client = BraveSearchClient(allow_missing_key=True)
    with pytest.raises(ValueError, match="No Brave API key for this request"):
        await client.search_response(BraveSearchParams(query="q"))
