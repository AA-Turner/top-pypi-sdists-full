from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.rancher_role_scope_type import RancherRoleScopeType

T = TypeVar("T", bound="RoleTemplate")


@_attrs_define
class RoleTemplate:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str): Role internal name
        scope_type (RancherRoleScopeType):
        display_name (str): Role public name
        settings (str):
    """

    url: str
    uuid: UUID
    name: str
    scope_type: RancherRoleScopeType
    display_name: str
    settings: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        scope_type = self.scope_type.value

        display_name = self.display_name

        settings = self.settings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "scope_type": scope_type,
                "display_name": display_name,
                "settings": settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        scope_type = RancherRoleScopeType(d.pop("scope_type"))

        display_name = d.pop("display_name")

        settings = d.pop("settings")

        role_template = cls(
            url=url,
            uuid=uuid,
            name=name,
            scope_type=scope_type,
            display_name=display_name,
            settings=settings,
        )

        role_template.additional_properties = d
        return role_template

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
