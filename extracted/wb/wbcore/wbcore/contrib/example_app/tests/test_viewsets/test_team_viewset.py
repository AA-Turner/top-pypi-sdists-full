import pytest
from django.test import Client, TestCase
from django.urls import reverse
from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.example_app.factories import TeamFactory
from wbcore.contrib.example_app.models import Team
from wbcore.contrib.example_app.serializers import TeamModelSerializer
from wbcore.contrib.example_app.tests.test_viewsets.test_utils_viewsets import (  # get_update_view,
    find_instances_in_response,
    get_create_view,
    get_delete_view,
    get_detail_view,
    get_partial_view,
    get_update_view,
)
from wbcore.contrib.example_app.viewsets import TeamModelViewSet


@pytest.mark.django_db
class TestTeamModelViewSet(TestCase):
    def setUp(self):
        self.user = SuperUserFactory.create()
        self.client = Client()
        self.client.force_login(user=self.user)
        self.list_url = reverse("example_app:team-list")
        self.detail_url_str = "example_app:team-detail"

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        team = TeamFactory.create()
        response = get_create_view(self.client, team, self.user, self.list_url, TeamModelViewSet)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Team.objects.filter(name=team.name).exists())

    def test_detail_view(self):
        team = TeamFactory.create()
        response = get_detail_view(self.client, team.pk, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], team.name)

    def test_update_view(self):
        instance = TeamFactory.create()
        instance.name = "Updated Instance"
        response = get_update_view(self.client, instance, TeamModelSerializer, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], instance.name)

    def test_partial_update_view(self):
        instance = TeamFactory.create()
        response = get_partial_view(self.client, instance.id, {"name": "Updated Instance"}, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], instance.name)

    def test_delete_view(self):
        team = TeamFactory.create()
        response = get_delete_view(self.client, self.detail_url_str, team.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Team.objects.filter(pk=team.pk).exists())

    def test_ordering_fields(self):
        team_a = TeamFactory.create(name="BBB", order=1)
        team_b = TeamFactory.create(name="AAA", order=0)
        team_c = TeamFactory.create(name="CCC", order=2)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], Team.objects.count())
        self.assertEqual(response.data["results"][0]["id"], team_b.id)
        self.assertEqual(response.data["results"][1]["id"], team_a.id)
        self.assertEqual(response.data["results"][2]["id"], team_c.id)

    def test_team_stadium(self):
        team_a = TeamFactory.create()
        team_b = TeamFactory.create(home_stadium=team_a.home_stadium)
        team_c = TeamFactory.create()
        expected_number_of_teams = Team.objects.filter(home_stadium=team_a.home_stadium).count()
        team_stadium_url = reverse("example_app:team-stadium-list", args=[team_a.home_stadium.id])
        response = self.client.get(team_stadium_url)
        team_a_found, team_b_found, team_c_found = find_instances_in_response([team_a, team_b, team_c], response)
        self.assertEqual(
            response.data["count"],
            expected_number_of_teams,
            f"The answer should contain {expected_number_of_teams} teams",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(team_a_found, "Team A was not found in Response")
        self.assertTrue(team_b_found, "Team B was not found in Response")
        self.assertFalse(team_c_found, "Team C was found in Response, but should not be found")
