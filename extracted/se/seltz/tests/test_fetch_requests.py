"""The FetchRequest a call builds, field by field.

Every optional field is absent unless the caller names it, because the service
reads an absent `formats` as ["markdown"] and an absent `tier` as "pro". A
wrapper that sent a default instead would pin those choices client-side and go
stale the moment the service moves.
"""

import inspect

import pytest

from seltz._types import OMIT
from seltz.services.fetch_service import (
    AsyncFetchService,
    FetchService,
    _build_fetch_request,
)

URLS = ["https://example.com/", "https://example.org/"]


def _request(**overrides):
    args = dict(urls=URLS, api_key="k", formats=OMIT, tier=OMIT, timeout_ms=OMIT)
    args.update(overrides)
    return _build_fetch_request(**args)


def test_only_urls_and_the_key_are_sent_by_default() -> None:
    req = _request()
    assert list(req.urls) == URLS
    assert req.api_key == "k"
    assert list(req.formats) == []
    assert not req.HasField("tier")
    assert not req.HasField("timeout_ms")


def test_formats_is_reachable() -> None:
    assert list(_request(formats=["markdown"]).formats) == ["markdown"]


def test_tier_is_reachable() -> None:
    assert _request(tier="pro").tier == "pro"


def test_timeout_ms_is_reachable() -> None:
    assert _request(timeout_ms=15000).timeout_ms == 15000


@pytest.mark.parametrize("field", ["formats", "tier", "timeout_ms"])
def test_none_and_omit_agree(field: str) -> None:
    """Nothing on fetch is clearable, so the two must serialize identically."""
    assert (
        _request(**{field: None}).SerializeToString() == _request().SerializeToString()
    )


def test_urls_accepts_any_iterable() -> None:
    assert list(_request(urls=iter(URLS)).urls) == URLS


def test_the_async_service_defines_its_own_body() -> None:
    assert AsyncFetchService.fetch is not FetchService.fetch
    assert inspect.iscoroutinefunction(AsyncFetchService.fetch)


def test_the_two_services_take_the_same_arguments() -> None:
    assert list(inspect.signature(AsyncFetchService.fetch).parameters) == list(
        inspect.signature(FetchService.fetch).parameters
    )
