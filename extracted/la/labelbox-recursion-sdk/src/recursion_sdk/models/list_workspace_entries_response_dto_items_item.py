from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.list_workspace_entries_response_dto_items_item_type import ListWorkspaceEntriesResponseDtoItemsItemType
from typing import cast






T = TypeVar("T", bound="ListWorkspaceEntriesResponseDtoItemsItem")



@_attrs_define
class ListWorkspaceEntriesResponseDtoItemsItem:
    """ One file or directory in a run's live output workspace.

        Attributes:
            name (str): Entry name within its parent directory.
            path (str): Path of the entry relative to the run's output directory (e.g. core/report.md).
            type_ (ListWorkspaceEntriesResponseDtoItemsItemType): Whether the entry is a file or a directory.
            size_bytes (int | None): File size in bytes. Null for directories or when the size is unknown.
     """

    name: str
    path: str
    type_: ListWorkspaceEntriesResponseDtoItemsItemType
    size_bytes: int | None





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        path = self.path

        type_ = self.type_.value

        size_bytes: int | None
        size_bytes = self.size_bytes


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "path": path,
            "type": type_,
            "sizeBytes": size_bytes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        path = d.pop("path")

        type_ = ListWorkspaceEntriesResponseDtoItemsItemType(d.pop("type"))




        def _parse_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size_bytes = _parse_size_bytes(d.pop("sizeBytes"))


        list_workspace_entries_response_dto_items_item = cls(
            name=name,
            path=path,
            type_=type_,
            size_bytes=size_bytes,
        )

        return list_workspace_entries_response_dto_items_item

