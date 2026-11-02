from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RuntimeWorkspaceSearchMatch")


@_attrs_define
class RuntimeWorkspaceSearchMatch:
    """
    Attributes:
        path (str):
        line (int):
        preview (str):
    """

    path: str
    line: int
    preview: str

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        line = self.line

        preview = self.preview

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
                "line": line,
                "preview": preview,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        line = d.pop("line")

        preview = d.pop("preview")

        runtime_workspace_search_match = cls(
            path=path,
            line=line,
            preview=preview,
        )

        return runtime_workspace_search_match
