"""Shared ESI provider for Eve Universe."""

from pathlib import Path

from esi.openapi_clients import ESIClientProvider

from . import __version__

spec_file = Path(__file__).parent / "openapi_2025-12-16.json"
esi = ESIClientProvider(
    compatibility_date="2025-12-16",
    ua_appname="django-eveuniverse",
    ua_version=__version__,
    operations=[
        "GetDogmaAttributes",
        "GetDogmaAttributesAttributeId",
        "GetDogmaEffects",
        "GetDogmaEffectsEffectId",
        "GetMarketsGroups",
        "GetMarketsGroupsMarketGroupId",
        "GetMarketsPrices",
        "GetStatus",
        "GetUniverseAncestries",
        "GetUniverseAsteroidBeltsAsteroidBeltId",
        "GetUniverseBloodlines",
        "GetUniverseCategories",
        "GetUniverseCategoriesCategoryId",
        "GetUniverseConstellations",
        "GetUniverseConstellationsConstellationId",
        "GetUniverseFactions",
        "GetUniverseGraphics",
        "GetUniverseGraphicsGraphicId",
        "GetUniverseGroups",
        "GetUniverseGroupsGroupId",
        "GetUniverseMoonsMoonId",
        "GetUniversePlanetsPlanetId",
        "GetUniverseRaces",
        "GetUniverseRegions",
        "GetUniverseRegionsRegionId",
        "GetUniverseStargatesStargateId",
        "GetUniverseStarsStarId",
        "GetUniverseStationsStationId",
        "GetUniverseSystems",
        "GetUniverseSystemsSystemId",
        "GetUniverseTypes",
        "GetUniverseTypesTypeId",
        "PostRoute",
        "PostUniverseIds",
        "PostUniverseNames",
    ],
    spec_file=spec_file,
)
