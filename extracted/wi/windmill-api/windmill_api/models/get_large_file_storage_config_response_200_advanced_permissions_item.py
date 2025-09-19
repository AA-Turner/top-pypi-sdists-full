from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetLargeFileStorageConfigResponse200AdvancedPermissionsItem")


@_attrs_define
class GetLargeFileStorageConfigResponse200AdvancedPermissionsItem:
    """
    Attributes:
        pattern (str):
        allow (str):
    """

    pattern: str
    allow: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pattern = self.pattern
        allow = self.allow

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pattern": pattern,
                "allow": allow,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pattern = d.pop("pattern")

        allow = d.pop("allow")

        get_large_file_storage_config_response_200_advanced_permissions_item = cls(
            pattern=pattern,
            allow=allow,
        )

        get_large_file_storage_config_response_200_advanced_permissions_item.additional_properties = d
        return get_large_file_storage_config_response_200_advanced_permissions_item

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
