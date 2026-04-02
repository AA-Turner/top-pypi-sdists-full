"""Settings for Inactivity."""

from app_utils.app_settings import clean_setting

INACTIVITY_TASKS_DEFAULT_PRIORITY = clean_setting(
    "INACTIVITY_TASKS_DEFAULT_PRIORITY", 6
)
"""Default priority for all tasks."""
