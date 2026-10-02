import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.invoice_price_source_enum import InvoicePriceSourceEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowSettingsCreate")


@_attrs_define
class ArrowSettingsCreate:
    """
    Attributes:
        uuid (UUID):
        url (str):
        api_url (str): Arrow API base URL
        partner_reference (str): Arrow partner reference (discovered from API)
        partner_name (str): Arrow partner name (discovered from API)
        created (datetime.datetime):
        modified (datetime.datetime):
        export_type_reference (Union[Unset, str]): Billing export template reference
        classification_filter (Union[Unset, str]): Filter for IaaS/SaaS classification
        is_active (Union[Unset, bool]): Whether this settings record is active
        sync_enabled (Union[Unset, bool]): Whether automatic billing sync is enabled
        invoice_price_source (Union[Unset, InvoicePriceSourceEnum]):
        invoice_item_prefix (Union[Unset, str]): Prefix for invoice item names (e.g. 'Arrow consumption')
    """

    uuid: UUID
    url: str
    api_url: str
    partner_reference: str
    partner_name: str
    created: datetime.datetime
    modified: datetime.datetime
    export_type_reference: Union[Unset, str] = UNSET
    classification_filter: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    sync_enabled: Union[Unset, bool] = UNSET
    invoice_price_source: Union[Unset, InvoicePriceSourceEnum] = UNSET
    invoice_item_prefix: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        api_url = self.api_url

        partner_reference = self.partner_reference

        partner_name = self.partner_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

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
                "uuid": uuid,
                "url": url,
                "api_url": api_url,
                "partner_reference": partner_reference,
                "partner_name": partner_name,
                "created": created,
                "modified": modified,
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
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        api_url = d.pop("api_url")

        partner_reference = d.pop("partner_reference")

        partner_name = d.pop("partner_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

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

        arrow_settings_create = cls(
            uuid=uuid,
            url=url,
            api_url=api_url,
            partner_reference=partner_reference,
            partner_name=partner_name,
            created=created,
            modified=modified,
            export_type_reference=export_type_reference,
            classification_filter=classification_filter,
            is_active=is_active,
            sync_enabled=sync_enabled,
            invoice_price_source=invoice_price_source,
            invoice_item_prefix=invoice_item_prefix,
        )

        arrow_settings_create.additional_properties = d
        return arrow_settings_create

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
