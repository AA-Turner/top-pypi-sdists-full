from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsSandboxProviderStatus")



@_attrs_define
class ManagedAgentsSandboxProviderStatus:
    """ Result of a live connectivity check against a deployment-owned sandbox compute provider. Returned when probing a
    provider, and provisions no billable compute.

        Example:
            {'checked_at': '2026-02-18T09:30:00Z', 'message': 'example', 'provider': 'example', 'status': 'example'}

        Attributes:
            checked_at (datetime.datetime): RFC 3339 timestamp (UTC) of when this check ran. Never cached; each request
                probes live.
            message (str): Operator-facing explanation of the status. Deliberately contains no endpoint or credential
                material.
            provider (str): Sandbox compute provider this status describes, echoed from the request. Connectivity status is
                only available for the agent runner provider ("runs").
            status (str): Outcome of the check: connected (authentication succeeded), misconfigured (no connection
                configured in this deployment), unauthorized (the configured API key was rejected), or unavailable (the runner
                could not be reached).
     """

    checked_at: datetime.datetime
    message: str
    provider: str
    status: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        checked_at = self.checked_at.isoformat()

        message = self.message

        provider = self.provider

        status = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "checked_at": checked_at,
            "message": message,
            "provider": provider,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checked_at = datetime.datetime.fromisoformat(d.pop("checked_at"))




        message = d.pop("message")

        provider = d.pop("provider")

        status = d.pop("status")

        managed_agents_sandbox_provider_status = cls(
            checked_at=checked_at,
            message=message,
            provider=provider,
            status=status,
        )


        managed_agents_sandbox_provider_status.additional_properties = d
        return managed_agents_sandbox_provider_status

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
