from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TokenSavingsSummary")


@_attrs_define
class TokenSavingsSummary:
    """Totals over everything the filter selects, not merely the page returned.

    Attributes:
        applied_events (int):
        saved_wire_bytes (int):
        saved_estimated_tokens (int):
        malformed_events (int):
    """

    applied_events: int
    saved_wire_bytes: int
    saved_estimated_tokens: int
    malformed_events: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        applied_events = self.applied_events

        saved_wire_bytes = self.saved_wire_bytes

        saved_estimated_tokens = self.saved_estimated_tokens

        malformed_events = self.malformed_events

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "applied_events": applied_events,
                "saved_wire_bytes": saved_wire_bytes,
                "saved_estimated_tokens": saved_estimated_tokens,
                "malformed_events": malformed_events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        applied_events = d.pop("applied_events")

        saved_wire_bytes = d.pop("saved_wire_bytes")

        saved_estimated_tokens = d.pop("saved_estimated_tokens")

        malformed_events = d.pop("malformed_events")

        token_savings_summary = cls(
            applied_events=applied_events,
            saved_wire_bytes=saved_wire_bytes,
            saved_estimated_tokens=saved_estimated_tokens,
            malformed_events=malformed_events,
        )

        token_savings_summary.additional_properties = d
        return token_savings_summary

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
