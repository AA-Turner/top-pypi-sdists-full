from unittest.mock import patch

from allianceauth.admin_status.models import ApplicationAnnouncement
from allianceauth.utils.testing import NoSocketsTestCase


class TestApplicationAnnouncementModel(NoSocketsTestCase):
    def test___str__returns_application_and_number(self):
        obj = ApplicationAnnouncement.objects.create(
            application_name="MyApp",
            announcement_number=7,
            announcement_text="Summary",
            announcement_url="https://example/7",
            announcement_hash="hash-7",
        )
        self.assertEqual(str(obj), "MyApp announcement #7")

    def test_is_hidden_reflects_hide_announcement_field(self):
        visible = ApplicationAnnouncement.objects.create(
            application_name="AppVis",
            announcement_number=1,
            announcement_text="Visible",
            announcement_url="https://example/1",
            announcement_hash="hash-vis",
            hide_announcement=False,
        )
        hidden = ApplicationAnnouncement.objects.create(
            application_name="AppHidden",
            announcement_number=2,
            announcement_text="Hidden",
            announcement_url="https://example/2",
            announcement_hash="hash-hid",
            hide_announcement=True,
        )
        self.assertFalse(visible.is_hidden())
        self.assertTrue(hidden.is_hidden())
