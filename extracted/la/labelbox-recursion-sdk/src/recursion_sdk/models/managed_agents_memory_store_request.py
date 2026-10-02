from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsMemoryStoreRequest")



@_attrs_define
class ManagedAgentsMemoryStoreRequest:
    """ Fields for creating or renaming a curated memory store. An omitted field is left unchanged on update.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'description': 'example', 'name': 'example-name'}

        Attributes:
            agent_id (str | Unset): Scope the store to one agent. Omit for a workspace store any session may attach.
            description (str | Unset): What this store contains. Disclosed to the agent in every session the store is
                attached to, so write it as what the agent would be looking for.
            name (str | Unset): Human-readable name. Shown to the agent as part of the store's note.
     """

    agent_id: str | Unset = UNSET
    description: str | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        description = self.description

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        managed_agents_memory_store_request = cls(
            agent_id=agent_id,
            description=description,
            name=name,
        )


        managed_agents_memory_store_request.additional_properties = d
        return managed_agents_memory_store_request

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
