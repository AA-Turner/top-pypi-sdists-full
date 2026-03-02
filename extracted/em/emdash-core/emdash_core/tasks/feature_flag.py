"""Feature flag for Tasks v2 system."""

import os
import uuid

# Session ID is generated once per process and cached
_session_id: str | None = None


def is_tasks_v2_enabled() -> bool:
    """Check if new Tasks system is enabled.

    Checks in order (first match wins):
        1. EMDASH_TASKS_V2 env var
        2. emdash.config.json → experimental.tasks_v2
    """
    env_val = os.environ.get("EMDASH_TASKS_V2", "").strip().lower()
    if env_val in ("1", "true", "yes"):
        return True
    if env_val in ("0", "false", "no"):
        return False

    from emdash_core.core.config import get_config
    return get_config().experimental.tasks_v2


def get_current_task_list() -> str:
    """Get task list name from env var, defaults to 'default'."""
    return os.environ.get("EMDASH_TASK_LIST", "default")


def get_session_id() -> str:
    """
    Get or create session ID for this agent instance.

    Session ID is:
    1. Inherited from parent via EMDASH_SESSION_ID env var (subagent case)
    2. Generated once per process and cached
    """
    global _session_id

    # Check if inherited from parent (subagent case)
    env_session_id = os.environ.get("EMDASH_SESSION_ID")
    if env_session_id:
        return env_session_id

    # Generate new ID for this session (cached)
    if _session_id is None:
        _session_id = f"session-{uuid.uuid4().hex[:8]}"

    return _session_id


def get_assigned_tasks() -> list[str]:
    """Get list of task IDs assigned to this agent via env var."""
    work_on = os.environ.get("EMDASH_WORK_ON", "")
    if not work_on:
        return []
    return [t.strip() for t in work_on.split(",") if t.strip()]


def get_parent_session_id() -> str | None:
    """Get parent session ID if this is a subagent."""
    return os.environ.get("EMDASH_PARENT_SESSION_ID")
