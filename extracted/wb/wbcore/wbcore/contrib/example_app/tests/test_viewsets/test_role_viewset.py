import pytest
from django.test import Client, TestCase
from django.urls import reverse
from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.example_app.factories import RoleFactory
from wbcore.contrib.example_app.models import Role
from wbcore.contrib.example_app.serializers import RoleModelSerializer
from wbcore.contrib.example_app.tests.test_viewsets.test_utils_viewsets import (
    get_create_view,
    get_delete_view,
    get_detail_view,
    get_partial_view,
    get_update_view,
)
from wbcore.contrib.example_app.viewsets import RoleModelViewSet


@pytest.mark.django_db
class TestRoleModelViewSet(TestCase):
    def setUp(self):
        self.user = SuperUserFactory.create()
        self.client = Client()
        self.client.force_login(user=self.user)
        self.list_url = reverse("example_app:role-list")
        self.detail_url_str = "example_app:role-detail"

    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        role = RoleFactory.create()
        response = get_create_view(self.client, role, self.user, self.list_url, RoleModelViewSet)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Role.objects.filter(title=role.title).exists())

    def test_detail_view(self):
        instance = RoleFactory.create()
        response = get_detail_view(self.client, instance.pk, self.detail_url_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["title"], instance.title)

    def test_update_view(self):
        instance = RoleFactory.create()
        instance.title = "Updated Instance"
        response = get_update_view(self.client, instance, RoleModelSerializer, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["title"], instance.title)

    def test_partial_update_view(self):
        instance = RoleFactory.create()
        response = get_partial_view(self.client, instance.id, {"title": "Patched Title"}, self.detail_url_str)
        instance.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["instance"]["title"], instance.title)

    def test_delete_view(self):
        instance = RoleFactory.create()
        response = get_delete_view(self.client, self.detail_url_str, instance.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Role.objects.filter(pk=instance.pk).exists())

    def test_ordering_fields(self):
        first_role, second_role, third_role = "Role A", "Role B", "Role C"
        RoleFactory.create(title=second_role)
        RoleFactory.create(title=first_role)
        RoleFactory.create(title=third_role)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], Role.objects.count())
        self.assertEqual(response.data["results"][0]["title"], first_role)
        self.assertEqual(response.data["results"][1]["title"], second_role)
        self.assertEqual(response.data["results"][2]["title"], third_role)
