from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_agent_version_toolsets_type_0_item_type import ManagedAgentsAgentVersionToolsetsType0ItemType






T = TypeVar("T", bound="ManagedAgentsAgentVersionToolsetsType0Item")



@_attrs_define
class ManagedAgentsAgentVersionToolsetsType0Item:
    """ 
        Attributes:
            type_ (ManagedAgentsAgentVersionToolsetsType0ItemType): The evaluation marker is the only supported toolset
                type.
     """

    type_: ManagedAgentsAgentVersionToolsetsType0ItemType





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ManagedAgentsAgentVersionToolsetsType0ItemType(d.pop("type"))




        managed_agents_agent_version_toolsets_type_0_item = cls(
            type_=type_,
        )

        return managed_agents_agent_version_toolsets_type_0_item

