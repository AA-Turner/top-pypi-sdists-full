from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_file_dto_mode import RunConfigFileDtoMode
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="RunConfigFileDto")



@_attrs_define
class RunConfigFileDto:
    """ A file attached to a run-config version and mounted into the container workspace at run time.

        Attributes:
            file_id (UUID): Identifier of the underlying uploaded file object.
            filename (str): Original filename of the uploaded file; appended to the mount directory.
            size_bytes (float | None): Size of the file in bytes, or null when unknown.
            mount_dir (str): Directory inside the container workspace where the file mounts.
            mount_path (str): Resolved absolute container path the file mounts at (mountDir + / + filename).
            mode (RunConfigFileDtoMode): Mount mode — read-only or read-write.
            created_at (datetime.datetime): Timestamp when the file was attached to the version (ISO-8601, UTC).
     """

    file_id: UUID
    filename: str
    size_bytes: float | None
    mount_dir: str
    mount_path: str
    mode: RunConfigFileDtoMode
    created_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        file_id = str(self.file_id)

        filename = self.filename

        size_bytes: float | None
        size_bytes = self.size_bytes

        mount_dir = self.mount_dir

        mount_path = self.mount_path

        mode = self.mode.value

        created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "fileId": file_id,
            "filename": filename,
            "sizeBytes": size_bytes,
            "mountDir": mount_dir,
            "mountPath": mount_path,
            "mode": mode,
            "createdAt": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = UUID(d.pop("fileId"))




        filename = d.pop("filename")

        def _parse_size_bytes(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        size_bytes = _parse_size_bytes(d.pop("sizeBytes"))


        mount_dir = d.pop("mountDir")

        mount_path = d.pop("mountPath")

        mode = RunConfigFileDtoMode(d.pop("mode"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        run_config_file_dto = cls(
            file_id=file_id,
            filename=filename,
            size_bytes=size_bytes,
            mount_dir=mount_dir,
            mount_path=mount_path,
            mode=mode,
            created_at=created_at,
        )

        return run_config_file_dto

