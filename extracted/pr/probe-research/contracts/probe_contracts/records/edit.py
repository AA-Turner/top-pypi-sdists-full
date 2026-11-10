"""RunEdit: one change to a run's recorded data (hide, shift, scale, rename, move, set config, revert), kept with who
made it and why, so it can be undone. How edits apply: app/runs/edits/DESIGN.md."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..compat import StrEnum
from .records import Record


class EditOp(StrEnum):
    """What an edit does. One list for the server, SDK, CLI, MCP and dashboard (review A4)."""

    HIDE = "hide"
    SHIFT_STEP = "shift_step"
    SHIFT_TIME = "shift_time"
    SCALE = "scale"
    RENAME = "rename"
    MOVE_SERIES = "move_series"
    SET_CONFIG = "set_config"
    REVERT = "revert"


class EditState(StrEnum):
    """Where an edit is. Reads of its series carry an `edit_applying` advisory until it is applied or failed."""

    APPLYING = "applying"
    APPLIED = "applied"
    # Three failed attempts: the edit undoes what it did, then reads `failed` ("failed, nothing changed").
    ROLLING_BACK = "rolling_back"
    FAILED = "failed"


class EditPhase(StrEnum):
    """The last durable step of an apply or an undo, so a retry resumes there instead of guessing."""

    CREATED = "created"
    # Apply: originals copied to the shelf, transformed copies written, originals taken out of the main table.
    SHELVED = "shelved"
    WRITTEN = "written"
    ORIGINALS_REMOVED = "originals_removed"
    # Undo (a revert, or a failed edit rolling back): its own rows removed, then the shelf put back.
    EDITED_REMOVED = "edited_removed"
    RESTORED = "restored"


class EditActorKind(StrEnum):
    """Who made an edit: a person in the dashboard or CLI, a coding agent, the SDK (config, rewind), an import."""

    PERSON = "person"
    AGENT = "agent"
    SDK = "sdk"
    IMPORT = "import"


class EditTarget(BaseModel):
    """Which recorded data an edit touches. Steps are the half-open range [from_step, to_step), clocks
    [from_time, to_time). No `keys` means every key; no `kinds` means every kind but `hardware`."""

    #: Exact keys or globs (`eval/*`).
    keys: list[str] = Field(default_factory=list)
    kinds: list[str] = Field(default_factory=list)
    #: A coordinate filter: series whose dimensions contain these.
    dimensions: dict | None = None
    from_step: int | None = None
    to_step: int | None = None
    from_time: datetime | None = None
    to_time: datetime | None = None
    #: `hide` only: the run's step spans in the step range too (a rewind).
    step_spans: bool = False
    #: `hide` only: these files instead of points.
    file_ids: list[UUID] = Field(default_factory=list)


class HideArgs(BaseModel):
    """`hide` takes no arguments: its target says what to hide."""


class ShiftStepArgs(BaseModel):
    """Add `by` to every step."""

    by: int


class ShiftTimeArgs(BaseModel):
    """Add `seconds` to every wall clock."""

    seconds: float


class ScaleArgs(BaseModel):
    """value -> multiply * value + add."""

    multiply: float = 1.0
    add: float = 0.0


class RenameArgs(BaseModel):
    """The target's one key becomes `to_key`."""

    to_key: str


class MoveSeriesArgs(BaseModel):
    """Bring the target's series from `from_run` into this run, optionally shifted. Needs write on both runs."""

    from_run: UUID
    shift_steps: int = 0
    shift_seconds: float = 0.0


class SetConfigArgs(BaseModel):
    """Set these config values; the old ones are kept on the edit (`config_before`)."""

    values: dict


class RevertArgs(BaseModel):
    """Undo an earlier edit of this run."""

    edit_id: UUID


#: Each op's arguments model, picked once here (the server validates `args` with it, the SDK builds it).
EDIT_OP_ARGS: dict[EditOp, type[BaseModel]] = {
    EditOp.HIDE: HideArgs,
    EditOp.SHIFT_STEP: ShiftStepArgs,
    EditOp.SHIFT_TIME: ShiftTimeArgs,
    EditOp.SCALE: ScaleArgs,
    EditOp.RENAME: RenameArgs,
    EditOp.MOVE_SERIES: MoveSeriesArgs,
    EditOp.SET_CONFIG: SetConfigArgs,
    EditOp.REVERT: RevertArgs,
}


class EditCounts(BaseModel):
    """What an edit changed, for its receipt and History."""

    #: Points taken out of every read (now on the shelf).
    points: int = 0
    #: Transformed copies written back.
    written: int = 0
    spans: int = 0
    files: int = 0
    findings: int = 0
    #: Identities other points already hold: refused unless the edit replaces them.
    collisions: int = 0
    config_keys: int = 0


class RunEdit(Record):
    """An edit as every surface reads it: what, to which data, who, why, and where it is."""

    id: UUID
    customer_id: str
    run_id: UUID
    #: 1, 2, 3, ... per run: "edit #3".
    seq: int
    op: EditOp
    target: EditTarget
    #: The op's arguments (`EDIT_OP_ARGS[op]`), as sent.
    args: dict = Field(default_factory=dict)
    reason: str
    actor_kind: EditActorKind
    actor: str
    session_id: UUID | None = None
    state: EditState
    phase: EditPhase
    #: On a revert: the edit it undoes. On an undone edit: the revert that undid it.
    revert_of: UUID | None = None
    reverted_by: UUID | None = None
    counts: EditCounts
    #: `set_config`: the values the changed keys held before.
    config_before: dict | None = None
    error: str | None = None
    created_at: datetime
    applied_at: datetime | None = None
