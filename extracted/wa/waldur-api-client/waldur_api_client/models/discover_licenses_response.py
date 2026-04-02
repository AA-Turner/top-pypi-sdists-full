from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.arrow_license import ArrowLicense
    from ..models.license_suggestion import LicenseSuggestion
    from ..models.waldur_resource_for_linking import WaldurResourceForLinking


T = TypeVar("T", bound="DiscoverLicensesResponse")


@_attrs_define
class DiscoverLicensesResponse:
    """
    Attributes:
        customer_mapping_uuid (UUID):
        arrow_reference (str):
        waldur_customer_name (str):
        arrow_licenses (list['ArrowLicense']): Arrow licenses from billing export for this customer.
        waldur_resources (list['WaldurResourceForLinking']): Waldur resources for this customer.
        suggestions (list['LicenseSuggestion']): Suggested matches based on name similarity.
        error (Union[None, str]):
    """

    customer_mapping_uuid: UUID
    arrow_reference: str
    waldur_customer_name: str
    arrow_licenses: list["ArrowLicense"]
    waldur_resources: list["WaldurResourceForLinking"]
    suggestions: list["LicenseSuggestion"]
    error: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_mapping_uuid = str(self.customer_mapping_uuid)

        arrow_reference = self.arrow_reference

        waldur_customer_name = self.waldur_customer_name

        arrow_licenses = []
        for arrow_licenses_item_data in self.arrow_licenses:
            arrow_licenses_item = arrow_licenses_item_data.to_dict()
            arrow_licenses.append(arrow_licenses_item)

        waldur_resources = []
        for waldur_resources_item_data in self.waldur_resources:
            waldur_resources_item = waldur_resources_item_data.to_dict()
            waldur_resources.append(waldur_resources_item)

        suggestions = []
        for suggestions_item_data in self.suggestions:
            suggestions_item = suggestions_item_data.to_dict()
            suggestions.append(suggestions_item)

        error: Union[None, str]
        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_mapping_uuid": customer_mapping_uuid,
                "arrow_reference": arrow_reference,
                "waldur_customer_name": waldur_customer_name,
                "arrow_licenses": arrow_licenses,
                "waldur_resources": waldur_resources,
                "suggestions": suggestions,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrow_license import ArrowLicense
        from ..models.license_suggestion import LicenseSuggestion
        from ..models.waldur_resource_for_linking import WaldurResourceForLinking

        d = dict(src_dict)
        customer_mapping_uuid = UUID(d.pop("customer_mapping_uuid"))

        arrow_reference = d.pop("arrow_reference")

        waldur_customer_name = d.pop("waldur_customer_name")

        arrow_licenses = []
        _arrow_licenses = d.pop("arrow_licenses")
        for arrow_licenses_item_data in _arrow_licenses:
            arrow_licenses_item = ArrowLicense.from_dict(arrow_licenses_item_data)

            arrow_licenses.append(arrow_licenses_item)

        waldur_resources = []
        _waldur_resources = d.pop("waldur_resources")
        for waldur_resources_item_data in _waldur_resources:
            waldur_resources_item = WaldurResourceForLinking.from_dict(waldur_resources_item_data)

            waldur_resources.append(waldur_resources_item)

        suggestions = []
        _suggestions = d.pop("suggestions")
        for suggestions_item_data in _suggestions:
            suggestions_item = LicenseSuggestion.from_dict(suggestions_item_data)

            suggestions.append(suggestions_item)

        def _parse_error(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        error = _parse_error(d.pop("error"))

        discover_licenses_response = cls(
            customer_mapping_uuid=customer_mapping_uuid,
            arrow_reference=arrow_reference,
            waldur_customer_name=waldur_customer_name,
            arrow_licenses=arrow_licenses,
            waldur_resources=waldur_resources,
            suggestions=suggestions,
            error=error,
        )

        discover_licenses_response.additional_properties = d
        return discover_licenses_response

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
