from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsRunAutomationRequest")



@_attrs_define
class ManagedAgentsRunAutomationRequest:
    """ Structured input for manually starting an automation without a webhook delivery.

        Example:
            {'idempotency_key': 'example', 'payload': 'example'}

        Attributes:
            payload (Any): Structured event or task input supplied to the agent for this manual run.
            idempotency_key (str | Unset): Caller-chosen key that makes retrying the same manual run safe.
     """

    payload: Any
    idempotency_key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        payload = self.payload

        idempotency_key = self.idempotency_key


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "payload": payload,
        })
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        payload = d.pop("payload")

        idempotency_key = d.pop("idempotency_key", UNSET)

        managed_agents_run_automation_request = cls(
            payload=payload,
            idempotency_key=idempotency_key,
        )


        managed_agents_run_automation_request.additional_properties = d
        return managed_agents_run_automation_request

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
