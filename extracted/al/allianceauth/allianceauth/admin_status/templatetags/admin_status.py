import logging

import requests
from packaging.version import InvalidVersion, Version as Pep440Version, Version

from django import template
from django.conf import settings
from django.db.models import Case, When, Value, IntegerField

from allianceauth import __version__
from allianceauth.admin_status.models import ApplicationAnnouncement, SoftwareVersion
from allianceauth.authentication.task_statistics.counters import (
    dashboard_results,
)

register = template.Library()

# timeout for all requests
REQUESTS_TIMEOUT = 5  # 5 seconds
# max pages to be fetched from gitlab
MAX_PAGES = 50

GITLAB_AUTH_REPOSITORY_TAGS_URL = (
    "https://gitlab.com/api/v4/projects/allianceauth%2Fallianceauth/repository/tags"
)

logger = logging.getLogger(__name__)


@register.simple_tag()
def decimal_widthratio(this_value, max_value, max_width) -> str:
    if max_value == 0:
        return str(0)

    return str(round(this_value / max_value * max_width, 2))


@register.inclusion_tag("admin_status/overview.html")
def status_overview() -> dict:
    response = {
        "notifications": [],
        "current_version": __version__,
        "tasks_succeeded": 0,
        "tasks_retried": 0,
        "tasks_failed": 0,
        "tasks_total": 0,
        "tasks_hours": 0,
        "earliest_task": None,
        "debug": settings.DEBUG if settings.DISPLAY_DEBUG else False,
    }
    response.update(_current_notifications())
    response.update(_current_version_summary())
    response.update(_celery_stats())
    return response


def _celery_stats() -> dict:
    hours = getattr(settings, "ALLIANCEAUTH_DASHBOARD_TASKS_MAX_HOURS", 24)
    results = dashboard_results(hours=hours)
    return {
        "tasks_succeeded": results.succeeded,
        "tasks_retried": results.retried,
        "tasks_failed": results.failed,
        "tasks_total": results.total,
        "tasks_hours": results.hours,
        "earliest_task": results.earliest_task,
    }


def _current_notifications() -> dict:
    """returns announcements from AllianceAuth and third party applications"""

    # Ensure "Alliance Auth" appears first, then the rest alphabetically.
    # We annotate a custom ordering field: 0 for Alliance Auth, 1 for others.
    application_announcements_qs = (
        ApplicationAnnouncement.objects.annotate(
            order_priority=Case(
                When(application_name="Alliance Auth", then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("order_priority", "application_name", "-announcement_number")
    )

    # change the dict format to a list of dicts for easier template rendering
    # `application_notifications = [{"application_name": "", "announcements": []}]`
    # Build groups in Python to ensure we preserve the queryset order and avoid
    # duplicates regardless of DB distinct behavior. This also avoids extra
    # per-application queries by iterating the queryset once.
    grouped = {}
    ordered_names = []

    for announcement in application_announcements_qs:
        name = announcement.application_name

        if name not in grouped:
            grouped[name] = []
            ordered_names.append(name)

        grouped[name].append(announcement)

    application_notifications = [
        {
            "application_name": app_name,
            "announcements": [
                {
                    "announcement_number": announcement.announcement_number,
                    "announcement_text": announcement.announcement_text,
                    "announcement_url": announcement.announcement_url,
                    "hide_announcement": announcement.hide_announcement,
                }
                for announcement in grouped.get(app_name, [])
            ],
        }
        for app_name in ordered_names
    ]

    response = {
        "notifications": application_notifications,
    }

    return response


def _current_version_summary() -> dict[str, bool | str | None | Version]:
    """returns the current version info"""

    version_summary = SoftwareVersion.get_solo()

    current_version = Pep440Version(__version__)

    # Safely parse stored versions (they may be empty strings or invalid)
    latest_stable_version = None
    latest_development_version = None
    try:
        if version_summary.latest_stable_version:
            latest_stable_version = Pep440Version(version_summary.latest_stable_version)
    except InvalidVersion:
        latest_stable_version = None

    try:
        if version_summary.latest_development_version:
            latest_development_version = Pep440Version(
                version_summary.latest_development_version
            )
    except InvalidVersion:
        latest_development_version = None

    has_latest_patch = (
        current_version >= latest_stable_version
        if latest_stable_version is not None
        else False
    )

    has_current_beta = (
        (current_version <= latest_development_version)
        and (
            latest_stable_version <= latest_development_version
            if latest_stable_version is not None
            else True
        )
        if latest_development_version is not None
        else False
    )

    logger.debug(
        f"Current version: {current_version}, Latest stable: {version_summary.latest_stable_version}, Latest beta: {version_summary.latest_development_version}"
    )

    return {
        "latest_patch": has_latest_patch,
        "latest_beta": has_current_beta,
        "current_version": __version__,
        "latest_patch_version": latest_stable_version,
        "latest_beta_version": latest_development_version,
    }


def _fetch_tags_from_gitlab():
    return _fetch_list_from_gitlab(GITLAB_AUTH_REPOSITORY_TAGS_URL)


def _latests_versions(tags: list) -> tuple:
    """returns latests version from given tags list

    Non-compliant tags will be ignored
    """
    versions = []
    betas = []
    for tag in tags:
        try:
            version = Pep440Version(tag.get("name"))
        except InvalidVersion:
            pass
        else:
            if version.is_prerelease or version.is_devrelease:
                betas.append(version)
            else:
                versions.append(version)

    latest_patch_version = max(versions)
    latest_beta_version = max(betas)
    return latest_patch_version, latest_beta_version


def _fetch_list_from_gitlab(url: str, max_pages: int = MAX_PAGES) -> list:
    """returns a list from the GitLab API. Supports paging"""
    result = []

    for page in range(1, max_pages + 1):
        try:
            request = requests.get(url, params={"page": page}, timeout=REQUESTS_TIMEOUT)
            request.raise_for_status()
        except requests.exceptions.RequestException as e:
            error_str = str(e)

            logger.warning(
                f"Unable to fetch from GitLab API. Error: {error_str}",
                exc_info=True,
            )

            return result

        result += request.json()

        if "x-total-pages" in request.headers:
            try:
                total_pages = int(request.headers["x-total-pages"])
            except ValueError:
                total_pages = None
        else:
            total_pages = None

        if not total_pages or page >= total_pages:
            break

    return result
