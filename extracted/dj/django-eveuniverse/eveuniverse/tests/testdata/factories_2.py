"""Factory classes for generating test objects with factory boy."""

from typing import Generic, TypeVar

import factory
import factory.fuzzy

from eveuniverse.models import (
    EveCategory,
    EveConstellation,
    EveEntity,
    EveGroup,
    EveMoon,
    EvePlanet,
    EveRegion,
    EveSolarSystem,
    EveType,
)

T = TypeVar("T")

factory.Faker._DEFAULT_LOCALE = "en_US"

_POSITION_MIN = -100_000_000_000_000_000
_POSITION_MAX = 100_000_000_000_000_000


class BaseMetaFactory(Generic[T], factory.base.FactoryMetaClass):
    def __call__(cls, *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)


class EveCategoryFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveCategory]
):
    class Meta:
        model = EveCategory
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 100_000 + n)
    name = factory.Faker("color_name")
    published = True


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


class EvePlanetFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EvePlanet]
):
    class Meta:
        model = EvePlanet
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 40_910_000 + n)
    name = factory.Faker("street_name")
    eve_solar_system = factory.SubFactory(EveSolarSystemFactory)
    eve_type = factory.SubFactory(EveTypeFactory)
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


class EveEntityFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveEntity]
):
    class Meta:
        model = EveEntity
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 90_000_001 + n)
    category = EveEntity.CATEGORY_CHARACTER
    name = factory.Faker("color_name")
