from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentQueueInfo")


@_attrs_define
class AgentQueueInfo:
    """
    Attributes:
        name (str): Queue name
        messages (int): Number of messages in queue
        consumers (int): Number of active consumers
        object_type (Union[None, str]): Parsed object type from queue name
    """

    name: str
    messages: int
    consumers: int
    object_type: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        messages = self.messages

        consumers = self.consumers

        object_type: Union[None, str]
        object_type = self.object_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "messages": messages,
                "consumers": consumers,
                "object_type": object_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        messages = d.pop("messages")

        consumers = d.pop("consumers")

        def _parse_object_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        object_type = _parse_object_type(d.pop("object_type"))

        agent_queue_info = cls(
            name=name,
            messages=messages,
            consumers=consumers,
            object_type=object_type,
        )

        agent_queue_info.additional_properties = d
        return agent_queue_info

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
