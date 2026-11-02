from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage")


@_attrs_define
class GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage:
    """
    Attributes:
        path (str):
        storage (Union[Unset, str]):
    """

    path: str
    storage: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        storage = self.storage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
            }
        )
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        storage = d.pop("storage", UNSET)

        get_settings_response_200_ducklake_ducklakes_additional_property_storage = cls(
            path=path,
            storage=storage,
        )

        get_settings_response_200_ducklake_ducklakes_additional_property_storage.additional_properties = d
        return get_settings_response_200_ducklake_ducklakes_additional_property_storage

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
