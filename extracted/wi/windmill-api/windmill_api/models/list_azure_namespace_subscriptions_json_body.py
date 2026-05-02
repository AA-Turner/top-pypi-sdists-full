from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListAzureNamespaceSubscriptionsJsonBody")


@_attrs_define
class ListAzureNamespaceSubscriptionsJsonBody:
    """
    Attributes:
        scope_resource_id (str):
        topic_name (str):
    """

    scope_resource_id: str
    topic_name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scope_resource_id = self.scope_resource_id
        topic_name = self.topic_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope_resource_id": scope_resource_id,
                "topic_name": topic_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scope_resource_id = d.pop("scope_resource_id")

        topic_name = d.pop("topic_name")

        list_azure_namespace_subscriptions_json_body = cls(
            scope_resource_id=scope_resource_id,
            topic_name=topic_name,
        )

        list_azure_namespace_subscriptions_json_body.additional_properties = d
        return list_azure_namespace_subscriptions_json_body

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
