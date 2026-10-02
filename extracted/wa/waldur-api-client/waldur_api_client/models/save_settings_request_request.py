from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customer_mapping_input_request import CustomerMappingInputRequest


T = TypeVar("T", bound="SaveSettingsRequestRequest")


@_attrs_define
class SaveSettingsRequestRequest:
    """
    Attributes:
        api_url (str): Arrow API base URL
        api_key (str): Arrow API Key
        export_type_reference (Union[Unset, str]):
        classification_filter (Union[Unset, str]):  Default: 'IAAS'.
        sync_enabled (Union[Unset, bool]):  Default: False.
        customer_mappings (Union[Unset, list['CustomerMappingInputRequest']]):
    """

    api_url: str
    api_key: str
    export_type_reference: Union[Unset, str] = UNSET
    classification_filter: Union[Unset, str] = "IAAS"
    sync_enabled: Union[Unset, bool] = False
    customer_mappings: Union[Unset, list["CustomerMappingInputRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_url = self.api_url

        api_key = self.api_key

        export_type_reference = self.export_type_reference

        classification_filter = self.classification_filter

        sync_enabled = self.sync_enabled

        customer_mappings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.customer_mappings, Unset):
            customer_mappings = []
            for customer_mappings_item_data in self.customer_mappings:
                customer_mappings_item = customer_mappings_item_data.to_dict()
                customer_mappings.append(customer_mappings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_url": api_url,
                "api_key": api_key,
            }
        )
        if export_type_reference is not UNSET:
            field_dict["export_type_reference"] = export_type_reference
        if classification_filter is not UNSET:
            field_dict["classification_filter"] = classification_filter
        if sync_enabled is not UNSET:
            field_dict["sync_enabled"] = sync_enabled
        if customer_mappings is not UNSET:
            field_dict["customer_mappings"] = customer_mappings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customer_mapping_input_request import CustomerMappingInputRequest

        d = dict(src_dict)
        api_url = d.pop("api_url")

        api_key = d.pop("api_key")

        export_type_reference = d.pop("export_type_reference", UNSET)

        classification_filter = d.pop("classification_filter", UNSET)

        sync_enabled = d.pop("sync_enabled", UNSET)

        customer_mappings = []
        _customer_mappings = d.pop("customer_mappings", UNSET)
        for customer_mappings_item_data in _customer_mappings or []:
            customer_mappings_item = CustomerMappingInputRequest.from_dict(customer_mappings_item_data)

            customer_mappings.append(customer_mappings_item)

        save_settings_request_request = cls(
            api_url=api_url,
            api_key=api_key,
            export_type_reference=export_type_reference,
            classification_filter=classification_filter,
            sync_enabled=sync_enabled,
            customer_mappings=customer_mappings,
        )

        save_settings_request_request.additional_properties = d
        return save_settings_request_request

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
