from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListAllTGoogleTopicSubscriptionsJsonBody")


@_attrs_define
class ListAllTGoogleTopicSubscriptionsJsonBody:
    """
    Attributes:
        topic_id (str):
    """

    topic_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        topic_id = self.topic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic_id": topic_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        topic_id = d.pop("topic_id")

        list_all_t_google_topic_subscriptions_json_body = cls(
            topic_id=topic_id,
        )

        list_all_t_google_topic_subscriptions_json_body.additional_properties = d
        return list_all_t_google_topic_subscriptions_json_body

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
