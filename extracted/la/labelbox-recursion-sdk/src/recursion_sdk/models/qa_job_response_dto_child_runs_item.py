from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qa_job_response_dto_child_runs_item_status import QaJobResponseDtoChildRunsItemStatus
from ..models.qa_job_response_dto_child_runs_item_strategy import QaJobResponseDtoChildRunsItemStrategy
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.qa_job_response_dto_child_runs_item_rubric_scores_item import QaJobResponseDtoChildRunsItemRubricScoresItem





T = TypeVar("T", bound="QaJobResponseDtoChildRunsItem")



@_attrs_define
class QaJobResponseDtoChildRunsItem:
    """ One per-leaf child container execution of a composite QA job.

        Attributes:
            id (UUID): Stable QA-job-run identifier (UUID). One per-leaf child container execution of a composite QA job.
            qa_job_id (UUID): Parent QA job this child run belongs to.
            strategy (QaJobResponseDtoChildRunsItemStrategy): Strategy executed by this child run.
            weight (float): Weight of this child run when aggregating the composite QA job score.
            node_path (None | str): Position of this child run within the grading-config tree (dot-delimited). Nullable in
                storage, but always set by the service that creates child runs.
            status (QaJobResponseDtoChildRunsItemStatus): Current lifecycle status of the child run.
            score (float | None): Normalized score between zero and one produced by this child run; null until completion.
            error (None | str): Error message if the child run failed; null on success or while still running.
            justification (None | str): Grader-authored justification for the score; null for rubric child runs or before
                completion.
            external_run_id (None | str): Launcher-assigned external run identifier for this child, or null before dispatch.
            attempt_count (float): Number of attempts executed so far for this child run.
            created_at (str): Timestamp when the child run was created (ISO-8601, UTC).
            run_config_name (None | str): Display name of the run config whose locked version this child run executed
                (resolved from the run-config-version FK); null when no run config is bound.
            version_number (int | None): Version number of the bound run-config version this child run executed; null when
                no run config is bound.
            rubric_scores (list[QaJobResponseDtoChildRunsItemRubricScoresItem] | Unset): Per-criterion rubric scores for a
                rubric child run; populated on the detail endpoint for rubric leaves when the caller may read rubric scores,
                omitted otherwise.
     """

    id: UUID
    qa_job_id: UUID
    strategy: QaJobResponseDtoChildRunsItemStrategy
    weight: float
    node_path: None | str
    status: QaJobResponseDtoChildRunsItemStatus
    score: float | None
    error: None | str
    justification: None | str
    external_run_id: None | str
    attempt_count: float
    created_at: str
    run_config_name: None | str
    version_number: int | None
    rubric_scores: list[QaJobResponseDtoChildRunsItemRubricScoresItem] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.qa_job_response_dto_child_runs_item_rubric_scores_item import QaJobResponseDtoChildRunsItemRubricScoresItem # noqa: PLC0415
        id = str(self.id)

        qa_job_id = str(self.qa_job_id)

        strategy = self.strategy.value

        weight = self.weight

        node_path: None | str
        node_path = self.node_path

        status = self.status.value

        score: float | None
        score = self.score

        error: None | str
        error = self.error

        justification: None | str
        justification = self.justification

        external_run_id: None | str
        external_run_id = self.external_run_id

        attempt_count = self.attempt_count

        created_at = self.created_at

        run_config_name: None | str
        run_config_name = self.run_config_name

        version_number: int | None
        version_number = self.version_number

        rubric_scores: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rubric_scores, Unset):
            rubric_scores = []
            for rubric_scores_item_data in self.rubric_scores:
                rubric_scores_item = rubric_scores_item_data.to_dict()
                rubric_scores.append(rubric_scores_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "qaJobId": qa_job_id,
            "strategy": strategy,
            "weight": weight,
            "nodePath": node_path,
            "status": status,
            "score": score,
            "error": error,
            "justification": justification,
            "externalRunId": external_run_id,
            "attemptCount": attempt_count,
            "createdAt": created_at,
            "runConfigName": run_config_name,
            "versionNumber": version_number,
        })
        if rubric_scores is not UNSET:
            field_dict["rubricScores"] = rubric_scores

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.qa_job_response_dto_child_runs_item_rubric_scores_item import QaJobResponseDtoChildRunsItemRubricScoresItem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        qa_job_id = UUID(d.pop("qaJobId"))




        strategy = QaJobResponseDtoChildRunsItemStrategy(d.pop("strategy"))




        weight = d.pop("weight")

        def _parse_node_path(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        node_path = _parse_node_path(d.pop("nodePath"))


        status = QaJobResponseDtoChildRunsItemStatus(d.pop("status"))




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


        def _parse_external_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_run_id = _parse_external_run_id(d.pop("externalRunId"))


        attempt_count = d.pop("attemptCount")

        created_at = d.pop("createdAt")

        def _parse_run_config_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        run_config_name = _parse_run_config_name(d.pop("runConfigName"))


        def _parse_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        version_number = _parse_version_number(d.pop("versionNumber"))


        _rubric_scores = d.pop("rubricScores", UNSET)
        rubric_scores: list[QaJobResponseDtoChildRunsItemRubricScoresItem] | Unset = UNSET
        if _rubric_scores is not UNSET:
            rubric_scores = []
            for rubric_scores_item_data in _rubric_scores:
                rubric_scores_item = QaJobResponseDtoChildRunsItemRubricScoresItem.from_dict(rubric_scores_item_data)



                rubric_scores.append(rubric_scores_item)


        qa_job_response_dto_child_runs_item = cls(
            id=id,
            qa_job_id=qa_job_id,
            strategy=strategy,
            weight=weight,
            node_path=node_path,
            status=status,
            score=score,
            error=error,
            justification=justification,
            external_run_id=external_run_id,
            attempt_count=attempt_count,
            created_at=created_at,
            run_config_name=run_config_name,
            version_number=version_number,
            rubric_scores=rubric_scores,
        )

        return qa_job_response_dto_child_runs_item

