from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_allowed_address_pair_request import OpenStackAllowedAddressPairRequest
    from ..models.open_stack_fixed_ip_request import OpenStackFixedIpRequest
    from ..models.open_stack_port_nested_security_group_request import OpenStackPortNestedSecurityGroupRequest


T = TypeVar("T", bound="OpenStackPortRequest")


@_attrs_define
class OpenStackPortRequest:
    """
    Attributes:
        name (str):
        description (Union[Unset, str]):
        fixed_ips (Union[Unset, list['OpenStackFixedIpRequest']]):
        mac_address (Union[Unset, str]): MAC address of the port
        allowed_address_pairs (Union[Unset, list['OpenStackAllowedAddressPairRequest']]):
        target_tenant (Union[Unset, str]): Target tenant for shared network port creation. If not specified, defaults to
            network's tenant.
        network (Union[None, Unset, str]): Network to which this port belongs
        port_security_enabled (Union[Unset, bool]): If True, security groups and rules will be applied to this port
        security_groups (Union[Unset, list['OpenStackPortNestedSecurityGroupRequest']]):
    """

    name: str
    description: Union[Unset, str] = UNSET
    fixed_ips: Union[Unset, list["OpenStackFixedIpRequest"]] = UNSET
    mac_address: Union[Unset, str] = UNSET
    allowed_address_pairs: Union[Unset, list["OpenStackAllowedAddressPairRequest"]] = UNSET
    target_tenant: Union[Unset, str] = UNSET
    network: Union[None, Unset, str] = UNSET
    port_security_enabled: Union[Unset, bool] = UNSET
    security_groups: Union[Unset, list["OpenStackPortNestedSecurityGroupRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        fixed_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.fixed_ips, Unset):
            fixed_ips = []
            for fixed_ips_item_data in self.fixed_ips:
                fixed_ips_item = fixed_ips_item_data.to_dict()
                fixed_ips.append(fixed_ips_item)

        mac_address = self.mac_address

        allowed_address_pairs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.allowed_address_pairs, Unset):
            allowed_address_pairs = []
            for allowed_address_pairs_item_data in self.allowed_address_pairs:
                allowed_address_pairs_item = allowed_address_pairs_item_data.to_dict()
                allowed_address_pairs.append(allowed_address_pairs_item)

        target_tenant = self.target_tenant

        network: Union[None, Unset, str]
        if isinstance(self.network, Unset):
            network = UNSET
        else:
            network = self.network

        port_security_enabled = self.port_security_enabled

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
        if fixed_ips is not UNSET:
            field_dict["fixed_ips"] = fixed_ips
        if mac_address is not UNSET:
            field_dict["mac_address"] = mac_address
        if allowed_address_pairs is not UNSET:
            field_dict["allowed_address_pairs"] = allowed_address_pairs
        if target_tenant is not UNSET:
            field_dict["target_tenant"] = target_tenant
        if network is not UNSET:
            field_dict["network"] = network
        if port_security_enabled is not UNSET:
            field_dict["port_security_enabled"] = port_security_enabled
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_allowed_address_pair_request import OpenStackAllowedAddressPairRequest
        from ..models.open_stack_fixed_ip_request import OpenStackFixedIpRequest
        from ..models.open_stack_port_nested_security_group_request import OpenStackPortNestedSecurityGroupRequest

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        fixed_ips = []
        _fixed_ips = d.pop("fixed_ips", UNSET)
        for fixed_ips_item_data in _fixed_ips or []:
            fixed_ips_item = OpenStackFixedIpRequest.from_dict(fixed_ips_item_data)

            fixed_ips.append(fixed_ips_item)

        mac_address = d.pop("mac_address", UNSET)

        allowed_address_pairs = []
        _allowed_address_pairs = d.pop("allowed_address_pairs", UNSET)
        for allowed_address_pairs_item_data in _allowed_address_pairs or []:
            allowed_address_pairs_item = OpenStackAllowedAddressPairRequest.from_dict(allowed_address_pairs_item_data)

            allowed_address_pairs.append(allowed_address_pairs_item)

        target_tenant = d.pop("target_tenant", UNSET)

        def _parse_network(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        network = _parse_network(d.pop("network", UNSET))

        port_security_enabled = d.pop("port_security_enabled", UNSET)

        security_groups = []
        _security_groups = d.pop("security_groups", UNSET)
        for security_groups_item_data in _security_groups or []:
            security_groups_item = OpenStackPortNestedSecurityGroupRequest.from_dict(security_groups_item_data)

            security_groups.append(security_groups_item)

        open_stack_port_request = cls(
            name=name,
            description=description,
            fixed_ips=fixed_ips,
            mac_address=mac_address,
            allowed_address_pairs=allowed_address_pairs,
            target_tenant=target_tenant,
            network=network,
            port_security_enabled=port_security_enabled,
            security_groups=security_groups,
        )

        open_stack_port_request.additional_properties = d
        return open_stack_port_request

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
