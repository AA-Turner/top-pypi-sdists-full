from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.attach_run_config_file_dto_mode import AttachRunConfigFileDtoMode
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="AttachRunConfigFileDto")



@_attrs_define
class AttachRunConfigFileDto:
    """ Input for attaching an uploaded file to a draft run-config version.

        Attributes:
            file_id (UUID): Identifier of the already-uploaded file object to attach.
            mount_dir (str | Unset): Directory the file mounts under. Defaults to /workspace when omitted.
            mode (AttachRunConfigFileDtoMode | Unset): Mount mode. Defaults to read-only when omitted.
     """

    file_id: UUID
    mount_dir: str | Unset = UNSET
    mode: AttachRunConfigFileDtoMode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_id = str(self.file_id)

        mount_dir = self.mount_dir

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fileId": file_id,
        })
        if mount_dir is not UNSET:
            field_dict["mountDir"] = mount_dir
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = UUID(d.pop("fileId"))




        mount_dir = d.pop("mountDir", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: AttachRunConfigFileDtoMode | Unset
        if isinstance(_mode,  Unset):
            mode = UNSET
        else:
            mode = AttachRunConfigFileDtoMode(_mode)




        attach_run_config_file_dto = cls(
            file_id=file_id,
            mount_dir=mount_dir,
            mode=mode,
        )


        attach_run_config_file_dto.additional_properties = d
        return attach_run_config_file_dto

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
