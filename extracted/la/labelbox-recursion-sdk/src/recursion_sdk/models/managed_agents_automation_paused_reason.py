from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsAutomationPausedReason")



@_attrs_define
class ManagedAgentsAutomationPausedReason:
    """ Why an automation is not firing, and which resource to repair.

        Example:
            {'message': 'example', 'occurred_at': '2026-02-18T09:30:00Z', 'paused_by': 'example', 'reason': 'example',
                'resource_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            occurred_at (datetime.datetime): Server-assigned RFC 3339 instant the pause took effect.
            reason (str): Why the automation stopped firing. paused_by_operator is deliberate; every other value names a
                configuration problem the platform detected while trying to start a run.
            message (str | Unset): Human-readable detail, safe to show an operator.
            paused_by (str | Unset): Authenticated principal, when a person paused it.
            resource_id (str | Unset): Identifier of the resource that could not be resolved, when the reason names one. The
                console deep-links to it.
            run_id (str | Unset): Run whose failure caused the pause, when one did.
     """

    occurred_at: datetime.datetime
    reason: str
    message: str | Unset = UNSET
    paused_by: str | Unset = UNSET
    resource_id: str | Unset = UNSET
    run_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        occurred_at = self.occurred_at.isoformat()

        reason = self.reason

        message = self.message

        paused_by = self.paused_by

        resource_id = self.resource_id

        run_id = self.run_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "occurred_at": occurred_at,
            "reason": reason,
        })
        if message is not UNSET:
            field_dict["message"] = message
        if paused_by is not UNSET:
            field_dict["paused_by"] = paused_by
        if resource_id is not UNSET:
            field_dict["resource_id"] = resource_id
        if run_id is not UNSET:
            field_dict["run_id"] = run_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        occurred_at = datetime.datetime.fromisoformat(d.pop("occurred_at"))




        reason = d.pop("reason")

        message = d.pop("message", UNSET)

        paused_by = d.pop("paused_by", UNSET)

        resource_id = d.pop("resource_id", UNSET)

        run_id = d.pop("run_id", UNSET)

        managed_agents_automation_paused_reason = cls(
            occurred_at=occurred_at,
            reason=reason,
            message=message,
            paused_by=paused_by,
            resource_id=resource_id,
            run_id=run_id,
        )


        managed_agents_automation_paused_reason.additional_properties = d
        return managed_agents_automation_paused_reason

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
