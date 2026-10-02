from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.evaluation_detail_response_dto_solvers_item_metadata_schema_version import EvaluationDetailResponseDtoSolversItemMetadataSchemaVersion
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.evaluation_detail_response_dto_solvers_item_metadata_tuning_run_checkpoint import EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint





T = TypeVar("T", bound="EvaluationDetailResponseDtoSolversItemMetadata")



@_attrs_define
class EvaluationDetailResponseDtoSolversItemMetadata:
    """ Orchestration metadata persisted on this solver (per-solver concurrency cap).

        Attributes:
            schema_version (EvaluationDetailResponseDtoSolversItemMetadataSchemaVersion): Version discriminant of the
                metadata shape. Always 1 today.
            concurrency (int | Unset): Maximum solver runs this solver keeps alive on the agent service at once (requests
                are capped at 2000). Omitted means the platform default applies.
            tuning_run_checkpoint (EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint | Unset): Durable copy
                of this checkpoint-eval solver's (step, checkpointRef), written in the SAME transaction as the
                evaluation/solver/jobs_v2 rows. This is the crash-safe dedup key tuning_run polls against — createV2 commits
                atomically, so once this field is set on a solver row, that (tuning_run, step) pair is guaranteed already
                spawned on every subsequent poll, regardless of what tuning_run's own in-memory bookkeeping lost to a crash.
     """

    schema_version: EvaluationDetailResponseDtoSolversItemMetadataSchemaVersion
    concurrency: int | Unset = UNSET
    tuning_run_checkpoint: EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_detail_response_dto_solvers_item_metadata_tuning_run_checkpoint import EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint # noqa: PLC0415
        schema_version = self.schema_version.value

        concurrency = self.concurrency

        tuning_run_checkpoint: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tuning_run_checkpoint, Unset):
            tuning_run_checkpoint = self.tuning_run_checkpoint.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "schemaVersion": schema_version,
        })
        if concurrency is not UNSET:
            field_dict["concurrency"] = concurrency
        if tuning_run_checkpoint is not UNSET:
            field_dict["tuningRunCheckpoint"] = tuning_run_checkpoint

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_detail_response_dto_solvers_item_metadata_tuning_run_checkpoint import EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint # noqa: PLC0415
        d = dict(src_dict)
        schema_version = EvaluationDetailResponseDtoSolversItemMetadataSchemaVersion(d.pop("schemaVersion"))




        concurrency = d.pop("concurrency", UNSET)

        _tuning_run_checkpoint = d.pop("tuningRunCheckpoint", UNSET)
        tuning_run_checkpoint: EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint | Unset
        if isinstance(_tuning_run_checkpoint,  Unset):
            tuning_run_checkpoint = UNSET
        else:
            tuning_run_checkpoint = EvaluationDetailResponseDtoSolversItemMetadataTuningRunCheckpoint.from_dict(_tuning_run_checkpoint)




        evaluation_detail_response_dto_solvers_item_metadata = cls(
            schema_version=schema_version,
            concurrency=concurrency,
            tuning_run_checkpoint=tuning_run_checkpoint,
        )

        return evaluation_detail_response_dto_solvers_item_metadata

