from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_memory_store_attachment_access import ManagedAgentsMemoryStoreAttachmentAccess
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsMemoryStoreAttachment")



@_attrs_define
class ManagedAgentsMemoryStoreAttachment:
    """ One memory store bound to a session at creation time, with the access it is granted.

        Example:
            {'access': 'read_only', 'instructions': 'example', 'memory_store_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            memory_store_id (str): Store to attach.
            access (ManagedAgentsMemoryStoreAttachmentAccess | Unset): How the session may use the store. Defaults to
                read_only.
            instructions (str | Unset): Session-specific guidance on using this store, shown to the agent beside its name
                and description. Capped at 4096 characters.
     """

    memory_store_id: str
    access: ManagedAgentsMemoryStoreAttachmentAccess | Unset = UNSET
    instructions: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        memory_store_id = self.memory_store_id

        access: str | Unset = UNSET
        if not isinstance(self.access, Unset):
            access = self.access.value


        instructions = self.instructions


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "memory_store_id": memory_store_id,
        })
        if access is not UNSET:
            field_dict["access"] = access
        if instructions is not UNSET:
            field_dict["instructions"] = instructions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        memory_store_id = d.pop("memory_store_id")

        _access = d.pop("access", UNSET)
        access: ManagedAgentsMemoryStoreAttachmentAccess | Unset
        if isinstance(_access,  Unset):
            access = UNSET
        else:
            access = ManagedAgentsMemoryStoreAttachmentAccess(_access)




        instructions = d.pop("instructions", UNSET)

        managed_agents_memory_store_attachment = cls(
            memory_store_id=memory_store_id,
            access=access,
            instructions=instructions,
        )


        managed_agents_memory_store_attachment.additional_properties = d
        return managed_agents_memory_store_attachment

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
