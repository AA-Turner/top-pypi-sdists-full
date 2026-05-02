from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delete_azure_subscription_json_body_azure_mode import DeleteAzureSubscriptionJsonBodyAzureMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteAzureSubscriptionJsonBody")


@_attrs_define
class DeleteAzureSubscriptionJsonBody:
    """
    Attributes:
        azure_mode (DeleteAzureSubscriptionJsonBodyAzureMode): Azure Event Grid trigger mode.
        scope_resource_id (str):
        subscription_name (str):
        topic_name (Union[Unset, None, str]):
    """

    azure_mode: DeleteAzureSubscriptionJsonBodyAzureMode
    scope_resource_id: str
    subscription_name: str
    topic_name: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        azure_mode = self.azure_mode.value

        scope_resource_id = self.scope_resource_id
        subscription_name = self.subscription_name
        topic_name = self.topic_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "azure_mode": azure_mode,
                "scope_resource_id": scope_resource_id,
                "subscription_name": subscription_name,
            }
        )
        if topic_name is not UNSET:
            field_dict["topic_name"] = topic_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        azure_mode = DeleteAzureSubscriptionJsonBodyAzureMode(d.pop("azure_mode"))

        scope_resource_id = d.pop("scope_resource_id")

        subscription_name = d.pop("subscription_name")

        topic_name = d.pop("topic_name", UNSET)

        delete_azure_subscription_json_body = cls(
            azure_mode=azure_mode,
            scope_resource_id=scope_resource_id,
            subscription_name=subscription_name,
            topic_name=topic_name,
        )

        delete_azure_subscription_json_body.additional_properties = d
        return delete_azure_subscription_json_body

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
