from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_tuning_run_dto_training_template_problems_item import CreateTuningRunDtoTrainingTemplateProblemsItem





T = TypeVar("T", bound="CreateTuningRunDtoTrainingTemplate")



@_attrs_define
class CreateTuningRunDtoTrainingTemplate:
    """ The training problem set a tuning_run materializes into the trainer dataset_ref.

        Attributes:
            environment_id (UUID): Environment the training problem set is drawn from.
            problems (list[CreateTuningRunDtoTrainingTemplateProblemsItem]): Locked problem-versions materialized into the
                trainer dataset (one or more).
     """

    environment_id: UUID
    problems: list[CreateTuningRunDtoTrainingTemplateProblemsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_tuning_run_dto_training_template_problems_item import CreateTuningRunDtoTrainingTemplateProblemsItem # noqa: PLC0415
        environment_id = str(self.environment_id)

        problems = []
        for problems_item_data in self.problems:
            problems_item = problems_item_data.to_dict()
            problems.append(problems_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "environmentId": environment_id,
            "problems": problems,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_tuning_run_dto_training_template_problems_item import CreateTuningRunDtoTrainingTemplateProblemsItem # noqa: PLC0415
        d = dict(src_dict)
        environment_id = UUID(d.pop("environmentId"))




        problems = []
        _problems = d.pop("problems")
        for problems_item_data in (_problems):
            problems_item = CreateTuningRunDtoTrainingTemplateProblemsItem.from_dict(problems_item_data)



            problems.append(problems_item)


        create_tuning_run_dto_training_template = cls(
            environment_id=environment_id,
            problems=problems,
        )

        return create_tuning_run_dto_training_template

