from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.observable_object_type_enum import ObservableObjectTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentEventSubscriptionCreateRequest")


@_attrs_define
class AgentEventSubscriptionCreateRequest:
    """
    Attributes:
        observable_object_type (ObservableObjectTypeEnum):
        description (Union[Unset, str]): Optional description for the event subscription
    """

    observable_object_type: ObservableObjectTypeEnum
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        observable_object_type = self.observable_object_type.value

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "observable_object_type": observable_object_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        observable_object_type = ObservableObjectTypeEnum(d.pop("observable_object_type"))

        description = d.pop("description", UNSET)

        agent_event_subscription_create_request = cls(
            observable_object_type=observable_object_type,
            description=description,
        )

        agent_event_subscription_create_request.additional_properties = d
        return agent_event_subscription_create_request

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
