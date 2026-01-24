from datetime import date, datetime, timedelta

import pytest
from django.forms.models import model_to_dict
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from wbcore.contrib.example_app.factories import LeagueFactory, SportFactory
from wbcore.contrib.example_app.serializers import LeagueModelSerializer


@pytest.mark.django_db
class TestLeagueModelSerializer(APITestCase):
    def test_league_serializer(self):
        sport = SportFactory.create()
        league_data: dict = model_to_dict(LeagueFactory.build(sport=sport))
        league_serializer = LeagueModelSerializer(data=league_data)

        self.assertTrue(league_serializer.is_valid())

    def test_league_exists(self):
        sport = SportFactory.create()
        league = LeagueFactory.create(sport=sport)
        new_league_data: dict = model_to_dict(LeagueFactory.build(sport=sport, name=league.name))

        with pytest.raises(ValidationError):
            LeagueModelSerializer(data=new_league_data).is_valid(raise_exception=True)

    def test_league_wrong_date(self):
        sport = SportFactory.create()
        future_date: date = (datetime.now() + timedelta(days=1)).date()
        league_data: dict = model_to_dict(LeagueFactory.build(sport=sport, established_date=future_date))

        with pytest.raises(ValidationError):
            LeagueModelSerializer(data=league_data).is_valid(raise_exception=True)
