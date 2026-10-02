from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="CreateEvaluationBodyDtoProblemsItem")



@_attrs_define
class CreateEvaluationBodyDtoProblemsItem:
    """ Reference to one problem (pinned to a specific version) to include in a new evaluation.

        Attributes:
            problem_id (UUID): Stable problem identifier (UUID).
            problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this
                points at one specific version.
            environment_id (UUID): Stable environment identifier (UUID).
     """

    problem_id: UUID
    problem_version_id: UUID
    environment_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        problem_id = str(self.problem_id)

        problem_version_id = str(self.problem_version_id)

        environment_id = str(self.environment_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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




        create_evaluation_body_dto_problems_item = cls(
            problem_id=problem_id,
            problem_version_id=problem_version_id,
            environment_id=environment_id,
        )


        create_evaluation_body_dto_problems_item.additional_properties = d
        return create_evaluation_body_dto_problems_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
