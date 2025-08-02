"""Settings configuration for app_utils."""

from .app_settings import clean_setting

APP_UTILS_NOTIFY_THROTTLED_TIMEOUT = clean_setting(
    "APP_UTILS_NOTIFY_THROTTLED_TIMEOUT", 86400
)
"""Timeout for throttled notifications in seconds."""

APPUTILS_ESI_ERROR_LIMIT_THRESHOLD = clean_setting(
    "APPUTILS_ESI_ERROR_LIMIT_THRESHOLD", 25
)
"""ESI error limit remain threshold.

The number of remaining errors is counted down from 100 as errors occur.
Because multiple tasks may request the value simultaneously and get the same response,
the threshold must be above 0 to prevent the API from shutting down with a 420 error.
"""

APPUTILS_ESI_DAILY_DOWNTIME_START = clean_setting("APPUTILS_ESI_DOWNTIME_START", 11.0)
"""Start time of daily downtime in UTC hours.

esi.fetch_esi_status() will report ESI as offline during this time.
"""

APPUTILS_ESI_DAILY_DOWNTIME_END = clean_setting("APPUTILS_ESI_DOWNTIME_END", 11.25)
"""End time of daily downtime in UTC hours.

esi.fetch_esi_status() will report ESI as offline during this time.
"""
