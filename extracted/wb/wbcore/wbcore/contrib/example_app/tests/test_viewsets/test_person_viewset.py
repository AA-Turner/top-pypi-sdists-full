import pytest
from django.test import Client, TestCase
from django.urls import reverse
from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.example_app.factories import (
    PlayerFactory,
    SportPersonFactory,
    TeamFactory,
)
from wbcore.contrib.example_app.models import Player, SportPerson
from wbcore.contrib.example_app.serializers import (
    PlayerModelSerializer,
    SportPersonModelSerializer,
)
from wbcore.contrib.example_app.tests.test_viewsets.test_utils_viewsets import (
    find_instances_in_response,
    get_create_view,
    get_delete_view,
    get_detail_view,
    get_partial_view,
    get_update_view,
)
from wbcore.contrib.example_app.viewsets import (
    PlayerModelViewSet,
    SportPersonModelViewSet,
)


@pytest.mark.django_db
class TestSportPersonModelViewSet(TestCase):
    def setUp(self):
        self.user = SuperUserFactory.create()
        self.client = Client()
        self.client.force_login(user=self.user)
        self.list_url = reverse("example_app:person-list")
        self.detail_url_str = "example_app:person-detail"

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        person = SportPersonFactory.create()
        response = get_create_view(self.client, person, self.user, self.list_url, SportPersonModelViewSet)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(SportPerson.objects.filter(last_name=person.last_name).exists())

    def test_detail_view(self):
        instance = SportPersonFactory.create()
        response = get_detail_view(self.client, instance.pk, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["last_name"], instance.last_name)

    def test_update_view(self):
        instance = SportPersonFactory.create()
        instance.last_name = "Updated Instance"
        instance.profile_image = None
        response = get_update_view(self.client, instance, SportPersonModelSerializer, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["last_name"], instance.last_name)

    def test_partial_update_view(self):
        instance = SportPersonFactory.create()
        response = get_partial_view(self.client, instance.id, {"last_name": "Updated Instance"}, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["last_name"], instance.last_name)

    def test_delete_view(self):
        instance = SportPersonFactory.create()
        response = get_delete_view(self.client, self.detail_url_str, instance.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(SportPerson.objects.filter(pk=instance.pk).exists())

    def test_ordering_fields(self):
        person_a = SportPersonFactory.create(first_name="Hans", last_name="Brecht")
        person_b = SportPersonFactory.create(first_name="Hans", last_name="Ahrens")
        person_c = SportPersonFactory.create(first_name="Ralf", last_name="Christ")

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], SportPerson.objects.count())
        self.assertEqual(response.data["results"][0]["id"], person_b.id)
        self.assertEqual(response.data["results"][1]["id"], person_a.id)
        self.assertEqual(response.data["results"][2]["id"], person_c.id)


@pytest.mark.django_db
class TestPlayerModelViewSet(TestCase):
    def setUp(self):
        self.user = SuperUserFactory.create()
        self.client = Client()
        self.client.force_login(user=self.user)
        self.detail_url_str = "example_app:player-detail"
        self.list_url = reverse("example_app:player-list")

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        player = PlayerFactory.create()
        response = get_create_view(self.client, player, self.user, self.list_url, PlayerModelViewSet)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Player.objects.filter(last_name=player.last_name).exists())

    def test_detail_view(self):
        instance = PlayerFactory.create()
        response = get_detail_view(self.client, instance.pk, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["last_name"], instance.last_name)

    def test_update_view(self):
        instance = PlayerFactory.create()
        instance.last_name = "Updated Instance"
        response = get_update_view(self.client, instance, PlayerModelSerializer, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["last_name"], instance.last_name)

    def test_partial_update_view(self):
        instance = PlayerFactory.create()
        response = get_partial_view(self.client, instance.id, {"last_name": "Updated Instance"}, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["last_name"], instance.last_name)

    def test_delete_view(self):
        instance = PlayerFactory.create()
        response = get_delete_view(self.client, self.detail_url_str, instance.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Player.objects.filter(pk=instance.pk).exists())

    def test_ordering_fields(self):
        team_a, team_b = TeamFactory.create(name="Team A"), TeamFactory(name="Team B")
        person_a = PlayerFactory(first_name="Hans", last_name="Ahrens", current_team=team_b)
        person_b = PlayerFactory(first_name="Hans", last_name="Ahrens", current_team=team_a)
        person_c = PlayerFactory(first_name="Ralf", last_name="Brecht")

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], Player.objects.count())
        self.assertEqual(response.data["results"][0]["id"], person_b.id)
        self.assertEqual(response.data["results"][1]["id"], person_a.id)
        self.assertEqual(response.data["results"][2]["id"], person_c.id)

    def test_player_team(self):
        player_a = PlayerFactory()
        player_b = PlayerFactory(current_team=player_a.current_team)
        player_c = PlayerFactory()
        expected_number_of_player = Player.objects.filter(current_team=player_a.current_team).count()
        player_team_url = reverse("example_app:player-team-list", args=[player_a.current_team.id])
        response = self.client.get(player_team_url)
        player_a_found, player_b_found, player_c_found = find_instances_in_response(
            [player_a, player_b, player_c], response
        )
        self.assertEqual(
            response.data["count"],
            expected_number_of_player,
            f"The answer should contain {expected_number_of_player} players",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(player_a_found, "Player A was not found in Response")
        self.assertTrue(player_b_found, "Player B was not found in Response")
        self.assertFalse(player_c_found, "Player C was found in Response, but should not be found")
