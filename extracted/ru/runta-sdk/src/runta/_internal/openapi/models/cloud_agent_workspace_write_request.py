from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CloudAgentWorkspaceWriteRequest")


@_attrs_define
class CloudAgentWorkspaceWriteRequest:
    """
    Attributes:
        path (str):
        content_base64 (str):
    """

    path: str
    content_base64: str

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        content_base64 = self.content_base64

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
                "content_base64": content_base64,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        content_base64 = d.pop("content_base64")

        cloud_agent_workspace_write_request = cls(
            path=path,
            content_base64=content_base64,
        )

        return cloud_agent_workspace_write_request
