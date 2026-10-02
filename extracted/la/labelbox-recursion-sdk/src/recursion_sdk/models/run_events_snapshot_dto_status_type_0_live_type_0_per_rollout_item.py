from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_status_type_0_live_type_0_per_rollout_item_phase_type_0 import RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItemPhaseType0
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem")



@_attrs_define
class RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem:
    """ One entry in the live section's bounded per-rollout progress sample.

        Attributes:
            run_id (str): Opaque agent-service run id for this in-flight rollout.
            seq (int | None | Unset): Sequence index of the rollout within its step.
            turn (int | None | Unset): Current agent turn number within the rollout.
            tokens (int | None | Unset): Tokens generated so far in this rollout.
            last_progress_age_s (float | None | Unset): Seconds since this rollout last made observable progress.
            phase (None | RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItemPhaseType0 | Unset): This rollout's current
                in-flight phase: 'generating' the trajectory, or 'grading' the completed trajectory. Absent when the trainer
                does not report a phase (treated as 'generating').
     """

    run_id: str
    seq: int | None | Unset = UNSET
    turn: int | None | Unset = UNSET
    tokens: int | None | Unset = UNSET
    last_progress_age_s: float | None | Unset = UNSET
    phase: None | RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItemPhaseType0 | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        seq: int | None | Unset
        if isinstance(self.seq, Unset):
            seq = UNSET
        else:
            seq = self.seq

        turn: int | None | Unset
        if isinstance(self.turn, Unset):
            turn = UNSET
        else:
            turn = self.turn

        tokens: int | None | Unset
        if isinstance(self.tokens, Unset):
            tokens = UNSET
        else:
            tokens = self.tokens

        last_progress_age_s: float | None | Unset
        if isinstance(self.last_progress_age_s, Unset):
            last_progress_age_s = UNSET
        else:
            last_progress_age_s = self.last_progress_age_s

        phase: None | str | Unset
        if isinstance(self.phase, Unset):
            phase = UNSET
        elif isinstance(self.phase, RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItemPhaseType0):
            phase = self.phase.value
        else:
            phase = self.phase


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "run_id": run_id,
        })
        if seq is not UNSET:
            field_dict["seq"] = seq
        if turn is not UNSET:
            field_dict["turn"] = turn
        if tokens is not UNSET:
            field_dict["tokens"] = tokens
        if last_progress_age_s is not UNSET:
            field_dict["last_progress_age_s"] = last_progress_age_s
        if phase is not UNSET:
            field_dict["phase"] = phase

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_id = d.pop("run_id")

        def _parse_seq(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        seq = _parse_seq(d.pop("seq", UNSET))


        def _parse_turn(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        turn = _parse_turn(d.pop("turn", UNSET))


        def _parse_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        tokens = _parse_tokens(d.pop("tokens", UNSET))


        def _parse_last_progress_age_s(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        last_progress_age_s = _parse_last_progress_age_s(d.pop("last_progress_age_s", UNSET))


        def _parse_phase(data: object) -> None | RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItemPhaseType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                phase_type_0 = RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItemPhaseType0(data)



                return phase_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItemPhaseType0 | Unset, data)

        phase = _parse_phase(d.pop("phase", UNSET))


        run_events_snapshot_dto_status_type_0_live_type_0_per_rollout_item = cls(
            run_id=run_id,
            seq=seq,
            turn=turn,
            tokens=tokens,
            last_progress_age_s=last_progress_age_s,
            phase=phase,
        )

        return run_events_snapshot_dto_status_type_0_live_type_0_per_rollout_item

