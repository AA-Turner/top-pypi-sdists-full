# import pytest
# from django.test import Client, TestCase
# from django.urls import reverse
# from wbcore.contrib.authentication.factories import UserFactory
# from wbcore.contrib.example_app.factories import EventFactory, EventTypeFactory
# from wbcore.contrib.example_app.models import Event, EventType
# from wbcore.contrib.example_app.serializers import (
#     EventModelSerializer,
#     EventTypeModelSerializer,
# )
# from wbcore.contrib.example_app.tests.test_viewsets.test_utils_viewsets import (
#     find_instances_in_response,
#     get_create_view,
#     get_delete_view,
#     get_detail_view,
#     get_partial_view,
#     get_update_view,
# )
# from wbcore.contrib.example_app.viewsets import EventModelViewSet, EventTypeModelViewSet
#
#
# @pytest.mark.django_db
# class TestEventModelViewSet(TestCase):
#     def setUp(self) -> None:
#         self.user = UserFactory.create(is_active=True, is_superuser=True)
#         self.client = Client()
#         self.client.force_login(user=self.user)
#         self.list_url = reverse("example_app:event-list")
#         self.detail_url_str = "example_app:event-detail"
#
#     def test_list_view(self):
#         response = self.client.get(self.list_url)
#         print(response.content)
#         self.assertEqual(response.status_code, 200)
#
#     def test_create_view(self):
#         event = EventFactory.create()
#         response = get_create_view(self.client, event, self.user, self.list_url, EventModelViewSet)
#         print(response.content)
#         self.assertEqual(response.status_code, 201)
#         self.assertTrue(
#             Event.objects.filter(event_type=event.event_type, match=event.match, minute=event.minute).exists()
#         )
#
#     def test_detail_view(self):
#         instance = EventFactory.create()
#         response = get_detail_view(self.client, instance.pk, self.detail_url_str)
#         print(response.content)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["instance"]["id"], instance.id)
#
#     def test_update_view(self):
#         instance = EventFactory.create()
#         max_match_duration = instance.match.sport.match_duration
#         instance.minute = max_match_duration - instance.minute
#         response = get_update_view(self.client, instance, EventModelSerializer, self.detail_url_str)
#         print(response.content)
#         instance.refresh_from_db()
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["instance"]["minute"], instance.minute)
#
#     def test_partial_update_view(self):
#         instance = EventFactory.create()
#         max_match_duration = instance.match.sport.match_duration
#         response = get_partial_view(
#             self.client, instance.id, {"minute": max_match_duration - instance.minute}, self.detail_url_str
#         )
#         print(response.content)
#         instance.refresh_from_db()
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["instance"]["minute"], instance.minute)
#
#     def test_delete_view(self):
#         instance = EventFactory.create()
#         response = get_delete_view(self.client, self.detail_url_str, instance.pk)
#         # It is not possible to delete an event, since the get_endpoint_url returns None. I suppose that is expected behavior.
#         self.assertEqual(response.status_code, 405)
#         self.assertTrue(Event.objects.filter(pk=instance.pk).exists())
#
#     def test_ordering_fields(self):
#         event1 = EventFactory.create(minute=30)
#         EventFactory.create(person=event1.person, minute=20, event_type=event1.event_type, match=event1.match)
#         EventFactory.create(person=event1.person, minute=40, event_type=event1.event_type, match=event1.match)
#
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["count"], Event.objects.count())
#         self.assertEqual(response.data["results"][0]["minute"], 20)
#         self.assertEqual(response.data["results"][1]["minute"], 30)
#         self.assertEqual(response.data["results"][2]["minute"], 40)
#
#
# @pytest.mark.django_db
# class TestEventTypeModelViewSet(TestCase):
#     def setUp(self) -> None:
#         self.user = UserFactory.create(is_active=True, is_superuser=True)
#         self.client = Client()
#         self.client.force_login(user=self.user)
#         self.list_url = reverse("example_app:eventtype-list")
#         self.detail_url_str = "example_app:eventtype-detail"
#
#     def test_list_view(self):
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_create_view(self):
#         event_type = EventTypeFactory.create()
#         response = get_create_view(self.client, event_type, self.user, self.list_url, EventTypeModelViewSet)
#         self.assertEqual(response.status_code, 201)
#         self.assertTrue(EventType.objects.filter(name=event_type.name).exists())
#
#     def test_detail_view(self):
#         instance = EventTypeFactory.create()
#         response = get_detail_view(self.client, instance.pk, self.detail_url_str)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["instance"]["id"], instance.id)
#
#     def test_update_view(self):
#         instance = EventTypeFactory.create()
#         instance.name = "Updated Instance"
#         response = get_update_view(self.client, instance, EventTypeModelSerializer, self.detail_url_str)
#         instance.refresh_from_db()
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["instance"]["name"], instance.name)
#
#     def test_partial_update_view(self):
#         instance = EventTypeFactory.create()
#         response = get_partial_view(self.client, instance.id, {"name": "Updated Instance"}, self.detail_url_str)
#         instance.refresh_from_db()
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["instance"]["name"], instance.name)
#
#     def test_delete_view(self):
#         instance = EventTypeFactory.create()
#         response = get_delete_view(self.client, self.detail_url_str, instance.pk)
#         self.assertEqual(response.status_code, 204)
#         self.assertFalse(Event.objects.filter(pk=instance.pk).exists())
#
#     def test_ordering_fields(self):
#         event_a = EventTypeFactory.create(name="BBB")
#         event_b = EventTypeFactory.create(name="AAA", sport=event_a.sport)
#         event_c = EventTypeFactory.create(name="CCC", sport=event_a.sport)
#
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["count"], EventType.objects.count())
#         self.assertEqual(response.data["results"][0]["id"], event_b.id)
#         self.assertEqual(response.data["results"][1]["id"], event_a.id)
#         self.assertEqual(response.data["results"][2]["id"], event_c.id)
#
#     def test_event_type_sport(self):
#         type_a = EventTypeFactory.create()
#         type_b = EventTypeFactory.create(sport=type_a.sport)
#         type_c = EventTypeFactory.create()
#         expected_number_of_types = EventType.objects.filter(sport=type_a.sport).count()
#         event_type_url = reverse("example_app:eventtype-sport-list", args=[type_a.sport.id])
#         response = self.client.get(event_type_url)
#         type_a_found, type_b_found, type_c_found = find_instances_in_response([type_a, type_b, type_c], response)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             response.data["count"],
#             expected_number_of_types,
#             f"The answer should contain {expected_number_of_types} types",
#         )
#         self.assertTrue(type_a_found, "Type A was not found in Response")
#         self.assertTrue(type_b_found, "Type B was not found in Response")
#         self.assertFalse(type_c_found, "type C was found in Response, but should not be found")
