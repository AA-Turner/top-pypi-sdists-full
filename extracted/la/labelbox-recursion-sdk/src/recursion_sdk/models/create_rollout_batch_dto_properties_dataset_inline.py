from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_rollout_batch_dto_properties_dataset_inline_kind import CreateRolloutBatchDtoPropertiesDatasetInlineKind
from typing import cast

if TYPE_CHECKING:
  from ..models.create_rollout_batch_dto_properties_dataset_inline_items_item import CreateRolloutBatchDtoPropertiesDatasetInlineItemsItem





T = TypeVar("T", bound="CreateRolloutBatchDtoPropertiesDatasetInline")



@_attrs_define
class CreateRolloutBatchDtoPropertiesDatasetInline:
    """ 
        Attributes:
            kind (CreateRolloutBatchDtoPropertiesDatasetInlineKind): Dataset items embedded directly in the payload.
            items (list[CreateRolloutBatchDtoPropertiesDatasetInlineItemsItem]): Materialized dataset items (M). Also the
                required shape of a fileRef dataset file: a JSON array of item records.
     """

    kind: CreateRolloutBatchDtoPropertiesDatasetInlineKind
    items: list[CreateRolloutBatchDtoPropertiesDatasetInlineItemsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_rollout_batch_dto_properties_dataset_inline_items_item import CreateRolloutBatchDtoPropertiesDatasetInlineItemsItem # noqa: PLC0415
        kind = self.kind.value

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "items": items,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_rollout_batch_dto_properties_dataset_inline_items_item import CreateRolloutBatchDtoPropertiesDatasetInlineItemsItem # noqa: PLC0415
        d = dict(src_dict)
        kind = CreateRolloutBatchDtoPropertiesDatasetInlineKind(d.pop("kind"))




        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = CreateRolloutBatchDtoPropertiesDatasetInlineItemsItem.from_dict(items_item_data)



            items.append(items_item)


        create_rollout_batch_dto_properties_dataset_inline = cls(
            kind=kind,
            items=items,
        )

        return create_rollout_batch_dto_properties_dataset_inline

