import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.pubsub_circuit_breaker_summary import PubsubCircuitBreakerSummary
    from ..models.pubsub_metrics_summary import PubsubMetricsSummary


T = TypeVar("T", bound="PubsubOverview")


@_attrs_define
class PubsubOverview:
    """
    Attributes:
        health_status (str): Overall health: healthy, degraded, or critical
        issues (list[str]): List of current issues affecting health
        circuit_breaker (PubsubCircuitBreakerSummary):
        metrics (PubsubMetricsSummary):
        last_updated (datetime.datetime): Timestamp when overview was generated
    """

    health_status: str
    issues: list[str]
    circuit_breaker: "PubsubCircuitBreakerSummary"
    metrics: "PubsubMetricsSummary"
    last_updated: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        health_status = self.health_status

        issues = self.issues

        circuit_breaker = self.circuit_breaker.to_dict()

        metrics = self.metrics.to_dict()

        last_updated = self.last_updated.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "health_status": health_status,
                "issues": issues,
                "circuit_breaker": circuit_breaker,
                "metrics": metrics,
                "last_updated": last_updated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pubsub_circuit_breaker_summary import PubsubCircuitBreakerSummary
        from ..models.pubsub_metrics_summary import PubsubMetricsSummary

        d = dict(src_dict)
        health_status = d.pop("health_status")

        issues = cast(list[str], d.pop("issues"))

        circuit_breaker = PubsubCircuitBreakerSummary.from_dict(d.pop("circuit_breaker"))

        metrics = PubsubMetricsSummary.from_dict(d.pop("metrics"))

        last_updated = isoparse(d.pop("last_updated"))

        pubsub_overview = cls(
            health_status=health_status,
            issues=issues,
            circuit_breaker=circuit_breaker,
            metrics=metrics,
            last_updated=last_updated,
        )

        pubsub_overview.additional_properties = d
        return pubsub_overview

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
