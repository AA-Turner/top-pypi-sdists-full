from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_run_execution_evidence_dto_graders_item_status import ProblemRunExecutionEvidenceDtoGradersItemStatus
from ..models.problem_run_execution_evidence_dto_graders_item_strategy import ProblemRunExecutionEvidenceDtoGradersItemStrategy
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ProblemRunExecutionEvidenceDtoGradersItem")



@_attrs_define
class ProblemRunExecutionEvidenceDtoGradersItem:
    """ Execution identity and persisted evidence for one grader sub-run.

        Attributes:
            grading_run_id (UUID): Stable grading-run identifier (UUID). One grader execution producing rubric scores for a
                problem run.
            external_run_id (None | str): Agent-service run ID for this grader sub-run, when dispatched.
            strategy (ProblemRunExecutionEvidenceDtoGradersItemStrategy): Grading strategy used for a sub-run: rubric
                aggregation, LLM-based grading, a programmatic checker, fixed read-only MCP tool calls compared against an
                expected value, or a command executed against the solver’s persistent compute.
            status (ProblemRunExecutionEvidenceDtoGradersItemStatus): Lifecycle status of a grading run.
            has_transcript (bool): Whether the grader transcript is available to fetch.
            grader_run_config_version_id (None | UUID): Locked run-config version that governed this grader sub-run. Null
                when no run-config version was recorded.
     """

    grading_run_id: UUID
    external_run_id: None | str
    strategy: ProblemRunExecutionEvidenceDtoGradersItemStrategy
    status: ProblemRunExecutionEvidenceDtoGradersItemStatus
    has_transcript: bool
    grader_run_config_version_id: None | UUID





    def to_dict(self) -> dict[str, Any]:
        grading_run_id = str(self.grading_run_id)

        external_run_id: None | str
        external_run_id = self.external_run_id

        strategy = self.strategy.value

        status = self.status.value

        has_transcript = self.has_transcript

        grader_run_config_version_id: None | str
        if isinstance(self.grader_run_config_version_id, UUID):
            grader_run_config_version_id = str(self.grader_run_config_version_id)
        else:
            grader_run_config_version_id = self.grader_run_config_version_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gradingRunId": grading_run_id,
            "externalRunId": external_run_id,
            "strategy": strategy,
            "status": status,
            "hasTranscript": has_transcript,
            "graderRunConfigVersionId": grader_run_config_version_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grading_run_id = UUID(d.pop("gradingRunId"))




        def _parse_external_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_run_id = _parse_external_run_id(d.pop("externalRunId"))


        strategy = ProblemRunExecutionEvidenceDtoGradersItemStrategy(d.pop("strategy"))




        status = ProblemRunExecutionEvidenceDtoGradersItemStatus(d.pop("status"))




        has_transcript = d.pop("hasTranscript")

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


        problem_run_execution_evidence_dto_graders_item = cls(
            grading_run_id=grading_run_id,
            external_run_id=external_run_id,
            strategy=strategy,
            status=status,
            has_transcript=has_transcript,
            grader_run_config_version_id=grader_run_config_version_id,
        )

        return problem_run_execution_evidence_dto_graders_item

