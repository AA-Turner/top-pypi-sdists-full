from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateLoadBalancerRequest")


@_attrs_define
class CreateLoadBalancerRequest:
    """
    Attributes:
        tenant (str): OpenStack tenant this load balancer belongs to
        name (str):
        vip_subnet_id (str):
    """

    tenant: str
    name: str
    vip_subnet_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tenant = self.tenant

        name = self.name

        vip_subnet_id = self.vip_subnet_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenant": tenant,
                "name": name,
                "vip_subnet_id": vip_subnet_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tenant = d.pop("tenant")

        name = d.pop("name")

        vip_subnet_id = d.pop("vip_subnet_id")

        create_load_balancer_request = cls(
            tenant=tenant,
            name=name,
            vip_subnet_id=vip_subnet_id,
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
