from unittest.mock import patch
from allianceauth.admin_status.tasks import fetch_announcements, fetch_software_version
from allianceauth.utils.testing import NoSocketsTestCase


class TestFetchAnnouncementsTask(NoSocketsTestCase):
    def test_calls_manager_sync_announcements(self):
        with patch(
            "allianceauth.admin_status.tasks.ApplicationAnnouncement.objects.sync_announcements"
        ) as mock_sync:
            fetch_announcements()
            mock_sync.assert_called_once()

    def test_propagates_exception_from_manager(self):
        with patch(
            "allianceauth.admin_status.tasks.ApplicationAnnouncement.objects.sync_announcements",
            side_effect=Exception("sync failed"),
        ):
            with self.assertRaises(Exception):
                fetch_announcements()


class TestFetchSoftwareVersionTask(NoSocketsTestCase):
    def test_calls_manager_sync_versions(self):
        with patch(
            "allianceauth.admin_status.tasks.SoftwareVersion.objects.sync_versions"
        ) as mock_sync:
            fetch_software_version()
            mock_sync.assert_called_once()

    def test_propagates_exception_from_manager(self):
        with patch(
            "allianceauth.admin_status.tasks.SoftwareVersion.objects.sync_versions",
            side_effect=Exception("sync failed"),
        ):
            with self.assertRaises(Exception):
                fetch_software_version()


class TestRunAdminStatusTasks(NoSocketsTestCase):
    def test_triggers_both_tasks_async(self):
        with (
            patch(
                "allianceauth.admin_status.tasks.fetch_announcements.delay"
            ) as mock_ann_delay,
            patch(
                "allianceauth.admin_status.tasks.fetch_software_version.delay"
            ) as mock_ver_delay,
        ):
            from allianceauth.admin_status.tasks import run_admin_status_tasks

            run_admin_status_tasks()
            mock_ann_delay.assert_called_once()
            mock_ver_delay.assert_called_once()

    def test_propagates_exception_when_first_delay_raises_and_second_not_called(self):
        with patch(
            "allianceauth.admin_status.tasks.fetch_announcements.delay",
            side_effect=Exception("boom"),
        ):
            with patch(
                "allianceauth.admin_status.tasks.fetch_software_version.delay"
            ) as mock_ver_delay:
                from allianceauth.admin_status.tasks import run_admin_status_tasks

                with self.assertRaises(Exception):
                    run_admin_status_tasks()
                self.assertFalse(mock_ver_delay.called)
