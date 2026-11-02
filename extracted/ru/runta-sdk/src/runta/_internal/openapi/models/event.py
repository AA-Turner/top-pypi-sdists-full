from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Event")


@_attrs_define
class Event:
    """
    Attributes:
        id (str):
        runtime_id (str):
        kind (str):
        payload (Any):
        occurred_at_unix_millis (int):
    """

    id: str
    runtime_id: str
    kind: str
    payload: Any
    occurred_at_unix_millis: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        runtime_id = self.runtime_id

        kind = self.kind

        payload = self.payload

        occurred_at_unix_millis = self.occurred_at_unix_millis

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "runtime_id": runtime_id,
                "kind": kind,
                "payload": payload,
                "occurred_at_unix_millis": occurred_at_unix_millis,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        runtime_id = d.pop("runtime_id")

        kind = d.pop("kind")

        payload = d.pop("payload")

        occurred_at_unix_millis = d.pop("occurred_at_unix_millis")

        event = cls(
            id=id,
            runtime_id=runtime_id,
            kind=kind,
            payload=payload,
            occurred_at_unix_millis=occurred_at_unix_millis,
        )

        event.additional_properties = d
        return event

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
