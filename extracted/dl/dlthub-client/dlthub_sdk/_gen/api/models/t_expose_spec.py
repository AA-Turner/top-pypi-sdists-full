from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.t_expose_spec_category_type_0 import TExposeSpecCategoryType0
from ..models.t_expose_spec_interface_type_0 import TExposeSpecInterfaceType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_job_object_input import TJobObjectInput


T = TypeVar("T", bound="TExposeSpec")


@_attrs_define
class TExposeSpec:
    """
    Attributes:
        category (str | TExposeSpecCategoryType0 | Unset):
        display_name (str | Unset):
        interface (str | TExposeSpecInterfaceType0 | Unset):
        manual (bool | Unset):
        object_input (TJobObjectInput | Unset):
        starred (bool | Unset):
        tags (list[str] | str | Unset):
    """

    category: str | TExposeSpecCategoryType0 | Unset = UNSET
    display_name: str | Unset = UNSET
    interface: str | TExposeSpecInterfaceType0 | Unset = UNSET
    manual: bool | Unset = UNSET
    object_input: TJobObjectInput | Unset = UNSET
    starred: bool | Unset = UNSET
    tags: list[str] | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category: str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        elif isinstance(self.category, TExposeSpecCategoryType0):
            category = self.category.value
        else:
            category = self.category

        display_name = self.display_name

        interface: str | Unset
        if isinstance(self.interface, Unset):
            interface = UNSET
        elif isinstance(self.interface, TExposeSpecInterfaceType0):
            interface = self.interface.value
        else:
            interface = self.interface

        manual = self.manual

        object_input: dict[str, Any] | Unset = UNSET
        if not isinstance(self.object_input, Unset):
            object_input = self.object_input.to_dict()

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
        if object_input is not UNSET:
            field_dict["object_input"] = object_input
        if starred is not UNSET:
            field_dict["starred"] = starred
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.t_job_object_input import TJobObjectInput

        d = dict(src_dict)

        def _parse_category(data: object) -> str | TExposeSpecCategoryType0 | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_type_0 = TExposeSpecCategoryType0(data)

                return category_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | TExposeSpecCategoryType0 | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        display_name = d.pop("display_name", UNSET)

        def _parse_interface(data: object) -> str | TExposeSpecInterfaceType0 | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interface_type_0 = TExposeSpecInterfaceType0(data)

                return interface_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | TExposeSpecInterfaceType0 | Unset, data)

        interface = _parse_interface(d.pop("interface", UNSET))

        manual = d.pop("manual", UNSET)

        _object_input = d.pop("object_input", UNSET)
        object_input: TJobObjectInput | Unset
        if isinstance(_object_input, Unset):
            object_input = UNSET
        else:
            object_input = TJobObjectInput.from_dict(_object_input)

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
            object_input=object_input,
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
