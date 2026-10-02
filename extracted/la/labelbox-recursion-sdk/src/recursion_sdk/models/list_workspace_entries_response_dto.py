from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.list_workspace_entries_response_dto_items_item import ListWorkspaceEntriesResponseDtoItemsItem





T = TypeVar("T", bound="ListWorkspaceEntriesResponseDto")



@_attrs_define
class ListWorkspaceEntriesResponseDto:
    """ One page of a run workspace directory listing under output/.

        Example:
            {'items': [{'name': 'reports', 'path': 'reports', 'type': 'directory', 'sizeBytes': None}, {'name': 'defect-
                report.json', 'path': 'defect-report.json', 'type': 'file', 'sizeBytes': 2048}], 'nextCursor': None,
                'workspaceAvailable': True, 'directoryTruncated': False}

        Attributes:
            items (list[ListWorkspaceEntriesResponseDtoItemsItem]): Entries in this page, directories first then files, each
                sorted by name.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            workspace_available (bool): False when the live workspace can no longer be listed (retention window elapsed, run
                unknown, or the directory is gone). Items are empty in that case; fall back to the persisted output files.
            directory_truncated (bool): True when the directory holds more entries than the server-side listing buffer;
                entries beyond the buffer are not reachable through pagination.
     """

    items: list[ListWorkspaceEntriesResponseDtoItemsItem]
    next_cursor: None | str
    workspace_available: bool
    directory_truncated: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.list_workspace_entries_response_dto_items_item import ListWorkspaceEntriesResponseDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        next_cursor: None | str
        next_cursor = self.next_cursor

        workspace_available = self.workspace_available

        directory_truncated = self.directory_truncated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "nextCursor": next_cursor,
            "workspaceAvailable": workspace_available,
            "directoryTruncated": directory_truncated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_workspace_entries_response_dto_items_item import ListWorkspaceEntriesResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ListWorkspaceEntriesResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        workspace_available = d.pop("workspaceAvailable")

        directory_truncated = d.pop("directoryTruncated")

        list_workspace_entries_response_dto = cls(
            items=items,
            next_cursor=next_cursor,
            workspace_available=workspace_available,
            directory_truncated=directory_truncated,
        )

        return list_workspace_entries_response_dto

