from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_run_execution_evidence_dto_solver_status import ProblemRunExecutionEvidenceDtoSolverStatus
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.problem_run_execution_evidence_dto_solver_manifest import ProblemRunExecutionEvidenceDtoSolverManifest





T = TypeVar("T", bound="ProblemRunExecutionEvidenceDtoSolver")



@_attrs_define
class ProblemRunExecutionEvidenceDtoSolver:
    """ Solver execution identity and manifest evidence.

        Attributes:
            status (ProblemRunExecutionEvidenceDtoSolverStatus): Lifecycle status of a problem run from queueing through
                grading to a terminal state.
            external_run_id (None | str): Agent-service run ID for the solver, when submitted.
            run_config_version_id (None | UUID): Locked run-config version that governed the solver run. Null when no run-
                config version was recorded.
            manifest (ProblemRunExecutionEvidenceDtoSolverManifest): Sanitized evidence extracted from the solver manifest.
     """

    status: ProblemRunExecutionEvidenceDtoSolverStatus
    external_run_id: None | str
    run_config_version_id: None | UUID
    manifest: ProblemRunExecutionEvidenceDtoSolverManifest





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_run_execution_evidence_dto_solver_manifest import ProblemRunExecutionEvidenceDtoSolverManifest # noqa: PLC0415
        status = self.status.value

        external_run_id: None | str
        external_run_id = self.external_run_id

        run_config_version_id: None | str
        if isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id

        manifest = self.manifest.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
            "externalRunId": external_run_id,
            "runConfigVersionId": run_config_version_id,
            "manifest": manifest,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_run_execution_evidence_dto_solver_manifest import ProblemRunExecutionEvidenceDtoSolverManifest # noqa: PLC0415
        d = dict(src_dict)
        status = ProblemRunExecutionEvidenceDtoSolverStatus(d.pop("status"))




        def _parse_external_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_run_id = _parse_external_run_id(d.pop("externalRunId"))


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


        manifest = ProblemRunExecutionEvidenceDtoSolverManifest.from_dict(d.pop("manifest"))




        problem_run_execution_evidence_dto_solver = cls(
            status=status,
            external_run_id=external_run_id,
            run_config_version_id=run_config_version_id,
            manifest=manifest,
        )

        return problem_run_execution_evidence_dto_solver

