from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.runtime_workspace_file_kind import RuntimeWorkspaceFileKind

T = TypeVar("T", bound="RuntimeWorkspaceFileEntry")


@_attrs_define
class RuntimeWorkspaceFileEntry:
    """
    Attributes:
        name (str):
        path (str):
        kind (RuntimeWorkspaceFileKind):
        size (int):
    """

    name: str
    path: str
    kind: RuntimeWorkspaceFileKind
    size: int

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        path = self.path

        kind = self.kind.value

        size = self.size

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "path": path,
                "kind": kind,
                "size": size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        path = d.pop("path")

        kind = RuntimeWorkspaceFileKind(d.pop("kind"))

        size = d.pop("size")

        runtime_workspace_file_entry = cls(
            name=name,
            path=path,
            kind=kind,
            size=size,
        )

        return runtime_workspace_file_entry
