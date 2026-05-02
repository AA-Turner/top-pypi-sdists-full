from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.edit_ducklake_config_json_body_settings import EditDucklakeConfigJsonBodySettings


T = TypeVar("T", bound="EditDucklakeConfigJsonBody")


@_attrs_define
class EditDucklakeConfigJsonBody:
    """
    Attributes:
        settings (EditDucklakeConfigJsonBodySettings):
    """

    settings: "EditDucklakeConfigJsonBodySettings"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        settings = self.settings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings": settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_ducklake_config_json_body_settings import EditDucklakeConfigJsonBodySettings

        d = src_dict.copy()
        settings = EditDucklakeConfigJsonBodySettings.from_dict(d.pop("settings"))

        edit_ducklake_config_json_body = cls(
            settings=settings,
        )

        edit_ducklake_config_json_body.additional_properties = d
        return edit_ducklake_config_json_body

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
