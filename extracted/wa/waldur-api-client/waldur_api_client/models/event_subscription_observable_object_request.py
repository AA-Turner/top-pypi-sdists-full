from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EventSubscriptionObservableObjectRequest")


@_attrs_define
class EventSubscriptionObservableObjectRequest:
    """
    Attributes:
        object_type (str):
        offering_uuid (Union[Unset, UUID]):
        object_id (Union[Unset, int]):
    """

    object_type: str
    offering_uuid: Union[Unset, UUID] = UNSET
    object_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_type = self.object_type

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        object_id = self.object_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object_type": object_type,
            }
        )
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if object_id is not UNSET:
            field_dict["object_id"] = object_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_type = d.pop("object_type")

        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        object_id = d.pop("object_id", UNSET)

        event_subscription_observable_object_request = cls(
            object_type=object_type,
            offering_uuid=offering_uuid,
            object_id=object_id,
        )

        event_subscription_observable_object_request.additional_properties = d
        return event_subscription_observable_object_request

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
