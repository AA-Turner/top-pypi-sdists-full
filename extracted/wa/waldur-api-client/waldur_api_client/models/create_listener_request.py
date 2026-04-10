from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.load_balancer_protocol_enum import LoadBalancerProtocolEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateListenerRequest")


@_attrs_define
class CreateListenerRequest:
    """
    Attributes:
        load_balancer (str): Load balancer this listener belongs to
        protocol (LoadBalancerProtocolEnum):
        protocol_port (int): Port on which the listener listens
        name (Union[Unset, str]):
        default_pool (Union[None, Unset, str]):
    """

    load_balancer: str
    protocol: LoadBalancerProtocolEnum
    protocol_port: int
    name: Union[Unset, str] = UNSET
    default_pool: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        load_balancer = self.load_balancer

        protocol = self.protocol.value

        protocol_port = self.protocol_port

        name = self.name

        default_pool: Union[None, Unset, str]
        if isinstance(self.default_pool, Unset):
            default_pool = UNSET
        else:
            default_pool = self.default_pool

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "load_balancer": load_balancer,
                "protocol": protocol,
                "protocol_port": protocol_port,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if default_pool is not UNSET:
            field_dict["default_pool"] = default_pool

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        load_balancer = d.pop("load_balancer")

        protocol = LoadBalancerProtocolEnum(d.pop("protocol"))

        protocol_port = d.pop("protocol_port")

        name = d.pop("name", UNSET)

        def _parse_default_pool(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_pool = _parse_default_pool(d.pop("default_pool", UNSET))

        create_listener_request = cls(
            load_balancer=load_balancer,
            protocol=protocol,
            protocol_port=protocol_port,
            name=name,
            default_pool=default_pool,
        )

        create_listener_request.additional_properties = d
        return create_listener_request

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
