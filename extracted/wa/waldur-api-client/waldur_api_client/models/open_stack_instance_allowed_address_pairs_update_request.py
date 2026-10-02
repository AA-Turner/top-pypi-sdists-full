from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.open_stack_allowed_address_pair_request import OpenStackAllowedAddressPairRequest


T = TypeVar("T", bound="OpenStackInstanceAllowedAddressPairsUpdateRequest")


@_attrs_define
class OpenStackInstanceAllowedAddressPairsUpdateRequest:
    """
    Attributes:
        subnet (str): The subnet to update allowed address pairs for.
        allowed_address_pairs (list['OpenStackAllowedAddressPairRequest']): List of allowed address pairs to set on the
            port. Each pair should contain 'ip_address' and optional 'mac_address'.
    """

    subnet: str
    allowed_address_pairs: list["OpenStackAllowedAddressPairRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subnet = self.subnet

        allowed_address_pairs = []
        for allowed_address_pairs_item_data in self.allowed_address_pairs:
            allowed_address_pairs_item = allowed_address_pairs_item_data.to_dict()
            allowed_address_pairs.append(allowed_address_pairs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subnet": subnet,
                "allowed_address_pairs": allowed_address_pairs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_allowed_address_pair_request import OpenStackAllowedAddressPairRequest

        d = dict(src_dict)
        subnet = d.pop("subnet")

        allowed_address_pairs = []
        _allowed_address_pairs = d.pop("allowed_address_pairs")
        for allowed_address_pairs_item_data in _allowed_address_pairs:
            allowed_address_pairs_item = OpenStackAllowedAddressPairRequest.from_dict(allowed_address_pairs_item_data)

            allowed_address_pairs.append(allowed_address_pairs_item)

        open_stack_instance_allowed_address_pairs_update_request = cls(
            subnet=subnet,
            allowed_address_pairs=allowed_address_pairs,
        )

        open_stack_instance_allowed_address_pairs_update_request.additional_properties = d
        return open_stack_instance_allowed_address_pairs_update_request

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
