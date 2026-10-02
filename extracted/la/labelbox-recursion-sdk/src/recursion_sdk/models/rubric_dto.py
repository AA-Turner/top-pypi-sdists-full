from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="RubricDto")



@_attrs_define
class RubricDto:
    """ A weighted grading criterion attached to a problem version.

        Example:
            {'id': '0abbf992-d9f0-46eb-8d44-939b8b2d055f', 'problemVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71',
                'criterion': 'Correctly identifies all surface defects present in the image', 'weight': 2, 'useGraderSupport':
                True, 'sortOrder': 0, 'issueTemplate': None, 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z'}

        Attributes:
            id (UUID): Stable rubric identifier (UUID). Rubrics are versioned grading specifications attached to a problem
                version.
            problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this
                points at one specific version.
            criterion (str): Human-readable description of what this rubric measures.
            weight (float): Relative weight when aggregating rubric scores. Positive weights reward; negative weights
                penalize. Example: 1.
            use_grader_support (bool): True when the rubric should be evaluated by the LLM grader; false when human-only.
            sort_order (int): Display order of the rubric within its problem version.
            issue_template (None | str): Markdown template that overrides the env-wide rubric issue template for issues
                attached to this rubric. Null inherits the env template.
            created_at (datetime.datetime): Timestamp when the rubric was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the rubric was last updated (ISO-8601, UTC).
     """

    id: UUID
    problem_version_id: UUID
    criterion: str
    weight: float
    use_grader_support: bool
    sort_order: int
    issue_template: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        problem_version_id = str(self.problem_version_id)

        criterion = self.criterion

        weight = self.weight

        use_grader_support = self.use_grader_support

        sort_order = self.sort_order

        issue_template: None | str
        issue_template = self.issue_template

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "problemVersionId": problem_version_id,
            "criterion": criterion,
            "weight": weight,
            "useGraderSupport": use_grader_support,
            "sortOrder": sort_order,
            "issueTemplate": issue_template,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        problem_version_id = UUID(d.pop("problemVersionId"))




        criterion = d.pop("criterion")

        weight = d.pop("weight")

        use_grader_support = d.pop("useGraderSupport")

        sort_order = d.pop("sortOrder")

        def _parse_issue_template(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        issue_template = _parse_issue_template(d.pop("issueTemplate"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        rubric_dto = cls(
            id=id,
            problem_version_id=problem_version_id,
            criterion=criterion,
            weight=weight,
            use_grader_support=use_grader_support,
            sort_order=sort_order,
            issue_template=issue_template,
            created_at=created_at,
            updated_at=updated_at,
        )

        return rubric_dto

