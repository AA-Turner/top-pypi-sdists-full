from typing import Optional


# GRS scheduling priority bounds for the user-facing `priority` field. None = unset;
# 0 is valid (distinct from unset). Single CLI source of truth, mirroring the backend
# `SCHEDULING_PRIORITY_MIN/MAX` in backend/server/common/models/validation.py.
SCHEDULING_PRIORITY_MIN = 0
SCHEDULING_PRIORITY_MAX = 1000


def validate_scheduling_priority(priority: Optional[int]) -> None:
    """Validate the GRS `priority` field, shared across workload config models."""
    if priority is None:
        return

    if not isinstance(priority, int):
        raise TypeError(f"'priority' must be an int (it is {type(priority)}).")

    if priority < SCHEDULING_PRIORITY_MIN or priority > SCHEDULING_PRIORITY_MAX:
        raise ValueError(
            f"'priority' must be >= {SCHEDULING_PRIORITY_MIN} "
            f"and <= {SCHEDULING_PRIORITY_MAX}."
        )
