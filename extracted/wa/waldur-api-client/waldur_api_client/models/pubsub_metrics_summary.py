from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PubsubMetricsSummary")


@_attrs_define
class PubsubMetricsSummary:
    """
    Attributes:
        messages_sent (int): Total messages sent
        messages_failed (int): Total messages failed
        failure_rate (str): Failure rate as percentage string
        avg_latency_ms (float): Average publish latency in milliseconds
    """

    messages_sent: int
    messages_failed: int
    failure_rate: str
    avg_latency_ms: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        messages_sent = self.messages_sent

        messages_failed = self.messages_failed

        failure_rate = self.failure_rate

        avg_latency_ms = self.avg_latency_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "messages_sent": messages_sent,
                "messages_failed": messages_failed,
                "failure_rate": failure_rate,
                "avg_latency_ms": avg_latency_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        messages_sent = d.pop("messages_sent")

        messages_failed = d.pop("messages_failed")

        failure_rate = d.pop("failure_rate")

        avg_latency_ms = d.pop("avg_latency_ms")

        pubsub_metrics_summary = cls(
            messages_sent=messages_sent,
            messages_failed=messages_failed,
            failure_rate=failure_rate,
            avg_latency_ms=avg_latency_ms,
        )

        pubsub_metrics_summary.additional_properties = d
        return pubsub_metrics_summary

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
