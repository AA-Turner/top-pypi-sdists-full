from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_fixed_ip_request import OpenStackFixedIpRequest


T = TypeVar("T", bound="OpenStackNestedPortRequest")


@_attrs_define
class OpenStackNestedPortRequest:
    """
    Attributes:
        fixed_ips (Union[Unset, list['OpenStackFixedIpRequest']]):
        subnet (Union[None, Unset, str]): Subnet to which this port belongs
    """

    fixed_ips: Union[Unset, list["OpenStackFixedIpRequest"]] = UNSET
    subnet: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fixed_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.fixed_ips, Unset):
            fixed_ips = []
            for fixed_ips_item_data in self.fixed_ips:
                fixed_ips_item = fixed_ips_item_data.to_dict()
                fixed_ips.append(fixed_ips_item)

        subnet: Union[None, Unset, str]
        if isinstance(self.subnet, Unset):
            subnet = UNSET
        else:
            subnet = self.subnet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fixed_ips is not UNSET:
            field_dict["fixed_ips"] = fixed_ips
        if subnet is not UNSET:
            field_dict["subnet"] = subnet

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_fixed_ip_request import OpenStackFixedIpRequest

        d = dict(src_dict)
        fixed_ips = []
        _fixed_ips = d.pop("fixed_ips", UNSET)
        for fixed_ips_item_data in _fixed_ips or []:
            fixed_ips_item = OpenStackFixedIpRequest.from_dict(fixed_ips_item_data)

            fixed_ips.append(fixed_ips_item)

        def _parse_subnet(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subnet = _parse_subnet(d.pop("subnet", UNSET))

        open_stack_nested_port_request = cls(
            fixed_ips=fixed_ips,
            subnet=subnet,
        )

        open_stack_nested_port_request.additional_properties = d
        return open_stack_nested_port_request

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
