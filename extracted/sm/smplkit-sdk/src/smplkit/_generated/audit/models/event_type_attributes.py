from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
import datetime


T = TypeVar("T", bound="EventTypeAttributes")


@_attrs_define
class EventTypeAttributes:
    """
    Attributes:
        event_type (str): The event_type slug. Same as the JSON:API ``id``.
        created_at (datetime.datetime): First sighting of this event_type for the account. When the request includes
            ``filter[resource_type]``, this is the first sighting of the (event_type, resource_type) triple rather than the
            event_type overall.
    """

    event_type: str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_type = self.event_type

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_type": event_type,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        event_type = d.pop("event_type")

        created_at = isoparse(d.pop("created_at"))

        event_type_attributes = cls(
            event_type=event_type,
            created_at=created_at,
        )

        event_type_attributes.additional_properties = d
        return event_type_attributes

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
