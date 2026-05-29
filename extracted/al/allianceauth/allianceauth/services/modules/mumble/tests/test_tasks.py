import datetime
from unittest.mock import patch

from django.test import TestCase

from allianceauth.services.modules.mumble.tasks import tidy_up_temp_links


class TestTidyUpTempLinks(TestCase):
    @patch("allianceauth.services.modules.mumble.tasks.TempUser")
    @patch("allianceauth.services.modules.mumble.tasks.TempLink")
    @patch("allianceauth.services.modules.mumble.tasks.timezone")
    def test_expired_temp_links_are_deleted(
        self, mock_tz, mock_templink, mock_tempuser
    ):
        now = datetime.datetime(2026, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        mock_tz.now.return_value = now

        tidy_up_temp_links()

        mock_templink.objects.filter.assert_called_once_with(expires__lt=now)
        mock_templink.objects.filter.return_value.delete.assert_called_once()

    @patch("allianceauth.services.modules.mumble.tasks.TempUser")
    @patch("allianceauth.services.modules.mumble.tasks.TempLink")
    @patch("allianceauth.services.modules.mumble.tasks.timezone")
    def test_orphaned_temp_users_are_deleted_after_link_cleanup(
        self, mock_tz, mock_templink, mock_tempuser
    ):
        mock_tz.now.return_value = datetime.datetime(
            2026, 1, 1, tzinfo=datetime.timezone.utc
        )

        tidy_up_temp_links()

        mock_tempuser.objects.filter.assert_called_once_with(templink__isnull=True)
        mock_tempuser.objects.filter.return_value.delete.assert_called_once()

    @patch("allianceauth.services.modules.mumble.tasks.TempUser")
    @patch("allianceauth.services.modules.mumble.tasks.TempLink")
    @patch("allianceauth.services.modules.mumble.tasks.timezone")
    def test_link_cleanup_runs_before_user_cleanup(
        self, mock_tz, mock_templink, mock_tempuser
    ):
        call_order = []
        mock_tz.now.return_value = datetime.datetime(
            2026, 1, 1, tzinfo=datetime.timezone.utc
        )
        mock_templink.objects.filter.return_value.delete.side_effect = (
            lambda: call_order.append("links")
        )
        mock_tempuser.objects.filter.return_value.delete.side_effect = (
            lambda: call_order.append("users")
        )

        tidy_up_temp_links()

        self.assertEqual(call_order, ["links", "users"])

    @patch("allianceauth.services.modules.mumble.tasks.TempUser")
    @patch("allianceauth.services.modules.mumble.tasks.TempLink")
    @patch("allianceauth.services.modules.mumble.tasks.timezone")
    def test_nothing_deleted_when_no_expired_links_or_orphaned_users_exist(
        self, mock_tz, mock_templink, mock_tempuser
    ):
        mock_tz.now.return_value = datetime.datetime(
            2026, 1, 1, tzinfo=datetime.timezone.utc
        )
        mock_templink.objects.filter.return_value.delete.return_value = (0, {})
        mock_tempuser.objects.filter.return_value.delete.return_value = (0, {})

        tidy_up_temp_links()

        mock_templink.objects.filter.return_value.delete.assert_called_once()
        mock_tempuser.objects.filter.return_value.delete.assert_called_once()
