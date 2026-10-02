from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.problem_run_execution_evidence_dto_graders_item import ProblemRunExecutionEvidenceDtoGradersItem
  from ..models.problem_run_execution_evidence_dto_handoff import ProblemRunExecutionEvidenceDtoHandoff
  from ..models.problem_run_execution_evidence_dto_solver import ProblemRunExecutionEvidenceDtoSolver





T = TypeVar("T", bound="ProblemRunExecutionEvidenceDto")



@_attrs_define
class ProblemRunExecutionEvidenceDto:
    """ Read-only execution evidence for a solver run and its grader sub-runs.

        Attributes:
            problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one problem version.
            solver (ProblemRunExecutionEvidenceDtoSolver): Solver execution identity and manifest evidence.
            graders (list[ProblemRunExecutionEvidenceDtoGradersItem]): Persisted execution identity and evidence for each
                grader sub-run.
            handoff (ProblemRunExecutionEvidenceDtoHandoff): Evidence about the solver-to-grader state handoff. It does not
                claim live restore verification.
     """

    problem_run_id: UUID
    solver: ProblemRunExecutionEvidenceDtoSolver
    graders: list[ProblemRunExecutionEvidenceDtoGradersItem]
    handoff: ProblemRunExecutionEvidenceDtoHandoff





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_run_execution_evidence_dto_graders_item import ProblemRunExecutionEvidenceDtoGradersItem # noqa: PLC0415
        from ..models.problem_run_execution_evidence_dto_handoff import ProblemRunExecutionEvidenceDtoHandoff # noqa: PLC0415
        from ..models.problem_run_execution_evidence_dto_solver import ProblemRunExecutionEvidenceDtoSolver # noqa: PLC0415
        problem_run_id = str(self.problem_run_id)

        solver = self.solver.to_dict()

        graders = []
        for graders_item_data in self.graders:
            graders_item = graders_item_data.to_dict()
            graders.append(graders_item)



        handoff = self.handoff.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemRunId": problem_run_id,
            "solver": solver,
            "graders": graders,
            "handoff": handoff,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_run_execution_evidence_dto_graders_item import ProblemRunExecutionEvidenceDtoGradersItem # noqa: PLC0415
        from ..models.problem_run_execution_evidence_dto_handoff import ProblemRunExecutionEvidenceDtoHandoff # noqa: PLC0415
        from ..models.problem_run_execution_evidence_dto_solver import ProblemRunExecutionEvidenceDtoSolver # noqa: PLC0415
        d = dict(src_dict)
        problem_run_id = UUID(d.pop("problemRunId"))




        solver = ProblemRunExecutionEvidenceDtoSolver.from_dict(d.pop("solver"))




        graders = []
        _graders = d.pop("graders")
        for graders_item_data in (_graders):
            graders_item = ProblemRunExecutionEvidenceDtoGradersItem.from_dict(graders_item_data)



            graders.append(graders_item)


        handoff = ProblemRunExecutionEvidenceDtoHandoff.from_dict(d.pop("handoff"))




        problem_run_execution_evidence_dto = cls(
            problem_run_id=problem_run_id,
            solver=solver,
            graders=graders,
            handoff=handoff,
        )

        return problem_run_execution_evidence_dto

