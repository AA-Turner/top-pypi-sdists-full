import pytest
from django.test import Client, TestCase
from django.urls import reverse
from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.example_app.factories import LeagueFactory
from wbcore.contrib.example_app.models import League
from wbcore.contrib.example_app.serializers import LeagueModelSerializer
from wbcore.contrib.example_app.tests.test_viewsets.test_utils_viewsets import (
    find_instances_in_response,
    get_create_view,
    get_delete_view,
    get_detail_view,
    get_partial_view,
    get_update_view,
)
from wbcore.contrib.example_app.viewsets import LeagueModelViewSet


@pytest.mark.django_db
class TestLeagueModelViewSet(TestCase):
    def setUp(self):
        self.user = SuperUserFactory.create()
        self.client = Client()
        self.client.force_login(user=self.user)
        self.list_url = reverse("example_app:league-list")
        self.detail_url_str = "example_app:league-detail"

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        league = LeagueFactory.create()
        response = get_create_view(self.client, league, self.user, self.list_url, LeagueModelViewSet)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(League.objects.filter(name=league.name).exists())

    def test_detail_view(self):
        instance = LeagueFactory.create()
        response = get_detail_view(self.client, instance.pk, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], instance.name)

    def test_update_view(self):
        instance = LeagueFactory.create()
        instance.name = "Updated Instance"
        response = get_update_view(self.client, instance, LeagueModelSerializer, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], instance.name)

    def test_partial_update_view(self):
        instance = LeagueFactory.create()
        response = get_partial_view(self.client, instance.id, {"name": "Updated Instance"}, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], instance.name)

    def test_delete_view(self):
        instance = LeagueFactory.create()
        response = get_delete_view(self.client, self.detail_url_str, instance.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(League.objects.filter(pk=instance.pk).exists())

    def test_league_sport(self):
        league_a = LeagueFactory.create()
        league_b = LeagueFactory.create(sport=league_a.sport)
        league_c = LeagueFactory.create()
        expected_number_of_league = League.objects.filter(sport=league_a.sport).count()
        league_sport_url = reverse("example_app:league-sport-list", args=[league_a.sport.id])
        response = self.client.get(league_sport_url)
        league_a_found, league_b_found, league_c_found = find_instances_in_response(
            [league_a, league_b, league_c], response
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["count"],
            expected_number_of_league,
            f"The answer should contain {expected_number_of_league} leagues",
        )
        self.assertTrue(league_a_found, "Player A was not found in Response.")
        self.assertTrue(league_b_found, "Player B was not found in Response.")
        self.assertFalse(league_c_found, "Player C was found in Response, but should not be found.")
