"""A run's declared type (`general` or `rl`) as the text the server takes, checked before any request."""

from __future__ import annotations

from ...generated.records import RunType
from .. import errors


def to_run_type(value: str | RunType, *, label: str = "run_type") -> str:
    """``value`` as a `RunType` value; anything else is refused here, so a typo creates nothing.

    Case-sensitive like the server: "RL" is refused, not guessed. ``label`` names the argument."""
    try:
        return RunType(value).value
    except ValueError:
        choices = ", ".join(member.value for member in RunType)
        raise errors.ValidationError(
            f"{label} {value!r} is not a run type. Use one of: {choices} "
            "(rl for RL training or agent evals)."
        ) from None
