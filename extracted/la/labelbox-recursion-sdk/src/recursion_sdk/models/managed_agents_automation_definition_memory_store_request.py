from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_definition_memory_store_request_access import ManagedAgentsAutomationDefinitionMemoryStoreRequestAccess
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionMemoryStoreRequest")



@_attrs_define
class ManagedAgentsAutomationDefinitionMemoryStoreRequest:
    """ A memory store attached to each automation session with explicit access and optional instructions.

        Example:
            {'access': 'read_only', 'instructions': 'example', 'memoryStoreId': 'example'}

        Attributes:
            access (ManagedAgentsAutomationDefinitionMemoryStoreRequestAccess): Access to the attached memory store.
            memory_store_id (str): Active memory store in this workspace.
            instructions (str | Unset): Instructions for using this memory store.
     """

    access: ManagedAgentsAutomationDefinitionMemoryStoreRequestAccess
    memory_store_id: str
    instructions: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        access = self.access.value

        memory_store_id = self.memory_store_id

        instructions = self.instructions


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "access": access,
            "memoryStoreId": memory_store_id,
        })
        if instructions is not UNSET:
            field_dict["instructions"] = instructions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access = ManagedAgentsAutomationDefinitionMemoryStoreRequestAccess(d.pop("access"))




        memory_store_id = d.pop("memoryStoreId")

        instructions = d.pop("instructions", UNSET)

        managed_agents_automation_definition_memory_store_request = cls(
            access=access,
            memory_store_id=memory_store_id,
            instructions=instructions,
        )

        return managed_agents_automation_definition_memory_store_request

