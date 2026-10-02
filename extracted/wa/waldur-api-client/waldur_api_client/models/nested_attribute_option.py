from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedAttributeOption")


@_attrs_define
class NestedAttributeOption:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        key (Union[Unset, str]):
        title (Union[Unset, str]):
        is_default (Union[Unset, bool]): Return True if this option is the default for its attribute.
    """

    uuid: Union[Unset, UUID] = UNSET
    key: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    is_default: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        key = self.key

        title = self.title

        is_default = self.is_default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if key is not UNSET:
            field_dict["key"] = key
        if title is not UNSET:
            field_dict["title"] = title
        if is_default is not UNSET:
            field_dict["is_default"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        key = d.pop("key", UNSET)

        title = d.pop("title", UNSET)

        is_default = d.pop("is_default", UNSET)

        nested_attribute_option = cls(
            uuid=uuid,
            key=key,
            title=title,
            is_default=is_default,
        )

        nested_attribute_option.additional_properties = d
        return nested_attribute_option

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
