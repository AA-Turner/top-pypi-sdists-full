from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="PublicProblemDetailDtoRubricsByVersionIdAdditionalPropertyItem")



@_attrs_define
class PublicProblemDetailDtoRubricsByVersionIdAdditionalPropertyItem:
    """ Slimmed-down rubric projection used by the frontend rubric editor.

        Attributes:
            id (UUID): Stable rubric identifier (UUID). Rubrics are versioned grading specifications attached to a problem
                version.
            criterion (str): Human-readable description of what this rubric measures.
            weight (float): Relative weight when aggregating rubric scores. Example: 1.
            use_grader_support (bool): True when the rubric should be evaluated by the LLM grader.
            issue_template (None | str): Markdown template that overrides the env-wide rubric issue template. Null inherits
                the env template.
     """

    id: UUID
    criterion: str
    weight: float
    use_grader_support: bool
    issue_template: None | str





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        criterion = self.criterion

        weight = self.weight

        use_grader_support = self.use_grader_support

        issue_template: None | str
        issue_template = self.issue_template


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "criterion": criterion,
            "weight": weight,
            "useGraderSupport": use_grader_support,
            "issueTemplate": issue_template,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        criterion = d.pop("criterion")

        weight = d.pop("weight")

        use_grader_support = d.pop("useGraderSupport")

        def _parse_issue_template(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        issue_template = _parse_issue_template(d.pop("issueTemplate"))


        public_problem_detail_dto_rubrics_by_version_id_additional_property_item = cls(
            id=id,
            criterion=criterion,
            weight=weight,
            use_grader_support=use_grader_support,
            issue_template=issue_template,
        )

        return public_problem_detail_dto_rubrics_by_version_id_additional_property_item

