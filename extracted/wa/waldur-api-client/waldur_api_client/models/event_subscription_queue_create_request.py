from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.observable_object_type_enum import ObservableObjectTypeEnum

T = TypeVar("T", bound="EventSubscriptionQueueCreateRequest")


@_attrs_define
class EventSubscriptionQueueCreateRequest:
    """
    Attributes:
        offering_uuid (UUID): UUID of the offering to receive events for
        object_type (ObservableObjectTypeEnum):
    """

    offering_uuid: UUID
    object_type: ObservableObjectTypeEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        object_type = self.object_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "object_type": object_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        object_type = ObservableObjectTypeEnum(d.pop("object_type"))

        event_subscription_queue_create_request = cls(
            offering_uuid=offering_uuid,
            object_type=object_type,
        )

        event_subscription_queue_create_request.additional_properties = d
        return event_subscription_queue_create_request

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
