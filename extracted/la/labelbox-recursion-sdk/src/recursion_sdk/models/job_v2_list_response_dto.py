from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.job_v2_list_response_dto_items_item import JobV2ListResponseDtoItemsItem





T = TypeVar("T", bound="JobV2ListResponseDto")



@_attrs_define
class JobV2ListResponseDto:
    """ Paginated list of jobs_v2 rows for a scope.

        Example:
            {'items': [{'id': '11111111-1111-4111-8111-111111111111', 'parentJobId': None, 'userId':
                '11111111-1111-4111-8111-111111111111', 'type': 'run_config_run', 'name': 'grpo-trainer-run', 'status':
                'executing', 'payload': {}, 'externalState': None, 'output': None, 'errorMessage': None, 'attempts': 1,
                'maxAttempts': 1, 'scheduledAt': '2026-01-01T00:00:00.000Z', 'pollAfter': None, 'startedAt':
                '2026-01-01T00:00:01.000Z', 'completedAt': None, 'createdAt': '2026-01-01T00:00:00.000Z', 'updatedAt':
                '2026-01-01T00:00:01.000Z'}], 'nextCursor': None, 'total': 1}

        Attributes:
            items (list[JobV2ListResponseDtoItemsItem]): Jobs_v2 rows on the current page.
            next_cursor (None | str): Opaque cursor for fetching the next page. Null when there are no more rows.
            total (int | Unset): Total row count for the query when the backend chose to compute it.
     """

    items: list[JobV2ListResponseDtoItemsItem]
    next_cursor: None | str
    total: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.job_v2_list_response_dto_items_item import JobV2ListResponseDtoItemsItem # noqa: PLC0415
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
        })
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_v2_list_response_dto_items_item import JobV2ListResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = JobV2ListResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total", UNSET)

        job_v2_list_response_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return job_v2_list_response_dto

