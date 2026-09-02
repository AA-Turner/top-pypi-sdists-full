from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SetInstanceConfigJsonBodyGlobalSettings")


@_attrs_define
class SetInstanceConfigJsonBodyGlobalSettings:
    """Global settings keyed by setting name. Known fields include base_url, license_key, retention_period_secs,
    smtp_settings, otel, etc. Unknown fields are preserved as-is.

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        set_instance_config_json_body_global_settings = cls()

        set_instance_config_json_body_global_settings.additional_properties = d
        return set_instance_config_json_body_global_settings

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
