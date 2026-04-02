from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.celery_worker_pool_writes import CeleryWorkerPoolWrites


T = TypeVar("T", bound="CeleryWorkerPool")


@_attrs_define
class CeleryWorkerPool:
    """
    Attributes:
        max_concurrency (int): Maximum number of concurrent processes
        processes (list[int]): List of worker process IDs
        max_tasks_per_child (int): Maximum tasks per child process
        put_guarded_by_semaphore (bool):
        timeouts (list[int]): Timeout values
        writes (CeleryWorkerPoolWrites): Write statistics
    """

    max_concurrency: int
    processes: list[int]
    max_tasks_per_child: int
    put_guarded_by_semaphore: bool
    timeouts: list[int]
    writes: "CeleryWorkerPoolWrites"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_concurrency = self.max_concurrency

        processes = self.processes

        max_tasks_per_child = self.max_tasks_per_child

        put_guarded_by_semaphore = self.put_guarded_by_semaphore

        timeouts = self.timeouts

        writes = self.writes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_concurrency": max_concurrency,
                "processes": processes,
                "max_tasks_per_child": max_tasks_per_child,
                "put_guarded_by_semaphore": put_guarded_by_semaphore,
                "timeouts": timeouts,
                "writes": writes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.celery_worker_pool_writes import CeleryWorkerPoolWrites

        d = dict(src_dict)
        max_concurrency = d.pop("max_concurrency")

        processes = cast(list[int], d.pop("processes"))

        max_tasks_per_child = d.pop("max_tasks_per_child")

        put_guarded_by_semaphore = d.pop("put_guarded_by_semaphore")

        timeouts = cast(list[int], d.pop("timeouts"))

        writes = CeleryWorkerPoolWrites.from_dict(d.pop("writes"))

        celery_worker_pool = cls(
            max_concurrency=max_concurrency,
            processes=processes,
            max_tasks_per_child=max_tasks_per_child,
            put_guarded_by_semaphore=put_guarded_by_semaphore,
            timeouts=timeouts,
            writes=writes,
        )

        celery_worker_pool.additional_properties = d
        return celery_worker_pool

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
