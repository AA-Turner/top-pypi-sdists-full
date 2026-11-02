from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.partitions_in_range_partition_kind import PartitionsInRangePartitionKind

if TYPE_CHECKING:
    from ..models.partitions_in_range_partitions_item import PartitionsInRangePartitionsItem


T = TypeVar("T", bound="PartitionsInRange")


@_attrs_define
class PartitionsInRange:
    """
    Attributes:
        producer_path (str): the pipeline script that materializes the asset (managed `// materialize` target, or a
            partitioned writer using the SDK helpers) — the runnable a backfill launches
        partition_kind (PartitionsInRangePartitionKind):
        partitions (List['PartitionsInRangePartitionsItem']):
    """

    producer_path: str
    partition_kind: PartitionsInRangePartitionKind
    partitions: List["PartitionsInRangePartitionsItem"]
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
        from ..models.partitions_in_range_partitions_item import PartitionsInRangePartitionsItem

        d = src_dict.copy()
        producer_path = d.pop("producer_path")

        partition_kind = PartitionsInRangePartitionKind(d.pop("partition_kind"))

        partitions = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = PartitionsInRangePartitionsItem.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        partitions_in_range = cls(
            producer_path=producer_path,
            partition_kind=partition_kind,
            partitions=partitions,
        )

        partitions_in_range.additional_properties = d
        return partitions_in_range

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
