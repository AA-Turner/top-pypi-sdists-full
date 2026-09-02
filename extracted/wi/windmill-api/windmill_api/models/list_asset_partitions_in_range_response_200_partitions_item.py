from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_asset_partitions_in_range_response_200_partitions_item_status import (
    ListAssetPartitionsInRangeResponse200PartitionsItemStatus,
)

T = TypeVar("T", bound="ListAssetPartitionsInRangeResponse200PartitionsItem")


@_attrs_define
class ListAssetPartitionsInRangeResponse200PartitionsItem:
    """
    Attributes:
        partition (str):
        status (ListAssetPartitionsInRangeResponse200PartitionsItemStatus):
    """

    partition: str
    status: ListAssetPartitionsInRangeResponse200PartitionsItemStatus
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        partition = self.partition
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partition": partition,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        partition = d.pop("partition")

        status = ListAssetPartitionsInRangeResponse200PartitionsItemStatus(d.pop("status"))

        list_asset_partitions_in_range_response_200_partitions_item = cls(
            partition=partition,
            status=status,
        )

        list_asset_partitions_in_range_response_200_partitions_item.additional_properties = d
        return list_asset_partitions_in_range_response_200_partitions_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
