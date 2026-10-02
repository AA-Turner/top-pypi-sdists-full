from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsProbeMCPServerRequest")



@_attrs_define
class ManagedAgentsProbeMCPServerRequest:
    """ Request body for a live connection test against an MCP server, running the same credential resolution a session
    would. An unreachable server is reported in the response body, not as an HTTP error.

        Example:
            {'server_url': 'https://example.com', 'vault_ids': ['example']}

        Attributes:
            server_url (str): The MCP server to connect to. Must be http or https and must not embed credentials.
            vault_ids (list[str] | Unset): Vaults whose credentials may be used, scoped exactly as a session's grant is.
                Omit to probe unauthenticated.
     """

    server_url: str
    vault_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        server_url = self.server_url

        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "server_url": server_url,
        })
        if vault_ids is not UNSET:
            field_dict["vault_ids"] = vault_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        server_url = d.pop("server_url")

        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))


        managed_agents_probe_mcp_server_request = cls(
            server_url=server_url,
            vault_ids=vault_ids,
        )


        managed_agents_probe_mcp_server_request.additional_properties = d
        return managed_agents_probe_mcp_server_request

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
