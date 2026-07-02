from typing import Generic, TypeVar

import factory
import factory.fuzzy

from memberaudit.models import CharacterRole
from memberaudit.tests.testdata.factories_2 import LocationStationFactory

from memberaudit_securegroups.models import (
    ActivityFilter,
    AgeFilter,
    AssetFilter,
    ComplianceFilter,
    CorporationRoleFilter,
    CorporationTitleFilter,
    HomeStationFilter,
    SkillPointFilter,
    SkillSetFilter,
    TimeInCorporationFilter,
)

T = TypeVar("T")


class BaseMetaFactory(Generic[T], factory.base.FactoryMetaClass):
    def __call__(cls, *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)


class ActivityFilterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[ActivityFilter]
):
    class Meta:
        model = ActivityFilter

    inactivity_threshold = factory.fuzzy.FuzzyInteger(1, 90)


class AgeFilterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[AgeFilter]
):
    class Meta:
        model = AgeFilter

    age_threshold = factory.fuzzy.FuzzyInteger(1, 90)


class AssetFilterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[AssetFilter]
):
    class Meta:
        model = AssetFilter

    @factory.post_generation
    def assets(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.assets.add(*extracted)


class ComplianceFilterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[ComplianceFilter]
):
    class Meta:
        model = ComplianceFilter

    reversed_logic = False


class CorporationRoleFilterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[CorporationRoleFilter]
):
    class Meta:
        model = CorporationRoleFilter

    role = CharacterRole.Role.DIRECTOR

    @factory.post_generation
    def corporations(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.corporations.add(*extracted)


class CorporationTitleFilterFactory(
    factory.django.DjangoModelFactory,
    metaclass=BaseMetaFactory[CorporationTitleFilter],
):
    class Meta:
        model = CorporationTitleFilter

    title = "title"

    @factory.post_generation
    def corporations(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.corporations.add(*extracted)


class HomeStationFilterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[HomeStationFilter]
):
    class Meta:
        model = HomeStationFilter

    home_station = factory.SubFactory(LocationStationFactory)
    include_alts = False


class SkillPointFilterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[SkillPointFilter]
):
    class Meta:
        model = SkillPointFilter

    skill_point_threshold = factory.fuzzy.FuzzyInteger(1_000_000, 50_000_000)


class SkillSetFilterFilterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[SkillSetFilter]
):
    class Meta:
        model = SkillSetFilter

    character_type = SkillSetFilter.CharacterType.ANY

    @factory.post_generation
    def skill_sets(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.skill_sets.add(*extracted)


class TimeInCorporationFilterFactory(
    factory.django.DjangoModelFactory,
    metaclass=BaseMetaFactory[TimeInCorporationFilter],
):
    class Meta:
        model = TimeInCorporationFilter

    minimum_days = 30
