from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EventSubscriptionRequest")


@_attrs_define
class EventSubscriptionRequest:
    """
    Attributes:
        description (Union[Unset, str]):
        observable_objects (Union[Unset, Any]): List of objects to observe. Each item must have 'object_type' (one of:
            order, user_role, resource, offering_user, importable_resources, service_account, course_account,
            resource_periodic_limits) and optionally 'object_id' (integer). Example: [{"object_type": "resource"},
            {"object_type": "order", "object_id": 123}]
    """

    description: Union[Unset, str] = UNSET
    observable_objects: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        observable_objects = self.observable_objects

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if observable_objects is not UNSET:
            field_dict["observable_objects"] = observable_objects

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        observable_objects = d.pop("observable_objects", UNSET)

        event_subscription_request = cls(
            description=description,
            observable_objects=observable_objects,
        )

        event_subscription_request.additional_properties = d
        return event_subscription_request

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
