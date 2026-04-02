from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_port_nested_security_group_request import OpenStackPortNestedSecurityGroupRequest


T = TypeVar("T", bound="PatchedOpenStackPortRequest")


@_attrs_define
class PatchedOpenStackPortRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        target_tenant (Union[Unset, str]): Target tenant for shared network port creation. If not specified, defaults to
            network's tenant.
        security_groups (Union[Unset, list['OpenStackPortNestedSecurityGroupRequest']]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    target_tenant: Union[Unset, str] = UNSET
    security_groups: Union[Unset, list["OpenStackPortNestedSecurityGroupRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        target_tenant = self.target_tenant

        security_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.security_groups, Unset):
            security_groups = []
            for security_groups_item_data in self.security_groups:
                security_groups_item = security_groups_item_data.to_dict()
                security_groups.append(security_groups_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if target_tenant is not UNSET:
            field_dict["target_tenant"] = target_tenant
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_port_nested_security_group_request import OpenStackPortNestedSecurityGroupRequest

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        target_tenant = d.pop("target_tenant", UNSET)

        security_groups = []
        _security_groups = d.pop("security_groups", UNSET)
        for security_groups_item_data in _security_groups or []:
            security_groups_item = OpenStackPortNestedSecurityGroupRequest.from_dict(security_groups_item_data)

            security_groups.append(security_groups_item)

        patched_open_stack_port_request = cls(
            name=name,
            description=description,
            target_tenant=target_tenant,
            security_groups=security_groups,
        )

        patched_open_stack_port_request.additional_properties = d
        return patched_open_stack_port_request

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
