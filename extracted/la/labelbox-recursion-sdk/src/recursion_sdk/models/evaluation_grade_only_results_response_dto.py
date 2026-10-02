from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.evaluation_grade_only_results_response_dto_kind import EvaluationGradeOnlyResultsResponseDtoKind
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.evaluation_grade_only_results_response_dto_cells_item import EvaluationGradeOnlyResultsResponseDtoCellsItem
  from ..models.evaluation_grade_only_results_response_dto_graders_item import EvaluationGradeOnlyResultsResponseDtoGradersItem
  from ..models.evaluation_grade_only_results_response_dto_trajectories_item import EvaluationGradeOnlyResultsResponseDtoTrajectoriesItem





T = TypeVar("T", bound="EvaluationGradeOnlyResultsResponseDto")



@_attrs_define
class EvaluationGradeOnlyResultsResponseDto:
    """ Full grade-only comparison matrix across trajectories and graders.

        Attributes:
            kind (EvaluationGradeOnlyResultsResponseDtoKind): Discriminant identifying this as a grade-only results payload.
            evaluation_id (UUID): Stable evaluation identifier (UUID). An evaluation is a multi-problem comparison run.
            graders (list[EvaluationGradeOnlyResultsResponseDtoGradersItem]): Ordered grader columns, including the labels
                and run-config versions for cell IDs.
            cells (list[EvaluationGradeOnlyResultsResponseDtoCellsItem]): One cell per (trajectory x grader) pair in the
                evaluation.
            trajectories (list[EvaluationGradeOnlyResultsResponseDtoTrajectoriesItem]): Per-trajectory grader-agreement
                summaries, one per picked trajectory.
     """

    kind: EvaluationGradeOnlyResultsResponseDtoKind
    evaluation_id: UUID
    graders: list[EvaluationGradeOnlyResultsResponseDtoGradersItem]
    cells: list[EvaluationGradeOnlyResultsResponseDtoCellsItem]
    trajectories: list[EvaluationGradeOnlyResultsResponseDtoTrajectoriesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_grade_only_results_response_dto_cells_item import EvaluationGradeOnlyResultsResponseDtoCellsItem # noqa: PLC0415
        from ..models.evaluation_grade_only_results_response_dto_graders_item import EvaluationGradeOnlyResultsResponseDtoGradersItem # noqa: PLC0415
        from ..models.evaluation_grade_only_results_response_dto_trajectories_item import EvaluationGradeOnlyResultsResponseDtoTrajectoriesItem # noqa: PLC0415
        kind = self.kind.value

        evaluation_id = str(self.evaluation_id)

        graders = []
        for graders_item_data in self.graders:
            graders_item = graders_item_data.to_dict()
            graders.append(graders_item)



        cells = []
        for cells_item_data in self.cells:
            cells_item = cells_item_data.to_dict()
            cells.append(cells_item)



        trajectories = []
        for trajectories_item_data in self.trajectories:
            trajectories_item = trajectories_item_data.to_dict()
            trajectories.append(trajectories_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "evaluationId": evaluation_id,
            "graders": graders,
            "cells": cells,
            "trajectories": trajectories,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_grade_only_results_response_dto_cells_item import EvaluationGradeOnlyResultsResponseDtoCellsItem # noqa: PLC0415
        from ..models.evaluation_grade_only_results_response_dto_graders_item import EvaluationGradeOnlyResultsResponseDtoGradersItem # noqa: PLC0415
        from ..models.evaluation_grade_only_results_response_dto_trajectories_item import EvaluationGradeOnlyResultsResponseDtoTrajectoriesItem # noqa: PLC0415
        d = dict(src_dict)
        kind = EvaluationGradeOnlyResultsResponseDtoKind(d.pop("kind"))




        evaluation_id = UUID(d.pop("evaluationId"))




        graders = []
        _graders = d.pop("graders")
        for graders_item_data in (_graders):
            graders_item = EvaluationGradeOnlyResultsResponseDtoGradersItem.from_dict(graders_item_data)



            graders.append(graders_item)


        cells = []
        _cells = d.pop("cells")
        for cells_item_data in (_cells):
            cells_item = EvaluationGradeOnlyResultsResponseDtoCellsItem.from_dict(cells_item_data)



            cells.append(cells_item)


        trajectories = []
        _trajectories = d.pop("trajectories")
        for trajectories_item_data in (_trajectories):
            trajectories_item = EvaluationGradeOnlyResultsResponseDtoTrajectoriesItem.from_dict(trajectories_item_data)



            trajectories.append(trajectories_item)


        evaluation_grade_only_results_response_dto = cls(
            kind=kind,
            evaluation_id=evaluation_id,
            graders=graders,
            cells=cells,
            trajectories=trajectories,
        )

        return evaluation_grade_only_results_response_dto

