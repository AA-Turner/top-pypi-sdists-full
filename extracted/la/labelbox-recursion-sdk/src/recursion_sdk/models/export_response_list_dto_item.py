from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.export_response_list_dto_item_format_type_0_type_0 import ExportResponseListDtoItemFormatType0Type0
from ..models.export_response_list_dto_item_kind import ExportResponseListDtoItemKind
from ..models.export_response_list_dto_item_status import ExportResponseListDtoItemStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.export_response_list_dto_item_evaluation_config_type_0 import ExportResponseListDtoItemEvaluationConfigType0





T = TypeVar("T", bound="ExportResponseListDtoItem")



@_attrs_define
class ExportResponseListDtoItem:
    """ An asynchronous export job and its progress, downloadable artifact, and persisted configuration.

        Attributes:
            id (UUID): Stable export-job identifier (UUID).
            kind (ExportResponseListDtoItemKind): Discriminator selecting which scope identifier applies to this export.
            environment_id (None | UUID): Environment that owns the export. Set for problem-archive exports; null otherwise.
            evaluation_id (None | UUID): Evaluation the export is scoped to. Set for evaluation-results exports; null
                otherwise.
            user_id (UUID): User who created the export job.
            status (ExportResponseListDtoItemStatus): Current lifecycle status of the export job.
            format_ (ExportResponseListDtoItemFormatType0Type0 | None | str): Archive format for problem-archive exports.
                Null for other export kinds, which carry their own format dimension.
            total_problems (int): Total work units to process. Semantics depend on kind — see ExportKind for per-kind
                details. Example: 100.
            processed_problems (int): Work units processed so far, in the same unit as the total. Example: 42.
            download_url (None | str): Signed download URL for the produced artifact. Null until the job completes.
            file_size_bytes (float | None): Size of the produced artifact in bytes. Null until the job completes. Example:
                1048576.
            error_message (None | str): Failure reason when the job ended in failure. Null otherwise.
            started_at (datetime.datetime | None): Timestamp when the job began processing (ISO-8601, UTC). Null while
                pending.
            completed_at (datetime.datetime | None): Timestamp when the job reached a terminal state (ISO-8601, UTC). Null
                until the job ends.
            created_at (datetime.datetime): Timestamp when the export job was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the export job row was last updated (ISO-8601, UTC).
            evaluation_config (ExportResponseListDtoItemEvaluationConfigType0 | None): Persisted configuration for
                evaluation-results exports, capturing format, included columns, and filters. Null for other export kinds.
     """

    id: UUID
    kind: ExportResponseListDtoItemKind
    environment_id: None | UUID
    evaluation_id: None | UUID
    user_id: UUID
    status: ExportResponseListDtoItemStatus
    format_: ExportResponseListDtoItemFormatType0Type0 | None | str
    total_problems: int
    processed_problems: int
    download_url: None | str
    file_size_bytes: float | None
    error_message: None | str
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    evaluation_config: ExportResponseListDtoItemEvaluationConfigType0 | None





    def to_dict(self) -> dict[str, Any]:
        from ..models.export_response_list_dto_item_evaluation_config_type_0 import ExportResponseListDtoItemEvaluationConfigType0 # noqa: PLC0415
        id = str(self.id)

        kind = self.kind.value

        environment_id: None | str
        if isinstance(self.environment_id, UUID):
            environment_id = str(self.environment_id)
        else:
            environment_id = self.environment_id

        evaluation_id: None | str
        if isinstance(self.evaluation_id, UUID):
            evaluation_id = str(self.evaluation_id)
        else:
            evaluation_id = self.evaluation_id

        user_id = str(self.user_id)

        status = self.status.value

        format_: None | str
        if isinstance(self.format_, ExportResponseListDtoItemFormatType0Type0):
            format_ = self.format_.value
        else:
            format_ = self.format_

        total_problems = self.total_problems

        processed_problems = self.processed_problems

        download_url: None | str
        download_url = self.download_url

        file_size_bytes: float | None
        file_size_bytes = self.file_size_bytes

        error_message: None | str
        error_message = self.error_message

        started_at: None | str
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        evaluation_config: dict[str, Any] | None
        if isinstance(self.evaluation_config, ExportResponseListDtoItemEvaluationConfigType0):
            evaluation_config = self.evaluation_config.to_dict()
        else:
            evaluation_config = self.evaluation_config


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "kind": kind,
            "environmentId": environment_id,
            "evaluationId": evaluation_id,
            "userId": user_id,
            "status": status,
            "format": format_,
            "totalProblems": total_problems,
            "processedProblems": processed_problems,
            "downloadUrl": download_url,
            "fileSizeBytes": file_size_bytes,
            "errorMessage": error_message,
            "startedAt": started_at,
            "completedAt": completed_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "evaluationConfig": evaluation_config,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.export_response_list_dto_item_evaluation_config_type_0 import ExportResponseListDtoItemEvaluationConfigType0 # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        kind = ExportResponseListDtoItemKind(d.pop("kind"))




        def _parse_environment_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                environment_id_type_0 = UUID(data)



                return environment_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        environment_id = _parse_environment_id(d.pop("environmentId"))


        def _parse_evaluation_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                evaluation_id_type_0 = UUID(data)



                return evaluation_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        evaluation_id = _parse_evaluation_id(d.pop("evaluationId"))


        user_id = UUID(d.pop("userId"))




        status = ExportResponseListDtoItemStatus(d.pop("status"))




        def _parse_format_(data: object) -> ExportResponseListDtoItemFormatType0Type0 | None | str:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                format_type_0_type_0 = ExportResponseListDtoItemFormatType0Type0(data)



                return format_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExportResponseListDtoItemFormatType0Type0 | None | str, data)

        format_ = _parse_format_(d.pop("format"))


        total_problems = d.pop("totalProblems")

        processed_problems = d.pop("processedProblems")

        def _parse_download_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        download_url = _parse_download_url(d.pop("downloadUrl"))


        def _parse_file_size_bytes(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        file_size_bytes = _parse_file_size_bytes(d.pop("fileSizeBytes"))


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        def _parse_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = datetime.datetime.fromisoformat(data)



                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        started_at = _parse_started_at(d.pop("startedAt"))


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


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        def _parse_evaluation_config(data: object) -> ExportResponseListDtoItemEvaluationConfigType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                evaluation_config_type_0 = ExportResponseListDtoItemEvaluationConfigType0.from_dict(data)



                return evaluation_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExportResponseListDtoItemEvaluationConfigType0 | None, data)

        evaluation_config = _parse_evaluation_config(d.pop("evaluationConfig"))


        export_response_list_dto_item = cls(
            id=id,
            kind=kind,
            environment_id=environment_id,
            evaluation_id=evaluation_id,
            user_id=user_id,
            status=status,
            format_=format_,
            total_problems=total_problems,
            processed_problems=processed_problems,
            download_url=download_url,
            file_size_bytes=file_size_bytes,
            error_message=error_message,
            started_at=started_at,
            completed_at=completed_at,
            created_at=created_at,
            updated_at=updated_at,
            evaluation_config=evaluation_config,
        )

        return export_response_list_dto_item

