from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsCostReceiptRecovery")



@_attrs_define
class ManagedAgentsCostReceiptRecovery:
    """ How a provider receipt was obtained after the original response was lost, so a charge settled out of band is still
    auditable back to the provider.

        Example:
            {'method': 'example', 'recovered_at': '2026-02-18T09:30:00Z', 'reference': 'example'}

        Attributes:
            method (str): How the receipt was recovered: provider_lookup means it was fetched from the provider by request
                id, and idempotent_retry means it came from replaying the call under the attempt's provider idempotency key.
            recovered_at (datetime.datetime): RFC 3339 timestamp of when the receipt was recovered.
            reference (str): Identifier the recovery was keyed on: the receipt's provider_request_id for provider_lookup, or
                the attempt's provider idempotency key for idempotent_retry.
     """

    method: str
    recovered_at: datetime.datetime
    reference: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        method = self.method

        recovered_at = self.recovered_at.isoformat()

        reference = self.reference


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "method": method,
            "recovered_at": recovered_at,
            "reference": reference,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        method = d.pop("method")

        recovered_at = datetime.datetime.fromisoformat(d.pop("recovered_at"))




        reference = d.pop("reference")

        managed_agents_cost_receipt_recovery = cls(
            method=method,
            recovered_at=recovered_at,
            reference=reference,
        )


        managed_agents_cost_receipt_recovery.additional_properties = d
        return managed_agents_cost_receipt_recovery

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
