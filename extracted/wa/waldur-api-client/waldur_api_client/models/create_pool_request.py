from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.load_balancer_protocol_enum import LoadBalancerProtocolEnum

T = TypeVar("T", bound="CreatePoolRequest")


@_attrs_define
class CreatePoolRequest:
    """
    Attributes:
        name (str):
        load_balancer (str): Load balancer this pool belongs to
        protocol (LoadBalancerProtocolEnum):
    """

    name: str
    load_balancer: str
    protocol: LoadBalancerProtocolEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        load_balancer = self.load_balancer

        protocol = self.protocol.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "load_balancer": load_balancer,
                "protocol": protocol,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        load_balancer = d.pop("load_balancer")

        protocol = LoadBalancerProtocolEnum(d.pop("protocol"))

        create_pool_request = cls(
            name=name,
            load_balancer=load_balancer,
            protocol=protocol,
        )

        create_pool_request.additional_properties = d
        return create_pool_request

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
