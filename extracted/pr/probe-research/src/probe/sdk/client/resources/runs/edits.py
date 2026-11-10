"""EditsMixin (Client's methods) and EditsResource (`client.edits`): edit a run's recorded data, never destructively
(twin: app/runs/edits). Build an edit by op, never from a string:
`client.edits.create(run, Edit.hide(keys="loss", from_step=2000), reason="diverged after the LR spike")`."""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .... import errors
from .....generated.records import (
    EditCounts,
    EditOp,
    EditState,
    EditTarget,
    MoveSeriesArgs,
    RenameArgs,
    RunEdit,
    ScaleArgs,
    SetConfigArgs,
    ShiftStepArgs,
    ShiftTimeArgs,
)
from ...resource import Resource

#: States an edit is still moving in (`applying`, `rolling_back`): `wait` polls past them.
_IN_FLIGHT = frozenset({EditState.APPLYING, EditState.ROLLING_BACK})


def _make_target(keys: str | list[str] | None = None, **fields: Any) -> EditTarget:
    """A target from keys (one, or several; globs allowed) and the range and coordinate filters."""
    names = [keys] if isinstance(keys, str) else list(keys or [])
    return EditTarget(keys=names, **{name: value for name, value in fields.items() if value is not None})


class Edit:
    """One edit: its op, which data it touches (`target`) and its arguments. Made by `Edit.<op>(...)`."""

    __slots__ = ("args", "op", "target")

    def __init__(self, op: EditOp, target: EditTarget | None = None, args: BaseModel | None = None) -> None:
        if not isinstance(op, EditOp):
            raise TypeError(f"an edit's op is an EditOp (Edit.hide(...), Edit.scale(...)), not {op!r}")
        self.op = op
        self.target = target or EditTarget()
        self.args = args

    def to_body(self) -> dict[str, Any]:
        """The request body's op, target and args."""
        return {
            "op": self.op.value,
            "target": self.target.model_dump(mode="json", exclude_defaults=True),
            "args": self.args.model_dump(mode="json") if self.args is not None else {},
        }

    def __repr__(self) -> str:
        return f"Edit({self.op.value}, target={self.to_body()['target']}, args={self.to_body()['args']})"

    @classmethod
    def hide(
        cls,
        keys: str | list[str] | None = None,
        *,
        kinds: list[str] | None = None,
        dimensions: dict | None = None,
        from_step: int | None = None,
        to_step: int | None = None,
        from_time: datetime | None = None,
        to_time: datetime | None = None,
    ) -> Edit:
        """Take points out of every read (Undo puts them back). Steps are [from_step, to_step)."""
        target = _make_target(
            keys, kinds=kinds, dimensions=dimensions, from_step=from_step, to_step=to_step,
            from_time=from_time, to_time=to_time,
        )  # fmt: skip
        return cls(EditOp.HIDE, target)

    @classmethod
    def hide_files(cls, file_ids: list[str]) -> Edit:
        """Hide files of the run (a soft delete Undo restores)."""
        return cls(EditOp.HIDE, EditTarget(file_ids=list(file_ids)))

    @classmethod
    def shift_step(cls, by: int, keys: str | list[str] | None = None, **target: Any) -> Edit:
        """Add `by` to every selected point's step (an eval logged on its own counter)."""
        return cls(EditOp.SHIFT_STEP, _make_target(keys, **target), ShiftStepArgs(by=by))

    @classmethod
    def shift_time(cls, seconds: float, keys: str | list[str] | None = None, **target: Any) -> Edit:
        """Add `seconds` to every selected point's wall clock (a clock from another machine)."""
        return cls(EditOp.SHIFT_TIME, _make_target(keys, **target), ShiftTimeArgs(seconds=seconds))

    @classmethod
    def scale(
        cls, multiply: float = 1.0, add: float = 0.0, keys: str | list[str] | None = None, **target: Any
    ) -> Edit:
        """value -> multiply * value + add (bad units)."""
        return cls(EditOp.SCALE, _make_target(keys, **target), ScaleArgs(multiply=multiply, add=add))

    @classmethod
    def rename(cls, key: str, to_key: str, **target: Any) -> Edit:
        """The series `key` becomes `to_key`."""
        return cls(EditOp.RENAME, _make_target(key, **target), RenameArgs(to_key=to_key))

    @classmethod
    def move_series(
        cls,
        from_run: str,
        keys: str | list[str] | None = None,
        *,
        shift_steps: int = 0,
        shift_seconds: float = 0.0,
        **target: Any,
    ) -> Edit:
        """Bring series from another run (its id) into this one, optionally shifted. Needs write on both runs."""
        args = MoveSeriesArgs(from_run=from_run, shift_steps=shift_steps, shift_seconds=shift_seconds)
        return cls(EditOp.MOVE_SERIES, _make_target(keys, **target), args)

    @classmethod
    def set_config(cls, values: dict[str, Any]) -> Edit:
        """Set config values; the old ones stay on the edit. A run still running takes `send config` instead."""
        return cls(EditOp.SET_CONFIG, None, SetConfigArgs(values=dict(values)))


class EditsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def create_edit(
        self, run_id: str, edit: Edit, *, reason: str, should_replace: bool = False, is_dry_run: bool = False
    ) -> dict:
        """Edit a run's data (`POST /v1/runs/{run}/edits`). A point edit answers `applying` and applies in the
        background; config and file edits answer `applied`. `is_dry_run` answers `{op, counts}` and changes
        nothing. `should_replace` hides the points already where the edit's points land, instead of a refusal."""
        if not isinstance(edit, Edit):
            raise TypeError("pass an Edit: Edit.hide(...), Edit.scale(...), Edit.set_config({...})")
        if not reason or not reason.strip():
            raise errors.ValidationError("an edit needs a reason: it is what History shows")
        body = {**edit.to_body(), "reason": reason, "replace": should_replace, "dry_run": is_dry_run}
        return self.transport.post(f"/v1/runs/{run_id}/edits", body)

    def list_edits(self, run_id: str) -> list[dict]:
        """A run's edits, newest first (History)."""
        return self.transport.get(f"/v1/runs/{run_id}/edits").get("edits", [])

    def get_edit(self, edit_id: str) -> dict:
        return self.transport.get(f"/v1/edits/{edit_id}")

    def revert_edit(self, edit_id: str, *, reason: str) -> dict:
        """Undo an edit. Refused while a later edit changed the same data, or once the run wrote over it."""
        if not reason or not reason.strip():
            raise errors.ValidationError("a revert needs a reason")
        return self.transport.post(f"/v1/edits/{edit_id}/revert", {"reason": reason})

    def wait_for_edit(self, edit_id: str, *, timeout: float = 600.0, interval: float = 1.0) -> dict:
        """Poll an edit until it is applied or failed; raises TimeoutError past `timeout` seconds."""
        deadline = time.monotonic() + timeout
        while True:
            edit = self.get_edit(edit_id)
            if EditState(edit["state"]) not in _IN_FLIGHT:
                return edit
            if time.monotonic() >= deadline:
                raise TimeoutError(f"edit {edit_id} is still {edit['state']} after {timeout:.0f} s")
            time.sleep(interval)


class EditsResource(Resource):
    """`client.edits`: create, preview, list, read, wait for and revert run edits, typed."""

    def preview(self, run: str, edit: Edit, *, reason: str, should_replace: bool = False) -> EditCounts:
        """What `edit` would change (points, collisions, findings, ...); changes nothing."""
        answer = self._client.create_edit(run, edit, reason=reason, should_replace=should_replace, is_dry_run=True)
        return EditCounts.model_validate(answer["counts"])

    def create(
        self, run: str, edit: Edit, *, reason: str, should_replace: bool = False, should_wait: bool = False
    ) -> RunEdit:
        """Make the edit; with `should_wait`, return once it is applied (or failed)."""
        made = self._to_model(RunEdit, self._client.create_edit(run, edit, reason=reason, should_replace=should_replace))
        return self.wait(str(made.id)) if should_wait and made.state in _IN_FLIGHT else made

    def list(self, run: str) -> list[RunEdit]:
        return self._to_models(RunEdit, self._client.list_edits(run))

    def get(self, edit_id: str) -> RunEdit:
        return self._to_model(RunEdit, self._client.get_edit(edit_id))

    def revert(self, edit_id: str, *, reason: str, should_wait: bool = False) -> RunEdit:
        made = self._to_model(RunEdit, self._client.revert_edit(edit_id, reason=reason))
        return self.wait(str(made.id)) if should_wait and made.state in _IN_FLIGHT else made

    def wait(self, edit_id: str, *, timeout: float = 600.0) -> RunEdit:
        return self._to_model(RunEdit, self._client.wait_for_edit(edit_id, timeout=timeout))
