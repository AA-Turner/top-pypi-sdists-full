from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.reaped_run_config_page_dto_items_item import ReapedRunConfigPageDtoItemsItem





T = TypeVar("T", bound="ReapedRunConfigPageDto")



@_attrs_define
class ReapedRunConfigPageDto:
    """ A single page of soft-deleted run configs at a scope, ordered newest-deleted first.

        Example:
            {'items': [{'id': '48eabce5-62a9-4356-9614-2de7d1b487a3', 'scope': {'level': 'env', 'id':
                '784e2386-e297-4f9d-a886-838422383b65'}, 'type': 'agent-harness', 'name': 'claude-sonnet-baseline',
                'description': 'Baseline Claude Sonnet solver harness for the vision-agent-eval environment.',
                'defaultRunConfigVersionId': None, 'tags': ['baseline'], 'createdByUserId':
                '49dea803-7390-49c4-abb1-5629718fc9cd', 'updatedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'createdAt':
                '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z', 'deletedAt': '2026-01-20T11:05:00.000Z',
                'deletedReason': 'unused_unbound', 'deletedBy': None}], 'nextCursor': None, 'total': 1}

        Attributes:
            items (list[ReapedRunConfigPageDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[ReapedRunConfigPageDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.reaped_run_config_page_dto_items_item import ReapedRunConfigPageDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        next_cursor: None | str
        next_cursor = self.next_cursor

        total = self.total


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "nextCursor": next_cursor,
            "total": total,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reaped_run_config_page_dto_items_item import ReapedRunConfigPageDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ReapedRunConfigPageDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        reaped_run_config_page_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return reaped_run_config_page_dto

