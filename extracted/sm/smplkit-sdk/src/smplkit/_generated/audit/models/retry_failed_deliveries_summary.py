from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="RetryFailedDeliveriesSummary")


@_attrs_define
class RetryFailedDeliveriesSummary:
    """Counts returned by the retry-failed-deliveries action.

    Attributes:
        attempted (int): Number of failed deliveries that were re-attempted.
        succeeded (int): Number of re-attempts that succeeded.
        failed (int): Number of re-attempts that failed again.
    """

    attempted: int
    succeeded: int
    failed: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempted = self.attempted

        succeeded = self.succeeded

        failed = self.failed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempted": attempted,
                "succeeded": succeeded,
                "failed": failed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempted = d.pop("attempted")

        succeeded = d.pop("succeeded")

        failed = d.pop("failed")

        retry_failed_deliveries_summary = cls(
            attempted=attempted,
            succeeded=succeeded,
            failed=failed,
        )

        retry_failed_deliveries_summary.additional_properties = d
        return retry_failed_deliveries_summary

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
