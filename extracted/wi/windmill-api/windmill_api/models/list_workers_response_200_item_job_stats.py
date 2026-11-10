from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_workers_response_200_item_job_stats_last_24h import ListWorkersResponse200ItemJobStatsLast24H
    from ..models.list_workers_response_200_item_job_stats_last_100 import ListWorkersResponse200ItemJobStatsLast100
    from ..models.list_workers_response_200_item_job_stats_total import ListWorkersResponse200ItemJobStatsTotal


T = TypeVar("T", bound="ListWorkersResponse200ItemJobStats")


@_attrs_define
class ListWorkersResponse200ItemJobStats:
    """script and flow-step jobs this worker ran and how many of them failed, over its whole life, the last 24 hours and
    its last 100 jobs. A flow's own outcome is not counted, since its failure is that of a step already counted on the
    worker that ran it. Canceled jobs count as executed, not failed.

        Attributes:
            total (ListWorkersResponse200ItemJobStatsTotal):
            last_24h (ListWorkersResponse200ItemJobStatsLast24H):
            last_100 (ListWorkersResponse200ItemJobStatsLast100):
    """

    total: "ListWorkersResponse200ItemJobStatsTotal"
    last_24h: "ListWorkersResponse200ItemJobStatsLast24H"
    last_100: "ListWorkersResponse200ItemJobStatsLast100"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total = self.total.to_dict()

        last_24h = self.last_24h.to_dict()

        last_100 = self.last_100.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "last_24h": last_24h,
                "last_100": last_100,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_workers_response_200_item_job_stats_last_24h import ListWorkersResponse200ItemJobStatsLast24H
        from ..models.list_workers_response_200_item_job_stats_last_100 import ListWorkersResponse200ItemJobStatsLast100
        from ..models.list_workers_response_200_item_job_stats_total import ListWorkersResponse200ItemJobStatsTotal

        d = src_dict.copy()
        total = ListWorkersResponse200ItemJobStatsTotal.from_dict(d.pop("total"))

        last_24h = ListWorkersResponse200ItemJobStatsLast24H.from_dict(d.pop("last_24h"))

        last_100 = ListWorkersResponse200ItemJobStatsLast100.from_dict(d.pop("last_100"))

        list_workers_response_200_item_job_stats = cls(
            total=total,
            last_24h=last_24h,
            last_100=last_100,
        )

        list_workers_response_200_item_job_stats.additional_properties = d
        return list_workers_response_200_item_job_stats

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
