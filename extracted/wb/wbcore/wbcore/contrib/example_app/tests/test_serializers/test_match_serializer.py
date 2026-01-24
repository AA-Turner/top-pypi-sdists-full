import pytest
from django.forms.models import model_to_dict
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from wbcore.contrib.example_app.factories import (
    EventFactory,
    EventTypeFactory,
    LeagueFactory,
    MatchFactory,
    SportFactory,
    SportPersonFactory,
    StadiumFactory,
    TeamFactory,
)
from wbcore.contrib.example_app.serializers import (
    EventErrorMessages,
    EventModelSerializer,
    EventTypeModelSerializer,
    LeaguePlayerStatisticsModelSerializer,
    LeagueTeamStatisticsModelSerializer,
    MatchErrorMessages,
    MatchModelSerializer,
)


@pytest.mark.django_db
class TestMatchModelSerializer(APITestCase):
    def test_match_serializer(self):
        match_data: dict = model_to_dict(
            MatchFactory.build(
                away=TeamFactory.create(),
                home=TeamFactory.create(),
                sport=SportFactory.create(),
                stadium=StadiumFactory.create(),
            )
        )
        match_serializer = MatchModelSerializer(data=match_data)
        self.assertTrue(match_serializer.is_valid())

    def test_match_same_teams(self):
        team = TeamFactory.create()
        match_data: dict = model_to_dict(
            MatchFactory.build(away=team, home=team, sport=SportFactory.create(), stadium=StadiumFactory.create())
        )
        with self.assertRaisesMessage(ValidationError, MatchErrorMessages.same_teams.value):
            league_serializer = MatchModelSerializer(data=match_data)
            self.assertFalse(league_serializer.is_valid(raise_exception=True))

    def test_match_same_date(self):
        match = MatchFactory()
        match_data: dict = model_to_dict(match)
        with pytest.raises(ValidationError):
            MatchModelSerializer(data=match_data).is_valid(raise_exception=True)

    def test_match_wrong_sport(self):
        match_data: dict = model_to_dict(
            MatchFactory.build(
                away=TeamFactory(),
                home=TeamFactory(),
                stadium=StadiumFactory(),
                sport=SportFactory(),
                league=LeagueFactory(),
            )
        )
        with self.assertRaisesMessage(ValidationError, MatchErrorMessages.wrong_sport.value):
            league_serializer = MatchModelSerializer(data=match_data)
            self.assertFalse(league_serializer.is_valid(raise_exception=True))


@pytest.mark.django_db
class TestEventTypeModelSerializer(APITestCase):
    def test_event_type_serializer(self):
        event_type_data: dict = model_to_dict(EventTypeFactory.build(sport=SportFactory()))
        event_type_serializer = EventTypeModelSerializer(data=event_type_data)
        self.assertTrue(event_type_serializer.is_valid())

    def test_event_type_same_name(self):
        event_type = EventTypeFactory()
        event_type_data: dict = model_to_dict(EventTypeFactory.build(name=event_type.name, sport=event_type.sport))
        with pytest.raises(ValidationError):
            EventTypeModelSerializer(data=event_type_data).is_valid(raise_exception=True)


@pytest.mark.django_db
class TestEventModelSerializer(APITestCase):
    def test_event_serializer(self):
        match = MatchFactory()
        event_type = EventTypeFactory(sport=match.sport)
        event_data: dict = model_to_dict(
            EventFactory.build(person=SportPersonFactory(), event_type=event_type, match=match)
        )
        event_serializer = EventModelSerializer(data=event_data)
        self.assertTrue(event_serializer.is_valid())

    def test_event_wrong_duration(self):
        sport = SportFactory(match_duration=60)
        event_type = EventTypeFactory(sport=sport)
        match = MatchFactory(sport=sport)
        event: dict = model_to_dict(
            EventFactory.build(person=SportPersonFactory(), minute=61, event_type=event_type, match=match)
        )
        with self.assertRaisesMessage(ValidationError, EventErrorMessages.wrong_duration.value):
            event_serializer = EventModelSerializer(data=event)
            self.assertFalse(event_serializer.is_valid(raise_exception=True))

    def test_event_duplication(self):
        event = EventFactory.create()
        event_data = model_to_dict(event)

        with pytest.raises(ValidationError):
            EventModelSerializer(data=event_data).is_valid(raise_exception=True)

    def test_event_wrong_type(self):
        event_type = EventTypeFactory()
        match = MatchFactory()
        event_data: dict = model_to_dict(
            EventFactory.build(person=SportPersonFactory(), event_type=event_type, match=match)
        )
        with self.assertRaisesMessage(
            ValidationError, EventErrorMessages.wrong_event_type.value.format(match.sport.name)
        ):
            event_serializer = EventModelSerializer(data=event_data)
            self.assertFalse(event_serializer.is_valid(raise_exception=True))


@pytest.mark.django_db
class TestLeaguePlayerStatisticsModelSerializer(APITestCase):
    def test_league_player_statistics_serializer(self):
        statistic_data = {"person_id": 1, "person_name": "Foo", "count": 1, "id": "id"}
        statistic_serializer = LeaguePlayerStatisticsModelSerializer(data=statistic_data)
        self.assertTrue(statistic_serializer.is_valid())


@pytest.mark.django_db
class TestLeagueTeamStatisticsModelSerializer(APITestCase):
    def test_league_player_statistics_serializer(self):
        statistic_data = {"team_id": 1, "team_name": "Foo", "count": 1, "id": "id"}
        statistic_serializer = LeagueTeamStatisticsModelSerializer(data=statistic_data)
        self.assertTrue(statistic_serializer.is_valid())
