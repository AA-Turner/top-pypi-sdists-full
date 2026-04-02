from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackRouterInterfaceRequest")


@_attrs_define
class OpenStackRouterInterfaceRequest:
    """
    Attributes:
        subnet (Union[Unset, str]): The subnet to connect to the router. Either subnet or port must be specified, but
            not both.
        port (Union[Unset, str]): The port to connect to the router. Either subnet or port must be specified, but not
            both.
    """

    subnet: Union[Unset, str] = UNSET
    port: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subnet = self.subnet

        port = self.port

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if subnet is not UNSET:
            field_dict["subnet"] = subnet
        if port is not UNSET:
            field_dict["port"] = port

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        subnet = d.pop("subnet", UNSET)

        port = d.pop("port", UNSET)

        open_stack_router_interface_request = cls(
            subnet=subnet,
            port=port,
        )

        open_stack_router_interface_request.additional_properties = d
        return open_stack_router_interface_request

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
