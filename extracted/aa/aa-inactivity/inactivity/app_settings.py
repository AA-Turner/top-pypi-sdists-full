"""Settings for Inactivity."""

from app_utils.app_settings import clean_setting

INACTIVITY_TASKS_DEFAULT_PRIORITY = clean_setting(
    "INACTIVITY_TASKS_DEFAULT_PRIORITY", 6
)
"""Default priority for all tasks."""

INACTIVITY_NOTIFY_USER = clean_setting("INACTIVITY_NOTIFY_USER", True)
"""Whether inactive users receive a direct in-app notification.

Disable this to stop users from being tipped off that they have been
detected as inactive, e.g. to prevent them from logging in solely to
dodge detection.
"""
