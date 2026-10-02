from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_dto_properties_scope_system_level import RunConfigDtoPropertiesScopeSystemLevel






T = TypeVar("T", bound="RunConfigDtoPropertiesScopeSystem")



@_attrs_define
class RunConfigDtoPropertiesScopeSystem:
    """ System-wide scope — owned by the platform, visible to all organizations.

        Attributes:
            level (RunConfigDtoPropertiesScopeSystemLevel): Discriminator: scope is platform-wide.
            id (None): Always null for system scope (no owning resource).
     """

    level: RunConfigDtoPropertiesScopeSystemLevel
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
        level = RunConfigDtoPropertiesScopeSystemLevel(d.pop("level"))




        id = d.pop("id")

        run_config_dto_properties_scope_system = cls(
            level=level,
            id=id,
        )

        return run_config_dto_properties_scope_system

