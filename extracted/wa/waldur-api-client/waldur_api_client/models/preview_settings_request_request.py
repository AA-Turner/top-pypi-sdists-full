from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewSettingsRequestRequest")


@_attrs_define
class PreviewSettingsRequestRequest:
    """
    Attributes:
        api_url (str): Arrow API base URL
        api_key (str): Arrow API Key
        export_type_reference (Union[Unset, str]):
        classification_filter (Union[Unset, str]):  Default: 'IAAS'.
        sync_enabled (Union[Unset, bool]):  Default: False.
    """

    api_url: str
    api_key: str
    export_type_reference: Union[Unset, str] = UNSET
    classification_filter: Union[Unset, str] = "IAAS"
    sync_enabled: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_url = self.api_url

        api_key = self.api_key

        export_type_reference = self.export_type_reference

        classification_filter = self.classification_filter

        sync_enabled = self.sync_enabled

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_url = d.pop("api_url")

        api_key = d.pop("api_key")

        export_type_reference = d.pop("export_type_reference", UNSET)

        classification_filter = d.pop("classification_filter", UNSET)

        sync_enabled = d.pop("sync_enabled", UNSET)

        preview_settings_request_request = cls(
            api_url=api_url,
            api_key=api_key,
            export_type_reference=export_type_reference,
            classification_filter=classification_filter,
            sync_enabled=sync_enabled,
        )

        preview_settings_request_request.additional_properties = d
        return preview_settings_request_request

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
