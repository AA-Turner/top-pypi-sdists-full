from typing import TYPE_CHECKING

import requests
from django.db import models, transaction

from allianceauth.admin_status.hooks import (
    Announcement,
    get_all_applications_announcements,
)
from allianceauth.services.hooks import get_extension_logger

if TYPE_CHECKING:
    from allianceauth.admin_status.models import ApplicationAnnouncement

from packaging.version import InvalidVersion, Version as Pep440Version

logger = get_extension_logger(__name__)


class ApplicationAnnouncementManager(models.Manager):
    def sync_announcements(self):
        """
        Checks all hooks if new notifications need to be created.
        """

        logger.info("Syncing announcements")

        with transaction.atomic():
            current_announcements = get_all_applications_announcements()
            self._delete_obsolete_announcements(current_announcements)
            self._store_new_announcements(current_announcements)

    def _delete_obsolete_announcements(self, current_announcements: list[Announcement]):
        """Deletes all announcements stored in the database that aren't retrieved anymore"""
        hashes = [announcement.get_hash() for announcement in current_announcements]
        self.exclude(announcement_hash__in=hashes).delete()

    def _store_new_announcements(self, current_announcements: list[Announcement]):
        """Stores a new database object for new application announcements"""

        for current_announcement in current_announcements:
            try:
                announcement = self.get(
                    announcement_hash=current_announcement.get_hash()
                )
            except self.model.DoesNotExist:
                self.create_from_announcement(current_announcement)
            else:
                # if exists update the text only
                if (
                    announcement.announcement_text
                    != current_announcement.announcement_text
                ):
                    announcement.announcement_text = (
                        current_announcement.announcement_text
                    )
                    announcement.save()

    def create_from_announcement(
        self, announcement: Announcement
    ) -> "ApplicationAnnouncement":
        """Creates from the Announcement dataclass"""
        return self.create(
            application_name=announcement.application_name,
            announcement_number=announcement.announcement_number,
            announcement_text=announcement.announcement_text,
            announcement_url=announcement.announcement_url,
            announcement_hash=announcement.get_hash(),
        )


class SoftwareVersionManager(models.Manager):
    @staticmethod
    def fetch_current_version():
        # Import helpers here to avoid circular imports at module import time
        try:
            from .templatetags.admin_status import (
                _latests_versions,
                _fetch_tags_from_gitlab,
            )
        except Exception as e:
            logger.warning(
                "Error importing admin_status templatetag helpers: %s", e, exc_info=True
            )

            return {}

        try:
            tags = _fetch_tags_from_gitlab()
        except requests.HTTPError:
            logger.warning("Error while getting gitlab release tags", exc_info=True)
            return {}

        if not tags:
            return {}

        latest_patch_version, latest_beta_version = _latests_versions(tags)

        response = {
            "latest_patch_version": str(latest_patch_version),
            "latest_beta_version": str(latest_beta_version),
        }

        return response

    def sync_versions(self):
        """
        Fetches the current version of the software from GitLab and updates the database.
        """

        # Prevent circular imports by importing the SoftwareVersion model here
        from allianceauth.admin_status.models import SoftwareVersion

        logger.info("Fetching software version")

        try:
            version = self.fetch_current_version()
        except Exception as e:
            logger.warning(f"Error while fetching software version: {e}", exc_info=True)
            return

        if not version:
            logger.warning("No version found")
            return

        # Update the database
        SoftwareVersion.objects.update_or_create(
            id=1,
            defaults={
                "latest_stable_version": version["latest_patch_version"],
                "latest_development_version": version["latest_beta_version"],
            },
        )
