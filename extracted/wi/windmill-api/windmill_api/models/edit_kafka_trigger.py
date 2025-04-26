from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EditKafkaTrigger")


@_attrs_define
class EditKafkaTrigger:
    """
    Attributes:
        kafka_resource_path (str):
        group_id (str):
        topics (List[str]):
        path (str):
        script_path (str):
        is_flow (bool):
    """

    kafka_resource_path: str
    group_id: str
    topics: List[str]
    path: str
    script_path: str
    is_flow: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kafka_resource_path = self.kafka_resource_path
        group_id = self.group_id
        topics = self.topics

        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kafka_resource_path": kafka_resource_path,
                "group_id": group_id,
                "topics": topics,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kafka_resource_path = d.pop("kafka_resource_path")

        group_id = d.pop("group_id")

        topics = cast(List[str], d.pop("topics"))

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        edit_kafka_trigger = cls(
            kafka_resource_path=kafka_resource_path,
            group_id=group_id,
            topics=topics,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
        )

        edit_kafka_trigger.additional_properties = d
        return edit_kafka_trigger

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
