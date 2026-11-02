from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RuntimeWorkspacePort")


@_attrs_define
class RuntimeWorkspacePort:
    """
    Attributes:
        port (int):
        forwardable (bool | Unset): Whether the listener accepts traffic addressed to the Runtime rather than loopback
            only. Omitted by older Runtime agents.
    """

    port: int
    forwardable: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        port = self.port

        forwardable = self.forwardable

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "port": port,
            }
        )
        if forwardable is not UNSET:
            field_dict["forwardable"] = forwardable

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        port = d.pop("port")

        forwardable = d.pop("forwardable", UNSET)

        runtime_workspace_port = cls(
            port=port,
            forwardable=forwardable,
        )

        return runtime_workspace_port
