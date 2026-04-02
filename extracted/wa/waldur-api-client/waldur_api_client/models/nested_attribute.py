from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.nested_attribute_type_enum import NestedAttributeTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_attribute_option import NestedAttributeOption


T = TypeVar("T", bound="NestedAttribute")


@_attrs_define
class NestedAttribute:
    """
    Attributes:
        key (Union[Unset, str]):
        title (Union[Unset, str]):
        type_ (Union[Unset, NestedAttributeTypeEnum]):
        options (Union[Unset, list['NestedAttributeOption']]):
        required (Union[Unset, bool]): A value must be provided for the attribute.
        default (Union[Unset, Any]):
    """

    key: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    type_: Union[Unset, NestedAttributeTypeEnum] = UNSET
    options: Union[Unset, list["NestedAttributeOption"]] = UNSET
    required: Union[Unset, bool] = UNSET
    default: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        title = self.title

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        options: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        required = self.required

        default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if title is not UNSET:
            field_dict["title"] = title
        if type_ is not UNSET:
            field_dict["type"] = type_
        if options is not UNSET:
            field_dict["options"] = options
        if required is not UNSET:
            field_dict["required"] = required
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_attribute_option import NestedAttributeOption

        d = dict(src_dict)
        key = d.pop("key", UNSET)

        title = d.pop("title", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, NestedAttributeTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = NestedAttributeTypeEnum(_type_)

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = NestedAttributeOption.from_dict(options_item_data)

            options.append(options_item)

        required = d.pop("required", UNSET)

        default = d.pop("default", UNSET)

        nested_attribute = cls(
            key=key,
            title=title,
            type_=type_,
            options=options,
            required=required,
            default=default,
        )

        nested_attribute.additional_properties = d
        return nested_attribute

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
