from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PreviewSettingsResponse")


@_attrs_define
class PreviewSettingsResponse:
    """
    Attributes:
        api_url (str):
        partner_name (str):
        partner_reference (str):
        export_type_reference (str):
        classification_filter (str):
        sync_enabled (bool):
    """

    api_url: str
    partner_name: str
    partner_reference: str
    export_type_reference: str
    classification_filter: str
    sync_enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_url = self.api_url

        partner_name = self.partner_name

        partner_reference = self.partner_reference

        export_type_reference = self.export_type_reference

        classification_filter = self.classification_filter

        sync_enabled = self.sync_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_url": api_url,
                "partner_name": partner_name,
                "partner_reference": partner_reference,
                "export_type_reference": export_type_reference,
                "classification_filter": classification_filter,
                "sync_enabled": sync_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_url = d.pop("api_url")

        partner_name = d.pop("partner_name")

        partner_reference = d.pop("partner_reference")

        export_type_reference = d.pop("export_type_reference")

        classification_filter = d.pop("classification_filter")

        sync_enabled = d.pop("sync_enabled")

        preview_settings_response = cls(
            api_url=api_url,
            partner_name=partner_name,
            partner_reference=partner_reference,
            export_type_reference=export_type_reference,
            classification_filter=classification_filter,
            sync_enabled=sync_enabled,
        )

        preview_settings_response.additional_properties = d
        return preview_settings_response

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
