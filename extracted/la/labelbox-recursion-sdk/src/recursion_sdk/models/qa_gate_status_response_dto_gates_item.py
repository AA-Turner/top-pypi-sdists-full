from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qa_gate_status_response_dto_gates_item_blocked_stage import QaGateStatusResponseDtoGatesItemBlockedStage
from ..models.qa_gate_status_response_dto_gates_item_latest_job_status_type_0 import QaGateStatusResponseDtoGatesItemLatestJobStatusType0
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="QaGateStatusResponseDtoGatesItem")



@_attrs_define
class QaGateStatusResponseDtoGatesItem:
    """ Pass/fail status of a single QA gate for a specific problem version.

        Attributes:
            gate_id (UUID): Gate this status row reports on.
            qa_config_id (UUID): QA config bound to the gate.
            qa_config_name (str): Display name of the QA config bound to the gate.
            blocked_stage (QaGateStatusResponseDtoGatesItemBlockedStage): Workflow stage blocked by the gate.
            passed (bool): True if the latest QA result for this gate satisfies the pass criteria.
            latest_score (float | None): Most recent normalized QA score for the gate. Null if no job has produced a score.
                Example: 0.92.
            latest_grade (None | str): Most recent categorical QA grade for the gate. Null if no job has produced a grade.
            latest_job_id (None | UUID): QA job whose result is reflected by this status. Null if no job has run for the
                gate.
            latest_job_status (None | QaGateStatusResponseDtoGatesItemLatestJobStatusType0): Lifecycle status of the most
                recent QA job. Null when no job has run.
     """

    gate_id: UUID
    qa_config_id: UUID
    qa_config_name: str
    blocked_stage: QaGateStatusResponseDtoGatesItemBlockedStage
    passed: bool
    latest_score: float | None
    latest_grade: None | str
    latest_job_id: None | UUID
    latest_job_status: None | QaGateStatusResponseDtoGatesItemLatestJobStatusType0





    def to_dict(self) -> dict[str, Any]:
        gate_id = str(self.gate_id)

        qa_config_id = str(self.qa_config_id)

        qa_config_name = self.qa_config_name

        blocked_stage = self.blocked_stage.value

        passed = self.passed

        latest_score: float | None
        latest_score = self.latest_score

        latest_grade: None | str
        latest_grade = self.latest_grade

        latest_job_id: None | str
        if isinstance(self.latest_job_id, UUID):
            latest_job_id = str(self.latest_job_id)
        else:
            latest_job_id = self.latest_job_id

        latest_job_status: None | str
        if isinstance(self.latest_job_status, QaGateStatusResponseDtoGatesItemLatestJobStatusType0):
            latest_job_status = self.latest_job_status.value
        else:
            latest_job_status = self.latest_job_status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gateId": gate_id,
            "qaConfigId": qa_config_id,
            "qaConfigName": qa_config_name,
            "blockedStage": blocked_stage,
            "passed": passed,
            "latestScore": latest_score,
            "latestGrade": latest_grade,
            "latestJobId": latest_job_id,
            "latestJobStatus": latest_job_status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate_id = UUID(d.pop("gateId"))




        qa_config_id = UUID(d.pop("qaConfigId"))




        qa_config_name = d.pop("qaConfigName")

        blocked_stage = QaGateStatusResponseDtoGatesItemBlockedStage(d.pop("blockedStage"))




        passed = d.pop("passed")

        def _parse_latest_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        latest_score = _parse_latest_score(d.pop("latestScore"))


        def _parse_latest_grade(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        latest_grade = _parse_latest_grade(d.pop("latestGrade"))


        def _parse_latest_job_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_job_id_type_0 = UUID(data)



                return latest_job_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        latest_job_id = _parse_latest_job_id(d.pop("latestJobId"))


        def _parse_latest_job_status(data: object) -> None | QaGateStatusResponseDtoGatesItemLatestJobStatusType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_job_status_type_0 = QaGateStatusResponseDtoGatesItemLatestJobStatusType0(data)



                return latest_job_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QaGateStatusResponseDtoGatesItemLatestJobStatusType0, data)

        latest_job_status = _parse_latest_job_status(d.pop("latestJobStatus"))


        qa_gate_status_response_dto_gates_item = cls(
            gate_id=gate_id,
            qa_config_id=qa_config_id,
            qa_config_name=qa_config_name,
            blocked_stage=blocked_stage,
            passed=passed,
            latest_score=latest_score,
            latest_grade=latest_grade,
            latest_job_id=latest_job_id,
            latest_job_status=latest_job_status,
        )

        return qa_gate_status_response_dto_gates_item

