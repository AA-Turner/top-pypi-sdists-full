from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.settings_item_default import SettingsItemDefault
    from ..models.settings_item_option import SettingsItemOption


T = TypeVar("T", bound="SettingsItem")


@_attrs_define
class SettingsItem:
    """
    Attributes:
        key (str):
        description (str):
        type_ (str):
        default (Union[Unset, SettingsItemDefault]):
        options (Union[Unset, list['SettingsItemOption']]):
    """

    key: str
    description: str
    type_: str
    default: Union[Unset, "SettingsItemDefault"] = UNSET
    options: Union[Unset, list["SettingsItemOption"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        description = self.description

        type_ = self.type_

        default: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default, Unset):
            default = self.default.to_dict()

        options: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "description": description,
                "type": type_,
            }
        )
        if default is not UNSET:
            field_dict["default"] = default
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.settings_item_default import SettingsItemDefault
        from ..models.settings_item_option import SettingsItemOption

        d = dict(src_dict)
        key = d.pop("key")

        description = d.pop("description")

        type_ = d.pop("type")

        _default = d.pop("default", UNSET)
        default: Union[Unset, SettingsItemDefault]
        if isinstance(_default, Unset):
            default = UNSET
        else:
            default = SettingsItemDefault.from_dict(_default)

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = SettingsItemOption.from_dict(options_item_data)

            options.append(options_item)

        settings_item = cls(
            key=key,
            description=description,
            type_=type_,
            default=default,
            options=options,
        )

        settings_item.additional_properties = d
        return settings_item

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
