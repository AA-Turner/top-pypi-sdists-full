from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="AttachSynthesizerJobFileBodyDto")



@_attrs_define
class AttachSynthesizerJobFileBodyDto:
    """ Payload for attaching an existing uploaded file to a synthesizer job at a given mount path.

        Example:
            {'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951', 'mountPath': '/workspace/files/style-guide.md'}

        Attributes:
            file_id (UUID): Stable file identifier (UUID). Files are problem-scoped uploads.
            mount_path (str): Absolute container path where the file is mounted. Must avoid reserved tarball paths used by
                the synthesizer engine.
     """

    file_id: UUID
    mount_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_id = str(self.file_id)

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fileId": file_id,
            "mountPath": mount_path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = UUID(d.pop("fileId"))




        mount_path = d.pop("mountPath")

        attach_synthesizer_job_file_body_dto = cls(
            file_id=file_id,
            mount_path=mount_path,
        )


        attach_synthesizer_job_file_body_dto.additional_properties = d
        return attach_synthesizer_job_file_body_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
