import pytest
from django.test import Client, TestCase
from django.urls import reverse
from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.example_app.factories import StadiumFactory
from wbcore.contrib.example_app.models import Stadium
from wbcore.contrib.example_app.serializers import StadiumModelSerializer
from wbcore.contrib.example_app.tests.test_viewsets.test_utils_viewsets import (
    get_create_view,
    get_delete_view,
    get_detail_view,
    get_partial_view,
    get_update_view,
)
from wbcore.contrib.example_app.viewsets import StadiumModelViewSet


@pytest.mark.django_db
class TestStadiumModelViewSet(TestCase):
    def setUp(self):
        self.user = SuperUserFactory.create()
        self.client = Client()
        self.client.force_login(user=self.user)
        self.list_url = reverse("example_app:stadium-list")
        self.detail_url_str = "example_app:stadium-detail"

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        stadium = StadiumFactory.create()
        response = get_create_view(self.client, stadium, self.user, self.list_url, StadiumModelViewSet)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Stadium.objects.filter(name=stadium.name).exists())

    def test_detail_view(self):
        instance = StadiumFactory.create()
        response = get_detail_view(self.client, instance.pk, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], instance.name)

    def test_update_view(self):
        instance = StadiumFactory.create()
        instance.name = "Updated Instance"
        response = get_update_view(self.client, instance, StadiumModelSerializer, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], instance.name)

    def test_partial_update_view(self):
        instance = StadiumFactory.create()
        response = get_partial_view(self.client, instance.id, {"name": "Updated Instance"}, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["name"], instance.name)

    def test_delete_view(self):
        instance = StadiumFactory.create()
        response = get_delete_view(self.client, self.detail_url_str, instance.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Stadium.objects.filter(pk=instance.pk).exists())

    def test_ordering_fields(self):
        first_name, second_name, third_name = "Stadium A", "Stadium B", "Stadium C"
        StadiumFactory.create(name=second_name)
        StadiumFactory.create(name=first_name)
        StadiumFactory.create(name=third_name)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], Stadium.objects.count())
        self.assertEqual(response.data["results"][0]["name"], first_name)
        self.assertEqual(response.data["results"][1]["name"], second_name)
        self.assertEqual(response.data["results"][2]["name"], third_name)
