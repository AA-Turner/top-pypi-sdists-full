"""A run's total steps (the step it is set to end at) as the whole number the server takes, checked before any request."""

from __future__ import annotations

from .. import errors

#: The server's bound (`TotalSteps`, app/runs/schemas.py): a JSON number holds it exactly.
MAX_TOTAL_STEPS = 2**53 - 1


def to_total_steps(value: int, *, label: str = "total_steps") -> int:
    """``value`` as a step count from 1 to `MAX_TOTAL_STEPS`; anything else is refused here, so a typo creates
    nothing. A bool or a float is refused, not rounded. ``label`` names the argument."""
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_TOTAL_STEPS:
        raise errors.ValidationError(
            f"{label} {value!r} is not a step count. Pass the whole number of steps the run is set to end at (1 or more)."
        )
    return value


def read_total_steps(value: object) -> int | None:
    """A trainer's own step count as `to_total_steps` takes it, or None when it is unknown (None, 0, -1, inf, a
    float that is not whole): what an integration sends only when it has one."""
    if isinstance(value, bool):
        return None
    if isinstance(value, float):
        if not value.is_integer():
            return None
        value = int(value)
    if isinstance(value, int) and 1 <= value <= MAX_TOTAL_STEPS:
        return value
    return None
