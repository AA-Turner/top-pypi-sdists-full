from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PublishingMetrics")


@_attrs_define
class PublishingMetrics:
    """
    Attributes:
        messages_sent (int): Total messages successfully sent
        messages_failed (int): Total failed message attempts
        messages_retried (int): Messages that required retry
        messages_skipped (int): Messages skipped due to circuit breaker
        circuit_breaker_trips (int): Number of times circuit breaker opened
        rate_limiter_rejections (int): Messages rejected by rate limiter
        avg_publish_time_ms (float): Average message publish latency in milliseconds
        last_publish_time (Union[None, float]): Unix timestamp of last publish attempt
    """

    messages_sent: int
    messages_failed: int
    messages_retried: int
    messages_skipped: int
    circuit_breaker_trips: int
    rate_limiter_rejections: int
    avg_publish_time_ms: float
    last_publish_time: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        messages_sent = self.messages_sent

        messages_failed = self.messages_failed

        messages_retried = self.messages_retried

        messages_skipped = self.messages_skipped

        circuit_breaker_trips = self.circuit_breaker_trips

        rate_limiter_rejections = self.rate_limiter_rejections

        avg_publish_time_ms = self.avg_publish_time_ms

        last_publish_time: Union[None, float]
        last_publish_time = self.last_publish_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "messages_sent": messages_sent,
                "messages_failed": messages_failed,
                "messages_retried": messages_retried,
                "messages_skipped": messages_skipped,
                "circuit_breaker_trips": circuit_breaker_trips,
                "rate_limiter_rejections": rate_limiter_rejections,
                "avg_publish_time_ms": avg_publish_time_ms,
                "last_publish_time": last_publish_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        messages_sent = d.pop("messages_sent")

        messages_failed = d.pop("messages_failed")

        messages_retried = d.pop("messages_retried")

        messages_skipped = d.pop("messages_skipped")

        circuit_breaker_trips = d.pop("circuit_breaker_trips")

        rate_limiter_rejections = d.pop("rate_limiter_rejections")

        avg_publish_time_ms = d.pop("avg_publish_time_ms")

        def _parse_last_publish_time(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        last_publish_time = _parse_last_publish_time(d.pop("last_publish_time"))

        publishing_metrics = cls(
            messages_sent=messages_sent,
            messages_failed=messages_failed,
            messages_retried=messages_retried,
            messages_skipped=messages_skipped,
            circuit_breaker_trips=circuit_breaker_trips,
            rate_limiter_rejections=rate_limiter_rejections,
            avg_publish_time_ms=avg_publish_time_ms,
            last_publish_time=last_publish_time,
        )

        publishing_metrics.additional_properties = d
        return publishing_metrics

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
