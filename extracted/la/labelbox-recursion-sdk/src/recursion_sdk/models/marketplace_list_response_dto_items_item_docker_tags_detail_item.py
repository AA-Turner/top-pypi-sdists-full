from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="MarketplaceListResponseDtoItemsItemDockerTagsDetailItem")



@_attrs_define
class MarketplaceListResponseDtoItemsItemDockerTagsDetailItem:
    """ Per-tag metadata for a marketplace Docker image.

        Attributes:
            tag (str): Docker image tag name.
            size_bytes (float): Size of this specific tagged image in bytes. Example: 1048576000.
            pushed_at (str): Timestamp when this tag was last pushed to the registry (ISO-8601, UTC).
     """

    tag: str
    size_bytes: float
    pushed_at: str





    def to_dict(self) -> dict[str, Any]:
        tag = self.tag

        size_bytes = self.size_bytes

        pushed_at = self.pushed_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "tag": tag,
            "sizeBytes": size_bytes,
            "pushedAt": pushed_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tag = d.pop("tag")

        size_bytes = d.pop("sizeBytes")

        pushed_at = d.pop("pushedAt")

        marketplace_list_response_dto_items_item_docker_tags_detail_item = cls(
            tag=tag,
            size_bytes=size_bytes,
            pushed_at=pushed_at,
        )

        return marketplace_list_response_dto_items_item_docker_tags_detail_item

