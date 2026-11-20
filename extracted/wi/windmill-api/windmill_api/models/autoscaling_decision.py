import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.autoscaling_decision_jobs_waiting import AutoscalingDecisionJobsWaiting


T = TypeVar("T", bound="AutoscalingDecision")


@_attrs_define
class AutoscalingDecision:
    """
    Attributes:
        recorded_at (datetime.datetime):
        worker_count (int):
        jobs_waiting (AutoscalingDecisionJobsWaiting):
        decision (str):
        occupancy_rate_15s (Union[Unset, None, float]):
        occupancy_rate_5m (Union[Unset, None, float]):
        occupancy_rate_30m (Union[Unset, None, float]):
    """

    recorded_at: datetime.datetime
    worker_count: int
    jobs_waiting: "AutoscalingDecisionJobsWaiting"
    decision: str
    occupancy_rate_15s: Union[Unset, None, float] = UNSET
    occupancy_rate_5m: Union[Unset, None, float] = UNSET
    occupancy_rate_30m: Union[Unset, None, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        recorded_at = self.recorded_at.isoformat()

        worker_count = self.worker_count
        jobs_waiting = self.jobs_waiting.to_dict()

        decision = self.decision
        occupancy_rate_15s = self.occupancy_rate_15s
        occupancy_rate_5m = self.occupancy_rate_5m
        occupancy_rate_30m = self.occupancy_rate_30m

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recorded_at": recorded_at,
                "worker_count": worker_count,
                "jobs_waiting": jobs_waiting,
                "decision": decision,
            }
        )
        if occupancy_rate_15s is not UNSET:
            field_dict["occupancy_rate_15s"] = occupancy_rate_15s
        if occupancy_rate_5m is not UNSET:
            field_dict["occupancy_rate_5m"] = occupancy_rate_5m
        if occupancy_rate_30m is not UNSET:
            field_dict["occupancy_rate_30m"] = occupancy_rate_30m

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.autoscaling_decision_jobs_waiting import AutoscalingDecisionJobsWaiting

        d = src_dict.copy()
        recorded_at = isoparse(d.pop("recorded_at"))

        worker_count = d.pop("worker_count")

        jobs_waiting = AutoscalingDecisionJobsWaiting.from_dict(d.pop("jobs_waiting"))

        decision = d.pop("decision")

        occupancy_rate_15s = d.pop("occupancy_rate_15s", UNSET)

        occupancy_rate_5m = d.pop("occupancy_rate_5m", UNSET)

        occupancy_rate_30m = d.pop("occupancy_rate_30m", UNSET)

        autoscaling_decision = cls(
            recorded_at=recorded_at,
            worker_count=worker_count,
            jobs_waiting=jobs_waiting,
            decision=decision,
            occupancy_rate_15s=occupancy_rate_15s,
            occupancy_rate_5m=occupancy_rate_5m,
            occupancy_rate_30m=occupancy_rate_30m,
        )

        autoscaling_decision.additional_properties = d
        return autoscaling_decision

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
