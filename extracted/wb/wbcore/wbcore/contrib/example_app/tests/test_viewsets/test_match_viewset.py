import pytest
from django.test import Client, TestCase
from django.urls import reverse
from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.example_app.factories import MatchFactory, TeamFactory
from wbcore.contrib.example_app.models import Match
from wbcore.contrib.example_app.serializers import MatchModelSerializer
from wbcore.contrib.example_app.tests.test_viewsets.test_utils_viewsets import (
    get_create_view,
    get_delete_view,
    get_detail_view,
    get_partial_view,
    get_update_view,
)
from wbcore.contrib.example_app.viewsets import MatchModelViewSet


@pytest.mark.django_db
class TestMatchModelViewSet(TestCase):
    def setUp(self):
        self.user = SuperUserFactory.create()
        self.client = Client()
        self.client.force_login(user=self.user)
        self.list_url = reverse("example_app:match-list")
        self.detail_url_str = "example_app:match-detail"

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        match = MatchFactory.create()
        response = get_create_view(self.client, match, self.user, self.list_url, MatchModelViewSet)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Match.objects.filter(home=match.home, away=match.away).exists())

    def test_detail_view(self):
        instance = MatchFactory.create()
        response = get_detail_view(self.client, instance.pk, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["id"], instance.id)

    def test_update_view(self):
        instance = MatchFactory.create(status=Match.MatchStatus.SCHEDULED)
        new_home_team = TeamFactory.create()
        instance.home = new_home_team
        response = get_update_view(self.client, instance, MatchModelSerializer, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["home"], instance.home.id)

    def test_partial_update_view(self):
        instance = MatchFactory.create()
        new_home_team = TeamFactory.create()
        response = get_partial_view(self.client, instance.id, {"home": new_home_team.id}, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["home"], instance.home.id)

    def test_delete_view(self):
        instance = MatchFactory.create()
        self.assertTrue(Match.objects.filter(pk=instance.pk).exists())
        response = get_delete_view(self.client, self.detail_url_str, instance.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Match.objects.filter(pk=instance.pk).exists())
