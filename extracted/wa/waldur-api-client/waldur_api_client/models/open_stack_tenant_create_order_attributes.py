from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_tenant_security_group_request import OpenStackTenantSecurityGroupRequest


T = TypeVar("T", bound="OpenStackTenantCreateOrderAttributes")


@_attrs_define
class OpenStackTenantCreateOrderAttributes:
    """
    Attributes:
        name (str):
        description (Union[Unset, str]):
        subnet_cidr (Union[Unset, str]):  Default: '192.168.42.0/24'.
        skip_connection_extnet (Union[Unset, bool]):  Default: False.
        skip_creation_of_default_router (Union[Unset, bool]):  Default: False.
        skip_creation_of_default_subnet (Union[Unset, bool]):  Default: False.
        availability_zone (Union[Unset, str]): Optional availability group. Will be used for all instances provisioned
            in this tenant
        security_groups (Union[Unset, list['OpenStackTenantSecurityGroupRequest']]):
    """

    name: str
    description: Union[Unset, str] = UNSET
    subnet_cidr: Union[Unset, str] = "192.168.42.0/24"
    skip_connection_extnet: Union[Unset, bool] = False
    skip_creation_of_default_router: Union[Unset, bool] = False
    skip_creation_of_default_subnet: Union[Unset, bool] = False
    availability_zone: Union[Unset, str] = UNSET
    security_groups: Union[Unset, list["OpenStackTenantSecurityGroupRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        subnet_cidr = self.subnet_cidr

        skip_connection_extnet = self.skip_connection_extnet

        skip_creation_of_default_router = self.skip_creation_of_default_router

        skip_creation_of_default_subnet = self.skip_creation_of_default_subnet

        availability_zone = self.availability_zone

        security_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.security_groups, Unset):
            security_groups = []
            for security_groups_item_data in self.security_groups:
                security_groups_item = security_groups_item_data.to_dict()
                security_groups.append(security_groups_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if subnet_cidr is not UNSET:
            field_dict["subnet_cidr"] = subnet_cidr
        if skip_connection_extnet is not UNSET:
            field_dict["skip_connection_extnet"] = skip_connection_extnet
        if skip_creation_of_default_router is not UNSET:
            field_dict["skip_creation_of_default_router"] = skip_creation_of_default_router
        if skip_creation_of_default_subnet is not UNSET:
            field_dict["skip_creation_of_default_subnet"] = skip_creation_of_default_subnet
        if availability_zone is not UNSET:
            field_dict["availability_zone"] = availability_zone
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_tenant_security_group_request import OpenStackTenantSecurityGroupRequest

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        subnet_cidr = d.pop("subnet_cidr", UNSET)

        skip_connection_extnet = d.pop("skip_connection_extnet", UNSET)

        skip_creation_of_default_router = d.pop("skip_creation_of_default_router", UNSET)

        skip_creation_of_default_subnet = d.pop("skip_creation_of_default_subnet", UNSET)

        availability_zone = d.pop("availability_zone", UNSET)

        security_groups = []
        _security_groups = d.pop("security_groups", UNSET)
        for security_groups_item_data in _security_groups or []:
            security_groups_item = OpenStackTenantSecurityGroupRequest.from_dict(security_groups_item_data)

            security_groups.append(security_groups_item)

        open_stack_tenant_create_order_attributes = cls(
            name=name,
            description=description,
            subnet_cidr=subnet_cidr,
            skip_connection_extnet=skip_connection_extnet,
            skip_creation_of_default_router=skip_creation_of_default_router,
            skip_creation_of_default_subnet=skip_creation_of_default_subnet,
            availability_zone=availability_zone,
            security_groups=security_groups,
        )

        open_stack_tenant_create_order_attributes.additional_properties = d
        return open_stack_tenant_create_order_attributes

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
