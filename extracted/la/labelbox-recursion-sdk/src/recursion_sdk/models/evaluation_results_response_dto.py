from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.evaluation_results_response_dto_cells_item import EvaluationResultsResponseDtoCellsItem





T = TypeVar("T", bound="EvaluationResultsResponseDto")



@_attrs_define
class EvaluationResultsResponseDto:
    """ Full results matrix for an evaluation across solvers and problem versions.

        Example:
            {'evaluationId': '40811982-da7a-42bb-9963-5ca612372c63', 'cells': [{'solverId':
                'b5d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e', 'problemVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'meanScore':
                0.67, 'stddev': 0.47, 'minScore': 0, 'maxScore': 1, 'passCount': 2, 'failCount': 1, 'totalRuns': 3,
                'completedRuns': 3, 'totalCostUsd': 0.42, 'meanExecutionTimeMs': 18500, 'attempts': [{'problemRunId':
                'e8f7a6b5-4c3d-4e2f-9a1b-0c8d7e6f5a4b', 'attemptNumber': 1, 'score': 1, 'status': 'completed', 'costUsd': 0.14,
                'executionTimeMs': 18500, 'startedAt': '2026-01-15T10:00:00.000Z', 'completedAt': '2026-01-15T10:00:18.500Z',
                'errorMessage': None, 'inputTokens': 1200, 'outputTokens': 340, 'cacheReadInputTokens': 0,
                'cacheCreationInputTokens': 0, 'infraRetryCount': 0, 'jobV2Id': '5b6c7d8e-9f0a-4b1c-8d2e-3f4a5b6c7d8e'},
                {'problemRunId': '1be7d569-e271-4926-af2c-569798de74d7', 'attemptNumber': 2, 'score': 1, 'status': 'completed',
                'costUsd': 0.14, 'executionTimeMs': 18500, 'startedAt': '2026-01-15T10:00:00.000Z', 'completedAt':
                '2026-01-15T10:00:18.500Z', 'errorMessage': None, 'inputTokens': 1200, 'outputTokens': 340,
                'cacheReadInputTokens': 0, 'cacheCreationInputTokens': 0, 'infraRetryCount': 1, 'jobV2Id':
                '6c7d8e9f-0a1b-4c2d-8e3f-4a5b6c7d8e9f'}, {'problemRunId': 'a3f4d5e6-7b8c-4d9e-8a1b-2c3d4e5f6a7b',
                'attemptNumber': 3, 'score': 0, 'status': 'completed', 'costUsd': 0.14, 'executionTimeMs': 18500, 'startedAt':
                '2026-01-15T10:00:00.000Z', 'completedAt': '2026-01-15T10:00:18.500Z', 'errorMessage': None, 'inputTokens':
                1200, 'outputTokens': 340, 'cacheReadInputTokens': 0, 'cacheCreationInputTokens': 0, 'infraRetryCount': 0,
                'jobV2Id': '7d8e9f0a-1b2c-4d3e-8f4a-5b6c7d8e9f0a'}]}]}

        Attributes:
            evaluation_id (UUID): Stable evaluation identifier (UUID). An evaluation is a multi-problem comparison run.
            cells (list[EvaluationResultsResponseDtoCellsItem]): One cell per solver and problem-version pair in the
                evaluation.
     """

    evaluation_id: UUID
    cells: list[EvaluationResultsResponseDtoCellsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_results_response_dto_cells_item import EvaluationResultsResponseDtoCellsItem # noqa: PLC0415
        evaluation_id = str(self.evaluation_id)

        cells = []
        for cells_item_data in self.cells:
            cells_item = cells_item_data.to_dict()
            cells.append(cells_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "evaluationId": evaluation_id,
            "cells": cells,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_results_response_dto_cells_item import EvaluationResultsResponseDtoCellsItem # noqa: PLC0415
        d = dict(src_dict)
        evaluation_id = UUID(d.pop("evaluationId"))




        cells = []
        _cells = d.pop("cells")
        for cells_item_data in (_cells):
            cells_item = EvaluationResultsResponseDtoCellsItem.from_dict(cells_item_data)



            cells.append(cells_item)


        evaluation_results_response_dto = cls(
            evaluation_id=evaluation_id,
            cells=cells,
        )

        return evaluation_results_response_dto

