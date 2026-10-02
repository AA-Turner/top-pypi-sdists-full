from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.customer_secret_list_dto_items_properties_scope_system_level import CustomerSecretListDtoItemsPropertiesScopeSystemLevel






T = TypeVar("T", bound="CustomerSecretListDtoItemsPropertiesScopeSystem")



@_attrs_define
class CustomerSecretListDtoItemsPropertiesScopeSystem:
    """ 
        Attributes:
            level (CustomerSecretListDtoItemsPropertiesScopeSystemLevel): System-wide secret available to every
                organization.
            id (None): Always null at system scope.
     """

    level: CustomerSecretListDtoItemsPropertiesScopeSystemLevel
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
        level = CustomerSecretListDtoItemsPropertiesScopeSystemLevel(d.pop("level"))




        id = d.pop("id")

        customer_secret_list_dto_items_properties_scope_system = cls(
            level=level,
            id=id,
        )

        return customer_secret_list_dto_items_properties_scope_system

