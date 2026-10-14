from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateLoadBalancerRequest")


@_attrs_define
class CreateLoadBalancerRequest:
    """
    Attributes:
        name (str):
        tenant (str): OpenStack tenant this load balancer belongs to
        vip_subnet (str):
        vip_address (Union[None, Unset, str]): Virtual IP address to request, IPv4 or IPv6. It must be of the same
            family as vip_subnet and lie inside it. Octavia allocates one from vip_subnet when omitted.
    """

    name: str
    tenant: str
    vip_subnet: str
    vip_address: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        tenant = self.tenant

        vip_subnet = self.vip_subnet

        vip_address: Union[None, Unset, str]
        if isinstance(self.vip_address, Unset):
            vip_address = UNSET
        else:
            vip_address = self.vip_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "tenant": tenant,
                "vip_subnet": vip_subnet,
            }
        )
        if vip_address is not UNSET:
            field_dict["vip_address"] = vip_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        tenant = d.pop("tenant")

        vip_subnet = d.pop("vip_subnet")

        def _parse_vip_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        vip_address = _parse_vip_address(d.pop("vip_address", UNSET))

        create_load_balancer_request = cls(
            name=name,
            tenant=tenant,
            vip_subnet=vip_subnet,
            vip_address=vip_address,
        )

        create_load_balancer_request.additional_properties = d
        return create_load_balancer_request

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
