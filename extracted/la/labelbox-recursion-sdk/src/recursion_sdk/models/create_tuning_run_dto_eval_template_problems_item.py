from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="CreateTuningRunDtoEvalTemplateProblemsItem")



@_attrs_define
class CreateTuningRunDtoEvalTemplateProblemsItem:
    """ One selected locked problem-version, with its problem and owning environment.

        Attributes:
            problem_id (UUID): Stable problem identifier (UUID).
            problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this
                points at one specific version.
            environment_id (UUID): Stable environment identifier (UUID).
     """

    problem_id: UUID
    problem_version_id: UUID
    environment_id: UUID





    def to_dict(self) -> dict[str, Any]:
        problem_id = str(self.problem_id)

        problem_version_id = str(self.problem_version_id)

        environment_id = str(self.environment_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemId": problem_id,
            "problemVersionId": problem_version_id,
            "environmentId": environment_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        problem_id = UUID(d.pop("problemId"))




        problem_version_id = UUID(d.pop("problemVersionId"))




        environment_id = UUID(d.pop("environmentId"))




        create_tuning_run_dto_eval_template_problems_item = cls(
            problem_id=problem_id,
            problem_version_id=problem_version_id,
            environment_id=environment_id,
        )

        return create_tuning_run_dto_eval_template_problems_item

