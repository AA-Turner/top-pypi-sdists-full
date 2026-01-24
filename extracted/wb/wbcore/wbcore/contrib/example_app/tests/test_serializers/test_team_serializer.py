from datetime import date, datetime, timedelta

import pytest
from django.forms.models import model_to_dict
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from wbcore.contrib.directory.factories import PersonFactory
from wbcore.contrib.example_app.factories import (
    PlayerFactory,
    SportPersonFactory,
    StadiumFactory,
    TeamFactory,
)
from wbcore.contrib.example_app.serializers import (
    PlayerModelSerializer,
    SportPersonModelSerializer,
    TeamErrorMessages,
    TeamModelSerializer,
)


@pytest.mark.django_db
class TestSportPersonModelSerializer(APITestCase):
    def test_person_serializer(self):
        person_data: dict = model_to_dict(SportPersonFactory.build(profile=PersonFactory.create()))
        sport_person_serializer = SportPersonModelSerializer(data=person_data)
        self.assertTrue(sport_person_serializer.is_valid())

    def test_player_serializer(self):
        player_data: dict = model_to_dict(PlayerFactory.build(current_team=TeamFactory.create()))
        player_serializer = PlayerModelSerializer(data=player_data)
        self.assertTrue(player_serializer.is_valid())


@pytest.mark.django_db
class TestTeamModelSerializer(APITestCase):
    def test_team_serializer(self):
        coach = SportPersonFactory.create()
        stadium = StadiumFactory.create()

        team_data: dict = model_to_dict(TeamFactory.build(coach=coach, home_stadium=stadium))
        team_serializer = TeamModelSerializer(data=team_data)
        self.assertTrue(team_serializer.is_valid())

    def test_team_exists(self):
        coach = SportPersonFactory.create()
        stadium = StadiumFactory.create()
        team = TeamFactory.create(coach=coach, home_stadium=stadium)
        new_team_data: dict = model_to_dict(TeamFactory.build(home_stadium=stadium, name=team.name))
        with self.assertRaisesMessage(ValidationError, TeamErrorMessages.team_exists.value):
            team_serializer = TeamModelSerializer(data=new_team_data)
            self.assertFalse(team_serializer.is_valid(raise_exception=True))

    def test_team_wrong_date(self):
        stadium = StadiumFactory.create()
        future_date: date = (datetime.now() + timedelta(days=1)).date()
        team_data: dict = model_to_dict(TeamFactory.build(founded_date=future_date, home_stadium=stadium))

        with self.assertRaisesMessage(ValidationError, TeamErrorMessages.wrong_founding_date.value):
            team_serializer = TeamModelSerializer(data=team_data)
            self.assertFalse(team_serializer.is_valid(raise_exception=True))

    def test_team_name_placeholder(self):
        coach = SportPersonFactory.create()
        stadium = StadiumFactory.create()
        team_data: dict = model_to_dict(TeamFactory.build(home_stadium=stadium, coach=coach))
        team_serializer = TeamModelSerializer(data=team_data)
        self.assertTrue(team_serializer.is_valid())
        self.assertTrue("name" in team_serializer.fields)
        self.assertTrue(team_serializer.fields["name"].placeholder == "Enter team name here")
