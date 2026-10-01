from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.trigger_type import TriggerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestDestinationRequest")


@_attrs_define
class TestDestinationRequest:
    """
    Attributes:
        trigger (TriggerType): Machine-readable trigger identifier, lower-kebab-case (e.g. 'job-run-failure')
        actor_id (None | str | Unset): Optional user ID who initiated the test for audit trail
    """

    trigger: TriggerType
    actor_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trigger = self.trigger.value

        actor_id: None | str | Unset
        if isinstance(self.actor_id, Unset):
            actor_id = UNSET
        else:
            actor_id = self.actor_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger": trigger,
            }
        )
        if actor_id is not UNSET:
            field_dict["actor_id"] = actor_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        trigger = TriggerType(d.pop("trigger"))

        def _parse_actor_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        actor_id = _parse_actor_id(d.pop("actor_id", UNSET))

        test_destination_request = cls(
            trigger=trigger,
            actor_id=actor_id,
        )

        test_destination_request.additional_properties = d
        return test_destination_request

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
