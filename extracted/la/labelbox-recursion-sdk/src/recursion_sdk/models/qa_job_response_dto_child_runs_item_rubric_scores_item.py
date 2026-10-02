from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qa_job_response_dto_child_runs_item_rubric_scores_item_status import QaJobResponseDtoChildRunsItemRubricScoresItemStatus
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="QaJobResponseDtoChildRunsItemRubricScoresItem")



@_attrs_define
class QaJobResponseDtoChildRunsItemRubricScoresItem:
    """ One per-criterion rubric score belonging to a rubric child run of a composite QA job.

        Attributes:
            id (UUID): Stable rubric-score identifier (UUID). Points at one rubric's score for one problem run.
            rubric_id (UUID): Rubric criterion this score was produced for.
            criterion (str): Human-readable text of the rubric criterion being scored.
            weight (float): Relative weight of this criterion when aggregating the rubric leaf score.
            sort_order (int): Display order of this criterion within its rubric leaf.
            achieved_score (float | None): Normalized score between zero and one the grader assigned this criterion; null
                until completion. For a penalty (negative-weight) criterion, 1 means the penalized behavior occurred and 0 means
                it did not.
            justification (str): Grader-authored justification for this criterion score.
            status (QaJobResponseDtoChildRunsItemRubricScoresItemStatus): Current lifecycle status of this criterion score.
     """

    id: UUID
    rubric_id: UUID
    criterion: str
    weight: float
    sort_order: int
    achieved_score: float | None
    justification: str
    status: QaJobResponseDtoChildRunsItemRubricScoresItemStatus





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        rubric_id = str(self.rubric_id)

        criterion = self.criterion

        weight = self.weight

        sort_order = self.sort_order

        achieved_score: float | None
        achieved_score = self.achieved_score

        justification = self.justification

        status = self.status.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "rubricId": rubric_id,
            "criterion": criterion,
            "weight": weight,
            "sortOrder": sort_order,
            "achievedScore": achieved_score,
            "justification": justification,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        rubric_id = UUID(d.pop("rubricId"))




        criterion = d.pop("criterion")

        weight = d.pop("weight")

        sort_order = d.pop("sortOrder")

        def _parse_achieved_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        achieved_score = _parse_achieved_score(d.pop("achievedScore"))


        justification = d.pop("justification")

        status = QaJobResponseDtoChildRunsItemRubricScoresItemStatus(d.pop("status"))




        qa_job_response_dto_child_runs_item_rubric_scores_item = cls(
            id=id,
            rubric_id=rubric_id,
            criterion=criterion,
            weight=weight,
            sort_order=sort_order,
            achieved_score=achieved_score,
            justification=justification,
            status=status,
        )

        return qa_job_response_dto_child_runs_item_rubric_scores_item

