from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.owned_compute_list_response_dto_items_item import OwnedComputeListResponseDtoItemsItem





T = TypeVar("T", bound="OwnedComputeListResponseDto")



@_attrs_define
class OwnedComputeListResponseDto:
    """ List of computes owned by the caller, scoped by environment or run-config.

        Example:
            {'items': [{'id': 'b394e9de-3306-498a-b9a5-34749b57aaf1', 'name': 'vision-agent-dev', 'status': 'running',
                'errorMessage': None, 'createdAt': '2026-01-15T09:30:00.000Z', 'startedAt': '2026-01-15T09:30:12.000Z',
                'stoppedAt': None, 'containerImage': 'us-docker.pkg.dev/example-project/recursion-agents/vision-agent:1.4.2',
                'pvcSizeGi': 20, 'httpPort': 8080, 'idleStopAfterSeconds': 2592000, 'stoppedDeleteAfterSeconds': 2592000,
                'environmentId': '784e2386-e297-4f9d-a886-838422383b65', 'runConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad', 'runConfigId': '5b1f0e2a-7c3d-4e8f-9a6b-2d4c8e1f3a57',
                'runConfigVersionNumber': 3}]}

        Attributes:
            items (list[OwnedComputeListResponseDtoItemsItem]): Owned computes returned for the caller scope.
     """

    items: list[OwnedComputeListResponseDtoItemsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.owned_compute_list_response_dto_items_item import OwnedComputeListResponseDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.owned_compute_list_response_dto_items_item import OwnedComputeListResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = OwnedComputeListResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        owned_compute_list_response_dto = cls(
            items=items,
        )

        return owned_compute_list_response_dto

