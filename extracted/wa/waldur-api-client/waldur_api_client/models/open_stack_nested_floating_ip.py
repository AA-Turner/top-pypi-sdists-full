from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_fixed_ip import OpenStackFixedIp


T = TypeVar("T", bound="OpenStackNestedFloatingIP")


@_attrs_define
class OpenStackNestedFloatingIP:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        address (Union[None, Unset, str]): The public IPv4 address of the floating IP
        port_fixed_ips (Union[Unset, list['OpenStackFixedIp']]):
        port_mac_address (Union[None, Unset, str]): MAC address of the port
        subnet (Union[Unset, str]):
        subnet_uuid (Union[Unset, UUID]):
        subnet_name (Union[Unset, str]):
        subnet_description (Union[Unset, str]):
        subnet_cidr (Union[Unset, str]): IPv4 network address in CIDR format (e.g. 192.168.0.0/24)
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    address: Union[None, Unset, str] = UNSET
    port_fixed_ips: Union[Unset, list["OpenStackFixedIp"]] = UNSET
    port_mac_address: Union[None, Unset, str] = UNSET
    subnet: Union[Unset, str] = UNSET
    subnet_uuid: Union[Unset, UUID] = UNSET
    subnet_name: Union[Unset, str] = UNSET
    subnet_description: Union[Unset, str] = UNSET
    subnet_cidr: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        address: Union[None, Unset, str]
        if isinstance(self.address, Unset):
            address = UNSET
        else:
            address = self.address

        port_fixed_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.port_fixed_ips, Unset):
            port_fixed_ips = []
            for port_fixed_ips_item_data in self.port_fixed_ips:
                port_fixed_ips_item = port_fixed_ips_item_data.to_dict()
                port_fixed_ips.append(port_fixed_ips_item)

        port_mac_address: Union[None, Unset, str]
        if isinstance(self.port_mac_address, Unset):
            port_mac_address = UNSET
        else:
            port_mac_address = self.port_mac_address

        subnet = self.subnet

        subnet_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.subnet_uuid, Unset):
            subnet_uuid = str(self.subnet_uuid)

        subnet_name = self.subnet_name

        subnet_description = self.subnet_description

        subnet_cidr = self.subnet_cidr

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if address is not UNSET:
            field_dict["address"] = address
        if port_fixed_ips is not UNSET:
            field_dict["port_fixed_ips"] = port_fixed_ips
        if port_mac_address is not UNSET:
            field_dict["port_mac_address"] = port_mac_address
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_fixed_ip import OpenStackFixedIp

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        def _parse_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        address = _parse_address(d.pop("address", UNSET))

        port_fixed_ips = []
        _port_fixed_ips = d.pop("port_fixed_ips", UNSET)
        for port_fixed_ips_item_data in _port_fixed_ips or []:
            port_fixed_ips_item = OpenStackFixedIp.from_dict(port_fixed_ips_item_data)

            port_fixed_ips.append(port_fixed_ips_item)

        def _parse_port_mac_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        port_mac_address = _parse_port_mac_address(d.pop("port_mac_address", UNSET))

        subnet = d.pop("subnet", UNSET)

        _subnet_uuid = d.pop("subnet_uuid", UNSET)
        subnet_uuid: Union[Unset, UUID]
        if isinstance(_subnet_uuid, Unset):
            subnet_uuid = UNSET
        else:
            subnet_uuid = UUID(_subnet_uuid)

        subnet_name = d.pop("subnet_name", UNSET)

        subnet_description = d.pop("subnet_description", UNSET)

        subnet_cidr = d.pop("subnet_cidr", UNSET)

        open_stack_nested_floating_ip = cls(
            url=url,
            uuid=uuid,
            address=address,
            port_fixed_ips=port_fixed_ips,
            port_mac_address=port_mac_address,
            subnet=subnet,
            subnet_uuid=subnet_uuid,
            subnet_name=subnet_name,
            subnet_description=subnet_description,
            subnet_cidr=subnet_cidr,
        )

        open_stack_nested_floating_ip.additional_properties = d
        return open_stack_nested_floating_ip

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
