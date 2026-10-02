from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.arrow_customer_discovery import ArrowCustomerDiscovery
    from ..models.waldur_customer_brief import WaldurCustomerBrief


T = TypeVar("T", bound="CustomerMappingSuggestion")


@_attrs_define
class CustomerMappingSuggestion:
    """
    Attributes:
        arrow_customer (ArrowCustomerDiscovery):
        suggested_waldur_customer (Union[Unset, WaldurCustomerBrief]):
        confidence (Union[Unset, float]):
        existing_mapping (Union[Unset, bool]):  Default: False.
    """

    arrow_customer: "ArrowCustomerDiscovery"
    suggested_waldur_customer: Union[Unset, "WaldurCustomerBrief"] = UNSET
    confidence: Union[Unset, float] = UNSET
    existing_mapping: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        arrow_customer = self.arrow_customer.to_dict()

        suggested_waldur_customer: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.suggested_waldur_customer, Unset):
            suggested_waldur_customer = self.suggested_waldur_customer.to_dict()

        confidence = self.confidence

        existing_mapping = self.existing_mapping

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "arrow_customer": arrow_customer,
            }
        )
        if suggested_waldur_customer is not UNSET:
            field_dict["suggested_waldur_customer"] = suggested_waldur_customer
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if existing_mapping is not UNSET:
            field_dict["existing_mapping"] = existing_mapping

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrow_customer_discovery import ArrowCustomerDiscovery
        from ..models.waldur_customer_brief import WaldurCustomerBrief

        d = dict(src_dict)
        arrow_customer = ArrowCustomerDiscovery.from_dict(d.pop("arrow_customer"))

        _suggested_waldur_customer = d.pop("suggested_waldur_customer", UNSET)
        suggested_waldur_customer: Union[Unset, WaldurCustomerBrief]
        if isinstance(_suggested_waldur_customer, Unset):
            suggested_waldur_customer = UNSET
        else:
            suggested_waldur_customer = WaldurCustomerBrief.from_dict(_suggested_waldur_customer)

        confidence = d.pop("confidence", UNSET)

        existing_mapping = d.pop("existing_mapping", UNSET)

        customer_mapping_suggestion = cls(
            arrow_customer=arrow_customer,
            suggested_waldur_customer=suggested_waldur_customer,
            confidence=confidence,
            existing_mapping=existing_mapping,
        )

        customer_mapping_suggestion.additional_properties = d
        return customer_mapping_suggestion

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
