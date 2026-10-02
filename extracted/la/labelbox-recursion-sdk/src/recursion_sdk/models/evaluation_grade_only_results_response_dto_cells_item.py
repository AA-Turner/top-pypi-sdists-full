from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.evaluation_grade_only_results_response_dto_cells_item_grade_type_0 import EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0





T = TypeVar("T", bound="EvaluationGradeOnlyResultsResponseDtoCellsItem")



@_attrs_define
class EvaluationGradeOnlyResultsResponseDtoCellsItem:
    """ One (trajectory x grader) cell in a grade-only comparison matrix.

        Attributes:
            source_problem_run_id (UUID): The picked trajectory (existing solver run) this cell grades — the matrix row.
            grader_id (UUID): The grader config that produced this cell — the matrix column.
            grade (EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0 | None): This grader’s verdict on this
                trajectory. Null when the grade job has not yet produced a row (e.g. still pending).
     """

    source_problem_run_id: UUID
    grader_id: UUID
    grade: EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0 | None





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_grade_only_results_response_dto_cells_item_grade_type_0 import EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0 # noqa: PLC0415
        source_problem_run_id = str(self.source_problem_run_id)

        grader_id = str(self.grader_id)

        grade: dict[str, Any] | None
        if isinstance(self.grade, EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0):
            grade = self.grade.to_dict()
        else:
            grade = self.grade


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "sourceProblemRunId": source_problem_run_id,
            "graderId": grader_id,
            "grade": grade,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_grade_only_results_response_dto_cells_item_grade_type_0 import EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0 # noqa: PLC0415
        d = dict(src_dict)
        source_problem_run_id = UUID(d.pop("sourceProblemRunId"))




        grader_id = UUID(d.pop("graderId"))




        def _parse_grade(data: object) -> EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                grade_type_0 = EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0.from_dict(data)



                return grade_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EvaluationGradeOnlyResultsResponseDtoCellsItemGradeType0 | None, data)

        grade = _parse_grade(d.pop("grade"))


        evaluation_grade_only_results_response_dto_cells_item = cls(
            source_problem_run_id=source_problem_run_id,
            grader_id=grader_id,
            grade=grade,
        )

        return evaluation_grade_only_results_response_dto_cells_item

