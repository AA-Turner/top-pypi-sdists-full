from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAllTGoogleTopicSubscriptionsWithDefaultCredentialsJsonBody")


@_attrs_define
class ListAllTGoogleTopicSubscriptionsWithDefaultCredentialsJsonBody:
    """
    Attributes:
        topic_id (str):
        project_id (Union[Unset, str]):
    """

    topic_id: str
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        topic_id = self.topic_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic_id": topic_id,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        topic_id = d.pop("topic_id")

        project_id = d.pop("project_id", UNSET)

        list_all_t_google_topic_subscriptions_with_default_credentials_json_body = cls(
            topic_id=topic_id,
            project_id=project_id,
        )

        list_all_t_google_topic_subscriptions_with_default_credentials_json_body.additional_properties = d
        return list_all_t_google_topic_subscriptions_with_default_credentials_json_body

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
