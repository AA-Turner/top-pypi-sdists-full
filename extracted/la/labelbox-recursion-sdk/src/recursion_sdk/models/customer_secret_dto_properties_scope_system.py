from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.customer_secret_dto_properties_scope_system_level import CustomerSecretDtoPropertiesScopeSystemLevel






T = TypeVar("T", bound="CustomerSecretDtoPropertiesScopeSystem")



@_attrs_define
class CustomerSecretDtoPropertiesScopeSystem:
    """ 
        Attributes:
            level (CustomerSecretDtoPropertiesScopeSystemLevel): System-wide secret available to every organization.
            id (None): Always null at system scope.
     """

    level: CustomerSecretDtoPropertiesScopeSystemLevel
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
        level = CustomerSecretDtoPropertiesScopeSystemLevel(d.pop("level"))




        id = d.pop("id")

        customer_secret_dto_properties_scope_system = cls(
            level=level,
            id=id,
        )

        return customer_secret_dto_properties_scope_system

