from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EditGuestAccessJsonBody")


@_attrs_define
class EditGuestAccessJsonBody:
    """
    Attributes:
        guest_access_enabled (bool):
    """

    guest_access_enabled: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        guest_access_enabled = self.guest_access_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "guest_access_enabled": guest_access_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        guest_access_enabled = d.pop("guest_access_enabled")

        edit_guest_access_json_body = cls(
            guest_access_enabled=guest_access_enabled,
        )

        edit_guest_access_json_body.additional_properties = d
        return edit_guest_access_json_body

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
