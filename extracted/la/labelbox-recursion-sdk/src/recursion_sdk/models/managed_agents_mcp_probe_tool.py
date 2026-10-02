from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsMCPProbeTool")



@_attrs_define
class ManagedAgentsMCPProbeTool:
    """ One tool advertised by a probed MCP server, reported verbatim from its tools/list response. Appears only inside
    MCPProbeResponse.tools; the service does not persist or validate these entries, so their presence proves the server
    answered, not that the tool works.

        Example:
            {'description': 'example', 'name': 'example-name'}

        Attributes:
            name (str): The tool name as the MCP server reported it, which is the name an agent would call it by.
            description (str | Unset): The tool's own self-description as returned by the server, passed through verbatim.
                Absent when the server advertised the tool without one.
     """

    name: str
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
        })
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        managed_agents_mcp_probe_tool = cls(
            name=name,
            description=description,
        )


        managed_agents_mcp_probe_tool.additional_properties = d
        return managed_agents_mcp_probe_tool

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
