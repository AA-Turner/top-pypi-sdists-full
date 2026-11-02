from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CommitKafkaOffsetsJsonBody")


@_attrs_define
class CommitKafkaOffsetsJsonBody:
    """
    Attributes:
        topic (str):
        partition (int):
        offset (int):
    """

    topic: str
    partition: int
    offset: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        topic = self.topic
        partition = self.partition
        offset = self.offset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic": topic,
                "partition": partition,
                "offset": offset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        topic = d.pop("topic")

        partition = d.pop("partition")

        offset = d.pop("offset")

        commit_kafka_offsets_json_body = cls(
            topic=topic,
            partition=partition,
            offset=offset,
        )

        commit_kafka_offsets_json_body.additional_properties = d
        return commit_kafka_offsets_json_body

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
