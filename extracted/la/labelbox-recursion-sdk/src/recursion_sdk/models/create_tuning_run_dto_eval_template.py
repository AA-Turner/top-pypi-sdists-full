from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_tuning_run_dto_eval_template_problems_item import CreateTuningRunDtoEvalTemplateProblemsItem





T = TypeVar("T", bound="CreateTuningRunDtoEvalTemplate")



@_attrs_define
class CreateTuningRunDtoEvalTemplate:
    """ Template for the per-checkpoint evaluations a tuning_run spawns.

        Attributes:
            environment_id (UUID): Primary environment for the spawned evaluations.
            solver_run_config_version_id (UUID): Locked, agent-harness solver run-config version. Must accept a checkpoint-
                eval placeholder model (see the checkpointContext pass-through in this file).
            grader_run_config_version_id (UUID): Locked grader run-config version pinned on every spawned evaluation -- held
                constant across every checkpoint so score-over-checkpoints shares one reward scale.
            problems (list[CreateTuningRunDtoEvalTemplateProblemsItem]): Problems included in every spawned per-checkpoint
                evaluation (one or more).
            attempts_per_problem (int | Unset): Attempts each spawned checkpoint-eval makes per problem (pass@k), 1-25.
                Absent = 1, applied at dispatch.
     """

    environment_id: UUID
    solver_run_config_version_id: UUID
    grader_run_config_version_id: UUID
    problems: list[CreateTuningRunDtoEvalTemplateProblemsItem]
    attempts_per_problem: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_tuning_run_dto_eval_template_problems_item import CreateTuningRunDtoEvalTemplateProblemsItem # noqa: PLC0415
        environment_id = str(self.environment_id)

        solver_run_config_version_id = str(self.solver_run_config_version_id)

        grader_run_config_version_id = str(self.grader_run_config_version_id)

        problems = []
        for problems_item_data in self.problems:
            problems_item = problems_item_data.to_dict()
            problems.append(problems_item)



        attempts_per_problem = self.attempts_per_problem


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "environmentId": environment_id,
            "solverRunConfigVersionId": solver_run_config_version_id,
            "graderRunConfigVersionId": grader_run_config_version_id,
            "problems": problems,
        })
        if attempts_per_problem is not UNSET:
            field_dict["attemptsPerProblem"] = attempts_per_problem

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_tuning_run_dto_eval_template_problems_item import CreateTuningRunDtoEvalTemplateProblemsItem # noqa: PLC0415
        d = dict(src_dict)
        environment_id = UUID(d.pop("environmentId"))




        solver_run_config_version_id = UUID(d.pop("solverRunConfigVersionId"))




        grader_run_config_version_id = UUID(d.pop("graderRunConfigVersionId"))




        problems = []
        _problems = d.pop("problems")
        for problems_item_data in (_problems):
            problems_item = CreateTuningRunDtoEvalTemplateProblemsItem.from_dict(problems_item_data)



            problems.append(problems_item)


        attempts_per_problem = d.pop("attemptsPerProblem", UNSET)

        create_tuning_run_dto_eval_template = cls(
            environment_id=environment_id,
            solver_run_config_version_id=solver_run_config_version_id,
            grader_run_config_version_id=grader_run_config_version_id,
            problems=problems,
            attempts_per_problem=attempts_per_problem,
        )

        return create_tuning_run_dto_eval_template

