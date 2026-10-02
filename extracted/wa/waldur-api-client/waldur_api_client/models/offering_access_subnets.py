from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_access_subnet_expanded import OfferingAccessSubnetExpanded


T = TypeVar("T", bound="OfferingAccessSubnets")


@_attrs_define
class OfferingAccessSubnets:
    """
    Attributes:
        expanded (list['OfferingAccessSubnetExpanded']):
        packed (list[str]):
        defaults (list[str]):
    """

    expanded: list["OfferingAccessSubnetExpanded"]
    packed: list[str]
    defaults: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expanded = []
        for expanded_item_data in self.expanded:
            expanded_item = expanded_item_data.to_dict()
            expanded.append(expanded_item)

        packed = self.packed

        defaults = self.defaults

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expanded": expanded,
                "packed": packed,
                "defaults": defaults,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_access_subnet_expanded import OfferingAccessSubnetExpanded

        d = dict(src_dict)
        expanded = []
        _expanded = d.pop("expanded")
        for expanded_item_data in _expanded:
            expanded_item = OfferingAccessSubnetExpanded.from_dict(expanded_item_data)

            expanded.append(expanded_item)

        packed = cast(list[str], d.pop("packed"))

        defaults = cast(list[str], d.pop("defaults"))

        offering_access_subnets = cls(
            expanded=expanded,
            packed=packed,
            defaults=defaults,
        )

        offering_access_subnets.additional_properties = d
        return offering_access_subnets

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
