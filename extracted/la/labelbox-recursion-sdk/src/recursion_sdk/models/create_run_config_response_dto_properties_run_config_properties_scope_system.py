from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_run_config_response_dto_properties_run_config_properties_scope_system_level import CreateRunConfigResponseDtoPropertiesRunConfigPropertiesScopeSystemLevel






T = TypeVar("T", bound="CreateRunConfigResponseDtoPropertiesRunConfigPropertiesScopeSystem")



@_attrs_define
class CreateRunConfigResponseDtoPropertiesRunConfigPropertiesScopeSystem:
    """ System-wide scope — owned by the platform, visible to all organizations.

        Attributes:
            level (CreateRunConfigResponseDtoPropertiesRunConfigPropertiesScopeSystemLevel): Discriminator: scope is
                platform-wide.
            id (None): Always null for system scope (no owning resource).
     """

    level: CreateRunConfigResponseDtoPropertiesRunConfigPropertiesScopeSystemLevel
    id: None





    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        id = self.id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "level": level,
            "id": id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        level = CreateRunConfigResponseDtoPropertiesRunConfigPropertiesScopeSystemLevel(d.pop("level"))




        id = d.pop("id")

        create_run_config_response_dto_properties_run_config_properties_scope_system = cls(
            level=level,
            id=id,
        )

        return create_run_config_response_dto_properties_run_config_properties_scope_system

