from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsBuiltInIntegrationRequest")



@_attrs_define
class ManagedAgentsBuiltInIntegrationRequest:
    """ One admin-configured vendor integration an agent may use, named by its organization connection. The connection row
    carries the vendor and the tools its agents may call; the agent inherits both.

        Example:
            {'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}

        Attributes:
            connection_id (str | Unset): Organization integration connection (UUID) the agent may use. Must belong to the
                caller's organization, use a provider that serves built-in integrations (merge), and be active.
            tools (list[str] | Unset): Reserved for per-agent narrowing below the connection's admin allow-list. Must be
                omitted or empty today; the agent inherits the connection's full allow-list.
     """

    connection_id: str | Unset = UNSET
    tools: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        connection_id = self.connection_id

        tools: list[str] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = self.tools




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if connection_id is not UNSET:
            field_dict["connection_id"] = connection_id
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = d.pop("connection_id", UNSET)

        tools = cast(list[str], d.pop("tools", UNSET))


        managed_agents_built_in_integration_request = cls(
            connection_id=connection_id,
            tools=tools,
        )


        managed_agents_built_in_integration_request.additional_properties = d
        return managed_agents_built_in_integration_request

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
