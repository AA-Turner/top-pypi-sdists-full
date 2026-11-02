from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.runtime_workspace_operation_kind import RuntimeWorkspaceOperationKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="RuntimeWorkspaceOperationRequest")


@_attrs_define
class RuntimeWorkspaceOperationRequest:
    """
    Attributes:
        kind (RuntimeWorkspaceOperationKind):
        path (str | Unset):
        query (str | Unset):
        offset (int | Unset):
    """

    kind: RuntimeWorkspaceOperationKind
    path: str | Unset = UNSET
    query: str | Unset = UNSET
    offset: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        path = self.path

        query = self.query

        offset = self.offset

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if query is not UNSET:
            field_dict["query"] = query
        if offset is not UNSET:
            field_dict["offset"] = offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = RuntimeWorkspaceOperationKind(d.pop("kind"))

        path = d.pop("path", UNSET)

        query = d.pop("query", UNSET)

        offset = d.pop("offset", UNSET)

        runtime_workspace_operation_request = cls(
            kind=kind,
            path=path,
            query=query,
            offset=offset,
        )

        return runtime_workspace_operation_request
