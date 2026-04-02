from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SaveSettingsResponse")


@_attrs_define
class SaveSettingsResponse:
    """
    Attributes:
        settings_uuid (UUID):
        mappings_created (int):
        message (str):
    """

    settings_uuid: UUID
    mappings_created: int
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings_uuid = str(self.settings_uuid)

        mappings_created = self.mappings_created

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings_uuid": settings_uuid,
                "mappings_created": mappings_created,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        settings_uuid = UUID(d.pop("settings_uuid"))

        mappings_created = d.pop("mappings_created")

        message = d.pop("message")

        save_settings_response = cls(
            settings_uuid=settings_uuid,
            mappings_created=mappings_created,
            message=message,
        )

        save_settings_response.additional_properties = d
        return save_settings_response

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
