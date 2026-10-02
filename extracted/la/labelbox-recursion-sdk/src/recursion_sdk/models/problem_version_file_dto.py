from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_version_file_dto_type import ProblemVersionFileDtoType
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.problem_version_file_dto_file import ProblemVersionFileDtoFile





T = TypeVar("T", bound="ProblemVersionFileDto")



@_attrs_define
class ProblemVersionFileDto:
    """ An attachment of an environment-scoped file to a specific problem version, with its role and tags.

        Example:
            {'id': 'adcdd7cb-10ed-432f-863e-88a9bacaca60', 'problemVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71',
                'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951', 'type': 'problem', 'createdAt': '2026-01-16T14:20:00.000Z',
                'file': {'id': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951', 'url': 'https://storage.googleapis.com/recursion-example-
                uploads/environments/784e2386-e297-4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-
                c7190a8c1951/dataset.jsonl?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Expires=900&X-Goog-
                Signature=4a1f9c2e7b5d3a8f0e6c1b9d2a4f7e3c8b5a0d6f1e9c2b4a7d3f8e5c0b6a1d9f', 'filename': 'dataset.jsonl',
                'sizeBytes': 1048576, 'createdAt': '2026-01-15T09:30:00.000Z', 'createdById':
                '49dea803-7390-49c4-abb1-5629718fc9cd'}, 'isGoldStandard': False, 'goldStandardMountPath': None, 'tags':
                ['tests']}

        Attributes:
            id (UUID): Stable problem-version-file association identifier (UUID).
            problem_version_id (UUID): Problem version this file is attached to.
            file_id (UUID): Underlying file that this attachment points at.
            type_ (ProblemVersionFileDtoType): Role of the attached file: solver-visible input, reference material, or
                grader-only assets such as expected outputs.
            created_at (datetime.datetime): Timestamp when the file was attached to the problem version (ISO-8601, UTC).
            file (ProblemVersionFileDtoFile): Materialized file record, included so consumers do not need a second fetch.
            is_gold_standard (bool): When true, the file is mounted inside the grader container at the configured mount path
                as a gold-standard reference.
            gold_standard_mount_path (None | str): Container mount path for the gold-standard reference. Null when the file
                is not gold-standard.
            tags (list[str]): User-defined tags that drive format-specific placement in exports.
     """

    id: UUID
    problem_version_id: UUID
    file_id: UUID
    type_: ProblemVersionFileDtoType
    created_at: datetime.datetime
    file: ProblemVersionFileDtoFile
    is_gold_standard: bool
    gold_standard_mount_path: None | str
    tags: list[str]





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_version_file_dto_file import ProblemVersionFileDtoFile # noqa: PLC0415
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
        from ..models.problem_version_file_dto_file import ProblemVersionFileDtoFile # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        problem_version_id = UUID(d.pop("problemVersionId"))




        file_id = UUID(d.pop("fileId"))




        type_ = ProblemVersionFileDtoType(d.pop("type"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        file = ProblemVersionFileDtoFile.from_dict(d.pop("file"))




        is_gold_standard = d.pop("isGoldStandard")

        def _parse_gold_standard_mount_path(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gold_standard_mount_path = _parse_gold_standard_mount_path(d.pop("goldStandardMountPath"))


        tags = cast(list[str], d.pop("tags"))


        problem_version_file_dto = cls(
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

        return problem_version_file_dto

