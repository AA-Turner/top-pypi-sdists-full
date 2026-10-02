from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_version_file_list_dto_item_type import ProblemVersionFileListDtoItemType
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.problem_version_file_list_dto_item_file import ProblemVersionFileListDtoItemFile





T = TypeVar("T", bound="ProblemVersionFileListDtoItem")



@_attrs_define
class ProblemVersionFileListDtoItem:
    """ An attachment of an environment-scoped file to a specific problem version, with its role and tags.

        Attributes:
            id (UUID): Stable problem-version-file association identifier (UUID).
            problem_version_id (UUID): Problem version this file is attached to.
            file_id (UUID): Underlying file that this attachment points at.
            type_ (ProblemVersionFileListDtoItemType): Role of the attached file: solver-visible input, reference material,
                or grader-only assets such as expected outputs.
            created_at (datetime.datetime): Timestamp when the file was attached to the problem version (ISO-8601, UTC).
            file (ProblemVersionFileListDtoItemFile): Materialized file record, included so consumers do not need a second
                fetch.
            is_gold_standard (bool): When true, the file is mounted inside the grader container at the configured mount path
                as a gold-standard reference.
            gold_standard_mount_path (None | str): Container mount path for the gold-standard reference. Null when the file
                is not gold-standard.
            tags (list[str]): User-defined tags that drive format-specific placement in exports.
     """

    id: UUID
    problem_version_id: UUID
    file_id: UUID
    type_: ProblemVersionFileListDtoItemType
    created_at: datetime.datetime
    file: ProblemVersionFileListDtoItemFile
    is_gold_standard: bool
    gold_standard_mount_path: None | str
    tags: list[str]





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_version_file_list_dto_item_file import ProblemVersionFileListDtoItemFile # noqa: PLC0415
        id = str(self.id)

        problem_version_id = str(self.problem_version_id)

        file_id = str(self.file_id)

        type_ = self.type_.value

        created_at = self.created_at.isoformat()

        file = self.file.to_dict()

        is_gold_standard = self.is_gold_standard

        gold_standard_mount_path: None | str
        gold_standard_mount_path = self.gold_standard_mount_path

        tags = self.tags




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "problemVersionId": problem_version_id,
            "fileId": file_id,
            "type": type_,
            "createdAt": created_at,
            "file": file,
            "isGoldStandard": is_gold_standard,
            "goldStandardMountPath": gold_standard_mount_path,
            "tags": tags,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_version_file_list_dto_item_file import ProblemVersionFileListDtoItemFile # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        problem_version_id = UUID(d.pop("problemVersionId"))




        file_id = UUID(d.pop("fileId"))




        type_ = ProblemVersionFileListDtoItemType(d.pop("type"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        file = ProblemVersionFileListDtoItemFile.from_dict(d.pop("file"))




        is_gold_standard = d.pop("isGoldStandard")

        def _parse_gold_standard_mount_path(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gold_standard_mount_path = _parse_gold_standard_mount_path(d.pop("goldStandardMountPath"))


        tags = cast(list[str], d.pop("tags"))


        problem_version_file_list_dto_item = cls(
            id=id,
            problem_version_id=problem_version_id,
            file_id=file_id,
            type_=type_,
            created_at=created_at,
            file=file,
            is_gold_standard=is_gold_standard,
            gold_standard_mount_path=gold_standard_mount_path,
            tags=tags,
        )

        return problem_version_file_list_dto_item

