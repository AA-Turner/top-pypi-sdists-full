import pytest
from django.test import Client, TestCase
from django.urls import reverse
from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.example_app.factories import TeamResultsFactory
from wbcore.contrib.example_app.serializers import TeamResultsModelSerializer
from wbcore.contrib.example_app.tests.test_viewsets.test_utils_viewsets import (
    get_create_view,
    get_delete_view,
    get_detail_view,
    get_partial_view,
    get_update_view,
)
from wbcore.contrib.example_app.viewsets import TeamResultsModelViewSet


@pytest.mark.django_db
class TestTeamResultsModelViewSet(TestCase):
    def setUp(self):
        self.user = SuperUserFactory.create()
        self.client = Client()
        self.client.force_login(user=self.user)
        self.list_url = reverse("example_app:teamresults-list")
        self.detail_url_str = "example_app:teamresults-detail"

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        team_result = TeamResultsFactory.create()
        response = get_create_view(self.client, team_result, self.user, self.list_url, TeamResultsModelViewSet)
        # It is not possible to create an team results, since the get_endpoint_url returns None.
        self.assertEqual(response.status_code, 405)

    def test_detail_view(self):
        instance = TeamResultsFactory.create()
        response = get_detail_view(self.client, instance.pk, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["id"], instance.id)

    def test_update_view(self):
        instance = TeamResultsFactory.create()
        instance.points = 5
        response = get_update_view(self.client, instance, TeamResultsModelSerializer, self.detail_url_str)
        # It is not possible to update an team results, since the get_endpoint_url returns None.
        self.assertEqual(response.status_code, 405)

    def test_partial_update_view(self):
        instance = TeamResultsFactory.create()
        response = get_partial_view(self.client, instance.id, {"points": 5}, self.detail_url_str)
        self.assertEqual(response.status_code, 405)

    def test_delete_view(self):
        instance = TeamResultsFactory.create()
        response = get_delete_view(self.client, self.detail_url_str, instance.pk)
        # It is not possible to delete an team results, since the get_endpoint_url returns None.
        self.assertEqual(response.status_code, 405)
