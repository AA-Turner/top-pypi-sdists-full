from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.marketplace_list_response_dto_items_item import MarketplaceListResponseDtoItemsItem





T = TypeVar("T", bound="MarketplaceListResponseDto")



@_attrs_define
class MarketplaceListResponseDto:
    """ Paginated listing of marketplace images.

        Example:
            {'items': [{'id': 'd1effba4-1efa-47b2-8032-d041e3f0d03c', 'imageRepo': 'us-central1-docker.pkg.dev/example-
                project/marketplace/swe-bench-verified', 'description': 'SWE-bench Verified harness image — runs agentic patch-
                and-test rollouts against 500 human-verified GitHub issues.', 'dockerTags': ['latest', 'v1.2.0', 'v1.1.0'],
                'dockerTagsDetail': [{'tag': 'latest', 'sizeBytes': 5368709120, 'pushedAt': '2026-01-16T14:20:00.000Z'}, {'tag':
                'v1.2.0', 'sizeBytes': 5368709120, 'pushedAt': '2026-01-16T14:20:00.000Z'}], 'imageSizeBytes': 10737418240,
                'lastPushedAt': '2026-01-16T14:20:00.000Z', 'registry': 'us-central1-docker.pkg.dev', 'syncedAt':
                '2026-01-16T15:00:00.000Z', 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T15:00:00.000Z'}],
                'total': 1, 'limit': 24, 'offset': 0}

        Attributes:
            items (list[MarketplaceListResponseDtoItemsItem]): Page of marketplace images matching the query.
            total (float): Total number of marketplace images matching the query across all pages. Example: 142.
            limit (float): Maximum number of items returned in this page. Example: 24.
            offset (float): Zero-based offset into the result set used to produce this page. Example: 0.
     """

    items: list[MarketplaceListResponseDtoItemsItem]
    total: float
    limit: float
    offset: float





    def to_dict(self) -> dict[str, Any]:
        from ..models.marketplace_list_response_dto_items_item import MarketplaceListResponseDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        total = self.total

        limit = self.limit

        offset = self.offset


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.marketplace_list_response_dto_items_item import MarketplaceListResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = MarketplaceListResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        total = d.pop("total")

        limit = d.pop("limit")

        offset = d.pop("offset")

        marketplace_list_response_dto = cls(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
        )

        return marketplace_list_response_dto

