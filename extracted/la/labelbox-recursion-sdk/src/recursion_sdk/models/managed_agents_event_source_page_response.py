from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_event_source_summary import ManagedAgentsEventSourceSummary





T = TypeVar("T", bound="ManagedAgentsEventSourcePageResponse")



@_attrs_define
class ManagedAgentsEventSourcePageResponse:
    """ Bounded page of event sources owned by the calling workspace.

        Example:
            {'items': [{'createdAt': '2026-02-18T09:30:00Z', 'delivery': {'kind': 'webhook', 'webhookUrl': 'example'},
                'displayName': 'example', 'eventSourceId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'revision': 1, 'status':
                'paused', 'type': 'slack_events_api', 'updatedAt': '2026-02-18T09:30:00Z'}], 'nextCursor': 'example', 'total':
                1}

        Attributes:
            items (list[ManagedAgentsEventSourceSummary]): Event sources in newest-first order.
            next_cursor (None | str): Opaque cursor for the next page, or null when this is the last page.
            total (int): Total event sources visible to the caller.
     """

    items: list[ManagedAgentsEventSourceSummary]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_event_source_summary import ManagedAgentsEventSourceSummary # noqa: PLC0415
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
        from ..models.managed_agents_event_source_summary import ManagedAgentsEventSourceSummary # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ManagedAgentsEventSourceSummary.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        managed_agents_event_source_page_response = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return managed_agents_event_source_page_response

