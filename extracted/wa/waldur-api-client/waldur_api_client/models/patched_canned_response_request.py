from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedCannedResponseRequest")


@_attrs_define
class PatchedCannedResponseRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        text (Union[Unset, str]): Template text. Supports Django template syntax.
        category (Union[Unset, str]):
        is_active (Union[Unset, bool]):
    """

    name: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        text = self.text

        category = self.category

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if text is not UNSET:
            field_dict["text"] = text
        if category is not UNSET:
            field_dict["category"] = category
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        text = d.pop("text", UNSET)

        category = d.pop("category", UNSET)

        is_active = d.pop("is_active", UNSET)

        patched_canned_response_request = cls(
            name=name,
            text=text,
            category=category,
            is_active=is_active,
        )

        patched_canned_response_request.additional_properties = d
        return patched_canned_response_request

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
