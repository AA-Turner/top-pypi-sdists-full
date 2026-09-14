from django.test import RequestFactory
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from allianceauth.admin_status.admin import ApplicationAnnouncementAdmin
from allianceauth.admin_status.models import ApplicationAnnouncement
from allianceauth.utils.testing import NoSocketsTestCase


class TestApplicationAnnouncementAdmin(NoSocketsTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.admin_instance = ApplicationAnnouncementAdmin(
            ApplicationAnnouncement, self.site
        )
        # create a sample announcement to use when testing delete permission with an object
        self.announcement = ApplicationAnnouncement.objects.create(
            application_name="UnitTest App",
            announcement_number=1,
            announcement_text="An announcement",
            announcement_url="https://example.org/1",
            announcement_hash="unittest-hash-1",
        )

    def test_has_add_permission_is_false_for_regular_request(self):
        request = self.factory.get("/")
        self.assertFalse(self.admin_instance.has_add_permission(request))

    def test_has_add_permission_is_false_for_superuser_request(self):
        request = self.factory.get("/")
        request.user = type(
            "U", (), {"is_active": True, "is_staff": True, "is_superuser": True}
        )()
        self.assertFalse(self.admin_instance.has_add_permission(request))

    def test_has_delete_permission_is_false_when_obj_is_none(self):
        request = self.factory.get("/")
        self.assertFalse(self.admin_instance.has_delete_permission(request, obj=None))

    def test_has_delete_permission_is_false_for_existing_object(self):
        request = self.factory.get("/")
        self.assertFalse(
            self.admin_instance.has_delete_permission(request, obj=self.announcement)
        )

    def test_admin_registration_and_configuration_fields(self):
        # admin class should be registered for the model
        self.assertIn(ApplicationAnnouncement, admin.site._registry)
        # verify list_display, readonly_fields and fields contain the expected keys
        expected_list_display = {
            "application_name",
            "announcement_number",
            "announcement_text",
            "hide_announcement",
        }
        expected_readonly = {
            "application_name",
            "announcement_number",
            "announcement_text",
            "announcement_url",
        }
        expected_fields = {
            "application_name",
            "announcement_number",
            "announcement_text",
            "announcement_url",
            "hide_announcement",
        }

        self.assertTrue(
            expected_list_display.issubset(set(self.admin_instance.list_display))
        )
        self.assertTrue(
            expected_readonly.issubset(set(self.admin_instance.readonly_fields))
        )
        self.assertTrue(expected_fields.issubset(set(self.admin_instance.fields)))
