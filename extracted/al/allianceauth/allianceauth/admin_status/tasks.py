from celery import shared_task

from allianceauth.admin_status.models import ApplicationAnnouncement, SoftwareVersion
from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


@shared_task()
def fetch_announcements() -> None:
    """
    Fetches announcements from AllianceAuth and third party applications

    :return:
    """

    logger.info("Task: Fetching announcements")

    ApplicationAnnouncement.objects.sync_announcements()


@shared_task()
def fetch_software_version() -> None:
    """
    Fetches the current version of the software from GitLab

    :return:
    """

    logger.info("Task: Fetching software versions")

    SoftwareVersion.objects.sync_versions()


@shared_task()
def run_admin_status_tasks() -> None:
    """
    Runs all tasks related to the admin status dashboard

    :return:
    """

    logger.info("Task: Running admin status tasks")

    # Fetch announcements
    fetch_announcements.delay()

    # Fetch software version
    fetch_software_version.delay()
