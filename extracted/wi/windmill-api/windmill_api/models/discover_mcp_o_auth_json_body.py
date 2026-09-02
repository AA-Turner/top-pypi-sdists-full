from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DiscoverMcpOAuthJsonBody")


@_attrs_define
class DiscoverMcpOAuthJsonBody:
    """
    Attributes:
        mcp_server_url (str): URL of the MCP server to discover OAuth metadata from
    """

    mcp_server_url: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mcp_server_url = self.mcp_server_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mcp_server_url": mcp_server_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mcp_server_url = d.pop("mcp_server_url")

        discover_mcp_o_auth_json_body = cls(
            mcp_server_url=mcp_server_url,
        )

        discover_mcp_o_auth_json_body.additional_properties = d
        return discover_mcp_o_auth_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
