from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_create_floating_ip_request import OpenStackCreateFloatingIPRequest


T = TypeVar("T", bound="OpenStackInstanceFloatingIPsUpdateRequest")


@_attrs_define
class OpenStackInstanceFloatingIPsUpdateRequest:
    """
    Attributes:
        floating_ips (Union[Unset, list['OpenStackCreateFloatingIPRequest']]):
    """

    floating_ips: Union[Unset, list["OpenStackCreateFloatingIPRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        floating_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.floating_ips, Unset):
            floating_ips = []
            for floating_ips_item_data in self.floating_ips:
                floating_ips_item = floating_ips_item_data.to_dict()
                floating_ips.append(floating_ips_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if floating_ips is not UNSET:
            field_dict["floating_ips"] = floating_ips

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_create_floating_ip_request import OpenStackCreateFloatingIPRequest

        d = dict(src_dict)
        floating_ips = []
        _floating_ips = d.pop("floating_ips", UNSET)
        for floating_ips_item_data in _floating_ips or []:
            floating_ips_item = OpenStackCreateFloatingIPRequest.from_dict(floating_ips_item_data)

            floating_ips.append(floating_ips_item)

        open_stack_instance_floating_i_ps_update_request = cls(
            floating_ips=floating_ips,
        )

        open_stack_instance_floating_i_ps_update_request.additional_properties = d
        return open_stack_instance_floating_i_ps_update_request

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
