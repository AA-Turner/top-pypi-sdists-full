from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_reference import OfferingReference


T = TypeVar("T", bound="OfferingGroups")


@_attrs_define
class OfferingGroups:
    """
    Attributes:
        customer_name (str):
        customer_uuid (str):
        offerings (list['OfferingReference']):
    """

    customer_name: str
    customer_uuid: str
    offerings: list["OfferingReference"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_name = self.customer_name

        customer_uuid = self.customer_uuid

        offerings = []
        for offerings_item_data in self.offerings:
            offerings_item = offerings_item_data.to_dict()
            offerings.append(offerings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "offerings": offerings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_reference import OfferingReference

        d = dict(src_dict)
        customer_name = d.pop("customer_name")

        customer_uuid = d.pop("customer_uuid")

        offerings = []
        _offerings = d.pop("offerings")
        for offerings_item_data in _offerings:
            offerings_item = OfferingReference.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        offering_groups = cls(
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            offerings=offerings,
        )

        offering_groups.additional_properties = d
        return offering_groups

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
