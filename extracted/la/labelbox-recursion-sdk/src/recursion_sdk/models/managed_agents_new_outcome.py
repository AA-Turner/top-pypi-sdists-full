from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsNewOutcome")



@_attrs_define
class ManagedAgentsNewOutcome:
    """ A session's definition of done, graded against a rubric. The description is the objective the grader measures; a
    message sent alongside it is context the grader never sees.

        Example:
            {'description': 'example', 'grader_model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'max_iterations': 1,
                'rubric': 'example', 'rubric_file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            description (str): The objective the grader measures. Independent of any message sent alongside it, which is
                context the grader never sees.
            rubric (str): Inline grading rubric. Exactly one of rubric and rubric_file_id is set.
            grader_model_ref_id (str | Unset): Model reference the grader runs on. Omit to use the platform's grading model.
            max_iterations (int | Unset): Maximum grading passes before the outcome ends as max_iterations_reached. Omit or
                send 0 for unbounded: the loop runs until the grader is satisfied.
            rubric_file_id (str | Unset): File whose text is the rubric, resolved when the outcome is defined. Exactly one
                of rubric and rubric_file_id is set.
     """

    description: str
    rubric: str
    grader_model_ref_id: str | Unset = UNSET
    max_iterations: int | Unset = UNSET
    rubric_file_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        rubric = self.rubric

        grader_model_ref_id = self.grader_model_ref_id

        max_iterations = self.max_iterations

        rubric_file_id = self.rubric_file_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "description": description,
            "rubric": rubric,
        })
        if grader_model_ref_id is not UNSET:
            field_dict["grader_model_ref_id"] = grader_model_ref_id
        if max_iterations is not UNSET:
            field_dict["max_iterations"] = max_iterations
        if rubric_file_id is not UNSET:
            field_dict["rubric_file_id"] = rubric_file_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        rubric = d.pop("rubric")

        grader_model_ref_id = d.pop("grader_model_ref_id", UNSET)

        max_iterations = d.pop("max_iterations", UNSET)

        rubric_file_id = d.pop("rubric_file_id", UNSET)

        managed_agents_new_outcome = cls(
            description=description,
            rubric=rubric,
            grader_model_ref_id=grader_model_ref_id,
            max_iterations=max_iterations,
            rubric_file_id=rubric_file_id,
        )


        managed_agents_new_outcome.additional_properties = d
        return managed_agents_new_outcome

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
