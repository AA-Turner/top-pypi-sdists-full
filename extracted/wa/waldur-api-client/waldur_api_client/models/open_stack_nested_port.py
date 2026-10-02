from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_allowed_address_pair import OpenStackAllowedAddressPair
    from ..models.open_stack_fixed_ip import OpenStackFixedIp
    from ..models.open_stack_security_group import OpenStackSecurityGroup


T = TypeVar("T", bound="OpenStackNestedPort")


@_attrs_define
class OpenStackNestedPort:
    """
    Attributes:
        url (Union[Unset, str]):
        fixed_ips (Union[Unset, list['OpenStackFixedIp']]):
        mac_address (Union[Unset, str]): MAC address of the port
        subnet (Union[None, Unset, str]): Subnet to which this port belongs
        subnet_uuid (Union[None, UUID, Unset]):
        subnet_name (Union[None, Unset, str]):
        subnet_description (Union[None, Unset, str]):
        subnet_cidr (Union[None, Unset, str]): IPv4 network address in CIDR format (e.g. 192.168.0.0/24)
        allowed_address_pairs (Union[Unset, list['OpenStackAllowedAddressPair']]):
        device_id (Union[None, Unset, str]): ID of device (instance, router etc) to which this port is connected
        device_owner (Union[None, Unset, str]): Entity that uses this port (e.g. network:router_interface)
        security_groups (Union[Unset, list['OpenStackSecurityGroup']]):
    """

    url: Union[Unset, str] = UNSET
    fixed_ips: Union[Unset, list["OpenStackFixedIp"]] = UNSET
    mac_address: Union[Unset, str] = UNSET
    subnet: Union[None, Unset, str] = UNSET
    subnet_uuid: Union[None, UUID, Unset] = UNSET
    subnet_name: Union[None, Unset, str] = UNSET
    subnet_description: Union[None, Unset, str] = UNSET
    subnet_cidr: Union[None, Unset, str] = UNSET
    allowed_address_pairs: Union[Unset, list["OpenStackAllowedAddressPair"]] = UNSET
    device_id: Union[None, Unset, str] = UNSET
    device_owner: Union[None, Unset, str] = UNSET
    security_groups: Union[Unset, list["OpenStackSecurityGroup"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        fixed_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.fixed_ips, Unset):
            fixed_ips = []
            for fixed_ips_item_data in self.fixed_ips:
                fixed_ips_item = fixed_ips_item_data.to_dict()
                fixed_ips.append(fixed_ips_item)

        mac_address = self.mac_address

        subnet: Union[None, Unset, str]
        if isinstance(self.subnet, Unset):
            subnet = UNSET
        else:
            subnet = self.subnet

        subnet_uuid: Union[None, Unset, str]
        if isinstance(self.subnet_uuid, Unset):
            subnet_uuid = UNSET
        elif isinstance(self.subnet_uuid, UUID):
            subnet_uuid = str(self.subnet_uuid)
        else:
            subnet_uuid = self.subnet_uuid

        subnet_name: Union[None, Unset, str]
        if isinstance(self.subnet_name, Unset):
            subnet_name = UNSET
        else:
            subnet_name = self.subnet_name

        subnet_description: Union[None, Unset, str]
        if isinstance(self.subnet_description, Unset):
            subnet_description = UNSET
        else:
            subnet_description = self.subnet_description

        subnet_cidr: Union[None, Unset, str]
        if isinstance(self.subnet_cidr, Unset):
            subnet_cidr = UNSET
        else:
            subnet_cidr = self.subnet_cidr

        allowed_address_pairs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.allowed_address_pairs, Unset):
            allowed_address_pairs = []
            for allowed_address_pairs_item_data in self.allowed_address_pairs:
                allowed_address_pairs_item = allowed_address_pairs_item_data.to_dict()
                allowed_address_pairs.append(allowed_address_pairs_item)

        device_id: Union[None, Unset, str]
        if isinstance(self.device_id, Unset):
            device_id = UNSET
        else:
            device_id = self.device_id

        device_owner: Union[None, Unset, str]
        if isinstance(self.device_owner, Unset):
            device_owner = UNSET
        else:
            device_owner = self.device_owner

        security_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.security_groups, Unset):
            security_groups = []
            for security_groups_item_data in self.security_groups:
                security_groups_item = security_groups_item_data.to_dict()
                security_groups.append(security_groups_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if fixed_ips is not UNSET:
            field_dict["fixed_ips"] = fixed_ips
        if mac_address is not UNSET:
            field_dict["mac_address"] = mac_address
        if subnet is not UNSET:
            field_dict["subnet"] = subnet
        if subnet_uuid is not UNSET:
            field_dict["subnet_uuid"] = subnet_uuid
        if subnet_name is not UNSET:
            field_dict["subnet_name"] = subnet_name
        if subnet_description is not UNSET:
            field_dict["subnet_description"] = subnet_description
        if subnet_cidr is not UNSET:
            field_dict["subnet_cidr"] = subnet_cidr
        if allowed_address_pairs is not UNSET:
            field_dict["allowed_address_pairs"] = allowed_address_pairs
        if device_id is not UNSET:
            field_dict["device_id"] = device_id
        if device_owner is not UNSET:
            field_dict["device_owner"] = device_owner
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_allowed_address_pair import OpenStackAllowedAddressPair
        from ..models.open_stack_fixed_ip import OpenStackFixedIp
        from ..models.open_stack_security_group import OpenStackSecurityGroup

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        fixed_ips = []
        _fixed_ips = d.pop("fixed_ips", UNSET)
        for fixed_ips_item_data in _fixed_ips or []:
            fixed_ips_item = OpenStackFixedIp.from_dict(fixed_ips_item_data)

            fixed_ips.append(fixed_ips_item)

        mac_address = d.pop("mac_address", UNSET)

        def _parse_subnet(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subnet = _parse_subnet(d.pop("subnet", UNSET))

        def _parse_subnet_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                subnet_uuid_type_0 = UUID(data)

                return subnet_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        subnet_uuid = _parse_subnet_uuid(d.pop("subnet_uuid", UNSET))

        def _parse_subnet_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subnet_name = _parse_subnet_name(d.pop("subnet_name", UNSET))

        def _parse_subnet_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subnet_description = _parse_subnet_description(d.pop("subnet_description", UNSET))

        def _parse_subnet_cidr(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subnet_cidr = _parse_subnet_cidr(d.pop("subnet_cidr", UNSET))

        allowed_address_pairs = []
        _allowed_address_pairs = d.pop("allowed_address_pairs", UNSET)
        for allowed_address_pairs_item_data in _allowed_address_pairs or []:
            allowed_address_pairs_item = OpenStackAllowedAddressPair.from_dict(allowed_address_pairs_item_data)

            allowed_address_pairs.append(allowed_address_pairs_item)

        def _parse_device_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        device_id = _parse_device_id(d.pop("device_id", UNSET))

        def _parse_device_owner(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        device_owner = _parse_device_owner(d.pop("device_owner", UNSET))

        security_groups = []
        _security_groups = d.pop("security_groups", UNSET)
        for security_groups_item_data in _security_groups or []:
            security_groups_item = OpenStackSecurityGroup.from_dict(security_groups_item_data)

            security_groups.append(security_groups_item)

        open_stack_nested_port = cls(
            url=url,
            fixed_ips=fixed_ips,
            mac_address=mac_address,
            subnet=subnet,
            subnet_uuid=subnet_uuid,
            subnet_name=subnet_name,
            subnet_description=subnet_description,
            subnet_cidr=subnet_cidr,
            allowed_address_pairs=allowed_address_pairs,
            device_id=device_id,
            device_owner=device_owner,
            security_groups=security_groups,
        )

        open_stack_nested_port.additional_properties = d
        return open_stack_nested_port

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
