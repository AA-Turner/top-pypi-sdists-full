from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.import_response_list_dto_item_format import ImportResponseListDtoItemFormat
from ..models.import_response_list_dto_item_status import ImportResponseListDtoItemStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.import_response_list_dto_item_errors_item import ImportResponseListDtoItemErrorsItem





T = TypeVar("T", bound="ImportResponseListDtoItem")



@_attrs_define
class ImportResponseListDtoItem:
    """ An asynchronous import job and its progress, per-row errors, and lifecycle timestamps.

        Attributes:
            id (UUID): Stable import-job identifier (UUID).
            environment_id (UUID): Environment the import job targets.
            user_id (UUID): User who initiated the import.
            status (ImportResponseListDtoItemStatus): Current lifecycle status of the import job.
            format_ (ImportResponseListDtoItemFormat): Detected wire format of the uploaded archive.
            assign_external_ids (bool): Whether this import assigns the archive's external IDs to the imported problems.
            total_problems (int): Total number of problems detected in the archive. Example: 100.
            processed_problems (int): Problems the processor has finished examining so far. Example: 42.
            created_problems (int): Problems newly created in the environment by this import. Example: 35.
            skipped_problems (int): Problems skipped because they already existed and matched an existing row. Example: 5.
            failed_problems (int): Problems that failed to import. Example: 2.
            error_message (None | str): Top-level failure reason when the job ended in a failed state; null otherwise.
            errors (list[ImportResponseListDtoItemErrorsItem]): Per-row errors and warnings captured during import.
            started_at (datetime.datetime | None): Timestamp when the job started processing (ISO-8601, UTC); null while
                pending.
            completed_at (datetime.datetime | None): Timestamp when the job reached a terminal state (ISO-8601, UTC); null
                until the job ends.
            created_at (datetime.datetime): Timestamp when the import job was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the import job row was last updated (ISO-8601, UTC).
     """

    id: UUID
    environment_id: UUID
    user_id: UUID
    status: ImportResponseListDtoItemStatus
    format_: ImportResponseListDtoItemFormat
    assign_external_ids: bool
    total_problems: int
    processed_problems: int
    created_problems: int
    skipped_problems: int
    failed_problems: int
    error_message: None | str
    errors: list[ImportResponseListDtoItemErrorsItem]
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.import_response_list_dto_item_errors_item import ImportResponseListDtoItemErrorsItem # noqa: PLC0415
        id = str(self.id)

        environment_id = str(self.environment_id)

        user_id = str(self.user_id)

        status = self.status.value

        format_ = self.format_.value

        assign_external_ids = self.assign_external_ids

        total_problems = self.total_problems

        processed_problems = self.processed_problems

        created_problems = self.created_problems

        skipped_problems = self.skipped_problems

        failed_problems = self.failed_problems

        error_message: None | str
        error_message = self.error_message

        errors = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()
            errors.append(errors_item)



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


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "userId": user_id,
            "status": status,
            "format": format_,
            "assignExternalIds": assign_external_ids,
            "totalProblems": total_problems,
            "processedProblems": processed_problems,
            "createdProblems": created_problems,
            "skippedProblems": skipped_problems,
            "failedProblems": failed_problems,
            "errorMessage": error_message,
            "errors": errors,
            "startedAt": started_at,
            "completedAt": completed_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.import_response_list_dto_item_errors_item import ImportResponseListDtoItemErrorsItem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        user_id = UUID(d.pop("userId"))




        status = ImportResponseListDtoItemStatus(d.pop("status"))




        format_ = ImportResponseListDtoItemFormat(d.pop("format"))




        assign_external_ids = d.pop("assignExternalIds")

        total_problems = d.pop("totalProblems")

        processed_problems = d.pop("processedProblems")

        created_problems = d.pop("createdProblems")

        skipped_problems = d.pop("skippedProblems")

        failed_problems = d.pop("failedProblems")

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        errors = []
        _errors = d.pop("errors")
        for errors_item_data in (_errors):
            errors_item = ImportResponseListDtoItemErrorsItem.from_dict(errors_item_data)



            errors.append(errors_item)


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




        import_response_list_dto_item = cls(
            id=id,
            environment_id=environment_id,
            user_id=user_id,
            status=status,
            format_=format_,
            assign_external_ids=assign_external_ids,
            total_problems=total_problems,
            processed_problems=processed_problems,
            created_problems=created_problems,
            skipped_problems=skipped_problems,
            failed_problems=failed_problems,
            error_message=error_message,
            errors=errors,
            started_at=started_at,
            completed_at=completed_at,
            created_at=created_at,
            updated_at=updated_at,
        )

        return import_response_list_dto_item

