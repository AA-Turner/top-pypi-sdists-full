"""Deal with app names of tasks."""

from allianceauth.services.hooks import get_extension_logger
from app_utils.logging import LoggerAddTag

from taskmonitor import __title__
from taskmonitor.app_settings import (
    TASKMONITOR_APP_NAME_MAPPING_CONFIG,
    TASKMONITOR_APP_NAME_MAPPING_DEFAULTS,
)

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


def from_task_name(task_name: str) -> str:
    """Return the app name from a typical task name, if possible.
    Otherwise return an empty string.
    """
    app_name = _extract_app_name(task_name)
    app_name = _map_app_names(app_name)
    return app_name


def _extract_app_name(task_name: str):
    """Return the app name extracted from a task name or an empty string."""
    parts = task_name.split(".")
    try:
        idx = parts.index("tasks")
    except ValueError:
        if len(parts) == 2:
            return parts[0]
        return ""

    app_name = parts[idx - 1] if idx > 0 else ""
    return app_name


def _map_app_names(app_name: str):
    """Return the mapped app name (if any) or return itself."""
    new_app_name = _app_names_mapping.get(app_name, app_name)
    return new_app_name


def _consolidate_app_names_mapping():
    """Return map of each section and their time until an update is stale."""
    mapping = {
        alternate_name: name
        for name, alternate_names in TASKMONITOR_APP_NAME_MAPPING_DEFAULTS.items()
        for alternate_name in alternate_names
    }
    for name, alternate_names in TASKMONITOR_APP_NAME_MAPPING_CONFIG.items():
        try:
            for alternate_name in alternate_names:
                mapping[alternate_name] = name
        except TypeError:
            logger.warning(
                "Mapping for %s is invalid and will be ignored. "
                "Please correct or remove it.",
                name,
            )

    return mapping


_app_names_mapping = _consolidate_app_names_mapping()
