from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ducklake_settings_ducklakes import DucklakeSettingsDucklakes


T = TypeVar("T", bound="DucklakeSettings")


@_attrs_define
class DucklakeSettings:
    """
    Attributes:
        ducklakes (DucklakeSettingsDucklakes):
    """

    ducklakes: "DucklakeSettingsDucklakes"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ducklakes = self.ducklakes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ducklakes": ducklakes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ducklake_settings_ducklakes import DucklakeSettingsDucklakes

        d = src_dict.copy()
        ducklakes = DucklakeSettingsDucklakes.from_dict(d.pop("ducklakes"))

        ducklake_settings = cls(
            ducklakes=ducklakes,
        )

        ducklake_settings.additional_properties = d
        return ducklake_settings

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
