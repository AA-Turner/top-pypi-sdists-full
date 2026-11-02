from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="CloudAgentVncSessionChannel")


@_attrs_define
class CloudAgentVncSessionChannel:
    """
    Attributes:
        websocket_url (str):
        protocols (list[str]):
    """

    websocket_url: str
    protocols: list[str]

    def to_dict(self) -> dict[str, Any]:
        websocket_url = self.websocket_url

        protocols = self.protocols

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "websocket_url": websocket_url,
                "protocols": protocols,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        websocket_url = d.pop("websocket_url")

        protocols = cast(list[str], d.pop("protocols"))

        cloud_agent_vnc_session_channel = cls(
            websocket_url=websocket_url,
            protocols=protocols,
        )

        return cloud_agent_vnc_session_channel
