from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_run_config_dto_properties_scope_org_level import CreateRunConfigDtoPropertiesScopeOrgLevel
from uuid import UUID






T = TypeVar("T", bound="CreateRunConfigDtoPropertiesScopeOrg")



@_attrs_define
class CreateRunConfigDtoPropertiesScopeOrg:
    """ Organization-level scope — visible to every environment in the organization.

        Attributes:
            level (CreateRunConfigDtoPropertiesScopeOrgLevel): Discriminator: scope is an organization.
            id (UUID): Organization that owns this scope.
     """

    level: CreateRunConfigDtoPropertiesScopeOrgLevel
    id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        id = str(self.id)


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
        level = CreateRunConfigDtoPropertiesScopeOrgLevel(d.pop("level"))




        id = UUID(d.pop("id"))




        create_run_config_dto_properties_scope_org = cls(
            level=level,
            id=id,
        )


        create_run_config_dto_properties_scope_org.additional_properties = d
        return create_run_config_dto_properties_scope_org

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
