from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.customer_secret_dto_properties_scope_problem_level import CustomerSecretDtoPropertiesScopeProblemLevel
from uuid import UUID






T = TypeVar("T", bound="CustomerSecretDtoPropertiesScopeProblem")



@_attrs_define
class CustomerSecretDtoPropertiesScopeProblem:
    """ 
        Attributes:
            level (CustomerSecretDtoPropertiesScopeProblemLevel): Problem-scoped secret available within one problem.
            id (UUID): Problem that owns the secret.
     """

    level: CustomerSecretDtoPropertiesScopeProblemLevel
    id: UUID





    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        id = str(self.id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "level": level,
            "id": id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        level = CustomerSecretDtoPropertiesScopeProblemLevel(d.pop("level"))




        id = UUID(d.pop("id"))




        customer_secret_dto_properties_scope_problem = cls(
            level=level,
            id=id,
        )

        return customer_secret_dto_properties_scope_problem

