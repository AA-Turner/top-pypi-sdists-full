from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsTrigger")



@_attrs_define
class ManagedAgentsTrigger:
    """ Why one repository automation ran. Webhook provenance is recorded without persisting the provider's raw payload; a
    manual run carries the mode alone and no provenance fields at all.

        Example:
            {'binding_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'delivery_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'event': 'example', 'mode': 'example'}

        Attributes:
            mode (str): How the automation started: manual for a direct API call, webhook for a verified provider delivery.
                A run recorded before triggers were tracked reads back as manual.
            binding_id (str | Unset): Trigger binding (UUID) that selected this run. Present only on a webhook trigger,
                where it is required.
            delivery_id (str | Unset): Provider delivery id, which ties the GitHub delivery, this session, and the published
                review to one another. Present only on a webhook trigger, where it is required.
            event (str | Unset): Provider event that started the run, e.g. pull_request.synchronize. Present only on a
                webhook trigger, where it is required.
     """

    mode: str
    binding_id: str | Unset = UNSET
    delivery_id: str | Unset = UNSET
    event: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mode = self.mode

        binding_id = self.binding_id

        delivery_id = self.delivery_id

        event = self.event


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
        })
        if binding_id is not UNSET:
            field_dict["binding_id"] = binding_id
        if delivery_id is not UNSET:
            field_dict["delivery_id"] = delivery_id
        if event is not UNSET:
            field_dict["event"] = event

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = d.pop("mode")

        binding_id = d.pop("binding_id", UNSET)

        delivery_id = d.pop("delivery_id", UNSET)

        event = d.pop("event", UNSET)

        managed_agents_trigger = cls(
            mode=mode,
            binding_id=binding_id,
            delivery_id=delivery_id,
            event=event,
        )


        managed_agents_trigger.additional_properties = d
        return managed_agents_trigger

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
