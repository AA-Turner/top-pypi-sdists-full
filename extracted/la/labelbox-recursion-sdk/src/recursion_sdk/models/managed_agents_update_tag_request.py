from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsUpdateTagRequest")



@_attrs_define
class ManagedAgentsUpdateTagRequest:
    """ Request body for changing a tag definition. Every field is optional and tag applications remain unchanged.

        Example:
            {'color': '#14b8a6', 'description': 'example', 'label': 'example'}

        Attributes:
            color (str | Unset): Replacement display color in #RRGGBB form. Omit to keep the current color.
            description (str | Unset): Replacement description. Send an empty string to clear it; omit to keep the current
                description.
            label (str | Unset): Replacement display label. Leading and trailing whitespace is removed. Omit to keep the
                current label.
     """

    color: str | Unset = UNSET
    description: str | Unset = UNSET
    label: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        color = self.color

        description = self.description

        label = self.label


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if color is not UNSET:
            field_dict["color"] = color
        if description is not UNSET:
            field_dict["description"] = description
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = d.pop("color", UNSET)

        description = d.pop("description", UNSET)

        label = d.pop("label", UNSET)

        managed_agents_update_tag_request = cls(
            color=color,
            description=description,
            label=label,
        )


        managed_agents_update_tag_request.additional_properties = d
        return managed_agents_update_tag_request

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
