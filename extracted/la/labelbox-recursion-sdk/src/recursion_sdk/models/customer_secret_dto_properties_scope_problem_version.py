from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.customer_secret_dto_properties_scope_problem_version_level import CustomerSecretDtoPropertiesScopeProblemVersionLevel
from uuid import UUID






T = TypeVar("T", bound="CustomerSecretDtoPropertiesScopeProblemVersion")



@_attrs_define
class CustomerSecretDtoPropertiesScopeProblemVersion:
    """ 
        Attributes:
            level (CustomerSecretDtoPropertiesScopeProblemVersionLevel): Problem-version-scoped secret pinned to one
                specific problem version.
            id (UUID): Problem version that owns the secret.
     """

    level: CustomerSecretDtoPropertiesScopeProblemVersionLevel
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
        level = CustomerSecretDtoPropertiesScopeProblemVersionLevel(d.pop("level"))




        id = UUID(d.pop("id"))




        customer_secret_dto_properties_scope_problem_version = cls(
            level=level,
            id=id,
        )

        return customer_secret_dto_properties_scope_problem_version

