"""How `tier` reaches the wire on a SearchRequest.

`tier` is a plain string field, so there is nothing to map: the caller's name
travels as written. The service owns which tiers exist -- it matches the name
case-insensitively and rejects one it does not recognize, naming the tiers it
accepts -- so this SDK neither normalizes nor validates.

That division is what these tests pin. Validating here would duplicate the
service's check and go stale the first time a tier is added; normalizing here
would send a tier the caller did not write. The server reads an absent `tier`
as the pro tier, so the SDK still sends nothing unless the caller names one:
hardcoding pro would pin that choice client-side and go stale the moment the
service moves its default.
"""

import inspect

import pytest

from seltz._types import OMIT
from seltz.services.search_service import (
    AsyncSearchService,
    SearchService,
    _build_search_request,
)


def _request(**overrides):
    args = dict(
        query="q",
        api_key="k",
        max_results=10,
        scope=OMIT,
        include_domains=OMIT,
        exclude_domains=OMIT,
        from_date=OMIT,
        to_date=OMIT,
        tier=OMIT,
        fields=OMIT,
    )
    args.update(overrides)
    return _build_search_request(**args)


def test_an_omitted_tier_is_absent_from_the_request() -> None:
    """No client-side default: the field stays unset so the server picks."""
    assert not _request().HasField("tier")


def test_base_is_transmitted_when_asked_for() -> None:
    """Base is the opt-out, so it only travels when the caller names it."""
    request = _request(tier="base")
    assert request.HasField("tier")
    assert request.tier == "base"


def test_pro_is_transmitted_when_asked_for() -> None:
    request = _request(tier="pro")
    assert request.HasField("tier")
    assert request.tier == "pro"


@pytest.mark.parametrize("name", ["PRO", "Pro", "pRo", "pro", "  pro  "])
def test_a_tier_name_travels_exactly_as_written(name: str) -> None:
    """The SDK does not fold case; the service does.

    Normalizing here would look harmless and would not be: `tier` selects a
    price, so the value that reaches billing should be the value the caller
    sent, not one this SDK decided on their behalf.
    """
    request = _request(tier=name)
    assert request.HasField("tier")
    assert request.tier == name


@pytest.mark.parametrize(
    "name",
    [
        "turbo",
        "TURBO",
        "unspecified",
        "search_tier_unspecified",
        "SEARCH_TIER_PRO",
        "constructor",
        "0",
        "2",
    ],
)
def test_an_unrecognized_tier_is_forwarded_rather_than_rejected(name: str) -> None:
    """No local rejection, whatever the name.

    This is the behaviour that replaced a locally raised ValueError. An unknown
    name is the service's 400 to give, and that 400 names the tiers it accepts
    -- which a released SDK cannot, since the set can grow without it. Included
    are the full enum label and the old tag numbers: both were meaningful while
    the field was an enum, and neither is a tier name now.
    """
    request = _request(tier=name)
    assert request.HasField("tier")
    assert request.tier == name


def test_nothing_in_the_tier_path_raises() -> None:
    """Belt and braces on the above: no input to `tier` is an SDK error."""
    for name in ["", " ", "pro", "nonsense", "\n", "pro "]:
        _request(tier=name)


def test_the_two_services_take_the_same_arguments() -> None:
    assert list(inspect.signature(AsyncSearchService.search).parameters) == list(
        inspect.signature(SearchService.search).parameters
    )


def test_tier_is_a_monitor_search_request_field() -> None:
    """Monitors derive their accepted keys from the descriptor, so a monitored
    search can carry a tier without a second edit."""
    from seltz.services.monitor_service import _SEARCH_REQUEST_FIELDS

    assert "tier" in _SEARCH_REQUEST_FIELDS
