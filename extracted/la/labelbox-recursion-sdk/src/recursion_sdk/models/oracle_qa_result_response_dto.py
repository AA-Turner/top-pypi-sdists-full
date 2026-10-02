from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.oracle_qa_result_response_dto_status import OracleQaResultResponseDtoStatus
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.oracle_qa_result_response_dto_result_type_0 import OracleQaResultResponseDtoResultType0





T = TypeVar("T", bound="OracleQaResultResponseDto")



@_attrs_define
class OracleQaResultResponseDto:
    """ Oracle QA outcome surfaced alongside grading results so the UI can show whether the grader matched the gold
    standard.

        Attributes:
            job_id (UUID): Stable QA-job identifier (UUID).
            status (OracleQaResultResponseDtoStatus): Lifecycle status of a QA job from queueing through dispatch and
                execution to a terminal state.
            score (float | None): Summary score from the oracle QA job; null when not yet produced.
            grade (None | str): Summary grade label from the oracle QA job; null when not yet produced.
            result (None | OracleQaResultResponseDtoResultType0): Detailed oracle QA result payload, or null when the job is
                still in flight.
     """

    job_id: UUID
    status: OracleQaResultResponseDtoStatus
    score: float | None
    grade: None | str
    result: None | OracleQaResultResponseDtoResultType0





    def to_dict(self) -> dict[str, Any]:
        from ..models.oracle_qa_result_response_dto_result_type_0 import OracleQaResultResponseDtoResultType0 # noqa: PLC0415
        job_id = str(self.job_id)

        status = self.status.value

        score: float | None
        score = self.score

        grade: None | str
        grade = self.grade

        result: dict[str, Any] | None
        if isinstance(self.result, OracleQaResultResponseDtoResultType0):
            result = self.result.to_dict()
        else:
            result = self.result


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "jobId": job_id,
            "status": status,
            "score": score,
            "grade": grade,
            "result": result,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.oracle_qa_result_response_dto_result_type_0 import OracleQaResultResponseDtoResultType0 # noqa: PLC0415
        d = dict(src_dict)
        job_id = UUID(d.pop("jobId"))




        status = OracleQaResultResponseDtoStatus(d.pop("status"))




        def _parse_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        score = _parse_score(d.pop("score"))


        def _parse_grade(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        grade = _parse_grade(d.pop("grade"))


        def _parse_result(data: object) -> None | OracleQaResultResponseDtoResultType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = OracleQaResultResponseDtoResultType0.from_dict(data)



                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OracleQaResultResponseDtoResultType0, data)

        result = _parse_result(d.pop("result"))


        oracle_qa_result_response_dto = cls(
            job_id=job_id,
            status=status,
            score=score,
            grade=grade,
            result=result,
        )

        return oracle_qa_result_response_dto

