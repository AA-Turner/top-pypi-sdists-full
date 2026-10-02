from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_run_config_file_dto_mode import UpdateRunConfigFileDtoMode
from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateRunConfigFileDto")



@_attrs_define
class UpdateRunConfigFileDto:
    """ Patch-style update for a run-config file attachment (mount directory and/or mode).

        Attributes:
            mount_dir (str | Unset): New mount directory. Omit to leave unchanged.
            mode (UpdateRunConfigFileDtoMode | Unset): New mount mode. Omit to leave unchanged.
     """

    mount_dir: str | Unset = UNSET
    mode: UpdateRunConfigFileDtoMode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mount_dir = self.mount_dir

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if mount_dir is not UNSET:
            field_dict["mountDir"] = mount_dir
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mount_dir = d.pop("mountDir", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: UpdateRunConfigFileDtoMode | Unset
        if isinstance(_mode,  Unset):
            mode = UNSET
        else:
            mode = UpdateRunConfigFileDtoMode(_mode)




        update_run_config_file_dto = cls(
            mount_dir=mount_dir,
            mode=mode,
        )


        update_run_config_file_dto.additional_properties = d
        return update_run_config_file_dto

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
