from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.invoice_price_source_enum import InvoicePriceSourceEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowSettingsCreateRequest")


@_attrs_define
class ArrowSettingsCreateRequest:
    """
    Attributes:
        api_url (str): Arrow API base URL
        api_key (str): Arrow API Key (required for creation)
        export_type_reference (Union[Unset, str]): Billing export template reference
        classification_filter (Union[Unset, str]): Filter for IaaS/SaaS classification
        is_active (Union[Unset, bool]): Whether this settings record is active
        sync_enabled (Union[Unset, bool]): Whether automatic billing sync is enabled
        invoice_price_source (Union[Unset, InvoicePriceSourceEnum]):
        invoice_item_prefix (Union[Unset, str]): Prefix for invoice item names (e.g. 'Arrow consumption')
    """

    api_url: str
    api_key: str
    export_type_reference: Union[Unset, str] = UNSET
    classification_filter: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    sync_enabled: Union[Unset, bool] = UNSET
    invoice_price_source: Union[Unset, InvoicePriceSourceEnum] = UNSET
    invoice_item_prefix: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_url = self.api_url

        api_key = self.api_key

        export_type_reference = self.export_type_reference

        classification_filter = self.classification_filter

        is_active = self.is_active

        sync_enabled = self.sync_enabled

        invoice_price_source: Union[Unset, str] = UNSET
        if not isinstance(self.invoice_price_source, Unset):
            invoice_price_source = self.invoice_price_source.value

        invoice_item_prefix = self.invoice_item_prefix

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
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if sync_enabled is not UNSET:
            field_dict["sync_enabled"] = sync_enabled
        if invoice_price_source is not UNSET:
            field_dict["invoice_price_source"] = invoice_price_source
        if invoice_item_prefix is not UNSET:
            field_dict["invoice_item_prefix"] = invoice_item_prefix

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_url = d.pop("api_url")

        api_key = d.pop("api_key")

        export_type_reference = d.pop("export_type_reference", UNSET)

        classification_filter = d.pop("classification_filter", UNSET)

        is_active = d.pop("is_active", UNSET)

        sync_enabled = d.pop("sync_enabled", UNSET)

        _invoice_price_source = d.pop("invoice_price_source", UNSET)
        invoice_price_source: Union[Unset, InvoicePriceSourceEnum]
        if isinstance(_invoice_price_source, Unset):
            invoice_price_source = UNSET
        else:
            invoice_price_source = InvoicePriceSourceEnum(_invoice_price_source)

        invoice_item_prefix = d.pop("invoice_item_prefix", UNSET)

        arrow_settings_create_request = cls(
            api_url=api_url,
            api_key=api_key,
            export_type_reference=export_type_reference,
            classification_filter=classification_filter,
            is_active=is_active,
            sync_enabled=sync_enabled,
            invoice_price_source=invoice_price_source,
            invoice_item_prefix=invoice_item_prefix,
        )

        arrow_settings_create_request.additional_properties = d
        return arrow_settings_create_request

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
