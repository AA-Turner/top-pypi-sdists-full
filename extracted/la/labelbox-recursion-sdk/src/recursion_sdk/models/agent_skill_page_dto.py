from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.agent_skill_page_dto_items_item import AgentSkillPageDtoItemsItem





T = TypeVar("T", bound="AgentSkillPageDto")



@_attrs_define
class AgentSkillPageDto:
    """ Cursor-paginated page of agent skills (org skills plus platform skills).

        Example:
            {'items': [{'id': 'a7b8c9d0-e1f2-4a3b-8c4d-5e6f708192a3', 'organizationId':
                '3f1a2b6c-4d5e-4f7a-8b9c-0d1e2f3a4b5c', 'slug': 'xlsx', 'name': 'Excel / spreadsheet helpers', 'description':
                'Read and write .xlsx workbooks from the agent workspace.', 'fileId': 'b8c9d0e1-f2a3-4b4c-9d5e-6f708192a3b4',
                'createdAt': '2026-07-03T08:00:00.000Z', 'updatedAt': '2026-07-03T08:15:00.000Z'}], 'nextCursor': None, 'total':
                1}

        Attributes:
            items (list[AgentSkillPageDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[AgentSkillPageDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_skill_page_dto_items_item import AgentSkillPageDtoItemsItem # noqa: PLC0415
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
        from ..models.agent_skill_page_dto_items_item import AgentSkillPageDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = AgentSkillPageDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        agent_skill_page_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return agent_skill_page_dto

