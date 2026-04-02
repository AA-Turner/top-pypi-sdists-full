"""Settings for Task Monitor."""

from app_utils.app_settings import clean_setting

TASKMONITOR_ENABLED = clean_setting("TASKMONITOR_ENABLED", True)
"""Global switch to enable/disable task monitor."""

TASKMONITOR_DATA_MAX_AGE = clean_setting("TASKMONITOR_DATA_MAX_AGE", 24)
"""Max age of logged tasks in hours. Older logs be deleted automatically."""

TASKMONITOR_DELETE_STALE_BATCH_SIZE = clean_setting(
    "TASKMONITOR_DELETE_STALE_BATCH_SIZE", 5_000
)
"""Size of task logs deleted together in one batch."""

TASKMONITOR_HOUSEKEEPING_FREQUENCY = clean_setting(
    "TASKMONITOR_HOUSEKEEPING_FREQUENCY", 30
)
"""Frequency of house keeping runs in minutes."""

TASKMONITOR_REPORTS_MAX_AGE = clean_setting("TASKMONITOR_REPORTS_MAX_AGE", 60)
"""Max age of cached reports in minutes."""


TASKMONITOR_QUEUED_TASKS_CACHE_TIMEOUT = clean_setting(
    "TASKMONITOR_QUEUED_TASKS_CACHE_TIMEOUT", 10
)
"""Timeout for caching queued tasks in seconds. 0 will deactivate the cache."""

TASKMONITOR_QUEUED_TASKS_ADMIN_LIMIT = clean_setting(
    "TASKMONITOR_QUEUED_TASKS_ADMIN_LIMIT", 100_000
)
"""The admin page will stop showing the list of queued tasks above this limit
to protect against crashing caused by too high memory consumption.
"""

TASKMONITOR_REPORTS_MAX_TOP = clean_setting("TASKMONITOR_REPORTS_MAX_TOP", 20)
"""Max items to show in the top reports. e.g. 10 will shop the top ten items."""

TASKMONITOR_TRUNCATE_NESTED_DATA = clean_setting(
    "TASKMONITOR_TRUNCATE_NESTED_DATA", True
)
"""Whether deeply nested task params and results are truncated."""

TASKMONITOR_APP_NAME_MAPPING_CONFIG = clean_setting(
    "TASKMONITOR_APP_NAME_MAPPING_CONFIG", {}
)
"""Ability to map tasks to the same app name.
Map must be a dictionary with string keys and list of strings as value.
All app names in the list will be replaced by it's key.
"""

TASKMONITOR_APP_NAME_MAPPING_DEFAULTS = {"standingsrequests": ["standings_requests"]}
"""Default app mappings.

Can be overridden or extended through TASKMONITOR_APP_NAME_MAPPING_CONFIG.
"""
