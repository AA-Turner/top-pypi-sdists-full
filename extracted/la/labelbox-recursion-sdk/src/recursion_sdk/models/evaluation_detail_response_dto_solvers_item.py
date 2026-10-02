from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.evaluation_detail_response_dto_solvers_item_job_status_type_0 import EvaluationDetailResponseDtoSolversItemJobStatusType0
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.evaluation_detail_response_dto_solvers_item_metadata import EvaluationDetailResponseDtoSolversItemMetadata





T = TypeVar("T", bound="EvaluationDetailResponseDtoSolversItem")



@_attrs_define
class EvaluationDetailResponseDtoSolversItem:
    """ One solver participating in an evaluation, with its run-config bindings and job status.

        Attributes:
            id (UUID): Stable evaluation-solver identifier (UUID). Refers to one solver participating in an evaluation.
            evaluation_id (UUID): Stable evaluation identifier (UUID). An evaluation is a multi-problem comparison run.
            display_name (str): Human-readable label distinguishing this solver in evaluation results.
            run_config_version_id (None | UUID): Locked run-config version (kind "solver") that governs this solver's
                invocation. Null only on legacy solvers created before run-config-native evaluations.
            solver_label (str): Display label for results, derived from the bound run-config name. "(legacy)" for pre-
                cutover solvers with no bound run-config.
            job_status (EvaluationDetailResponseDtoSolversItemJobStatusType0 | None): Current aggregate status of the jobs
                executing this solver. Null before the evaluation has been started, and on pre-cutover solvers that predate the
                current execution engine.
            sort_order (int): Position of this solver in evaluation results, left-to-right. Example: 0.
            metadata (EvaluationDetailResponseDtoSolversItemMetadata): Orchestration metadata persisted on this solver (per-
                solver concurrency cap).
     """

    id: UUID
    evaluation_id: UUID
    display_name: str
    run_config_version_id: None | UUID
    solver_label: str
    job_status: EvaluationDetailResponseDtoSolversItemJobStatusType0 | None
    sort_order: int
    metadata: EvaluationDetailResponseDtoSolversItemMetadata





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_detail_response_dto_solvers_item_metadata import EvaluationDetailResponseDtoSolversItemMetadata # noqa: PLC0415
        id = str(self.id)

        evaluation_id = str(self.evaluation_id)

        display_name = self.display_name

        run_config_version_id: None | str
        if isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id

        solver_label = self.solver_label

        job_status: None | str
        if isinstance(self.job_status, EvaluationDetailResponseDtoSolversItemJobStatusType0):
            job_status = self.job_status.value
        else:
            job_status = self.job_status

        sort_order = self.sort_order

        metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "evaluationId": evaluation_id,
            "displayName": display_name,
            "runConfigVersionId": run_config_version_id,
            "solverLabel": solver_label,
            "jobStatus": job_status,
            "sortOrder": sort_order,
            "metadata": metadata,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_detail_response_dto_solvers_item_metadata import EvaluationDetailResponseDtoSolversItemMetadata # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        evaluation_id = UUID(d.pop("evaluationId"))




        display_name = d.pop("displayName")

        def _parse_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_config_version_id_type_0 = UUID(data)



                return run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        run_config_version_id = _parse_run_config_version_id(d.pop("runConfigVersionId"))


        solver_label = d.pop("solverLabel")

        def _parse_job_status(data: object) -> EvaluationDetailResponseDtoSolversItemJobStatusType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_status_type_0 = EvaluationDetailResponseDtoSolversItemJobStatusType0(data)



                return job_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EvaluationDetailResponseDtoSolversItemJobStatusType0 | None, data)

        job_status = _parse_job_status(d.pop("jobStatus"))


        sort_order = d.pop("sortOrder")

        metadata = EvaluationDetailResponseDtoSolversItemMetadata.from_dict(d.pop("metadata"))




        evaluation_detail_response_dto_solvers_item = cls(
            id=id,
            evaluation_id=evaluation_id,
            display_name=display_name,
            run_config_version_id=run_config_version_id,
            solver_label=solver_label,
            job_status=job_status,
            sort_order=sort_order,
            metadata=metadata,
        )

        return evaluation_detail_response_dto_solvers_item

