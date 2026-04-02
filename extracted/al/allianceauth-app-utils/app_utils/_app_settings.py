"""Settings configuration for app_utils."""

from .app_settings import clean_setting

APP_UTILS_NOTIFY_THROTTLED_TIMEOUT = clean_setting(
    "APP_UTILS_NOTIFY_THROTTLED_TIMEOUT", 86400
)
"""Timeout for throttled notifications in seconds."""


APPUTILS_ESI_DAILY_DOWNTIME_START = clean_setting("APPUTILS_ESI_DOWNTIME_START", 11.0)
"""Start time of daily downtime in UTC hours.

esi.fetch_esi_status() will report ESI as offline during this time.
"""

APPUTILS_ESI_DAILY_DOWNTIME_END = clean_setting("APPUTILS_ESI_DOWNTIME_END", 11.25)
"""End time of daily downtime in UTC hours.

esi.fetch_esi_status() will report ESI as offline during this time.
"""
