from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_list_entry import ManagedAgentsListEntry





T = TypeVar("T", bound="ManagedAgentsMemoryListResponse")



@_attrs_define
class ManagedAgentsMemoryListResponse:
    """ One level of a memory store's namespace: memories and the prefixes standing for the paths beneath them.

        Example:
            {'entries': [{'byte_size': 1, 'count': 1, 'path': 'example', 'summary': 'example', 'type': 'memory'}]}

        Attributes:
            entries (list[ManagedAgentsListEntry] | None): Memories and directory prefixes under the requested path,
                interleaved in path order.
     """

    entries: list[ManagedAgentsListEntry] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_list_entry import ManagedAgentsListEntry # noqa: PLC0415
        entries: list[dict[str, Any]] | None
        if isinstance(self.entries, list):
            entries = []
            for entries_type_0_item_data in self.entries:
                entries_type_0_item = entries_type_0_item_data.to_dict()
                entries.append(entries_type_0_item)


        else:
            entries = self.entries


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "entries": entries,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_list_entry import ManagedAgentsListEntry # noqa: PLC0415
        d = dict(src_dict)
        def _parse_entries(data: object) -> list[ManagedAgentsListEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entries_type_0 = []
                _entries_type_0 = data
                for entries_type_0_item_data in (_entries_type_0):
                    entries_type_0_item = ManagedAgentsListEntry.from_dict(entries_type_0_item_data)



                    entries_type_0.append(entries_type_0_item)

                return entries_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsListEntry] | None, data)

        entries = _parse_entries(d.pop("entries"))


        managed_agents_memory_list_response = cls(
            entries=entries,
        )


        managed_agents_memory_list_response.additional_properties = d
        return managed_agents_memory_list_response

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
