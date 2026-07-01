from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.t_expose_spec_category import TExposeSpecCategory
from ..models.t_expose_spec_interface import TExposeSpecInterface
from ..types import UNSET, Unset

T = TypeVar("T", bound="TExposeSpec")


@_attrs_define
class TExposeSpec:
    """
    Attributes:
        category (TExposeSpecCategory | Unset):
        display_name (str | Unset):
        interface (TExposeSpecInterface | Unset):
        manual (bool | Unset):
        starred (bool | Unset):
        tags (list[str] | str | Unset):
    """

    category: TExposeSpecCategory | Unset = UNSET
    display_name: str | Unset = UNSET
    interface: TExposeSpecInterface | Unset = UNSET
    manual: bool | Unset = UNSET
    starred: bool | Unset = UNSET
    tags: list[str] | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category: str | Unset = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        display_name = self.display_name

        interface: str | Unset = UNSET
        if not isinstance(self.interface, Unset):
            interface = self.interface.value

        manual = self.manual

        starred = self.starred

        tags: list[str] | str | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if category is not UNSET:
            field_dict["category"] = category
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if interface is not UNSET:
            field_dict["interface"] = interface
        if manual is not UNSET:
            field_dict["manual"] = manual
        if starred is not UNSET:
            field_dict["starred"] = starred
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _category = d.pop("category", UNSET)
        category: TExposeSpecCategory | Unset
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = TExposeSpecCategory(_category)

        display_name = d.pop("display_name", UNSET)

        _interface = d.pop("interface", UNSET)
        interface: TExposeSpecInterface | Unset
        if isinstance(_interface, Unset):
            interface = UNSET
        else:
            interface = TExposeSpecInterface(_interface)

        manual = d.pop("manual", UNSET)

        starred = d.pop("starred", UNSET)

        def _parse_tags(data: object) -> list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_1 = cast(list[str], data)

                return tags_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        t_expose_spec = cls(
            category=category,
            display_name=display_name,
            interface=interface,
            manual=manual,
            starred=starred,
            tags=tags,
        )

        t_expose_spec.additional_properties = d
        return t_expose_spec

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
