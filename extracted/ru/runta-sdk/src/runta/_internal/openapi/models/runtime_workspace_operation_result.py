from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.runtime_workspace_operation_kind import RuntimeWorkspaceOperationKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.runtime_workspace_file_entry import RuntimeWorkspaceFileEntry
    from ..models.runtime_workspace_port import RuntimeWorkspacePort
    from ..models.runtime_workspace_search_match import RuntimeWorkspaceSearchMatch


T = TypeVar("T", bound="RuntimeWorkspaceOperationResult")


@_attrs_define
class RuntimeWorkspaceOperationResult:
    """
    Attributes:
        kind (RuntimeWorkspaceOperationKind):
        entries (list[RuntimeWorkspaceFileEntry]):
        matches (list[RuntimeWorkspaceSearchMatch]):
        ports (list[RuntimeWorkspacePort]):
        truncated (bool):
        text (str | Unset):
        media_base64 (str | Unset):
        media_type (str | Unset):
        next_offset (int | Unset):
    """

    kind: RuntimeWorkspaceOperationKind
    entries: list[RuntimeWorkspaceFileEntry]
    matches: list[RuntimeWorkspaceSearchMatch]
    ports: list[RuntimeWorkspacePort]
    truncated: bool
    text: str | Unset = UNSET
    media_base64: str | Unset = UNSET
    media_type: str | Unset = UNSET
    next_offset: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        matches = []
        for matches_item_data in self.matches:
            matches_item = matches_item_data.to_dict()
            matches.append(matches_item)

        ports = []
        for ports_item_data in self.ports:
            ports_item = ports_item_data.to_dict()
            ports.append(ports_item)

        truncated = self.truncated

        text = self.text

        media_base64 = self.media_base64

        media_type = self.media_type

        next_offset = self.next_offset

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "entries": entries,
                "matches": matches,
                "ports": ports,
                "truncated": truncated,
            }
        )
        if text is not UNSET:
            field_dict["text"] = text
        if media_base64 is not UNSET:
            field_dict["media_base64"] = media_base64
        if media_type is not UNSET:
            field_dict["media_type"] = media_type
        if next_offset is not UNSET:
            field_dict["next_offset"] = next_offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.runtime_workspace_file_entry import RuntimeWorkspaceFileEntry
        from ..models.runtime_workspace_port import RuntimeWorkspacePort
        from ..models.runtime_workspace_search_match import RuntimeWorkspaceSearchMatch

        d = dict(src_dict)
        kind = RuntimeWorkspaceOperationKind(d.pop("kind"))

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = RuntimeWorkspaceFileEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        matches = []
        _matches = d.pop("matches")
        for matches_item_data in _matches:
            matches_item = RuntimeWorkspaceSearchMatch.from_dict(matches_item_data)

            matches.append(matches_item)

        ports = []
        _ports = d.pop("ports")
        for ports_item_data in _ports:
            ports_item = RuntimeWorkspacePort.from_dict(ports_item_data)

            ports.append(ports_item)

        truncated = d.pop("truncated")

        text = d.pop("text", UNSET)

        media_base64 = d.pop("media_base64", UNSET)

        media_type = d.pop("media_type", UNSET)

        next_offset = d.pop("next_offset", UNSET)

        runtime_workspace_operation_result = cls(
            kind=kind,
            entries=entries,
            matches=matches,
            ports=ports,
            truncated=truncated,
            text=text,
            media_base64=media_base64,
            media_type=media_type,
            next_offset=next_offset,
        )

        return runtime_workspace_operation_result
