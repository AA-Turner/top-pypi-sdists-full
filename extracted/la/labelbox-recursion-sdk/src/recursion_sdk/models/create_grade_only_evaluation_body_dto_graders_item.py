from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="CreateGradeOnlyEvaluationBodyDtoGradersItem")



@_attrs_define
class CreateGradeOnlyEvaluationBodyDtoGradersItem:
    """ One grader config to compare in a grade-only evaluation.

        Attributes:
            display_name (str): Human-readable label distinguishing this grader column in the comparison matrix.
            run_config_version_id (UUID): Locked run-config version (kind "grader") to run against every picked trajectory.
     """

    display_name: str
    run_config_version_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        run_config_version_id = str(self.run_config_version_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "displayName": display_name,
            "runConfigVersionId": run_config_version_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        display_name = d.pop("displayName")

        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        create_grade_only_evaluation_body_dto_graders_item = cls(
            display_name=display_name,
            run_config_version_id=run_config_version_id,
        )


        create_grade_only_evaluation_body_dto_graders_item.additional_properties = d
        return create_grade_only_evaluation_body_dto_graders_item

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
