"""A plan stage's key (`training`, `eval-v2`): the id a run, an experiment or a plan file names a stage by; the
one-time warnings a create gives about the stage it carried; and the statuses and limits a plan write is held to.
Light on purpose: the CLI reads these at startup without loading the SDK client."""

from __future__ import annotations

import re
import threading
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .. import errors
from ...foundation.compat.compat import StrEnum
from ...foundation.safe_warn import safe_warn

#: Short, lowercase, written once and never changed (twin: probe_contracts PLAN_STAGE_KEY_PATTERN).
STAGE_KEY_PATTERN = r"^[a-z][a-z0-9-]{1,39}$"
_STAGE_KEY = re.compile(STAGE_KEY_PATTERN)
#: The server feature (`GET /v1/server/features`) that says creates take `stage`.
PLAN_STAGES_FEATURE = "plan_stages"
#: The server also stores and serves the plan's Markdown.
PLAN_BODY_FEATURE = "plan_body"
#: What a refused key is told.
STAGE_KEY_RULE = "2-40 lowercase letters, digits or '-', starting with a letter"


@dataclass(frozen=True)
class PlanLimits:
    """The server's limits on a plan write (twin: app/projects/plans/schemas.py)."""

    title: int = 200
    criterion: int = 1000
    source_path: int = 500
    repo: int = 300
    stages: int = 6
    evidence: int = 20
    note: int = 2000
    body_bytes: int = 128 * 1024


PLAN_LIMITS = PlanLimits()


class StageStatus(StrEnum):
    """A stage's status (twin: probe_contracts plan status)."""

    PLANNED = "planned"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETE = "complete"


def is_stage_key(value: object) -> bool:
    """Is `value` a key the server would take?"""
    return isinstance(value, str) and _STAGE_KEY.fullmatch(value) is not None


def to_stage_key(value: object, *, label: str = "stage") -> str:
    """`value` as a stage key; anything else is refused before any request. `label` names the argument."""
    text = value.strip() if isinstance(value, str) else value
    if not is_stage_key(text):
        raise errors.ValidationError(
            f"{label} {value!r} is not a stage key: {STAGE_KEY_RULE} (`probe plan show`)"
        )
    return str(text)


def warn_if_stage_not_applied(stage: str | None, row: Mapping[str, Any] | None) -> None:
    """One warning when a run create that sent `stage` was not answered `stage_applied: true`: false means the key
    is not a live stage of the project's plan (the run may inherit its experiment's); no answer means the server
    did not say it kept it."""
    if stage is None or not isinstance(row, Mapping) or row.get("stage_applied") is True:
        return
    fix = f"probe run set {row.get('id') or '<run>'} --stage"
    if row.get("stage_applied") is False:
        warn_stage_once(
            f"unapplied:{stage}",
            f"probe: {stage!r} is not a stage of this project's plan; the run "
            f"has no stage of its own. Fix it: {fix} <key> (`probe plan show` lists them)",
        )
    else:
        warn_stage_once(
            f"unanswered:{stage}",
            f"probe: the server did not say it kept stage {stage!r}. Check "
            f"`probe plan show`; set it with: {fix} {stage}",
        )


_WARNED: set[str] = set()
_WARNED_LOCK = threading.Lock()


def warn_stage_once(kind: str, message: str) -> None:
    """Print `message` the first time this process meets `kind`."""
    with _WARNED_LOCK:
        if kind in _WARNED:
            return
        _WARNED.add(kind)
    safe_warn.warn(message, stacklevel=3)
