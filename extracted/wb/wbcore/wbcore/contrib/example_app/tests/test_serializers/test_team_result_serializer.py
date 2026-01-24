import pytest
from django.forms.models import model_to_dict
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from wbcore.contrib.example_app.factories import (
    LeagueFactory,
    TeamFactory,
    TeamResultsFactory,
)
from wbcore.contrib.example_app.serializers import TeamResultsModelSerializer


@pytest.mark.django_db
class TestTeamResultSerializer(APITestCase):
    def test_result_serializer(self):
        team = TeamFactory.create()
        league = LeagueFactory.create()
        result: dict = model_to_dict(TeamResultsFactory.build(team=team, league=league))
        result["games_played"] = 3
        result_serializer = TeamResultsModelSerializer(data=result)

        self.assertTrue(result_serializer.is_valid())

    def test_same_result(self):
        result = TeamResultsFactory.create()
        new_result: dict = model_to_dict(TeamResultsFactory.build(team=result.team, league=result.league))
        new_result["games_played"] = 3

        with pytest.raises(ValidationError):
            TeamResultsModelSerializer(data=new_result).is_valid(raise_exception=True)
