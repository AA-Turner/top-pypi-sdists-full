from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_mqtt_trigger_subscribe_topics_item_qos import NewMqttTriggerSubscribeTopicsItemQos

T = TypeVar("T", bound="NewMqttTriggerSubscribeTopicsItem")


@_attrs_define
class NewMqttTriggerSubscribeTopicsItem:
    """
    Attributes:
        qos (NewMqttTriggerSubscribeTopicsItemQos):
        topic (str):
    """

    qos: NewMqttTriggerSubscribeTopicsItemQos
    topic: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        qos = self.qos.value

        topic = self.topic

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "qos": qos,
                "topic": topic,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        qos = NewMqttTriggerSubscribeTopicsItemQos(d.pop("qos"))

        topic = d.pop("topic")

        new_mqtt_trigger_subscribe_topics_item = cls(
            qos=qos,
            topic=topic,
        )

        new_mqtt_trigger_subscribe_topics_item.additional_properties = d
        return new_mqtt_trigger_subscribe_topics_item

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
