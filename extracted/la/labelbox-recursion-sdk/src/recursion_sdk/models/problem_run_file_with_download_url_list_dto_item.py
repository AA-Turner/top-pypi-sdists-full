from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_run_file_with_download_url_list_dto_item_type import ProblemRunFileWithDownloadUrlListDtoItemType
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ProblemRunFileWithDownloadUrlListDtoItem")



@_attrs_define
class ProblemRunFileWithDownloadUrlListDtoItem:
    """ Output file produced by one problem run, flattened with a ready-to-use signed download URL.

        Attributes:
            id (UUID): Stable problem-run-file association identifier (UUID). Outputs produced by a single problem run.
            problem_run_id (UUID): Problem run this output file was produced by.
            file_id (UUID): Underlying file storing the output bytes.
            type_ (ProblemRunFileWithDownloadUrlListDtoItemType): Problem-run files carry persisted solver or grader
                outputs.
            created_at (datetime.datetime): Timestamp when the output file was recorded (ISO-8601, UTC).
            filename (str): Original filename to surface to download clients.
            path (None | str): Path of the file relative to the run's output directory (e.g. core/report.md). Null for files
                recorded before paths were captured.
            download_url (str): Signed download URL for the output file contents.
     """

    id: UUID
    problem_run_id: UUID
    file_id: UUID
    type_: ProblemRunFileWithDownloadUrlListDtoItemType
    created_at: datetime.datetime
    filename: str
    path: None | str
    download_url: str





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        problem_run_id = str(self.problem_run_id)

        file_id = str(self.file_id)

        type_ = self.type_.value

        created_at = self.created_at.isoformat()

        filename = self.filename

        path: None | str
        path = self.path

        download_url = self.download_url


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "problemRunId": problem_run_id,
            "fileId": file_id,
            "type": type_,
            "createdAt": created_at,
            "filename": filename,
            "path": path,
            "downloadUrl": download_url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        problem_run_id = UUID(d.pop("problemRunId"))




        file_id = UUID(d.pop("fileId"))




        type_ = ProblemRunFileWithDownloadUrlListDtoItemType(d.pop("type"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        filename = d.pop("filename")

        def _parse_path(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        path = _parse_path(d.pop("path"))


        download_url = d.pop("downloadUrl")

        problem_run_file_with_download_url_list_dto_item = cls(
            id=id,
            problem_run_id=problem_run_id,
            file_id=file_id,
            type_=type_,
            created_at=created_at,
            filename=filename,
            path=path,
            download_url=download_url,
        )

        return problem_run_file_with_download_url_list_dto_item

