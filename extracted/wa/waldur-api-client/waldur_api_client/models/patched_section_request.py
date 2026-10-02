from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedSectionRequest")


@_attrs_define
class PatchedSectionRequest:
    """
    Attributes:
        key (Union[Unset, str]):
        title (Union[Unset, str]):
        category (Union[Unset, str]):
        is_standalone (Union[Unset, bool]): Whether section is rendered as a separate tab.
    """

    key: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    is_standalone: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        title = self.title

        category = self.category

        is_standalone = self.is_standalone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if title is not UNSET:
            field_dict["title"] = title
        if category is not UNSET:
            field_dict["category"] = category
        if is_standalone is not UNSET:
            field_dict["is_standalone"] = is_standalone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key", UNSET)

        title = d.pop("title", UNSET)

        category = d.pop("category", UNSET)

        is_standalone = d.pop("is_standalone", UNSET)

        patched_section_request = cls(
            key=key,
            title=title,
            category=category,
            is_standalone=is_standalone,
        )

        patched_section_request.additional_properties = d
        return patched_section_request

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
