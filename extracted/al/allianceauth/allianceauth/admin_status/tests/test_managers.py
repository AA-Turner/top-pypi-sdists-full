from importlib import import_module

import requests

from unittest.mock import patch, MagicMock
from django.test import TestCase
from packaging.version import Version as Pep440Version
from allianceauth.admin_status.hooks import Announcement
from allianceauth.admin_status.models import ApplicationAnnouncement
from allianceauth.admin_status.managers import SoftwareVersionManager


class TestApplicationAnnouncementManagerIntegration(TestCase):
    def test_create_from_announcement_persists_expected_fields(self):
        ann = Announcement("MyApp", "https://example/1", 1, "Title One")
        created = ApplicationAnnouncement.objects.create_from_announcement(ann)
        self.assertEqual(created.application_name, "MyApp")
        self.assertEqual(created.announcement_number, 1)
        self.assertEqual(created.announcement_text, "Title One")
        self.assertEqual(created.announcement_url, "https://example/1")
        self.assertEqual(created.announcement_hash, ann.get_hash())

    def test_sync_announcements_creates_updates_and_deletes_records(self):
        # existing entries: keep_one and remove_me
        keep_ann = Announcement("KeepApp", "https://keep/1", 1, "Keep me")
        remove_ann = Announcement("RemoveApp", "https://rm/1", 1, "Remove me")
        keep_obj = ApplicationAnnouncement.objects.create_from_announcement(keep_ann)
        remove_obj = ApplicationAnnouncement.objects.create_from_announcement(
            remove_ann
        )

        # prepare current announcements: same hash as keep_obj but updated text
        updated_keep = Announcement("KeepApp", "https://keep/1", 1, "Updated text")
        with patch(
            "allianceauth.admin_status.managers.get_all_applications_announcements",
            return_value=[updated_keep],
        ):
            ApplicationAnnouncement.objects.sync_announcements()

        # remove_obj should be deleted
        all_objs = list(ApplicationAnnouncement.objects.all())
        self.assertEqual(len(all_objs), 1)
        remaining = all_objs[0]
        self.assertEqual(remaining.application_name, "KeepApp")
        # text should have been updated
        self.assertEqual(remaining.announcement_text, "Updated text")


class TestSoftwareVersionManager(TestCase):
    def test_fetch_current_version_returns_empty_on_tag_fetch_error(self):
        # patch the templatetag fetch to raise HTTPError
        with patch(
            "allianceauth.admin_status.templatetags.admin_status._fetch_tags_from_gitlab",
            side_effect=requests.HTTPError(),
        ):
            result = SoftwareVersionManager.fetch_current_version()
            self.assertEqual(result, {})

    def test_fetch_current_version_returns_versions_when_tags_present(self):
        fake_tags = [{"name": "2.0.0"}, {"name": "2.1.0a1"}]
        with (
            patch(
                "allianceauth.admin_status.templatetags.admin_status._fetch_tags_from_gitlab",
                return_value=fake_tags,
            ),
            patch(
                "allianceauth.admin_status.templatetags.admin_status._latests_versions",
                return_value=(Pep440Version("2.0.0"), Pep440Version("2.1.0a1")),
            ),
        ):
            result = SoftwareVersionManager.fetch_current_version()
            self.assertIn("latest_patch_version", result)
            self.assertIn("latest_beta_version", result)
            self.assertEqual(result["latest_patch_version"], "2.0.0")
            self.assertEqual(result["latest_beta_version"], "2.1.0a1")

    def test_sync_versions_updates_database_when_fetch_returns_versions(self):
        models_mod = import_module("allianceauth.admin_status.models")
        # Ensure SoftwareVersion attribute exists in models module and has an objects.update_or_create
        mock_sw = MagicMock()
        mock_sw.objects = MagicMock()
        models_mod.SoftwareVersion = mock_sw

        with patch.object(
            SoftwareVersionManager,
            "fetch_current_version",
            return_value={
                "latest_patch_version": "3.0.0",
                "latest_beta_version": "3.1.0a1",
            },
        ):
            mgr = SoftwareVersionManager()
            mgr.sync_versions()

        mock_sw.objects.update_or_create.assert_called_once_with(
            id=1,
            defaults={
                "latest_stable_version": "3.0.0",
                "latest_development_version": "3.1.0a1",
            },
        )

    def test_sync_versions_does_not_update_database_when_no_version_found(self):
        models_mod = import_module("allianceauth.admin_status.models")
        mock_sw = MagicMock()
        mock_sw.objects = MagicMock()
        models_mod.SoftwareVersion = mock_sw

        with patch.object(
            SoftwareVersionManager, "fetch_current_version", return_value={}
        ):
            mgr = SoftwareVersionManager()
            mgr.sync_versions()

        mock_sw.objects.update_or_create.assert_not_called()

    def test_sync_versions_does_not_update_database_when_fetch_raises_exception(self):
        models_mod = import_module("allianceauth.admin_status.models")
        mock_sw = MagicMock()
        mock_sw.objects = MagicMock()
        models_mod.SoftwareVersion = mock_sw

        with patch.object(
            SoftwareVersionManager,
            "fetch_current_version",
            side_effect=Exception("fetch failed"),
        ):
            mgr = SoftwareVersionManager()
            mgr.sync_versions()

        mock_sw.objects.update_or_create.assert_not_called()
