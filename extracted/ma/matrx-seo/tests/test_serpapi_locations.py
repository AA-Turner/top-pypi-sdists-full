from __future__ import annotations

from typing import Any

import pytest

from matrx_seo.providers.serpapi_locations import (
    SerpApiLocationCatalogUnavailable,
    SerpApiLocationResolver,
    SerpApiLocationUnresolved,
    normalize_location_query,
)

# Rows shaped exactly like live https://serpapi.com/locations.json responses
# (captured 2026-08-15). The catalogue text-matches `name`, NOT the canonical
# form — which is why "Newport Beach, CA" returns nothing at all.
_CATALOG: dict[str, list[dict[str, Any]]] = {
    "newport beach,ca": [],
    "newport beach": [
        {
            "name": "Newport Beach",
            "canonical_name": "Newport Beach,California,United States",
            "target_type": "City",
            "reach": 297000,
        }
    ],
    "austin,texas,united states": [
        {
            "name": "Austin",
            "canonical_name": "Austin,Texas,United States",
            "target_type": "City",
            "reach": 6440000,
        },
        {
            "name": "Downtown Austin",
            "canonical_name": "Downtown Austin,Texas,United States",
            "target_type": "Neighborhood",
            "reach": 1180000,
        },
    ],
    "london,uk": [],
    "london": [
        {
            "name": "London",
            "canonical_name": "London,England,United Kingdom",
            "target_type": "City",
            "reach": 39400000,
        },
        {
            "name": "London",
            "canonical_name": "London,Ontario,Canada",
            "target_type": "City",
            "reach": 1300000,
        },
        {
            "name": "London",
            "canonical_name": "London,Kentucky,United States",
            "target_type": "City",
            "reach": 66000,
        },
        {
            "name": "London TV Region",
            "canonical_name": "London TV Region,England,United Kingdom",
            "target_type": "TV Region",
            "reach": 42900000,
        },
    ],
    "paris,france": [
        {
            "name": "Paris",
            "canonical_name": "Paris,Paris,Ile-de-France,France",
            "target_type": "City",
            "reach": 28700000,
        },
        {
            "name": "Paris",
            "canonical_name": "Paris,Ile-de-France,France",
            "target_type": "Department",
            "reach": 28700000,
        },
    ],
    "atlantis,ca": [],
    "atlantis": [],
}


class FakeTransport:
    def __init__(self, catalog: dict[str, list[dict[str, Any]]] | None = None) -> None:
        self.catalog = catalog if catalog is not None else _CATALOG
        self.calls: list[str] = []

    async def search(self, query: str, limit: int) -> list[dict[str, Any]]:
        del limit
        self.calls.append(query)
        return list(self.catalog.get(query.casefold(), []))


class BrokenTransport:
    async def search(self, query: str, limit: int) -> list[dict[str, Any]]:
        del query, limit
        raise SerpApiLocationCatalogUnavailable("simulated outage")


def resolver(transport: Any | None = None) -> SerpApiLocationResolver:
    return SerpApiLocationResolver(transport=transport or FakeTransport())


def test_normalize_strips_the_spaces_serpapi_rejects() -> None:
    assert normalize_location_query(" Newport Beach , California , United States ") == (
        "Newport Beach,California,United States"
    )
    with pytest.raises(ValueError):
        normalize_location_query("  ,  ")


@pytest.mark.asyncio
async def test_the_live_defect_state_resolves_instead_of_failing_forever() -> None:
    # rank_target ce251dfc ('gastroenterology' -> iopbm.com) carried this exact
    # string and 400'd on every scheduled check since 2026-07-27.
    assert await resolver().resolve("Newport Beach, CA") == (
        "Newport Beach,California,United States"
    )


@pytest.mark.asyncio
async def test_already_canonical_name_is_returned_unchanged_in_one_call() -> None:
    transport = FakeTransport()
    assert await resolver(transport).resolve("Austin,Texas,United States") == (
        "Austin,Texas,United States"
    )
    # An exact hit must never fall through to the second (head-only) lookup.
    assert transport.calls == ["Austin,Texas,United States"]


@pytest.mark.asyncio
async def test_spaced_canonical_form_is_accepted() -> None:
    assert await resolver().resolve("Austin, Texas, United States") == (
        "Austin,Texas,United States"
    )


@pytest.mark.asyncio
async def test_country_abbreviation_disambiguates_a_shared_city_name() -> None:
    assert await resolver().resolve("London, UK") == "London,England,United Kingdom"


@pytest.mark.asyncio
async def test_city_type_breaks_a_tie_against_a_coextensive_region() -> None:
    assert await resolver().resolve("Paris, France") == "Paris,Paris,Ile-de-France,France"


@pytest.mark.asyncio
async def test_ambiguous_name_is_refused_with_canonical_suggestions() -> None:
    with pytest.raises(SerpApiLocationUnresolved) as excinfo:
        await resolver().resolve("London")
    error = excinfo.value
    assert error.ambiguous is True
    # Suggestions are ranked by reach and are exact canonical strings.
    assert error.suggestions[0] == "London,England,United Kingdom"
    assert "London,Ontario,Canada" in error.suggestions
    assert "matches more than one place" in str(error)


@pytest.mark.asyncio
async def test_unknown_name_is_refused_and_is_a_valueerror_for_the_422_path() -> None:
    with pytest.raises(ValueError) as excinfo:
        await resolver().resolve("Atlantis, CA")
    assert isinstance(excinfo.value, SerpApiLocationUnresolved)
    assert excinfo.value.ambiguous is False
    assert "not a SerpAPI location" in str(excinfo.value)


@pytest.mark.asyncio
async def test_catalog_outage_raises_its_own_type_not_a_refusal() -> None:
    # Never a ValueError: an unreachable validator must not refuse a creation.
    with pytest.raises(SerpApiLocationCatalogUnavailable):
        await resolver(BrokenTransport()).resolve("Newport Beach, CA")


@pytest.mark.asyncio
async def test_results_are_cached_so_repeat_creations_do_not_re_query() -> None:
    transport = FakeTransport()
    instance = resolver(transport)
    assert await instance.resolve("Newport Beach, CA")
    calls_after_first = len(transport.calls)
    assert await instance.resolve("newport beach,  ca") == (
        "Newport Beach,California,United States"
    )
    assert len(transport.calls) == calls_after_first

    # Refusals are cached too — a bad name must not hammer the catalogue.
    with pytest.raises(SerpApiLocationUnresolved):
        await instance.resolve("London")
    calls_after_refusal = len(transport.calls)
    with pytest.raises(SerpApiLocationUnresolved):
        await instance.resolve("London")
    assert len(transport.calls) == calls_after_refusal


@pytest.mark.asyncio
async def test_live_catalog_matches_the_fixtures(request: pytest.FixtureRequest) -> None:
    """Truth-vs-code check against the REAL catalogue — the fixtures above are
    only as good as their agreement with SerpAPI. Free endpoint (no API key, no
    search credit); opt in with --run-live-serpapi-locations."""
    if not request.config.getoption("--run-live-serpapi-locations"):
        pytest.skip("requires --run-live-serpapi-locations (network)")
    live = SerpApiLocationResolver()
    assert await live.resolve("Newport Beach, CA") == "Newport Beach,California,United States"
    assert await live.resolve("Austin, Texas, United States") == "Austin,Texas,United States"
    assert await live.resolve("London, UK") == "London,England,United Kingdom"
    with pytest.raises(SerpApiLocationUnresolved):
        await live.resolve("London")
