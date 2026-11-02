from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CloudAgentWorkspaceDeleteRequest")


@_attrs_define
class CloudAgentWorkspaceDeleteRequest:
    """
    Attributes:
        path (str):
        recursive (bool | Unset):  Default: False.
    """

    path: str
    recursive: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        recursive = self.recursive

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
            }
        )
        if recursive is not UNSET:
            field_dict["recursive"] = recursive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        recursive = d.pop("recursive", UNSET)

        cloud_agent_workspace_delete_request = cls(
            path=path,
            recursive=recursive,
        )

        return cloud_agent_workspace_delete_request
