from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_asset_partitions_in_range_response_200_partition_kind import (
    ListAssetPartitionsInRangeResponse200PartitionKind,
)

if TYPE_CHECKING:
    from ..models.list_asset_partitions_in_range_response_200_partitions_item import (
        ListAssetPartitionsInRangeResponse200PartitionsItem,
    )


T = TypeVar("T", bound="ListAssetPartitionsInRangeResponse200")


@_attrs_define
class ListAssetPartitionsInRangeResponse200:
    """
    Attributes:
        producer_path (str): the pipeline script that materializes the asset (managed `// materialize` target, or a
            partitioned writer using the SDK helpers) — the runnable a backfill launches
        partition_kind (ListAssetPartitionsInRangeResponse200PartitionKind):
        partitions (List['ListAssetPartitionsInRangeResponse200PartitionsItem']):
    """

    producer_path: str
    partition_kind: ListAssetPartitionsInRangeResponse200PartitionKind
    partitions: List["ListAssetPartitionsInRangeResponse200PartitionsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        producer_path = self.producer_path
        partition_kind = self.partition_kind.value

        partitions = []
        for partitions_item_data in self.partitions:
            partitions_item = partitions_item_data.to_dict()

            partitions.append(partitions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "producer_path": producer_path,
                "partition_kind": partition_kind,
                "partitions": partitions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_asset_partitions_in_range_response_200_partitions_item import (
            ListAssetPartitionsInRangeResponse200PartitionsItem,
        )

        d = src_dict.copy()
        producer_path = d.pop("producer_path")

        partition_kind = ListAssetPartitionsInRangeResponse200PartitionKind(d.pop("partition_kind"))

        partitions = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = ListAssetPartitionsInRangeResponse200PartitionsItem.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        list_asset_partitions_in_range_response_200 = cls(
            producer_path=producer_path,
            partition_kind=partition_kind,
            partitions=partitions,
        )

        list_asset_partitions_in_range_response_200.additional_properties = d
        return list_asset_partitions_in_range_response_200

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
