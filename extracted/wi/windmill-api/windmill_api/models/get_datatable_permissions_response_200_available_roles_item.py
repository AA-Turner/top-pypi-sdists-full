from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetDatatablePermissionsResponse200AvailableRolesItem")


@_attrs_define
class GetDatatablePermissionsResponse200AvailableRolesItem:
    """
    Attributes:
        id (str):
        name (str):
        enabled (bool):
    """

    id: str
    name: str
    enabled: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "enabled": enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        enabled = d.pop("enabled")

        get_datatable_permissions_response_200_available_roles_item = cls(
            id=id,
            name=name,
            enabled=enabled,
        )

        get_datatable_permissions_response_200_available_roles_item.additional_properties = d
        return get_datatable_permissions_response_200_available_roles_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
