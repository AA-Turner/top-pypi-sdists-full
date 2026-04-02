from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.celery_broker import CeleryBroker
    from ..models.celery_worker_pool import CeleryWorkerPool
    from ..models.celery_worker_stats_rusage import CeleryWorkerStatsRusage
    from ..models.celery_worker_stats_total import CeleryWorkerStatsTotal


T = TypeVar("T", bound="CeleryWorkerStats")


@_attrs_define
class CeleryWorkerStats:
    """
    Attributes:
        broker (CeleryBroker):
        clock (str): Logical clock value
        uptime (float): Worker uptime in seconds
        pid (int): Worker process ID
        pool (CeleryWorkerPool):
        prefetch_count (int): Number of tasks prefetched
        rusage (CeleryWorkerStatsRusage): Resource usage statistics
        total (CeleryWorkerStatsTotal): Total task counts by type
    """

    broker: "CeleryBroker"
    clock: str
    uptime: float
    pid: int
    pool: "CeleryWorkerPool"
    prefetch_count: int
    rusage: "CeleryWorkerStatsRusage"
    total: "CeleryWorkerStatsTotal"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        broker = self.broker.to_dict()

        clock = self.clock

        uptime = self.uptime

        pid = self.pid

        pool = self.pool.to_dict()

        prefetch_count = self.prefetch_count

        rusage = self.rusage.to_dict()

        total = self.total.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "broker": broker,
                "clock": clock,
                "uptime": uptime,
                "pid": pid,
                "pool": pool,
                "prefetch_count": prefetch_count,
                "rusage": rusage,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.celery_broker import CeleryBroker
        from ..models.celery_worker_pool import CeleryWorkerPool
        from ..models.celery_worker_stats_rusage import CeleryWorkerStatsRusage
        from ..models.celery_worker_stats_total import CeleryWorkerStatsTotal

        d = dict(src_dict)
        broker = CeleryBroker.from_dict(d.pop("broker"))

        clock = d.pop("clock")

        uptime = d.pop("uptime")

        pid = d.pop("pid")

        pool = CeleryWorkerPool.from_dict(d.pop("pool"))

        prefetch_count = d.pop("prefetch_count")

        rusage = CeleryWorkerStatsRusage.from_dict(d.pop("rusage"))

        total = CeleryWorkerStatsTotal.from_dict(d.pop("total"))

        celery_worker_stats = cls(
            broker=broker,
            clock=clock,
            uptime=uptime,
            pid=pid,
            pool=pool,
            prefetch_count=prefetch_count,
            rusage=rusage,
            total=total,
        )

        celery_worker_stats.additional_properties = d
        return celery_worker_stats

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
