from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.arrow_customer_discovery import ArrowCustomerDiscovery
    from ..models.customer_mapping_suggestion import CustomerMappingSuggestion
    from ..models.waldur_customer_brief import WaldurCustomerBrief


T = TypeVar("T", bound="AvailableArrowCustomersResponse")


@_attrs_define
class AvailableArrowCustomersResponse:
    """
    Attributes:
        settings_uuid (UUID):
        arrow_customers (list['ArrowCustomerDiscovery']):
        waldur_customers (list['WaldurCustomerBrief']):
        suggestions (list['CustomerMappingSuggestion']):
    """

    settings_uuid: UUID
    arrow_customers: list["ArrowCustomerDiscovery"]
    waldur_customers: list["WaldurCustomerBrief"]
    suggestions: list["CustomerMappingSuggestion"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings_uuid = str(self.settings_uuid)

        arrow_customers = []
        for arrow_customers_item_data in self.arrow_customers:
            arrow_customers_item = arrow_customers_item_data.to_dict()
            arrow_customers.append(arrow_customers_item)

        waldur_customers = []
        for waldur_customers_item_data in self.waldur_customers:
            waldur_customers_item = waldur_customers_item_data.to_dict()
            waldur_customers.append(waldur_customers_item)

        suggestions = []
        for suggestions_item_data in self.suggestions:
            suggestions_item = suggestions_item_data.to_dict()
            suggestions.append(suggestions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings_uuid": settings_uuid,
                "arrow_customers": arrow_customers,
                "waldur_customers": waldur_customers,
                "suggestions": suggestions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrow_customer_discovery import ArrowCustomerDiscovery
        from ..models.customer_mapping_suggestion import CustomerMappingSuggestion
        from ..models.waldur_customer_brief import WaldurCustomerBrief

        d = dict(src_dict)
        settings_uuid = UUID(d.pop("settings_uuid"))

        arrow_customers = []
        _arrow_customers = d.pop("arrow_customers")
        for arrow_customers_item_data in _arrow_customers:
            arrow_customers_item = ArrowCustomerDiscovery.from_dict(arrow_customers_item_data)

            arrow_customers.append(arrow_customers_item)

        waldur_customers = []
        _waldur_customers = d.pop("waldur_customers")
        for waldur_customers_item_data in _waldur_customers:
            waldur_customers_item = WaldurCustomerBrief.from_dict(waldur_customers_item_data)

            waldur_customers.append(waldur_customers_item)

        suggestions = []
        _suggestions = d.pop("suggestions")
        for suggestions_item_data in _suggestions:
            suggestions_item = CustomerMappingSuggestion.from_dict(suggestions_item_data)

            suggestions.append(suggestions_item)

        available_arrow_customers_response = cls(
            settings_uuid=settings_uuid,
            arrow_customers=arrow_customers,
            waldur_customers=waldur_customers,
            suggestions=suggestions,
        )

        available_arrow_customers_response.additional_properties = d
        return available_arrow_customers_response

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
