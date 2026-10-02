from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsDisclosureEntry")



@_attrs_define
class ManagedAgentsDisclosureEntry:
    """ One attached skill as a turn's prompt will list it, and whether the budget left room for its description. An entry
    without one still activates, but the model has only the name to decide with.

        Example:
            {'description_included': True, 'name': 'example-name'}

        Attributes:
            description_included (bool): False when the budget was exhausted before this skill and it is listed by name
                only.
            name (str): The skill's name, as the model sees it.
     """

    description_included: bool
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        description_included = self.description_included

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "description_included": description_included,
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description_included = d.pop("description_included")

        name = d.pop("name")

        managed_agents_disclosure_entry = cls(
            description_included=description_included,
            name=name,
        )


        managed_agents_disclosure_entry.additional_properties = d
        return managed_agents_disclosure_entry

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
