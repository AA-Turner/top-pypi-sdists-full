from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.settings_metadata_response_settings_item import SettingsMetadataResponseSettingsItem


T = TypeVar("T", bound="SettingsMetadataResponse")


@_attrs_define
class SettingsMetadataResponse:
    """
    Attributes:
        settings (list['SettingsMetadataResponseSettingsItem']): List of settings sections with configuration items
    """

    settings: list["SettingsMetadataResponseSettingsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings = []
        for settings_item_data in self.settings:
            settings_item = settings_item_data.to_dict()
            settings.append(settings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings": settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.settings_metadata_response_settings_item import SettingsMetadataResponseSettingsItem

        d = dict(src_dict)
        settings = []
        _settings = d.pop("settings")
        for settings_item_data in _settings:
            settings_item = SettingsMetadataResponseSettingsItem.from_dict(settings_item_data)

            settings.append(settings_item)

        settings_metadata_response = cls(
            settings=settings,
        )

        settings_metadata_response.additional_properties = d
        return settings_metadata_response

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
