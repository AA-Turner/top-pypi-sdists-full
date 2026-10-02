from typing import Any, Dict, List, Optional, Union

from anyscale._private.sdk import sdk_command
from anyscale.scheduler._private.scheduler_sdk import PrivateSchedulerSDK
from anyscale.scheduler.models import (
    SchedulerConfig,
    SchedulerConfigVersion,
    SchedulerConfigVersionSummary,
)


_SCHEDULER_SDK_SINGLETON_KEY = "scheduler_sdk"

_APPLY_CONFIG_EXAMPLE = """
import anyscale
from anyscale.scheduler.models import SchedulerConfig

# Load from a YAML file (recommended).
config = SchedulerConfig.from_yaml("scheduler-config.yaml")
version = anyscale.scheduler.apply_config(config)
print(f"Applied scheduler config version {version}")

# Or pass a dict directly.
anyscale.scheduler.apply_config({
    "resource_flavors": [...],
    "resource_queues": [...],
    "scheduling_rules": [...],
})
"""

_APPLY_CONFIG_DOCSTRINGS = {
    "config": (
        "Scheduler config to apply. Either a SchedulerConfig dataclass or a dict "
        "matching the API schema."
    ),
}


_ROLLBACK_CONFIG_EXAMPLE = """
import anyscale

# Re-apply the contents of version 3 as a new version.
new_version = anyscale.scheduler.rollback_config(version=3)
print(f"Rolled back to version 3, applied as version {new_version}")
"""

_ROLLBACK_CONFIG_DOCSTRINGS = {
    "version": "Existing config version whose contents are applied as a new version.",
}


_GET_CONFIG_EXAMPLE = """
import anyscale

# Active config (default).
active = anyscale.scheduler.get_config()
print(active.version, active.config)

# A specific historical version.
v3 = anyscale.scheduler.get_config(version=3)
"""

_GET_CONFIG_DOCSTRINGS = {
    "version": "Specific version to fetch. Omit to fetch the active config.",
}


_LIST_CONFIG_VERSIONS_EXAMPLE = """
import anyscale

# Default: 10 most recent versions.
for summary in anyscale.scheduler.list_config_versions():
    print(summary.version, summary.created_at, summary.creator_id)

# Fetch any number; the SDK paginates internally.
recent = anyscale.scheduler.list_config_versions(max_items=200)
"""

_LIST_CONFIG_VERSIONS_DOCSTRINGS = {
    "max_items": "Maximum number of versions to return. Defaults to 10.",
}


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_APPLY_CONFIG_EXAMPLE,
    arg_docstrings=_APPLY_CONFIG_DOCSTRINGS,
)
def apply_config(
    config: Union[SchedulerConfig, Dict[str, Any]],
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> int:
    """Apply a scheduler config (creates a new active version). Returns the new version number.

    The previous active version becomes inactive but remains queryable via
    list_config_versions and get_config(version=N). Schema is validated locally
    before the API call; cross-reference checks (queue refs, flavor refs)
    happen on the server.
    """
    return _private_sdk.apply_config(config)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_ROLLBACK_CONFIG_EXAMPLE,
    arg_docstrings=_ROLLBACK_CONFIG_DOCSTRINGS,
)
def rollback_config(
    version: int,
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> int:
    """Roll back to an existing config version. Returns the new version number.

    The config stored at `version` is applied as a new active version. `version`
    itself stays in history unchanged, so a rollback is itself reversible.
    """
    return _private_sdk.rollback_config(version=version)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_GET_CONFIG_EXAMPLE,
    arg_docstrings=_GET_CONFIG_DOCSTRINGS,
)
def get_config(
    version: Optional[int] = None,
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> SchedulerConfigVersion:
    """Get the active scheduler config (or a specific version).

    Returns the version number, active flag, creator, created_at, and the full
    SchedulerConfig.
    """
    return _private_sdk.get_config(version=version)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_LIST_CONFIG_VERSIONS_EXAMPLE,
    arg_docstrings=_LIST_CONFIG_VERSIONS_DOCSTRINGS,
)
def list_config_versions(
    max_items: int = 10,
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> List[SchedulerConfigVersionSummary]:
    """List scheduler config version history (newest first).

    Returns metadata (version, created_at, creator_id) without the config blob.
    Use get_config(version=N) to fetch the full config for a specific version.
    """
    return _private_sdk.list_config_versions(max_items=max_items)  # type: ignore
