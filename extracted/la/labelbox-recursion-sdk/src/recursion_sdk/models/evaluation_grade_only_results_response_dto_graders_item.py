from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="EvaluationGradeOnlyResultsResponseDtoGradersItem")



@_attrs_define
class EvaluationGradeOnlyResultsResponseDtoGradersItem:
    """ One ordered grader column in a grade-only comparison matrix.

        Attributes:
            id (UUID): Stable identifier referenced by grade-only matrix cells.
            display_name (str): Human-readable label distinguishing this grader column in the comparison matrix.
            run_config_version_id (UUID): Locked grader run-config version used for this matrix column.
            sort_order (int): Position of this grader in the comparison matrix, left-to-right. Example: 0.
     """

    id: UUID
    display_name: str
    run_config_version_id: UUID
    sort_order: int





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        display_name = self.display_name

        run_config_version_id = str(self.run_config_version_id)

        sort_order = self.sort_order


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "displayName": display_name,
            "runConfigVersionId": run_config_version_id,
            "sortOrder": sort_order,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        display_name = d.pop("displayName")

        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        sort_order = d.pop("sortOrder")

        evaluation_grade_only_results_response_dto_graders_item = cls(
            id=id,
            display_name=display_name,
            run_config_version_id=run_config_version_id,
            sort_order=sort_order,
        )

        return evaluation_grade_only_results_response_dto_graders_item

