from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.permission_description_option import PermissionDescriptionOption


T = TypeVar("T", bound="PermissionDescription")


@_attrs_define
class PermissionDescription:
    """
    Attributes:
        label (str): Category name
        options (list['PermissionDescriptionOption']): List of permissions in this category
    """

    label: str
    options: list["PermissionDescriptionOption"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()
            options.append(options_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "options": options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission_description_option import PermissionDescriptionOption

        d = dict(src_dict)
        label = d.pop("label")

        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = PermissionDescriptionOption.from_dict(options_item_data)

            options.append(options_item)

        permission_description = cls(
            label=label,
            options=options,
        )

        permission_description.additional_properties = d
        return permission_description

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
