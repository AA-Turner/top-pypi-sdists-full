from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transcript_reformat_run_dto_status import TranscriptReformatRunDtoStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.transcript_reformat_run_dto_properties_result_any_of_0_already_formatted import TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted
  from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted import TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted





T = TypeVar("T", bound="TranscriptReformatRunDto")



@_attrs_define
class TranscriptReformatRunDto:
    """ One async transcript-reformat run: enqueue returns 202 with the run id, then a background poller writes the terminal
    result back for the UI to poll.

        Attributes:
            id (UUID): Stable transcript-reformat-run identifier (UUID). One async re-segmentation attempt at one problem
                run’s transcript, executed off the request path by a background poller.
            problem_run_id (UUID): Problem run whose transcript this run re-segments.
            status (TranscriptReformatRunDtoStatus): Lifecycle status of this reformat run.
            result (None | TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted |
                TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted): Re-segmentation outcome. Populated only on a
                terminal succeeded run; null otherwise.
            error_message (None | str): User-facing failure reason. Populated only on a terminal failed run; null otherwise.
            submitted_at (datetime.datetime): Timestamp when the reformat run was enqueued (ISO-8601, UTC).
            completed_at (datetime.datetime | None): Timestamp when the reformat run reached a terminal status (ISO-8601,
                UTC). Null while non-terminal.
     """

    id: UUID
    problem_run_id: UUID
    status: TranscriptReformatRunDtoStatus
    result: None | TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted | TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted
    error_message: None | str
    submitted_at: datetime.datetime
    completed_at: datetime.datetime | None





    def to_dict(self) -> dict[str, Any]:
        from ..models.transcript_reformat_run_dto_properties_result_any_of_0_already_formatted import TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted # noqa: PLC0415
        from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted import TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted # noqa: PLC0415
        id = str(self.id)

        problem_run_id = str(self.problem_run_id)

        status = self.status.value

        result: dict[str, Any] | None
        if isinstance(self.result, TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted):
            result = self.result.to_dict()
        elif isinstance(self.result, TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted):
            result = self.result.to_dict()
        else:
            result = self.result

        error_message: None | str
        error_message = self.error_message

        submitted_at = self.submitted_at.isoformat()

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "problemRunId": problem_run_id,
            "status": status,
            "result": result,
            "errorMessage": error_message,
            "submittedAt": submitted_at,
            "completedAt": completed_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transcript_reformat_run_dto_properties_result_any_of_0_already_formatted import TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted # noqa: PLC0415
        from ..models.transcript_reformat_run_dto_properties_result_any_of_0_reformatted import TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        problem_run_id = UUID(d.pop("problemRunId"))




        status = TranscriptReformatRunDtoStatus(d.pop("status"))




        def _parse_result(data: object) -> None | TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted | TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0_type_0 = TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted.from_dict(data)



                return result_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0_type_1 = TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted.from_dict(data)



                return result_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TranscriptReformatRunDtoPropertiesResultAnyOf0AlreadyFormatted | TranscriptReformatRunDtoPropertiesResultAnyOf0Reformatted, data)

        result = _parse_result(d.pop("result"))


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        submitted_at = datetime.datetime.fromisoformat(d.pop("submittedAt"))




        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)



                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completedAt"))


        transcript_reformat_run_dto = cls(
            id=id,
            problem_run_id=problem_run_id,
            status=status,
            result=result,
            error_message=error_message,
            submitted_at=submitted_at,
            completed_at=completed_at,
        )

        return transcript_reformat_run_dto

