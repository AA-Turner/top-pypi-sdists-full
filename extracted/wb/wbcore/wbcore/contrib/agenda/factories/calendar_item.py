import random

import factory
from django.utils.timezone import make_aware
from faker import Faker
from pandas.tseries.offsets import BDay
from psycopg.types.range import TimestamptzRange

from wbcore.contrib.agenda.models import CalendarItem
from wbcore.contrib.icons.icons import WBIcon

from .conference_room import ConferenceRoomFactory

fake = Faker()


def _get_random_period():
    lower = Faker().future_datetime() + BDay(0)
    upper = lower + BDay(random.randint(1, 7))
    return TimestamptzRange(
        lower=make_aware(lower),
        upper=make_aware(upper),
    )


class CalendarItemFactory(factory.django.DjangoModelFactory):
    color = factory.Faker("color")
    icon = factory.LazyAttribute(lambda x: WBIcon[random.choice(WBIcon.names)].icon)
    visibility = CalendarItem.Visibility.PUBLIC
    period = factory.LazyAttribute(lambda x: _get_random_period())
    title = factory.Faker("sentence")
    conference_room = factory.SubFactory(ConferenceRoomFactory)
    all_day = False
    is_cancelled = False
    is_deletable = True

    @factory.post_generation
    def entities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for entitie in extracted:
                self.entities.add(entitie)

    class Meta:
        model = CalendarItem
        django_get_or_create = ("title",)
        skip_postgeneration_save = True
