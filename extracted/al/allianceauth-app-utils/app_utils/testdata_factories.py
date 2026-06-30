"""This module provides factories for generating test objects from Django and AA Models.

Important: You need to add the dependency ``factory_boy`` to your test environment.
"""

from typing import Generic, TypeVar

import factory
import factory.fuzzy

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Max

from allianceauth.authentication.models import State
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from allianceauth.groupmanagement.models import AuthGroup

from .django import add_permissions_to_user_by_name, permission_by_name
from .testing import add_character_to_user

T = TypeVar("T")
User = get_user_model()


class BaseMetaFactory(Generic[T], factory.base.FactoryMetaClass):
    """:meta private:"""

    def __call__(cls, *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)


class EveAllianceInfoFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveAllianceInfo]
):
    """Generate an EveAllianceInfo object."""

    class Meta:
        model = EveAllianceInfo
        django_get_or_create = ("alliance_id", "alliance_name")

    alliance_name = factory.Faker("catch_phrase")
    alliance_ticker = factory.LazyAttribute(lambda obj: obj.alliance_name[:4].upper())
    executor_corp_id = 0

    @factory.lazy_attribute
    def alliance_id(self):
        last_id = (
            EveAllianceInfo.objects.aggregate(Max("alliance_id"))["alliance_id__max"]
            or 99_000_000
        )
        return last_id + 1


class EveCorporationInfoFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveCorporationInfo]
):
    """Generate an EveCorporationInfo object.

    Will create an alliance by default. Can be turned off with `create_alliance=False`.
    """

    class Meta:
        model = EveCorporationInfo
        django_get_or_create = ("corporation_id", "corporation_name")

    corporation_name = factory.Faker("catch_phrase")
    corporation_ticker = factory.LazyAttribute(
        lambda obj: obj.corporation_name[:4].upper()
    )
    member_count = factory.fuzzy.FuzzyInteger(1000)

    @factory.lazy_attribute
    def corporation_id(self):
        last_id = (
            EveCorporationInfo.objects.aggregate(Max("corporation_id"))[
                "corporation_id__max"
            ]
            or 98_000_000
        )
        return last_id + 1

    @factory.post_generation
    def create_alliance(obj, create, extracted, **kwargs):
        if not create or extracted is False or obj.alliance:
            return
        obj.alliance = EveAllianceInfoFactory(executor_corp_id=obj.corporation_id)


class EveCharacterFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[EveCharacter]
):
    """Generate an EveCharacter object."""

    class Meta:
        model = EveCharacter
        django_get_or_create = ("character_id", "character_name")
        exclude = ("corporation",)

    character_name = factory.Faker("name")
    corporation = factory.SubFactory(EveCorporationInfoFactory)
    corporation_id = factory.LazyAttribute(lambda obj: obj.corporation.corporation_id)
    corporation_name = factory.LazyAttribute(
        lambda obj: obj.corporation.corporation_name
    )
    corporation_ticker = factory.LazyAttribute(
        lambda obj: obj.corporation.corporation_ticker
    )

    @factory.lazy_attribute
    def character_id(self):
        last_id = (
            EveCharacter.objects.aggregate(Max("character_id"))["character_id__max"]
            or 90_000_000
        )
        return last_id + 1

    @factory.lazy_attribute
    def alliance_id(self):
        return (
            self.corporation.alliance.alliance_id if self.corporation.alliance else None
        )

    @factory.lazy_attribute
    def alliance_name(self):
        return (
            self.corporation.alliance.alliance_name if self.corporation.alliance else ""
        )

    @factory.lazy_attribute
    def alliance_ticker(self):
        return (
            self.corporation.alliance.alliance_ticker
            if self.corporation.alliance
            else ""
        )


class GroupFactory(factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[Group]):
    """Generate a Group for AllianceAuth.

    The authgroup can optionally be configured by providing parameters to `authgroup`.
    For example: `GroupFactory(authgroup__public=True)`
    """

    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"Group #{n + 1}")

    @factory.post_generation
    def authgroup(self, create, extracted, **kwargs):
        authgroup: AuthGroup = self.authgroup

        if kwargs:
            for field in ["states", "group_leaders", "group_leader_groups"]:
                if field in kwargs:
                    x = kwargs.pop(field)
                    getattr(self.authgroup, field).add(*x)

            for field, value in kwargs.items():
                setattr(authgroup, field, value)

        authgroup.save()


class StateFactory(factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[State]):
    """Generate a State object.

    Args:
        member_alliances (List[EveAlliance]): Members of alliances that have this state (optional)
        member_characters (List[EveCharacter]): Characters that have this state (optional)
        member_corporations (List[EveCorporation]): Members of corporations that have this state (optional)
        member_factions (List[EveFaction]): Members of factions that have this state (optional)
        permissions (List[str]): Names of permissions of this state (optional),
            e.g. ``["moonmining.basic_access"]``
    """

    class Meta:
        model = State

    name = factory.LazyAttribute(lambda o: f"State #{o.priority}")
    priority = factory.Sequence(lambda n: n + 900)
    public = False

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        permissions = [permission_by_name(p) for p in set(extracted)]
        self.permissions.add(*permissions)

    @factory.post_generation
    def member_characters(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.member_characters.add(*extracted)

    @factory.post_generation
    def member_corporations(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.member_corporations.add(*extracted)

    @factory.post_generation
    def member_alliances(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.member_alliances.add(*extracted)

    @factory.post_generation
    def member_factions(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.member_factions.add(*extracted)


class UserFactory(factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[User]):
    """Generate a User object.

    Args:
        permissions (List[str]): Names of permissions (optional),
            e.g. ``["moonmining.basic_access"]``
    """

    class Meta:
        model = User
        django_get_or_create = ("username",)
        exclude = ("_generated_name",)

    _generated_name = factory.Faker("name")
    username = factory.LazyAttribute(lambda obj: obj._generated_name.replace(" ", "_"))
    first_name = factory.LazyAttribute(lambda obj: obj._generated_name.split(" ")[0])
    last_name = factory.LazyAttribute(lambda obj: obj._generated_name.split(" ")[1])
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com"
    )

    @factory.post_generation
    def permissions(obj, create, extracted, **kwargs):
        """Set default permissions. Overwrite with `permissions=["app.perm1"]`."""
        if not create or not extracted:
            return

        add_permissions_to_user_by_name(obj, extracted)

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        """Reset permission cache to force an update."""
        super()._after_postgeneration(obj, create, results)
        if hasattr(obj, "_perm_cache"):
            del obj._perm_cache
        if hasattr(obj, "_user_perm_cache"):
            del obj._user_perm_cache


class UserMainFactory(UserFactory):
    """Generate a User object with main character.

    Args:
        main_character__character (EveCharacter): Character to be used as main (optional)
        main_character__scopes (List[str]): ESI scope names (optional),
            e.g. ``["esi-characters.read_contacts.v1"]``
        permissions (List[str]): Names of permissions (optional),
            e.g. ``["moonmining.basic_access"]``
    """

    @factory.post_generation
    def main_character(obj, create, _extracted, **kwargs):
        if not create:
            return
        if "character" in kwargs:
            character = kwargs["character"]
        else:
            character_name = f"{obj.first_name} {obj.last_name}"
            character = EveCharacterFactory(character_name=character_name)

        scopes = kwargs.get("scopes", None)
        add_character_to_user(
            user=obj, character=character, is_main=True, scopes=scopes
        )
