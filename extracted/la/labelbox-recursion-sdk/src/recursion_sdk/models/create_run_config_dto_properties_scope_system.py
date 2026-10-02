from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_run_config_dto_properties_scope_system_level import CreateRunConfigDtoPropertiesScopeSystemLevel






T = TypeVar("T", bound="CreateRunConfigDtoPropertiesScopeSystem")



@_attrs_define
class CreateRunConfigDtoPropertiesScopeSystem:
    """ System-wide scope — owned by the platform, visible to all organizations.

        Attributes:
            level (CreateRunConfigDtoPropertiesScopeSystemLevel): Discriminator: scope is platform-wide.
            id (None): Always null for system scope (no owning resource).
     """

    level: CreateRunConfigDtoPropertiesScopeSystemLevel
    id: None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        id = self.id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "level": level,
            "id": id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        level = CreateRunConfigDtoPropertiesScopeSystemLevel(d.pop("level"))




        id = d.pop("id")

        create_run_config_dto_properties_scope_system = cls(
            level=level,
            id=id,
        )


        create_run_config_dto_properties_scope_system.additional_properties = d
        return create_run_config_dto_properties_scope_system

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
