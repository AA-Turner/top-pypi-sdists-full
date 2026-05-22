"""Factory classes for generating test objects with factory boy."""

import urllib.parse
from typing import Generic, TypeVar

import factory
import factory.fuzzy

from eveuniverse.constants import EveCategoryId, EveGroupId, EveRegionId, EveTypeId
from eveuniverse.models import (
    EveAsteroidBelt,
    EveBloodline,
    EveCategory,
    EveConstellation,
    EveDogmaAttribute,
    EveDogmaEffect,
    EveEntity,
    EveFaction,
    EveGraphic,
    EveGroup,
    EveMarketGroup,
    EveMarketPrice,
    EveMoon,
    EvePlanet,
    EveRace,
    EveRegion,
    EveSolarSystem,
    EveStar,
    EveStargate,
    EveStation,
    EveStationService,
    EveType,
)

T = TypeVar("T")

factory.Faker._DEFAULT_LOCALE = "en_US"

_POSITION_MIN = -100_000_000_000_000_000
_POSITION_MAX = 100_000_000_000_000_000
_BASE_URL = "https://esi.evetech.net/"


def make_esi_url(path: str) -> str:
    if path.startswith("/"):
        raise ValueError("path can not start with a slash")
    if path.endswith("/"):
        raise ValueError("path can not end with a slash")

    url = urllib.parse.urljoin(_BASE_URL, path)
    return url


class BaseMetaFactory(Generic[T], factory.base.FactoryMetaClass):
    def __call__(cls, *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)


# Entities


class PositionFactory(factory.DictFactory, metaclass=BaseMetaFactory[dict]):
    x = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    y = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    z = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)


class EveEntityFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveEntity]
):
    class Meta:
        model = EveEntity
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 90_900_001 + n)
    category = EveEntity.CATEGORY_CHARACTER
    name = factory.LazyAttribute(lambda o: f"character_{o.id}")


class EveEntityAllianceFactory(EveEntityFactory):
    id = factory.Sequence(lambda n: 99_900_001 + n)
    name = factory.LazyAttribute(lambda o: f"alliance_{o.id}")
    category = EveEntity.CATEGORY_ALLIANCE


class EveEntityCharacterFactory(EveEntityFactory):
    pass


class EveEntityCorporationFactory(EveEntityFactory):
    id = factory.Sequence(lambda n: 98_900_001 + n)
    name = factory.LazyAttribute(lambda o: f"corporation_{o.id}")
    category = EveEntity.CATEGORY_CORPORATION


class EveEntityFactionFactory(EveEntityFactory):
    id = factory.Sequence(lambda n: 509_001 + n)
    name = factory.LazyAttribute(lambda o: f"faction_{o.id}")
    category = EveEntity.CATEGORY_FACTION


class EveEntityUnresolvedFactory(EveEntityFactory):
    name = ""
    category = ""


class EveRaceFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveRace]
):
    class Meta:
        model = EveRace
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 1 + n)
    alliance_id = factory.fuzzy.FuzzyInteger(590_001, 600_000)
    name = factory.Faker("color_name")
    description = factory.Faker("paragraph")


# Types


class EveCategoryFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveCategory]
):
    class Meta:
        model = EveCategory
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 100_000 + n)
    name = factory.Faker("color_name")
    published = True


class CelestialCategoryFactory(EveCategoryFactory):
    id = EveCategoryId.CELESTIAL
    name = "Celestial"


class EveGroupFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveGroup]
):
    class Meta:
        model = EveGroup
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 200_000 + n)
    name = factory.Faker("color_name")
    eve_category = factory.SubFactory(EveCategoryFactory)
    published = True


class EveDogmaAttributeFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveDogmaAttribute]
):
    class Meta:
        model = EveDogmaAttribute
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 100 + n)
    name = factory.Faker("color_name")
    description = factory.Faker("paragraph")
    display_name = factory.Faker("word")
    icon_id = factory.fuzzy.FuzzyInteger(10, 10_000)
    published = True


class EveDogmaEffectFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveDogmaEffect]
):
    class Meta:
        model = EveDogmaEffect
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 100 + n)
    name = factory.Faker("color_name")

    description = factory.Faker("paragraph")
    display_name = factory.Faker("word")
    icon_id = factory.fuzzy.FuzzyInteger(10, 10_000)


class EveGraphicFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveGraphic]
):
    class Meta:
        model = EveGraphic
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 100 + n)
    name = factory.Faker("color_name")
    sof_dna = factory.Faker("word")
    sof_fation_name = factory.Faker("word")
    sof_hull_name = factory.Faker("word")
    sof_race_name = factory.Faker("word")


class EveMarketGroupFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveMarketGroup]
):
    class Meta:
        model = EveMarketGroup
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 100 + n)
    name = factory.Faker("color_name")
    description = factory.Faker("paragraph")


class EveTypeFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveType]
):
    class Meta:
        model = EveType
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 300_000 + n)
    name = factory.Faker("color_name")
    description = factory.Faker("paragraph")
    eve_group = factory.SubFactory(EveGroupFactory)
    published = True


class AsteroidBeltTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.CELESTIAL,
        eve_category__name="Celestial",
        id=EveGroupId.ASTEROID_BELT,
        name="Asteroid Belt",
    )
    id = EveTypeId.ASTEROID_BELT
    name = "Asteroid Belt"


class AllianceTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.OWNER,
        eve_category__name="Owner",
        id=EveGroupId.ALLIANCE,
        name="Alliance",
    )
    id = 16159
    name = "Alliance"


class CharacterTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.OWNER,
        eve_category__name="Owner",
        id=EveGroupId.CHARACTER,
        name="Character",
    )


class CorporationTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.OWNER,
        eve_category__name="Owner",
        id=EveGroupId.CORPORATION,
        name="Corporation",
    )
    id = 2
    name = "Corporation"


class CitadelTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.STRUCTURE,
        eve_category__name="Structure",
        id=EveGroupId.CITADEL,
        name="Citadel",
    )


class BlueprintTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.BLUEPRINT,
        eve_category__name="Blueprint",
        id=105,
        name="Frigate Blueprint",
    )


class MoonTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.CELESTIAL,
        eve_category__name="Celestial",
        id=EveGroupId.MOON,
        name="Moon",
    )
    id = EveTypeId.MOON
    name = "Moon"


class PlanetTypeFactory(EveTypeFactory):
    class Params:
        planet_type = "Barren"

    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.CELESTIAL,
        eve_category__name="Celestial",
        id=EveGroupId.PLANET,
        name="Planet",
    )
    name = factory.LazyAttribute(lambda o: f"Planet ({o.planet_type})")


class SolarSystemTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.CELESTIAL,
        eve_category__name="Celestial",
        id=EveGroupId.SOLAR_SYSTEM,
        name="Solar System",
    )
    id = EveTypeId.SOLAR_SYSTEM
    name = "Solar System"


class StarTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.CELESTIAL,
        eve_category__name="Celestial",
        id=EveGroupId.STAR,
        name="Star",
    )


class StationTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.CELESTIAL,
        eve_category__name="Celestial",
        id=EveGroupId.STATION,
        name="Station",
    )


class SKINTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.SKIN,
        eve_category__name="SKINs",
        id=EveGroupId.PERMANENT_SKIN,
        name="Permanent SKIN",
    )


class ShipTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.SHIP,
        eve_category__name="Ship",
        id=EveGroupId.FRIGATE,
        name="Frigate",
    )


class StargateTypeFactory(EveTypeFactory):
    eve_group = factory.SubFactory(
        EveGroupFactory,
        eve_category__id=EveCategoryId.CELESTIAL,
        eve_category__name="Celestial",
        id=EveGroupId.STARGATE,
        name="Stargate",
    )


class EveMarketPriceFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveMarketPrice]
):
    class Meta:
        model = EveMarketPrice

    adjusted_price = factory.fuzzy.FuzzyFloat(1, 100_000_000)
    average_price = factory.fuzzy.FuzzyFloat(1, 100_000_000)
    eve_type = factory.SubFactory(EveTypeFactory)


# Map


class EveRegionFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveRegion]
):
    class Meta:
        model = EveRegion
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 10_900_000 + n)
    name = factory.Faker("country")
    description = factory.Faker("paragraph")


class EveConstellationFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveConstellation]
):
    class Meta:
        model = EveConstellation
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 20_900_000 + n)
    name = factory.Faker("country")
    eve_region = factory.SubFactory(EveRegionFactory)
    position_x = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_y = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_z = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)


class EveSolarSystemFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveSolarSystem]
):
    class Meta:
        model = EveSolarSystem
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 30_900_000 + n)
    name = factory.Faker("city")
    eve_constellation = factory.SubFactory(EveConstellationFactory)
    eve_star = None
    position_x = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_y = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_z = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    security_status = factory.fuzzy.FuzzyFloat(-1, 1)


class EveSolarSystemNullSecFactory(EveSolarSystemFactory):
    security_status = -1.0


class EveSolarSystemLowSecFactory(EveSolarSystemFactory):
    security_status = 0.3


class EveSolarSystemHighSecFactory(EveSolarSystemFactory):
    security_status = 0.9


class EveSolarSystemWSpaceFactory(EveSolarSystemFactory):
    id = factory.Sequence(lambda n: 31_900_000 + n)
    security_status = -1.0


class EveSolarSystemTrigSpaceFactory(EveSolarSystemFactory):
    eve_constellation = factory.SubFactory(
        EveConstellationFactory,
        eve_region__id=EveRegionId.POCHVEN,
    )
    security_status = -1.0


class EveSolarSystemAbyssalSpaceFactory(EveSolarSystemFactory):
    id = factory.Sequence(lambda n: 32_900_000 + n)
    security_status = -1.0


class EveStarFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveStar]
):
    class Meta:
        model = EveStar
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 40_940_000 + n)
    name = factory.Faker("street_name")
    age = factory.fuzzy.FuzzyInteger(0, 100_000_000_000)
    eve_type = factory.SubFactory(StarTypeFactory)
    luminosity = factory.fuzzy.FuzzyFloat(0, 1)
    radius = factory.fuzzy.FuzzyInteger(0, 100_000_000)
    spectral_class = "M6 V"
    temperature = factory.fuzzy.FuzzyInteger(0, 10_000)


class EveStationServiceFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveStationService]
):
    class Meta:
        model = EveStationService

    name = factory.Faker("word")


class EveStationFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveStation]
):
    class Meta:
        model = EveStation
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 40_950_000 + n)
    name = factory.Faker("city")
    eve_race = factory.SubFactory(EveRaceFactory)
    eve_solar_system = factory.SubFactory(EveSolarSystemFactory)
    eve_type = factory.SubFactory(StationTypeFactory)
    max_dockable_ship_volume = factory.fuzzy.FuzzyFloat(0, 100_000_000)
    office_rental_cost = factory.fuzzy.FuzzyFloat(0, 100_000_000)
    owner_id = factory.fuzzy.FuzzyInteger(0, 500_000)
    position_x = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_y = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_z = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    reprocessing_efficiency = factory.fuzzy.FuzzyFloat(0, 1)
    reprocessing_stations_take = factory.fuzzy.FuzzyFloat(0, 100_000)

    @factory.post_generation
    def services(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.services.add(*extracted)


class EvePlanetFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EvePlanet]
):
    class Meta:
        model = EvePlanet
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 40_910_000 + n)
    name = factory.Faker("street_name")
    eve_solar_system = factory.SubFactory(EveSolarSystemFactory)
    eve_type = factory.SubFactory(PlanetTypeFactory)
    position_x = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_y = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_z = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)


class EveAsteroidBeltFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveAsteroidBelt]
):
    class Meta:
        model = EveAsteroidBelt
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 40_930_000 + n)
    name = factory.Faker("city")
    eve_planet = factory.SubFactory(EvePlanetFactory)
    position_x = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_y = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_z = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)


class EveMoonFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveMoon]
):
    class Meta:
        model = EveMoon
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 40_920_000 + n)
    name = factory.Faker("street_name")
    eve_planet = factory.SubFactory(EvePlanetFactory)
    position_x = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_y = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_z = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)


class EveStargateFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveStargate]
):
    class Meta:
        model = EveStargate
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 50_900_000 + n)
    name = factory.Faker("city")
    eve_solar_system = factory.SubFactory(EveSolarSystemFactory)
    eve_type = factory.SubFactory(StargateTypeFactory)
    position_x = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_y = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)
    position_z = factory.fuzzy.FuzzyFloat(_POSITION_MIN, _POSITION_MAX)


# Other


class EveBloodlineFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveBloodline]
):
    class Meta:
        model = EveBloodline
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 1 + n)
    name = factory.Faker("city")
    charisma = factory.fuzzy.FuzzyInteger(17, 32)
    corporation_id = factory.fuzzy.FuzzyInteger(1_000_000, 2_000_000)
    description = factory.Faker("paragraph")
    eve_ship_type = factory.SubFactory(ShipTypeFactory)
    intelligence = factory.fuzzy.FuzzyInteger(17, 32)
    memory = factory.fuzzy.FuzzyInteger(17, 32)
    perception = factory.fuzzy.FuzzyInteger(17, 32)
    willpower = factory.fuzzy.FuzzyInteger(17, 32)


class EveFactionFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveFaction]
):
    class Meta:
        model = EveFaction
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 509_001 + n)
    name = factory.Sequence(lambda n: f"faction{n}")

    description = factory.Faker("paragraph")
    corporation_id = factory.fuzzy.FuzzyInteger(1_000_000, 1_999_999)
    eve_solar_system = factory.SubFactory(EveSolarSystemFactory)
    is_unique = True
    militia_corporation_id = factory.fuzzy.FuzzyInteger(1_000_000, 1_999_999)
    size_factor = factory.fuzzy.FuzzyInteger(1, 5)
    station_count = factory.fuzzy.FuzzyInteger(1, 100)
    station_system_count = factory.fuzzy.FuzzyInteger(1, 100)
