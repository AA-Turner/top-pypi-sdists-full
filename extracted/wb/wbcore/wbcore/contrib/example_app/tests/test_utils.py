import pytest

from wbcore.contrib.example_app.factories import (
    EventFactory,
    EventTypeFactory,
    LeagueFactory,
)
from wbcore.contrib.example_app.utils import get_event_types_for_league


@pytest.mark.django_db
class TestUtils:
    def test_get_event_types_for_league(self):
        league = LeagueFactory.create()
        event_type1 = EventTypeFactory.create(sport=league.sport)
        event_type2 = EventTypeFactory.create(sport=league.sport)
        event_type3 = EventTypeFactory.create()
        event_type4 = EventTypeFactory.create(sport=league.sport)
        EventFactory.create(event_type=event_type1)
        EventFactory.create(event_type=event_type2)
        EventFactory.create(event_type=event_type3)
        league_event_types = get_event_types_for_league(league.pk)
        for event_type in league_event_types:
            assert event_type["name"] in [event_type1.name, event_type2.name]
            assert event_type["name"] not in [event_type3.name, event_type4.name]
            assert " " not in event_type["slugified_name"]
