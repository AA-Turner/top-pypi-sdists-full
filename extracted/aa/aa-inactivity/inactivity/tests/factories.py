import datetime as dt
from typing import Generic, TypeVar

import factory
import factory.fuzzy

from django.contrib.auth.models import Group
from django.db.models import Max
from django.utils.timezone import now

from allianceauth.authentication.models import State
from app_utils.testdata_factories import UserMainFactory

from inactivity.models import (
    InactivityPing,
    InactivityPingConfig,
    LeaveOfAbsence,
    Webhook,
)

T = TypeVar("T")


class BaseMetaFactory(Generic[T], factory.base.FactoryMetaClass):
    def __call__(cls, *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)


# class ResponseFactory(factory.Factory):
#     class Meta:
#         model = requests.Response

#     @factory.post_generation
#     def default_auth_group(self, create, extracted, **kwargs):
#         if not create:
#             return
#         self.status_code = 200
#         self.url = factory.Faker("url")


class GroupFactory(factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[Group]):
    class Meta:
        model = Group
        django_get_or_create = ("name",)

    name = factory.Faker("job")

    @factory.post_generation
    def default_auth_group(self, create, extracted, **kwargs):
        if not create:
            return
        self.authgroup.internal = False
        self.authgroup.hidden = False
        self.authgroup.save()


class StateFactory(factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[State]):
    class Meta:
        model = State
        django_get_or_create = ("name", "priority")

    name = factory.Faker("color")

    @factory.lazy_attribute
    def priority(self):
        last_id = State.objects.aggregate(Max("priority"))["priority__max"] or 100
        return last_id + 10

    @factory.post_generation
    def member_characters(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obj in extracted:
                self.member_characters.add(obj)

    @factory.post_generation
    def member_corporations(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obj in extracted:
                self.member_corporations.add(obj)

    @factory.post_generation
    def member_alliances(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obj in extracted:
                self.member_alliances.add(obj)

    @factory.post_generation
    def member_factions(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obj in extracted:
                self.member_factions.add(obj)


class UserMainRequestorFactory(UserMainFactory):
    """A normal user with access to this app."""

    permissions__ = ["inactivity.basic_access", "memberaudit.basic_access"]

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)


class UserMainManagerFactory(UserMainFactory):
    """A user who can manage loa requests."""

    permissions__ = ["inactivity.basic_access", "inactivity.manage_leave"]


class LeaveOfAbsenceFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[LeaveOfAbsence]
):
    class Meta:
        model = LeaveOfAbsence

    class Params:
        is_approved = factory.Trait(
            approver=factory.SubFactory(UserMainManagerFactory), reason=None
        )
        is_denied = factory.Trait(
            approver=factory.SubFactory(UserMainManagerFactory),
            reason=factory.Faker("sentence"),
        )

    user = factory.SubFactory(UserMainRequestorFactory)
    start = factory.fuzzy.FuzzyDateTime(
        start_dt=now() + dt.timedelta(days=1),
        end_dt=now() + dt.timedelta(days=7),
        force_microsecond=0,
    )
    reason = None
    end = factory.LazyAttribute(
        lambda obj: factory.fuzzy.FuzzyDateTime(
            start_dt=obj.start,
            end_dt=obj.start + dt.timedelta(days=7),
            force_microsecond=0,
        ).fuzz()
    )
    notes = factory.Faker("sentence")


class InactivityPingConfigFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[InactivityPingConfig]
):
    class Meta:
        model = InactivityPingConfig

    name = factory.Faker("city")
    days = 3
    text = factory.Faker("sentences")

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obj in extracted:
                self.groups.add(obj)

    @factory.post_generation
    def states(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obj in extracted:
                self.states.add(obj)


class InactivityPingFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[InactivityPing]
):
    class Meta:
        model = InactivityPing

    config = factory.SubFactory(InactivityPingConfigFactory)
    user = factory.SubFactory(UserMainRequestorFactory)


class WebhookFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[Webhook]
):
    class Meta:
        model = Webhook
        django_get_or_create = ("name", "url")

    name = factory.Faker("color")
    notification_types = [
        Webhook.NotificationType.INACTIVE_USER,
        Webhook.NotificationType.LOA_APPROVED,
        Webhook.NotificationType.LOA_NEW,
    ]

    @factory.lazy_attribute
    def url(self):
        snowflake = factory.fuzzy.FuzzyInteger(
            100000000000000000, 1000000000000000000
        ).fuzz()
        token = factory.fuzzy.FuzzyText(length=68).fuzz()
        url = f"https://discord.com/api/webhooks/{snowflake}/{token}"
        return url

    @factory.post_generation
    def ping_configs(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for obj in extracted:
                self.ping_configs.add(obj)
