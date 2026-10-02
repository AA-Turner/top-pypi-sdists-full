from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_list_item_list_dto_items_properties_scope_system_level import RunConfigListItemListDtoItemsPropertiesScopeSystemLevel






T = TypeVar("T", bound="RunConfigListItemListDtoItemsPropertiesScopeSystem")



@_attrs_define
class RunConfigListItemListDtoItemsPropertiesScopeSystem:
    """ System-wide scope — owned by the platform, visible to all organizations.

        Attributes:
            level (RunConfigListItemListDtoItemsPropertiesScopeSystemLevel): Discriminator: scope is platform-wide.
            id (None): Always null for system scope (no owning resource).
     """

    level: RunConfigListItemListDtoItemsPropertiesScopeSystemLevel
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
        level = RunConfigListItemListDtoItemsPropertiesScopeSystemLevel(d.pop("level"))




        id = d.pop("id")

        run_config_list_item_list_dto_items_properties_scope_system = cls(
            level=level,
            id=id,
        )

        return run_config_list_item_list_dto_items_properties_scope_system

