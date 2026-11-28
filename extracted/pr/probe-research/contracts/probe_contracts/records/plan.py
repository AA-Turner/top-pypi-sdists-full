"""A project plan's stage vocabulary: the key format and the statuses. One copy for the server, CLI and SDK.
How plans work: app/projects/plans/DESIGN.md."""

from __future__ import annotations

from ..compat import StrEnum

#: A stage's key: written once in the plan file (`Stage: <key>`), never changed; links and updates name it.
PLAN_STAGE_KEY_PATTERN = r"^[a-z][a-z0-9-]{1,39}$"


def get_stage_key_text(value: object) -> object:
    """A create's `stage` as text: a number, object or list becomes its string form, so it reads as an
    unknown key (nothing applied) instead of refusing the create. None stays None."""
    return value if value is None or isinstance(value, str) else str(value)


class PlanStageStatus(StrEnum):
    """Where a stage stands. `complete` comes only from an update, never derived."""

    PLANNED = "planned"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETE = "complete"
