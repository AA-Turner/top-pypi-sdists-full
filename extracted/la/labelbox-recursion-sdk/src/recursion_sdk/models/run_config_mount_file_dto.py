from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RunConfigMountFileDto")



@_attrs_define
class RunConfigMountFileDto:
    """ An agent-service file uploaded for use as a run-config mount source.

        Attributes:
            id (str): Agent-service file id; use directly as a mount source on a run-config payload.
            filename (str): Sanitized filename as stored by the agent service.
            size_bytes (float): Uploaded file size in bytes.
     """

    id: str
    filename: str
    size_bytes: float





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        filename = self.filename

        size_bytes = self.size_bytes


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "filename": filename,
            "sizeBytes": size_bytes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        filename = d.pop("filename")

        size_bytes = d.pop("sizeBytes")

        run_config_mount_file_dto = cls(
            id=id,
            filename=filename,
            size_bytes=size_bytes,
        )

        return run_config_mount_file_dto

