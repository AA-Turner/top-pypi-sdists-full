from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_sub_run_response_array_dto_item_status import GradingSubRunResponseArrayDtoItemStatus
from ..models.grading_sub_run_response_array_dto_item_strategy import GradingSubRunResponseArrayDtoItemStrategy
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="GradingSubRunResponseArrayDtoItem")



@_attrs_define
class GradingSubRunResponseArrayDtoItem:
    """ One strategy-level grader execution that contributes to the overall grading run for a problem run.

        Attributes:
            id (UUID): Stable grading-run identifier (UUID). One grader execution producing rubric scores for a problem run.
            strategy (GradingSubRunResponseArrayDtoItemStrategy): Grading strategy executed by this sub-run.
            weight (float): Weight of this sub-run when aggregating the overall score. A weight of zero marks the strategy
                as auxiliary, meaning it is evaluated but excluded from the final score. Example: 0.5.
            status (GradingSubRunResponseArrayDtoItemStatus): Current lifecycle status of the sub-run.
            score (float | None): Score produced by this sub-run, passed through faithfully from the grader with no domain
                limits (may be negative, e.g. a penalty). Null until completion. Example: 0.9.
            error (None | str): Error message if the sub-run failed. Null on success or while still running.
            justification (None | str): Grader-authored justification for the score. Null for rubric sub-runs and for legacy
                data.
            has_transcript (bool): True if a transcript was captured for this sub-run and can be fetched separately.
            node_path (None | str): Position of this sub-run within the grading-config tree (slash-delimited). Null for
                legacy sub-runs.
            grader_run_config_version_id (None | UUID): Run-config-version that drove this grader sub-run, captured at
                INSERT time. Null when no binding hit.
            grader_run_config_name (None | str): Display name of the grader run-config. Non-null when the grader run-config-
                version id is non-null.
            grader_run_config_version_number (int | None): Version number of the grader run-config-version, starting at one.
                Non-null when the grader run-config-version id is non-null. Example: 3.
     """

    id: UUID
    strategy: GradingSubRunResponseArrayDtoItemStrategy
    weight: float
    status: GradingSubRunResponseArrayDtoItemStatus
    score: float | None
    error: None | str
    justification: None | str
    has_transcript: bool
    node_path: None | str
    grader_run_config_version_id: None | UUID
    grader_run_config_name: None | str
    grader_run_config_version_number: int | None





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        strategy = self.strategy.value

        weight = self.weight

        status = self.status.value

        score: float | None
        score = self.score

        error: None | str
        error = self.error

        justification: None | str
        justification = self.justification

        has_transcript = self.has_transcript

        node_path: None | str
        node_path = self.node_path

        grader_run_config_version_id: None | str
        if isinstance(self.grader_run_config_version_id, UUID):
            grader_run_config_version_id = str(self.grader_run_config_version_id)
        else:
            grader_run_config_version_id = self.grader_run_config_version_id

        grader_run_config_name: None | str
        grader_run_config_name = self.grader_run_config_name

        grader_run_config_version_number: int | None
        grader_run_config_version_number = self.grader_run_config_version_number


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "strategy": strategy,
            "weight": weight,
            "status": status,
            "score": score,
            "error": error,
            "justification": justification,
            "hasTranscript": has_transcript,
            "nodePath": node_path,
            "graderRunConfigVersionId": grader_run_config_version_id,
            "graderRunConfigName": grader_run_config_name,
            "graderRunConfigVersionNumber": grader_run_config_version_number,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        strategy = GradingSubRunResponseArrayDtoItemStrategy(d.pop("strategy"))




        weight = d.pop("weight")

        status = GradingSubRunResponseArrayDtoItemStatus(d.pop("status"))




        def _parse_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        score = _parse_score(d.pop("score"))


        def _parse_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error = _parse_error(d.pop("error"))


        def _parse_justification(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        justification = _parse_justification(d.pop("justification"))


        has_transcript = d.pop("hasTranscript")

        def _parse_node_path(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        node_path = _parse_node_path(d.pop("nodePath"))


        def _parse_grader_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grader_run_config_version_id_type_0 = UUID(data)



                return grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        grader_run_config_version_id = _parse_grader_run_config_version_id(d.pop("graderRunConfigVersionId"))


        def _parse_grader_run_config_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        grader_run_config_name = _parse_grader_run_config_name(d.pop("graderRunConfigName"))


        def _parse_grader_run_config_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        grader_run_config_version_number = _parse_grader_run_config_version_number(d.pop("graderRunConfigVersionNumber"))


        grading_sub_run_response_array_dto_item = cls(
            id=id,
            strategy=strategy,
            weight=weight,
            status=status,
            score=score,
            error=error,
            justification=justification,
            has_transcript=has_transcript,
            node_path=node_path,
            grader_run_config_version_id=grader_run_config_version_id,
            grader_run_config_name=grader_run_config_name,
            grader_run_config_version_number=grader_run_config_version_number,
        )

        return grading_sub_run_response_array_dto_item

