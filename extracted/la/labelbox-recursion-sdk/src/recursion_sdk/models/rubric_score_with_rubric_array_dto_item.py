from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.rubric_score_with_rubric_array_dto_item_status import RubricScoreWithRubricArrayDtoItemStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="RubricScoreWithRubricArrayDtoItem")



@_attrs_define
class RubricScoreWithRubricArrayDtoItem:
    """ Rubric score joined with criterion, weight, and sort order from the parent rubric.

        Example:
            {'id': '70e02cd5-6e85-42ba-bc8e-39fd7279112a', 'problemRunId': '22d435e7-9e41-4554-b0bd-dab57a202b71',
                'gradingRunId': '1be7d569-e271-4926-af2c-569798de74d7', 'rubricId': '0abbf992-d9f0-46eb-8d44-939b8b2d055f',
                'externalRunId': None, 'achievedScore': 0.92, 'justification': 'The agent flagged every visible scratch and dent
                on the panel, matching all ground-truth defects with no omissions.', 'status': 'completed', 'createdAt':
                '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-15T09:32:45.000Z', 'criterion': 'Correctly identifies all
                surface defects', 'weight': 1, 'sortOrder': 0}

        Attributes:
            id (UUID): Stable rubric-score identifier (UUID). Points at one rubric's score for one problem run.
            problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one problem version.
            grading_run_id (None | UUID): Grading run that produced this score. Null for legacy rows or scores produced
                outside a grading run.
            rubric_id (UUID): Stable rubric identifier (UUID). Rubrics are versioned grading specifications attached to a
                problem version.
            external_run_id (None | str): Upstream grader-service run identifier, if the score came from an external grader.
            achieved_score (float | None): Normalized score in [0, 1] achieved for this rubric. For a penalty (negative-
                weight) rubric, 1 means the penalized behavior occurred and 0 means it did not. Null until grading completes.
                Example: 0.85.
            justification (str): Grader-authored explanation for the achieved score.
            status (RubricScoreWithRubricArrayDtoItemStatus): Current lifecycle status of the rubric score.
            created_at (datetime.datetime): Timestamp when the rubric score row was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the rubric score row was last updated (ISO-8601, UTC).
            criterion (str): Human-readable criterion text from the associated rubric.
            weight (float): Weight of the associated rubric used when aggregating the final score.
            sort_order (int): Display order of the rubric within its problem version.
     """

    id: UUID
    problem_run_id: UUID
    grading_run_id: None | UUID
    rubric_id: UUID
    external_run_id: None | str
    achieved_score: float | None
    justification: str
    status: RubricScoreWithRubricArrayDtoItemStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    criterion: str
    weight: float
    sort_order: int





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        problem_run_id = str(self.problem_run_id)

        grading_run_id: None | str
        if isinstance(self.grading_run_id, UUID):
            grading_run_id = str(self.grading_run_id)
        else:
            grading_run_id = self.grading_run_id

        rubric_id = str(self.rubric_id)

        external_run_id: None | str
        external_run_id = self.external_run_id

        achieved_score: float | None
        achieved_score = self.achieved_score

        justification = self.justification

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        criterion = self.criterion

        weight = self.weight

        sort_order = self.sort_order


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "problemRunId": problem_run_id,
            "gradingRunId": grading_run_id,
            "rubricId": rubric_id,
            "externalRunId": external_run_id,
            "achievedScore": achieved_score,
            "justification": justification,
            "status": status,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "criterion": criterion,
            "weight": weight,
            "sortOrder": sort_order,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        problem_run_id = UUID(d.pop("problemRunId"))




        def _parse_grading_run_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grading_run_id_type_0 = UUID(data)



                return grading_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        grading_run_id = _parse_grading_run_id(d.pop("gradingRunId"))


        rubric_id = UUID(d.pop("rubricId"))




        def _parse_external_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_run_id = _parse_external_run_id(d.pop("externalRunId"))


        def _parse_achieved_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        achieved_score = _parse_achieved_score(d.pop("achievedScore"))


        justification = d.pop("justification")

        status = RubricScoreWithRubricArrayDtoItemStatus(d.pop("status"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        criterion = d.pop("criterion")

        weight = d.pop("weight")

        sort_order = d.pop("sortOrder")

        rubric_score_with_rubric_array_dto_item = cls(
            id=id,
            problem_run_id=problem_run_id,
            grading_run_id=grading_run_id,
            rubric_id=rubric_id,
            external_run_id=external_run_id,
            achieved_score=achieved_score,
            justification=justification,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            criterion=criterion,
            weight=weight,
            sort_order=sort_order,
        )

        return rubric_score_with_rubric_array_dto_item

