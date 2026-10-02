from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsCatalogTool")



@_attrs_define
class ManagedAgentsCatalogTool:
    """ One tool exposed by a Merge connector. A read-only, non-destructive classification admits it to the read preset; the
    write preset admits every catalog tool and stores all others at write level.

        Example:
            {'description': 'example', 'destructive': True, 'name': 'example-name', 'read_only': True}

        Attributes:
            destructive (bool): Merge classifies the tool as destructive: it updates or deletes vendor data.
            name (str): Tool name as the connector exposes it, e.g. get_issue. What a registration's resources name.
            read_only (bool): Merge classifies the tool as read-only. Only a tool with this flag and without destructive
                qualifies for a read permission preset; an unclassified tool does not.
            description (str | Unset): Merge's description of the tool.
     """

    destructive: bool
    name: str
    read_only: bool
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        destructive = self.destructive

        name = self.name

        read_only = self.read_only

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "destructive": destructive,
            "name": name,
            "read_only": read_only,
        })
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        destructive = d.pop("destructive")

        name = d.pop("name")

        read_only = d.pop("read_only")

        description = d.pop("description", UNSET)

        managed_agents_catalog_tool = cls(
            destructive=destructive,
            name=name,
            read_only=read_only,
            description=description,
        )


        managed_agents_catalog_tool.additional_properties = d
        return managed_agents_catalog_tool

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
