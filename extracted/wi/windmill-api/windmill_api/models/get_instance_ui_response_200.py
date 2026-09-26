from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetInstanceUiResponse200")


@_attrs_define
class GetInstanceUiResponse200:
    """
    Attributes:
        instance_banner (Union[Unset, Any]):
        accent_color (Union[Unset, Any]):
    """

    instance_banner: Union[Unset, Any] = UNSET
    accent_color: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instance_banner = self.instance_banner
        accent_color = self.accent_color

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instance_banner is not UNSET:
            field_dict["instance_banner"] = instance_banner
        if accent_color is not UNSET:
            field_dict["accent_color"] = accent_color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        instance_banner = d.pop("instance_banner", UNSET)

        accent_color = d.pop("accent_color", UNSET)

        get_instance_ui_response_200 = cls(
            instance_banner=instance_banner,
            accent_color=accent_color,
        )

        get_instance_ui_response_200.additional_properties = d
        return get_instance_ui_response_200

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
