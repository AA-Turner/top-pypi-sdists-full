from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_instance_groups_json_body_roles import EditInstanceGroupsJsonBodyRoles


T = TypeVar("T", bound="EditInstanceGroupsJsonBody")


@_attrs_define
class EditInstanceGroupsJsonBody:
    """
    Attributes:
        groups (Union[Unset, List[str]]):
        roles (Union[Unset, EditInstanceGroupsJsonBodyRoles]):
    """

    groups: Union[Unset, List[str]] = UNSET
    roles: Union[Unset, "EditInstanceGroupsJsonBodyRoles"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        roles: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if groups is not UNSET:
            field_dict["groups"] = groups
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_instance_groups_json_body_roles import EditInstanceGroupsJsonBodyRoles

        d = src_dict.copy()
        groups = cast(List[str], d.pop("groups", UNSET))

        _roles = d.pop("roles", UNSET)
        roles: Union[Unset, EditInstanceGroupsJsonBodyRoles]
        if isinstance(_roles, Unset):
            roles = UNSET
        else:
            roles = EditInstanceGroupsJsonBodyRoles.from_dict(_roles)

        edit_instance_groups_json_body = cls(
            groups=groups,
            roles=roles,
        )

        edit_instance_groups_json_body.additional_properties = d
        return edit_instance_groups_json_body

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
