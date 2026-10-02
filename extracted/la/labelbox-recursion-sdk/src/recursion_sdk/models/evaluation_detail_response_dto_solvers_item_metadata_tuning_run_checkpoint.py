from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint")



@_attrs_define
class EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint:
    """ Durable copy of this checkpoint-eval solver's (step, checkpointRef), written in the SAME transaction as the
    evaluation/solver/jobs_v2 rows. This is the crash-safe dedup key tuning_run polls against — createV2 commits
    atomically, so once this field is set on a solver row, that (tuning_run, step) pair is guaranteed already spawned on
    every subsequent poll, regardless of what tuning_run's own in-memory bookkeeping lost to a crash.

        Attributes:
            step (int): Trainer checkpoint step this evaluation was spawned for.
            checkpoint_ref (None | str): Opaque training-checkpoint reference loaded by this solver. Null when the
                checkpoint announcement did not provide a loadable artifact reference.
     """

    step: int
    checkpoint_ref: None | str





    def to_dict(self) -> dict[str, Any]:
        step = self.step

        checkpoint_ref: None | str
        checkpoint_ref = self.checkpoint_ref


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "step": step,
            "checkpointRef": checkpoint_ref,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        step = d.pop("step")

        def _parse_checkpoint_ref(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        checkpoint_ref = _parse_checkpoint_ref(d.pop("checkpointRef"))


        evaluation_detail_response_dto_solvers_item_metadata_tuning_run_checkpoint = cls(
            step=step,
            checkpoint_ref=checkpoint_ref,
        )

        return evaluation_detail_response_dto_solvers_item_metadata_tuning_run_checkpoint

