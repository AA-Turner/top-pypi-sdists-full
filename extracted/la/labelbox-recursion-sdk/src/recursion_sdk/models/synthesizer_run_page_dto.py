from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.synthesizer_run_page_dto_items_item import SynthesizerRunPageDtoItemsItem





T = TypeVar("T", bound="SynthesizerRunPageDto")



@_attrs_define
class SynthesizerRunPageDto:
    """ Cursor-paginated page of synthesizer runs.

        Example:
            {'items': [{'id': 'e6016881-c0b4-4412-92af-c84c3093e770', 'synthesizerJobId':
                'b45c081d-3069-4e32-98d4-aa5ec3d442c6', 'builtInKey': None, 'problemVersionId':
                '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'triggeredByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'status':
                'completed', 'diffPayload': [{'target': 'prompt', 'kind': 'row', 'current': 'Find the defect in the image.',
                'proposed': 'Inspect the product image and report each surface defect with its type and location.', 'canWrite':
                True}], 'appliedTargets': ['prompt'], 'appliedAt': '2026-01-16T15:05:00.000Z', 'appliedByUserId':
                '49dea803-7390-49c4-abb1-5629718fc9cd', 'errorMessage': None, 'startedAt': '2026-01-16T14:50:00.000Z',
                'completedAt': '2026-01-16T14:52:30.000Z', 'createdAt': '2026-01-16T14:49:45.000Z', 'updatedAt':
                '2026-01-16T15:05:00.000Z', 'synthesizerRunConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad',
                'synthesizerRunConfigName': 'claude-sonnet-baseline', 'synthesizerRunConfigVersionNumber': 1}], 'nextCursor':
                None, 'total': 1}

        Attributes:
            items (list[SynthesizerRunPageDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[SynthesizerRunPageDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.synthesizer_run_page_dto_items_item import SynthesizerRunPageDtoItemsItem # noqa: PLC0415
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
        from ..models.synthesizer_run_page_dto_items_item import SynthesizerRunPageDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = SynthesizerRunPageDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        synthesizer_run_page_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return synthesizer_run_page_dto

