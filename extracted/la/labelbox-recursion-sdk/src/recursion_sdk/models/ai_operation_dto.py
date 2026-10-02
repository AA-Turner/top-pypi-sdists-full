from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.ai_operation_dto_status import AiOperationDtoStatus
from ..models.ai_operation_dto_type import AiOperationDtoType
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="AiOperationDto")



@_attrs_define
class AiOperationDto:
    """ One LLM-backed editor action (suggestion or generation) attached to a problem version.

        Example:
            {'id': 'a1f6c2d4-9b3e-4c8a-8f1d-2e7b9c0a4d51', 'type': 'improve_prompt', 'status': 'completed', 'versionId':
                '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'result': {'improved': True, 'prompt': 'You are a manufacturing QA
                agent. Inspect the metal panel image at /workspace/panel.png and identify every surface defect (scratch, dent,
                corrosion). Write a JSON report to /workspace/report.json with one entry per defect: { "type", "bbox": [x, y, w,
                h], "severity": "low" | "medium" | "high" }.', 'explanation': 'Specified the exact output path and JSON shape so
                the programmatic grader can parse the report unambiguously.'}, 'errorMessage': None, 'createdAt':
                '2026-01-16T11:05:00.000Z', 'completedAt': '2026-01-16T11:05:08.000Z'}

        Attributes:
            id (UUID): Stable AI-operation identifier (UUID). Captures a single LLM-backed action (suggestion, generation).
            type_ (AiOperationDtoType): Kind of LLM-backed editor action performed against a problem version.
            status (AiOperationDtoStatus): Lifecycle status of an LLM-backed operation.
            version_id (UUID): Problem version this AI operation targets.
            result (Any | None): Operation-specific result payload produced on success. Null while pending or after failure.
            error_message (None | str): Failure detail when the operation errored; null otherwise.
            created_at (datetime.datetime): Timestamp when the AI operation was created (ISO-8601, UTC).
            completed_at (datetime.datetime | None): Timestamp when the AI operation reached a terminal state (ISO-8601,
                UTC). Null while pending.
     """

    id: UUID
    type_: AiOperationDtoType
    status: AiOperationDtoStatus
    version_id: UUID
    result: Any | None
    error_message: None | str
    created_at: datetime.datetime
    completed_at: datetime.datetime | None





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        type_ = self.type_.value

        status = self.status.value

        version_id = str(self.version_id)

        result: Any | None
        result = self.result

        error_message: None | str
        error_message = self.error_message

        created_at = self.created_at.isoformat()

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "type": type_,
            "status": status,
            "versionId": version_id,
            "result": result,
            "errorMessage": error_message,
            "createdAt": created_at,
            "completedAt": completed_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        type_ = AiOperationDtoType(d.pop("type"))




        status = AiOperationDtoStatus(d.pop("status"))




        version_id = UUID(d.pop("versionId"))




        def _parse_result(data: object) -> Any | None:
            if data is None:
                return data
            return cast(Any | None, data)

        result = _parse_result(d.pop("result"))


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




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


        ai_operation_dto = cls(
            id=id,
            type_=type_,
            status=status,
            version_id=version_id,
            result=result,
            error_message=error_message,
            created_at=created_at,
            completed_at=completed_at,
        )

        return ai_operation_dto

