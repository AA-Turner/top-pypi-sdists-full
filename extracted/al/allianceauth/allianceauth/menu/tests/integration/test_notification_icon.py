from django.test import TestCase
from django.urls import reverse

from allianceauth.menu.tests.utils import extract_html
from allianceauth.notifications.models import Notification
from allianceauth.tests.auth_utils import AuthUtils


class TestNotificationIcon(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AuthUtils.create_member("member")
        AuthUtils.add_main_character_2(cls.user, "Member Char", 1001)
        # Creating the user sends notifications, start from none
        Notification.objects.filter(user=cls.user).delete()

    def setUp(self):
        # The unread count is cached per user pk, which can outlive other tests' rows
        Notification.objects.invalidate_user_notification_cache(self.user.pk)
        self.client.force_login(self.user)

    def get_icon(self, url_name):
        soup = extract_html(self.client.get(reverse(url_name)))
        return soup.select_one("#menu_item_notifications")

    def test_bells_found_by_refresh_script(self):
        # refresh-notification-icon.js toggles text-danger on '#menu_item_notifications .fa-bell'
        icon = self.get_icon("authentication:dashboard")
        self.assertTrue(icon.select(".fa-bell"))

    def test_no_unread_notifications(self):
        icon = self.get_icon("authentication:dashboard")
        self.assertFalse(icon.select(".fa-bell.text-danger"))

    def test_unread_notifications(self):
        Notification.objects.notify_user(self.user, "Hello")
        icon = self.get_icon("authentication:dashboard")
        bells = icon.select(".fa-bell")
        self.assertEqual(len(bells), len(icon.select(".fa-bell.text-danger")))

    def test_links_to_notifications(self):
        icon = self.get_icon("authentication:dashboard")
        self.assertEqual(icon.select_one("a.nav-link")["href"], reverse("notifications:list"))

    def test_active_on_notifications_page(self):
        icon = self.get_icon("notifications:list")
        self.assertIn("active", icon.select_one("a.nav-link")["class"])

    def test_not_active_elsewhere(self):
        icon = self.get_icon("authentication:dashboard")
        self.assertNotIn("active", icon.select_one("a.nav-link")["class"])
