import pytest
from django.db import IntegrityError
from wbcore.contrib.example_app.factories import (
    EventFactory,
    EventTypeFactory,
    PlayerFactory,
)


@pytest.mark.django_db
class TestEvent:
    def test_str(self):
        event = EventFactory.create(
            minute=69,
            person__first_name="Test",
            person__last_name="Person",
            event_type__name="Test Event Type",
            match__sport__match_duration=90,
        )
        assert event.__str__() == "Test Event Type (69.) - Test Person"

    @pytest.mark.parametrize(
        "home, away, points, home_score, away_score", [(2, 1, 5, 7, 1), (0, 3, 2, 2, 3), (1, 1, 0, 1, 1)]
    )
    def test_save_home_scored(self, home, away, points, home_score, away_score):
        person = PlayerFactory.create()
        event = EventFactory.create(
            person=person,
            match__home=person.current_team,
            match__score_home=home,
            match__score_away=away,
            event_type__points=points,
        )
        assert event.match.score_home == home_score
        assert event.match.score_away == away_score

    @pytest.mark.parametrize(
        "home, away, points, home_score, away_score", [(41, 27, 4, 41, 31), (19, 0, 2, 19, 2), (22, 23, 0, 22, 23)]
    )
    def test_save_away_scored(self, home, away, points, home_score, away_score):
        person = PlayerFactory.create()
        event = EventFactory.create(
            person=person,
            match__away=person.current_team,
            match__score_home=home,
            match__score_away=away,
            event_type__points=points,
        )
        assert event.match.score_home == home_score
        assert event.match.score_away == away_score

    def test_save_no_team(self):
        person = PlayerFactory.create()
        event = EventFactory.create(
            person=person,
            match__score_home=2,
            match__score_away=1,
            event_type__points=4,
        )
        assert event.match.score_home == 2
        assert event.match.score_away == 1

    def test_save_no_player(self):
        event = EventFactory.create(
            match__score_home=2,
            match__score_away=1,
            event_type__points=4,
        )
        assert event.match.score_home == 2
        assert event.match.score_away == 1

    def test_unique_constraint(self):
        event = EventFactory.create()
        with pytest.raises(IntegrityError):
            EventFactory.create(
                person=event.person, minute=event.minute, event_type=event.event_type, match=event.match
            )


@pytest.mark.django_db
class TestEventType:
    def test_str(self):
        event_type = EventTypeFactory.create(name="Test Event Type")
        assert event_type.__str__() == "Test Event Type"

    def test_unique_constraint(self):
        event_type = EventTypeFactory.create()
        with pytest.raises(IntegrityError):
            EventTypeFactory.create(name=event_type.name, sport=event_type.sport)
