from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.set_datatable_permissions_json_body_roles_item import SetDatatablePermissionsJsonBodyRolesItem


T = TypeVar("T", bound="SetDatatablePermissionsJsonBody")


@_attrs_define
class SetDatatablePermissionsJsonBody:
    """
    Attributes:
        permissioned (bool):
        default_role (Union[Unset, str]):
        roles (Union[Unset, List['SetDatatablePermissionsJsonBodyRolesItem']]):
    """

    permissioned: bool
    default_role: Union[Unset, str] = UNSET
    roles: Union[Unset, List["SetDatatablePermissionsJsonBodyRolesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        permissioned = self.permissioned
        default_role = self.default_role
        roles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = []
            for roles_item_data in self.roles:
                roles_item = roles_item_data.to_dict()

                roles.append(roles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "permissioned": permissioned,
            }
        )
        if default_role is not UNSET:
            field_dict["default_role"] = default_role
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.set_datatable_permissions_json_body_roles_item import SetDatatablePermissionsJsonBodyRolesItem

        d = src_dict.copy()
        permissioned = d.pop("permissioned")

        default_role = d.pop("default_role", UNSET)

        roles = []
        _roles = d.pop("roles", UNSET)
        for roles_item_data in _roles or []:
            roles_item = SetDatatablePermissionsJsonBodyRolesItem.from_dict(roles_item_data)

            roles.append(roles_item)

        set_datatable_permissions_json_body = cls(
            permissioned=permissioned,
            default_role=default_role,
            roles=roles,
        )

        set_datatable_permissions_json_body.additional_properties = d
        return set_datatable_permissions_json_body

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
